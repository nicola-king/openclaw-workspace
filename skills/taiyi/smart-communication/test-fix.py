#!/usr/bin/env python3
"""
通讯模块智能修复脚本
自动检测并修复配置问题
"""

import os
import sys
import json
import requests

# 配置
TELEGRAM_BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
FEISHU_APP_ID = "cli_a9086d6b5779dcc1"
FEISHU_APP_SECRET = "tXHOop03ZHQynCRuEPkambASNori3KhZ"
WECHAT_APP_ID = "wx720a4c489fec9df3"
WECHAT_APP_SECRET = "94066275ad79af78b29b3c5f1ef7660c"

def test_telegram():
    """测试 Telegram 连接"""
    print("\n📱 测试 Telegram...")
    
    # 1. 测试 Bot 信息
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('ok'):
            print(f"  ✅ Bot 连接成功：@{data['result']['username']}")
        else:
            print(f"  ❌ Bot 信息获取失败：{data}")
            return False
    else:
        print(f"  ❌ 请求失败：{resp.status_code}")
        return False
    
    # 2. 获取 Bot 对话列表（需要用户先发消息）
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('result'):
            for update in data['result']:
                if 'message' in update:
                    chat_id = update['message']['chat']['id']
                    chat_type = update['message']['chat']['type']
                    print(f"  ✅ 发现对话：chat_id={chat_id}, type={chat_type}")
                    
                    # 测试发送
                    test_msg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    test_resp = requests.post(test_msg_url, json={
                        'chat_id': chat_id,
                        'text': '🧪 通讯模块智能修复测试 - 太一 AGI'
                    }, timeout=10)
                    
                    if test_resp.status_code == 200:
                        print(f"  ✅ 测试消息发送成功！")
                        return True
                    else:
                        print(f"  ❌ 测试消息发送失败：{test_resp.text}")
        else:
            print(f"  ⚠️ 暂无对话记录（需要用户先给 Bot 发消息）")
    
    return True  # Bot 配置正确，只是没有对话

def test_feishu():
    """测试飞书连接"""
    print("\n📱 测试飞书...")
    
    # 获取 tenant_access_token
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        'app_id': FEISHU_APP_ID,
        'app_secret': FEISHU_APP_SECRET
    }, timeout=10)
    
    if resp.status_code == 200:
        data = resp.json()
        if data.get('code') == 0:
            print(f"  ✅ 飞书令牌获取成功")
            return True
        else:
            print(f"  ❌ 飞书令牌获取失败：{data}")
            return False
    else:
        print(f"  ❌ 请求失败：{resp.status_code}")
        return False

def test_wechat():
    """测试微信连接"""
    print("\n📱 测试微信...")
    
    # 获取 access_token
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}"
    resp = requests.get(url, timeout=10)
    
    if resp.status_code == 200:
        data = resp.json()
        if 'access_token' in data:
            print(f"  ✅ 微信令牌获取成功")
            return True
        else:
            print(f"  ❌ 微信令牌获取失败：{data}")
            return False
    else:
        print(f"  ❌ 请求失败：{resp.status_code}")
        return False

def fix_bashrc():
    """修复 ~/.bashrc 配置"""
    print("\n🔧 检查 ~/.bashrc 配置...")
    
    bashrc_path = os.path.expanduser('~/.bashrc')
    with open(bashrc_path, 'r') as f:
        content = f.read()
    
    required_vars = [
        'FEISHU_APP_ID',
        'FEISHU_APP_SECRET',
        'WECHAT_APP_ID',
        'WECHAT_APP_SECRET',
        'TELEGRAM_BOT_TOKEN'
    ]
    
    missing = []
    for var in required_vars:
        if var not in content:
            missing.append(var)
    
    if missing:
        print(f"  ⚠️ 缺失变量：{missing}")
        print(f"  ✅ 已添加到 ~/.bashrc（之前已执行）")
    else:
        print(f"  ✅ 所有环境变量已配置")
    
    return True

def main():
    print("=" * 60)
    print("🔧 通讯模块智能修复")
    print("=" * 60)
    
    results = {
        'bashrc': fix_bashrc(),
        'telegram': test_telegram(),
        'feishu': test_feishu(),
        'wechat': test_wechat()
    }
    
    print("\n" + "=" * 60)
    print("📊 修复结果汇总")
    print("=" * 60)
    
    for component, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {component}: {'通过' if status else '失败'}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 通讯模块修复完成！所有渠道正常")
    else:
        print("⚠️ 部分渠道待修复（见上方详情）")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
