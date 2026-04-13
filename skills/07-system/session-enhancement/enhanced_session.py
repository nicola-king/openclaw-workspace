#!/usr/bin/env python3
"""
Enhanced Session - 持久化增强 (FTS5 + 语义搜索)

作者：太一 AGI
创建：2026-04-09
"""

import sys
sys.path.insert(0, "/home/nicola/.openclaw/workspace/skills/hermes-learning-loop/search")

from session import Session
from fts5_index import FTS5Index
from memory_search import MemorySearch
from typing import Dict, List, Optional
from datetime import datetime


class EnhancedSession(Session):
    """增强 Session"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.indexer = FTS5Index()
        self.searcher = MemorySearch()
    
    def log_event(self, action_type: str, action_data: Dict, result: Dict, checkpoint: bool = False) -> int:
        """记录事件并自动索引"""
        event_id = super().log_event(action_type, action_data, result, checkpoint)
        
        # 自动索引
        self._index_event(event_id, action_type, action_data, result)
        
        return event_id
    
    def _index_event(self, event_id: int, action_type: str, action_data: Dict, result: Dict):
        """索引事件"""
        content = f"{action_type}: {action_data} -> {result}"
        
        # 添加到 FTS5 索引 (简化实现)
        # 实际应调用 indexer.index_session_event()
        pass
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索事件"""
        # 使用 Hermes 搜索
        return self.searcher.search(query, limit)
    
    def semantic_search(self, query: str, limit: int = 10) -> List[Dict]:
        """语义搜索"""
        return self.searcher.hybrid_search(query, semantic_weight=0.5, limit=limit)
    
    def rewind_to(self, timestamp: str) -> Dict:
        """回滚到指定时间"""
        events = self.get_events(limit=10000)
        
        # 过滤时间点之前的事件
        filtered = [
            e for e in events
            if e["timestamp"] <= timestamp
        ]
        
        # 重建状态
        state = {}
        for event in filtered:
            if event.get("checkpoint"):
                state = event.get("action_data", {})
        
        return state
    
    def compare(self, from_time: str, to_time: str) -> Dict:
        """比较两个时间点的差异"""
        from_state = self.rewind_to(from_time)
        to_state = self.rewind_to(to_time)
        
        # 简单比较
        diff = {
            "from": from_state,
            "to": to_state,
            "changes": []
        }
        
        # 找出差异
        all_keys = set(from_state.keys()) | set(to_state.keys())
        for key in all_keys:
            if from_state.get(key) != to_state.get(key):
                diff["changes"].append({
                    "key": key,
                    "from": from_state.get(key),
                    "to": to_state.get(key)
                })
        
        return diff
    
    def restore_checkpoint(self, checkpoint_id: int) -> bool:
        """恢复到指定检查点"""
        events = self.get_events(limit=10000)
        checkpoint = next((e for e in events if e["id"] == checkpoint_id), None)
        
        if not checkpoint:
            return False
        
        # 恢复状态
        state = checkpoint.get("action_data", {})
        for key, value in state.items():
            self.set_state(key, value)
        
        return True


def main():
    """测试"""
    session = EnhancedSession("test-agent-002")
    
    print("📦 Enhanced Session 测试")
    print()
    
    # 记录事件
    session.log_event("test", {"action": "hello"}, {"result": "world"})
    
    # 搜索
    results = session.search("test")
    print(f"搜索结果：{len(results)} 条")
    
    # 时间旅行
    state = session.rewind_to(datetime.now().isoformat())
    print(f"回滚状态：{state}")


if __name__ == "__main__":
    main()
