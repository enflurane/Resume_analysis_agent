from typing import Dict, Any, List
import json
from smolagents import tool

@tool
async def format_json(data: Dict[str, Any]) -> str:
    """格式化JSON数据
    
    Args:
        data: 需要格式化的JSON数据
        
    Returns:
        格式化后的JSON字符串
    """
    return json.dumps(data, ensure_ascii=False, indent=2)

@tool
async def extract_key_info(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """提取指定键的信息
    
    Args:
        data: 源数据字典
        keys: 需要提取的键列表
        
    Returns:
        提取的键值对
    """
    return {key: data.get(key) for key in keys}
