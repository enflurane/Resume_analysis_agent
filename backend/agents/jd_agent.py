from smolagents import CodeAgent
from . import get_model

def build_jd_agent() -> CodeAgent:
    """构建岗位分析Agent"""
    model = get_model()
    
    agent = CodeAgent(
        tools=[],
        model=model,
        code_block_tags="markdown"
    )
    return agent
