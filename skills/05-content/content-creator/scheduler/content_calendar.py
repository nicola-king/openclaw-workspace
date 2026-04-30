#!/usr/bin/env python3
"""
Content Calendar - 内容日历管理
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class ContentTask:
    """内容任务"""
    id: str
    platform: str
    content_type: str
    scheduled_time: str
    topic: str
    status: str  # idea, draft, ready, published, archived
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")


class ContentScheduler:
    """内容排期器"""
    
    def __init__(self, db_path: str = "/home/nicola/.openclaw/workspace/data/content-calendar.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> Dict[str, ContentTask]:
        """加载任务"""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {k: ContentTask(**v) for k, v in data.items()}
        return {}
    
    def _save_tasks(self):
        """保存任务"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.tasks.items()}, f, indent=2, ensure_ascii=False)
    
    def add_task(
        self,
        platform: str,
        content_type: str,
        scheduled_time: str,
        topic: str,
        status: str = 'idea'
    ) -> str:
        """添加任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        task = ContentTask(
            id=task_id,
            platform=platform,
            content_type=content_type,
            scheduled_time=scheduled_time,
            topic=topic,
            status=status
        )
        self.tasks[task_id] = task
        self._save_tasks()
        return task_id
    
    def get_week_calendar(self, week_start: str) -> List[ContentTask]:
        """获取周日历"""
        start = datetime.strptime(week_start, "%Y-%m-%d")
        end = start + timedelta(days=7)
        
        week_tasks = []
        for task in self.tasks.values():
            task_date = datetime.strptime(task.scheduled_time[:10], "%Y-%m-%d")
            if start <= task_date < end:
                week_tasks.append(task)
        
        return sorted(week_tasks, key=lambda t: t.scheduled_time)
    
    def move_task(self, task_id: str, new_status: str):
        """移动任务状态"""
        if task_id in self.tasks:
            self.tasks[task_id].status = new_status
            self._save_tasks()
    
    def get_tasks_by_status(self, status: str) -> List[ContentTask]:
        """按状态获取任务"""
        return [t for t in self.tasks.values() if t.status == status]
