#!/usr/bin/env python3
"""
Nudge Manager - 知识持久化管理

灵感：Hermes Agent Learning Loop
作者：太一 AGI
创建：2026-04-08
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
CORE_FILE = MEMORY_DIR / "core.md"
RESIDUAL_FILE = MEMORY_DIR / "residual.md"
LONGTERM_FILE = WORKSPACE / "MEMORY.md"
NUDGE_LOG = WORKSPACE / "skills/hermes-learning-loop/nudge_log.json"


@dataclass
class Nudge:
    """Nudge 定义"""
    content: str
    nudge_type: str  # [决策] [任务] [洞察] [能力涌现] [宪法修订] [元目·待发布]
    target: str  # core/residual/longterm/daily
    priority: str  # P0/P1/P2
    created_at: str
    processed: bool = False


class NudgeManager:
    """Nudge 管理器"""
    
    def __init__(self):
        self.nudges = self.load_nudges()
    
    def load_nudges(self) -> List[Dict]:
        """加载 Nudge 列表"""
        if NUDGE_LOG.exists():
            with open(NUDGE_LOG, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_nudges(self):
        """保存 Nudge 列表"""
        NUDGE_LOG.parent.mkdir(exist_ok=True)
        with open(NUDGE_LOG, "w", encoding="utf-8") as f:
            json.dump(self.nudges, f, indent=2, ensure_ascii=False)
    
    def create_nudge(
        self,
        content: str,
        nudge_type: str,
        target: str = "daily",
        priority: str = "P1"
    ) -> Nudge:
        """
        创建 Nudge
        
        Args:
            content: 内容
            nudge_type: 类型标签
            target: 目标文件 (core/residual/longterm/daily)
            priority: 优先级
        
        Returns:
            Nudge 对象
        """
        nudge = Nudge(
            content=content,
            nudge_type=nudge_type,
            target=target,
            priority=priority,
            created_at=datetime.now().isoformat()
        )
        
        self.nudges.append(asdict(nudge))
        self.save_nudges()
        
        return nudge
    
    def process_nudge(self, nudge: Dict) -> Dict:
        """
        处理 Nudge (持久化到文件)
        
        Args:
            nudge: Nudge 字典
        
        Returns:
            处理结果
        """
        target = nudge["target"]
        content = nudge["content"]
        nudge_type = nudge["nudge_type"]
        
        # 确定目标文件
        if target == "longterm":
            target_file = LONGTERM_FILE
        elif target == "core":
            target_file = CORE_FILE
        elif target == "residual":
            target_file = RESIDUAL_FILE
        else:  # daily
            today = datetime.now().strftime("%Y-%m-%d")
            target_file = MEMORY_DIR / f"{today}.md"
        
        # 读取或创建文件
        if target_file.exists():
            with open(target_file, "r", encoding="utf-8") as f:
                file_content = f.read()
        else:
            file_content = f"# {target_file.stem}\n\n"
        
        # 添加 Nudge 内容
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n### {nudge_type} {timestamp}\n\n{content}\n\n"
        
        # 写入
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(file_content + entry)
        
        # 标记为已处理
        nudge["processed"] = True
        nudge["processed_at"] = datetime.now().isoformat()
        nudge["target_file"] = str(target_file)
        self.save_nudges()
        
        return {
            "status": "processed",
            "target_file": str(target_file),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_pending_nudges(self) -> List[Dict]:
        """获取待处理的 Nudge"""
        return [n for n in self.nudges if not n.get("processed", False)]
    
    def persist(
        self,
        content: str,
        type: str = "[洞察]",
        target: str = "memory/core.md"
    ) -> Dict:
        """
        快捷持久化
        
        Args:
            content: 内容
            type: 类型标签
            target: 目标路径
        
        Returns:
            处理结果
        """
        # 创建 Nudge
        nudge = self.create_nudge(
            content=content,
            nudge_type=type,
            target="daily" if "daily" in target else target.split("/")[1].replace(".md", ""),
            priority="P1"
        )
        
        # 立即处理
        result = self.process_nudge(asdict(nudge))
        
        return result
    
    def get_nudge_history(self, days: int = 7) -> List[Dict]:
        """获取 Nudge 历史"""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        return [
            n for n in self.nudges
            if datetime.fromisoformat(n["created_at"]) > cutoff
        ]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = len(self.nudges)
        processed = sum(1 for n in self.nudges if n.get("processed", False))
        pending = total - processed
        
        by_type = {}
        for n in self.nudges:
            t = n["nudge_type"]
            by_type[t] = by_type.get(t, 0) + 1
        
        return {
            "total": total,
            "processed": processed,
            "pending": pending,
            "by_type": by_type
        }


def main():
    """测试"""
    manager = NudgeManager()
    
    print("📊 Nudge 统计:")
    stats = manager.get_stats()
    print(f"  总计：{stats['total']}")
    print(f"  已处理：{stats['processed']}")
    print(f"  待处理：{stats['pending']}")
    print(f"  按类型：{stats['by_type']}")
    
    print("\n⏳ 待处理 Nudge:")
    for n in manager.get_pending_nudges():
        print(f"  - {n['nudge_type']}: {n['content'][:50]}...")


if __name__ == "__main__":
    main()
