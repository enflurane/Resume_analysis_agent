# 简历分析系统

智能简历解析与岗位匹配分析系统，支持PDF/DOCX/图片格式的简历文件上传、解析、信息提取，以及与岗位需求的匹配分析。

## 功能特性

### 简历文件读取解析功能
- 支持上传PDF/DOCX格式的简历文件
- 支持上传图片格式的JD文件（JPG/JPEG/PNG/GIF），自动进行OCR文字识别
- 解析PDF内容，提取文本信息（兼容多页简历）
- 对提取文本进行清洗和结构化处理（去除冗余字符、合理分段等）
- 支持JD图片中的无关信息过滤

### 关键信息提取
利用AI模型从简历文本中全面提取关键信息，采用自然灵活的方式适应不同简历格式：

| 类别 | 包含内容 |
|------|----------|
| 基本信息 | 姓名、电话、邮箱、地址 |
| 求职信息 | 求职意向、期望薪资 |
| 教育背景 | 学校、专业、学位、毕业时间 |
| 工作经历 | 公司名称、职位、工作时间、工作描述 |
| 项目经历 | 项目名称、项目时间、职责、成果 |
| 科研经历 | 研究方向、研究内容、成果、发表论文等 |
| 学术经历 | 学术活动、学术奖项、学术任职等 |
| 技能证书 | 专业技能、资格证书 |
| 其他信息 | 其他相关信息 |

### 简历分析功能

#### 岗位JD输入和分析功能
- 提供接口，接收招聘岗位的需求描述（文本或图片）
- 对岗位需求进行关键词提取和分析
- 将解析后的简历信息与岗位需求进行匹配，计算匹配度评分
- 利用AI模型对匹配度进行更精准的评分
- 在提示词中包含当前时间信息，提高分析准确性

#### 结果返回与缓存
- 以JSON格式结构化返回解析结果、关键信息和匹配度评分
- 支持智能缓存机制，当简历或JD只改变其中一项时，读取缓存避免重复分析
- 缓存过期时间为1小时

### 前端页面
- 使用原生HTML/CSS/JavaScript完成简洁可用的交互页面
- 支持文件拖拽上传
- 实时显示分析结果
- 响应式设计，支持移动端访问
- 全面展示候选人背景信息（教育、工作、项目、科研、学术、技能等）

### 当前简历的不足分析
- 分析当前简历距离JD还有哪些差距
- 考虑科研经历和学术经历与岗位需求的相关性

### 学习路径和建议
- 为简历拥有者提供具体的可以满足JD要求的学习路径和建议
- 建议简历上需要什么项目、科研或学术经验来体现这些能力

### Agent智能分析功能
- 基于AI Agent的智能简历分析，提供更灵活的分析能力
- 支持自定义查询，回答关于简历的具体问题
- 使用Agent进行岗位需求深度分析
- 通过Agent实现简历与岗位的智能匹配分析
- **流式输出**：实时显示Agent的分析过程，提高响应速度
- **思考过程可视化**：展示Agent的思考过程、执行代码和分析结果

## 项目结构

```
Resume_analysis_local/
├── backend/
│   ├── __init__.py
│   ├── config.py          # 配置文件
│   ├── cache.py           # 缓存模块
│   ├── parser.py          # PDF/DOCX/图片解析器（含OCR）
│   ├── analyzer.py        # 简历信息提取器
│   ├── jd_matcher.py      # JD匹配分析器
│   ├── main.py            # FastAPI主程序
│   ├── agents/            # AI Agent模块
│   │   ├── __init__.py
│   │   ├── resume_agent.py    # 简历分析Agent
│   │   ├── jd_agent.py        # 岗位分析Agent
│   │   ├── matcher_agent.py   # 匹配分析Agent
│   │   └── tools/             # Agent工具集
│   │       ├── __init__.py
│   │       ├── common_tools.py    # 通用工具
│   │       ├── resume_tools.py    # 简历相关工具
│   │       └── jd_tools.py        # 岗位相关工具
│   └── core/              # 核心功能模块
│       ├── __init__.py
│       ├── memory.py      # 内存管理
│       └── utils.py       # 工具函数
├── frontend/
│   ├── index.html         # 前端页面
│   ├── style.css          # 样式文件
│   └── script.js          # JavaScript逻辑
├── requirements.txt       # Python依赖
├── .env.example           # 环境变量示例
└── README.md              # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
API_KEY=your_openai_api_key_here
BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo
```

支持DeepSeek API：
```bash
API_KEY=your_deepseek_api_key_here
BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat
```

如果不配置API Key，系统将使用模拟数据进行演示。

### 3. 启动后端服务

```bash
# 方式1：直接运行
python backend/main.py

# 方式2：使用uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 `http://localhost:8000` 启动

### 4. 启动前端服务

```bash
python -m http.server 3000 --directory frontend
```

然后访问 http://localhost:3000

## API接口文档

### 1. 上传简历
```
POST /api/upload
Content-Type: multipart/form-data

参数:
- file: 简历文件（PDF/DOCX）

返回:
{
  "success": true,
  "message": "简历上传并解析成功",
  "data": {
    "filename": "resume.pdf",
    "text": "提取的文本内容"
  }
}
```

### 2. 提取简历信息
```
POST /api/extract
Content-Type: application/json

参数:
{
  "text": "简历文本内容"
}

返回:
{
  "success": true,
  "message": "信息提取成功",
  "data": {
    "basic_info": {...},
    "job_info": {...},
    "background_info": {
      "work_years": "",
      "education": [],
      "work_experience": [],
      "projects": [],
      "research_experience": [],
      "academic_experience": [],
      "skills": [],
      "certificates": [],
      "other_info": []
    }
  }
}
```

### 3. 分析岗位需求（JD）
```
POST /api/analyze-jd
Content-Type: application/json

参数:
{
  "jd_text": "岗位需求描述"
}

返回:
{
  "success": true,
  "message": "JD分析成功",
  "data": {
    "basic_info": {...},
    "skills": {...},
    "experience": {...},
    "education": {...},
    "other_requirements": {...}
  }
}
```

### 4. 上传JD文件
```
POST /api/upload-jd
Content-Type: multipart/form-data

参数:
- file: JD文件（PDF/DOCX/图片）

返回:
{
  "success": true,
  "message": "JD上传并解析成功",
  "data": {
    "filename": "jd.pdf",
    "text": "提取的文本内容"
  }
}
```

### 5. 匹配简历与JD
```
POST /api/match
Content-Type: application/json

参数:
{
  "resume_info": {...},
  "jd_info": {...}
}

返回:
{
  "success": true,
  "message": "匹配分析成功",
  "data": {
    "match_score": {...},
    "strengths": {...},
    "gaps": {...},
    "suggestions": {...}
  }
}
```

### 6. 完整分析（一步完成）
```
POST /api/full-analysis
Content-Type: multipart/form-data

参数:
- file: 简历文件（PDF/DOCX）
- jd_text: 岗位需求描述（可选）
- jd_file: JD文件（PDF/DOCX/图片，可选）

返回:
{
  "success": true,
  "message": "完整分析成功",
  "data": {
    "resume_text": "...",
    "resume_info": {...},
    "jd_analysis": {...},
    "match_result": {...}
  }
}
```

### 7. Agent智能分析
```
POST /api/agent-analysis
Content-Type: multipart/form-data

参数:
- file: 简历文件（PDF/DOCX）
- query: 自定义查询问题

返回: 流式响应（SSE格式）

流式数据格式:
{
  "type": "step",
  "content": {
    "thinking": "Agent的思考过程",
    "code": "执行的代码",
    "output": "执行结果",
    "final_answer": "最终答案"
  }
}
```

### 8. Agent岗位需求分析
```
POST /api/agent-jd-analysis
Content-Type: application/json

参数:
{
  "jd_text": "岗位需求描述"
}

返回:
{
  "success": true,
  "message": "Agent岗位分析成功",
  "data": {
    "result": "分析结果"
  }
}
```

### 9. Agent简历与岗位匹配
```
POST /api/agent-match
Content-Type: application/json

参数:
{
  "resume_info": {...},
  "jd_info": {...}
}

返回:
{
  "success": true,
  "message": "Agent匹配分析成功",
  "data": {
    "result": "分析结果"
  }
}
```

## 技术栈

### 后端
- **FastAPI**: 高性能Web框架
- **pdfplumber**: PDF文本提取
- **python-docx**: DOCX文档解析
- **pytesseract**: OCR文字识别
- **Pillow**: 图像处理
- **OpenAI API**: AI模型调用（支持OpenAI和DeepSeek）
- **Pydantic**: 数据验证
- **AI Agent**: 智能分析代理
- **Agent Tools**: 自定义Agent工具
- **SSE (Server-Sent Events)**: 流式响应技术

### 前端
- **原生HTML/CSS/JavaScript**
- **Fetch API**: HTTP请求
- **响应式设计**: 支持移动端
- **SSE (Server-Sent Events)**: 流式响应处理

## 使用说明

### 上传简历
1. 点击上传区域或拖拽文件到上传区域
2. 支持PDF和DOCX格式
3. 文件大小限制为10MB

### 输入岗位需求（可选）
1. 在"岗位需求"文本框中输入JD描述
2. 或上传JD文件（支持PDF/DOCX/图片格式）
3. 可以包含职位名称、技能要求、经验要求等

### 开始分析
1. 点击"开始分析"按钮
2. 等待分析完成（通常需要几秒钟）
3. 查看分析结果

### 查看分析结果
- **基本信息**: 姓名、电话、邮箱等
- **背景信息**: 
  - 教育背景
  - 工作经历
  - 项目经历
  - 科研经历
  - 学术经历
  - 技能证书
  - 其他信息
- **匹配分析**: 
  - 匹配度评分（技能、经验、学历、综合）
  - 优势分析
  - 差距分析
  - 改进建议（学习路径、项目建议等）

## 注意事项

1. **API Key配置**: 如果需要使用真实的AI分析功能，请配置OpenAI或DeepSeek API Key
2. **文件格式**: 支持PDF、DOCX格式（简历），支持PDF、DOCX、图片格式（JD）
3. **文件大小**: 单个文件最大10MB
4. **网络连接**: 使用AI分析功能需要网络连接
5. **隐私保护**: 上传的简历不会被保存，仅用于实时分析
6. **OCR识别**: JD图片中的文字识别准确率取决于图片质量

## 常见问题

### Q: 为什么分析结果不准确？
A: 可能原因：
- 简历格式不规范
- 未配置API Key，使用的是模拟数据
- 简历内容不完整
- JD图片质量不佳导致OCR识别错误

### Q: 如何提高分析准确度？
A: 建议：
- 使用格式规范的简历
- 确保简历信息完整
- 配置真实的API Key
- 上传清晰的JD图片

### Q: 支持哪些文件格式？
A: 
- 简历：PDF、DOCX
- JD：PDF、DOCX、JPG、JPEG、PNG、GIF

### Q: 分析需要多长时间？
A: 通常需要3-10秒，取决于简历长度和网络状况。使用缓存后重复分析会更快。

### Q: 是否支持批量分析？
A: 目前版本仅支持单简历分析，批量分析功能在开发计划中。

## 开发计划

- [x] 支持JD图片OCR识别
- [x] 添加智能缓存机制
- [x] 在提示词中添加当前时间信息
- [x] 优化科研经历和学术经历提取
- [x] 全面展示候选人背景信息
- [ ] 添加简历模板生成功能
- [ ] 支持批量简历分析
- [ ] 添加简历评分系统
- [ ] 支持导出分析报告（PDF/Word）
- [ ] 添加用户认证和权限管理
- [ ] 支持历史记录查看

## 更新日志

### v1.2.0 (2026-03-25)
- 新增AI Agent智能分析功能
- 新增三个Agent API接口：agent-analysis、agent-jd-analysis、agent-match
- 新增Agent工具集，支持简历分析、岗位分析和匹配分析
- 优化系统架构，添加agents和core模块
- 实现Agent流式输出，提高响应速度
- 添加Agent思考过程可视化，展示分析过程和执行代码

### v1.1.0 (2026-03-05)
- 新增JD图片上传和OCR识别功能
- 新增智能缓存机制，提高响应速度
- 新增当前时间获取功能，提高分析准确性
- 优化科研经历和学术经历提取能力
- 优化前端页面，全面展示候选人背景信息
- 支持DeepSeek API

### v1.0.0 (2024)
- 初始版本发布
- 支持PDF/DOCX简历解析
- 支持基本信息、工作经历、项目经历提取
- 支持JD分析和简历匹配

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue。
