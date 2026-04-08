#!/usr/bin/env python3
"""
10 分钟自主进度汇报触发器
由 main session cron 调用，执行汇报脚本并发送 Telegram
"""

import subprocess
import sys
from datetime import datetime

LOG_FILE = "/tmp/10m-progress-report.log"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def main():
    log("🚀 10 分钟自主进度汇报触发")
    
    # 执行汇报脚本
    cmd = [
        "python3",
        "/home/nicola/.openclaw/workspace/scripts/auto-report-v2.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            log("✅ 10 分钟进度汇报发送成功")
            print("✅ 10 分钟进度汇报已发送")
            return True
        else:
            log(f"❌ 汇报失败：{result.stderr[:200]}")
            print(f"❌ 汇报失败：{result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"❌ 异常：{e}")
        print(f"❌ 异常：{e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
