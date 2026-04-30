#!/usr/bin/env python3
import os
import sys

# 添加用户 site-packages 到路径
user_site = '/home/nicola/.local/lib/python3.12/site-packages'
sys.path.insert(0, user_site)
os.environ['PYTHONPATH'] = user_site

from poly_clob_client.client import ClobClient

API_KEY = "019d1b31-787e-7829-87b7-f8382effbab2"

print("=== Polymarket CLOB API 测试 ===")
print(f"API Key: {API_KEY[:20]}...")

try:
    client = ClobClient(
        host="https://clob.polymarket.com",
        api_key=API_KEY,
    )
    
    print("\n✅ CLOB 客户端创建成功")
    
    # 测试余额
    print("\n查询余额...")
    balance = client.get_balance()
    print(f"✅ 余额：{balance}")
    
except Exception as e:
    print(f"\n⚠️ 测试：{type(e).__name__}: {str(e)[:300]}")
