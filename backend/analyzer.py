import json
from openai import OpenAI
from typing import Dict, Any, Optional
from datetime import datetime
from .config import settings

class ResumeAnalyzer:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or settings.API_KEY
        self.base_url = base_url or settings.BASE_URL
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url) if self.api_key else None
    
    def extract_info(self, resume_text: str) -> Dict[str, Any]:
        if not self.client:
            return self._mock_extract_info(resume_text)
        
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        prompt = f"""
请分析以下完整的简历文本，提取所有关键信息，并以结构化的JSON格式返回。

当前时间：{current_time}

简历文本：
{resume_text}

分析要求：
1. 全面分析简历内容，不要遗漏任何重要信息
2. 识别简历中的所有关键部分，包括但不限于：
   - 个人基本信息（姓名、联系方式、地址等）
   - 求职意向和期望薪资
   - 工作经历（包括公司、职位、时间、职责、成就）
   - 项目经历（包括项目名称、时间、职责、成果）
   - 教育背景（包括学校、专业、学位、毕业时间）
   - 科研经历（包括研究方向、研究内容、成果、论文等）
   - 学术经历（包括学术活动、奖项、任职等）
   - 技能证书
   - 其他相关信息

3. 以自然、灵活的方式提取信息，适应不同简历的格式和结构
4. 保持信息的完整性和准确性
5. 按时间倒序排列经历类信息（最近的在前）

返回格式：
{{
    "basic_info": {{
        "name": "",
        "phone": "",
        "email": "",
        "address": ""
    }},
    "job_info": {{
        "job_intention": "",
        "expected_salary": ""
    }},
    "background_info": {{
        "work_years": "",
        "education": [],
        "work_experience": [],
        "projects": [],
        "research_experience": [],
        "academic_experience": [],
        "skills": [],
        "certificates": [],
        "other_info": []
    }}
}}

请确保返回的JSON格式正确，字段名使用英文。
"""

        
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个专业的简历分析助手，擅长从简历中提取结构化信息。"},
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
            print(f"AI提取信息失败: {str(e)}")
            return self._mock_extract_info(resume_text)
    
    def _mock_extract_info(self, resume_text: str) -> Dict[str, Any]:
        return {
            "basic_info": {
                "name": "示例姓名",
                "phone": "13800138000",
                "email": "example@email.com",
                "address": "北京市"
            },
            "job_info": {
                "job_intention": "软件工程师",
                "expected_salary": "15-25K"
            },
            "background_info": {
                "work_years": "3年",
                "education": [
                    {
                        "school": "示例大学",
                        "major": "计算机科学与技术",
                        "degree": "本科",
                        "graduation_time": "2020年"
                    }
                ],
                "work_experience": [
                    {
                        "company": "示例科技有限公司",
                        "position": "后端开发工程师",
                        "period": "2021年7月 - 至今",
                        "description": "负责公司核心产品的后端开发，使用Python和Django框架，参与数据库设计和API开发，优化系统性能，提升用户体验。"
                    },
                    {
                        "company": "示例互联网公司",
                        "position": "软件实习生",
                        "period": "2020年3月 - 2020年6月",
                        "description": "参与Web项目开发，负责前端页面实现和后端接口调试，学习并应用现代Web开发技术。"
                    }
                ],
                "projects": [
                    {
                        "name": "智能简历分析系统",
                        "period": "2023年1月 - 2023年3月",
                        "responsibility": "负责核心模块开发，包括简历解析和岗位匹配算法",
                        "achievement": "提升系统性能30%，减少分析时间从10秒到3秒"
                    },
                    {
                        "name": "在线教育平台",
                        "period": "2022年5月 - 2022年8月",
                        "responsibility": "负责用户模块和课程管理模块的开发",
                        "achievement": "成功上线并获得1000+用户注册"
                    }
                ],
                "research_experience": [
                    {
                        "field": "人工智能，自然语言处理",
                        "content": "研究简历文本的自动分析和信息提取技术，开发基于深度学习的简历解析模型",
                        "achievements": "提出了一种新的简历信息提取算法，准确率达到95%以上",
                        "papers": ["基于深度学习的简历信息提取方法研究，《计算机科学》，2023年"]
                    },
                    {
                        "field": "机器学习，数据挖掘",
                        "content": "研究大规模简历数据的分析和挖掘技术，开发简历与岗位匹配算法",
                        "achievements": "开发了一个简历与岗位匹配系统，匹配准确率达到85%",
                        "papers": ["简历与岗位匹配算法研究，《信息系统学报》，2022年"]
                    }
                ],
                "academic_experience": [
                    {
                        "activity": "参加第10届全国人工智能大会，发表论文并做口头报告",
                        "awards": ["优秀论文奖"],
                        "positions": ["计算机学会会员"]
                    },
                    {
                        "activity": "担任《计算机科学》期刊审稿人",
                        "awards": [],
                        "positions": ["研究生会学术部部长"]
                    }
                ]
            }
        }
