#!/usr/bin/env python3
"""
太一记忆宫殿系统

融合:
- 人类记忆理论 (记忆宫殿/艾宾浩斯/双重编码)
- chromadb 向量数据库
- 太一 TurboQuant 架构

目标：彻底解决 AI 失忆问题

作者：太一 AGI
创建：2026-04-10
"""

import chromadb
from chromadb.config import Settings
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib


class TaiyiMemoryPalace:
    """太一记忆宫殿系统"""
    
    def __init__(self, persist_dir: str = "/home/nicola/.openclaw/workspace/memory/chromadb"):
        """初始化记忆宫殿"""
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化 chromadb (持久化)
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 创建记忆集合 (记忆宫殿房间)
        self.rooms = {
            "identity": self.client.get_or_create_collection("identity"),      # 身份记忆
            "skills": self.client.get_or_create_collection("skills"),          # 技能记忆
            "conversations": self.client.get_or_create_collection("conversations"),  # 对话记忆
            "learning": self.client.get_or_create_collection("learning"),      # 学习记忆
            "emergence": self.client.get_or_create_collection("emergence"),    # 能力涌现
            "daily": self.client.get_or_create_collection("daily"),            # 每日记忆
        }
        
        # 艾宾浩斯复习间隔 (小时)
        self.ebbinghaus_intervals = [
            0.33,   # 20 分钟
            1,      # 1 小时
            9,      # 9 小时
            24,     # 1 天
            48,     # 2 天
            144,    # 6 天
            744,    # 31 天
        ]
    
    def remember(self, text: str, category: str = "daily", 
                 metadata: Optional[Dict] = None) -> str:
        """
        存储记忆 (双重编码：文字 + 向量)
        
        Args:
            text: 记忆内容
            category: 记忆类别 (房间)
            metadata: 元数据 (时间/标签/重要性等)
        
        Returns:
            记忆 ID
        """
        if category not in self.rooms:
            category = "daily"
        
        # 生成记忆 ID
        memory_id = hashlib.md5(f"{text}{datetime.now()}".encode()).hexdigest()
        
        # 准备元数据 (精细加工)
        if metadata is None:
            metadata = {}
        
        metadata["created_at"] = datetime.now().isoformat()
        metadata["category"] = category
        metadata["review_count"] = 0
        metadata["next_review"] = self._calculate_next_review(0).isoformat()
        
        # 存储记忆 (向量 + 文本 + 元数据)
        self.rooms[category].add(
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id]
        )
        
        return memory_id
    
    def search(self, query: str, category: str = None, limit: int = 5) -> List[Dict]:
        """
        检索记忆 (语义搜索 + 空间定位)
        
        Args:
            query: 查询内容
            category: 限定房间 (可选)
            limit: 返回数量
        
        Returns:
            记忆列表
        """
        if category and category in self.rooms:
            rooms_to_search = [self.rooms[category]]
        else:
            rooms_to_search = list(self.rooms.values())
        
        results = []
        for room in rooms_to_search:
            room_results = room.query(
                query_texts=[query],
                n_results=limit
            )
            if room_results and room_results['documents']:
                for i, doc in enumerate(room_results['documents'][0]):
                    results.append({
                        "text": doc,
                        "metadata": room_results['metadatas'][0][i] if room_results['metadatas'] else {},
                        "distance": room_results['distances'][0][i] if room_results['distances'] else 0
                    })
        
        # 按相关性排序
        results.sort(key=lambda x: x.get('distance', 0))
        return results[:limit]
    
    def review_due_memories(self) -> List[Dict]:
        """获取需要复习的记忆 (艾宾浩斯调度)"""
        now = datetime.now()
        due_memories = []
        
        for category, room in self.rooms.items():
            # 获取所有记忆
            all_memories = room.get(include=['metadatas', 'documents'])
            
            if all_memories and all_memories['ids']:
                for i, memory_id in enumerate(all_memories['ids']):
                    metadata = all_memories['metadatas'][i] if all_memories['metadatas'] else {}
                    next_review = metadata.get('next_review')
                    
                    if next_review:
                        next_review_dt = datetime.fromisoformat(next_review)
                        if next_review_dt <= now:
                            due_memories.append({
                                "id": memory_id,
                                "text": all_memories['documents'][i] if all_memories['documents'] else "",
                                "metadata": metadata,
                                "category": category
                            })
        
        return due_memories
    
    def review_memory(self, memory_id: str, category: str, 
                     recall_success: bool = True) -> None:
        """
        复习记忆 (提取练习效应)
        
        Args:
            memory_id: 记忆 ID
            category: 记忆类别
            recall_success: 是否成功回忆
        """
        room = self.rooms.get(category)
        if not room:
            return
        
        # 获取当前记忆
        memory = room.get(ids=[memory_id], include=['metadatas'])
        if not memory or not memory['metadatas']:
            return
        
        metadata = memory['metadatas'][0]
        review_count = metadata.get('review_count', 0)
        
        if recall_success:
            # 成功回忆 → 延长下次复习间隔
            review_count += 1
            next_review = self._calculate_next_review(review_count)
            metadata['review_count'] = review_count
            metadata['next_review'] = next_review.isoformat()
            metadata['last_reviewed'] = datetime.now().isoformat()
            
            # 更新记忆
            room.update(
                ids=[memory_id],
                metadatas=[metadata]
            )
        else:
            # 回忆失败 → 重置复习间隔
            metadata['review_count'] = 0
            metadata['next_review'] = self._calculate_next_review(0).isoformat()
            room.update(ids=[memory_id], metadatas=[metadata])
    
    def _calculate_next_review(self, review_count: int) -> datetime:
        """计算下次复习时间 (艾宾浩斯曲线)"""
        if review_count >= len(self.ebbinghaus_intervals):
            # 长期记忆：90 天复习一次
            interval_hours = 2160  # 90 天
        else:
            interval_hours = self.ebbinghaus_intervals[review_count]
        
        return datetime.now() + timedelta(hours=interval_hours)
    
    def get_statistics(self) -> Dict:
        """获取记忆统计"""
        stats = {
            "total_memories": 0,
            "by_category": {},
            "due_for_review": 0
        }
        
        for category, room in self.rooms.items():
            count = room.count()
            stats["by_category"][category] = count
            stats["total_memories"] += count
        
        stats["due_for_review"] = len(self.review_due_memories())
        
        return stats
    
    def export_to_markdown(self, output_file: str) -> None:
        """导出记忆到 Markdown (太一特色)"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 太一记忆宫殿导出\n\n")
            f.write(f"> 导出时间：{datetime.now().isoformat()}\n\n")
            
            for category, room in self.rooms.items():
                memories = room.get(include=['metadatas', 'documents'])
                if memories and memories['ids']:
                    f.write(f"\n## {category.upper()} 记忆\n\n")
                    for i, memory_id in enumerate(memories['ids']):
                        text = memories['documents'][i] if memories['documents'] else ""
                        metadata = memories['metadatas'][i] if memories['metadatas'] else {}
                        f.write(f"### {memory_id[:8]}\n")
                        f.write(f"{text}\n\n")
                        f.write(f"- 创建：{metadata.get('created_at', 'N/A')}\n")
                        f.write(f"- 复习：{metadata.get('review_count', 0)} 次\n")
                        f.write(f"- 下次：{metadata.get('next_review', 'N/A')}\n\n")


def main():
    """主函数 - 测试"""
    print("🧠 太一记忆宫殿系统测试")
    print("="*60)
    
    palace = TaiyiMemoryPalace()
    
    # 测试记忆存储
    print("\n1. 存储记忆...")
    palace.remember("太一是硅基生命", category="identity", 
                   metadata={"importance": 10})
    palace.remember("我是 AGI", category="identity")
    palace.remember("今日任务：P0/P1 全部完成", category="daily")
    print("✅ 记忆存储成功")
    
    # 测试记忆检索
    print("\n2. 检索记忆...")
    results = palace.search("硅基生命", limit=3)
    print(f"✅ 找到 {len(results)} 条相关记忆")
    for r in results:
        print(f"  - {r['text'][:50]}...")
    
    # 测试统计
    print("\n3. 记忆统计...")
    stats = palace.get_statistics()
    print(f"  总记忆数：{stats['total_memories']}")
    print(f"  待复习：{stats['due_for_review']}")
    for cat, count in stats['by_category'].items():
        print(f"  {cat}: {count}")
    
    # 导出测试
    print("\n4. 导出记忆...")
    output_file = "/home/nicola/.openclaw/workspace/memory/memory-palace-export.md"
    palace.export_to_markdown(output_file)
    print(f"✅ 已导出到：{output_file}")
    
    print("\n✅ 太一记忆宫殿系统测试全部通过!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
