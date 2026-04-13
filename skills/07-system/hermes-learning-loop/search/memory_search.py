#!/usr/bin/env python3
"""
Memory Search - 统一搜索接口

灵感：Hermes Agent FTS5+LLM Search
作者：太一 AGI
创建：2026-04-08
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fts5_index import FTS5Index

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"


class MemorySearch:
    """记忆搜索统一接口"""
    
    def __init__(self):
        self.indexer = FTS5Index()
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        关键词搜索
        
        Args:
            query: 搜索词
            limit: 返回数量
        
        Returns:
            搜索结果
        """
        results = self.indexer.search(query, "memory", limit)
        return self._format_results(results)
    
    def search_skills(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索技能"""
        results = self.indexer.search(query, "skill", limit)
        return self._format_results(results, type="skill")
    
    def search_constitution(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索宪法"""
        results = self.indexer.search(query, "constitution", limit)
        return self._format_results(results, type="constitution")
    
    def search_by_date(self, query: str, start: str, end: str, limit: int = 10) -> List[Dict]:
        """
        时间范围搜索
        
        Args:
            query: 搜索词
            start: 开始日期 (YYYY-MM-DD)
            end: 结束日期
            limit: 返回数量
        
        Returns:
            搜索结果
        """
        # 先 FTS5 搜索
        results = self.indexer.search(query, "memory", limit * 3)  # 多取一些用于过滤
        
        # 过滤日期范围
        filtered = []
        for r in results:
            if start <= r.get("date", "") <= end:
                filtered.append(r)
            if len(filtered) >= limit:
                break
        
        return self._format_results(filtered)
    
    def search_by_tag(self, query: str, tags: List[str], limit: int = 10) -> List[Dict]:
        """
        标签过滤搜索
        
        Args:
            query: 搜索词
            tags: 标签列表
            limit: 返回数量
        
        Returns:
            搜索结果
        """
        # 先 FTS5 搜索
        results = self.indexer.search(query, "memory", limit * 3)
        
        # 过滤标签
        filtered = []
        for r in results:
            r_tags = r.get("tags", "").lower()
            if any(tag.lower() in r_tags for tag in tags):
                filtered.append(r)
            if len(filtered) >= limit:
                break
        
        return self._format_results(filtered)
    
    def hybrid_search(self, query: str, semantic_weight: float = 0.3, limit: int = 10) -> List[Dict]:
        """
        混合搜索 (关键词 + 语义)
        
        TODO: 实现语义搜索后增强
        
        Args:
            query: 搜索词
            semantic_weight: 语义权重 (0-1)
            limit: 返回数量
        
        Returns:
            搜索结果
        """
        # 当前简化实现：仅关键词搜索
        # 未来：结合向量搜索
        return self.search(query, limit)
    
    def _format_results(self, results: List[Dict], type: str = "memory") -> List[Dict]:
        """格式化搜索结果"""
        formatted = []
        for r in results:
            formatted.append({
                "type": type,
                "title": r.get("title", "Untitled"),
                "file_path": r.get("file_path", ""),
                "date": r.get("date", "unknown"),
                "tags": r.get("tags", "").split(",") if r.get("tags") else [],
                "relevance": r.get("relevance", 0),
                "snippet": self._generate_snippet(r.get("content", ""))
            })
        return formatted
    
    def _generate_snippet(self, content: str, max_len: int = 200) -> str:
        """生成摘要"""
        if not content:
            return ""
        
        # 移除 markdown
        import re
        text = re.sub(r'#+\s*', '', content)
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # 截取
        if len(text) > max_len:
            text = text[:max_len] + "..."
        
        return text.strip()
    
    def get_stats(self) -> Dict:
        """获取搜索统计"""
        return self.indexer.get_stats()
    
    def rebuild_index(self):
        """重建索引"""
        self.indexer.rebuild_all()


def main():
    """测试"""
    searcher = MemorySearch()
    
    print("📊 索引统计:")
    stats = searcher.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v} 条")
    
    print("\n🔍 测试搜索 'Hermes':")
    results = searcher.search("Hermes", limit=5)
    for r in results:
        print(f"  - [{r['date']}] {r['title']}")
        print(f"    文件：{r['file_path']}")
        print(f"    摘要：{r['snippet'][:100]}...")
        print()


if __name__ == "__main__":
    main()
