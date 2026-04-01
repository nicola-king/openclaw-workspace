#!/usr/bin/env python3
# scripts/model-router-executor.py

"""
太一模型路由执行器

功能:
1. 根据任务类型自动选择模型
2. 集成 FTS5 智能记忆检索
3. 集成智能记忆加载器
4. 记录模型使用统计

使用:
    python3 scripts/model-router-executor.py "用户请求"

依赖:
    - FTS5 索引 (scripts/fts5-memory-index.py)
    - 智能记忆加载 (scripts/smart-memory-loader.py)
"""

import os
import sys
import json
import sqlite3
import requests
from datetime import datetime
from typing import Dict, Tuple

# 配置
INDEX_DB = os.path.expanduser("~/.openclaw/workspace/data/memory_index.db")
USAGE_LOG = os.path.expanduser("~/.openclaw/workspace/memory/model-usage-today.md")
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

# 模型配置
MODELS = {
    "local": {
        "name": "qwen2.5:7b-instruct-q4_K_M",
        "endpoint": OLLAMA_ENDPOINT,
        "cost_per_1k": 0.0,
        "max_context": 8192,
    },
    "standard": {
        "name": "qwen3.5-plus",
        "endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "cost_per_1k": 0.05,  # 估算
        "max_context": 131072,
    },
    "advanced": {
        "name": "gemini-2.5-pro",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent",
        "cost_per_1k": 0.10,  # 估算
        "max_context": 1048576,
    },
}

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
    if any(kw in query_lower for kw in ['代码', '脚本', 'bug', '写函数', 'debug']):
        return "code", "medium", 5000
    
    # 简单任务
    if any(kw in query_lower for kw in ['你好', '谢谢', '再见', '几点', '天气']):
        return "chat", "easy", 500
    
    if any(kw in query_lower for kw in ['翻译', '润色', '优化', '总结', '摘要']):
        if token_estimate < 2000:
            return "simple", "easy", 1000
    
    # 长文本
    if any(kw in query_lower for kw in ['文档', '报告', '文章', '文件']):
        if token_estimate > 10000:
            return "long_text", "hard", 50000
    
    # 复杂推理
    if any(kw in query_lower for kw in ['分析', '对比', '评估', '为什么', '如何', '策略']):
        return "analysis", "medium", 5000
    
    # 默认
    return "chat", "easy", 1000

def select_model(task_type: str, complexity: str, token_estimate: int) -> str:
    """选择模型"""
    # 本地模型优先
    if complexity == "easy" and token_estimate < 8000:
        if task_type in ["simple", "chat", "calc"]:
            return "local"
    
    # 长文本/复杂
    if complexity == "hard" or token_estimate >= 50000:
        return "advanced"
    
    # 代码
    if task_type == "code":
        return "standard"  # qwen3-coder-plus
    
    # 分析/中等
    if complexity == "medium":
        return "standard"
    
    return "standard"  # 默认

def search_memory(query: str, limit: int = 5) -> str:
    """FTS5 记忆检索"""
    if not os.path.exists(INDEX_DB):
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

def log_usage(model: str, task_type: str, tokens: int):
    """记录模型使用"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 追加到日志
    log_entry = f"- {timestamp} | {model} | {task_type} | {tokens} tokens\n"
    
    os.makedirs(os.path.dirname(USAGE_LOG), exist_ok=True)
    with open(USAGE_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 scripts/model-router-executor.py \"用户请求\"")
        return
    
    query = sys.argv[1]
    
    print("=" * 60)
    print("🤖 太一模型路由执行器")
    print("=" * 60)
    
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
    print(f"  层级：{'L1 本地' if model_key == 'local' else 'L2 云端' if model_key == 'standard' else 'L3 专项'}")
    
    # 3. 记忆检索
    print(f"\n🔍 检索记忆...")
    memory_context = search_memory(query)
    if memory_context:
        print(f"  找到相关记忆")
        query_with_memory = query + memory_context
    else:
        print(f"  无相关记忆")
        query_with_memory = query
    
    # 4. 调用模型
    print(f"\n🚀 执行任务...")
    if model_key == "local":
        result = call_local_model(query_with_memory)
        print(f"\n📝 结果:\n{result[:500]}...")
    else:
        print(f"  ⚠️  云端模型调用需要 API Key，此处仅演示路由逻辑")
        result = f"[{model_info['name']} 将处理：{query_with_memory[:200]}...]"
    
    # 5. 记录使用
    log_usage(model_key, task_type, token_estimate)
    print(f"\n✅ 使用已记录到 {USAGE_LOG}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
