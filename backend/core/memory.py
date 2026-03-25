from typing import List, Dict, Any
from datetime import datetime

class Memory:
    def __init__(self):
        self.steps: List[Dict[str, Any]] = []
    
    def add_step(self, step_type: str, content: Dict[str, Any]):
        """添加一个步骤到内存"""
        step = {
            "type": step_type,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.steps.append(step)
    
    def get_last_steps(self, n: int = 5) -> List[Dict[str, Any]]:
        """获取最近的n个步骤"""
        return self.steps[-n:]
    
    def clear(self):
        """清空内存"""
        self.steps = []
    
    def get_all_steps(self) -> List[Dict[str, Any]]:
        """获取所有步骤"""
        return self.steps
