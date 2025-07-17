from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.scanner.models import FileTree
from backend.api.serializers import FileTreeSerializer
from backend.scanner.tasks import scan_directory
from django.utils.timezone import now

scan_status = {"running": False, "last_updated": None}


@api_view(["POST"])
def trigger_scan(request):
    if scan_status["running"]:
        return Response({"message": "Scan already in progress"}, status=400)

    scan_status["running"] = True
    scan_status["last_updated"] = None

    # 你也可以用 Celery 异步，这里用同步方式
    scan_directory()
    scan_status["running"] = False
    scan_status["last_updated"] = now()

    return Response({"message": "Scan complete"})


@api_view(["GET"])
def scan_result(request):
    queryset = FileTree.objects.all().order_by("-scanned_at")
    serializer = FileTreeSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def scan_status_view(request):
    return Response({
        "running": scan_status["running"],
        "last_updated": scan_status["last_updated"]
    })
