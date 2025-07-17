import os
import datetime
from django.conf import settings
from backend.utils.path_utils import generate_path_hash
from backend.scanner.models import FileTree
from backend.utils.time_utils import safe_aware


def scan_directory(root_path=None, scan_hidden=False):
    """
    扫描指定路径下的所有目录与文件，并写入或更新数据库中的 FileTree 表。

    参数：
    - root_path: 可选，扫描起始根路径。默认读取 settings.DEFAULT_SCAN_ROOT
    - scan_hidden: 可选，是否扫描隐藏文件。默认读取 settings.SCAN_HIDDEN
    """
    print(f"DEFAULT_SCAN_ROOT = {settings.DEFAULT_SCAN_ROOT}")
    print(f"SCAN_HIDDEN = {settings.SCAN_HIDDEN}")

    # 如果未传入参数，则使用 settings 中的默认值
    root = root_path or settings.DEFAULT_SCAN_ROOT
    scan_hidden = scan_hidden or settings.SCAN_HIDDEN

    # 使用 os.walk 遍历整个目录结构（包含所有子目录）
    for dirpath, dirnames, filenames in os.walk(root):
        # 过滤隐藏的目录和文件（以 "." 开头）
        if not scan_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            filenames = [f for f in filenames if not f.startswith('.')]

        # 处理当前目录本身（写入 FileTree 表）
        create_or_update_file(dirpath, is_directory=True)

        # 遍历并处理当前目录下所有文件
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            create_or_update_file(filepath, is_directory=False)


def create_or_update_file(path, is_directory):
    """
    将单个文件或目录写入数据库，如果已存在则更新其信息。

    参数：
    - path: 完整文件或目录路径
    - is_directory: 是否为目录，True 表示是目录，False 表示是文件
    """
    try:
        # 使用 os.stat 获取文件状态（大小、修改时间等）
        stat = os.stat(path)
    except FileNotFoundError:
        # 文件可能被删除或权限问题，跳过该文件
        return

    # 获取父路径（用于构建目录层级）
    parent_path = os.path.dirname(path)

    # 构建哈希
    path_hash = generate_path_hash(path)
    parent_path_hash = generate_path_hash(parent_path)

    # 构建数据库写入字段
    defaults = {
        'name': os.path.basename(path),
        'parent_path': parent_path if parent_path != path else None,
        'parent_path_hash': parent_path_hash,
        'type': 'directory' if is_directory else 'file',
        'size': 0 if is_directory else stat.st_size,
        'modified_at': safe_aware(datetime.datetime.fromtimestamp(stat.st_mtime)),
        'path': path,  # 如果 path 可更新
    }

    # 写入数据库（用 path_hash 唯一索引查找）
    FileTree.objects.update_or_create(
        path_hash=path_hash,
        defaults=defaults
    )
