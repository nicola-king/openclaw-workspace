#!/usr/bin/env python3
"""
Polymarket CLOB API 包装脚本
"""
import os
import site
import sys

# 显式添加用户 site-packages
user_site = '/home/nicola/.local/lib/python3.12/site-packages'
site.addsitedir(user_site)

# 清除代理环境变量
for key in list(os.environ.keys()):
    if 'proxy' in key.lower() or 'PROXY' in key:
        del os.environ[key]
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

# 现在导入
from poly_clob_client.client import ClobClient

def main():
    API_KEY = "019d1b31-787e-7829-87b7-f8382effbab2"
    
    print("=== Polymarket CLOB API 测试 ===")
    print(f"API Key: {API_KEY[:20]}...")
    
    try:
        client = ClobClient(
            host="https://clob.polymarket.com",
            api_key=API_KEY,
        )
        
        print("\n✅ CLOB 客户端创建成功")
        
        balance = client.get_balance()
        print(f"✅ 余额：{balance}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 错误：{type(e).__name__}: {str(e)[:300]}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
