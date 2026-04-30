#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task Tracker - 执行追踪器
每 30 分钟自动检查各 Bot 任务执行进度
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

AGENTS_DIR = Path.home() / ".openclaw" / "agents"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
STATE_FILE = WORKSPACE / "task-orchestrator-state.json"

class TaskTracker:
    """执行追踪器"""
    
    def __init__(self):
        self.agents_dir = AGENTS_DIR
        self.state_file = STATE_FILE
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """加载状态"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text(encoding='utf-8'))
        return {"tasks": {}, "last_check": None}
    
    def _save_state(self):
        """保存状态"""
        self.state["last_check"] = datetime.now().isoformat()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def scan_all_bots(self) -> Dict[str, List[Dict]]:
        """扫描所有 Bot 的任务状态"""
        results = {}
        
        for bot_dir in self.agents_dir.iterdir():
            if not bot_dir.is_dir():
                continue
            
            bot = bot_dir.name
            inbox = bot_dir / "inbox"
            outbox = bot_dir / "outbox"
            
            tasks = []
            
            # 扫描 inbox
            if inbox.exists():
                for task_file in inbox.glob("TASK-DISPATCH-*.md"):
                    content = task_file.read_text(encoding='utf-8')
                    task_id = self._extract_task_id(content)
                    tasks.append({
                        "id": task_id or task_file.stem,
                        "status": "pending",
                        "file": str(task_file),
                        "created": datetime.fromtimestamp(task_file.stat().st_mtime).isoformat()
                    })
            
            # 扫描 outbox
            if outbox.exists():
                for report_file in outbox.glob("*.md"):
                    content = report_file.read_text(encoding='utf-8')
                    status = "completed" if "✅" in content else "in_progress" if "🟡" in content else "blocked" if "🔴" in content else "unknown"
                    tasks.append({
                        "id": report_file.stem,
                        "status": status,
                        "file": str(report_file),
                        "created": datetime.fromtimestamp(report_file.stat().st_mtime).isoformat()
                    })
            
            results[bot] = tasks
        
        self.state["tasks"] = {bot: len(tasks) for bot, tasks in results.items()}
        self._save_state()
        
        return results
    
    def _extract_task_id(self, content: str) -> str:
        """从委派单中提取任务 ID"""
        import re
        match = re.search(r'TASK-\d{8}-\w+-\d+', content)
        return match.group(0) if match else None
    
    def check_overdue(self, deadline: str = "18:00") -> List[Dict]:
        """检查逾期任务"""
        overdue = []
        now = datetime.now()
        
        # 解析截止时间
        try:
            deadline_time = datetime.strptime(deadline, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
        except:
            deadline_time = now.replace(hour=18, minute=0)
        
        # 如果已过截止时间
        if now > deadline_time:
            for bot, tasks in self.scan_all_bots().items():
                for task in tasks:
                    if task["status"] in ["pending", "in_progress"]:
                        overdue.append({
                            "bot": bot,
                            "task_id": task["id"],
                            "status": task["status"],
                            "overdue_hours": (now - deadline_time).seconds / 3600
                        })
        
        return overdue
    
    def generate_status_report(self) -> str:
        """生成状态报告"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        report_file = WORKSPACE / "reports" / f"task-tracker-status-{timestamp}.md"
        
        all_tasks = self.scan_all_bots()
        
        content = f"""# 任务追踪状态报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Task Tracker v1.0**

---

## 📊 任务总览

| Bot | 任务数 | 状态 |
|-----|--------|------|
"""
        
        for bot, tasks in all_tasks.items():
            completed = sum(1 for t in tasks if t.get("status") == "completed")
            in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
            pending = sum(1 for t in tasks if t.get("status") == "pending")
            
            content += f"| {bot} | {len(tasks)} | ✅{completed} 🟡{in_progress} ⏳{pending} |\n"
        
        content += f"""
---

## 📋 任务详情

"""
        for bot, tasks in all_tasks.items():
            if tasks:
                content += f"### {bot}\n\n"
                for task in tasks:
                    status_emoji = {"completed": "✅", "in_progress": "🟡", "pending": "⏳", "blocked": "🔴"}.get(task.get("status", "pending"), "⏳")
                    content += f"- {status_emoji} `{task['id']}`\n"
                content += "\n"
        
        content += f"""---

*Task Tracker v1.0 | 太一 AGI*
"""
        
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(content, encoding='utf-8')
        
        return str(report_file)


def main():
    """主函数"""
    tracker = TaskTracker()
    
    import sys
    if len(sys.argv) < 2:
        command = "scan"
    else:
        command = sys.argv[1]
    
    if command == "scan":
        results = tracker.scan_all_bots()
        for bot, tasks in results.items():
            print(f"🤖 {bot}: {len(tasks)} 个任务")
            for task in tasks[:5]:  # 显示前 5 个
                status_emoji = {"completed": "✅", "in_progress": "🟡", "pending": "⏳", "blocked": "🔴"}.get(task.get("status", "pending"), "⏳")
                print(f"  {status_emoji} {task['id']}")
    
    elif command == "overdue":
        overdue = tracker.check_overdue()
        if overdue:
            print(f"⚠️ 发现 {len(overdue)} 个逾期任务:")
            for task in overdue:
                print(f"  🔴 {task['bot']}/{task['task_id']} (逾期{task['overdue_hours']:.1f}小时)")
        else:
            print("✅ 无逾期任务")
    
    elif command == "report":
        report = tracker.generate_status_report()
        print(f"✅ 状态报告已生成：{report}")
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
