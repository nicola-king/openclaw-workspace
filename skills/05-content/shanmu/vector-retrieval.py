#!/usr/bin/env python3
"""
山木 Bot - 向量检索模块 v1.0
功能：长文本一致性检查 / 上下文检索 / 避免重复

使用 ChromaDB 存储和检索历史内容
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("⚠️ ChromaDB 未安装，使用简化模式")

class ContentMemory:
    """内容记忆存储与检索"""
    
    def __init__(self, db_path: str = "/home/nicola/.openclaw/workspace/data/shanmu-memory"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        if CHROMA_AVAILABLE:
            # 初始化 ChromaDB
            self.client = chromadb.PersistentClient(path=str(self.db_path))
            self.collection = self.client.get_or_create_collection(
                name="content_memory",
                metadata={"hnsw:space": "cosine"}
            )
        else:
            self.client = None
            self.collection = None
            self.memory_file = self.db_path / "memory.json"
            self._load_memory()
    
    def _load_memory(self):
        """加载简化模式记忆"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                self.memories = json.load(f)
        else:
            self.memories = []
    
    def _save_memory(self):
        """保存简化模式记忆"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, ensure_ascii=False, indent=2)
    
    def add_content(self, content: str, metadata: Dict = None):
        """添加内容到记忆库"""
        doc_id = hashlib.md5(content.encode()).hexdigest()
        
        if self.collection:
            # ChromaDB 模式
            self.collection.add(
                documents=[content],
                ids=[doc_id],
                metadatas=[metadata or {}]
            )
        else:
            # 简化模式
            self.memories.append({
                "id": doc_id,
                "content": content,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            })
            self._save_memory()
        
        print(f"✅ 已添加内容：{len(content)} 字符")
    
    def search_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """搜索相似内容"""
        if self.collection:
            # ChromaDB 模式
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return [
                {
                    "content": doc,
                    "metadata": meta,
                    "distance": dist if results['distances'] else None
                }
                for doc, meta, dist in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0] if results['distances'] else [None]*len(results['documents'][0])
                )
            ]
        else:
            # 简化模式：关键词匹配
            query_words = set(query.lower().split())
            scored = []
            for mem in self.memories:
                overlap = len(query_words & set(mem['content'].lower().split()))
                if overlap > 0:
                    scored.append({
                        "content": mem['content'],
                        "metadata": mem['metadata'],
                        "score": overlap
                    })
            return sorted(scored, key=lambda x: -x['score'])[:n_results]
    
    def check_consistency(self, new_content: str, threshold: float = 0.7) -> Dict:
        """检查新内容与历史的一致性"""
        similar = self.search_similar(new_content, n_results=3)
        
        if not similar:
            return {
                "consistent": True,
                "conflicts": [],
                "suggestions": []
            }
        
        # 检测潜在冲突
        conflicts = []
        for s in similar:
            if s.get('distance', 1.0) < (1 - threshold):  # 余弦距离
                conflicts.append({
                    "content": s['content'][:200],
                    "similarity": 1 - s.get('distance', 0),
                    "metadata": s.get('metadata', {})
                })
        
        return {
            "consistent": len(conflicts) == 0,
            "conflicts": conflicts,
            "suggestions": [
                "检查是否存在内容重复",
                "确认上下文是否连贯",
                "验证事实是否一致"
            ] if conflicts else []
        }

# 使用示例
if __name__ == "__main__":
    memory = ContentMemory()
    
    # 添加测试内容
    memory.add_content(
        "太一 AGI v5.0 融合架构：8 Bot 舰队 + 宪法系统 + TurboQuant 记忆",
        {"type": "architecture", "date": "2026-04-05"}
    )
    
    # 测试检索
    results = memory.search_similar("太一 Bot 架构")
    print(f"\n📊 检索结果：{len(results)} 条")
    for r in results:
        print(f"  - {r['content'][:50]}...")
    
    # 测试一致性检查
    check = memory.check_consistency("太一有 8 个 Bot")
    print(f"\n✅ 一致性检查：{'通过' if check['consistent'] else '发现冲突'}")
    if check['conflicts']:
        print(f"   冲突数：{len(check['conflicts'])}")
