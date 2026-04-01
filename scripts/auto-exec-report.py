#!/usr/bin/env python3
"""
太一 AGI 自动执行进度汇报脚本
每 5 分钟自动发送进度到 Telegram 通道
"""

import json
import os
from datetime import datetime, timezone

STATUS_FILE = "/tmp/auto-exec-status.json"
TRACKER_FILE = "/tmp/task-tracker.json"

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}

def format_progress_bar(progress, length=10):
    filled = int(progress / 100 * length)
    return '█' * filled + '░' * (length - filled)

def generate_report():
    status = load_json(STATUS_FILE)
    tracker = load_json(TRACKER_FILE)
    
    # 进度条
    progress = status.get('progress', 0)
    bar = format_progress_bar(progress)
    
    # 当前任务
    task = status.get('currentTask', '无')
    task_status = status.get('status', 'unknown')
    next_step = status.get('nextStep', '-')
    eta = status.get('eta', '-')
    
    # 今日完成
    completed = tracker.get('completedToday', [])
    completed_str = '\n'.join([f"✅ {t}" for t in completed[-5:]]) or "暂无"
    
    # 阻塞任务
    blocked = tracker.get('blockedTasks', [])
    blocked_str = '\n'.join([f"⚠️ {t['id']}: {t['reason']}" for t in blocked]) or "无"
    
    report = f"""🔄 自动执行进度汇报 (每 5 分钟)

【当前任务】{task}
【进度】{bar} {progress}%
【状态】{task_status}
【下一步】{next_step}
【预计完成】{eta}

【今日完成】
{completed_str}

【阻塞任务】
{blocked_str}

---
自动执行保障机制：✅ 已激活
下次汇报：5 分钟后"""
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print(report)
