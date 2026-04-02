#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几首笔下注脚本 - TASK-050
截止：2026-03-31 12:00
"""

import os
import sys

# 清除 socks 代理 (httpx 不支持) - 必须在导入 py_clob_client 之前
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
from py_clob_client.clob_types import OrderArgs, OrderType, BalanceAllowanceParams, AssetType, ApiCreds

# 恢复代理 (后续可能需要)
for var, val in saved_proxies.items():
    os.environ[var] = val

# 加载配置
config_path = Path("~/.taiyi/zhiji/polymarket.json").expanduser()
with open(config_path) as f:
    config = json.load(f)

API_KEY = config['polymarket']['api_key']
API_SECRET = config['polymarket']['api_secret']
API_PASSPHRASE = config['polymarket']['api_passphrase']
WALLET_ADDRESS = config['polymarket']['wallet_address']
PRIVATE_KEY = config['polymarket'].get('private_key', '')
CHAIN_ID = config['polymarket'].get('chain_id', 137)
CLOB_URL = config['polymarket'].get('clob_url', 'https://clob.polymarket.com')

print("=" * 60)
print("  知几首笔下注 - TASK-050")
print("=" * 60)
print(f"时间：{datetime.now().isoformat()}")
print(f"钱包：{WALLET_ADDRESS}")
print(f"Chain ID: {CHAIN_ID}")
print()

# 初始化客户端
try:
    # 创建 API 凭证对象
    creds = ApiCreds(
        api_key=API_KEY,
        api_secret=API_SECRET,
        api_passphrase=API_PASSPHRASE,
    )
    
    # 初始化客户端（key=私钥）
    client = ClobClient(
        host=CLOB_URL,
        key=PRIVATE_KEY,  # 私钥用于签名
        chain_id=CHAIN_ID,
        creds=creds,  # API 凭证
    )
    
    print("✅ ClobClient 初始化成功")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"👛 钱包：{WALLET_ADDRESS}")
    
    # 获取余额 (USDC - ERC20, token_id 留空)
    balance = client.get_balance_allowance(
        params=BalanceAllowanceParams(
            asset_type=AssetType.COLLATERAL,  # USDC 是抵押品
            token_id="",  # ERC20 留空
        )
    )
    print(f"💰 USDC 余额：{balance}")
    
    # 获取热门市场
    print("\n📊 获取热门市场...")
    markets = client.get_sampling_simplified_markets()
    print(f"✅ 获取到 {len(markets)} 个市场")
    
    if markets:
        print("\n热门市场:")
        # markets 是 dict，需要正确解析
        market_list = list(markets.values()) if isinstance(markets, dict) else markets
        for m in market_list[:5]:
            if isinstance(m, dict):
                print(f"  - {m.get('question', 'N/A')[:50]}")
                print(f"    市场 ID: {m.get('token_id', 'N/A')[:20]}...")
                print(f"    流动性：${m.get('liquidity', 0):,.0f}")
    
    # 示例市场 ID (需要替换为实际市场)
    # 这里使用一个示例，实际应该通过 API 获取
    market_id = "0x5d14529cac90336a2f39a5c370391b940a0e97f2"  # 示例
    
    print(f"\n📝 准备下单...")
    print(f"  市场：{market_id[:20]}...")
    print(f"  方向：BUY YES")
    print(f"  数量：5 USDC (测试)")
    print(f"  价格：0.50")
    
    # 创建订单 (side 是字符串："BUY" 或 "SELL")
    order_args = OrderArgs(
        token_id=market_id,  # token_id 是条件代币的 ID
        price=0.50,
        size=5.0,
        side="BUY",
    )
    
    print("\n⚠️  注意：")
    print("  1. 这是测试脚本，实际下单需要真实市场 ID")
    print("  2. 确保钱包有足够 USDC 余额")
    print("  3. 当前余额不足时需先充值")
    
    # 实际下单 (取消注释以执行)
    # signed_order = client.create_order(order_args)
    # resp = client.post_order(signed_order)
    # print(f"✅ 订单已提交：{resp}")
    
    print("\n✅ 连接测试完成！准备执行首笔下注")
    
except Exception as e:
    import traceback
    print(f"❌ 错误：{e}")
    print(f"❌ 类型：{type(e).__name__}")
    print("\n完整堆栈:")
    traceback.print_exc()

print("\n" + "=" * 60)
