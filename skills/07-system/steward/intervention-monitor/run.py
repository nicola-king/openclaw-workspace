#!/usr/bin/env python3
"""干预监控 - 守藏吏 Skill - 每小时执行"""

import subprocess
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/home/nicola/.openclaw/workspace/memory/human-intervention-log.md")

def check_threshold():
    """检查阈值并告警"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 统计今日干预次数
    try:
        with open(LOG_FILE, 'r') as f:
            content = f.read()
            today_count = content.count(f"**日期**: {today}")
    except:
        today_count = 0
    
    # 告警逻辑
    if today_count >= 3:
        alert = f"⚠️ 今日人工干预{today_count}次（≥3 次警戒线）"
        notify_taiyi(alert)
        print(alert)
    else:
        print(f"✅ 今日干预：{today_count}次（正常）")
    
    return today_count

def notify_taiyi(message):
    """上报太一"""
    cmd = [
        "openclaw", "message", "send",
        "--channel", "openclaw-weixin",
        "--target", "o9cq80yz80T13iCV5N_djDCSVo88@im.wechat",
        "--account", "387504e97169-im-bot",
        "--message", f"🚨 守藏吏告警：{message}"
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
        print("✅ 告警已发送")
    except Exception as e:
        print(f"⚠️ 发送失败：{e}")

def main():
    """主函数"""
    print("🔍 守藏吏干预监控检查...")
    check_threshold()
    print("✅ 检查完成")

if __name__ == "__main__":
    main()
