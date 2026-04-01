#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几首笔下注脚本 - TASK-050 v2
使用最新 API Key 配置
"""

import os
import sys

# 清除 socks 代理 (httpx 不支持)
PROXY_VARS = ['ALL_PROXY', 'all_proxy', 'HTTP_PROXY', 'http_proxy', 'HTTPS_PROXY', 'https_proxy']
saved_proxies = {}
for var in PROXY_VARS:
    if var in os.environ:
        saved_proxies[var] = os.environ[var]
        del os.environ[var]

import json
from datetime import datetime
from pathlib import Path
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds

# 恢复代理
for var, val in saved_proxies.items():
    os.environ[var] = val

# 加载配置
config_path = Path("~/.taiyi/zhiji/polymarket.json").expanduser()
with open(config_path) as f:
    config = json.load(f)

API_KEY = config['polymarket']['api_key']
WALLET_ADDRESS = config['polymarket']['wallet_address']
CHAIN_ID = config['polymarket'].get('chain_id', 137)

print("=" * 60)
print("  知几首笔下注 - TASK-050 v2")
print("=" * 60)
print(f"时间：{datetime.now().isoformat()}")
print(f"钱包：{WALLET_ADDRESS}")
print(f"API Key: {API_KEY}")
print(f"Chain ID: {CHAIN_ID}")
print()

# 清除代理并初始化
for var in PROXY_VARS:
    if var in os.environ:
        del os.environ[var]

try:
    # 使用 API Key 初始化 (只读模式)
    client = ClobClient(
        host="https://clob.polymarket.com",
        key=API_KEY,  # 使用 API Key 而非私钥
        chain_id=CHAIN_ID,
    )
    
    print("✅ ClobClient 初始化成功 (只读模式)")
    
    # 测试连接
    ok = client.get_ok()
    print(f"✅ 连接状态：{ok}")
    
    # 获取服务器时间
    server_time = client.get_server_time()
    print(f"🕐 服务器时间：{server_time}")
    
    # 获取市场
    print("\n📊 获取市场信息...")
    markets = client.get_sampling_simplified_markets()
    print(f"✅ 获取到 {len(markets)} 个市场")
    
    if markets:
        print("\n热门市场:")
        market_list = list(markets.values()) if isinstance(markets, dict) else markets
        for m in market_list[:5]:
            if isinstance(m, dict):
                question = m.get('question', 'N/A')
                token_id = m.get('token_id', 'N/A')
                liquidity = m.get('liquidity', 0)
                print(f"  - {question[:50]}")
                print(f"    ID: {token_id[:20] if token_id != 'N/A' else 'N/A'}...")
                print(f"    流动性：${liquidity:,.0f}")
    
    print("\n" + "=" * 60)
    print("✅ 连接测试成功！")
    print("\n⚠️  注意：")
    print("  1. 当前是只读模式 (无 私钥)")
    print("  2. 下单需要私钥签名")
    print("  3. 钱包需要充值 USDC (Polygon)")
    print("=" * 60)
    
except Exception as e:
    import traceback
    print(f"❌ 错误：{e}")
    print(f"❌ 类型：{type(e).__name__}")
    print("\n完整堆栈:")
    traceback.print_exc()
