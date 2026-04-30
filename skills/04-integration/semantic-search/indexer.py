#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Search Indexer - FTS5 索引构建器

版本：v1.0 | 创建：2026-04-08
功能：构建和维护 SQLite FTS5 全文索引
"""

import sqlite3
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class SemanticIndexer:
    """语义索引构建器"""
    
    def __init__(self, db_path: str = '/home/nicola/.openclaw/workspace/skills/semantic-search/db/semantic_index.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        self.conn = sqlite3.connect(str(self.db_path))
        self._create_tables()
    
    def _create_tables(self):
        """创建索引表"""
        cursor = self.conn.cursor()
        
        # FTS5 记忆索引
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_index USING fts5(
                content,
                title,
                tags,
                type,
                date,
                file_path,
                tokenize='unicode61'
            )
        ''')
        
        # FTS5 技能索引
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS skill_index USING fts5(
                name,
                description,
                responsibilities,
                commands,
                tags,
                file_path,
                tokenize='unicode61'
            )
        ''')
        
        # FTS5 宪法索引
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS constitution_index USING fts5(
                name,
                content,
                directives,
                priority,
                file_path,
                tokenize='unicode61'
            )
        ''')
        
        # FTS5 对话索引
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS conversation_index USING fts5(
                content,
                participants,
                date,
                session_id,
                channel,
                tokenize='unicode61'
            )
        ''')
        
        # 文件元数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_metadata (
                file_path TEXT PRIMARY KEY,
                file_type TEXT,
                created_at TEXT,
                updated_at TEXT,
                word_count INTEGER,
                tags TEXT
            )
        ''')
        
        # 搜索历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                timestamp TEXT,
                results_count INTEGER,
                clicked_file TEXT
            )
        ''')
        
        self.conn.commit()
    
    def index_memory_files(self, memory_dir: str = '/home/nicola/.openclaw/workspace/memory'):
        """索引记忆文件"""
        memory_path = Path(memory_dir)
        if not memory_path.exists():
            return
        
        cursor = self.conn.cursor()
        
        for md_file in memory_path.glob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
                file_stat = md_file.stat()
                
                # 提取标题（第一个 # 标题）
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem
                
                # 提取标签
                tags = self._extract_tags(content)
                
                # 提取日期（从文件名）
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', md_file.stem)
                date = date_match.group(1) if date_match else 'unknown'
                
                # 插入索引
                cursor.execute('''
                    INSERT OR REPLACE INTO memory_index 
                    (content, title, tags, type, date, file_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (content, title, ' '.join(tags), 'memory', date, str(md_file)))
                
                # 更新元数据
                cursor.execute('''
                    INSERT OR REPLACE INTO file_metadata 
                    (file_path, file_type, created_at, updated_at, word_count, tags)
                    VALUES (?, 'memory', ?, ?, ?, ?)
                ''', (str(md_file), 
                      datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                      datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                      len(content.split()),
                      json.dumps(tags)))
                
            except Exception as e:
                print(f"索引失败 {md_file}: {e}")
        
        self.conn.commit()
    
    def index_skill_files(self, skills_dir: str = '/home/nicola/.openclaw/workspace/skills'):
        """索引技能文件"""
        skills_path = Path(skills_dir)
        if not skills_path.exists():
            return
        
        cursor = self.conn.cursor()
        
        for skill_dir in skills_path.iterdir():
            if not skill_dir.is_dir():
                continue
            
            skill_file = skill_dir / 'SKILL.md'
            if not skill_file.exists():
                continue
            
            try:
                content = skill_file.read_text(encoding='utf-8')
                
                # 提取 YAML 元数据
                yaml_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                metadata = {}
                if yaml_match:
                    yaml_content = yaml_match.group(1)
                    for line in yaml_content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                
                # 提取职责部分
                responsibilities = self._extract_section(content, '职责')
                
                # 提取命令
                commands = self._extract_commands(content)
                
                # 提取标签
                tags = metadata.get('tags', '').strip('[]').split(',')
                
                # 插入索引
                cursor.execute('''
                    INSERT OR REPLACE INTO skill_index 
                    (name, description, responsibilities, commands, tags, file_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    metadata.get('name', skill_dir.name),
                    metadata.get('description', ''),
                    responsibilities,
                    ' '.join(commands),
                    ' '.join(tags),
                    str(skill_file)
                ))
                
            except Exception as e:
                print(f"索引技能失败 {skill_file}: {e}")
        
        self.conn.commit()
    
    def index_constitution_files(self, constitution_dir: str = '/home/nicola/.openclaw/workspace/constitution'):
        """索引宪法文件"""
        constitution_path = Path(constitution_dir)
        if not constitution_path.exists():
            return
        
        cursor = self.conn.cursor()
        
        for directives_dir in constitution_path.iterdir():
            if not directives_dir.is_dir():
                continue
            
            for md_file in directives_dir.glob('*.md'):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    
                    # 提取标题
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1) if title_match else md_file.stem
                    
                    # 提取优先级
                    priority_match = re.search(r'优先级[：:]\s*(\w+)', content)
                    priority = priority_match.group(1) if priority_match else 'normal'
                    
                    # 提取指令
                    directives = self._extract_section(content, '核心原则')
                    
                    # 插入索引
                    cursor.execute('''
                        INSERT OR REPLACE INTO constitution_index 
                        (name, content, directives, priority, file_path)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (title, content, directives, priority, str(md_file)))
                
                except Exception as e:
                    print(f"索引宪法失败 {md_file}: {e}")
        
        self.conn.commit()
    
    def _extract_tags(self, content: str) -> List[str]:
        """提取标签"""
        tags = []
        # 从 YAML frontmatter 提取
        yaml_match = re.search(r'^---\n.*?tags:\s*\[(.*?)\]', content, re.DOTALL)
        if yaml_match:
            tags = [t.strip() for t in yaml_match.group(1).split(',')]
        # 从内容提取 # 标签
        hashtag_matches = re.findall(r'#(\w+)', content)
        tags.extend(hashtag_matches)
        return tags[:10]  # 限制标签数量
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """提取章节内容"""
        pattern = rf'##\s+{section_name}\n(.*?)(?=##|$)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else ''
    
    def _extract_commands(self, content: str) -> List[str]:
        """提取命令"""
        commands = []
        # 从表格提取命令
        table_matches = re.findall(r'\|\s*`?(/?\w+)`?\s*\|', content)
        commands.extend(table_matches)
        # 从代码块提取
        code_matches = re.findall(r'^\s*(/\w+)', content, re.MULTILINE)
        commands.extend(code_matches)
        return list(set(commands))[:20]
    
    def rebuild_all(self):
        """重建所有索引"""
        print("重建记忆索引...")
        self.index_memory_files()
        print("重建技能索引...")
        self.index_skill_files()
        print("重建宪法索引...")
        self.index_constitution_files()
        print("索引重建完成！")
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


# 使用示例
if __name__ == '__main__':
    indexer = SemanticIndexer()
    indexer.rebuild_all()
    indexer.close()
