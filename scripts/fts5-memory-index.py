#!/usr/bin/env python3
# scripts/fts5-memory-index.py

"""
太一 FTS5 记忆索引

功能:
1. 创建 SQLite FTS5 全文索引
2. 索引 memory/*.md 文件内容
3. 支持关键词检索 + BM25 排序
4. 替代简单文件加载，提升检索效率

使用:
    python3 scripts/fts5-memory-index.py          # 创建索引
    python3 scripts/fts5-memory-index.py --search "MemOS"  # 搜索

依赖:
    - SQLite 3.9.0+ (已验证 3.45.1 ✅)
    - Python 3.8+
"""

import os
import re
import sqlite3
import argparse
from datetime import datetime
from typing import List, Dict, Tuple

# 配置
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
INDEX_DB = os.path.expanduser("~/.openclaw/workspace/data/memory_index.db")
LOG_FILE = os.path.expanduser("~/.openclaw/workspace/logs/fts5-index.log")

def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(os.path.dirname(INDEX_DB), exist_ok=True)

def create_index(conn: sqlite3.Connection):
    """创建 FTS5 索引表"""
    cursor = conn.cursor()
    
    # 创建 FTS5 虚拟表
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS memory_index USING fts5(
            content,
            section_name,
            source_file,
            tags,
            tokenize='unicode61'
        )
    ''')
    
    # 创建元数据表 (存储额外信息)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_meta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rowid INTEGER,
            priority TEXT DEFAULT 'P2',
            created_at TEXT,
            updated_at TEXT,
            token_count INTEGER
        )
    ''')
    
    conn.commit()
    print("✅ FTS5 索引表创建成功")

def parse_sections(filepath: str) -> List[Dict]:
    """解析 Markdown 文件的章节"""
    sections = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按章节分割 (## 或 ###)
    pattern = r'\n(#{2,3})\s+(.+?)\n'
    matches = list(re.finditer(pattern, content))
    
    source_file = os.path.basename(filepath)
    
    for i, match in enumerate(matches):
        level = len(match.group(1))
        section_name = match.group(2).strip()
        
        # 获取章节内容 (从当前标题到下一个标题)
        start_pos = match.end()
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)
        
        section_content = content[start_pos:end_pos].strip()
        
        # 跳过太短的章节
        if len(section_content) < 50:
            continue
        
        # 提取标签
        tags = extract_tags(section_content)
        
        # 判断重要度
        priority = extract_priority(section_name, section_content)
        
        sections.append({
            "content": section_content,
            "section_name": section_name,
            "source_file": source_file,
            "tags": ','.join(tags),
            "priority": priority,
        })
    
    return sections

def extract_tags(content: str) -> List[str]:
    """提取标签"""
    tags = set()
    
    tag_map = {
        "决策": ["决策", "决定", "确认", "采用"],
        "任务": ["任务", "待办", "TODO", "待执行"],
        "洞察": ["洞察", "发现", "学习", "结论"],
        "能力涌现": ["能力涌现", "新建", "创建", "激活"],
        "宪法": ["宪法", "原则", "规则", "法则"],
        "学习": ["学习", "调研", "分析", "评估"],
        "MemOS": ["MemOS", "记忆", "Token", "检索"],
    }
    
    for tag, keywords in tag_map.items():
        if any(kw in content for kw in keywords):
            tags.add(tag)
    
    return list(tags) if tags else ["其他"]

def extract_priority(section_name: str, content: str) -> str:
    """判断重要度"""
    text = section_name + content
    
    if any(kw in text for kw in ['P0', '核心', '宪法', '决策', '原则']):
        return 'P0'
    elif any(kw in text for kw in ['P1', '任务', '重要', '关键']):
        return 'P1'
    else:
        return 'P2'

def index_memory_files(conn: sqlite3.Connection):
    """索引记忆文件"""
    cursor = conn.cursor()
    
    # 清空现有索引
    cursor.execute("DELETE FROM memory_index")
    cursor.execute("DELETE FROM memory_meta")
    
    # 要索引的文件
    memory_files = [
        "core.md",
        "residual.md",
        "2026-03-30.md",
    ]
    
    total_sections = 0
    
    for filename in memory_files:
        filepath = os.path.join(MEMORY_DIR, filename)
        if not os.path.exists(filepath):
            print(f"⚠️  文件不存在：{filepath}")
            continue
        
        print(f"  索引 {filename}...")
        sections = parse_sections(filepath)
        
        for section in sections:
            # 插入 FTS5 表
            cursor.execute('''
                INSERT INTO memory_index (content, section_name, source_file, tags)
                VALUES (?, ?, ?, ?)
            ''', (
                section["content"],
                section["section_name"],
                section["source_file"],
                section["tags"],
            ))
            
            # 获取 rowid
            rowid = cursor.lastrowid
            
            # 插入元数据
            cursor.execute('''
                INSERT INTO memory_meta (rowid, priority, created_at, updated_at, token_count)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                rowid,
                section["priority"],
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                len(section["content"]) // 4,  # 粗略估算 Token
            ))
            
            total_sections += 1
        
        conn.commit()
    
    print(f"✅ 索引完成：{total_sections} 个章节")
    return total_sections

def search(conn: sqlite3.Connection, query: str, limit: int = 10) -> List[Dict]:
    """搜索记忆"""
    cursor = conn.cursor()
    
    # FTS5 搜索 + BM25 排序
    cursor.execute('''
        SELECT 
            rowid,
            content,
            section_name,
            source_file,
            tags,
            bm25(memory_index, 1.0, 1.0, 0.5, 0.5) as score
        FROM memory_index
        WHERE memory_index MATCH ?
        ORDER BY score
        LIMIT ?
    ''', (query, limit))
    
    results = []
    for row in cursor.fetchall():
        # 获取元数据
        cursor.execute('''
            SELECT priority, token_count FROM memory_meta WHERE rowid = ?
        ''', (row[0],))
        meta = cursor.fetchone()
        
        results.append({
            "rowid": row[0],
            "content": row[1][:300] + "..." if len(row[1]) > 300 else row[1],
            "section_name": row[2],
            "source_file": row[3],
            "tags": row[4],
            "score": row[5],
            "priority": meta[0] if meta else 'P2',
            "token_count": meta[1] if meta else 0,
        })
    
    return results

def stats(conn: sqlite3.Connection) -> Dict:
    """获取索引统计"""
    cursor = conn.cursor()
    
    # 总章节数
    cursor.execute("SELECT COUNT(*) FROM memory_index")
    total = cursor.fetchone()[0]
    
    # 按来源文件统计
    cursor.execute('''
        SELECT source_file, COUNT(*) 
        FROM memory_index 
        GROUP BY source_file
    ''')
    by_file = cursor.fetchall()
    
    # 按重要度统计
    cursor.execute('''
        SELECT m.priority, COUNT(*) 
        FROM memory_meta m
        GROUP BY m.priority
    ''')
    by_priority = cursor.fetchall()
    
    # 总 Token 估算
    cursor.execute("SELECT SUM(token_count) FROM memory_meta")
    total_tokens = cursor.fetchone()[0] or 0
    
    return {
        "total_sections": total,
        "by_file": by_file,
        "by_priority": by_priority,
        "total_tokens": total_tokens,
    }

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="太一 FTS5 记忆索引")
    parser.add_argument("--search", type=str, help="搜索关键词")
    parser.add_argument("--limit", type=int, default=10, help="搜索结果数量")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--rebuild", action="store_true", help="重建索引")
    args = parser.parse_args()
    
    ensure_data_dir()
    
    # 连接数据库
    conn = sqlite3.connect(INDEX_DB)
    
    try:
        if args.rebuild or not table_exists(conn, "memory_index"):
            print("=" * 60)
            print("🔧 创建 FTS5 索引...")
            print("=" * 60)
            create_index(conn)
            index_memory_files(conn)
        
        if args.search:
            print("=" * 60)
            print(f"🔍 搜索：{args.search}")
            print("=" * 60)
            results = search(conn, args.search, args.limit)
            
            if not results:
                print("❌ 未找到匹配结果")
                return
            
            print(f"\n找到 {len(results)} 条结果:\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. [{result['priority']}] {result['section_name']}")
                print(f"   来源：{result['source_file']} | 标签：{result['tags']}")
                print(f"   评分：{result['score']:.4f} | Token: ~{result['token_count']}")
                print(f"   内容：{result['content']}")
                print()
        
        if args.stats:
            print("=" * 60)
            print("📊 索引统计")
            print("=" * 60)
            s = stats(conn)
            print(f"总章节数：{s['total_sections']}")
            print(f"总 Token 估算：~{s['total_tokens']:,}")
            print(f"\n按文件:")
            for file, count in s['by_file']:
                print(f"  {file}: {count}")
            print(f"\n按重要度:")
            for priority, count in s['by_priority']:
                print(f"  {priority}: {count}")
    
    finally:
        conn.close()

def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """检查表是否存在"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?
    ''', (table_name,))
    return cursor.fetchone() is not None

if __name__ == '__main__':
    # 创建日志目录
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    main()
