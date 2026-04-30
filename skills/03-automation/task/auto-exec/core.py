#!/usr/bin/env python3
"""
Auto-Exec Skill - 自动执行引擎
状态管理与任务追踪核心模块
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any

class AutoExecStatus:
    """自动执行状态管理器"""
    
    STATUS_FILE = Path("/tmp/auto-exec-status.json")
    TRACKER_FILE = Path("/tmp/task-tracker.json")
    HISTORY_FILE = Path("/tmp/progress-history.json")
    BLOCKED_FILE = Path("/tmp/blocked-tasks.json")
    
    def __init__(self):
        self._ensure_files()
    
    def _ensure_files(self):
        """确保状态文件存在"""
        for f in [self.STATUS_FILE, self.TRACKER_FILE, self.HISTORY_FILE, self.BLOCKED_FILE]:
            if not f.exists():
                f.parent.mkdir(parents=True, exist_ok=True)
                self._write_json(f, self._default_for(f))
    
    def _default_for(self, path: Path) -> dict:
        """返回文件的默认结构"""
        if path == self.STATUS_FILE:
            return {
                "lastUpdate": datetime.now(timezone.utc).isoformat(),
                "currentTask": None,
                "progress": 0,
                "status": "idle",
                "nextStep": "等待任务发现",
                "eta": None,
                "completedSteps": [],
                "blockedSteps": [],
                "skippedTasks": [],
                "errors": [],
                "autoExecActivated": True,
                "reportInterval": 300
            }
        elif path == self.TRACKER_FILE:
            return {
                "activeTasks": [],
                "completedToday": [],
                "blockedTasks": [],
                "nextCheck": datetime.now(timezone.utc).isoformat()
            }
        elif path == self.HISTORY_FILE:
            return {"entries": []}
        elif path == self.BLOCKED_FILE:
            return {"tasks": []}
        return {}
    
    def _read_json(self, path: Path) -> dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return self._default_for(path)
    
    def _write_json(self, path: Path, data: dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_status(self) -> dict:
        """获取当前执行状态"""
        return self._read_json(self.STATUS_FILE)
    
    def update_status(self, **kwargs):
        """更新执行状态"""
        status = self.get_status()
        status["lastUpdate"] = datetime.now(timezone.utc).isoformat()
        for key, value in kwargs.items():
            if key in status:
                status[key] = value
        self._write_json(self.STATUS_FILE, status)
    
    def set_task(self, task_id: str, task_name: str, progress: int = 0):
        """设置当前任务"""
        self.update_status(
            currentTask=task_id,
            progress=progress,
            status="running",
            nextStep="执行中"
        )
    
    def complete_step(self, step_name: str):
        """标记步骤完成"""
        status = self.get_status()
        if step_name not in status["completedSteps"]:
            status["completedSteps"].append(f"{step_name} ✅")
            self._write_json(self.STATUS_FILE, status)
    
    def block_task(self, task_id: str, reason: str):
        """标记任务阻塞"""
        status = self.get_status()
        status["blockedSteps"].append({
            "id": task_id,
            "reason": reason,
            "blockedAt": datetime.now(timezone.utc).isoformat()
        })
        status["status"] = "blocked"
        self._write_json(self.STATUS_FILE, status)
        
        # 添加到阻塞文件
        blocked = self._read_json(self.BLOCKED_FILE)
        blocked["tasks"].append({
            "id": task_id,
            "reason": reason,
            "blockedAt": datetime.now(timezone.utc).isoformat()
        })
        self._write_json(self.BLOCKED_FILE, blocked)
    
    def skip_task(self, task_id: str, reason: str):
        """跳过任务（阻塞时）"""
        status = self.get_status()
        status["skippedTasks"].append({
            "id": task_id,
            "reason": reason,
            "skipAt": datetime.now(timezone.utc).isoformat()
        })
        self._write_json(self.STATUS_FILE, status)
    
    def complete_task(self, task_id: str):
        """完成任务"""
        tracker = self._read_json(self.TRACKER_FILE)
        tracker["completedToday"].append(task_id)
        self._write_json(self.TRACKER_FILE, tracker)
        
        self.update_status(
            currentTask=None,
            progress=100,
            status="completed",
            nextStep="等待下一个任务"
        )
    
    def log_progress(self, task_id: str, progress: int, note: str = ""):
        """记录进度历史"""
        history = self._read_json(self.HISTORY_FILE)
        history["entries"].append({
            "taskId": task_id,
            "progress": progress,
            "note": note,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        # 保留最近 100 条
        history["entries"] = history["entries"][-100:]
        self._write_json(self.HISTORY_FILE, history)
    
    def get_tracker(self) -> dict:
        """获取任务追踪器"""
        return self._read_json(self.TRACKER_FILE)
    
    def add_active_task(self, task: dict):
        """添加活跃任务"""
        tracker = self.get_tracker()
        tracker["activeTasks"].append(task)
        self._write_json(self.TRACKER_FILE, tracker)
    
    def remove_active_task(self, task_id: str):
        """移除活跃任务"""
        tracker = self.get_tracker()
        tracker["activeTasks"] = [t for t in tracker["activeTasks"] if t.get("id") != task_id]
        self._write_json(self.TRACKER_FILE, tracker)


class TaskDiscovery:
    """任务发现器"""
    
    def __init__(self):
        self.workspace = Path.home() / ".openclaw" / "workspace"
    
    def discover(self) -> List[dict]:
        """发现所有待执行任务"""
        tasks = []
        
        # 从 HEARTBEAT.md 读取 P0 任务
        heartbeat = self.workspace / "HEARTBEAT.md"
        if heartbeat.exists():
            tasks.extend(self._parse_heartbeat(heartbeat.read_text()))
        
        # 从 memory/residual.md 读取 P1/P2 任务
        residual = self.workspace / "memory" / "residual.md"
        if residual.exists():
            tasks.extend(self._parse_residual(residual.read_text()))
        
        # 按优先级排序
        tasks.sort(key=lambda t: {"P0": 0, "P1": 1, "P2": 2}.get(t.get("priority", "P2"), 2))
        
        return tasks
    
    def _parse_heartbeat(self, content: str) -> List[dict]:
        """解析 HEARTBEAT.md"""
        tasks = []
        in_table = False
        
        for line in content.split("\n"):
            if "| TASK-" in line and "|" in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 4:
                    task_id = parts[0]
                    name = parts[1]
                    status = parts[2]
                    next_step = parts[3] if len(parts) > 3 else ""
                    
                    # 只获取待执行任务
                    if "🟡" in status or "🔴" in status:
                        tasks.append({
                            "id": task_id,
                            "name": name,
                            "priority": "P0",
                            "status": "pending",
                            "nextStep": next_step
                        })
        
        return tasks
    
    def _parse_residual(self, content: str) -> List[dict]:
        """解析 residual.md"""
        # 简化实现：查找 TASK-XXX 模式
        import re
        tasks = []
        
        for match in re.finditer(r'(TASK-\d+)\s*[:：]\s*(.+?)(?:\n|$)', content):
            task_id = match.group(1)
            name = match.group(2).strip()
            
            tasks.append({
                "id": task_id,
                "name": name,
                "priority": "P1",
                "status": "pending"
            })
        
        return tasks[:20]  # 限制数量


# 便捷函数
def status() -> dict:
    """获取执行状态"""
    return AutoExecStatus().get_status()

def discover_tasks() -> List[dict]:
    """发现任务"""
    return TaskDiscovery().discover()

def update_status(**kwargs):
    """更新状态"""
    AutoExecStatus().update_status(**kwargs)

if __name__ == "__main__":
    # 测试
    engine = AutoExecStatus()
    print("当前状态:", json.dumps(engine.get_status(), indent=2, ensure_ascii=False))
    
    discovery = TaskDiscovery()
    tasks = discovery.discover()
    print(f"\n发现 {len(tasks)} 个任务:")
    for task in tasks[:5]:
        print(f"  - {task['id']}: {task['name']} [{task['priority']}]")
