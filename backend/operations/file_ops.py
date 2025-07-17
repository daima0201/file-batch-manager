import os
import shutil
from backend.scanner.models import FileTree
from .models import OperationLog


def delete_files(file_ids, user):
    deleted = 0
    errors = []
    operation_details = []

    for file_id in file_ids:
        try:
            file = FileTree.objects.get(id=file_id)
            if file.type == 'directory':
                shutil.rmtree(file.path)
            else:
                os.remove(file.path)

            file.delete()
            deleted += 1
            operation_details.append({
                'id': file_id,
                'path': file.path,
                'status': 'success'
            })
        except FileTree.DoesNotExist:
            errors.append(f"文件ID {file_id} 不存在")
            operation_details.append({
                'id': file_id,
                'status': 'error',
                'message': '文件不存在'
            })
        except Exception as e:
            errors.append(f"删除失败: {file.path if 'file' in locals() else file_id} - {str(e)}")
            operation_details.append({
                'id': file_id,
                'path': file.path if 'file' in locals() else '',
                'status': 'error',
                'message': str(e)
            })

    # 记录操作日志
    if file_ids:
        OperationLog.objects.create(
            user=user,
            action='delete',
            details={
                'total': len(file_ids),
                'success': deleted,
                'errors': errors,
                'details': operation_details
            }
        )

    return deleted, errors


def move_files(file_ids, target_dir, user):
    moved = 0
    errors = []
    operation_details = []

    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    for file_id in file_ids:
        try:
            file = FileTree.objects.get(id=file_id)
            new_path = os.path.join(target_dir, file.name)

            # 移动文件
            shutil.move(file.path, new_path)

            # 更新数据库
            file.path = new_path
            file.parent_path = target_dir
            file.save()

            moved += 1
            operation_details.append({
                'id': file_id,
                'old_path': file.path,
                'new_path': new_path,
                'status': 'success'
            })
        except FileTree.DoesNotExist:
            errors.append(f"文件ID {file_id} 不存在")
            operation_details.append({
                'id': file_id,
                'status': 'error',
                'message': '文件不存在'
            })
        except Exception as e:
            errors.append(f"移动失败: {file.path if 'file' in locals() else file_id} -> {target_dir} - {str(e)}")
            operation_details.append({
                'id': file_id,
                'path': file.path if 'file' in locals() else '',
                'status': 'error',
                'message': str(e)
            })

    # 记录操作日志
    if file_ids:
        OperationLog.objects.create(
            user=user,
            action='move',
            target=target_dir,
            details={
                'total': len(file_ids),
                'success': moved,
                'errors': errors,
                'details': operation_details
            }
        )

    return moved, errors


def rename_file(file_id, new_name, user):
    try:
        file = FileTree.objects.get(id=file_id)
        parent_dir = os.path.dirname(file.path)
        new_path = os.path.join(parent_dir, new_name)

        # 重命名文件
        os.rename(file.path, new_path)

        # 更新数据库
        file.path = new_path
        file.name = new_name
        file.save()

        # 记录操作日志
        OperationLog.objects.create(
            user=user,
            action='rename',
            target=file.path,
            details={
                'old_name': file.name,
                'new_name': new_name,
                'old_path': file.path,
                'new_path': new_path
            }
        )

        return True, "重命名成功"
    except FileTree.DoesNotExist:
        return False, "文件不存在"
    except Exception as e:
        return False, f"重命名失败: {str(e)}"
