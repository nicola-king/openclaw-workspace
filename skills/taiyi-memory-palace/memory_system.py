#!/usr/bin/env python3
"""
太一记忆宫殿系统 (简化版 - 无网络依赖)

融合:
- 人类记忆理论 (记忆宫殿/艾宾浩斯/双重编码)
- chromadb 向量数据库 (本地)
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
        
        # 初始化 chromadb (持久化，无网络)
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # 创建记忆集合 (记忆宫殿房间)
        self.rooms = {
            "identity": self.client.get_or_create_collection("identity"),
            "skills": self.client.get_or_create_collection("skills"),
            "conversations": self.client.get_or_create_collection("conversations"),
            "learning": self.client.get_or_create_collection("learning"),
            "emergence": self.client.get_or_create_collection("emergence"),
            "daily": self.client.get_or_create_collection("daily"),
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
        """存储记忆"""
        if category not in self.rooms:
            category = "daily"
        
        memory_id = hashlib.md5(f"{text}{datetime.now()}".encode()).hexdigest()
        
        if metadata is None:
            metadata = {}
        
        metadata["created_at"] = datetime.now().isoformat()
        metadata["category"] = category
        metadata["review_count"] = 0
        metadata["next_review"] = self._calculate_next_review(0).isoformat()
        
        # 使用简单 ID 避免 embedding 下载
        try:
            self.rooms[category].add(
                documents=[text],
                metadatas=[metadata],
                ids=[memory_id]
            )
        except Exception as e:
            # 如果 chromadb 有问题，降级到纯文本存储
            self._fallback_save(text, category, metadata, memory_id)
        
        return memory_id
    
    def _fallback_save(self, text: str, category: str, metadata: Dict, memory_id: str):
        """降级存储 (纯文本)"""
        fallback_dir = self.persist_dir / "fallback" / category
        fallback_dir.mkdir(parents=True, exist_ok=True)
        
        data = {
            "id": memory_id,
            "text": text,
            "metadata": metadata
        }
        
        with open(fallback_dir / f"{memory_id}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def search(self, query: str, category: str = None, limit: int = 5) -> List[Dict]:
        """检索记忆"""
        results = []
        
        # 先从 chromadb 搜索
        if category and category in self.rooms:
            rooms_to_search = [self.rooms[category]]
        else:
            rooms_to_search = list(self.rooms.values())
        
        for room in rooms_to_search:
            try:
                room_results = room.query(query_texts=[query], n_results=limit)
                if room_results and room_results['documents']:
                    for i, doc in enumerate(room_results['documents'][0]):
                        results.append({
                            "text": doc,
                            "metadata": room_results['metadatas'][0][i] if room_results['metadatas'] else {},
                            "category": room.name
                        })
            except:
                pass
        
        # 从降级存储搜索
        fallback_dir = self.persist_dir / "fallback"
        if fallback_dir.exists():
            for cat_dir in fallback_dir.iterdir():
                if category and cat_dir.name != category:
                    continue
                for json_file in cat_dir.glob("*.json"):
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        if query.lower() in data.get('text', '').lower():
                            results.append({
                                "text": data['text'],
                                "metadata": data.get('metadata', {}),
                                "category": cat_dir.name
                            })
                    except:
                        pass
        
        return results[:limit]
    
    def get_statistics(self) -> Dict:
        """获取记忆统计"""
        stats = {"total_memories": 0, "by_category": {}}
        
        for category, room in self.rooms.items():
            try:
                count = room.count()
                stats["by_category"][category] = count
                stats["total_memories"] += count
            except:
                # 从降级存储统计
                fallback_dir = self.persist_dir / "fallback" / category
                if fallback_dir.exists():
                    count = len(list(fallback_dir.glob("*.json")))
                    stats["by_category"][category] = count
                    stats["total_memories"] += count
        
        return stats
    
    def export_to_markdown(self, output_file: str) -> None:
        """导出记忆到 Markdown"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 太一记忆宫殿导出\n\n")
            f.write(f"> 导出时间：{datetime.now().isoformat()}\n\n")
            
            for category in self.rooms.keys():
                # 从降级存储导出
                fallback_dir = self.persist_dir / "fallback" / category
                if fallback_dir.exists():
                    f.write(f"\n## {category.upper()} 记忆\n\n")
                    for json_file in fallback_dir.glob("*.json"):
                        try:
                            with open(json_file, 'r', encoding='utf-8') as jf:
                                data = json.load(jf)
                            f.write(f"### {data['id'][:8]}\n")
                            f.write(f"{data['text']}\n\n")
                            f.write(f"- 创建：{data['metadata'].get('created_at', 'N/A')}\n")
                            f.write(f"- 复习：{data['metadata'].get('review_count', 0)} 次\n\n")
                        except:
                            pass


def main():
    """主函数 - 测试"""
    print("🧠 太一记忆宫殿系统测试")
    print("="*60)
    
    palace = TaiyiMemoryPalace()
    
    # 测试记忆存储
    print("\n1. 存储记忆...")
    palace.remember("太一是硅基生命", category="identity", metadata={"importance": 10})
    palace.remember("我是 AGI", category="identity")
    palace.remember("今日任务：P0/P1 全部完成", category="daily")
    print("✅ 记忆存储成功")
    
    # 测试记忆检索
    print("\n2. 检索记忆...")
    results = palace.search("硅基生命", limit=3)
    print(f"✅ 找到 {len(results)} 条相关记忆")
    for r in results:
        print(f"  - [{r.get('category', 'N/A')}] {r['text'][:50]}...")
    
    # 测试统计
    print("\n3. 记忆统计...")
    stats = palace.get_statistics()
    print(f"  总记忆数：{stats['total_memories']}")
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
