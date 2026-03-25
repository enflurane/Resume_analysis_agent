import pdfplumber
import docx
from io import BytesIO
from typing import Optional
import re
from PIL import Image
import pytesseract

class ResumeParser:
    def __init__(self):
        self.supported_formats = {".pdf", ".docx", ".jpg", ".jpeg", ".png", ".gif"}
    
    def extract_text(self, file_content: bytes, file_extension: str) -> str:
        if file_extension == ".pdf":
            return self._extract_pdf_text(file_content)
        elif file_extension == ".docx":
            return self._extract_docx_text(file_content)
        elif file_extension in [".jpg", ".jpeg", ".png", ".gif"]:
            return self._extract_image_text(file_content)
        else:
            raise ValueError(f"不支持的文件格式: {file_extension}")
    
    def _extract_pdf_text(self, file_content: bytes) -> str:
        text = ""
        try:
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")
        
        return self._clean_text(text)
    
    def _extract_docx_text(self, file_content: bytes) -> str:
        text = ""
        try:
            doc = docx.Document(BytesIO(file_content))
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"DOCX解析失败: {str(e)}")
        
        return self._clean_text(text)
    
    def _extract_image_text(self, file_content: bytes) -> str:
        text = ""
        try:
            image = Image.open(BytesIO(file_content))
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        except Exception as e:
            raise Exception(f"图片OCR解析失败: {str(e)}")
        
        return self._clean_text(self._filter_jd_text(text))
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,;:!?()\-"\']', '', text)
        text = text.strip()
        
        paragraphs = []
        current_paragraph = ""
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = ""
            else:
                if current_paragraph:
                    current_paragraph += " " + line
                else:
                    current_paragraph = line
        
        if current_paragraph:
            paragraphs.append(current_paragraph)
        
        return '\n\n'.join(paragraphs)
    
    def _filter_jd_text(self, text: str) -> str:
        # 过滤掉无关信息，保留与JD相关的内容
        # 移除常见的无关信息
        irrelevant_patterns = [
            r'\b(微信|电话|邮箱|地址|联系人|招聘|HR|人力资源|公司|企业|集团)\b.*?\n',
            r'\b(薪资|待遇|福利|保险|公积金|年终奖|提成|补贴)\b.*?\n',
            r'\b(工作地点|上班地点|公司地址)\b.*?\n',
            r'\b(简历|投递|邮箱|联系方式|联系电话)\b.*?\n',
            r'\b(学历要求|学历限制|本科及以上|大专及以上)\b.*?\n',
            r'\b(工作经验|经验要求|3-5年|1-3年|5年以上)\b.*?\n',
            r'\b(岗位职责|工作内容|职位描述|岗位要求|任职要求)\b.*?\n',
        ]
        
        filtered_text = text
        for pattern in irrelevant_patterns:
            filtered_text = re.sub(pattern, '', filtered_text, flags=re.IGNORECASE)
        
        # 保留关键信息
        key_patterns = [
            r'\b(岗位|职位|职责|要求|技能|经验|学历|专业|资格)\b',
            r'\b(Python|Java|C\+\+|JavaScript|React|Vue|Node\.js|SQL|NoSQL|Docker|Kubernetes)\b',
            r'\b(前端|后端|全栈|算法|数据|测试|运维|产品|设计)\b',
            r'\b(本科|硕士|博士|大专)\b',
            r'\b(年经验|年以上|年以下)\b',
        ]
        
        # 检查是否包含关键信息
        has_key_info = any(re.search(pattern, filtered_text, re.IGNORECASE) for pattern in key_patterns)
        
        if not has_key_info:
            # 如果没有关键信息，返回原始文本的前500个字符
            return text[:500]
        
        return filtered_text
