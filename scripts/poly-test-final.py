#!/usr/bin/env python3
import os
import sys

# 关键：在导入任何模块前清除代理
for key in list(os.environ.keys()):
    if 'proxy' in key.lower() or 'PROXY' in key:
        del os.environ[key]
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

# 添加工作区路径
sys.path.insert(0, '/home/nicola/.openclaw/workspace')

# 现在导入
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds

# Polymarket 配置
CLOB_HOST = "https://clob.polymarket.com"
POLY_API_KEY = "019d1b31-787e-7829-87b7-f8382effbab2"

print("=== Polymarket CLOB API 测试 ===")
print(f"API Key: {POLY_API_KEY[:20]}...")
print(f"CLOB Host: {CLOB_HOST}")

try:
    # Level 0: 无需认证，测试公共端点
    print("\n1. 测试 Level 0 (无认证)...")
    client = ClobClient(host=CLOB_HOST)
    print("   ✅ CLOB 客户端创建成功 (Level 0)")
    
    # 测试获取时间
    print("\n2. 测试公共端点 (get time)...")
    try:
        time_data = client.get_time()
        print(f"   ✅ 服务器时间：{time_data}")
    except Exception as e:
        print(f"   ⚠️ 时间查询：{e}")
    
    # 测试获取市场
    print("\n3. 测试获取市场...")
    try:
        markets = client.get_markets()
        print(f"   ✅ 市场数量：{len(markets) if markets else 0}")
    except Exception as e:
        print(f"   ⚠️ 市场查询：{e}")
    
    # Level 2: 使用 API Key 认证
    print("\n4. 测试 Level 2 (API Key 认证)...")
    creds = ApiCreds(api_key=POLY_API_KEY)
    client_auth = ClobClient(host=CLOB_HOST, creds=creds)
    print("   ✅ 认证客户端创建成功 (Level 2)")
    
    # 测试余额
    print("\n5. 查询余额...")
    try:
        balance = client_auth.get_balance()
        print(f"   ✅ 余额：{balance}")
    except Exception as e:
        print(f"   ⚠️ 余额查询：{type(e).__name__}: {str(e)[:200]}")
    
    print("\n✅ Polymarket CLOB API 测试完成!")
    
except Exception as e:
    print(f"\n❌ 错误：{type(e).__name__}: {str(e)[:400]}")
    import traceback
    traceback.print_exc()
