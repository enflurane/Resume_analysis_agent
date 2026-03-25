from smolagents import CodeAgent
from . import get_model

def build_matcher_agent() -> CodeAgent:
    """构建匹配分析Agent"""
    model = get_model()
    
    agent = CodeAgent(
        tools=[],
        model=model,
        code_block_tags="markdown"
    )
    return agent
