#!/usr/bin/env python3
"""
Task Tracker - 任务追踪与模式识别

功能:
- 记录任务执行历史
- 识别任务模式
- 统计任务频率
- 检测重复任务类型

作者：太一 AGI
创建：2026-04-09
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
HEARTBEAT_FILE = WORKSPACE / "HEARTBEAT.md"
TASK_HISTORY_FILE = WORKSPACE / "skills/hermes-learning-loop/task_history.json"


@dataclass
class TaskRecord:
    """任务记录"""
    id: str
    name: str
    status: str  # todo/doing/done
    priority: str  # P0/P1/P2
    assignee: str
    due: str
    next_step: str
    tags: List[str]
    created_at: str
    completed_at: Optional[str] = None
    execution_count: int = 0
    avg_duration_minutes: float = 0.0


@dataclass
class TaskPattern:
    """任务模式"""
    task_type: str
    keywords: List[str]
    frequency: int
    last_executed: str
    avg_complexity: float  # 1-10
    common_steps: List[str]
    dependencies: List[str]
    success_rate: float  # 0-1


class TaskTracker:
    """任务追踪器"""
    
    def __init__(self):
        self.history = self.load_history()
        self.patterns = self.load_patterns()
    
    def load_history(self) -> List[TaskRecord]:
        """加载任务历史"""
        if TASK_HISTORY_FILE.exists():
            with open(TASK_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [TaskRecord(**r) for r in data]
        return []
    
    def save_history(self):
        """保存任务历史"""
        TASK_HISTORY_FILE.parent.mkdir(exist_ok=True)
        with open(TASK_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(r) for r in self.history],
                f,
                indent=2,
                ensure_ascii=False
            )
    
    def load_patterns(self) -> Dict[str, TaskPattern]:
        """加载任务模式"""
        pattern_file = WORKSPACE / "skills/hermes-learning-loop/task_patterns.json"
        if pattern_file.exists():
            with open(pattern_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {k: TaskPattern(**v) for k, v in data.items()}
        return {}
    
    def save_patterns(self):
        """保存任务模式"""
        pattern_file = WORKSPACE / "skills/hermes-learning-loop/task_patterns.json"
        pattern_file.parent.mkdir(exist_ok=True)
        with open(pattern_file, "w", encoding="utf-8") as f:
            json.dump(
                {k: asdict(v) for k, v in self.patterns.items()},
                f,
                indent=2,
                ensure_ascii=False
            )
    
    def parse_heartbeat(self) -> List[TaskRecord]:
        """解析 HEARTBEAT.md 获取当前任务"""
        if not HEARTBEAT_FILE.exists():
            return []
        
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        tasks = []
        # 解析任务表格：| **TASK-XXX** | 任务名 | 状态 | 下一步 | 截止 |
        pattern = r'\|\s*\*\*(TASK-\d+)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|'
        
        for match in re.finditer(pattern, content):
            task_id = match.group(1)
            name = match.group(2).strip()
            status_raw = match.group(3).strip()
            next_step = match.group(4).strip()
            due = match.group(5).strip()
            
            # 解析状态
            if '✅' in status_raw or '完成' in status_raw:
                status = 'done'
            elif '🟡' in status_raw or 'MVP' in status_raw:
                status = 'doing'
            else:
                status = 'todo'
            
            # 解析优先级
            priority = 'P2'
            if 'P0' in name or '🔴' in status_raw:
                priority = 'P0'
            elif 'P1' in name or '🟡' in status_raw:
                priority = 'P1'
            
            # 提取标签
            tags = []
            if 'Hermes' in name:
                tags.append('学习循环')
            if 'CLI' in name:
                tags.append('CLI')
            if '技能' in name or 'Skill' in name:
                tags.append('技能开发')
            if 'Dashboard' in name:
                tags.append('可视化')
            
            # 检查是否已存在
            existing = next((t for t in self.history if t.id == task_id), None)
            
            task = TaskRecord(
                id=task_id,
                name=name,
                status=status,
                priority=priority,
                assignee='太一',
                due=due,
                next_step=next_step,
                tags=tags,
                created_at=existing.created_at if existing else datetime.now().isoformat(),
                completed_at=datetime.now().isoformat() if status == 'done' else None,
                execution_count=existing.execution_count + 1 if existing else 1,
            )
            
            tasks.append(task)
        
        return tasks
    
    def update_history(self, tasks: List[TaskRecord]):
        """更新任务历史"""
        for task in tasks:
            existing = next((t for t in self.history if t.id == task.id), None)
            if existing:
                # 更新现有任务
                existing.status = task.status
                existing.next_step = task.next_step
                if task.status == 'done' and not existing.completed_at:
                    existing.completed_at = task.completed_at
            else:
                # 添加新任务
                self.history.append(task)
        
        self.save_history()
    
    def extract_task_type(self, task_name: str) -> str:
        """从任务名提取任务类型"""
        # 关键词映射
        type_keywords = {
            'skill': '技能开发',
            'skill-creation': '技能开发',
            'dashboard': '可视化开发',
            'kanban': '可视化开发',
            'learning': '学习集成',
            'hermes': '学习集成',
            'cli': 'CLI 集成',
            'integration': '系统集成',
            'repair': '系统修复',
            'fix': '系统修复',
            'cron': '定时任务',
            'task': '任务管理',
        }
        
        name_lower = task_name.lower()
        for keyword, task_type in type_keywords.items():
            if keyword in name_lower:
                return task_type
        
        # 默认按标签分类
        return '通用任务'
    
    def detect_patterns(self) -> Dict[str, TaskPattern]:
        """检测任务模式"""
        # 按任务类型分组
        type_groups = defaultdict(list)
        for task in self.history:
            task_type = self.extract_task_type(task.name)
            type_groups[task_type].append(task)
        
        # 分析每个类型
        patterns = {}
        for task_type, tasks in type_groups.items():
            if len(tasks) < 1:
                continue
            
            # 提取关键词
            keywords = self._extract_keywords([t.name for t in tasks])
            
            # 计算平均复杂度 (基于任务名长度和步骤数)
            avg_complexity = sum(len(t.name) for t in tasks) / len(tasks) / 10
            avg_complexity = min(10, max(1, avg_complexity))
            
            # 常见步骤
            common_steps = list(set(t.next_step for t in tasks if t.next_step))[:5]
            
            # 依赖
            dependencies = []
            if 'CLI' in task_type:
                dependencies.append('Python 3.10+')
            if '可视化' in task_type:
                dependencies.append('Node.js 18+')
            
            # 成功率
            completed = len([t for t in tasks if t.status == 'done'])
            success_rate = completed / len(tasks) if tasks else 0
            
            patterns[task_type] = TaskPattern(
                task_type=task_type,
                keywords=keywords,
                frequency=len(tasks),
                last_executed=max(t.created_at for t in tasks),
                avg_complexity=round(avg_complexity, 1),
                common_steps=common_steps,
                dependencies=dependencies,
                success_rate=round(success_rate, 2)
            )
        
        self.patterns = patterns
        self.save_patterns()
        return patterns
    
    def _extract_keywords(self, task_names: List[str]) -> List[str]:
        """从任务名提取共同关键词"""
        from collections import Counter
        
        words = []
        for name in task_names:
            # 简单分词
            ws = re.findall(r'[\w\u4e00-\u9fff]+', name.lower())
            words.extend([w for w in ws if len(w) > 1])
        
        # 返回最常见的 5 个词
        counter = Counter(words)
        return [word for word, _ in counter.most_common(5)]
    
    def get_repetition_alerts(self, threshold: int = 3) -> List[Dict]:
        """获取重复任务告警"""
        alerts = []
        
        # 按类型分组
        type_groups = defaultdict(list)
        for task in self.history:
            task_type = self.extract_task_type(task.name)
            type_groups[task_type].append(task)
        
        # 检查重复
        for task_type, tasks in type_groups.items():
            if len(tasks) >= threshold:
                alerts.append({
                    'task_type': task_type,
                    'count': len(tasks),
                    'task_ids': [t.id for t in tasks[-threshold:]],
                    'recommendation': f'建议创建"{task_type}"自动化技能',
                    'priority': 'P0' if len(tasks) >= 5 else 'P1'
                })
        
        return alerts
    
    def get_stats(self) -> Dict:
        """获取任务统计"""
        total = len(self.history)
        completed = len([t for t in self.history if t.status == 'done'])
        doing = len([t for t in self.history if t.status == 'doing'])
        todo = len([t for t in self.history if t.status == 'todo'])
        
        # 按优先级
        p0 = len([t for t in self.history if t.priority == 'P0'])
        p1 = len([t for t in self.history if t.priority == 'P1'])
        p2 = len([t for t in self.history if t.priority == 'P2'])
        
        # 按类型
        type_counts = defaultdict(int)
        for task in self.history:
            task_type = self.extract_task_type(task.name)
            type_counts[task_type] += 1
        
        return {
            'total': total,
            'completed': completed,
            'doing': doing,
            'todo': todo,
            'by_priority': {'P0': p0, 'P1': p1, 'P2': p2},
            'by_type': dict(type_counts),
            'patterns_detected': len(self.patterns),
            'last_updated': datetime.now().isoformat()
        }


def main():
    """主函数"""
    tracker = TaskTracker()
    
    print("🔍 太一任务追踪器 v1.0")
    print("=" * 50)
    
    # 解析当前任务
    tasks = tracker.parse_heartbeat()
    tracker.update_history(tasks)
    print(f"✅ 加载任务：{len(tasks)} 个")
    
    # 检测模式
    patterns = tracker.detect_patterns()
    print(f"✅ 检测模式：{len(patterns)} 个")
    
    # 显示告警
    alerts = tracker.get_repetition_alerts()
    if alerts:
        print(f"\n⚠️  发现 {len(alerts)} 个重复任务类型:")
        for alert in alerts:
            print(f"  - {alert['task_type']}: {alert['count']} 次 (建议：{alert['recommendation']})")
    else:
        print("\n✅ 无重复任务告警")
    
    # 显示统计
    stats = tracker.get_stats()
    print(f"\n📊 任务统计:")
    print(f"  总计：{stats['total']} | 完成：{stats['completed']} | 进行中：{stats['doing']}")
    print(f"  P0: {stats['by_priority']['P0']} | P1: {stats['by_priority']['P1']} | P2: {stats['by_priority']['P2']}")
    
    return tracker


if __name__ == "__main__":
    main()
