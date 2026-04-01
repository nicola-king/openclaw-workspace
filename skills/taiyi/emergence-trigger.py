#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
能力涌现触发器
- 每周一定时触发 (能力涌现协议)
- 自发触发 (同类任务重复 3 次+)
"""

import os
import sys
import json
import logging
from datetime import datetime

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/emergence-trigger.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('EmergenceTrigger')

# 配置
CONFIG = {
    'task_history_file': '/home/nicola/.openclaw/workspace/data/task-history.json',
    'emergence_threshold': 3,  # 同类任务重复 3 次触发
    'weekly_schedule': 'Monday 09:00',  # 每周一 09:00
}

class EmergenceTrigger:
    """能力涌现触发器"""
    
    def __init__(self):
        self.task_history = self._load_task_history()
        
    def _load_task_history(self):
        """加载任务历史"""
        if os.path.exists(CONFIG['task_history_file']):
            with open(CONFIG['task_history_file'], 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'tasks': []}
    
    def _save_task_history(self):
        """保存任务历史"""
        os.makedirs(os.path.dirname(CONFIG['task_history_file']), exist_ok=True)
        with open(CONFIG['task_history_file'], 'w', encoding='utf-8') as f:
            json.dump(self.task_history, f, ensure_ascii=False, indent=2)
    
    def record_task(self, task_type, description):
        """记录任务"""
        self.task_history['tasks'].append({
            'type': task_type,
            'description': description,
            'timestamp': datetime.now().isoformat()
        })
        self._save_task_history()
        
        logger.info(f"✅ 记录任务：{task_type} - {description}")
        
        # 检查是否触发涌现
        return self._check_emergence_trigger(task_type)
    
    def _check_emergence_trigger(self, task_type):
        """检查是否触发能力涌现"""
        # 统计同类任务数量
        same_type_tasks = [
            t for t in self.task_history['tasks']
            if t['type'] == task_type
        ]
        
        if len(same_type_tasks) >= CONFIG['emergence_threshold']:
            logger.info(f"🚀 触发能力涌现：{task_type} 重复 {len(same_type_tasks)} 次")
            return True
        
        return False
    
    def trigger_emergence(self, trigger_type, reason):
        """触发能力涌现流程"""
        logger.info(f"🦞 能力涌现触发：{trigger_type} - {reason}")
        
        # 创建涌现报告
        report = {
            'trigger_type': trigger_type,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'week': datetime.now().strftime('%Y-W%V')
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

报告：/home/nicola/.openclaw/workspace/reports/emergence/

---
太一 · 能力涌现协议"""
        
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

def main():
    """主函数"""
    trigger = EmergenceTrigger()
    
    # 测试自发触发
    if len(sys.argv) > 2:
        task_type = sys.argv[1]
        description = sys.argv[2]
        
        should_emerge = trigger.record_task(task_type, description)
        
        if should_emerge:
            trigger.trigger_emergence(task_type, f"同类任务重复{CONFIG['emergence_threshold']}次+")
        else:
            logger.info("✅ 任务已记录，未达到涌现阈值")
    else:
        # 每周触发模式
        logger.info(f"🦞 每周能力涌现启动...")
        trigger.trigger_emergence('weekly', '每周一自动触发')

if __name__ == '__main__':
    main()
