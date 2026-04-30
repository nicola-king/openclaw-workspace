#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试币安 API 连接

作者：太一 AGI
创建：2026-04-22
"""

import hashlib
import hmac
import requests
import time
from pathlib import Path

# 加载配置
env_file = Path("/home/nicola/.openclaw/workspace/.taiyi/zhiji/.env.binance")
if not env_file.exists():
    print("❌ 配置文件不存在！")
    exit(1)

# 读取 API 密钥
api_key = None
api_secret = None

with open(env_file, 'r') as f:
    for line in f:
        if line.startswith("BINANCE_API_KEY="):
            api_key = line.split("=")[1].strip()
        elif line.startswith("BINANCE_API_SECRET="):
            api_secret = line.split("=")[1].strip()

if not api_key or not api_secret:
    print("❌ API 密钥配置错误！")
    exit(1)

print("=" * 60)
print("🧪 币安 API 连接测试")
print("=" * 60)

# 测试 1: 获取服务器时间
print("\n1️⃣ 测试：获取服务器时间...")
try:
    response = requests.get("https://api.binance.com/api/v3/time", timeout=10)
    if response.status_code == 200:
        server_time = response.json()['serverTime']
        print(f"   ✅ 服务器时间：{server_time}")
    else:
        print(f"   ❌ 失败：{response.status_code}")
except Exception as e:
    print(f"   ❌ 错误：{e}")

# 测试 2: 获取账户信息 (需要签名)
print("\n2️⃣ 测试：获取账户信息...")
try:
    timestamp = int(time.time() * 1000)
    params = f"timestamp={timestamp}"
    
    signature = hmac.new(
        api_secret.encode('utf-8'),
        params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    url = f"https://api.binance.com/api/v3/account?{params}&signature={signature}"
    headers = {"X-MBX-APIKEY": api_key}
    
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        account = response.json()
        print(f"   ✅ 账户 ID: {account['accountCommissionId']}")
        print(f"   ✅  Maker 手续费：{account['makerCommission']/100:.2f}%")
        print(f"   ✅  Taker 手续费：{account['takerCommission']/100:.2f}%")
        print(f"   ✅ 账户状态：{account['accountStatus']}")
        
        # 显示 USDT 余额
        print(f"\n   💰 USDT 余额:")
        for asset in account['balances']:
            if asset['asset'] == 'USDT':
                free = float(asset['free'])
                locked = float(asset['locked'])
                print(f"      可用：{free:.2f} USDT")
                print(f"      冻结：{locked:.2f} USDT")
                print(f"      总计：{free + locked:.2f} USDT")
                break
    elif response.status_code == 401:
        print(f"   ❌ API 密钥无效！请检查密钥是否正确")
        print(f"      错误：{response.json()['msg']}")
    elif response.status_code == 403:
        print(f"   ❌ IP 不在白名单！")
        print(f"      错误：{response.json()['msg']}")
        print(f"      请将以下 IP 添加到币安 API 白名单:")
        print(f"      103.151.172.30")
    else:
        print(f"   ❌ 失败：{response.status_code}")
        print(f"      错误：{response.json()}")
        
except Exception as e:
    print(f"   ❌ 错误：{e}")

# 测试 3: 获取 BTC/USDT 价格
print("\n3️⃣ 测试：获取 BTC/USDT 价格...")
try:
    response = requests.get(
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        timeout=10
    )
    if response.status_code == 200:
        price = float(response.json()['price'])
        print(f"   ✅ BTC/USDT: ${price:,.2f}")
    else:
        print(f"   ❌ 失败：{response.status_code}")
except Exception as e:
    print(f"   ❌ 错误：{e}")

print("\n" + "=" * 60)
print("✅ 测试完成！")
print("=" * 60)
