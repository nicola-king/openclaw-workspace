#!/usr/bin/env python3
"""
主会话汇报触发器
由 main session cron 调用，使用 message tool 发送汇报
"""

import subprocess
import sys
from datetime import datetime

LOG_FILE = "/tmp/main-session-report.log"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def send_progress_report():
    """发送项目进度汇报"""
    log("🚀 项目进度汇报触发")
    
    cmd = [
        "python3",
        "/home/nicola/.openclaw/workspace/scripts/auto-report-v2.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            log("✅ 项目进度汇报发送成功")
            return True
        else:
            log(f"❌ 项目进度汇报失败：{result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"❌ 异常：{e}")
        return False

def send_completion_report():
    """发送任务完成率汇报"""
    log("🚀 任务完成率汇报触发")
    
    cmd = [
        "python3",
        "/home/nicola/.openclaw/workspace/scripts/task-completion-report.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            log("✅ 任务完成率汇报发送成功")
            return True
        else:
            log(f"❌ 任务完成率汇报失败：{result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"❌ 异常：{e}")
        return False

if __name__ == "__main__":
    # 根据调用参数决定发送哪种汇报
    if len(sys.argv) > 1 and sys.argv[1] == "completion":
        success = send_completion_report()
    else:
        success = send_progress_report()
    
    sys.exit(0 if success else 1)
