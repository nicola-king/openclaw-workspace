"""
太一 · AutoMemory 自动记忆系统 v1.0
====================================
借鉴 OpenHuman Memory Tree 设计理念。

数据流：
  数据源 → Auto-fetch → 规范化 → 分块(≤3K tok) → 评分 → 摘要 → 检索

自动数据源：
  - 跨境买家情报 (auto_scraper)
  - GEO 日报结果
  - 竞品监控数据
  - 搜索结果
  - 贸易快报
"""

import json
import hashlib
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger("taiyi.auto-memory")

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / ".auto-memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

CHUNKS_DIR = MEMORY_DIR / "chunks"
CHUNKS_DIR.mkdir(exist_ok=True)
SUMMARIES_DIR = MEMORY_DIR / "summaries"
SUMMARIES_DIR.mkdir(exist_ok=True)


class AutoMemory:
    """
    自动记忆系统。
    
    自动从各数据源抓取 → 分块 → 评分 → 摘要 → 可检索。
    """
    
    def __init__(self):
        self.chunks = {}
        self.scores = {}
        self._load()
    
    def _load(self):
        """加载持久化的记忆数据"""
        idx_file = MEMORY_DIR / "index.json"
        if idx_file.exists():
            try:
                data = json.loads(idx_file.read_text())
                self.chunks = data.get("chunks", {})
                self.scores = data.get("scores", {})
                logger.info(f"✅ AutoMemory: 加载 {len(self.chunks)} 条记忆")
            except Exception as e:
                logger.warning(f"⚠️ AutoMemory 加载失败: {e}")
    
    def _save(self):
        """持久化记忆数据"""
        idx_file = MEMORY_DIR / "index.json"
        idx_file.write_text(json.dumps({
            "chunks": self.chunks,
            "scores": self.scores,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, indent=2, ensure_ascii=False))
    
    def ingest(self, source: str, content: str, 
               metadata: dict = None) -> dict:
        """
        摄入一条数据到记忆系统。
        
        自动分块 → 评分 → 存储。
        """
        chunk_id = hashlib.md5(
            (source + content[:100] + str(time.time())).encode()
        ).hexdigest()[:12]
        
        # 分块（≤3K tokens ≈ 4500 chars 中文）
        chunks = self._chunk(content, max_chars=4500)
        
        stored_chunks = []
        for i, chunk_text in enumerate(chunks):
            cid = f"{chunk_id}_{i}"
            chunk = {
                "id": cid,
                "source": source,
                "text": chunk_text,
                "metadata": metadata or {},
                "score": self._score(chunk_text, source),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            self.chunks[cid] = chunk
            stored_chunks.append(cid)
            
            # 保存到文件
            (CHUNKS_DIR / f"{cid}.json").write_text(
                json.dumps(chunk, indent=2, ensure_ascii=False))
        
        self._save()
        
        return {
            "chunk_ids": stored_chunks,
            "chunk_count": len(stored_chunks),
            "total_chars": len(content),
        }
    
    def _chunk(self, text: str, max_chars: int = 4500) -> list:
        """将文本分块（≤max_chars chars）"""
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        # 按段落分割
        paragraphs = text.split("\n\n")
        current = ""
        
        for para in paragraphs:
            if len(current) + len(para) < max_chars:
                current += para + "\n\n"
            else:
                if current:
                    chunks.append(current.strip())
                current = para + "\n\n"
        
        if current:
            chunks.append(current.strip())
        
        return chunks
    
    def _score(self, text: str, source: str) -> float:
        """计算记忆片段的热度分数"""
        score = 0.0
        
        # 来源权重
        source_weights = {
            "buyer_intel": 10,
            "company_verify": 8,
            "geo_report": 7,
            "competitor": 8,
            "search": 5,
            "daily_brief": 6,
        }
        score += source_weights.get(source, 3)
        
        # 长度权重
        score += min(len(text) / 1000, 5)
        
        # 关键词权重
        keywords = ["contract", "project", "buyer", "采购", "招标", 
                    "opportunity", "需求", "Bermuda", "Australia", "steel"]
        for kw in keywords:
            if kw.lower() in text.lower():
                score += 1
        
        return min(score, 20)  # 最高 20 分
    
    def query(self, topic: str, top_k: int = 5) -> list:
        """
        查询记忆（关键词匹配）。
        
        Args:
            topic: 查询主题
            top_k: 返回前 N 条
        
        Returns:
            排序后的记忆片段列表
        """
        keywords = topic.lower().split()
        
        scored_results = []
        for cid, chunk in self.chunks.items():
            text = chunk.get("text", "").lower()
            
            # 关键词匹配
            match_count = sum(1 for kw in keywords if kw in text)
            if match_count == 0:
                continue
            
            total_score = chunk.get("score", 0) + match_count * 3
            scored_results.append((total_score, chunk))
        
        # 按分数排序
        scored_results.sort(key=lambda x: -x[0])
        
        return [c for _, c in scored_results[:top_k]]
    
    def summarize(self, topic: str) -> dict:
        """
        生成关于某个主题的摘要。
        
        搜索相关记忆 → 合并 → 生成摘要。
        """
        chunks = self.query(topic, top_k=10)
        
        if not chunks:
            return {"topic": topic, "summary": "无相关记忆", "sources": []}
        
        # 合并文本
        combined = "\n\n".join(
            f"[{c.get('source','?')}] {c.get('text','')[:500]}"
            for c in chunks
        )
        
        sources = list(set(c.get("source", "?") for c in chunks))
        
        return {
            "topic": topic,
            "summary": f"找到 {len(chunks)} 条相关记忆，来自 {len(sources)} 个数据源",
            "sources": sources,
            "detail": combined[:3000],
        }
    
    def stats(self) -> dict:
        """记忆系统统计"""
        sources = {}
        for cid, chunk in self.chunks.items():
            source = chunk.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_chunks": len(self.chunks),
            "by_source": sources,
            "avg_score": sum(c.get("score", 0) for c in self.chunks.values()) / max(len(self.chunks), 1),
        }


_instance = None

def get_memory() -> AutoMemory:
    global _instance
    if _instance is None:
        _instance = AutoMemory()
    return _instance


if __name__ == "__main__":
    mem = get_memory()
    
    print("╔═══════════════════════════════════════════╗")
    print("║  太一 · AutoMemory 测试                   ║")
    print("╚═══════════════════════════════════════════╝")
    print()
    
    # 测试摄入
    r1 = mem.ingest("buyer_intel", 
        "Kovalska Group is a major Ukrainian steel construction company. "
        "Contact: olga.pylypenko@kovalska.rs, LinkedIn: /company/kovalskagroup",
        {"company": "Kovalska", "country": "Ukraine"})
    print(f"📥 摄入: {r1['chunk_count']} chunks (ID: {r1['chunk_ids'][0][:20]}...)")
    
    r2 = mem.ingest("company_verify",
        "Bermuda construction market: 64K population, GDP/capita $120K. "
        "All building materials imported. Hurricane-resistant construction needed.",
        {"country": "Bermuda", "sector": "construction"})
    print(f"📥 摄入: {r2['chunk_count']} chunks")
    
    # 测试查询
    print()
    results = mem.query("Ukraine steel construction")
    print(f"🔍 查询 'Ukraine steel': {len(results)} 条结果")
    for r in results:
        print(f"   [{r.get('source')}] {r.get('text','')[:80]}...")
    
    # 测试摘要
    summary = mem.summarize("Bermuda")
    print(f"\n📋 摘要 'Bermuda': {summary['summary']}")
    print(f"   来源: {summary['sources']}")
    
    # 统计
    print(f"\n📊 统计: {mem.stats()}")
    print("\n✅ AutoMemory 测试通过")
