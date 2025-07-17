import hashlib


def generate_path_hash(path: str) -> str:
    """
    生成路径的 SHA256 哈希（64 字符十六进制字符串）
    """
    return hashlib.sha256(path.encode('utf-8')).hexdigest()
