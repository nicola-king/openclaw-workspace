#!/usr/bin/env python3
# scripts/smart-memory-loader.py

"""
太一智能记忆加载器 v2.0 (FTS5 增强版)

功能:
1. 按意图检索相关记忆 (替代全量加载)
2. FTS5 全文检索 + BM25 排序
3. 动态调整加载量 (context 占用高时精简)
4. Token 节省估算

使用:
    python3 scripts/smart-memory-loader.py "查询内容"

示例:
    python3 scripts/smart-memory-loader.py "MemOS Token 节省"
    python3 scripts/smart-memory-loader.py "币安 API 配置"
"""

import os
import re
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple

# 配置
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
CORE_FILE = os.path.join(MEMORY_DIR, "core.md")
RESIDUAL_FILE = os.path.join(MEMORY_DIR, "residual.md")
TODAY_FILE = os.path.join(MEMORY_DIR, "2026-03-30.md")
MEMORY_MD = os.path.expanduser("~/.openclaw/workspace/MEMORY.md")
INDEX_DB = os.path.expanduser("~/.openclaw/workspace/data/memory_index.db")

# Token 估算 (中文 ~0.6 字/token, 英文 ~0.75 字/token)
def estimate_tokens(text: str) -> int:
    """估算 Token 数量"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    return int(chinese_chars / 0.6 + english_words / 0.75)

def load_file(filepath: str) -> str:
    """加载文件内容"""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_sections(content: str) -> Dict[str, str]:
    """提取 Markdown 章节"""
    sections = {}
    current_section = "header"
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def keyword_match(query: str, text: str) -> float:
    """关键词匹配度 (0-1)"""
    query_terms = query.lower().split()
    text_lower = text.lower()
    
    matches = sum(1 for term in query_terms if term in text_lower)
    return matches / len(query_terms) if query_terms else 0

def fts5_search(query: str, limit: int = 5) -> List[Dict]:
    """FTS5 全文检索"""
    if not os.path.exists(INDEX_DB):
        return []
    
    try:
        conn = sqlite3.connect(INDEX_DB)
        cursor = conn.cursor()
        
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
            results.append({
                "content": row[0],
                "section_name": row[1],
                "source_file": row[2],
                "tags": row[3],
                "score": row[4],
            })
        
        conn.close()
        return results
    except Exception as e:
        print(f"⚠️  FTS5 搜索失败：{e}")
        return []

def smart_memory_load(query: str = None, context_usage: float = 0.5) -> Dict:
    """
    智能记忆加载
    
    Args:
        query: 查询关键词 (可选)
        context_usage: 当前 context 使用率 (0-1)
    
    Returns:
        {
            "loaded_content": str,
            "tokens": int,
            "sources": list,
            "savings": float
        }
    """
    result = {
        "loaded_content": "",
        "tokens": 0,
        "sources": [],
        "savings": 0.0
    }
    
    # 1. 核心记忆永远加载 (core.md)
    core_content = load_file(CORE_FILE)
    if core_content:
        result["loaded_content"] += core_content + "\n\n"
        result["sources"].append("core.md")
    
    # 2. 根据 context 使用率决定是否加载残差记忆
    if context_usage < 0.5:  # context 使用 <50%
        residual_content = load_file(RESIDUAL_FILE)
        if residual_content:
            result["loaded_content"] += residual_content + "\n\n"
            result["sources"].append("residual.md")
    
    # 3. 如果有查询，使用 FTS5 智能检索今日记忆
    if query:
        # 优先使用 FTS5 检索
        fts5_results = fts5_search(query, limit=5)
        
        if fts5_results:
            # FTS5 找到结果，使用检索结果
            for fts5_result in fts5_results:
                result["loaded_content"] += f"## {fts5_result['section_name']}\n{fts5_result['content']}\n\n"
                result["sources"].append(f"2026-03-30.md#{fts5_result['section_name']} (FTS5)")
        else:
            # FTS5 无结果，回退到关键词匹配
            today_content = load_file(TODAY_FILE)
            if today_content:
                sections = extract_sections(today_content)
                relevant_sections = []
                
                for section_name, section_content in sections.items():
                    score = keyword_match(query, section_content)
                    if score > 0.3:
                        relevant_sections.append((section_name, score, section_content))
                
                relevant_sections.sort(key=lambda x: x[1], reverse=True)
                for section_name, score, content in relevant_sections[:3]:
                    result["loaded_content"] += f"## {section_name}\n{content}\n\n"
                    result["sources"].append(f"2026-03-30.md#{section_name}")
    else:
        # 无查询时加载今日记忆全文
        today_content = load_file(TODAY_FILE)
        if today_content:
            result["loaded_content"] += today_content + "\n\n"
            result["sources"].append("2026-03-30.md")
    
    # 4. 计算 Token 节省
    full_load = core_content + load_file(RESIDUAL_FILE) + load_file(TODAY_FILE)
    full_tokens = estimate_tokens(full_load)
    actual_tokens = estimate_tokens(result["loaded_content"])
    result["tokens"] = actual_tokens
    result["savings"] = (full_tokens - actual_tokens) / full_tokens * 100 if full_tokens > 0 else 0
    
    return result

def main():
    """主函数"""
    import sys
    
    query = sys.argv[1] if len(sys.argv) > 1 else None
    
    # 模拟 context 使用率 (实际应从 session_status 获取)
    context_usage = 0.18  # 18%
    
    print(f"🔍 智能记忆加载")
    print(f"查询：{query or '无 (全量加载)'}")
    print(f"Context 使用率：{context_usage*100:.0f}%")
    print("=" * 60)
    
    result = smart_memory_load(query, context_usage)
    
    print(f"\n📊 加载结果:")
    print(f"  来源：{', '.join(result['sources'])}")
    print(f"  Token: ~{result['tokens']:,}")
    print(f"  节省：{result['savings']:.1f}%")
    
    if result['savings'] > 0:
        print(f"\n✅ 相比全量加载节省 {result['savings']:.1f}% Tokens")
    
    # 输出加载内容 (前 500 字)
    print(f"\n📝 加载内容预览 (前 500 字):")
    print("-" * 60)
    print(result['loaded_content'][:500])
    print("...")

if __name__ == '__main__':
    main()
