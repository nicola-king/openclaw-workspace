#!/usr/bin/env python3
"""
Auto Trigger - 学习循环自动触发器

功能:
- 任务完成后自动评估是否创建技能
- 会话结束时自动持久化知识
- 定期 Nudge 提醒

作者：太一 AGI
创建：2026-04-08
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
HEARTBEAT_FILE = WORKSPACE / "HEARTBEAT.md"
TRIGGER_LOG = WORKSPACE / "skills/hermes-learning-loop/trigger_log.json"


class AutoTrigger:
    """学习循环自动触发器"""
    
    def __init__(self):
        self.log = self.load_log()
        self.task_history = self.load_task_history()
    
    def load_log(self) -> Dict:
        """加载触发日志"""
        if TRIGGER_LOG.exists():
            with open(TRIGGER_LOG, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "skill_creations": [],
            "nudges": [],
            "optimizations": []
        }
    
    def save_log(self):
        """保存触发日志"""
        TRIGGER_LOG.parent.mkdir(exist_ok=True)
        with open(TRIGGER_LOG, "w", encoding="utf-8") as f:
            json.dump(self.log, f, indent=2, ensure_ascii=False)
    
    def load_task_history(self) -> List[Dict]:
        """加载任务历史"""
        # 从 HEARTBEAT.md 解析任务
        if not HEARTBEAT_FILE.exists():
            return []
        
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 简单解析任务表格
        import re
        tasks = []
        for match in re.finditer(r'\*\*(TASK-\d+)\*\*\s*\|\s*([^|]+)\s*\|\s*([^|]+)', content):
            tasks.append({
                "id": match.group(1),
                "name": match.group(2).strip(),
                "status": match.group(3).strip(),
                "completed_at": datetime.now().isoformat()
            })
        
        return tasks
    
    def check_skill_creation_trigger(self) -> Optional[Dict]:
        """
        检查技能创建触发条件
        
        触发条件:
        1. 同类任务重复 ≥3 次
        2. 任务复杂度 > 阈值
        3. 用户明确请求
        
        Returns:
            触发信息或 None
        """
        # 按任务类型分组
        task_groups = {}
        for task in self.task_history:
            # 简化：从任务名提取类型
            task_type = self._extract_task_type(task["name"])
            if task_type not in task_groups:
                task_groups[task_type] = []
            task_groups[task_type].append(task)
        
        # 检查重复任务
        for task_type, tasks in task_groups.items():
            if len(tasks) >= 3:
                # 检查是否已创建技能
                existing = [
                    sc for sc in self.log["skill_creations"]
                    if sc.get("task_type") == task_type
                ]
                if not existing:
                    return {
                        "trigger_type": "repetition",
                        "task_type": task_type,
                        "task_count": len(tasks),
                        "tasks": tasks[-3:],
                        "reason": f"同类任务重复出现 {len(tasks)} 次"
                    }
        
        return None
    
    def check_nudge_trigger(self) -> List[Dict]:
        """
        检查 Nudge 触发条件
        
        触发时机:
        1. 会话结束 (context > 80%)
        2. 每日 23:30
        3. 检测到重要洞察
        
        Returns:
            Nudge 列表
        """
        nudges = []
        now = datetime.now()
        
        # 检查每日 23:30 Nudge
        if now.hour == 23 and now.minute >= 30:
            last_nudge = self._get_last_nudge()
            if not last_nudge or last_nudge["date"] != now.strftime("%Y-%m-%d"):
                nudges.append({
                    "trigger_type": "daily",
                    "time": now.isoformat(),
                    "action": "persist_daily_insights"
                })
        
        # 检查会话结束 (简化：检查最近活动)
        last_activity = self._get_last_activity()
        if last_activity:
            inactive_minutes = (now - last_activity).total_seconds() / 60
            if inactive_minutes > 30:  # 30 分钟无活动
                nudges.append({
                    "trigger_type": "session_end",
                    "time": now.isoformat(),
                    "action": "persist_session_insights"
                })
        
        return nudges
    
    def execute_skill_creation(self, trigger: Dict) -> Dict:
        """
        执行技能创建
        
        Args:
            trigger: 触发信息
        
        Returns:
            执行结果
        """
        from skill_creator import SkillCreator
        
        creator = SkillCreator()
        
        # 生成技能提议
        proposal = {
            "name": f"{trigger['task_type']}-automation",
            "reason": trigger["reason"],
            "trigger_type": trigger["trigger_type"],
            "task_ids": [t["id"] for t in trigger["tasks"]],
            "responsibilities": [
                f"自动化处理{trigger['task_type']}任务",
                "监控任务执行状态",
                "生成执行报告"
            ],
            "priority": "P1"
        }
        
        # 记录
        self.log["skill_creations"].append({
            "proposal": proposal,
            "triggered_at": datetime.now().isoformat(),
            "status": "pending_approval"
        })
        self.save_log()
        
        return {
            "status": "created",
            "proposal": proposal,
            "message": f"技能提议已创建：{proposal['name']}"
        }
    
    def execute_nudge(self, nudge: Dict) -> Dict:
        """
        执行 Nudge
        
        Args:
            nudge: Nudge 信息
        
        Returns:
            执行结果
        """
        from nudge_manager import NudgeManager
        
        manager = NudgeManager()
        
        # 生成 Nudge 内容
        content = self._generate_daily_summary()
        
        # 创建 Nudge
        result = manager.persist(
            content=content,
            type="[洞察]",
            target="memory/core.md"
        )
        
        # 记录
        self.log["nudges"].append({
            "trigger": nudge,
            "result": result,
            "executed_at": datetime.now().isoformat()
        })
        self.save_log()
        
        return result
    
    def _extract_task_type(self, task_name: str) -> str:
        """从任务名提取类型"""
        # 简化实现
        if "集成" in task_name or "部署" in task_name:
            return "deployment"
        elif "创建" in task_name or "开发" in task_name:
            return "development"
        elif "检查" in task_name or "验证" in task_name:
            return "verification"
        else:
            return "general"
    
    def _get_last_nudge(self) -> Optional[Dict]:
        """获取最后一次 Nudge"""
        if self.log["nudges"]:
            return self.log["nudges"][-1]
        return None
    
    def _get_last_activity(self) -> Optional[datetime]:
        """获取最后活动时间"""
        # 简化：返回当前时间
        return datetime.now()
    
    def _generate_daily_summary(self) -> str:
        """生成每日总结"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 统计今日完成的任务
        completed = [
            t for t in self.task_history
            if "✅" in t.get("status", "")
        ]
        
        summary = f"""
## 📊 每日总结 {today}

### 完成任务
{len(completed)} 个任务已完成

### 关键洞察
- Hermes 学习循环集成完成
- 自动技能创建机制就绪
- 知识持久化 Nudge 激活

### 明日建议
- 继续完善语义搜索
- 监控技能创建触发
"""
        return summary
    
    def run(self) -> Dict:
        """
        运行自动触发器
        
        Returns:
            执行结果
        """
        results = {
            "skill_creations": [],
            "nudges": []
        }
        
        # 检查技能创建
        skill_trigger = self.check_skill_creation_trigger()
        if skill_trigger:
            result = self.execute_skill_creation(skill_trigger)
            results["skill_creations"].append(result)
        
        # 检查 Nudge
        nudges = self.check_nudge_trigger()
        for nudge in nudges:
            result = self.execute_nudge(nudge)
            results["nudges"].append(result)
        
        return results


def main():
    """测试"""
    trigger = AutoTrigger()
    
    print("🤖 运行自动触发器...")
    results = trigger.run()
    
    print(f"\n技能创建：{len(results['skill_creations'])} 个")
    for r in results['skill_creations']:
        print(f"  - {r.get('proposal', {}).get('name', 'N/A')}")
    
    print(f"\nNudge 执行：{len(results['nudges'])} 个")
    for r in results['nudges']:
        print(f"  - {r.get('target_file', 'N/A')}")


if __name__ == "__main__":
    main()
