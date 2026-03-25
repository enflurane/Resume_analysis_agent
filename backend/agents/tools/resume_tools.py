from typing import Dict, Any, Optional
from smolagents import tool
from ...parser import ResumeParser
from ...analyzer import ResumeAnalyzer

parser = ResumeParser()
analyzer = ResumeAnalyzer()

@tool
async def extract_resume_text(file_content: bytes, file_ext: str) -> str:
    """提取简历文本
    
    Args:
        file_content: 简历文件的字节内容
        file_ext: 简历文件的扩展名
        
    Returns:
        提取的文本内容
    """
    return parser.extract_text(file_content, file_ext)

@tool
async def analyze_resume(text: str) -> Dict[str, Any]:
    """分析简历信息
    
    Args:
        text: 简历文本内容
        
    Returns:
        结构化的简历信息
    """
    return analyzer.extract_info(text)
