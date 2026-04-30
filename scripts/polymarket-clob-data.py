#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polymarket CLOB API - 获取当前活跃市场 v2
"""

import os
import json
from datetime import datetime

# 清除代理
for var in ['ALL_PROXY', 'all_proxy', 'HTTP_PROXY', 'http_proxy', 'HTTPS_PROXY', 'https_proxy']:
    if var in os.environ:
        del os.environ[var]

import requests

CLOB_API = "https://clob.polymarket.com"

print("=" * 60)
print("  Polymarket CLOB API - 活跃市场 v2")
print("=" * 60)
print()

# 1. 获取采样市场
print("📊 获取采样市场...")
try:
    resp = requests.get(f"{CLOB_API}/sampling-simplified-markets", timeout=10)
    print(f"状态码：{resp.status_code}")
    
    if resp.ok:
        data = resp.json()
        print(f"返回类型：{type(data)}")
        print(f"Keys: {list(data.keys())[:10]}")
        
        # 保存原始数据
        with open('/home/nicola/polymarket-data/clob_sampling.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        # 解析数据
        markets = []
        for key, value in data.items():
            if isinstance(value, list):
                markets.extend(value)
            elif isinstance(value, dict):
                markets.append(value)
        
        print(f"市场数量：{len(markets)}")
        
        if markets:
            print("\n热门市场:")
            for i, m in enumerate(markets[:10], 1):
                if isinstance(m, dict):
                    question = m.get('question', 'N/A')[:50]
                    liquidity = float(m.get('liquidity', 0) or 0)
                    volume = float(m.get('volume24h', 0) or 0)
                    token_id = m.get('token_id', 'N/A')
                    
                    print(f"{i}. {question}")
                    print(f"   流动性：${liquidity:,.0f} | 24h 成交：${volume:,.0f}")
                    print(f"   Token ID: {token_id}")
                    print()
        
        print("✅ 数据已保存：/home/nicola/polymarket-data/clob_sampling.json")
        
except Exception as e:
    import traceback
    print(f"❌ 错误：{e}")
    traceback.print_exc()

# 2. 获取所有市场
print("\n📊 获取所有市场...")
try:
    resp = requests.get(f"{CLOB_API}/markets", timeout=10)
    print(f"状态码：{resp.status_code}")
    
    if resp.ok:
        data = resp.json()
        print(f"返回类型：{type(data)}")
        
        # 保存
        with open('/home/nicola/polymarket-data/clob_all.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        if isinstance(data, list):
            print(f"市场数量：{len(data)}")
            
            # 按流动性排序
            markets_with_liq = []
            for m in data:
                if isinstance(m, dict):
                    liq = float(m.get('liquidity', 0) or 0)
                    vol = float(m.get('volume24h', 0) or 0)
                    if liq > 0 or vol > 10000:
                        markets_with_liq.append({
                            'token_id': m.get('token_id'),
                            'question': m.get('question', m.get('event', 'N/A')),
                            'liquidity': liq,
                            'volume24h': vol,
                        })
            
            markets_with_liq.sort(key=lambda x: x['liquidity'], reverse=True)
            
            print(f"\n活跃市场：{len(markets_with_liq)}")
            print("\n前 10 个:")
            for i, m in enumerate(markets_with_liq[:10], 1):
                print(f"{i}. {m['question'][:50]}")
                print(f"   流动性：${m['liquidity']:,.0f} | 24h: ${m['volume24h']:,.0f}")
                print(f"   Token ID: {m['token_id']}")
                print()
                
        print("✅ 数据已保存：/home/nicola/polymarket-data/clob_all.json")
                
except Exception as e:
    print(f"❌ 错误：{e}")

print("=" * 60)
