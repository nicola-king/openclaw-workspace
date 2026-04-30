#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安 API 连接测试 v2 - 详细诊断

作者：太一 AGI
创建：2026-04-22
"""

import hashlib
import hmac
import requests
import time

# API 密钥 (直接使用)
api_key = "oIsi9bQiX2BCqHw29QQzSfcLWttt4BYwNWaZOxrNZOjuZyDI3qfILt4XHfzmVRS3"
api_secret = "jKSPGVEAcsvVTe50K2X7rVkI6SnfI2sPB63xPjHPvoTy6Wv8PIJ6u6SFpk01PdeC"

print("=" * 60)
print("🔍 币安 API 密钥诊断")
print("=" * 60)

# 密钥诊断
print(f"\n📋 密钥信息:")
print(f"   API Key 长度：{len(api_key)} 字符")
print(f"   Secret 长度：{len(api_secret)} 字符")
print(f"   API Key 前 10 位：{api_key[:10]}")
print(f"   API Key 后 10 位：{api_key[-10:]}")
print(f"   是否有空格：{'是' if ' ' in api_key else '否'}")
print(f"   是否有换行：{'是' if chr(10) in api_key else '否'}")

# 测试 1: 公开接口
print("\n" + "=" * 60)
print("1️⃣ 测试：公开接口 (无需认证)")
print("=" * 60)

try:
    response = requests.get("https://api.binance.com/api/v3/ping", timeout=10)
    print(f"\n✅ Ping: {response.json()}")
except Exception as e:
    print(f"\n❌ Ping 失败：{e}")

# 测试 2: 带 API Key 的请求 (无需签名)
print("\n" + "=" * 60)
print("2️⃣ 测试：带 API Key 的请求 (无需签名)")
print("=" * 60)

try:
    timestamp = int(time.time() * 1000)
    url = "https://api.binance.com/api/v3/account"
    headers = {
        "X-MBX-APIKEY": api_key,
    }
    params = {
        "timestamp": timestamp,
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    
    print(f"\n📊 响应状态码：{response.status_code}")
    print(f"📊 响应内容：{response.text[:200]}")
    
    if response.status_code == 200:
        print("\n✅ API Key 有效！")
    elif response.status_code == 401:
        error = response.json()
        print(f"\n❌ API Key 无效！")
        print(f"   错误代码：{error.get('code')}")
        print(f"   错误信息：{error.get('msg')}")
        
        if "IP" in error.get('msg', ''):
            print(f"\n⚠️  可能是 IP 白名单问题！")
            print(f"   当前 IP: 103.151.172.30")
            print(f"   请在币安后台确认已添加此 IP")
    elif response.status_code == 403:
        error = response.json()
        print(f"\n❌ 权限不足！")
        print(f"   错误信息：{error.get('msg')}")
        
except Exception as e:
    print(f"\n❌ 请求失败：{e}")

# 测试 3: 带签名的请求
print("\n" + "=" * 60)
print("3️⃣ 测试：带签名的请求 (完整认证)")
print("=" * 60)

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
    
    print(f"\n📊 响应状态码：{response.status_code}")
    
    if response.status_code == 200:
        account = response.json()
        print(f"\n✅ 认证成功！")
        print(f"   账户状态：{account.get('accountStatus')}")
        
        # 显示 USDT 余额
        for asset in account.get('balances', []):
            if asset['asset'] == 'USDT':
                free = float(asset['free'])
                locked = float(asset['locked'])
                print(f"\n💰 USDT 余额:")
                print(f"   可用：{free:.2f} USDT")
                print(f"   冻结：{locked:.2f} USDT")
                print(f"   总计：{free + locked:.2f} USDT")
                
                if free >= 10:
                    print(f"\n✅ 余额充足！可以进行实盘测试")
                else:
                    print(f"\n⚠️  余额不足！需要至少$10 USDT")
                break
    else:
        error = response.json()
        print(f"\n❌ 认证失败！")
        print(f"   错误代码：{error.get('code')}")
        print(f"   错误信息：{error.get('msg')}")
        
except Exception as e:
    print(f"\n❌ 请求失败：{e}")

print("\n" + "=" * 60)
print("✅ 诊断完成！")
print("=" * 60)
