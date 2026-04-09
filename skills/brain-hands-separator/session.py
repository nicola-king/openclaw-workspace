#!/usr/bin/env python3
"""
Session - 持久化层 (事件日志 + 状态检查点)

灵感：Claude Managed Agents
作者：太一 AGI
创建：2026-04-09
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DB_DIR = WORKSPACE / "skills/brain-hands-separator/sessions"
DB_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class Event:
    """事件记录"""
    id: int
    timestamp: str
    action_type: str
    action_data: Dict
    result: Dict
    checkpoint: bool = False


class Session:
    """持久化层 (Session)"""
    
    def __init__(self, agent_id: str):
        """
        初始化
        
        Args:
            agent_id: Agent 标识
        """
        self.agent_id = agent_id
        self.db_path = DB_DIR / f"{agent_id}.db"
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 事件表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action_type TEXT NOT NULL,
                action_data TEXT,
                result TEXT,
                checkpoint INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 状态表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_event(self, action_type: str, action_data: Dict, result: Dict, checkpoint: bool = False) -> int:
        """
        记录事件
        
        Args:
            action_type: 行动类型
            action_data: 行动数据
            result: 执行结果
            checkpoint: 是否检查点
        
        Returns:
            事件 ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO events (timestamp, action_type, action_data, result, checkpoint)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            action_type,
            json.dumps(action_data, ensure_ascii=False),
            json.dumps(result, ensure_ascii=False),
            1 if checkpoint else 0
        ))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return event_id
    
    def get_events(self, limit: int = 100, since_checkpoint: bool = False) -> List[Dict]:
        """
        获取事件历史
        
        Args:
            limit: 返回数量
            since_checkpoint: 是否只返回检查点后事件
        
        Returns:
            事件列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if since_checkpoint:
            # 找到最近检查点
            cursor.execute("""
                SELECT id FROM events WHERE checkpoint = 1 ORDER BY id DESC LIMIT 1
            """)
            row = cursor.fetchone()
            since_id = row["id"] if row else 0
            
            cursor.execute("""
                SELECT * FROM events WHERE id > ? ORDER BY id DESC LIMIT ?
            """, (since_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM events ORDER BY id DESC LIMIT ?
            """, (limit,))
        
        events = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # 解析 JSON
        for e in events:
            try:
                e["action_data"] = json.loads(e["action_data"])
                e["result"] = json.loads(e["result"])
            except Exception:
                pass
        
        return list(reversed(events))
    
    def get_checkpoint(self) -> Optional[Dict]:
        """获取最近检查点"""
        events = self.get_events(since_checkpoint=True)
        checkpoints = [e for e in events if e.get("checkpoint", False)]
        return checkpoints[-1] if checkpoints else None
    
    def set_checkpoint(self, state: Dict) -> int:
        """
        设置检查点
        
        Args:
            state: 状态数据
        
        Returns:
            事件 ID
        """
        return self.log_event(
            action_type="checkpoint",
            action_data=state,
            result={},
            checkpoint=True
        )
    
    def set_state(self, key: str, value: Any):
        """设置状态"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO state (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, json.dumps(value, ensure_ascii=False), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_state(self, key: str) -> Optional[Any]:
        """获取状态"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM state WHERE key = ?", (key,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return json.loads(row["value"])
        return None
    
    def get_final_output(self) -> Optional[Dict]:
        """获取最终输出"""
        return self.get_state("final_output")
    
    def set_final_output(self, output: Dict):
        """设置最终输出"""
        self.set_state("final_output", output)
    
    def rewind_to(self, event_id: int) -> List[Dict]:
        """
        回滚到指定事件
        
        Args:
            event_id: 事件 ID
        
        Returns:
            回滚后的事件历史
        """
        return self.get_events(limit=1000)[:event_id]
    
    def export(self) -> Dict:
        """导出会话"""
        return {
            "agent_id": self.agent_id,
            "events": self.get_events(limit=10000),
            "exported_at": datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM events")
        total_events = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM events WHERE checkpoint = 1")
        checkpoints = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM state")
        state_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_events": total_events,
            "checkpoints": checkpoints,
            "state_entries": state_count,
            "db_path": str(self.db_path)
        }


def main():
    """测试"""
    session = Session("test-agent-001")
    
    print("📦 Session 持久化层测试")
    print()
    
    # 记录事件
    event_id = session.log_event(
        action_type="shell",
        action_data={"command": "echo hello"},
        result={"output": "hello", "success": True}
    )
    print(f"事件记录：ID={event_id}")
    
    # 设置检查点
    session.set_checkpoint({"progress": 50, "stage": "analysis"})
    print("检查点已设置")
    
    # 获取事件
    events = session.get_events(limit=10)
    print(f"事件历史：{len(events)} 条")
    
    # 统计
    stats = session.get_stats()
    print(f"统计：{stats}")


if __name__ == "__main__":
    main()
