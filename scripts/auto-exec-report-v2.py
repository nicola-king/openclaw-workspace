#!/usr/bin/env python3
"""
太一 AGI 自动执行进度汇报脚本 v2
每 5 分钟自动发送进度到微信通道
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
    blocked_str = '\n'.join([f"⚠️ {t.get('id', 'TASK-XXX')}: {t.get('reason', '未知')}" for t in blocked]) or "无"
    
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

def send_report(report):
    """发送汇报到微信"""
    import subprocess
    import json
    
    # 使用 openclaw message 发送
    user_id = "o9cq80-xCy8pt54Dz3jqOJHAgVZ8@im.wechat"
    account_id = "0b1d2bb639e7-im-bot"
    
    cmd = [
        "openclaw", "message", "send",
        "--channel", "openclaw-weixin",
        "--target", user_id,
        "--account", account_id,
        "--message", report
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ 汇报发送成功")
        else:
            print(f"❌ 发送失败：{result.stderr}")
    except Exception as e:
        print(f"❌ 异常：{e}")

if __name__ == "__main__":
    report = generate_report()
    print(report)
    print("\n---\n发送汇报...")
    send_report(report)
