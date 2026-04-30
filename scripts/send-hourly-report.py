#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送小时汇总报告到 Telegram

功能:
1. 读取最新的小时汇总报告
2. 格式化消息
3. 通过 Telegram Bot 发送

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"

# Telegram Bot API
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def get_latest_hourly_summary():
    """获取最新的小时汇总报告"""
    reports = list(REPORTS_DIR.glob("hourly-summary-*.json"))
    
    if not reports:
        return None
    
    latest = max(reports)
    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f), latest


def send_message(text):
    """发送消息到 Telegram"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    
    try:
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'Markdown',
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Telegram 发送成功")
            return True
        else:
            print(f"❌ 发送失败：{response.status_code}")
            print(f"响应：{response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def main():
    """主函数"""
    print("📊 发送小时汇总报告到 Telegram...")
    
    # 获取最新报告
    report = get_latest_hourly_summary()
    
    if not report:
        print("⚠️ 未发现小时汇总报告")
        return 1
    
    report_data, report_file = report
    
    # 构建消息
    period_start = report_data.get('period_start', 'unknown')[:16]
    period_end = report_data.get('period_end', 'unknown')[:16]
    total_executions = report_data.get('total_executions', 0)
    total_skills = report_data.get('total_skills_created', 0)
    total_signals = report_data.get('total_signals', 0)
    
    message = f"""📊 太一自进化小时报告

⏰ 时间：{period_start} - {period_end}

📈 执行统计:
• 执行次数：{total_executions} 次
• 技能创建：{total_skills} 个
• 信号检测：{total_signals} 个

状态：✅ 正常

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 发送消息
    if send_message(message):
        print(f"✅ 报告已发送：{report_file.name}")
        return 0
    else:
        print("❌ 发送失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())
