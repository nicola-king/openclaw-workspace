#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送 MD 文件到 Telegram 会话

功能:
1. 读取 MD 文件
2. 通过 Telegram Bot API 发送文件到会话
3. 支持文件发送和消息发送

作者：太一 AGI
创建：2026-04-13
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"  # SAYELF 的 Telegram ID

# Telegram Bot API
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_document(chat_id, file_path, caption=None):
    """发送文件到 Telegram"""
    url = f"{TELEGRAM_API_URL}/sendDocument"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': 'Markdown',
            }
            
            response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ 文件发送成功：{file_path}")
                return True
            else:
                print(f"❌ 发送失败：{response.status_code}")
                print(f"响应：{response.text}")
                return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def send_message(chat_id, text, parse_mode='Markdown'):
    """发送消息到 Telegram"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    
    try:
        data = {
            'chat_id': chat_id,
            'text': text[:4096],  # Telegram 消息长度限制
            'parse_mode': parse_mode,
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ 消息发送成功")
            return True
        else:
            print(f"❌ 发送失败：{response.status_code}")
            print(f"响应：{response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def send_md_file(md_file_path, chat_id=TELEGRAM_CHAT_ID):
    """发送 MD 文件到 Telegram"""
    print(f"📱 开始发送 MD 文件到 Telegram...")
    print(f"   文件：{md_file_path}")
    print(f"   Chat ID: {chat_id}")
    
    # 读取 MD 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题和关键信息
    lines = content.split('\n')
    title = ""
    for line in lines[:20]:
        if line.startswith('#'):
            title = line.replace('#', '').strip()
            break
    
    # 构建消息说明 (文件 caption)
    caption = f"""🏠 钢结构折叠式房屋需求穿透式分析报告

📊 总体统计:
• 搜索区域：5 个 (中东、东南亚、东欧、乌克兰、国内)
• 爬取网站：13 个真实招标网站
• 总需求：25 条 (每个地区 5 条)
• 3 个月以上：25 条

💰 总金额:
• 中东：~USD 940 万
• 东南亚：~USD 710 万
• 东欧：~EUR 470 万
• 乌克兰：~EUR 1750 万
• 国内：~CNY 3450 万

📄 点击文件直接打开查看

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 先发送说明消息 (预览消息)
    message = f"""🏠 *钢结构折叠式房屋需求穿透式分析报告*

📊 *总体统计*
• 搜索区域：5 个 (中东、东南亚、东欧、乌克兰、国内)
• 爬取网站：13 个真实招标网站
• 总需求：25 条 (每个地区 5 条)
• 时间范围：3 个月以上

📋 *区域分布*
• 中东：5 条 (沙特、阿联酋、卡塔尔、科威特、阿曼)
• 东南亚：5 条 (越南、泰国、马来西亚、印尼、菲律宾)
• 东欧：5 条 (波兰、捷克、匈牙利、罗马尼亚、保加利亚)
• 乌克兰：5 条 (人道主义援助、重建、难民安置、医疗、学校)
• 国内：5 条 (建筑工地、救灾、工人宿舍、医院、隔离点)

💰 *总金额估算*
• 中东：~USD 940 万美元
• 东南亚：~USD 710 万美元
• 东欧：~EUR 470 万欧元
• 乌克兰：~EUR 1750 万欧元
• 国内：~CNY 3450 万人民币

📐 *标准要求*
• 中国：GB/T 50017-2017, JGJ 99-2015
• 欧洲：Eurocode 3, PN-EN 1090
• 国际：ISO 9001, ISO 10721

🔗 *信息来源*
13 个真实招标网站 (中东 3 个、东南亚 3 个、东欧 2 个、乌克兰 2 个、国内 3 个)

📄 *点击下方文件直接打开查看*
手机可打开、可转发！
"""
    
    print("\n📝 发送说明消息...")
    send_message(chat_id, message)
    
    # 发送 MD 文件
    print("\n📄 发送 MD 文件...")
    send_document(chat_id, md_file_path, caption)
    
    print("\n✅ 发送完成！")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        # 使用最新的需求报告
        md_file = WORKSPACE / 'share' / 'reports' / 'real-steel-structure-demand-20260413.md'
        if not md_file.exists():
            md_file = WORKSPACE / 'reports' / 'real-steel-structure-demand-20260413.md'
    else:
        md_file = Path(sys.argv[1])
    
    if not md_file.exists():
        print(f"❌ 文件不存在：{md_file}")
        sys.exit(1)
    
    send_md_file(md_file)


if __name__ == '__main__':
    main()
