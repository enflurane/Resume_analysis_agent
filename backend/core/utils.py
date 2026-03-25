from typing import Dict, Any, Optional
import hashlib

def generate_key(data: Any) -> str:
    """生成缓存键"""
    if isinstance(data, (dict, list)):
        data_str = str(data)
    else:
        data_str = str(data)
    return hashlib.md5(data_str.encode()).hexdigest()

def safe_extract(data: Dict[str, Any], keys: List[str], default: Any = None) -> Dict[str, Any]:
    """安全提取字典中的键值"""
    result = {}
    for key in keys:
        result[key] = data.get(key, default)
    return result
