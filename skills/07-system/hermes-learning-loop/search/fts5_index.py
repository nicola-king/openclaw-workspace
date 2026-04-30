#!/usr/bin/env python3
"""
FTS5 Index - 全文索引构建与管理

灵感：Hermes Agent FTS5 Search
作者：太一 AGI
创建：2026-04-08
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
SKILLS_DIR = WORKSPACE / "skills"
CONSTITUTION_DIR = WORKSPACE / "constitution"
DB_PATH = WORKSPACE / "skills/hermes-learning-loop/search/memory_index.db"


class FTS5Index:
    """FTS5 全文索引"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DB_PATH)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 记忆内容索引
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_index USING fts5(
                content,
                title,
                tags,
                type,
                date,
                file_path
            )
        """)
        
        # 技能索引
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS skill_index USING fts5(
                name,
                description,
                responsibilities,
                commands,
                tags,
                file_path
            )
        """)
        
        # 宪法索引
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS constitution_index USING fts5(
                content,
                title,
                type,
                file_path
            )
        """)
        
        # 元数据表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        print(f"📚 FTS5 索引初始化完成：{self.db_path}")
    
    def index_memory_file(self, file_path: str) -> int:
        """索引记忆文件"""
        path = Path(file_path)
        if not path.exists():
            return 0
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取元数据
        title = self._extract_title(content)
        tags = self._extract_tags(content)
        doc_type = "memory"
        date = self._extract_date(path.name)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 删除旧记录
        cursor.execute("DELETE FROM memory_index WHERE file_path = ?", (str(path),))
        
        # 插入新记录
        cursor.execute("""
            INSERT INTO memory_index (content, title, tags, type, date, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (content, title, tags, doc_type, date, str(path)))
        
        rowid = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return rowid
    
    def index_skill(self, file_path: str) -> int:
        """索引技能文件"""
        path = Path(file_path)
        if not path.exists():
            return 0
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取元数据
        name = self._extract_skill_name(content)
        description = self._extract_description(content)
        responsibilities = self._extract_responsibilities(content)
        commands = self._extract_commands(content)
        tags = self._extract_tags(content)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 删除旧记录
        cursor.execute("DELETE FROM skill_index WHERE file_path = ?", (str(path),))
        
        # 插入新记录
        cursor.execute("""
            INSERT INTO skill_index (name, description, responsibilities, commands, tags, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, responsibilities, commands, tags, str(path)))
        
        rowid = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return rowid
    
    def index_constitution(self, file_path: str) -> int:
        """索引宪法文件"""
        path = Path(file_path)
        if not path.exists():
            return 0
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取元数据
        title = self._extract_title(content)
        doc_type = self._extract_constitution_type(path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 删除旧记录
        cursor.execute("DELETE FROM constitution_index WHERE file_path = ?", (str(path),))
        
        # 插入新记录
        cursor.execute("""
            INSERT INTO constitution_index (content, title, type, file_path)
            VALUES (?, ?, ?, ?)
        """, (content, title, doc_type, str(path)))
        
        rowid = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return rowid
    
    def search(self, query: str, index: str = "memory", limit: int = 10) -> List[Dict]:
        """
        FTS5 搜索
        
        Args:
            query: 搜索词
            index: 索引类型 (memory/skill/constitution)
            limit: 返回数量
        
        Returns:
            搜索结果列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if index == "memory":
            cursor.execute("""
                SELECT *, bm25(memory_index) as relevance
                FROM memory_index
                WHERE memory_index MATCH ?
                ORDER BY relevance
                LIMIT ?
            """, (query, limit))
        elif index == "skill":
            cursor.execute("""
                SELECT *, bm25(skill_index) as relevance
                FROM skill_index
                WHERE skill_index MATCH ?
                ORDER BY relevance
                LIMIT ?
            """, (query, limit))
        elif index == "constitution":
            cursor.execute("""
                SELECT *, bm25(constitution_index) as relevance
                FROM constitution_index
                WHERE constitution_index MATCH ?
                ORDER BY relevance
                LIMIT ?
            """, (query, limit))
        else:
            conn.close()
            return []
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def rebuild_all(self):
        """重建所有索引"""
        print("🔨 重建索引...")
        
        # 索引记忆文件
        memory_files = list(MEMORY_DIR.glob("*.md"))
        for f in memory_files:
            self.index_memory_file(str(f))
        print(f"  ✅ 记忆文件：{len(memory_files)} 个")
        
        # 索引技能文件
        skill_files = list(SKILLS_DIR.glob("*/SKILL.md"))
        for f in skill_files:
            self.index_skill(str(f))
        print(f"  ✅ 技能文件：{len(skill_files)} 个")
        
        # 索引宪法文件
        constitution_files = list(CONSTITUTION_DIR.glob("**/*.md"))
        for f in constitution_files:
            self.index_constitution(str(f))
        print(f"  ✅ 宪法文件：{len(constitution_files)} 个")
        
        # 更新元数据
        self._update_metadata("last_rebuild", datetime.now().isoformat())
        
        print("✅ 索引重建完成")
    
    def _extract_title(self, content: str) -> str:
        """提取标题"""
        import re
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1) if match else "Untitled"
    
    def _extract_tags(self, content: str) -> str:
        """提取标签"""
        import re
        tags = re.findall(r'\[([^\]]+)\]', content)
        return ",".join(tags)
    
    def _extract_date(self, filename: str) -> str:
        """从文件名提取日期"""
        import re
        match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        return match.group(1) if match else "unknown"
    
    def _extract_skill_name(self, content: str) -> str:
        """提取技能名称"""
        import re
        match = re.search(r'name:\s*(\S+)', content)
        return match.group(1) if match else "unknown"
    
    def _extract_description(self, content: str) -> str:
        """提取描述"""
        import re
        match = re.search(r'description:\s*(.+)$', content, re.MULTILINE)
        return match.group(1) if match else ""
    
    def _extract_responsibilities(self, content: str) -> str:
        """提取职责"""
        import re
        matches = re.findall(r'^[-*]\s+(.+)$', content, re.MULTILINE)
        return ",".join(matches[:10])  # 限制前 10 条
    
    def _extract_commands(self, content: str) -> str:
        """提取命令"""
        import re
        matches = re.findall(r'`([^`]+)`', content)
        return ",".join(matches[:20])  # 限制前 20 条
    
    def _extract_constitution_type(self, path: Path) -> str:
        """提取宪法类型"""
        parts = path.parts
        if "directives" in parts:
            return "directive"
        elif "principles" in parts:
            return "principle"
        elif "axiom" in parts:
            return "axiom"
        else:
            return "other"
    
    def _update_metadata(self, key: str, value: str):
        """更新元数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO metadata (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, value, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """获取索引统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        for index in ["memory_index", "skill_index", "constitution_index"]:
            cursor.execute(f"SELECT COUNT(*) FROM {index}")
            stats[index] = cursor.fetchone()[0]
        
        conn.close()
        return stats


def main():
    """测试"""
    indexer = FTS5Index()
    
    print("\n📊 索引统计:")
    stats = indexer.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v} 条")
    
    print("\n🔍 测试搜索 'Hermes':")
    results = indexer.search("Hermes", "memory", limit=5)
    for r in results:
        print(f"  - {r['file_path']}: {r['title']}")


if __name__ == "__main__":
    main()
