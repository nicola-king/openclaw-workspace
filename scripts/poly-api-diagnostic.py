#!/usr/bin/env python3
"""
Polymarket API Key 状态诊断工具
检查当前配置状态并提供解决方案
"""

import json
import os
from pathlib import Path

CONFIG_FILE = "/home/nicola/.taiyi/zhiji/polymarket.json"

def check_config():
    print("=" * 70)
    print("Polymarket API Key 状态诊断")
    print("=" * 70)
    print()
    
    # 检查配置文件
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ 配置文件不存在：{CONFIG_FILE}")
        return
    
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    polymarket = config.get('polymarket', {})
    
    # 检查各项配置
    print("📋 当前配置状态:")
    print("-" * 70)
    
    checks = {
        'api_key': ('API Key', '✅ 已配置', '❌ 缺失'),
        'api_secret': ('API Secret', '✅ 已配置', '❌ 缺失'),
        'api_passphrase': ('API Passphrase', '✅ 已配置', '❌ 缺失'),
        'wallet_address': ('钱包地址', '✅ 已配置', '❌ 缺失'),
        'signer_private_key': ('私钥', '✅ 已配置', '❌ 缺失'),
    }
    
    missing = []
    for key, (name, has, missing_msg) in checks.items():
        value = polymarket.get(key)
        if value:
            if key in ['api_secret', 'api_passphrase', 'signer_private_key']:
                print(f"  {has}: {name} = {value[:20]}...")
            else:
                print(f"  {has}: {name} = {value}")
        else:
            print(f"  {missing_msg}: {name}")
            missing.append(key)
    
    print()
    print("-" * 70)
    
    # 分析状态
    if 'api_key' in polymarket and 'api_secret' in polymarket and 'api_passphrase' in polymarket:
        print("✅ 完整配置：API Key 三元组已完整配置")
        print("   可以直接进行交易!")
        return True
    
    elif 'signer_private_key' in polymarket:
        print("🟡 有私钥，可以生成 API Key 三元组")
        print("   运行：python3 scripts/poly-create-api-keys.py")
        return False
    
    else:
        print("🔴 配置不完整，无法交易")
        print()
        print("解决方案:")
        print("-" * 70)
        print()
        print("方案 A: 官网手动创建 API Key (推荐，无需私钥)")
        print("  1. 登录 https://polymarket.com")
        print("  2. 头像 → Profile → Builder Keys / API Keys")
        print("  3. 点击 '+ Create New'")
        print("  4. 复制三元组 (secret/passphrase 只显示一次):")
        print("     - api_key")
        print("     - api_secret")
        print("     - api_passphrase")
        print("  5. 配置到 ~/.taiyi/zhiji/polymarket.json")
        print()
        print("方案 B: 使用私钥生成 (需要私钥)")
        print("  1. 配置私钥到 polymarket.json")
        print("  2. 运行：python3 scripts/poly-create-api-keys.py")
        print()
        print("-" * 70)
        return False

if __name__ == "__main__":
    check_config()
