from django.conf import settings
from django.contrib.auth import get_user_model
from operations.models import OperationLog
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from scanner.models import FileTree

from .serializers import FileTreeSerializer, OperationLogSerializer

User = get_user_model()


class FileTreeViewSet(viewsets.ModelViewSet):
    queryset = FileTree.objects.all()
    serializer_class = FileTreeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        parent_path = self.request.query_params.get('parent_path', None)

        if parent_path:
            return queryset.filter(parent_path=parent_path)
        return queryset.filter(parent_path__isnull=True)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response([])
        files = FileTree.objects.filter(name__icontains=query)[:50]
        serializer = self.get_serializer(files, many=True)
        return Response(serializer.data)


class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OperationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OperationLog.objects.filter(user=self.request.user).order_by('-created_at')


class ScanViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        root_path = request.data.get('root_path', None)
        scan_hidden = request.data.get('scan_hidden', False)

        from scanner.tasks import scan_directory
        try:
            scan_directory(root_path, scan_hidden)
            # 记录操作日志
            OperationLog.objects.create(
                user=request.user,
                action='scan',
                target=root_path or settings.DEFAULT_SCAN_ROOT,
                details={'scan_hidden': scan_hidden}
            )
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileOperationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def delete_files(self, request):
        file_ids = request.data.get('file_ids', [])
        from operations.file_ops import delete_files
        deleted, errors = delete_files(file_ids, request.user)
        return Response({
            'status': 'success',
            'deleted': deleted,
            'errors': errors
        })

    @action(detail=False, methods=['post'])
    def move_files(self, request):
        file_ids = request.data.get('file_ids', [])
        target_dir = request.data.get('target_dir', '')
        from operations.file_ops import move_files
        moved, errors = move_files(file_ids, target_dir, request.user)
        return Response({
            'status': 'success',
            'moved': moved,
            'errors': errors
        })

    @action(detail=False, methods=['post'])
    def rename_file(self, request):
        file_id = request.data.get('file_id')
        new_name = request.data.get('new_name')
        from operations.file_ops import rename_file
        success, message = rename_file(file_id, new_name, request.user)
        return Response({
            'status': 'success' if success else 'error',
            'message': message
        })