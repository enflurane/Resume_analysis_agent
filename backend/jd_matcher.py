import json
from openai import OpenAI
from typing import Dict, Any, Optional, List
from datetime import datetime
from .config import settings

class JDMatcher:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or settings.API_KEY
        self.base_url = base_url or settings.BASE_URL
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url) if self.api_key else None
    
    def analyze_jd(self, jd_text: str) -> Dict[str, Any]:
        if not self.client:
            return self._mock_analyze_jd(jd_text)
        
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        prompt = f"""
请分析以下岗位需求（JD），提取关键信息并以JSON格式返回：

1. 岗位基本信息：
   - 岗位名称
   - 岗位级别

2. 技能要求（按重要性排序）：
   - 必备技能
   - 加分技能

3. 经验要求：
   - 工作年限要求
   - 相关领域经验

4. 学历要求：
   - 学历要求
   - 专业要求

5. 其他要求：
   - 语言要求
   - 其他软技能

当前时间：{current_time}

岗位需求文本：
{jd_text}

返回格式示例：
{{
    "basic_info": {{
        "position": "",
        "level": ""
    }},
    "skills": {{
        "required": [],
        "preferred": []
    }},
    "experience": {{
        "years": "",
        "related_experience": []
    }},
    "education": {{
        "degree": "",
        "major": ""
    }},
    "other_requirements": {{
        "language": "",
        "soft_skills": []
    }}
}}
"""

        
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个专业的招聘分析助手，擅长分析岗位需求。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            json_str = result_text[json_start:json_end]
            
            return json.loads(json_str)
        except Exception as e:
            print(f"JD分析失败: {str(e)}")
            return self._mock_analyze_jd(jd_text)
    
    def match_resume_jd(self, resume_info: Dict[str, Any], jd_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client:
            return self._mock_match_resume_jd(resume_info, jd_info)
        
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        prompt = f"""
请根据以下简历信息和岗位需求，进行匹配分析并返回JSON格式结果。特别注意分析简历中的科研经历和学术经历与岗位需求的相关性：

当前时间：{current_time}

简历信息：
{json.dumps(resume_info, ensure_ascii=False, indent=2)}

岗位需求：
{json.dumps(jd_info, ensure_ascii=False, indent=2)}

请分析以下内容：

1. 匹配度评分（0-100分）：
   - 技能匹配率
   - 经验相关性（包括工作经验、项目经验、科研经验和学术经验）
   - 学历匹配度
   - 综合匹配度

2. 优势分析：
   - 匹配的技能
   - 相关经验（包括工作经验、项目经验、科研经验和学术经验）
   - 其他优势

3. 差距分析：
   - 缺失的必备技能
   - 经验不足之处（包括工作经验、项目经验、科研经验和学术经验）
   - 其他差距

4. 改进建议：
   - 需要学习的技能
   - 建议补充的项目经验、科研经验和学术经验
   - 其他改进建议

返回格式示例：
{{
    "match_score": {{
        "skills_match": 0,
        "experience_relevance": 0,
        "education_match": 0,
        "overall_match": 0
    }},
    "strengths": {{
        "matched_skills": [],
        "relevant_experience": [],
        "other_strengths": []
    }},
    "gaps": {{
        "missing_skills": [],
        "experience_gaps": [],
        "other_gaps": []
    }},
    "suggestions": {{
        "skills_to_learn": [],
        "recommended_projects": [],
        "other_suggestions": []
    }}
}}
"""

        
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个专业的简历匹配分析助手，擅长评估简历与岗位的匹配度。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            json_str = result_text[json_start:json_end]
            
            return json.loads(json_str)
        except Exception as e:
            print(f"匹配分析失败: {str(e)}")
            return self._mock_match_resume_jd(resume_info, jd_info)
    
    def _mock_analyze_jd(self, jd_text: str) -> Dict[str, Any]:
        return {
            "basic_info": {
                "position": "软件工程师",
                "level": "中级"
            },
            "skills": {
                "required": ["Python", "Django", "MySQL"],
                "preferred": ["Redis", "Docker", "Kubernetes"]
            },
            "experience": {
                "years": "3-5年",
                "related_experience": ["Web开发", "后端开发"]
            },
            "education": {
                "degree": "本科及以上",
                "major": "计算机相关专业"
            },
            "other_requirements": {
                "language": "英语CET-4",
                "soft_skills": ["团队协作", "沟通能力"]
            }
        }
    
    def _mock_match_resume_jd(self, resume_info: Dict[str, Any], jd_info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "match_score": {
                "skills_match": 70,
                "experience_relevance": 65,
                "education_match": 80,
                "overall_match": 72
            },
            "strengths": {
                "matched_skills": ["Python", "Django"],
                "relevant_experience": ["Web开发"],
                "other_strengths": ["学习能力强"]
            },
            "gaps": {
                "missing_skills": ["Redis", "Docker"],
                "experience_gaps": ["缺乏大规模项目经验"],
                "other_gaps": ["缺少团队管理经验"]
            },
            "suggestions": {
                "skills_to_learn": ["Redis缓存技术", "Docker容器化部署"],
                "recommended_projects": [
                    "开发一个高并发的Web应用，使用Redis进行缓存优化",
                    "使用Docker和Kubernetes部署微服务架构项目"
                ],
                "other_suggestions": [
                    "参与开源项目，提升团队协作经验",
                    "考取相关技术认证，如AWS或Azure认证"
                ]
            }
        }
