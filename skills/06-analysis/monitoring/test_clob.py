#!/usr/bin/env python3
"""
测试 CLOB API 获取实时市场
"""

import requests

PROXY_CONFIG = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

print("=" * 70)
print("🔍 测试 CLOB API 实时市场")
print("=" * 70)

# 测试 CLOB API
url = "https://clob.polymarket.com/markets"
params = {"active": "true", "limit": 20}

try:
    print(f"\n请求：{url}")
    response = requests.get(url, params=params, proxies=PROXY_CONFIG, timeout=30)
    print(f"状态码：{response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 成功！返回 {len(data)} 个市场")
        print()
        
        if isinstance(data, list) and len(data) > 0:
            for m in data[:10]:
                slug = m.get('slug', m.get('eventSlug', 'N/A'))
                title = m.get('question', m.get('title', 'N/A'))[:60]
                print(f"  - {title}")
                print(f"    slug: {slug}")
                print()
        else:
            print("⚠️ 数据格式异常")
            print(f"类型：{type(data)}")
    else:
        print(f"❌ 错误：{response.text[:200]}")
        
except Exception as e:
    print(f"❌ 异常：{e}")

print("=" * 70)
