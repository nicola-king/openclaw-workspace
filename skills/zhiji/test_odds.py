#!/usr/bin/env python3
"""测试获取市场赔率"""

import requests

# 使用你的 API Key
api_key = "019d1b31-787e-7829-87b7-f8382effbab2"
headers = {"Authorization": f"Bearer {api_key}"}

# 测试市场：华盛顿天气
market_id = "will-it-be-sunny-in-washington-dc-at-noon-on-november-3rd"

# 获取赔率
url = f"https://gamma-api.polymarket.com/orderbook/{market_id}"
try:
    response = requests.get(url, headers=headers, timeout=30)
    print(f"状态码：{response.status_code}")
    print(f"响应：{response.text[:500]}")
except Exception as e:
    print(f"错误：{e}")
