#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polymarket 数据获取完整流程
Gamma API → CLOB Token IDs → 订单簿查询
作者：太一 AGI
日期：2026-03-31
"""

import requests
import json
import os

# 清除代理
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]

from py_clob_client.client import ClobClient

print("=" * 70)
print("Polymarket 完整数据获取流程")
print("=" * 70)
print("")

# ==================== 步骤 1: Gamma API 获取市场列表 ====================
print("【步骤 1】Gamma API 获取活跃市场")
print("-" * 70)

response = requests.get(
    "https://gamma-api.polymarket.com/markets",
    params={"active": "true", "closed": "false", "limit": 5},
    timeout=30
)

markets = response.json()
print(f"✅ 获取到 {len(markets)} 个活跃市场")
print("")

# ==================== 步骤 2: 解析市场数据 ====================
print("【步骤 2】解析市场数据")
print("-" * 70)

market_data = []
for i, market in enumerate(markets, 1):
    # 解析 clobTokenIds (可能是 JSON 字符串或列表)
    clob_ids = market.get('clobTokenIds', '[]')
    if isinstance(clob_ids, str):
        try:
            clob_ids = json.loads(clob_ids)
        except:
            clob_ids = [clob_ids]
    
    data = {
        'index': i,
        'question': market.get('question', 'N/A'),
        'market_id': market.get('id', 'N/A'),
        'condition_id': market.get('conditionId', 'N/A'),
        'yes_token': clob_ids[0] if len(clob_ids) > 0 else 'N/A',
        'no_token': clob_ids[1] if len(clob_ids) > 1 else 'N/A',
        'liquidity': float(market.get('liquidity', 0)),
        'volume': float(market.get('volume', 0)),
        'outcomes': market.get('outcomes', []),
        'outcome_prices': market.get('outcomePrices', []),
    }
    market_data.append(data)
    
    print(f"{i}. {data['question'][:60]}")
    print(f"   市场 ID: {data['market_id']}")
    print(f"   Yes Token: {data['yes_token'][:30]}...")
    print(f"   No Token:  {data['no_token'][:30] if data['no_token'] != 'N/A' else 'N/A'}")
    print(f"   流动性：${data['liquidity']:,.2f}")
    print(f"   成交量：${data['volume']:,.2f}")
    print(f"   结果：{data['outcomes']}")
    print(f"   价格：{data['outcome_prices']}")
    print("")

# ==================== 步骤 3: CLOB API 获取订单簿 ====================
print("【步骤 3】CLOB API 获取订单簿")
print("-" * 70)

client = ClobClient("https://clob.polymarket.com")

# 测试第一个市场
test_market = market_data[0]
print(f"测试市场：{test_market['question']}")
print(f"使用 Token: {test_market['yes_token'][:30]}...")
print("")

try:
    book = client.get_order_book(test_market['yes_token'])
    print(f"✅ 订单簿获取成功")
    
    if hasattr(book, 'bids') and hasattr(book, 'asks'):
        bids = book.bids[:5] if book.bids else []
        asks = book.asks[:5] if book.asks else []
        
        print(f"\n买盘 (Bids):")
        for i, bid in enumerate(bids, 1):
            price = getattr(bid, 'price', bid.get('price', 'N/A') if hasattr(bid, 'get') else bid)
            size = getattr(bid, 'size', bid.get('size', 'N/A') if hasattr(bid, 'get') else bid)
            print(f"  {i}. 价格：{price} | 数量：{size}")
        
        print(f"\n卖盘 (Asks):")
        for i, ask in enumerate(asks, 1):
            price = getattr(ask, 'price', ask.get('price', 'N/A') if hasattr(ask, 'get') else ask)
            size = getattr(ask, 'size', ask.get('size', 'N/A') if hasattr(ask, 'get') else ask)
            print(f"  {i}. 价格：{price} | 数量：{size}")
        
        # 计算中间价
        if bids and asks:
            best_bid = getattr(bids[0], 'price', bids[0].get('price') if hasattr(bids[0], 'get') else bids[0])
            best_ask = getattr(asks[0], 'price', asks[0].get('price') if hasattr(asks[0], 'get') else asks[0])
            mid_price = (float(best_bid) + float(best_ask)) / 2
            print(f"\n中间价：{mid_price:.4f} ({mid_price*100:.2f}%)")
            print(f"Spread: {float(best_ask) - float(best_bid):.4f}")
    
except Exception as e:
    print(f"❌ 失败：{type(e).__name__}: {e}")

# ==================== 步骤 4: 获取中间价 ====================
print("\n" + "=" * 70)
print("【步骤 4】获取所有市场中间价")
print("=" * 70)

for data in market_data:
    try:
        midpoint = client.get_midpoint(data['yes_token'])
        if isinstance(midpoint, dict) and 'mid' in midpoint:
            mid = float(midpoint['mid'])
            print(f"{data['index']}. {data['question'][:50]}")
            print(f"   中间价：{mid:.4f} ({mid*100:.2f}%)")
        else:
            print(f"{data['index']}. {data['question'][:50]} - 中间价：{midpoint}")
    except Exception as e:
        print(f"{data['index']}. {data['question'][:50]} - 失败：{e}")

# ==================== 总结 ====================
print("\n" + "=" * 70)
print("✅ 完整流程完成")
print("=" * 70)
print("\n数据流:")
print("  Gamma API → 市场列表 + clobTokenIds")
print("  ↓")
print("  CLOB API → 订单簿 + 价格")
print("  ↓")
print("  知几-E → 交易决策")
print("\n关键知识点:")
print("  1. clobTokenIds[0] = Yes token")
print("  2. clobTokenIds[1] = No token")
print("  3. 使用 token_id 查询订单簿")
print("  4. 中间价 = (best_bid + best_ask) / 2")
print("=" * 70 + "\n")
