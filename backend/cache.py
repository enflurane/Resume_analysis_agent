import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class Cache:
    def __init__(self, expiration_seconds: int = 3600):
        """初始化缓存
        
        Args:
            expiration_seconds: 缓存过期时间（秒），默认1小时
        """
        self.cache = {}
        self.expiration_seconds = expiration_seconds
    
    def _generate_key(self, data: Any) -> str:
        """生成缓存键
        
        Args:
            data: 要缓存的数据
        
        Returns:
            str: 缓存键
        """
        if isinstance(data, bytes):
            return hashlib.md5(data).hexdigest()
        elif isinstance(data, str):
            return hashlib.md5(data.encode('utf-8')).hexdigest()
        else:
            return hashlib.md5(json.dumps(data, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存
        
        Args:
            key: 缓存键
        
        Returns:
            Any: 缓存的数据，如果不存在或已过期则返回None
        """
        if key not in self.cache:
            return None
        
        cached_data, timestamp = self.cache[key]
        
        # 检查是否过期
        if datetime.now().timestamp() - timestamp > self.expiration_seconds:
            del self.cache[key]
            return None
        
        return cached_data
    
    def set(self, key: str, data: Any) -> None:
        """设置缓存
        
        Args:
            key: 缓存键
            data: 要缓存的数据
        """
        self.cache[key] = (data, datetime.now().timestamp())
    
    def delete(self, key: str) -> None:
        """删除缓存
        
        Args:
            key: 缓存键
        """
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
    
    def get_size(self) -> int:
        """获取缓存大小
        
        Returns:
            int: 缓存项数量
        """
        return len(self.cache)

# 创建全局缓存实例
cache = Cache()
