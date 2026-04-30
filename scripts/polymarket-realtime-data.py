#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polymarket 实时数据采集 v3 - 使用代理
"""

import os
import json
from datetime import datetime

# 设置 HTTP 代理 (Clash)
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

import requests

GAMMA_API = "https://gamma-api.polymarket.com"

print("=" * 60)
print("  Polymarket 实时数据采集 v3 (代理)")
print("=" * 60)
print(f"时间：{datetime.now().isoformat()}")
print()

# 1. 获取热门市场
print("📊 获取热门市场...")
try:
    resp = requests.get(f"{GAMMA_API}/markets", timeout=15)
    print(f"状态码：{resp.status_code}")
    
    if resp.ok:
        markets = resp.json()
        print(f"市场数量：{len(markets)}")
        
        # 提取关键信息
        market_list = []
        for m in markets:
            vol = float(m.get('volume', 0) or 0)
            liq = float(m.get('liquidity', 0) or 0)
            active = m.get('active', False)
            
            market_list.append({
                'id': m.get('id'),
                'question': m.get('question', 'N/A'),
                'volume': vol,
                'liquidity': liq,
                'active': active,
            })
        
        # 按成交量排序
        market_list.sort(key=lambda x: x['volume'], reverse=True)
        
        print(f"\n前 10 个市场 (按成交量):")
        for i, m in enumerate(market_list[:10], 1):
            print(f"{i}. {m['question'][:50]}")
            print(f"   成交量：${m['volume']:,.0f} | 流动性：${m['liquidity']:,.0f}")
            print(f"   活跃：{m['active']} | ID: {m['id']}")
            print()
        
        # 保存
        output_dir = '/home/nicola/polymarket-data'
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"{output_dir}/markets_{timestamp}.json", 'w') as f:
            json.dump(market_list, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 数据已保存：{output_dir}/markets_{timestamp}.json")
        
except Exception as e:
    import traceback
    print(f"❌ 错误：{e}")
    traceback.print_exc()

# 2. 搜索天气市场
print("\n🌤️  搜索天气市场...")
try:
    resp = requests.get(f"{GAMMA_API}/search", params={'q': 'weather'}, timeout=15)
    print(f"状态码：{resp.status_code}")
    
    if resp.ok:
        weather = resp.json()
        print(f"天气市场：{len(weather)} 个")
        for w in weather[:5]:
            print(f"  - {w.get('question', 'N/A')[:50]}")
            
except Exception as e:
    print(f"❌ 错误：{e}")

# 3. 搜索体育市场
print("\n🏀 搜索体育市场...")
try:
    resp = requests.get(f"{GAMMA_API}/sports", timeout=15)
    print(f"状态码：{resp.status_code}")
    
    if resp.ok:
        sports = resp.json()
        print(f"体育类别：{len(sports)} 个")
        
        # 获取热门体育市场
        if sports:
            for sport in list(sports.keys())[:3]:
                print(f"  - {sport}: {sports[sport]} 个市场")
                
except Exception as e:
    print(f"❌ 错误：{e}")

print("\n" + "=" * 60)
print("✅ 数据采集完成")
print("=" * 60)
