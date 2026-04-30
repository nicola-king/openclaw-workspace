#!/usr/bin/env python3
"""测试获取市场列表"""

import requests
import json

api_key = "019d1b31-787e-7829-87b7-f8382effbab2"
headers = {"Authorization": f"Bearer {api_key}"}

# 获取市场列表
url = "https://gamma-api.polymarket.com/events?limit=10"
try:
    response = requests.get(url, headers=headers, timeout=30)
    print(f"状态码：{response.status_code}")
    data = response.json()
    print(f"\n市场数量：{len(data)}")
    for m in data[:3]:
        print(f"  - {m.get('title', 'Unknown')[:60]}")
except Exception as e:
    print(f"错误：{e}")
