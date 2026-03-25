from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import json

from .config import settings
from .parser import ResumeParser
from .analyzer import ResumeAnalyzer
from .jd_matcher import JDMatcher
from .cache import cache
from .agents.resume_agent import build_resume_agent
from .agents.jd_agent import build_jd_agent
from .agents.matcher_agent import build_matcher_agent

app = FastAPI(title="简历分析系统API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

parser = ResumeParser()
analyzer = ResumeAnalyzer()
jd_matcher = JDMatcher()

# 初始化Agent
resume_agent = build_resume_agent()
jd_agent = build_jd_agent()
matcher_agent = build_matcher_agent()

# 挂载静态文件服务
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

class JDRequest(BaseModel):
    jd_text: str

class MatchRequest(BaseModel):
    resume_info: dict
    jd_info: dict

@app.get("/")
async def root():
    return {"message": "简历分析系统API", "version": "1.0.0", "frontend": "请访问 /static/index.html 使用前端界面"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式，仅支持: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    if len(await file.read()) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制（最大 {settings.MAX_FILE_SIZE // (1024*1024)}MB）"
        )
    
    await file.seek(0)
    
    try:
        file_content = await file.read()
        
        # 生成缓存键
        cache_key = f"upload:{cache._generate_key(file_content)}:{file_ext}"
        
        # 检查缓存
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        text = parser.extract_text(file_content, file_ext)
        
        result = {
            "success": True,
            "message": "简历上传并解析成功",
            "data": {
                "filename": file.filename,
                "text": text
            }
        }
        
        # 缓存结果
        cache.set(cache_key, result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"简历解析失败: {str(e)}")

@app.post("/api/extract")
async def extract_info(request: dict):
    resume_text = request.get("text", "")
    if not resume_text:
        raise HTTPException(status_code=400, detail="简历文本不能为空")
    
    try:
        # 生成缓存键
        cache_key = f"extract:{cache._generate_key(resume_text)}"
        
        # 检查缓存
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        info = analyzer.extract_info(resume_text)
        
        result = {
            "success": True,
            "message": "信息提取成功",
            "data": info
        }
        
        # 缓存结果
        cache.set(cache_key, result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"信息提取失败: {str(e)}")

@app.post("/api/analyze-jd")
async def analyze_jd(request: JDRequest):
    if not request.jd_text:
        raise HTTPException(status_code=400, detail="岗位需求文本不能为空")
    
    try:
        # 生成缓存键
        cache_key = f"analyze-jd:{cache._generate_key(request.jd_text)}"
        
        # 检查缓存
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        jd_info = jd_matcher.analyze_jd(request.jd_text)
        
        result = {
            "success": True,
            "message": "JD分析成功",
            "data": jd_info
        }
        
        # 缓存结果
        cache.set(cache_key, result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JD分析失败: {str(e)}")

@app.post("/api/match")
async def match_resume_jd(request: MatchRequest):
    if not request.resume_info or not request.jd_info:
        raise HTTPException(status_code=400, detail="简历信息和JD信息不能为空")
    
    try:
        # 生成缓存键
        cache_key = f"match:{cache._generate_key(request.resume_info)}:{cache._generate_key(request.jd_info)}"
        
        # 检查缓存
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        match_result = jd_matcher.match_resume_jd(request.resume_info, request.jd_info)
        
        result = {
            "success": True,
            "message": "匹配分析成功",
            "data": match_result
        }
        
        # 缓存结果
        cache.set(cache_key, result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"匹配分析失败: {str(e)}")

@app.post("/api/upload-jd")
async def upload_jd(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式，仅支持: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    if len(await file.read()) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制（最大 {settings.MAX_FILE_SIZE // (1024*1024)}MB）"
        )
    
    await file.seek(0)
    
    try:
        file_content = await file.read()
        
        # 生成缓存键
        cache_key = f"upload-jd:{cache._generate_key(file_content)}:{file_ext}"
        
        # 检查缓存
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        text = parser.extract_text(file_content, file_ext)
        
        result = {
            "success": True,
            "message": "JD上传并解析成功",
            "data": {
                "filename": file.filename,
                "text": text
            }
        }
        
        # 缓存结果
        cache.set(cache_key, result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JD解析失败: {str(e)}")

@app.post("/api/full-analysis")
async def full_analysis(file: UploadFile = File(...), jd_text: str = "", jd_file: Optional[UploadFile] = None):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式，仅支持: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    await file.seek(0)
    
    try:
        file_content = await file.read()
        
        # 处理JD文件
        jd_content = b""
        jd_ext = ""
        if jd_file:
            jd_ext = os.path.splitext(jd_file.filename)[1].lower()
            if jd_ext not in settings.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的JD文件格式，仅支持: {', '.join(settings.ALLOWED_EXTENSIONS)}"
                )
            await jd_file.seek(0)
            jd_content = await jd_file.read()
        
        # 生成缓存键
        cache_key = f"full-analysis:{cache._generate_key(file_content)}:{file_ext}:{cache._generate_key(jd_text)}:{cache._generate_key(jd_content)}:{jd_ext}"
        
        # 检查缓存
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        text = parser.extract_text(file_content, file_ext)
        resume_info = analyzer.extract_info(text)
        
        result = {
            "resume_text": text,
            "resume_info": resume_info,
            "jd_analysis": None,
            "match_result": None
        }
        
        # 处理JD信息
        jd_text_final = jd_text
        if jd_content:
            jd_text_final = parser.extract_text(jd_content, jd_ext)
        
        if jd_text_final:
            jd_info = jd_matcher.analyze_jd(jd_text_final)
            match_result = jd_matcher.match_resume_jd(resume_info, jd_info)
            result["jd_analysis"] = jd_info
            result["match_result"] = match_result
        
        response = {
            "success": True,
            "message": "完整分析成功",
            "data": result
        }
        
        # 缓存结果
        cache.set(cache_key, response)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"完整分析失败: {str(e)}")

@app.post("/api/agent-analysis")
async def agent_analysis(file: UploadFile = File(...), query: str = ""):
    """使用Agent进行智能分析"""
    try:
        file_content = await file.read()
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # 使用parser提取文本内容
        text = parser.extract_text(file_content, file_ext)
        
        # 构建任务
        task = f"分析以下简历文件，提取关键信息并回答问题：{query}\n"
        task += f"文件内容：{text}\n"
        task += f"文件类型：{file_ext}\n"
        task += "\n"
        task += "请特别注意：\n"
        task += "1. 对于项目经历，请详细提取项目名称、项目时间、职责描述和成果\n"
        task += "2. 确保职责和成果部分有具体内容，不要只提取标题\n"
        task += "3. 分析要全面，包括基本信息、教育背景、工作经历、项目经历、技能等\n"
        task += "4. 回答要详细、准确，基于简历内容进行分析"
        
        # 异步生成器函数
        async def stream_agent_response():
            # 使用Agent的流式输出
            for step in resume_agent.run(task, stream=True):
                # 构建响应数据
                response_data = {
                    "type": "step",
                    "content": {
                        "thinking": step.thinking if hasattr(step, 'thinking') else None,
                        "code": step.code if hasattr(step, 'code') else None,
                        "output": step.output if hasattr(step, 'output') else None,
                        "final_answer": step.final_answer if hasattr(step, 'final_answer') else None
                    }
                }
                # 发送SSE格式的数据
                yield f"data: {json.dumps(response_data)}\n\n"
        
        # 返回流式响应
        return StreamingResponse(
            stream_agent_response(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent分析失败: {str(e)}")

@app.post("/api/agent-jd-analysis")
async def agent_jd_analysis(jd_text: str):
    """使用Agent分析岗位需求"""
    try:
        if not jd_text:
            raise HTTPException(status_code=400, detail="岗位需求文本不能为空")
        
        # 使用Agent进行分析
        result = jd_agent.run(
            f"分析以下岗位需求，提取关键信息并提供分析结果：\n{jd_text}"
        )
        
        return {
            "success": True,
            "message": "Agent岗位分析成功",
            "data": {"result": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent岗位分析失败: {str(e)}")

@app.post("/api/agent-match")
async def agent_match(resume_info: dict, jd_info: dict):
    """使用Agent进行简历与岗位匹配"""
    try:
        if not resume_info or not jd_info:
            raise HTTPException(status_code=400, detail="简历信息和岗位信息不能为空")
        
        # 使用Agent进行匹配
        result = matcher_agent.run(
            f"根据以下简历信息和岗位需求进行匹配分析：\n"  
            f"简历信息：{resume_info}\n"  
            f"岗位需求：{jd_info}"
        )
        
        return {
            "success": True,
            "message": "Agent匹配分析成功",
            "data": {"result": result}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent匹配分析失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
