#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polymarket 实时数据采集 v4 - Events API
获取当前活跃市场
"""

import os
import json
from datetime import datetime

# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

import requests

GAMMA_API = "https://gamma-api.polymarket.com"

print("=" * 60)
print("  Polymarket 实时数据采集 v4")
print("=" * 60)
print(f"时间：{datetime.now().isoformat()}")
print()

output_dir = '/home/nicola/polymarket-data'
os.makedirs(output_dir, exist_ok=True)

# 1. 获取体育赛事市场
print("🏀 获取体育赛事市场...")
try:
    resp = requests.get(f"{GAMMA_API}/events?category=sports", timeout=15)
    
    if resp.ok:
        events = resp.json()
        print(f"✅ 赛事数量：{len(events)}")
        
        # 保存原始数据
        with open(f"{output_dir}/sports_events.json", 'w') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        
        # 解析市场
        markets = []
        for event in events:
            event_title = event.get('title', 'N/A')
            event_id = event.get('id', 'N/A')
            markets_data = event.get('markets', [])
            
            for m in markets_data:
                question = m.get('question', event_title)
                volume = float(m.get('volume', 0) or 0)
                liquidity = float(m.get('liquidity', 0) or 0)
                market_id = m.get('id', 'N/A')
                
                markets.append({
                    'event': event_title,
                    'question': question,
                    'volume': volume,
                    'liquidity': liquidity,
                    'market_id': market_id,
                })
        
        # 按流动性排序
        markets.sort(key=lambda x: x['liquidity'], reverse=True)
        
        print(f"\n市场总数：{len(markets)}")
        print(f"\n前 10 个高流动性市场:")
        for i, m in enumerate(markets[:10], 1):
            print(f"{i}. {m['question'][:55]}")
            print(f"   事件：{m['event'][:40]}")
            print(f"   流动性：${m['liquidity']:,.0f} | 成交量：${m['volume']:,.0f}")
            print(f"   Market ID: {m['market_id']}")
            print()
        
        # 保存市场数据
        with open(f"{output_dir}/sports_markets.json", 'w') as f:
            json.dump(markets, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 数据已保存")
        
except Exception as e:
    import traceback
    print(f"❌ 错误：{e}")
    traceback.print_exc()

# 2. 获取天气市场
print("\n🌤️  获取天气市场...")
try:
    resp = requests.get(f"{GAMMA_API}/events?category=weather", timeout=15)
    
    if resp.ok:
        events = resp.json()
        print(f"✅ 天气事件：{len(events)}")
        
        with open(f"{output_dir}/weather_events.json", 'w') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        
        # 解析市场
        weather_markets = []
        for event in events:
            event_title = event.get('title', 'N/A')
            markets_data = event.get('markets', [])
            
            for m in markets_data:
                question = m.get('question', event_title)
                volume = float(m.get('volume', 0) or 0)
                liquidity = float(m.get('liquidity', 0) or 0)
                
                weather_markets.append({
                    'event': event_title,
                    'question': question,
                    'volume': volume,
                    'liquidity': liquidity,
                })
        
        weather_markets.sort(key=lambda x: x['liquidity'], reverse=True)
        
        print(f"\n天气市场：{len(weather_markets)} 个")
        print("\n前 5 个:")
        for i, m in enumerate(weather_markets[:5], 1):
            print(f"{i}. {m['question'][:55]}")
            print(f"   流动性：${m['liquidity']:,.0f}")
            print()
        
        with open(f"{output_dir}/weather_markets.json", 'w') as f:
            json.dump(weather_markets, f, indent=2, ensure_ascii=False)
        
except Exception as e:
    print(f"❌ 错误：{e}")

# 3. 获取政治市场 (高流动性)
print("\n🏛️  获取政治市场...")
try:
    resp = requests.get(f"{GAMMA_API}/events?category=policy", timeout=15)
    
    if resp.ok:
        events = resp.json()
        print(f"✅ 政策事件：{len(events)}")
        
        policy_markets = []
        for event in events:
            event_title = event.get('title', 'N/A')
            markets_data = event.get('markets', [])
            
            for m in markets_data:
                question = m.get('question', event_title)
                volume = float(m.get('volume', 0) or 0)
                liquidity = float(m.get('liquidity', 0) or 0)
                
                policy_markets.append({
                    'event': event_title,
                    'question': question,
                    'volume': volume,
                    'liquidity': liquidity,
                })
        
        policy_markets.sort(key=lambda x: x['liquidity'], reverse=True)
        
        print(f"\n政策市场：{len(policy_markets)} 个")
        print("\n前 5 个:")
        for i, m in enumerate(policy_markets[:5], 1):
            print(f"{i}. {m['question'][:55]}")
            print(f"   流动性：${m['liquidity']:,.0f}")
            print()
        
        with open(f"{output_dir}/policy_markets.json", 'w') as f:
            json.dump(policy_markets, f, indent=2, ensure_ascii=False)
        
except Exception as e:
    print(f"❌ 错误：{e}")

print("\n" + "=" * 60)
print("✅ 数据采集完成")
print(f"📁 保存位置：{output_dir}/")
print("=" * 60)
