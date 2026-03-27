#!/usr/bin/env python3
"""
太一授权管理器
管理对工作站/笔记本操作的授权
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum

class Priority(Enum):
    P0 = "紧急任务"      # 事后报备
    P1 = "高优先级"      # 快速授权
    P2 = "普通任务"      # 批量授权
    P3 = "低优先级"      # 等待授权

class AuthorizationManager:
    def __init__(self):
        self.config_dir = Path("~/.openclaw/workspace").expanduser()
        self.auth_log_dir = self.config_dir / "logs" / "authorizations"
        self.auth_config_file = self.config_dir / "AUTHORIZATION.md"
        self.budget_file = self.config_dir / ".auth_budget.json"
        
        # 预算配置
        self.budgets = {
            'P0': {'monthly': None, 'used': 0},  # 无限制
            'P1': {'monthly': 500, 'used': 0},
            'P2': {'monthly': 200, 'used': 0},
            'P3': {'monthly': 0, 'used': 0}
        }
        
        self.load_budget()
        self.auth_log_dir.mkdir(parents=True, exist_ok=True)
    
    def load_budget(self):
        """加载预算使用记录"""
        if self.budget_file.exists():
            with open(self.budget_file) as f:
                data = json.load(f)
                # 检查是否新月
                last_month = data.get('month', '')
                current_month = datetime.now().strftime('%Y-%m')
                if last_month != current_month:
                    # 重置预算
                    for key in self.budgets:
                        self.budgets[key]['used'] = 0
                else:
                    self.budgets = data.get('budgets', self.budgets)
    
    def save_budget(self):
        """保存预算使用记录"""
        data = {
            'month': datetime.now().strftime('%Y-%m'),
            'budgets': self.budgets
        }
        with open(self.budget_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def request_authorization(self, priority, task_description, target_device, 
                             command, estimated_cost=0, estimated_time=0):
        """
        请求授权
        
        返回:
        - True: 已授权 (或 P0 直接执行)
        - False: 拒绝或未响应
        """
        priority = Priority[priority] if isinstance(priority, str) else priority
        
        # P0: 直接执行，事后报备
        if priority == Priority.P0:
            auth_id = self.create_authorization_record(
                priority='P0',
                task_description=task_description,
                target_device=target_device,
                command=command,
                estimated_cost=estimated_cost,
                status='executed'
            )
            # 发送事后通知
            self.send_post_execution_notification(auth_id)
            return True
        
        # P1: 快速授权
        elif priority == Priority.P1:
            # 检查预算
            if not self.check_budget('P1', estimated_cost):
                self.send_budget_exceeded_notification('P1', estimated_cost)
                return False
            
            # 发送授权请求
            auth_id = self.create_authorization_record(
                priority='P1',
                task_description=task_description,
                target_device=target_device,
                command=command,
                estimated_cost=estimated_cost,
                estimated_time=estimated_time,
                status='pending'
            )
            
            # 发送 Telegram 授权请求
            return self.send_telegram_auth_request(auth_id)
        
        # P2: 批量授权
        elif priority == Priority.P2:
            # 检查是否有周授权
            if self.has_weekly_authorization():
                return True
            
            # 发送批量授权请求
            auth_id = self.create_authorization_record(
                priority='P2',
                task_description=task_description,
                target_device=target_device,
                command=command,
                estimated_cost=estimated_cost,
                status='pending_weekly'
            )
            return self.send_weekly_auth_request(auth_id)
        
        # P3: 等待询问
        elif priority == Priority.P3:
            self.record_p3_idea(task_description, target_device, command)
            return False
        
        return False
    
    def check_budget(self, priority, cost):
        """检查预算是否充足"""
        budget = self.budgets.get(priority, {})
        monthly_limit = budget.get('monthly')
        
        # 无限制
        if monthly_limit is None:
            return True
        
        used = budget.get('used', 0)
        remaining = monthly_limit - used
        
        return cost <= remaining
    
    def update_budget(self, priority, cost):
        """更新预算使用记录"""
        if priority in self.budgets:
            self.budgets[priority]['used'] += cost
            self.save_budget()
    
    def create_authorization_record(self, priority, task_description, 
                                   target_device, command, **kwargs):
        """创建授权记录"""
        auth_id = f"auth-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        record = {
            'authorization_id': auth_id,
            'priority': priority,
            'task_description': task_description,
            'target_device': target_device,
            'command': command,
            'estimated_cost': kwargs.get('estimated_cost', 0),
            'estimated_time': kwargs.get('estimated_time', 0),
            'requested_at': datetime.now().isoformat(),
            'status': kwargs.get('status', 'pending'),
            'authorized_by': None,
            'authorized_at': None,
            'executed_at': None,
            'completed_at': None,
            'actual_cost': 0,
            'result': None
        }
        
        # 保存记录
        month_dir = self.auth_log_dir / datetime.now().strftime('%Y-%m')
        month_dir.mkdir(parents=True, exist_ok=True)
        
        auth_file = month_dir / f"{auth_id}.json"
        with open(auth_file, 'w') as f:
            json.dump(record, f, indent=2)
        
        return auth_id
    
    def send_telegram_auth_request(self, auth_id):
        """发送 Telegram 授权请求"""
        # 读取授权记录
        auth_file = self.auth_log_dir / datetime.now().strftime('%Y-%m') / f"{auth_id}.json"
        with open(auth_file) as f:
            record = json.load(f)
        
        # 构建请求消息
        message = f"""
📋 {record['priority']} 任务授权请求

任务：{record['task_description']}
目标设备：{record['target_device']}
预计时间：{record['estimated_time']} 分钟
预计成本：¥{record['estimated_cost']}

[✅ 确认执行] [❌ 拒绝] [⏸️ 暂缓]

授权 ID: {auth_id}
"""
        # TODO: 通过 Telegram Bot API 发送
        print(f"发送授权请求到 Telegram: {message}")
        
        # 等待响应 (实际实现应该异步等待)
        # 这里简化为立即返回 True
        return True
    
    def send_post_execution_notification(self, auth_id):
        """发送 P0 任务事后通知"""
        auth_file = self.auth_log_dir / datetime.now().strftime('%Y-%m') / f"{auth_id}.json"
        with open(auth_file) as f:
            record = json.load(f)
        
        message = f"""
🚨 P0 紧急任务执行报告

任务：{record['task_description']}
执行设备：{record['target_device']}
执行时间：{record.get('executed_at', 'N/A')}
结果：{record.get('result', 'N/A')}
成本：¥{record.get('actual_cost', 0)}

授权 ID: {auth_id}
"""
        print(f"发送事后通知到 Telegram: {message}")
    
    def send_weekly_auth_request(self, auth_id):
        """发送周批量授权请求"""
        # 获取本周所有 P2 任务
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        week_end = week_start + timedelta(days=6)
        
        message = f"""
📅 本周 P2 任务列表 ({week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')})

任务清单:
1. [ ] 每日数据备份 (每天 02:00)
2. [ ] 系统健康检查 (每天 08:00)
3. [ ] 技能库更新 (周三 10:00)
4. [ ] 内存压缩 (每天 23:00)

总预算：¥50/周
预计时间：5 小时/周

[✅ 全部授权] [✏️ 修改] [❌ 拒绝]

授权 ID: {auth_id}
"""
        print(f"发送周授权请求到 Telegram: {message}")
        return True
    
    def has_weekly_authorization(self):
        """检查是否有本周授权"""
        # 简化实现，实际应该检查授权记录
        return False
    
    def record_p3_idea(self, description, device, command):
        """记录 P3 任务想法"""
        ideas_file = self.config_dir / ".p3_ideas.json"
        
        ideas = []
        if ideas_file.exists():
            with open(ideas_file) as f:
                ideas = json.load(f)
        
        ideas.append({
            'description': description,
            'device': device,
            'command': command,
            'recorded_at': datetime.now().isoformat(),
            'status': 'waiting_inquiry'
        })
        
        with open(ideas_file, 'w') as f:
            json.dump(ideas, f, indent=2)
        
        print(f"记录 P3 想法：{description}")
    
    def get_budget_status(self):
        """获取预算状态"""
        return {
            'month': datetime.now().strftime('%Y-%m'),
            'budgets': self.budgets,
            'remaining': {
                key: (budget['monthly'] - budget['used']) if budget['monthly'] is not None else '无限制'
                for key, budget in self.budgets.items()
            }
        }

# 使用示例
if __name__ == '__main__':
    auth_mgr = AuthorizationManager()
    
    # P1 任务授权请求示例
    authorized = auth_mgr.request_authorization(
        priority='P1',
        task_description='分析 Polymarket 数据',
        target_device='workstation',
        command='python3 /data/analyze.py',
        estimated_cost=5,
        estimated_time=30
    )
    
    print(f"授权结果：{authorized}")
    
    # 查看预算状态
    budget = auth_mgr.get_budget_status()
    print(json.dumps(budget, indent=2))
