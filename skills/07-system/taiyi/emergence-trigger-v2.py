#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
能力涌现触发器 v2.0 - 动态触发 + 智能判断

触发条件 (满足任一即触发):
1. 自发秩序：同类任务重复 3 次+
2. 自我融合：跨域任务积累 5 个+ (涉及≥3 个 Bot)
3. 递归进化：现有技能迭代 3 个版本+
4. 智能涌现：新需求/新场景/新机会出现

核心原则:
- 原创第一 (≥70%)
- 零侵权 (100%)
- 价值创造 (负熵法则)
- 免费开源优先
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/emergence-trigger-v2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('EmergenceTrigger.v2')

# 配置
CONFIG = {
    'task_history_file': '/home/nicola/.openclaw/workspace/data/task-history.json',
    'skill_versions_file': '/home/nicola/.openclaw/workspace/data/skill-versions.json',
    'emergence_threshold': {
        'spontaneous_order': 3,      # 同类任务 3 次+
        'self_fusion': 5,            # 跨域任务 5 个+
        'recursive_evolution': 3,    # 技能版本 3 个+
        'intelligent_emergence': 1   # 新机会出现即触发
    },
    'core_principles': [
        'originality_70',           # 原创性≥70%
        'zero_infringement',        # 零侵权
        'value_creation',           # 价值创造
        'open_source_first'         # 免费开源优先
    ]
}

class EmergenceTriggerV2:
    """能力涌现触发器 v2.0 - 动态触发"""
    
    def __init__(self):
        self.task_history = self._load_task_history()
        self.skill_versions = self._load_skill_versions()
        
    def _load_task_history(self):
        """加载任务历史"""
        if os.path.exists(CONFIG['task_history_file']):
            with open(CONFIG['task_history_file'], 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'tasks': [], 'cross_domain_tasks': []}
    
    def _save_task_history(self):
        """保存任务历史"""
        os.makedirs(os.path.dirname(CONFIG['task_history_file']), exist_ok=True)
        with open(CONFIG['task_history_file'], 'w', encoding='utf-8') as f:
            json.dump(self.task_history, f, ensure_ascii=False, indent=2)
    
    def _load_skill_versions(self):
        """加载技能版本历史"""
        if os.path.exists(CONFIG['skill_versions_file']):
            with open(CONFIG['skill_versions_file'], 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'skills': {}}
    
    def _save_skill_versions(self):
        """保存技能版本历史"""
        os.makedirs(os.path.dirname(CONFIG['skill_versions_file']), exist_ok=True)
        with open(CONFIG['skill_versions_file'], 'w', encoding='utf-8') as f:
            json.dump(self.skill_versions, f, ensure_ascii=False, indent=2)
    
    def record_task(self, task_type, description, bot_involved=None):
        """记录任务"""
        task = {
            'type': task_type,
            'description': description,
            'bot_involved': bot_involved,
            'timestamp': datetime.now().isoformat()
        }
        
        self.task_history['tasks'].append(task)
        
        # 跨域任务追踪
        if bot_involved and len(bot_involved) >= 3:
            self.task_history['cross_domain_tasks'].append(task)
        
        self._save_task_history()
        
        logger.info(f"✅ 记录任务：{task_type} - {description}")
        
        # 检查所有触发条件
        triggers = self._check_all_triggers(task_type)
        
        return triggers
    
    def record_skill_version(self, skill_name, version):
        """记录技能版本"""
        if skill_name not in self.skill_versions['skills']:
            self.skill_versions['skills'][skill_name] = []
        
        self.skill_versions['skills'][skill_name].append({
            'version': version,
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_skill_versions()
        
        logger.info(f"✅ 记录技能版本：{skill_name} v{version}")
        
        # 检查递归进化触发
        return self._check_recursive_evolution(skill_name)
    
    def _check_all_triggers(self, task_type):
        """检查所有触发条件"""
        triggers = {
            'spontaneous_order': self._check_spontaneous_order(task_type),
            'self_fusion': self._check_self_fusion(),
            'recursive_evolution': self._check_recursive_evolution(task_type),
            'intelligent_emergence': self._check_intelligent_emergence()
        }
        
        # 返回满足的触发条件
        active_triggers = [k for k, v in triggers.items() if v['trigger']]
        
        if active_triggers:
            logger.info(f"🦞 触发能力涌现：{', '.join(active_triggers)}")
            for trigger_type in active_triggers:
                self._trigger_emergence(trigger_type, triggers[trigger_type]['reason'])
        
        return triggers
    
    def _check_spontaneous_order(self, task_type):
        """检查自发秩序 (同类任务重复 3 次+)"""
        same_type_tasks = [
            t for t in self.task_history['tasks']
            if t['type'] == task_type
        ]
        
        threshold = CONFIG['emergence_threshold']['spontaneous_order']
        
        if len(same_type_tasks) >= threshold:
            return {
                'trigger': True,
                'reason': f"同类任务重复{len(same_type_tasks)}次 (阈值{threshold})",
                'count': len(same_type_tasks)
            }
        
        return {'trigger': False, 'count': len(same_type_tasks)}
    
    def _check_self_fusion(self):
        """检查自我融合 (跨域任务积累 5 个+)"""
        cross_domain_tasks = self.task_history['cross_domain_tasks']
        
        # 按 Bot 组合分组
        bot_combinations = {}
        for task in cross_domain_tasks:
            bots = tuple(sorted(task.get('bot_involved', [])))
            if bots not in bot_combinations:
                bot_combinations[bots] = []
            bot_combinations[bots].append(task)
        
        # 找到涉及≥3 个 Bot 的组合
        for bots, tasks in bot_combinations.items():
            if len(bots) >= 3 and len(tasks) >= CONFIG['emergence_threshold']['self_fusion']:
                return {
                    'trigger': True,
                    'reason': f"跨域任务{len(tasks)}个 (Bot: {', '.join(bots)})",
                    'bots': bots,
                    'count': len(tasks)
                }
        
        return {'trigger': False}
    
    def _check_recursive_evolution(self, skill_name):
        """检查递归进化 (技能版本 3 个+)"""
        if skill_name not in self.skill_versions['skills']:
            return {'trigger': False}
        
        versions = self.skill_versions['skills'][skill_name]
        threshold = CONFIG['emergence_threshold']['recursive_evolution']
        
        if len(versions) >= threshold:
            return {
                'trigger': True,
                'reason': f"技能{skill_name}已迭代{len(versions)}个版本",
                'versions': [v['version'] for v in versions]
            }
        
        return {'trigger': False, 'versions': len(versions)}
    
    def _check_intelligent_emergence(self):
        """检查智能涌现 (新需求/新场景/新机会)"""
        # 基于外部信号判断
        # 1. 用户明确要求
        # 2. 市场热点 (小红书/X 热搜)
        # 3. 竞品发布新功能
        # 4. 技术突破 (新模型/新工具)
        
        # 这里简化为：检测到新领域任务
        recent_tasks = self.task_history['tasks'][-10:]
        new_domains = set(t['type'] for t in recent_tasks)
        
        if len(new_domains) >= 3:  # 短时间内出现 3 个新领域
            return {
                'trigger': True,
                'reason': f"新领域涌现：{', '.join(new_domains)}"
            }
        
        return {'trigger': False}
    
    def _trigger_emergence(self, trigger_type, reason):
        """触发能力涌现流程"""
        logger.info(f"🦞 能力涌现触发：{trigger_type} - {reason}")
        
        # 创建涌现报告
        report = {
            'trigger_type': trigger_type,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'week': datetime.now().strftime('%Y-W%V'),
            'core_principles': CONFIG['core_principles']
        }
        
        # 保存报告
        report_dir = f"/home/nicola/.openclaw/workspace/reports/emergence/{report['week']}"
        os.makedirs(report_dir, exist_ok=True)
        
        report_file = f"{report_dir}/emergence-{trigger_type}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📝 涌现报告已保存：{report_file}")
        
        # 发送 Telegram 通知
        self._send_telegram_notification(trigger_type, reason)
        
        return report_file
    
    def _send_telegram_notification(self, trigger_type, reason):
        """发送 Telegram 通知"""
        import requests
        
        bot_token = '8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY'
        chat_id = '7073481596'
        
        message = f"""🦞 能力涌现触发

触发类型：{trigger_type}
原因：{reason}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
核心原则：
- 原创≥70%
- 零侵权
- 价值创造
- 开源优先

报告：/home/nicola/.openclaw/workspace/reports/emergence/

---
太一 · 能力涌现协议 v2.0"""
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Telegram 通知已发送")
            else:
                logger.error(f"❌ Telegram 发送失败：{response.text}")
        except Exception as e:
            logger.error(f"❌ Telegram 发送异常：{e}")
    
    def check_status(self):
        """检查当前状态"""
        status = {
            'task_count': len(self.task_history['tasks']),
            'cross_domain_count': len(self.task_history['cross_domain_tasks']),
            'skill_count': len(self.skill_versions['skills']),
            'recent_tasks': self.task_history['tasks'][-5:],
            'next_likely_emergence': self._predict_next_emergence()
        }
        
        return status
    
    def _predict_next_emergence(self):
        """预测下次可能的涌现"""
        predictions = []
        
        # 检查接近阈值的任务类型
        task_types = {}
        for task in self.task_history['tasks']:
            task_type = task['type']
            if task_type not in task_types:
                task_types[task_type] = 0
            task_types[task_type] += 1
        
        for task_type, count in task_types.items():
            threshold = CONFIG['emergence_threshold']['spontaneous_order']
            if count >= threshold - 1:  # 接近阈值
                predictions.append({
                    'type': 'spontaneous_order',
                    'task_type': task_type,
                    'current': count,
                    'threshold': threshold,
                    'needed': threshold - count
                })
        
        return predictions

def main():
    """主函数"""
    trigger = EmergenceTriggerV2()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'record' and len(sys.argv) >= 4:
            task_type = sys.argv[2]
            description = sys.argv[3]
            bot_involved = sys.argv[4].split(',') if len(sys.argv) > 4 else None
            
            triggers = trigger.record_task(task_type, description, bot_involved)
            print(f"✅ 任务已记录，触发检查：{triggers}")
        
        elif command == 'version' and len(sys.argv) >= 4:
            skill_name = sys.argv[2]
            version = sys.argv[3]
            
            should_emerge = trigger.record_skill_version(skill_name, version)
            print(f"✅ 版本已记录，递归进化检查：{should_emerge}")
        
        elif command == 'status':
            status = trigger.check_status()
            print(f"\n📊 能力涌现状态")
            print(f"任务总数：{status['task_count']}")
            print(f"跨域任务：{status['cross_domain_count']}")
            print(f"技能数量：{status['skill_count']}")
            print(f"\n预测下次涌现:")
            for pred in status['next_likely_emergence']:
                print(f"  - {pred['task_type']}: 还需{pred['needed']}次")
        
        elif command == 'test':
            print("🧪 测试触发条件...")
            triggers = trigger._check_all_triggers('test')
            print(f"触发结果：{triggers}")
    
    else:
        print("🦞 能力涌现触发器 v2.0")
        print("用法:")
        print("  python3 emergence-trigger.py record <type> <description> [bots]")
        print("  python3 emergence-trigger.py version <skill> <version>")
        print("  python3 emergence-trigger.py status")
        print("  python3 emergence-trigger.py test")

if __name__ == '__main__':
    main()
