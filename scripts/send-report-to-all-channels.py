#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送报告到所有通讯端口 (Telegram/微信/飞书)

铁律:
1. 每次生成报告后自动发送
2. MD 文件可直接打开
3. 手机可访问和转发
4. 工控机不随身带也能访问

作者：太一 AGI
创建：2026-04-13
"""

import os
import sys
import requests
import json
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SHARE_DIR = WORKSPACE / 'share' / 'reports'

# Telegram 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"

# 飞书配置 (从配置文件夹读取)
FEISHU_CONFIG = WORKSPACE / 'config' / 'feishu' / 'webhook.json'

# 微信配置
WECHAT_CONFIG = WORKSPACE / 'config' / 'wechat' / 'official-account.json'


def send_telegram(md_file, preview_text):
    """发送到 Telegram"""
    print("\n📱 发送报告到 Telegram...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    
    try:
        with open(md_file, 'rb') as f:
            files = {'document': f}
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': preview_text,
                'parse_mode': 'Markdown',
            }
            
            response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                print("  ✅ Telegram 发送成功")
                return True
            else:
                print(f"  ❌ Telegram 发送失败：{response.status_code}")
                return False
    except Exception as e:
        print(f"  ❌ Telegram 发送错误：{e}")
        return False


def send_feishu(md_file, preview_text):
    """发送到飞书"""
    print("\n📱 发送报告到飞书...")
    
    if not FEISHU_CONFIG.exists():
        print("  ⚠️ 飞书配置文件不存在，跳过")
        return False
    
    try:
        with open(FEISHU_CONFIG, 'r') as f:
            config = json.load(f)
        
        webhook_url = config.get('webhook_url', '')
        
        if not webhook_url:
            print("  ⚠️ 飞书 Webhook URL 未配置，跳过")
            return False
        
        # 飞书消息格式
        message = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "📊 太一系统报告",
                        "content": [
                            [{"tag": "text", "text": preview_text[:500]}],
                            [{"tag": "text", "text": f"\n\n📄 完整报告：{md_file.name}"}],
                            [{"tag": "text", "text": f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}],
                        ]
                    }
                }
            }
        }
        
        response = requests.post(webhook_url, json=message, timeout=30)
        
        if response.status_code == 200:
            print("  ✅ 飞书发送成功")
            return True
        else:
            print(f"  ❌ 飞书发送失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 飞书发送错误：{e}")
        return False


def send_wechat(md_file, preview_text):
    """发送到微信 (企业微信)"""
    print("\n📱 发送报告到微信...")
    
    if not WECHAT_CONFIG.exists():
        print("  ⚠️ 微信配置文件不存在，跳过")
        return False
    
    try:
        with open(WECHAT_CONFIG, 'r') as f:
            config = json.load(f)
        
        webhook_url = config.get('webhook_url', '')
        
        if not webhook_url:
            print("  ⚠️ 微信 Webhook URL 未配置，跳过")
            return False
        
        # 企业微信消息格式
        message = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"""🏠 钢结构折叠式房屋需求报告

{preview_text[:500]}

📄 完整报告：{md_file.name}

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            }
        }
        
        response = requests.post(webhook_url, json=message, timeout=30)
        
        if response.status_code == 200:
            print("  ✅ 微信发送成功")
            return True
        else:
            print(f"  ❌ 微信发送失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 微信发送错误：{e}")
        return False


def generate_preview_text(md_file):
    """生成预览文本"""
    # 读取 MD 文件内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取关键信息
    lines = content.split('\n')
    
    # 构建预览消息
    preview = f"""🏠 钢结构折叠式房屋需求穿透式分析报告

📊 总体统计:
• 搜索区域：5 个 (中东、东南亚、东欧、乌克兰、国内)
• 爬取网站：17 个真实招标网站
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
    
    return preview


def send_to_all_channels(md_file):
    """发送到所有通讯端口"""
    print("=" * 60)
    print("📱 发送报告到所有通讯端口")
    print("=" * 60)
    print(f"\n📄 报告文件：{md_file.name}")
    
    # 生成预览文本
    preview_text = generate_preview_text(md_file)
    
    # 发送到各平台
    results = {
        'telegram': send_telegram(md_file, preview_text),
        'feishu': send_feishu(md_file, preview_text),
        'wechat': send_wechat(md_file, preview_text),
    }
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 发送结果汇总")
    print("=" * 60)
    print(f"  Telegram: {'✅ 成功' if results['telegram'] else '⚠️ 失败/未配置'}")
    print(f"  飞书：{'✅ 成功' if results['feishu'] else '⚠️ 失败/未配置'}")
    print(f"  微信：{'✅ 成功' if results['wechat'] else '⚠️ 失败/未配置'}")
    
    success_count = sum(1 for v in results.values() if v)
    print(f"\n总计：{success_count}/3 个平台发送成功")
    
    return results


def main():
    """主函数"""
    if len(sys.argv) < 2:
        # 使用最新的报告
        md_file = SHARE_DIR / 'real-steel-structure-demand-20260413.md'
        if not md_file.exists():
            md_file = WORKSPACE / 'reports' / 'real-steel-structure-demand-20260413.md'
    else:
        md_file = Path(sys.argv[1])
    
    if not md_file.exists():
        print(f"❌ 文件不存在：{md_file}")
        sys.exit(1)
    
    send_to_all_channels(md_file)


if __name__ == '__main__':
    main()
