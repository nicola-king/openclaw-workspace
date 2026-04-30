#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polymarket 实时数据采集 - TASK-050 数据准备
用途：获取真实市场数据，为下注决策提供依据
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 清除代理
PROXY_VARS = ['ALL_PROXY', 'all_proxy', 'HTTP_PROXY', 'http_proxy', 'HTTPS_PROXY', 'https_proxy']
for var in PROXY_VARS:
    if var in os.environ:
        del os.environ[var]

import requests

# Gamma API (市场发现)
GAMMA_API = "https://gamma-api.polymarket.com"
# Data API (用户数据)
DATA_API = "https://data-api.polymarket.com"
# CLOB API (交易)
CLOB_API = "https://clob.polymarket.com"

print("=" * 60)
print("  Polymarket 实时数据采集")
print("=" * 60)
print(f"时间：{datetime.now().isoformat()}")
print()

# 1. 获取热门市场
print("📊 获取热门市场...")
try:
    resp = requests.get(f"{GAMMA_API}/markets", timeout=10)
    resp.raise_for_status()
    markets = resp.json()
    
    print(f"✅ 获取到 {len(markets)} 个市场")
    
    # 筛选高流动性市场
    high_liquidity = []
    for m in markets:
        liquidity = float(m.get('liquidity', 0) or 0)
        if liquidity > 100000:  # >$100K
            high_liquidity.append({
                'event': m.get('event', 'N/A'),
                'question': m.get('question', 'N/A')[:50],
                'liquidity': liquidity,
                'volume': float(m.get('volume', 0) or 0),
                'token_id': m.get('token_id', 'N/A'),
            })
    
    high_liquidity.sort(key=lambda x: x['liquidity'], reverse=True)
    
    print(f"\n💰 高流动性市场 (>$100K): {len(high_liquidity)} 个")
    print("\n前 10 个市场:")
    for i, m in enumerate(high_liquidity[:10], 1):
        print(f"  {i}. {m['question']}")
        print(f"     流动性：${m['liquidity']:,.0f} | 成交量：${m['volume']:,.0f}")
        print(f"     Token ID: {m['token_id'][:20] if m['token_id'] != 'N/A' else 'N/A'}...")
        print()
    
    # 保存到文件
    output_dir = Path("~/polymarket-data").expanduser()
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"markets_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'total_markets': len(markets),
            'high_liquidity_markets': high_liquidity,
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 数据已保存：{output_file}")
    
except Exception as e:
    print(f"❌ 错误：{e}")

# 2. 获取体育/天气相关市场
print("\n🌤️  获取天气/体育市场...")
try:
    # 天气市场
    weather_resp = requests.get(f"{GAMMA_API}/search", params={'q': 'weather'}, timeout=10)
    if weather_resp.ok:
        weather_markets = weather_resp.json()
        print(f"✅ 天气市场：{len(weather_markets)} 个")
    
    # 体育市场
    sports_resp = requests.get(f"{GAMMA_API}/sports", timeout=10)
    if sports_resp.ok:
        sports = sports_resp.json()
        print(f"✅ 体育类别：{len(sports)} 个")
        
except Exception as e:
    print(f"❌ 错误：{e}")

# 3. 获取当前用户信息 (需要 API Key)
print("\n👤 获取用户信息...")
config_path = Path("~/.taiyi/zhiji/polymarket.json").expanduser()
if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)
    
    api_key = config.get('polymarket', {}).get('api_key', '')
    wallet = config.get('polymarket', {}).get('wallet_address', '')
    
    print(f"  钱包：{wallet}")
    print(f"  API Key: {api_key[:10]}...")
    
    # 获取用户持仓
    try:
        headers = {'Authorization': f'Bearer {api_key}'}
        positions_resp = requests.get(
            f"{DATA_API}/v1/portfolio/positions",
            headers=headers,
            params={'user': wallet},
            timeout=10
        )
        
        if positions_resp.ok:
            positions = positions_resp.json()
            print(f"✅ 持仓数量：{len(positions)}")
        else:
            print(f"⚠️  持仓查询失败：{positions_resp.status_code}")
            
    except Exception as e:
        print(f"❌ 持仓查询错误：{e}")
else:
    print("⚠️  配置文件不存在")

print("\n" + "=" * 60)
print("✅ 数据采集完成")
print("=" * 60)
