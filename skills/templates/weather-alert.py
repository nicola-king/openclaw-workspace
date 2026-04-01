#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气提醒技能
功能：每日天气推送 (重庆)
时间：每日 07:30
"""

import requests
from datetime import datetime

# 配置
CITY = "Chongqing"
TELEGRAM_BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID = "7073481596"

def get_weather():
    """获取天气"""
    url = f"http://wttr.in/{CITY}?format=%C+%t+%h+%w"
    response = requests.get(url, timeout=5)
    return response.text.strip()

def send_weather_alert():
    """发送天气提醒"""
    weather = get_weather()
    
    message = f"""🌤️ 重庆天气提醒

{datetime.now().strftime('%Y-%m-%d %H:%M')}

{weather}

💡 建议：
- 根据天气准备衣物
- 雨天记得带伞

---
太一 · 自动提醒"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, json=data, timeout=10)
    
    print("✅ 天气提醒发送成功")

if __name__ == '__main__':
    send_weather_alert()
