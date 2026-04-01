#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polymarket 实时数据采集 v2 - 调试版
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

GAMMA_API = "https://gamma-api.polymarket.com"

print("=" * 60)
print("  Polymarket 数据采集 v2 (调试)")
print("=" * 60)
print()

# 1. 获取热门市场
print("📊 获取热门市场...")
try:
    resp = requests.get(f"{GAMMA_API}/markets", timeout=10)
    print(f"状态码：{resp.status_code}")
    
    data = resp.json()
    print(f"返回类型：{type(data)}")
    
    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())[:10]}")
        # 尝试找到市场列表
        for key in ['markets', 'data', 'items', 'result']:
            if key in data:
                markets = data[key]
                print(f"✅ 找到市场列表：'{key}' ({len(markets)} 个)")
                break
        else:
            markets = data
    else:
        markets = data
    
    if isinstance(markets, list):
        print(f"\n市场数量：{len(markets)}")
        
        if markets:
            print(f"\n第一个市场结构:")
            m = markets[0]
            print(f"  Keys: {list(m.keys())[:15]}")
            
            # 提取关键信息
            print(f"\n示例市场:")
            for key in ['question', 'event', 'title', 'name', 'volume', 'liquidity', 'volume24h']:
                if key in m:
                    print(f"  {key}: {m[key]}")
    
    # 保存原始数据
    output_dir = Path("~/polymarket-data").expanduser()
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "raw_markets.json", 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 原始数据已保存：{output_dir}/raw_markets.json")
    
except Exception as e:
    import traceback
    print(f"❌ 错误：{e}")
    traceback.print_exc()

# 2. 尝试搜索天气市场
print("\n🌤️  搜索天气市场...")
try:
    resp = requests.get(f"{GAMMA_API}/search", params={'q': 'weather'}, timeout=10)
    print(f"状态码：{resp.status_code}")
    
    data = resp.json()
    print(f"返回类型：{type(data)}")
    
    if isinstance(data, list) and data:
        print(f"市场数量：{len(data)}")
        print(f"第一个市场：{data[0].get('question', data[0].get('title', 'N/A'))}")
        
except Exception as e:
    print(f"❌ 错误：{e}")

# 3. 获取简化市场 (CLOB)
print("\n📊 获取 CLOB 市场...")
try:
    resp = requests.get(f"{CLOB_API := 'https://clob.polymarket.com'}/markets", timeout=10)
    print(f"状态码：{resp.status_code}")
    
    if resp.ok:
        data = resp.json()
        print(f"返回类型：{type(data)}")
        if isinstance(data, list):
            print(f"市场数量：{len(data)}")
            
except Exception as e:
    print(f"❌ 错误：{e}")

print("\n" + "=" * 60)
