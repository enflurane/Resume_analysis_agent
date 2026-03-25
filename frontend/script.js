const API_BASE_URL = 'http://localhost:8000/api';

let selectedFile = null;
let selectedJdFile = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFile = document.getElementById('removeFile');

const jdUploadArea = document.getElementById('jdUploadArea');
const jdFileInput = document.getElementById('jdFileInput');
const jdFileInfo = document.getElementById('jdFileInfo');
const jdFileName = document.getElementById('jdFileName');
const removeJdFile = document.getElementById('removeJdFile');

const jdText = document.getElementById('jdText');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const matchTab = document.getElementById('matchTab');

// 简历文件上传事件
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0], false);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0], false);
    }
});

removeFile.addEventListener('click', (e) => {
    e.stopPropagation();
    clearFile(false);
});

// JD文件上传事件
jdUploadArea.addEventListener('click', () => jdFileInput.click());

jdUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    jdUploadArea.classList.add('dragover');
});

jdUploadArea.addEventListener('dragleave', () => {
    jdUploadArea.classList.remove('dragover');
});

jdUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    jdUploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0], true);
    }
});

jdFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0], true);
    }
});

removeJdFile.addEventListener('click', (e) => {
    e.stopPropagation();
    clearFile(true);
});

function handleFileSelect(file, isJdFile) {
    const validExtensions = ['.pdf', '.docx', '.jpg', '.jpeg', '.png', '.gif'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validExtensions.includes(fileExtension)) {
        alert('仅支持 PDF、DOCX 和图片格式的文件');
        return;
    }
    
    if (isJdFile) {
        selectedJdFile = file;
        jdUploadArea.querySelector('.upload-placeholder').style.display = 'none';
        jdFileInfo.style.display = 'flex';
        jdFileName.textContent = file.name;
    } else {
        selectedFile = file;
        uploadArea.querySelector('.upload-placeholder').style.display = 'none';
        fileInfo.style.display = 'flex';
        fileName.textContent = file.name;
        analyzeBtn.disabled = false;
    }
}

function clearFile(isJdFile) {
    if (isJdFile) {
        selectedJdFile = null;
        jdFileInput.value = '';
        jdUploadArea.querySelector('.upload-placeholder').style.display = 'block';
        jdFileInfo.style.display = 'none';
    } else {
        selectedFile = null;
        fileInput.value = '';
        uploadArea.querySelector('.upload-placeholder').style.display = 'block';
        fileInfo.style.display = 'none';
        analyzeBtn.disabled = true;
    }
}

analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        alert('请先上传简历文件');
        return;
    }
    
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoading = analyzeBtn.querySelector('.btn-loading');
    
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    analyzeBtn.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('jd_text', jdText.value);
        
        if (selectedJdFile) {
            formData.append('jd_file', selectedJdFile);
        }
        
        const response = await fetch(`${API_BASE_URL}/full-analysis`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('分析失败');
        }
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result.data);
        } else {
            throw new Error(result.message || '分析失败');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('分析过程中出现错误: ' + error.message);
    } finally {
        btnText.style.display = 'inline-flex';
        btnLoading.style.display = 'none';
        analyzeBtn.disabled = false;
    }
});

function displayResults(data) {
    resultsSection.style.display = 'block';
    
    displayBasicInfo(data.resume_info);
    displayBackgroundInfo(data.resume_info);
    
    if (data.jd_analysis && data.match_result) {
        matchTab.style.display = 'block';
        displayMatchResults(data.match_result);
    } else {
        matchTab.style.display = 'none';
    }
    
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayBasicInfo(resumeInfo) {
    const basicInfo = document.getElementById('basicInfo');
    const basic = resumeInfo.basic_info || {};
    const job = resumeInfo.job_info || {};
    
    basicInfo.innerHTML = `
        <div class="info-item">
            <label>姓名</label>
            <span>${basic.name || 'N/A'}</span>
        </div>
        <div class="info-item">
            <label>电话</label>
            <span>${basic.phone || 'N/A'}</span>
        </div>
        <div class="info-item">
            <label>邮箱</label>
            <span>${basic.email || 'N/A'}</span>
        </div>
        <div class="info-item">
            <label>地址</label>
            <span>${basic.address || 'N/A'}</span>
        </div>
        <div class="info-item">
            <label>求职意向</label>
            <span>${job.job_intention || 'N/A'}</span>
        </div>
        <div class="info-item">
            <label>期望薪资</label>
            <span>${job.expected_salary || 'N/A'}</span>
        </div>
    `;
}

function displayBackgroundInfo(resumeInfo) {
    const background = resumeInfo.background_info || {};
    
    const educationInfo = document.getElementById('educationInfo');
    const education = background.education || [];
    
    if (education.length > 0) {
        educationInfo.innerHTML = education.map(edu => `
            <div class="info-list-item">
                <h4>${edu.school || 'N/A'}</h4>
                <p>${edu.major || ''} ${edu.degree || ''} ${edu.graduation_time || ''}</p>
            </div>
        `).join('');
    } else {
        educationInfo.innerHTML = '<p>暂无教育背景信息</p>';
    }
    
    const workInfo = document.getElementById('workInfo');
    const work = background.work_experience || [];
    
    if (work.length > 0) {
        workInfo.innerHTML = work.map(job => `
            <div class="info-list-item">
                <h4>${job.company || 'N/A'} - ${job.position || ''}</h4>
                <p>${job.period || ''}</p>
                <p>${job.description || ''}</p>
            </div>
        `).join('');
    } else {
        workInfo.innerHTML = '<p>暂无工作经历信息</p>';
    }
    
    const projectInfo = document.getElementById('projectInfo');
    const projects = background.projects || [];
    
    if (projects.length > 0) {
        projectInfo.innerHTML = projects.map(proj => `
            <div class="info-list-item">
                <h4>${proj.name || 'N/A'}</h4>
                <p><strong>职责：</strong>${proj.responsibility || ''}</p>
                <p><strong>成果：</strong>${proj.achievement || ''}</p>
            </div>
        `).join('');
    } else {
        projectInfo.innerHTML = '<p>暂无项目经历信息</p>';
    }
    
    const researchInfo = document.getElementById('researchInfo');
    const research = background.research_experience || [];
    
    if (research.length > 0) {
        researchInfo.innerHTML = research.map(res => `
            <div class="info-list-item">
                <h4>${res.field || 'N/A'}</h4>
                <p><strong>研究内容：</strong>${res.content || ''}</p>
                <p><strong>成果：</strong>${res.achievements || ''}</p>
                ${res.papers && res.papers.length > 0 ? `<p><strong>论文：</strong>${res.papers.join('; ')}</p>` : ''}
            </div>
        `).join('');
    } else {
        researchInfo.innerHTML = '<p>暂无科研经历信息</p>';
    }
    
    const academicInfo = document.getElementById('academicInfo');
    const academic = background.academic_experience || [];
    
    if (academic.length > 0) {
        academicInfo.innerHTML = academic.map(aca => `
            <div class="info-list-item">
                <h4>${aca.activity || 'N/A'}</h4>
                ${aca.awards && aca.awards.length > 0 ? `<p><strong>奖项：</strong>${aca.awards.join('; ')}</p>` : ''}
                ${aca.positions && aca.positions.length > 0 ? `<p><strong>任职：</strong>${aca.positions.join('; ')}</p>` : ''}
            </div>
        `).join('');
    } else {
        academicInfo.innerHTML = '<p>暂无学术经历信息</p>';
    }
    
    const skillsInfo = document.getElementById('skillsInfo');
    const skills = background.skills || [];
    const certificates = background.certificates || [];
    
    let skillsHtml = '';
    if (skills.length > 0) {
        const skillsText = skills.map(skill => typeof skill === 'object' ? JSON.stringify(skill) : skill).join('; ');
        skillsHtml += '<div class="info-list-item"><h4>技能</h4><p>' + skillsText + '</p></div>';
    }
    if (certificates.length > 0) {
        const certificatesText = certificates.map(cert => typeof cert === 'object' ? JSON.stringify(cert) : cert).join('; ');
        skillsHtml += '<div class="info-list-item"><h4>证书</h4><p>' + certificatesText + '</p></div>';
    }
    if (skillsHtml) {
        skillsInfo.innerHTML = skillsHtml;
    } else {
        skillsInfo.innerHTML = '<p>暂无技能证书信息</p>';
    }
    
    const otherInfo = document.getElementById('otherInfo');
    const other = background.other_info || [];
    
    if (other.length > 0) {
        otherInfo.innerHTML = other.map(item => `
            <div class="info-list-item">
                <p>${typeof item === 'object' ? JSON.stringify(item) : item}</p>
            </div>
        `).join('');
    } else {
        otherInfo.innerHTML = '<p>暂无其他信息</p>';
    }
}

function displayMatchResults(matchResult) {
    const matchContent = document.getElementById('matchContent');
    const noJdMessage = document.getElementById('noJdMessage');
    
    matchContent.style.display = 'block';
    noJdMessage.style.display = 'none';
    
    const scoreGrid = document.getElementById('scoreGrid');
    const scores = matchResult.match_score || {};
    
    scoreGrid.innerHTML = `
        <div class="score-card">
            <h4>技能匹配率</h4>
            <div class="score-value">${scores.skills_match || 0}%</div>
        </div>
        <div class="score-card">
            <h4>经验相关性</h4>
            <div class="score-value">${scores.experience_relevance || 0}%</div>
        </div>
        <div class="score-card">
            <h4>学历匹配度</h4>
            <div class="score-value">${scores.education_match || 0}%</div>
        </div>
        <div class="score-card">
            <h4>综合匹配度</h4>
            <div class="score-value">${scores.overall_match || 0}%</div>
        </div>
    `;
    
    const strengths = matchResult.strengths || {};
    const strengthsList = document.getElementById('strengthsList');
    
    let strengthsHtml = '';
    if (strengths.matched_skills && strengths.matched_skills.length > 0) {
        strengthsHtml += `<h4>匹配的技能</h4><ul class="match-list strengths-list">${strengths.matched_skills.map(s => `<li>${s}</li>`).join('')}</ul>`;
    }
    if (strengths.relevant_experience && strengths.relevant_experience.length > 0) {
        strengthsHtml += `<h4>相关经验</h4><ul class="match-list strengths-list">${strengths.relevant_experience.map(e => `<li>${e}</li>`).join('')}</ul>`;
    }
    if (strengths.other_strengths && strengths.other_strengths.length > 0) {
        strengthsHtml += `<h4>其他优势</h4><ul class="match-list strengths-list">${strengths.other_strengths.map(s => `<li>${s}</li>`).join('')}</ul>`;
    }
    strengthsList.innerHTML = strengthsHtml || '<p>暂无优势信息</p>';
    
    const gaps = matchResult.gaps || {};
    const gapsList = document.getElementById('gapsList');
    
    let gapsHtml = '';
    if (gaps.missing_skills && gaps.missing_skills.length > 0) {
        gapsHtml += `<h4>缺失的技能</h4><ul class="match-list gaps-list">${gaps.missing_skills.map(s => `<li>${s}</li>`).join('')}</ul>`;
    }
    if (gaps.experience_gaps && gaps.experience_gaps.length > 0) {
        gapsHtml += `<h4>经验差距</h4><ul class="match-list gaps-list">${gaps.experience_gaps.map(g => `<li>${g}</li>`).join('')}</ul>`;
    }
    if (gaps.other_gaps && gaps.other_gaps.length > 0) {
        gapsHtml += `<h4>其他差距</h4><ul class="match-list gaps-list">${gaps.other_gaps.map(g => `<li>${g}</li>`).join('')}</ul>`;
    }
    gapsList.innerHTML = gapsHtml || '<p>暂无明显差距</p>';
    
    const suggestions = matchResult.suggestions || {};
    const suggestionsList = document.getElementById('suggestionsList');
    
    let suggestionsHtml = '';
    if (suggestions.skills_to_learn && suggestions.skills_to_learn.length > 0) {
        suggestionsHtml += `<h4>需要学习的技能</h4><ul class="match-list suggestions-list">${suggestions.skills_to_learn.map(s => `<li>${s}</li>`).join('')}</ul>`;
    }
    if (suggestions.recommended_projects && suggestions.recommended_projects.length > 0) {
        suggestionsHtml += `<h4>建议补充的项目</h4><ul class="match-list suggestions-list">${suggestions.recommended_projects.map(p => `<li>${p}</li>`).join('')}</ul>`;
    }
    if (suggestions.other_suggestions && suggestions.other_suggestions.length > 0) {
        suggestionsHtml += `<h4>其他建议</h4><ul class="match-list suggestions-list">${suggestions.other_suggestions.map(s => `<li>${s}</li>`).join('')}</ul>`;
    }
    suggestionsList.innerHTML = suggestionsHtml || '<p>暂无建议信息</p>';
}

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        tab.classList.add('active');
        const tabId = tab.dataset.tab;
        document.getElementById(tabId).classList.add('active');
    });
});

// Agent聊天功能
const agentChat = document.getElementById('agentChat');
const agentQuery = document.getElementById('agentQuery');
const agentSendBtn = document.getElementById('agentSendBtn');

agentSendBtn.addEventListener('click', async () => {
    await sendAgentMessage();
});

agentQuery.addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
        await sendAgentMessage();
    }
});

async function sendAgentMessage() {
    const query = agentQuery.value.trim();
    if (!query) return;
    
    if (!selectedFile) {
        alert('请先上传简历文件');
        return;
    }
    
    // 添加用户消息
    addMessage('user', query);
    agentQuery.value = '';
    
    // 显示加载状态
    const loadingMessage = addMessage('agent', '分析中...', true);
    
    try {
        // 创建FormData并发送实际请求
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('query', query);
        
        // 使用fetch的流式处理
        const streamResponse = await fetch(`${API_BASE_URL}/agent-analysis`, {
            method: 'POST',
            body: formData
        });
        
        if (!streamResponse.ok) {
            throw new Error('Agent分析失败');
        }
        
        // 获取响应流
        const reader = streamResponse.body.getReader();
        const decoder = new TextDecoder();
        
        // 移除加载消息
        loadingMessage.remove();
        
        // 创建一个消息容器用于显示流式输出
        const messageContainer = document.createElement('div');
        messageContainer.className = 'agent-message';
        messageContainer.innerHTML = `
            <div class="agent-avatar">🤖</div>
            <div class="agent-content">
                <div class="agent-thinking" style="display: none;"></div>
                <div class="agent-code" style="display: none;"></div>
                <div class="agent-answer"></div>
            </div>
        `;
        agentChat.appendChild(messageContainer);
        agentChat.scrollTop = agentChat.scrollHeight;
        
        let buffer = '';
        
        // 处理流数据
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
                break;
            }
            
            buffer += decoder.decode(value, { stream: true });
            
            // 处理SSE格式的数据
            const lines = buffer.split('\n\n');
            buffer = lines.pop(); // 保留未完成的行
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.substring(6);
                    try {
                        const jsonData = JSON.parse(data);
                        if (jsonData.type === 'step') {
                            const content = jsonData.content;
                            
                            // 更新思考过程
                            if (content.thinking) {
                                const thinkingElement = messageContainer.querySelector('.agent-thinking');
                                thinkingElement.style.display = 'block';
                                thinkingElement.innerHTML = `<strong>思考过程:</strong><p>${content.thinking}</p>`;
                            }
                            
                            // 更新代码
                            if (content.code) {
                                const codeElement = messageContainer.querySelector('.agent-code');
                                codeElement.style.display = 'block';
                                codeElement.innerHTML = `<strong>执行代码:</strong><pre><code>${content.code}</code></pre>`;
                            }
                            
                            // 更新输出
                            if (content.output) {
                                const answerElement = messageContainer.querySelector('.agent-answer');
                                const outputContent = typeof content.output === 'object' ? JSON.stringify(content.output, null, 2) : content.output;
                                answerElement.innerHTML += `<strong>执行结果:</strong><p>${outputContent}</p>`;
                            }
                            
                            // 更新最终答案
                            if (content.final_answer) {
                                const answerElement = messageContainer.querySelector('.agent-answer');
                                const finalAnswerContent = typeof content.final_answer === 'object' ? JSON.stringify(content.final_answer, null, 2) : content.final_answer;
                                answerElement.innerHTML += `<strong>最终答案:</strong><p>${finalAnswerContent}</p>`;
                            }
                            
                            // 滚动到底部
                            agentChat.scrollTop = agentChat.scrollHeight;
                        }
                    } catch (e) {
                        console.error('解析流式数据失败:', e);
                    }
                }
            }
        }
        
    } catch (error) {
        console.error('Error:', error);
        // 移除加载消息
        loadingMessage.remove();
        addMessage('agent', `抱歉，分析过程中出现错误: ${error.message}`);
    }
}

function addMessage(sender, content, isLoading = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'agent-message';
    
    if (sender === 'user') {
        messageDiv.innerHTML = `
            <div class="agent-avatar">👤</div>
            <div class="agent-content" style="background: var(--primary-color); color: white;">
                <p>${content}</p>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="agent-avatar">🤖</div>
            <div class="agent-content">
                <p>${content}</p>
            </div>
        `;
        if (isLoading) {
            messageDiv.style.opacity = '0.7';
        }
    }
    
    agentChat.appendChild(messageDiv);
    agentChat.scrollTop = agentChat.scrollHeight;
    return messageDiv;
}
