from django.contrib.auth import get_user_model
from operations.models import OperationLog
from rest_framework import serializers
from scanner.models import FileTree

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