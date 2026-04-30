#!/usr/bin/env python3
"""
Polymarket 市场数据采集 v3 (新 API Key)
"""

import requests
import json
from datetime import datetime
import sqlite3

# 新 API Key (2026-03-30 12:22)
API_KEY = "019d2560-86f6-710d-ad87-57af5ad6b47e"
SECRET_KEY = "_XojDuWKYjaxwqP4u04_ZqiilIQypU_Kdn6GtjhHmnc="
DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }

def test_api():
    """测试 API 连接"""
    print('🔑 测试 API 连接...')
    
    # 测试 1：获取账户信息
    url = "https://api.polymarket.com/user"
    try:
        response = requests.get(url, headers=get_headers(), timeout=30)
        print(f'  账户接口：{response.status_code}')
        if response.status_code == 200:
            user = response.json()
            print(f'  ✅ 账户：{user.get("address", "Unknown")[:10]}...')
            return True
    except Exception as e:
        print(f'  ❌ 账户接口失败：{e}')
    
    # 测试 2：获取市场列表（公开接口）
    url = "https://gamma-api.polymarket.com/events?limit=10"
    try:
        response = requests.get(url, timeout=30)
        print(f'  市场接口：{response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'  ✅ 市场数量：{len(data) if isinstance(data, list) else "OK"}')
            return True
    except Exception as e:
        print(f'  ❌ 市场接口失败：{e}')
    
    return False

def get_markets_simple():
    """简单获取市场列表（无认证）"""
    url = "https://gamma-api.polymarket.com/events"
    params = {"limit": 50}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取市场失败：{e}")
        return []

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🌤️  Polymarket API 测试 (新 Key)                        ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print(f'🔑 API Key: {API_KEY[:10]}...{API_KEY[-6:]}')
    print('')
    
    # 测试 API
    if test_api():
        print('')
        print('✅ API 连接正常')
    else:
        print('')
        print('⚠️  API 连接异常，尝试公开接口...')
    
    # 获取市场
    print('')
    print('📊 获取市场列表...')
    markets = get_markets_simple()
    print(f'  找到 {len(markets)} 个市场')
    
    if markets:
        print('')
        print('=== 前 5 个市场 ===')
        for m in markets[:5]:
            title = m.get("title", "Unknown")[:50]
            print(f"  - {title}")

if __name__ == '__main__':
    main()
