#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安 API 测试脚本
功能：账户查询、市场行情、下单测试
作者：太一 AGI
日期：2026-03-31
"""

import os
import sys
import time
import hmac
import hashlib
from datetime import datetime

# 清除代理
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]

import requests

# ==================== 配置 ====================
# 币安 API 端点
BINANCE_SPOT_URL = "https://api.binance.com"
BINANCE_TESTNET_URL = "https://testnet.binance.vision"

# 使用测试网 (先测试，后实盘)
USE_TESTNET = True
BASE_URL = BINANCE_TESTNET_URL if USE_TESTNET else BINANCE_SPOT_URL

# API Key (从环境变量读取)
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# ==================== 工具函数 ====================

def generate_signature(query_string):
    """生成 HMAC SHA256 签名"""
    return hmac.new(
        API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def get_server_time():
    """获取服务器时间"""
    url = f"{BASE_URL}/api/v3/time"
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        return data.get('serverTime', 0)
    return 0


def test_api_key():
    """测试 API Key 连通性"""
    print("=" * 60)
    print("测试 1: API Key 连通性")
    print("=" * 60)
    
    if not API_KEY or not API_SECRET:
        print("❌ 未配置 API Key")
        print("   请设置环境变量:")
        print("   export BINANCE_API_KEY='your_api_key'")
        print("   export BINANCE_API_SECRET='your_api_secret'")
        return None
    
    url = f"{BASE_URL}/api/v3/account"
    params = {
        "timestamp": int(time.time() * 1000)
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = generate_signature(query_string)
    params["signature"] = signature
    
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"HTTP 状态：{resp.status_code}")
        
        if resp.status_code == 200:
            account = resp.json()
            print("✅ API Key 有效")
            print(f"   账户 ID: {account.get('accountCommissionRates', {}).get('t', 'N/A')}")
            print(f"    maker 费率：{account.get('makerCommission', 'N/A')}")
            print(f"   taker 费率：{account.get('takerCommission', 'N/A')}")
            return account
        elif resp.status_code == 401:
            print("❌ API Key 无效或签名错误")
            print(f"   错误：{resp.json()}")
            return None
        elif resp.status_code == 403:
            print("❌ IP 被限制或未添加白名单")
            print(f"   错误：{resp.json()}")
            return None
        else:
            print(f"❌ 未知错误：{resp.status_code}")
            print(f"   响应：{resp.text}")
            return None
    except Exception as e:
        print(f"❌ 异常：{type(e).__name__}: {e}")
        return None


def get_account_balance(account=None):
    """获取账户余额"""
    print("\n" + "=" * 60)
    print("测试 2: 账户余额")
    print("=" * 60)
    
    if not account:
        print("⏭️ 跳过 (API Key 未配置)")
        return
    
    balances = account.get('balances', [])
    non_zero = [b for b in balances if float(b.get('free', 0)) > 0 or float(b.get('locked', 0)) > 0]
    
    print(f"总资产：{len(balances)} 种")
    print(f"非零资产：{len(non_zero)} 种")
    
    if non_zero:
        print("\n非零余额:")
        for b in non_zero[:10]:  # 显示前 10 个
            asset = b.get('asset', 'N/A')
            free = float(b.get('free', 0))
            locked = float(b.get('locked', 0))
            total = free + locked
            print(f"   {asset}: {total:.8f} (可用：{free:.8f}, 冻结：{locked:.8f})")


def get_market_ticker(symbol="BTCUSDT"):
    """获取市场行情"""
    print("\n" + "=" * 60)
    print(f"测试 3: 市场行情 - {symbol}")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v3/ticker/24hr"
    params = {"symbol": symbol}
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            ticker = resp.json()
            print(f"✅ {symbol} 24 小时行情:")
            print(f"   最新价：{ticker.get('lastPrice', 'N/A')}")
            print(f"   涨跌幅：{ticker.get('priceChangePercent', 'N/A')}%")
            print(f"   最高价：{ticker.get('highPrice', 'N/A')}")
            print(f"   最低价：{ticker.get('lowPrice', 'N/A')}")
            print(f"   成交量：{ticker.get('volume', 'N/A')} {symbol[:4]}")
            print(f"   成交额：{ticker.get('quoteVolume', 'N/A')} USDT")
            return ticker
        else:
            print(f"❌ 失败：{resp.status_code}")
            return None
    except Exception as e:
        print(f"❌ 异常：{type(e).__name__}: {e}")
        return None


def get_order_book(symbol="BTCUSDT", limit=5):
    """获取订单簿"""
    print("\n" + "=" * 60)
    print(f"测试 4: 订单簿 - {symbol}")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/v3/depth"
    params = {"symbol": symbol, "limit": limit}
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            bids = data.get('bids', [])
            asks = data.get('asks', [])
            
            print(f"✅ 订单簿 (前{limit}档):")
            print(f"\n买盘 (Bids):")
            for i, bid in enumerate(bids, 1):
                print(f"  {i}. 价格：{bid[0]} | 数量：{bid[1]}")
            
            print(f"\n卖盘 (Asks):")
            for i, ask in enumerate(asks, 1):
                print(f"  {i}. 价格：{ask[0]} | 数量：{ask[1]}")
            
            if bids and asks:
                spread = float(asks[0][0]) - float(bids[0][0])
                mid = (float(asks[0][0]) + float(bids[0][0])) / 2
                print(f"\n中间价：{mid:.2f}")
                print(f"Spread: {spread:.2f}")
            
            return data
        else:
            print(f"❌ 失败：{resp.status_code}")
            return None
    except Exception as e:
        print(f"❌ 异常：{type(e).__name__}: {e}")
        return None


def test_place_order(symbol="BTCUSDT", side="BUY", price=None, qty=0.001):
    """测试下单 (限价单)"""
    print("\n" + "=" * 60)
    print(f"测试 5: 下单测试 - {side} {symbol}")
    print("=" * 60)
    
    if not API_KEY or not API_SECRET:
        print("⏭️ 跳过 (API Key 未配置)")
        return
    
    # 获取当前价格
    if not price:
        ticker = get_market_ticker(symbol)
        if ticker:
            price = float(ticker.get('lastPrice', 0))
            # 调整价格到合理范围
            if side == "BUY":
                price = price * 0.95  # 低于市价 5%
            else:
                price = price * 1.05  # 高于市价 5%
    
    if not price:
        print("❌ 无法获取价格")
        return
    
    url = f"{BASE_URL}/api/v3/order"
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": qty,
        "price": f"{price:.2f}",
        "timestamp": int(time.time() * 1000)
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = generate_signature(query_string)
    params["signature"] = signature
    
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    
    try:
        resp = requests.post(url, headers=headers, params=params, timeout=10)
        print(f"HTTP 状态：{resp.status_code}")
        
        if resp.status_code == 200:
            order = resp.json()
            print("✅ 下单成功")
            print(f"   订单 ID: {order.get('orderId', 'N/A')}")
            print(f"   状态：{order.get('status', 'N/A')}")
            print(f"   价格：{order.get('price', 'N/A')}")
            print(f"   数量：{order.get('origQty', 'N/A')}")
            return order
        else:
            print(f"❌ 下单失败：{resp.status_code}")
            print(f"   响应：{resp.json()}")
            return None
    except Exception as e:
        print(f"❌ 异常：{type(e).__name__}: {e}")
        return None


def get_open_orders(symbol=None):
    """获取当前挂单"""
    print("\n" + "=" * 60)
    print("测试 6: 当前挂单")
    print("=" * 60)
    
    if not API_KEY or not API_SECRET:
        print("⏭️ 跳过 (API Key 未配置)")
        return
    
    url = f"{BASE_URL}/api/v3/openOrders"
    params = {
        "timestamp": int(time.time() * 1000)
    }
    
    if symbol:
        params["symbol"] = symbol
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = generate_signature(query_string)
    params["signature"] = signature
    
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            orders = resp.json()
            print(f"✅ 当前挂单：{len(orders)} 个")
            for order in orders[:5]:  # 显示前 5 个
                print(f"   {order.get('symbol', 'N/A')} | {order.get('side', 'N/A')} | "
                      f"价格：{order.get('price', 'N/A')} | 数量：{order.get('origQty', 'N/A')}")
            return orders
        else:
            print(f"❌ 失败：{resp.status_code}")
            return None
    except Exception as e:
        print(f"❌ 异常：{type(e).__name__}: {e}")
        return None


# ==================== 主函数 ====================

def main():
    """主测试流程"""
    print("\n" + "=" * 60)
    print("🟡 币安 API 测试")
    print(f"   时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   环境：{'测试网' if USE_TESTNET else '实盘'}")
    print(f"   URL: {BASE_URL}")
    print("=" * 60)
    
    # 测试 1: API Key 连通性
    account = test_api_key()
    
    # 测试 2: 账户余额
    get_account_balance(account)
    
    # 测试 3-4: 市场行情 (无需认证)
    get_market_ticker("BTCUSDT")
    get_order_book("BTCUSDT")
    
    # 测试 5-6: 下单相关 (需要认证)
    if account:
        test_place_order()
        get_open_orders()
    
    # ==================== 总结 ====================
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    print("\n📋 测试结果总结:")
    print(f"   环境：{'测试网' if USE_TESTNET else '实盘'}")
    print(f"   API Key: {'✅ 已配置' if API_KEY else '❌ 未配置'}")
    print(f"   账户查询：{'✅' if account else '❌'}")
    print(f"   市场行情：✅ (无需认证)")
    print(f"   下单交易：{'⏳ 待测试' if account else '❌ 需 API Key'}")
    print("\n🔧 配置 API Key:")
    print("   1. 登录 https://www.binance.com/my/settings/api-management")
    print("   2. 创建 API Key (启用 Spot & Margin Trading)")
    print("   3. 设置环境变量:")
    print("      export BINANCE_API_KEY='your_api_key'")
    print("      export BINANCE_API_SECRET='your_api_secret'")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
