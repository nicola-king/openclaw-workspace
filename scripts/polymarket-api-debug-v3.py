#!/usr/bin/env python3
"""
Polymarket API 深度调试工具 v3
目标：找到正确的赔率获取接口
"""

import requests
import json
from datetime import datetime

# 新 API Key
API_KEY = "019d2560-86f6-710d-ad87-57af5ad6b47e"

# 可能的 API 端点
ENDPOINTS = [
    # 公开接口（无需认证）
    {
        "name": "Gamma API - Events",
        "url": "https://gamma-api.polymarket.com/events",
        "params": {"limit": 10},
        "auth": False
    },
    {
        "name": "Gamma API - Event Details",
        "url": "https://gamma-api.polymarket.com/events/{}",
        "params": {},
        "auth": False,
        "needs_id": True
    },
    {
        "name": "Polymarket API v2 - Markets",
        "url": "https://api.polymarket.com/markets",
        "params": {"limit": 10},
        "auth": True
    },
    {
        "name": "Polymarket API v2 - Orderbook",
        "url": "https://api.polymarket.com/orderbook",
        "params": {"market": "{}"},
        "auth": False,
        "needs_id": True
    },
    {
        "name": "Polymarket API - Prices",
        "url": "https://api.polymarket.com/prices",
        "params": {"market": "{}"},
        "auth": False,
        "needs_id": True
    },
    # 条件订单合约 API
    {
        "name": "Conditional Tokens - Get Outcome Tokens",
        "url": "https://api.polymarket.com/condo/outcome-tokens",
        "params": {"market_id": "{}"},
        "auth": False,
        "needs_id": True
    },
]

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }

def test_endpoint(endpoint, market_id=None):
    """测试单个端点"""
    name = endpoint["name"]
    url = endpoint["url"]
    params = endpoint["params"].copy()
    auth = endpoint.get("auth", False)
    needs_id = endpoint.get("needs_id", False)
    
    if needs_id and market_id:
        if "{}" in url:
            url = url.format(market_id)
        for key in params:
            if isinstance(params[key], str) and "{}" in params[key]:
                params[key] = params[key].format(market_id)
    
    try:
        headers = get_headers() if auth else {}
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        status = response.status_code
        success = 200 <= status < 300
        
        print(f'\n{name}')
        print(f'  URL: {url}')
        print(f'  状态：{status} {"✅" if success else "❌"}')
        
        if success:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f'  数据：{len(data)} 条记录')
                elif isinstance(data, dict):
                    print(f'  数据：{list(data.keys())}')
                
                # 打印关键信息
                if isinstance(data, list) and len(data) > 0:
                    print(f'  示例：{json.dumps(data[0], indent=2)[:500]}...')
                elif isinstance(data, dict):
                    print(f'  内容：{json.dumps(data, indent=2)[:500]}...')
                
                return data
            except:
                print(f'  内容：{response.text[:200]}...')
        else:
            print(f'  错误：{response.text[:200]}')
        
        return None
    
    except Exception as e:
        print(f'\n{name}')
        print(f'  异常：{e}')
        return None

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🔍 Polymarket API 深度调试 v3                             ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print(f'🔑 API Key: {API_KEY[:10]}...{API_KEY[-6:]}')
    
    # 先获取一个市场 ID 用于测试
    print('\n📊 获取测试市场 ID...')
    url = "https://gamma-api.polymarket.com/events"
    params = {"limit": 5}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        markets = response.json()
        
        if markets and len(markets) > 0:
            market_id = markets[0].get("id")
            print(f'  ✅ 测试市场：{market_id}')
            print(f'  名称：{markets[0].get("title", "Unknown")[:50]}')
        else:
            market_id = None
            print('  ❌ 无法获取市场 ID')
    except Exception as e:
        market_id = None
        print(f'  ❌ 错误：{e}')
    
    # 测试所有端点
    print('\n🔍 测试 API 端点...')
    print('=' * 60)
    
    results = {}
    for endpoint in ENDPOINTS:
        data = test_endpoint(endpoint, market_id)
        results[endpoint["name"]] = data is not None
    
    # 汇总
    print('\n' + '=' * 60)
    print('📊 测试结果汇总')
    print('=' * 60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for name, success in results.items():
        icon = "✅" if success else "❌"
        print(f'  {icon} {name}')
    
    print(f'\n总计：{success_count}/{total_count} 端点可用')
    
    if success_count > 0:
        print('\n✅ 找到可用端点，可继续开发')
    else:
        print('\n❌ 所有端点均不可用，可能需要：')
        print('   1. 使用 WebSocket 接口')
        print('   2. 逆向工程网页 API')
        print('   3. 手动录入数据')

if __name__ == '__main__':
    main()
