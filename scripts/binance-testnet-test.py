#!/usr/bin/env python3
"""
币安测试网完整交易测试
无需 SAYELF 配置，使用测试网公开 API
"""

import requests
import json
from datetime import datetime

TESTNET = 'https://testnet.binance.vision'

def test_public_api():
    """测试公开 API（无需认证）"""
    print('=' * 60)
    print('🟡 币安测试网 - 公开 API 测试')
    print(f'时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 60)
    
    # 1. 服务器时间
    print('\n【1】服务器时间')
    resp = requests.get(f'{TESTNET}/api/v3/time', timeout=10)
    print(f'✅ {resp.json()}')
    
    # 2. 交易对信息
    print('\n【2】BTCUSDT 交易对信息')
    resp = requests.get(f'{TESTNET}/api/v3/exchangeInfo?symbol=BTCUSDT', timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        symbol = data['symbols'][0]
        print(f'✅ 状态：{symbol["status"]}')
        # 查找 LOT_SIZE 过滤器
        for f in symbol.get('filters', []):
            if f['filterType'] == 'LOT_SIZE':
                print(f'✅ 最小交易量：{f.get("minQty", "N/A")} BTC')
                break
        for f in symbol.get('filters', []):
            if f['filterType'] == 'PRICE_FILTER':
                print(f'✅ 价格精度：{f.get("tickSize", "N/A")}')
                break
    
    # 3. 当前价格
    print('\n【3】BTCUSDT 当前价格')
    resp = requests.get(f'{TESTNET}/api/v3/ticker/price?symbol=BTCUSDT', timeout=10)
    print(f'✅ {resp.json()}')
    
    # 4. 订单簿
    print('\n【4】订单簿 (前 3 档)')
    resp = requests.get(f'{TESTNET}/api/v3/depth?symbol=BTCUSDT&limit=5', timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        print('买盘:')
        for i, bid in enumerate(data['bids'][:3]):
            print(f'  {i+1}. 价格={bid[0]}, 数量={bid[1]}')
        print('卖盘:')
        for i, ask in enumerate(data['asks'][:3]):
            print(f'  {i+1}. 价格={ask[0]}, 数量={ask[1]}')
    
    # 5. 24 小时行情
    print('\n【5】24 小时行情')
    resp = requests.get(f'{TESTNET}/api/v3/ticker/24hr?symbol=BTCUSDT', timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        print(f'✅ 最新价：{data["lastPrice"]}')
        print(f'✅ 涨跌幅：{float(data["priceChangePercent"]):.2f}%')
        print(f'✅ 最高价：{data["highPrice"]}')
        print(f'✅ 最低价：{data["lowPrice"]}')
        print(f'✅ 成交量：{data["volume"]} BTC')
    
    print('\n' + '=' * 60)
    print('✅ 公开 API 测试完成')
    print('=' * 60)
    return True


def get_testnet_apikey_guide():
    """获取测试网 API Key 指南"""
    print('\n📋 测试网 API Key 获取指南:')
    print('-' * 60)
    print('1. 访问：https://testnet.binance.vision/')
    print('2. 点击 "GitHub Login"')
    print('3. 授权后自动生成测试 API Key')
    print('4. 复制 API Key 和 Secret Key')
    print('5. 免费获得测试 USDT (水龙头)')
    print('-' * 60)
    print('\n测试网优势:')
    print('✅ 无需真实资金')
    print('✅ 无需 IP 白名单')
    print('✅ 可完整测试下单/撤单')
    print('✅ 适合策略验证')


if __name__ == '__main__':
    test_public_api()
    get_testnet_apikey_guide()
    
    print('\n🚀 下一步：')
    print('   如需要测试下单，请访问测试网获取 API Key')
    print('   或等待 SAYELF 配置实盘 API Key')
