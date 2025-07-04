import os
import time

from django.conf import settings

from .models import FileTree


def scan_directory(root_path=None, scan_hidden=False):
    root = root_path or settings.DEFAULT_SCAN_ROOT
    scan_hidden = scan_hidden or settings.SCAN_HIDDEN

    for dirpath, dirnames, filenames in os.walk(root):
        # 过滤隐藏目录
        if not scan_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            filenames = [f for f in filenames if not f.startswith('.')]

        # 处理当前目录
        create_or_update_file(dirpath, is_directory=True)

        # 处理文件
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            create_or_update_file(filepath, is_directory=False)


def create_or_update_file(path, is_directory):
    try:
        stat = os.stat(path)
    except FileNotFoundError:
        return  # 文件可能已被删除

    parent_path = os.path.dirname(path)

    defaults = {
        'name': os.path.basename(path),
        'parent_path': parent_path if parent_path != path else None,
        'type': 'directory' if is_directory else 'file',
        'size': 0 if is_directory else stat.st_size,
        'modified_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
    }

    FileTree.objects.update_or_create(
        path=path,
        defaults=defaults
    )