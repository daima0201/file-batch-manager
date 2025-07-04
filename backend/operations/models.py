from django.db import models
from django.contrib.auth import get_user_model
from scanner.models import FileTree

User = get_user_model()


class OperationLog(models.Model):
    ACTION_CHOICES = [
        ('scan', 'Scan'),
        ('delete', 'Delete'),
        ('move', 'Move'),
        ('rename', 'Rename'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target = models.CharField(max_length=4096, null=True, blank=True)
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} by {self.user} at {self.created_at}"