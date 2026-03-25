# 简历分析系统

智能简历解析与岗位匹配分析系统，基于AI Agent技术，支持多格式简历文件上传、解析、信息提取，以及与岗位需求的智能匹配分析。

## 功能特性

### 文件解析
- 支持PDF/DOCX格式的简历文件
- 支持PDF/DOCX/图片格式（JPG/JPEG/PNG/GIF）的JD文件
- OCR文字识别，自动提取图片中的文本内容
- 智能文本清洗和结构化处理

### AI智能分析
- **关键信息提取**：全面提取基本信息、教育背景、工作经历、项目经历、科研经历、学术经历、技能证书等
- **岗位需求分析**：解析JD文本，提取关键要求和技能
- **智能匹配分析**：计算简历与岗位的匹配度，分析优势和差距
- **AI Agent对话**：支持自定义查询，回答关于简历的具体问题
- **流式输出**：实时显示Agent分析过程和思考链

### 智能缓存
- 自动缓存分析结果，避免重复计算
- 缓存过期时间1小时
- 提升响应速度

### 前端界面
- 原生HTML/CSS/JavaScript，无需框架
- 支持文件拖拽上传
- 响应式设计，支持移动端
- 实时显示分析结果

## 项目结构

```
Resume_analysis_agent/
├── backend/                    # 后端服务
│   ├── __init__.py
│   ├── main.py                # FastAPI主程序
│   ├── config.py              # 配置管理
│   ├── cache.py               # 缓存模块
│   ├── parser.py              # 文件解析器（PDF/DOCX/OCR）
│   ├── analyzer.py            # 简历信息提取
│   ├── jd_matcher.py          # JD匹配分析
│   ├── agents/                # AI Agent模块
│   │   ├── resume_agent.py    # 简历分析Agent
│   │   ├── jd_agent.py        # 岗位分析Agent
│   │   ├── matcher_agent.py   # 匹配分析Agent
│   │   └── tools/             # Agent工具集
│   │       ├── common_tools.py
│   │       ├── resume_tools.py
│   │       └── jd_tools.py
│   └── core/                  # 核心模块
│       ├── memory.py          # 内存管理
│       └── utils.py           # 工具函数
├── frontend/                  # 前端界面
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt           # Python依赖
├── .env                       # 环境变量（需自行创建）
└── README.md                  # 项目说明
```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
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

或使用DeepSeek API：

```bash
API_KEY=your_deepseek_api_key_here
BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat
```

> 注意：如果不配置API Key，系统将使用模拟数据进行演示。

### 3. 启动服务

```bash
# 启动后端服务
python backend/main.py

# 或使用uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 `http://localhost:8000` 启动

访问 `http://localhost:8000/static/index.html` 使用前端界面

## API接口

### 核心接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/upload` | POST | 上传并解析简历 |
| `/api/upload-jd` | POST | 上传并解析JD文件 |
| `/api/extract` | POST | 提取简历信息 |
| `/api/analyze-jd` | POST | 分析岗位需求 |
| `/api/match` | POST | 匹配简历与JD |
| `/api/full-analysis` | POST | 完整分析（一步完成） |
| `/api/agent-analysis` | POST | Agent智能分析（流式） |
| `/api/agent-jd-analysis` | POST | Agent岗位分析 |
| `/api/agent-match` | POST | Agent匹配分析 |

### 详细文档

启动服务后访问 `http://localhost:8000/docs` 查看完整的API文档（Swagger UI）

## 技术栈

### 后端
- **FastAPI** - 高性能Web框架
- **pdfplumber** - PDF文本提取
- **python-docx** - DOCX文档解析
- **pytesseract** - OCR文字识别
- **Pillow** - 图像处理
- **OpenAI API** - AI模型调用（支持OpenAI和DeepSeek）
- **Pydantic** - 数据验证
- **SSE** - 流式响应

### 前端
- **原生HTML/CSS/JavaScript**
- **Fetch API** - HTTP请求
- **SSE** - 流式响应处理

## 使用说明

### 上传简历
1. 点击上传区域或拖拽文件到上传区域
2. 支持PDF和DOCX格式
3. 文件大小限制为10MB

### 输入岗位需求
1. 在"岗位需求"文本框中输入JD描述
2. 或上传JD文件（支持PDF/DOCX/图片格式）

### 开始分析
1. 点击"开始分析"按钮
2. 查看分析结果

### 查看结果
- **基本信息**：姓名、电话、邮箱等
- **背景信息**：教育、工作、项目、科研、学术、技能等
- **匹配分析**：匹配度评分、优势、差距、改进建议
- **智能Agent**：自定义查询，获取深度分析

## 注意事项

1. **API Key**：配置OpenAI或DeepSeek API Key以使用真实AI分析
2. **文件格式**：简历支持PDF/DOCX，JD支持PDF/DOCX/图片
3. **文件大小**：单个文件最大10MB
4. **网络连接**：AI分析功能需要网络连接
5. **隐私保护**：上传的简历不会被保存，仅用于实时分析
6. **OCR识别**：JD图片识别准确率取决于图片质量

## 常见问题

**Q: 为什么分析结果不准确？**
A: 可能原因：简历格式不规范、未配置API Key、简历内容不完整、JD图片质量不佳

**Q: 如何提高分析准确度？**
A: 使用格式规范的简历、确保信息完整、配置真实API Key、上传清晰的JD图片

**Q: 支持哪些文件格式？**
A: 简历：PDF、DOCX；JD：PDF、DOCX、JPG、JPEG、PNG、GIF

**Q: 分析需要多长时间？**
A: 通常需要3-10秒，使用缓存后会更快

## 许可证

MIT License
