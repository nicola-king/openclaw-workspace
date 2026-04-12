#!/usr/bin/env python3
"""
任务依赖追踪器 v1.0
灵感来源：AI Novel Generator 伏笔追踪系统

功能:
1. 记录任务依赖关系
2. 自动追踪未完成事项
3. 到期提醒
4. 依赖链分析
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class DependencyTracker:
    """任务依赖追踪器"""
    
    def __init__(self, state_file: str = "/home/nicola/.openclaw/workspace/data/task-dependencies.json"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks: Dict[str, Dict] = {}
        self._load_state()
    
    def _load_state(self):
        """加载状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = data.get('tasks', {})
    
    def _save_state(self):
        """保存状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump({
                "tasks": self.tasks,
                "updated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def add_task(self, task_id: str, name: str, dependencies: List[str] = None,
                 deadline: str = None, priority: str = "P1") -> Dict:
        """添加任务"""
        task = {
            "id": task_id,
            "name": name,
            "status": TaskStatus.PENDING.value,
            "dependencies": dependencies or [],
            "deadline": deadline,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None,
            "metadata": {}
        }
        
        self.tasks[task_id] = task
        self._save_state()
        
        print(f"✅ 任务已添加：{task_id} - {name}")
        if dependencies:
            print(f"   依赖：{', '.join(dependencies)}")
        if deadline:
            print(f"   截止：{deadline}")
        
        return task
    
    def update_status(self, task_id: str, status: TaskStatus, metadata: Dict = None):
        """更新任务状态"""
        if task_id not in self.tasks:
            print(f"⚠️ 任务不存在：{task_id}")
            return
        
        task = self.tasks[task_id]
        task["status"] = status.value
        task["updated_at"] = datetime.now().isoformat()
        
        if status == TaskStatus.COMPLETED:
            task["completed_at"] = datetime.now().isoformat()
        
        if metadata:
            task["metadata"].update(metadata)
        
        self._save_state()
        print(f"✅ 任务更新：{task_id} → {status.value}")
    
    def check_dependencies(self, task_id: str) -> Dict:
        """检查任务依赖是否满足"""
        if task_id not in self.tasks:
            return {"ready": False, "reason": "任务不存在"}
        
        task = self.tasks[task_id]
        deps = task.get("dependencies", [])
        
        if not deps:
            return {"ready": True, "reason": "无依赖"}
        
        unmet = []
        for dep_id in deps:
            if dep_id not in self.tasks:
                unmet.append(f"{dep_id} (不存在)")
            elif self.tasks[dep_id]["status"] != TaskStatus.COMPLETED.value:
                unmet.append(f"{dep_id} ({self.tasks[dep_id]['status']})")
        
        if unmet:
            return {
                "ready": False,
                "reason": "依赖未满足",
                "unmet_dependencies": unmet
            }
        else:
            return {
                "ready": True,
                "reason": "所有依赖已完成"
            }
    
    def get_blocked_tasks(self) -> List[Dict]:
        """获取被阻塞的任务"""
        blocked = []
        for task_id, task in self.tasks.items():
            if task["status"] == TaskStatus.PENDING.value:
                check = self.check_dependencies(task_id)
                if not check["ready"]:
                    blocked.append({
                        "id": task_id,
                        "name": task["name"],
                        "reason": check["reason"],
                        "unmet": check.get("unmet_dependencies", [])
                    })
        return blocked
    
    def get_due_tasks(self, days_ahead: int = 3) -> List[Dict]:
        """获取即将到期的任务"""
        due = []
        now = datetime.now()
        deadline = now + timedelta(days=days_ahead)
        
        for task_id, task in self.tasks.items():
            if task["status"] in [TaskStatus.PENDING.value, TaskStatus.IN_PROGRESS.value]:
                task_deadline = task.get("deadline")
                if task_deadline:
                    try:
                        dl = datetime.fromisoformat(task_deadline)
                        if dl <= deadline:
                            due.append({
                                "id": task_id,
                                "name": task["name"],
                                "deadline": task_deadline,
                                "days_left": (dl - now).days,
                                "priority": task["priority"]
                            })
                    except:
                        pass
        
        return sorted(due, key=lambda x: x["deadline"])
    
    def get_dependency_chain(self, task_id: str) -> List[str]:
        """获取任务依赖链"""
        chain = []
        visited = set()
        
        def traverse(tid):
            if tid in visited or tid not in self.tasks:
                return
            visited.add(tid)
            task = self.tasks[tid]
            for dep in task.get("dependencies", []):
                traverse(dep)
            chain.append(tid)
        
        traverse(task_id)
        return chain
    
    def generate_report(self) -> str:
        """生成依赖追踪报告"""
        report = []
        report.append("# 任务依赖追踪报告")
        report.append(f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # 总体统计
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t["status"] == TaskStatus.COMPLETED.value)
        pending = sum(1 for t in self.tasks.values() if t["status"] == TaskStatus.PENDING.value)
        blocked = len(self.get_blocked_tasks())
        
        report.append(f"\n## 总体状态")
        report.append(f"- 总任务数：{total}")
        report.append(f"- 已完成：{completed} ({completed/total*100:.1f}%)")
        report.append(f"- 待处理：{pending}")
        report.append(f"- 被阻塞：{blocked}")
        
        # 被阻塞任务
        blocked_tasks = self.get_blocked_tasks()
        if blocked_tasks:
            report.append(f"\n## 🚨 被阻塞任务 ({len(blocked_tasks)})")
            for bt in blocked_tasks[:5]:
                report.append(f"- **{bt['name']}**")
                report.append(f"  - 原因：{bt['reason']}")
                report.append(f"  - 未满足：{', '.join(bt['unmet'])}")
        
        # 即将到期
        due_tasks = self.get_due_tasks()
        if due_tasks:
            report.append(f"\n## ⏰ 即将到期 ({len(due_tasks)})")
            for dt in due_tasks[:5]:
                report.append(f"- **{dt['name']}** [{dt['priority']}]")
                report.append(f"  - 截止：{dt['deadline'][:10]}")
                report.append(f"  - 剩余：{dt['days_left']} 天")
        
        return "\n".join(report)

# 使用示例
if __name__ == "__main__":
    tracker = DependencyTracker()
    
    # 添加示例任务
    tracker.add_task("TASK-001", "数据采集", priority="P0")
    tracker.add_task("TASK-002", "数据分析", dependencies=["TASK-001"], priority="P0")
    tracker.add_task("TASK-003", "报告生成", dependencies=["TASK-002"], deadline="2026-04-10", priority="P1")
    
    # 更新状态
    tracker.update_status("TASK-001", TaskStatus.COMPLETED)
    
    # 检查依赖
    print("\n🔍 检查依赖:")
    for tid in ["TASK-001", "TASK-002", "TASK-003"]:
        check = tracker.check_dependencies(tid)
        status = "✅ 就绪" if check["ready"] else f"❌ {check['reason']}"
        print(f"  {tid}: {status}")
    
    # 生成报告
    print("\n" + "="*50)
    print(tracker.generate_report())
