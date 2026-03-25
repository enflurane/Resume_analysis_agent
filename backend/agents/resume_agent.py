from smolagents import CodeAgent
from . import get_model

def build_resume_agent() -> CodeAgent:
    """构建简历分析Agent"""
    model = get_model()
    
    agent = CodeAgent(
        tools=[],
        model=model,
        code_block_tags="markdown"
    )
    return agent
