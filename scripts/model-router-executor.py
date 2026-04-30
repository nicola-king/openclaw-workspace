#!/usr/bin/env python3
# scripts/model-router-executor.py

"""
太一模型路由执行器 v2.0

功能：
1. 根据任务类型自动选择模型
2. 集成百炼配额监控（自动切换）
3. 三层模型池（本地/百炼/Gemini）
4. 智能记忆检索
5. 使用统计记录

使用：
    python3 scripts/model-router-executor.py "用户请求"

架构：
    L1 · 本地层 → Qwen 2.5 7B（简单问题，¥0）
    L2 · 百炼层 → qwen3.5-plus（中等任务，¥0.05/1K，限额时切 Gemini）
    L3 · Gemini 层 → gemini-2.5-pro（复杂任务/备用，免费）
"""

import os
import sys
import json
import sqlite3
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

# 配置
BASE_DIR = Path.home() / ".openclaw" / "workspace"
STATUS_FILE = BASE_DIR / "data" / "model-router-status.json"
INDEX_DB = BASE_DIR / "data" / "memory_index.db"
USAGE_LOG = BASE_DIR / "memory" / "model-usage-today.md"
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

# 模型配置
MODELS = {
    "local": {
        "name": "qwen2.5:7b-instruct-q4_K_M",
        "endpoint": OLLAMA_ENDPOINT,
        "cost_per_1k": 0.0,
        "max_context": 8192,
        "layer": "L1",
        "description": "本地模型（简单问题）"
    },
    "bailian": {
        "name": "qwen3.5-plus",
        "endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "cost_per_1k": 0.05,
        "max_context": 131072,
        "layer": "L2",
        "description": "百炼 Coding Plan（中等任务）"
    },
    "gemini": {
        "name": "gemini-2.5-pro",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent",
        "cost_per_1k": 0.0,  # 免费额度内
        "max_context": 1048576,
        "layer": "L3",
        "description": "Gemini 免费额度（复杂任务/备用）"
    }
}

def load_status() -> dict:
    """加载路由器状态"""
    if not STATUS_FILE.exists():
        return {
            "current_model": "qwen3.5-plus",
            "bailian_status": "normal"
        }
    
    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def estimate_tokens(text: str) -> int:
    """估算 Token 数量"""
    import re
    chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
    english = len(re.findall(r'[a-zA-Z]+', text))
    return int(chinese / 0.6 + english / 0.75)

def classify_task(query: str) -> Tuple[str, str, int]:
    """
    分类任务
    
    Returns:
        (task_type, complexity, token_estimate)
    """
    query_lower = query.lower()
    token_estimate = estimate_tokens(query)
    
    # 代码任务
    if any(kw in query_lower for kw in ['代码', '脚本', 'bug', '写函数', 'debug', 'python', 'javascript']):
        return "code", "medium", 5000
    
    # 简单任务
    if any(kw in query_lower for kw in ['你好', '谢谢', '再见', '几点', '天气', '是谁', '什么是']):
        return "chat", "easy", 500
    
    # 简单查询/翻译/润色
    if any(kw in query_lower for kw in ['翻译', '润色', '优化', '总结', '摘要']):
        if token_estimate < 2000:
            return "simple", "easy", 1000
    
    # 长文本
    if any(kw in query_lower for kw in ['文档', '报告', '文章', '文件', 'pdf']):
        if token_estimate > 10000:
            return "long_text", "hard", 50000
    
    # 复杂推理/分析
    if any(kw in query_lower for kw in ['分析', '对比', '评估', '为什么', '如何', '策略', '方案']):
        if token_estimate > 5000:
            return "analysis", "hard", 10000
        return "analysis", "medium", 5000
    
    # 创意写作
    if any(kw in query_lower for kw in ['写文章', '写故事', '写诗', '创意', '创作']):
        return "creative", "medium", 3000
    
    # 默认
    return "chat", "easy", 1000

def select_model(task_type: str, complexity: str, token_estimate: int) -> str:
    """
    选择模型（考虑配额状态）
    
    路由策略：
    1. 简单任务 → 本地 7B（无论配额状态）
    2. 中等任务 → 百炼（normal）/ Gemini（exhausted）
    3. 复杂任务 → Gemini（始终）
    """
    # 加载配额状态
    status = load_status()
    bailian_available = status.get("bailian_status") == "normal"
    
    # 规则 1：简单问题 → 本地 7B
    if complexity == "easy" and token_estimate < 8000:
        if task_type in ["simple", "chat", "calc"]:
            return "local"
    
    # 规则 2：复杂任务 → Gemini（始终）
    if complexity == "hard" or token_estimate >= 50000:
        return "gemini"
    
    # 规则 3：中等任务 → 百炼或 Gemini（取决于配额）
    if task_type == "code":
        return "bailian" if bailian_available else "gemini"
    
    if complexity == "medium":
        return "bailian" if bailian_available else "gemini"
    
    # 默认：根据配额状态选择
    return "bailian" if bailian_available else "gemini"

def search_memory(query: str, limit: int = 5) -> str:
    """FTS5 记忆检索"""
    if not INDEX_DB.exists():
        return ""
    
    conn = sqlite3.connect(INDEX_DB)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT content, section_name, source_file, tags,
                   bm25(memory_index, 1.0, 1.0, 0.5, 0.5) as score
            FROM memory_index
            WHERE memory_index MATCH ?
            ORDER BY score
            LIMIT ?
        ''', (query, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append(f"[{row[2]}#{row[1]}] {row[0][:200]}...")
        
        if results:
            return "\n\n相关记忆:\n" + "\n".join(results)
        return ""
    finally:
        conn.close()

def call_local_model(prompt: str) -> str:
    """调用本地 Ollama 模型"""
    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            json={
                "model": "qwen2.5:7b-instruct-q4_K_M",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 2048,
                    "temperature": 0.7,
                }
            },
            timeout=30
        )
        return response.json().get("response", "")
    except Exception as e:
        return f"[本地模型调用失败：{e}]"

def call_bailian_model(prompt: str) -> str:
    """调用百炼 API"""
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        return "[百炼 API Key 未配置]"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen3.5-plus",
        "input": {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        "parameters": {
            "max_tokens": 4096
        }
    }
    
    try:
        response = requests.post(
            MODELS["bailian"]["endpoint"],
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("output", {}).get("text", "")
        else:
            return f"[百炼 API 错误：{response.status_code}]"
    except Exception as e:
        return f"[百炼调用失败：{e}]"

def call_gemini_model(prompt: str) -> str:
    """调用 Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return "[Gemini API Key 未配置]"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "maxOutputTokens": 4096,
            "temperature": 0.7
        }
    }
    
    try:
        url = f"{MODELS['gemini']['endpoint']}?key={api_key}"
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        else:
            return f"[Gemini API 错误：{response.status_code}]"
    except Exception as e:
        return f"[Gemini 调用失败：{e}]"

def log_usage(model_key: str, task_type: str, tokens: int):
    """记录模型使用"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    model_info = MODELS[model_key]
    cost = (tokens / 1000) * model_info["cost_per_1k"]
    
    log_entry = f"- {timestamp} | {model_info['name']} | {task_type} | {tokens} tokens | ¥{cost:.4f}\n"
    
    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 scripts/model-router-executor.py \"用户请求\"")
        print("\n示例:")
        print('  python3 scripts/model-router-executor.py "你好"')
        print('  python3 scripts/model-router-executor.py "写一个 Python 函数"')
        return
    
    query = sys.argv[1]
    
    print("=" * 60)
    print("🤖 太一模型路由执行器 v2.0")
    print("=" * 60)
    
    # 0. 加载配额状态
    status = load_status()
    print(f"\n📊 配额状态:")
    print(f"  当前模型：{status.get('current_model', 'unknown')}")
    print(f"  百炼状态：{status.get('bailian_status', 'unknown')}")
    
    # 1. 分类任务
    task_type, complexity, token_estimate = classify_task(query)
    print(f"\n📊 任务分类:")
    print(f"  类型：{task_type}")
    print(f"  复杂度：{complexity}")
    print(f"  估算 Token: ~{token_estimate}")
    
    # 2. 选择模型
    model_key = select_model(task_type, complexity, token_estimate)
    model_info = MODELS[model_key]
    print(f"\n🎯 模型选择:")
    print(f"  模型：{model_info['name']}")
    print(f"  层级：{model_info['layer']} - {model_info['description']}")
    print(f"  成本：¥{model_info['cost_per_1k']}/1K tokens")
    
    # 3. 记忆检索
    print(f"\n🔍 检索记忆...")
    memory_context = search_memory(query)
    if memory_context:
        print(f"  ✅ 找到相关记忆")
        query_with_memory = query + memory_context
    else:
        print(f"  ⚪ 无相关记忆")
        query_with_memory = query
    
    # 4. 调用模型
    print(f"\n🚀 执行任务...")
    if model_key == "local":
        result = call_local_model(query_with_memory)
    elif model_key == "bailian":
        result = call_bailian_model(query_with_memory)
    else:  # gemini
        result = call_gemini_model(query_with_memory)
    
    print(f"\n📝 结果:\n{result[:500]}{'...' if len(result) > 500 else ''}")
    
    # 5. 记录使用
    log_usage(model_key, task_type, token_estimate)
    print(f"\n✅ 使用已记录到 {USAGE_LOG}")
    
    print("\n" + "=" * 60)
    
    return result

if __name__ == '__main__':
    main()
