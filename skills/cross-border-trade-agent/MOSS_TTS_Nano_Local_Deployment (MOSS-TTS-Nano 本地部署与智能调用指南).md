# MOSS-TTS-Nano 本地部署与智能调用指南

> **生成时间**: 2026 年 4 月 20 日 23:07 CST  
> **版本**: v1.0  
> **部署方式**: ONNX CPU (推荐) / PyTorch  
> **智能调用**: API 封装 + 批量处理 + 自动化工作流

---

## 📊 目录

1. [系统要求](#系统要求)
2. [快速部署 (5 分钟)](#快速部署 -5-分钟)
3. [API 封装](#api-封装)
4. [智能调用示例](#智能调用示例)
5. [批量处理](#批量处理)
6. [自动化工作流](#自动化工作流)
7. [跨境贸易集成](#跨境贸易集成)
8. [性能优化](#性能优化)
9. [故障排查](#故障排查)

---

## 💻 系统要求

### 最低配置

| 组件 | 要求 |
|------|------|
| **CPU** | 4 核 + (支持 AVX2) |
| **内存** | 4GB+ |
| **存储** | 2GB (模型 + 依赖) |
| **系统** | Windows 10 / macOS 10.15+ / Linux |
| **Python** | 3.10 - 3.12 |

### 推荐配置

| 组件 | 要求 |
|------|------|
| **CPU** | 8 核 + (M1/M2/M3 或 Intel i7+) |
| **内存** | 8GB+ |
| **存储** | 5GB SSD |
| **GPU** | 可选 (PyTorch 版本加速) |

---

## 🚀 快速部署 (5 分钟)

### 方案 A: ONNX CPU 版本 (推荐⭐)

**优势**: 无需 GPU，2x 性能，生产就绪

#### 步骤 1: 创建虚拟环境

```bash
# macOS/Linux
python3 -m venv moss-tts
source moss-tts/bin/activate

# Windows
python -m venv moss-tts
moss-tts\Scripts\activate
```

#### 步骤 2: 克隆仓库

```bash
git clone https://github.com/OpenMOSS/MOSS-TTS-Nano.git
cd MOSS-TTS-Nano
```

#### 步骤 3: 安装依赖

```bash
# 安装 ONNX Runtime (CPU)
pip install onnxruntime

# 安装其他依赖
pip install -r requirements.txt

# 安装项目本身
pip install -e .
```

#### 步骤 4: 测试安装

```bash
# 检查 moss-tts-nano 命令是否可用
moss-tts-nano --help
```

#### 步骤 5: 首次推理 (自动下载模型)

```bash
moss-tts-nano generate \
  --backend onnx \
  --text "欢迎使用 MOSS-TTS-Nano 本地部署。" \
  --output test_output.wav
```

**首次运行会自动下载**:
- MOSS-TTS-Nano-100M-ONNX (~300MB)
- MOSS-Audio-Tokenizer-Nano-ONNX (~100MB)

---

### 方案 B: PyTorch 版本

**优势**: 最新功能，GPU 加速支持

```bash
# 创建环境
conda create -n moss-tts python=3.12 -y
conda activate moss-tts

# 克隆仓库
git clone https://github.com/OpenMOSS/MOSS-TTS-Nano.git
cd MOSS-TTS-Nano

# 安装 PyTorch (根据系统选择)
# CPU 版本
pip install torch torchvision torchaudio

# GPU 版本 (NVIDIA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装项目依赖
pip install -r requirements.txt
pip install -e .

# 测试
python infer.py \
  --text "PyTorch 版本测试成功。" \
  --output test_pytorch.wav
```

---

## 🔌 API 封装

### 封装为 REST API (FastAPI)

创建文件：`tts_api.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOSS-TTS-Nano REST API Server
智能调用接口 - 支持语音克隆/多语言/批量处理
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import subprocess
import os
import uuid
from pathlib import Path

app = FastAPI(
    title="MOSS-TTS-Nano API",
    description="本地 TTS 服务 - 支持语音克隆和多语言",
    version="1.0.0"
)

# 配置
OUTPUT_DIR = Path("generated_audio")
OUTPUT_DIR.mkdir(exist_ok=True)

class TTSRequest(BaseModel):
    text: str
    language: str = "zh"  # zh, en, ja, ko, etc.
    voice_id: Optional[str] = None  # 内置声音 ID
    speed: float = 1.0
    output_format: str = "wav"  # wav, mp3, ogg

class TTSResponse(BaseModel):
    success: bool
    audio_url: Optional[str] = None
    duration: Optional[float] = None
    message: str

@app.get("/")
async def root():
    return {
        "service": "MOSS-TTS-Nano API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "generate": "POST /generate",
            "clone": "POST /clone (上传参考音频)",
            "batch": "POST /batch (批量生成)",
            "voices": "GET /voices (获取内置声音列表)"
        }
    }

@app.post("/generate", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """
    基础 TTS 生成 (使用内置声音)
    """
    try:
        output_filename = f"{uuid.uuid4()}.{request.output_format}"
        output_path = OUTPUT_DIR / output_filename
        
        # 构建命令
        cmd = [
            "moss-tts-nano", "generate",
            "--backend", "onnx",
            "--text", request.text,
            "--output", str(output_path)
        ]
        
        # 执行
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        
        return TTSResponse(
            success=True,
            audio_url=f"/audio/{output_filename}",
            message="生成成功"
        )
        
    except Exception as e:
        return TTSResponse(
            success=False,
            message=str(e)
        )

@app.post("/clone")
async def clone_voice(
    text: str,
    voice_file: UploadFile = File(...),
    output_format: str = "wav"
):
    """
    语音克隆 - 上传参考音频，克隆声音
    """
    try:
        # 保存上传的参考音频
        voice_path = OUTPUT_DIR / f"voice_{uuid.uuid4()}.wav"
        with open(voice_path, "wb") as f:
            f.write(await voice_file.read())
        
        # 生成输出文件名
        output_filename = f"{uuid.uuid4()}.{output_format}"
        output_path = OUTPUT_DIR / output_filename
        
        # 执行语音克隆
        cmd = [
            "moss-tts-nano", "generate",
            "--backend", "onnx",
            "--prompt-speech", str(voice_path),
            "--text", text,
            "--output", str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        
        # 清理参考音频
        os.remove(voice_path)
        
        return {
            "success": True,
            "audio_url": f"/audio/{output_filename}",
            "cloned_from": voice_file.filename,
            "message": "语音克隆成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch")
async def batch_generate(requests: List[TTSRequest]):
    """
    批量生成 - 一次处理多个 TTS 请求
    """
    results = []
    
    for i, req in enumerate(requests):
        try:
            output_filename = f"batch_{i}_{uuid.uuid4()}.{req.output_format}"
            output_path = OUTPUT_DIR / output_filename
            
            cmd = [
                "moss-tts-nano", "generate",
                "--backend", "onnx",
                "--text", req.text,
                "--output", str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                results.append({
                    "index": i,
                    "success": True,
                    "audio_url": f"/audio/{output_filename}"
                })
            else:
                results.append({
                    "index": i,
                    "success": False,
                    "error": result.stderr
                })
                
        except Exception as e:
            results.append({
                "index": i,
                "success": False,
                "error": str(e)
            })
    
    return {
        "total": len(requests),
        "success": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "results": results
    }

@app.get("/voices")
async def list_voices():
    """
    获取内置声音列表 (示例)
    """
    voices = [
        {"id": "zh_female_1", "name": "中文女声 1", "language": "zh"},
        {"id": "zh_male_1", "name": "中文男声 1", "language": "zh"},
        {"id": "en_female_1", "name": "English Female 1", "language": "en"},
        {"id": "en_male_1", "name": "English Male 1", "language": "en"},
        {"id": "ja_female_1", "name": "日本語 女性 1", "language": "ja"},
    ]
    return {"voices": voices}

@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    """
    提供音频文件下载
    """
    audio_path = OUTPUT_DIR / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(audio_path, media_type="audio/wav")

# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 启动 API 服务

```bash
# 安装 FastAPI 和 Uvicorn
pip install fastapi uvicorn python-multipart

# 启动服务
python tts_api.py

# 或使用 uvicorn 直接启动
uvicorn tts_api:app --host 0.0.0.0 --port 8000 --reload
```

**访问**: http://localhost:8000

**API 文档**: http://localhost:8000/docs

---

## 🎯 智能调用示例

### 示例 1: Python 调用

创建文件：`test_api.py`

```python
#!/usr/bin/env python3
import requests

# API 地址
API_URL = "http://localhost:8000"

# 1. 基础 TTS 生成
def basic_tts():
    response = requests.post(
        f"{API_URL}/generate",
        json={
            "text": "欢迎使用智能 TTS 服务。",
            "language": "zh",
            "output_format": "wav"
        }
    )
    result = response.json()
    print(f"生成结果：{result}")
    return result

# 2. 语音克隆
def voice_clone():
    # 准备参考音频
    with open("my_voice.wav", "rb") as f:
        voice_file = f.read()
    
    response = requests.post(
        f"{API_URL}/clone",
        files={"voice_file": ("my_voice.wav", voice_file, "audio/wav")},
        data={"text": "这是用我的声音克隆生成的语音。"}
    )
    result = response.json()
    print(f"克隆结果：{result}")
    return result

# 3. 批量生成
def batch_tts():
    requests_data = [
        {"text": "第一条消息", "language": "zh"},
        {"text": "Second message", "language": "en"},
        {"text": "三番目のメッセージ", "language": "ja"}
    ]
    
    response = requests.post(
        f"{API_URL}/batch",
        json=requests_data
    )
    result = response.json()
    print(f"批量结果：{result}")
    return result

# 测试
if __name__ == "__main__":
    print("=== 基础 TTS ===")
    basic_tts()
    
    print("\n=== 语音克隆 ===")
    voice_clone()
    
    print("\n=== 批量生成 ===")
    batch_tts()
```

---

### 示例 2: cURL 调用

```bash
# 1. 基础 TTS
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "欢迎使用智能 TTS 服务。",
    "language": "zh"
  }'

# 2. 语音克隆
curl -X POST "http://localhost:8000/clone" \
  -F "voice_file=@my_voice.wav" \
  -F "text=这是用我的声音克隆生成的语音。"

# 3. 批量生成
curl -X POST "http://localhost:8000/batch" \
  -H "Content-Type: application/json" \
  -d '[
    {"text": "第一条消息", "language": "zh"},
    {"text": "Second message", "language": "en"}
  ]'
```

---

### 示例 3: JavaScript/Node.js 调用

```javascript
// test_api.js
const axios = require('axios');
const fs = require('fs');

const API_URL = 'http://localhost:8000';

// 基础 TTS
async function basicTTS() {
  const response = await axios.post(`${API_URL}/generate`, {
    text: '欢迎使用智能 TTS 服务。',
    language: 'zh'
  });
  console.log('生成结果:', response.data);
  return response.data;
}

// 语音克隆
async function voiceClone() {
  const voiceBuffer = fs.readFileSync('my_voice.wav');
  const formData = new FormData();
  formData.append('voice_file', new Blob([voiceBuffer]), 'my_voice.wav');
  formData.append('text', '这是用我的声音克隆生成的语音。');
  
  const response = await axios.post(`${API_URL}/clone`, formData, {
    headers: formData.getHeaders()
  });
  console.log('克隆结果:', response.data);
  return response.data;
}

// 批量生成
async function batchTTS() {
  const response = await axios.post(`${API_URL}/batch`, [
    {text: '第一条消息', language: 'zh'},
    {text: 'Second message', language: 'en'},
    {text: '三番目のメッセージ', language: 'ja'}
  ]);
  console.log('批量结果:', response.data);
  return response.data;
}

// 测试
(async () => {
  await basicTTS();
  await voiceClone();
  await batchTTS();
})();
```

---

## 📦 批量处理

### 批量 TTS 脚本

创建文件：`batch_processor.py`

```python
#!/usr/bin/env python3
"""
批量 TTS 处理器
支持：CSV/Excel 导入，多语言，并发处理
"""

import pandas as pd
import requests
import concurrent.futures
from pathlib import Path
import time
from tqdm import tqdm

class BatchTTSProcessor:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.output_dir = Path("batch_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def load_csv(self, csv_file):
        """加载 CSV 文件"""
        df = pd.read_csv(csv_file)
        return df
    
    def load_excel(self, excel_file):
        """加载 Excel 文件"""
        df = pd.read_excel(excel_file)
        return df
    
    def generate_single(self, item):
        """生成单个 TTS"""
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json={
                    "text": item["text"],
                    "language": item.get("language", "zh"),
                    "output_format": "wav"
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "text": item["text"],
                    "audio_url": result.get("audio_url"),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "text": item["text"],
                    "audio_url": None,
                    "error": response.text
                }
        except Exception as e:
            return {
                "success": False,
                "text": item["text"],
                "audio_url": None,
                "error": str(e)
            }
    
    def process_batch(self, df, max_workers=4):
        """批量处理"""
        items = df.to_dict("records")
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.generate_single, item): i for i, item in enumerate(items)}
            
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(items)):
                result = future.result()
                results.append(result)
        
        # 保存结果
        results_df = pd.DataFrame(results)
        results_df.to_csv(self.output_dir / "batch_results.csv", index=False, encoding='utf-8-sig')
        
        # 统计
        success_count = sum(1 for r in results if r["success"])
        print(f"\n处理完成:")
        print(f"  总计：{len(items)}")
        print(f"  成功：{success_count}")
        print(f"  失败：{len(items) - success_count}")
        print(f"  结果保存：{self.output_dir / 'batch_results.csv'}")
        
        return results

# 使用示例
if __name__ == "__main__":
    processor = BatchTTSProcessor()
    
    # 加载数据
    df = processor.load_csv("tts_texts.csv")
    # 或
    # df = processor.load_excel("tts_texts.xlsx")
    
    print(f"加载了 {len(df)} 条文本")
    print(df.head())
    
    # 批量处理
    results = processor.process_batch(df, max_workers=4)
```

### CSV 示例格式

创建文件：`tts_texts.csv`

```csv
text,language,output_name
欢迎使用批量 TTS 服务，zh,output_001
Welcome to batch TTS service,en,output_002
バッチ TTS サービスへようこそ，ja,output_003
```

---

## 🔄 自动化工作流

### 工作流 1: 产品演示视频自动生成

```python
#!/usr/bin/env python3
"""
产品演示视频配音自动化
输入：产品脚本 → 输出：多语言配音视频
"""

import requests
import subprocess
from pathlib import Path

class VideoDubbingWorkflow:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.output_dir = Path("video_outputs")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_voiceover(self, script, language="en"):
        """生成配音"""
        response = requests.post(
            f"{self.api_url}/generate",
            json={
                "text": script,
                "language": language
            }
        )
        return response.json()
    
    def merge_audio_video(self, video_file, audio_file, output_file):
        """合并视频和音频 (使用 ffmpeg)"""
        cmd = [
            "ffmpeg", "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-y", output_file
        ]
        subprocess.run(cmd, check=True)
    
    def process_product_demo(self, product_name, script_zh, script_en):
        """处理产品演示"""
        print(f"处理产品：{product_name}")
        
        # 生成中文配音
        print("  生成中文配音...")
        zh_result = self.generate_voiceover(script_zh, "zh")
        
        # 生成英文配音
        print("  生成英文配音...")
        en_result = self.generate_voiceover(script_en, "en")
        
        # 下载音频文件
        zh_audio = self.download_audio(zh_result["audio_url"])
        en_audio = self.download_audio(en_result["audio_url"])
        
        # 合并视频 (假设有原始视频)
        video_file = f"videos/{product_name}_raw.mp4"
        if Path(video_file).exists():
            self.merge_audio_video(video_file, zh_audio, 
                                   self.output_dir / f"{product_name}_zh.mp4")
            self.merge_audio_video(video_file, en_audio,
                                   self.output_dir / f"{product_name}_en.mp4")
            print(f"  ✅ 完成：{product_name}")
        else:
            print(f"  ⚠️ 视频文件不存在：{video_file}")
        
        return {"zh": zh_result, "en": en_result}
    
    def download_audio(self, audio_url):
        """下载音频文件"""
        response = requests.get(f"{self.api_url}{audio_url}")
        output_file = self.output_dir / f"audio_{audio_url.split('/')[-1]}"
        with open(output_file, "wb") as f:
            f.write(response.content)
        return output_file

# 使用示例
if __name__ == "__main__":
    workflow = VideoDubbingWorkflow()
    
    # 产品演示脚本
    script_zh = "这款模块化房屋采用钢结构设计，60 天快速交付，适合矿业营地和度假村建设。"
    script_en = "This modular house features steel structure design, 60-day fast delivery, perfect for mining camps and resort construction."
    
    workflow.process_product_demo("Modular_House_001", script_zh, script_en)
```

---

### 工作流 2: 多语言客服系统

```python
#!/usr/bin/env python3
"""
多语言客服语音系统
输入：客户问题 → 输出：多语言语音回答
"""

import requests
import openai  # 或其他 LLM

class MultilingualCustomerService:
    def __init__(self):
        self.tts_api = "http://localhost:8000"
        self.llm_api = "https://api.openai.com/v1"  # 示例
        self.api_key = "your-api-key"
    
    def understand_question(self, audio_file):
        """语音识别 (使用 Whisper)"""
        # 这里调用 Whisper API 或本地模型
        # 简化示例
        return "客户询问产品价格"
    
    def generate_answer(self, question, language="en"):
        """生成回答 (使用 LLM)"""
        # 调用 ChatGPT 或其他 LLM
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a helpful customer service agent. Respond in {language}."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    
    def synthesize_speech(self, text, language="en"):
        """合成语音"""
        response = requests.post(
            f"{self.tts_api}/generate",
            json={
                "text": text,
                "language": language
            }
        )
        return response.json()
    
    def process_inquiry(self, audio_file, customer_language="en"):
        """处理客户咨询"""
        # 1. 语音识别
        question = self.understand_question(audio_file)
        print(f"客户问题：{question}")
        
        # 2. 生成回答
        answer = self.generate_answer(question, customer_language)
        print(f"回答：{answer}")
        
        # 3. 合成语音
        audio_result = self.synthesize_speech(answer, customer_language)
        print(f"语音生成：{audio_result}")
        
        return audio_result

# 使用示例
if __name__ == "__main__":
    service = MultilingualCustomerService()
    service.process_inquiry("customer_question.wav", "en")
```

---

## 🌐 跨境贸易集成

### 集成到你的 CRM 系统

```python
#!/usr/bin/env python3
"""
跨境贸易 CRM 集成
自动为每个客户生成多语言跟进语音
"""

import requests
from datetime import datetime

class CRMIntegration:
    def __init__(self, crm_api, tts_api="http://localhost:8000"):
        self.crm_api = crm_api
        self.tts_api = tts_api
    
    def get_follow_up_tasks(self):
        """获取今日跟进任务"""
        # 从 CRM 系统获取
        response = requests.get(f"{self.crm_api}/tasks/today")
        return response.json()
    
    def generate_followup_voice(self, customer_name, language, message):
        """生成跟进语音"""
        response = requests.post(
            f"{self.tts_api}/generate",
            json={
                "text": message,
                "language": language
            }
        )
        return response.json()
    
    def send_voice_message(self, customer_id, audio_url):
        """发送语音消息"""
        # 通过 WhatsApp/Telegram/邮件发送
        pass
    
    def daily_followup(self):
        """执行每日跟进"""
        tasks = self.get_follow_up_tasks()
        
        for task in tasks:
            customer_name = task["customer_name"]
            language = task["language"]
            message = task["followup_message"]
            
            # 生成语音
            audio_result = self.generate_followup_voice(
                customer_name, language, message
            )
            
            if audio_result["success"]:
                # 发送语音
                self.send_voice_message(task["customer_id"], audio_result["audio_url"])
                print(f"✅ 已发送跟进语音给 {customer_name}")
            else:
                print(f"❌ 生成失败：{customer_name}")

# 使用示例
if __name__ == "__main__":
    crm = CRMIntegration(crm_api="https://your-crm.com/api")
    crm.daily_followup()
```

---

## ⚡ 性能优化

### 1. 模型预热

```python
# 启动时预热模型
def warmup_model():
    requests.post(
        "http://localhost:8000/generate",
        json={"text": "预热", "language": "zh"}
    )
    print("模型预热完成")

# 在 API 启动时调用
warmup_model()
```

### 2. 并发控制

```python
# 限制并发请求数
from threading import Semaphore

max_concurrent = 4
semaphore = Semaphore(max_concurrent)

def generate_with_limit(text):
    with semaphore:
        return generate_tts(text)
```

### 3. 缓存机制

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_generate(text_hash, language):
    # 检查是否已生成
    if exists_in_cache(text_hash):
        return get_from_cache(text_hash)
    else:
        result = generate_tts(text_hash, language)
        save_to_cache(text_hash, result)
        return result
```

### 4. GPU 加速 (可选)

```bash
# 如果使用 PyTorch 版本 + NVIDIA GPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 启动时指定 GPU
CUDA_VISIBLE_DEVICES=0 python tts_api.py
```

---

## 🔧 故障排查

### 常见问题

#### 1. 模型下载失败

```bash
# 手动下载模型
cd models
wget https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Nano-100M-ONNX/resolve/main/model.onnx
```

#### 2. 内存不足

```bash
# 限制并发数
export OMP_NUM_THREADS=2
python tts_api.py
```

#### 3. 音频质量差

```bash
# 检查参考音频质量
# 要求：48kHz, 单声道，3-10 秒，清晰人声
```

#### 4. API 响应慢

```bash
# 检查 CPU 使用率
top -pid $(pgrep -f tts_api)

# 考虑使用 GPU 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 📞 快速参考

### 命令速查

```bash
# 启动 API 服务
python tts_api.py

# 基础生成
moss-tts-nano generate --text "你好" --backend onnx

# 语音克隆
moss-tts-nano generate --prompt-speech voice.wav --text "你好" --backend onnx

# Web Demo
moss-tts-nano serve --backend onnx

# 批量处理
python batch_processor.py

# 视频配音
python video_dubbing.py
```

### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 服务状态 |
| `/generate` | POST | 基础 TTS |
| `/clone` | POST | 语音克隆 |
| `/batch` | POST | 批量生成 |
| `/voices` | GET | 声音列表 |
| `/audio/{filename}` | GET | 下载音频 |

---

**部署完成时间**: 2026-04-20 23:07 CST  
**文件**: MOSS_TTS_Nano_Local_Deployment (MOSS-TTS-Nano 本地部署与智能调用指南).md  
**版本**: v1.0  

---

*太一 AGI · 本地部署专家 · 智能自动化*
