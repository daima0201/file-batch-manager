from django.contrib.auth import get_user_model
from rest_framework import serializers
from backend.scanner.models import FileTree
from backend.operations.models import OperationLog

User = get_user_model()


class FileTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTree
        fields = '__all__'


class OperationLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = OperationLog
        fields = '__all__'
