#!/usr/bin/env python3
"""退化检测 - 守藏吏 Skill - 每小时执行"""

from datetime import datetime
from pathlib import Path

def check_degradation():
    alerts = []
    
    # 检查 1: 等待指令
    passive_count = 0
    if passive_count >= 3:
        alerts.append(f"⚠️ 退化：连续{passive_count}任务等待指令")
    
    # 检查 2: 事前确认
    today = datetime.now().strftime('%Y-%m-%d')
    confirm_file = Path("/home/nicola/.openclaw/workspace/memory/confirmation-tracker.md")
    try:
        with open(confirm_file, 'r') as f:
            confirmations = f.read().count(f"**日期**: {today}")
            if confirmations >= 5:
                alerts.append(f"⚠️ 退化：今日事前确认{confirmations}次（≥5 次）")
    except:
        pass
    
    return alerts

def main():
    print("🔍 守藏吏退化检测...")
    alerts = check_degradation()
    
    if alerts:
        print("⚠️ 发现退化风险:")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print("✅ 无退化风险")

if __name__ == "__main__":
    main()
