#!/usr/bin/env python3
"""事前确认监控 - 守藏吏 Skill - 每小时执行"""

from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/home/nicola/.openclaw/workspace/memory/confirmation-tracker.md")

def count_confirmations():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        with open(LOG_FILE, 'r') as f:
            content = f.read()
            return content.count(f"**日期**: {today}")
    except:
        return 0

def main():
    print("🔍 守藏吏事前确认监控...")
    count = count_confirmations()
    status = "⚠️ 超标" if count >= 3 else "✅ 正常"
    print(f"📊 今日事前确认：{count}次 {status}")

if __name__ == "__main__":
    main()
