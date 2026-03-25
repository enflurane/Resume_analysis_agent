from typing import Dict, Any
from smolagents import tool
from ...jd_matcher import JDMatcher

jd_matcher = JDMatcher()

@tool
async def analyze_jd(jd_text: str) -> Dict[str, Any]:
    """分析岗位需求
    
    Args:
        jd_text: 岗位需求文本
        
    Returns:
        结构化的岗位需求信息
    """
    return jd_matcher.analyze_jd(jd_text)

@tool
async def match_resume_jd(resume_info: Dict[str, Any], jd_info: Dict[str, Any]) -> Dict[str, Any]:
    """匹配简历与岗位
    
    Args:
        resume_info: 简历信息
        jd_info: 岗位需求信息
        
    Returns:
        匹配分析结果
    """
    return jd_matcher.match_resume_jd(resume_info, jd_info)
