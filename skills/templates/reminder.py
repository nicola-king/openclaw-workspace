#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时提醒技能
功能：自定义定时提醒
使用：python3 reminder.py "提醒内容" "2026-03-28 15:00"
"""

import sys
import requests
from datetime import datetime

# 配置
TELEGRAM_BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID = "7073481596"

def send_reminder(message, remind_time):
    """发送提醒"""
    formatted_message = f"""⏰ 定时提醒

{message}

⏱️ 提醒时间：{remind_time}

---
太一 · 自动提醒"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': formatted_message}
    requests.post(url, json=data, timeout=10)
    
    print("✅ 提醒发送成功")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 reminder.py \"提醒内容\" \"YYYY-MM-DD HH:MM\"")
        sys.exit(1)
    
    message = sys.argv[1]
    remind_time = sys.argv[2]
    send_reminder(message, remind_time)
