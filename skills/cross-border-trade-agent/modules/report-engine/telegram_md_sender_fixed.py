#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram MD 文件发送 - 修复打开和大小显示问题 + 防重复发送
太一 AGI · 2026-04-19 11:26
"""

import requests
import os
import json
from pathlib import Path

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = '7073481596'

# 防重复发送记录
SENT_RECORDS = {}
SENT_RECORDS_FILE = Path('/home/sayelf/.openclaw/workspace/.telegram_sent_records.json')

# 加载已发送记录
if SENT_RECORDS_FILE.exists():
    try:
        with open(SENT_RECORDS_FILE, 'r') as f:
            SENT_RECORDS = json.load(f)
    except:
        SENT_RECORDS = {}


def save_sent_records():
    """保存已发送记录"""
    with open(SENT_RECORDS_FILE, 'w') as f:
        json.dump(SENT_RECORDS, f, ensure_ascii=False, indent=2)


def is_duplicate(file_path: str, interval_minutes: int = 30) -> bool:
    """
    检查是否为重复发送
    
    Args:
        file_path: 文件路径
        interval_minutes: 最小发送间隔（分钟）
    
    Returns:
        True 如果重复，False 如果可以发送
    """
    import time
    
    file_key = Path(file_path).name
    current_time = time.time()
    
    if file_key in SENT_RECORDS:
        last_sent = SENT_RECORDS[file_key]
        if current_time - last_sent < interval_minutes * 60:
            return True
    
    # 记录发送时间
    SENT_RECORDS[file_key] = current_time
    save_sent_records()
    
    return False


def send_md_file(file_path: str, caption: str = "", is_breaking: bool = False, check_duplicate: bool = True, custom_filename: str = None) -> dict:
    """
    发送 MD 文件到 Telegram - 确保可打开且显示大小
    
    Args:
        file_path: MD 文件路径
        caption: 文件说明
        is_breaking: 是否为突发新闻（影响推送优先级）
        check_duplicate: 是否检查重复发送（默认检查）
        custom_filename: 自定义文件名（用于 Telegram 显示，默认使用文件原名）
    
    Returns:
        Telegram API 响应
    """
    
    # 检查重复发送
    if check_duplicate and is_duplicate(file_path):
        print(f"⚠️ 检测到重复发送，已跳过：{file_path}")
        return {"ok": False, "error": "duplicate", "message": "文件已在 30 分钟内发送过"}
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    
    # 检查文件
    file = Path(file_path)
    if not file.exists():
        return {"ok": False, "error": f"文件不存在：{file_path}"}
    
    # 获取文件大小
    file_size = file.stat().st_size
    
    # 格式化大小
    if file_size < 1024:
        size_str = f"{file_size} B"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size/1024:.1f} KB"
    else:
        size_str = f"{file_size/(1024*1024):.1f} MB"
    
    # 添加到 caption
    full_caption = f"{caption}\n\n📄 {file.name}\n💾 {size_str}"
    
    # Telegram Bot API 会将中文文件名转为数字
    # 解决方案：同时提供 file_name 参数
    send_filename = custom_filename if custom_filename else file.name
    
    # 替换不兼容的特殊字符
    send_filename = send_filename.replace('·', '-').replace(':', '-').replace('/', '-')
    
    # 发送文件（添加 file_name 参数保留中文名）
    with open(file, 'rb') as f:
        files = {
            'document': (send_filename, f, 'text/markdown')
        }
        data = {
            'chat_id': CHAT_ID,
            'caption': full_caption,
            'parse_mode': 'Markdown',
            'file_name': send_filename  # 关键：保留中文文件名
        }
        
        response = requests.post(url, files=files, data=data)
    
    return response.json()


def main():
    """主函数 - 发送新闻简报"""
    import datetime
    
    # 新闻简报文件（中文名称）
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    news_file = f"/home/sayelf/.openclaw/workspace/news/daily/晨间新闻简报-{today}.md"
    
    print(f"📤 发送新闻简报：{news_file}")
    
    # 发送（使用中文文件名，兼容格式）
    custom_filename = f"晨间新闻简报-{today}.md"
    result = send_md_file(news_file, "🌅 晨间新闻简报", check_duplicate=True, custom_filename=custom_filename)
    
    if result.get("ok"):
        print("✅ 发送成功！")
        print(f"📄 显示文件名：{result['result']['document']['file_name']}")
        print(f"💾 文件大小：{result['result']['document']['file_size']} B")
    else:
        print(f"❌ 发送失败：{result}")
    
    return result


if __name__ == "__main__":
    main()
