#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一任务看板 - 可视化管理后台
参考：AI 军团 8 Agent 管理后台
功能：Bot 状态/任务进度/统计报表
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class TaiyiDashboard:
    """太一任务看板"""
    
    def __init__(self):
        self.bots = {
            'taiyi': {'name': '太一', 'role': '统筹/决策', 'status': 'online'},
            'zhiji': {'name': '知几', 'role': '量化交易', 'status': 'online'},
            'shanmu': {'name': '山木', 'role': '内容创意', 'status': 'online'},
            'suwen': {'name': '素问', 'role': '技术开发', 'status': 'online'},
            'wangliang': {'name': '罔两', 'role': '数据/CEO', 'status': 'online'},
            'paoding': {'name': '庖丁', 'role': '预算成本', 'status': 'online'},
        }
        self.tasks: List[Dict] = []
        self.stats = {
            'total_tasks': 0,
            'completed': 0,
            'pending': 0,
            'failed': 0,
        }
    
    def add_task(self, task: Dict):
        """添加任务"""
        self.tasks.append({
            'id': task.get('id', f'TASK-{len(self.tasks)+1:03d}'),
            'name': task.get('name', '未知任务'),
            'bot': task.get('bot', 'taiyi'),
            'priority': task.get('priority', 'P2'),
            'status': task.get('status', 'pending'),
            'created_at': task.get('created_at', datetime.now().isoformat()),
            'completed_at': task.get('completed_at', None),
        })
        self.stats['total_tasks'] += 1
        self.stats['pending'] += 1
    
    def complete_task(self, task_id: str):
        """完成任务"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                self.stats['completed'] += 1
                self.stats['pending'] -= 1
                break
    
    def get_bot_status(self) -> Dict:
        """获取 Bot 状态"""
        return self.bots
    
    def get_task_summary(self) -> Dict:
        """获取任务摘要"""
        return {
            'total': self.stats['total_tasks'],
            'completed': self.stats['completed'],
            'pending': self.stats['pending'],
            'failed': self.stats['failed'],
            'completion_rate': f"{self.stats['completed']/max(1,self.stats['total_tasks'])*100:.1f}%"
        }
    
    def get_recent_tasks(self, limit: int = 10) -> List[Dict]:
        """获取最近任务"""
        return sorted(self.tasks, key=lambda x: x['created_at'], reverse=True)[:limit]
    
    def render_dashboard(self) -> str:
        """渲染看板"""
        lines = []
        lines.append("=" * 60)
        lines.append("  太一任务管理看板")
        lines.append("=" * 60)
        lines.append("")
        
        # Bot 状态
        lines.append("【Bot 状态】")
        for bot_id, bot in self.bots.items():
            status_icon = "🟢" if bot['status'] == 'online' else "🔴"
            lines.append(f"  {status_icon} {bot['name']}: {bot['role']}")
        lines.append("")
        
        # 任务统计
        summary = self.get_task_summary()
        lines.append("【任务统计】")
        lines.append(f"  总计：{summary['total']}")
        lines.append(f"  完成：{summary['completed']}")
        lines.append(f"  进行中：{summary['pending']}")
        lines.append(f"  失败：{summary['failed']}")
        lines.append(f"  完成率：{summary['completion_rate']}")
        lines.append("")
        
        # 最近任务
        lines.append("【最近任务】")
        for task in self.get_recent_tasks(5):
            status_icon = "✅" if task['status'] == 'completed' else "🟡"
            lines.append(f"  {status_icon} {task['id']}: {task['name']} ({task['bot']})")
        lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    dashboard = TaiyiDashboard()
    
    # 添加测试任务
    dashboard.add_task({'id': 'TASK-001', 'name': '气象数据采集', 'bot': '知几', 'status': 'completed'})
    dashboard.add_task({'id': 'TASK-002', 'name': '晨间内容发布', 'bot': '山木', 'status': 'completed'})
    dashboard.add_task({'id': 'TASK-003', 'name': '午间进度汇报', 'bot': '太一', 'status': 'pending'})
    dashboard.add_task({'id': 'TASK-004', 'name': 'X 热点搜索', 'bot': '罔两', 'status': 'pending'})
    
    # 完成任务
    dashboard.complete_task('TASK-001')
    dashboard.complete_task('TASK-002')
    
    # 渲染看板
    print(dashboard.render_dashboard())
