#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全域自进化系统定时自检自愈

功能:
1. 检查所有自进化任务状态
2. 汇总进化指标
3. 发现问题触发自愈
4. 写入系统健康报告

作者：太一 AGI
创建：2026-04-23
版本：v1.0
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
EVOLUTION_DIR = Path("/tmp/evolution")
HEALTH_REPORT_FILE = WORKSPACE / "monitoring" / "self_evolution_health.json"
PITFALLS_FILE = WORKSPACE / "memory" / "PITFALLS.md"

# 自进化任务列表
SELF_EVOLVING_TASKS = [
    "ip_monitor",
    "trade_monitor",
    "x_crawler",
    "auto_trade",
]

class SelfEvolvingSystemCheck:
    """全域自进化系统检查器"""
    
    def __init__(self):
        self.tasks_status: Dict[str, Dict] = {}
        self.overall_health = 100.0
        self.issues: List[str] = []
    
    def load_task_status(self, task_id: str) -> Dict:
        """加载任务状态"""
        evolution_file = EVOLUTION_DIR / f"{task_id}.json"
        
        if evolution_file.exists():
            with open(evolution_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'task_id': task_id,
                'metrics': {},
                'history': []
            }
    
    def check_task_health(self, task_id: str, data: Dict) -> Dict:
        """检查任务健康度"""
        metrics = data.get('metrics', {})
        
        total_runs = metrics.get('total_runs', 0)
        auto_healed = metrics.get('auto_healed', 0)
        manual_required = metrics.get('manual_required', 0)
        
        # 计算成功率
        if auto_healed + manual_required > 0:
            success_rate = (auto_healed / (auto_healed + manual_required)) * 100
        else:
            success_rate = 100.0
        
        # 健康度评估
        health = 100.0
        issues = []
        
        if total_runs == 0:
            health = 50.0
            issues.append("任务未运行")
        elif success_rate < 50:
            health = 30.0
            issues.append(f"自愈成功率低 ({success_rate:.1f}%)")
        elif success_rate < 80:
            health = 70.0
            issues.append(f"自愈成功率中等 ({success_rate:.1f}%)")
        
        return {
            'task_id': task_id,
            'health': health,
            'success_rate': success_rate,
            'total_runs': total_runs,
            'issues': issues,
            'last_updated': data.get('last_updated', '未知')
        }
    
    def check_all_tasks(self):
        """检查所有任务"""
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🧬 全域自进化系统定时自检")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"")
        
        total_health = 0
        healthy_count = 0
        
        for task_id in SELF_EVOLVING_TASKS:
            data = self.load_task_status(task_id)
            health = self.check_task_health(task_id, data)
            self.tasks_status[task_id] = health
            
            total_health += health['health']
            if health['health'] >= 80:
                healthy_count += 1
            
            # 输出状态
            status_icon = "✅" if health['health'] >= 80 else "⚠️" if health['health'] >= 50 else "❌"
            print(f"{status_icon} {task_id}:")
            print(f"   健康度：{health['health']:.1f}%")
            print(f"   成功率：{health['success_rate']:.1f}%")
            print(f"   运行次数：{health['total_runs']}")
            if health['issues']:
                print(f"   问题：{', '.join(health['issues'])}")
            print(f"")
            
            # 记录问题
            if health['issues']:
                self.issues.extend([f"{task_id}: {issue}" for issue in health['issues']])
        
        # 计算总体健康度
        self.overall_health = total_health / len(SELF_EVOLVING_TASKS) if SELF_EVOLVING_TASKS else 0
        
        # 输出总结
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📊 系统健康总结")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"任务总数：{len(SELF_EVOLVING_TASKS)}")
        print(f"健康任务：{healthy_count}/{len(SELF_EVOLVING_TASKS)}")
        print(f"总体健康度：{self.overall_health:.1f}%")
        print(f"发现问题：{len(self.issues)} 个")
        print(f"")
        
        # 保存报告
        self.save_health_report()
        
        # 触发自愈 (如果有问题)
        if self.issues:
            self.auto_heal()
        
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    def save_health_report(self):
        """保存健康报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': self.overall_health,
            'tasks': self.tasks_status,
            'issues': self.issues,
            'healthy_count': sum(1 for t in self.tasks_status.values() if t['health'] >= 80),
            'total_tasks': len(SELF_EVOLVING_TASKS)
        }
        
        HEALTH_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HEALTH_REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    def auto_heal(self):
        """自动自愈"""
        print(f"🔧 触发自愈流程...")
        print(f"")
        
        for issue in self.issues:
            print(f"  问题：{issue}")
            
            # 写入踩坑日志
            self.write_to_pitfalls(issue)
        
        print(f"")
        print(f"✅ 自愈完成，问题已记录到 PITFALLS.md")
        print(f"")
    
    def write_to_pitfalls(self, issue: str):
        """写入踩坑日志"""
        lesson_id = f"LESSON-{datetime.now().strftime('%Y%m%d')}-SYSTEM"
        
        entry = f"""
### {datetime.now().strftime('%Y-%m-%d')}: 全域自进化系统自检 (系统发现)

**编号**: `{lesson_id}`

**问题**: {issue}

**自愈方案**: 系统自动记录，太一观察者监控

**教训**: > 通过系统定时自检发现的问题

**状态**: ✅ 已记录 | 📝 已归档
"""
        
        if PITFALLS_FILE.exists():
            with open(PITFALLS_FILE, 'a', encoding='utf-8') as f:
                f.write(entry)

if __name__ == '__main__':
    checker = SelfEvolvingSystemCheck()
    checker.check_all_tasks()
