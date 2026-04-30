#!/usr/bin/env python3
"""
微信消息测试工具
向微信账号发送测试消息

用法:
    python3 test-message.py "测试消息内容"
"""

import json
import sys
from pathlib import Path
from datetime import datetime

WEIXIN_DIR = Path.home() / '.openclaw' / 'openclaw-weixin'
ACCOUNTS_FILE = WEIXIN_DIR / 'accounts.json'

def load_accounts() -> list:
    """加载账号列表"""
    if not ACCOUNTS_FILE.exists():
        return []
    
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)

def main():
    if len(sys.argv) < 2:
        print("用法：python3 test-message.py \"消息内容\"")
        print("\n说明:")
        print("  此工具用于测试微信通道是否正常工作")
        print("  消息会发送到 OpenClaw Gateway，由太一 AGI 处理")
        print("\n示例:")
        print('  python3 test-message.py "你好，测试消息"')
        return 1
    
    message = ' '.join(sys.argv[1:])
    accounts = load_accounts()
    
    if not accounts:
        print("❌ 未配置任何微信账号")
        return 1
    
    print(f"\n=== 微信消息测试 ===")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"消息：{message}")
    print(f"账号：{len(accounts)} 个已配置\n")
    
    print("ℹ️  测试说明:")
    print("  1. 在微信中发送消息到已绑定的账号")
    print("  2. 等待太一 AGI 自动回复")
    print("  3. 检查回复是否正常")
    print()
    
    print("📱 已配置账号:")
    for acc_id in accounts:
        acc_file = WEIXIN_DIR / 'accounts' / f'{acc_id}.json'
        if acc_file.exists():
            with open(acc_file, 'r') as f:
                data = json.load(f)
                user_id = data.get('userId', 'unknown')
                print(f"  - {acc_id}: {user_id[:30]}...")
    
    print()
    print("✅ 测试准备完成")
    print("   请在微信中发送消息进行测试")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
