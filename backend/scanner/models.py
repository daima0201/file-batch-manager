from django.db import models


class FileTree(models.Model):
    # 文件或目录类型的可选值
    TYPE_CHOICES = [
        ('file', 'File'),  # 文件
        ('directory', 'Directory')  # 目录
    ]

    # 使用自动递增的 ID，作为主键（默认即可）
    path_id = models.BigAutoField(primary_key=True)
    # 文件或目录的绝对路径（唯一）
    path = models.TextField()
    # 给每个路径一个唯一 hash 编号（可选）
    path_hash = models.CharField(max_length=64, unique=True)
    # 文件或目录的名称（不包含路径）
    name = models.CharField(max_length=255)
    # 上级目录的路径（根目录则为 null）
    parent_path = models.TextField(null=True, blank=True)
    # 给每个父路径一个唯一 hash 编号
    parent_path_hash = models.CharField(max_length=64, null=True, blank=True)
    # 类型（file 或 directory）
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    # 文件大小（单位：字节；目录默认为 null）
    size = models.BigIntegerField(null=True, blank=True)
    # 创建时间（自动记录）
    created_at = models.DateTimeField(auto_now_add=True)
    # 修改时间（可选，通常由扫描脚本写入）
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'file_tree_list'  # ✅ 表名设置
        # 添加索引以提高查询性能（如根据路径或父路径查找）
        indexes = [
            models.Index(fields=['path_hash']),
        ]

    def __str__(self):
        # 显示在 admin 或 shell 中时的文本表示
        return self.path
