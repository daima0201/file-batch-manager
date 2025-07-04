from django.db import models


class FileTree(models.Model):
    TYPE_CHOICES = [
        ('file', 'File'),
        ('directory', 'Directory'),
    ]

    path = models.CharField(max_length=4096, unique=True)
    name = models.CharField(max_length=255)
    parent_path = models.CharField(max_length=4096, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    size = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['path']),
            models.Index(fields=['parent_path']),
        ]

    def __str__(self):
        return self.path
