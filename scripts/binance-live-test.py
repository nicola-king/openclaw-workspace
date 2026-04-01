#!/usr/bin/env python3
"""
币安实时 API 测试
验证 API Key 配置和连接
"""

import hashlib
import hmac
import time
import requests
import json

# 加载配置
with open('/home/nicola/.openclaw/workspace/config/binance-config.json') as f:
    config = json.load(f)

API_KEY = config['api_config']['api_key']
SECRET_KEY = config['api_config']['secret_key']
BASE_URL = config['api_config']['base_url']

def get_signature(query_string):
    return hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def test_public_api():
    """测试公开 API"""
    print('📊 测试公开 API...')
    resp = requests.get(f'{BASE_URL}/api/v3/ticker/price?symbol=ETHUSDT')
    if resp.status_code == 200:
        data = resp.json()
        print(f'  ✅ ETH 价格：${data["price"]}')
        return True
    else:
        print(f'  ❌ 失败：{resp.text}')
        return False

def test_private_api():
    """测试私有 API (账户信息)"""
    print('🔐 测试私有 API...')
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp}'
    signature = get_signature(query_string)
    
    headers = {'X-MBX-APIKEY': API_KEY}
    resp = requests.get(f'{BASE_URL}/api/v3/account?{query_string}&signature={signature}', headers=headers)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f'  ✅ 账户连接成功')
        # 查找 ETH 余额
        for asset in data.get('balances', []):
            if asset['asset'] == 'ETH':
                free = float(asset['free'])
                locked = float(asset['locked'])
                if free > 0 or locked > 0:
                    print(f'  💰 ETH 余额：{free:.4f} (可用) / {locked:.4f} (冻结)')
                break
        return True
    else:
        print(f'  ❌ 失败：{resp.status_code} - {resp.text}')
        return False

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🚀 币安 API 实时测试                                       ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    
    public_ok = test_public_api()
    print('')
    private_ok = test_private_api()
    print('')
    
    if public_ok and private_ok:
        print('✅ 币安 API 测试通过 - 可以实盘')
    else:
        print('🟡 币安 API 部分通过 - 请检查配置')

if __name__ == '__main__':
    main()
