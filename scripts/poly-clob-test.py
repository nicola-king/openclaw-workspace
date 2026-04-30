#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polymarket CLOB API 测试脚本
功能：市场查询、订单簿、价格等公开数据接入
作者：太一 AGI
日期：2026-03-31
"""

import os
import sys
from datetime import datetime

# 清除代理环境变量
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]
os.environ['NO_PROXY'] = '*'

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY, SELL

# ==================== 配置 ====================
HOST = "https://clob.polymarket.com"
CHAIN_ID = 137  # Polygon mainnet

# 测试市场（从 Gamma API 获取）
TEST_MARKETS = [
    {
        "id": "531202",
        "condition_id": "0xb48621f7eba07b0a3eeabc6afb09ae42490239903997b9d412b0f69aeb040c8b",
        "name": "BitBoy convicted?",
        "token_id_yes": "75467129615908319583031474642658885479135630431889036121812713428992454630178",
        "token_id_no": "3842963720267267286970642336860752782302644680156535061700039388405652129691",
    }
]

# ==================== 测试函数 ====================

def test_client_creation():
    """测试 1: 创建 ClobClient（无认证）"""
    print("=" * 60)
    print("测试 1: 创建 ClobClient（无认证）")
    print("=" * 60)
    
    try:
        client = ClobClient(HOST)
        print(f"✅ ClobClient 创建成功")
        print(f"   Host: {HOST}")
        return client
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        return None


def test_get_market(client, market_info):
    """测试 2: 获取市场详情"""
    print("\n" + "=" * 60)
    print(f"测试 2: 获取市场详情 - {market_info['name']}")
    print("=" * 60)
    
    try:
        market = client.get_market(market_info['condition_id'])
        print(f"✅ 市场信息获取成功")
        print(f"   市场 ID: {market_info['id']}")
        print(f"   Condition ID: {market_info['condition_id'][:20]}...")
        
        # 打印关键字段
        if isinstance(market, dict):
            print(f"   流动性：{market.get('liquidity', 'N/A')}")
            print(f"   成交量：{market.get('volume', 'N/A')}")
            print(f"   最小 tick: {market.get('minimum_tick_size', 'N/A')}")
            print(f"   Neg Risk: {market.get('neg_risk', 'N/A')}")
        else:
            print(f"   返回类型：{type(market)}")
            print(f"   数据：{market}")
        
        return market
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_get_order_book(client, market_info):
    """测试 3: 获取订单簿"""
    print("\n" + "=" * 60)
    print(f"测试 3: 获取订单簿 - {market_info['name']}")
    print("=" * 60)
    
    try:
        # 使用 token_id 获取订单簿
        book = client.get_order_book(market_info['token_id_yes'])
        print(f"✅ 订单簿获取成功")
        
        if hasattr(book, 'bids') and hasattr(book, 'asks'):
            bids = book.bids[:5] if book.bids else []
            asks = book.asks[:5] if book.asks else []
            
            print(f"   买盘数量：{len(bids)}")
            print(f"   卖盘数量：{len(asks)}")
            
            if bids:
                print(f"   最高买价：{bids[0].price if hasattr(bids[0], 'price') else bids[0]}")
            if asks:
                print(f"   最低卖价：{asks[0].price if hasattr(asks[0], 'price') else asks[0]}")
        else:
            print(f"   数据：{book}")
        
        return book
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_get_midpoint(client, market_info):
    """测试 4: 获取中间价"""
    print("\n" + "=" * 60)
    print(f"测试 4: 获取中间价 - {market_info['name']}")
    print("=" * 60)
    
    try:
        midpoint = client.get_midpoint(market_info['token_id_yes'])
        print(f"✅ 中间价获取成功")
        print(f"   中间价：{midpoint}")
        return midpoint
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        return None


def test_get_market_orders(client, market_info):
    """测试 5: 获取市场订单"""
    print("\n" + "=" * 60)
    print(f"测试 5: 获取市场订单 - {market_info['name']}")
    print("=" * 60)
    
    try:
        orders = client.get_orders(market_id=market_info['id'])
        print(f"✅ 市场订单获取成功")
        print(f"   订单数量：{len(orders) if orders else 0}")
        return orders
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        return None


def test_get_trades(client, market_info):
    """测试 6: 获取交易历史"""
    print("\n" + "=" * 60)
    print(f"测试 6: 获取交易历史 - {market_info['name']}")
    print("=" * 60)
    
    try:
        trades = client.get_trades(market_id=market_info['id'])
        print(f"✅ 交易历史获取成功")
        print(f"   交易数量：{len(trades) if trades else 0}")
        
        if trades and len(trades) > 0:
            first_trade = trades[0]
            print(f"   最新交易：{first_trade}")
        
        return trades
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        return None


def test_get_markets(client):
    """测试 7: 获取活跃市场列表"""
    print("\n" + "=" * 60)
    print("测试 7: 获取活跃市场列表")
    print("=" * 60)
    
    try:
        # 使用 Gamma API 获取活跃市场
        import requests
        resp = requests.get(
            "https://gamma-api.polymarket.com/markets",
            params={"active": True, "closed": False, "limit": 10},
            timeout=30
        )
        
        if resp.status_code == 200:
            markets = resp.json()
            print(f"✅ 活跃市场获取成功")
            print(f"   市场数量：{len(markets)}")
            
            print("\n   前 5 个市场:")
            for i, m in enumerate(markets[:5], 1):
                print(f"   {i}. {m.get('question', 'N/A')[:50]}")
                print(f"      流动性：${float(m.get('liquidity', 0)):,.2f}")
                print(f"      成交量：${float(m.get('volume', 0)):,.2f}")
            
            return markets
        else:
            print(f"❌ Gamma API 失败：{resp.status_code}")
            return None
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        return None


def test_api_credentials_flow():
    """测试 8: API 凭证创建流程（需要私钥）"""
    print("\n" + "=" * 60)
    print("测试 8: API 凭证创建流程（需要私钥）")
    print("=" * 60)
    
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    
    if not private_key:
        print("⚠️  未设置 PRIVATE_KEY 环境变量")
        print("   配置方法：export POLYMARKET_PRIVATE_KEY='your_private_key'")
        print("   跳过此测试")
        return None
    
    try:
        # 创建临时客户端
        temp_client = ClobClient(HOST, key=private_key, chain_id=CHAIN_ID)
        print("✅ 临时客户端创建成功")
        
        # 创建或派生 API 凭证
        api_creds = temp_client.create_or_derive_api_creds()
        print("✅ API 凭证创建成功")
        print(f"   API Key: {api_creds.api_key[:20]}...")
        
        # 创建交易客户端
        trading_client = ClobClient(
            HOST,
            key=private_key,
            chain_id=CHAIN_ID,
            creds=api_creds,
            signature_type=0,
        )
        print("✅ 交易客户端创建成功")
        
        return trading_client
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        return None


def test_create_order(client, market_info):
    """测试 9: 创建订单（需要认证）"""
    print("\n" + "=" * 60)
    print(f"测试 9: 创建订单 - {market_info['name']}")
    print("=" * 60)
    
    if not client or not hasattr(client, 'creds') or not client.creds:
        print("⚠️  客户端未认证，跳过此测试")
        print("   需要设置 POLYMARKET_PRIVATE_KEY 环境变量")
        return None
    
    try:
        # 获取市场详情
        market = client.get_market(market_info['condition_id'])
        tick_size = market.get('minimum_tick_size', '0.01')
        neg_risk = market.get('neg_risk', False)
        
        print(f"   Tick Size: {tick_size}")
        print(f"   Neg Risk: {neg_risk}")
        
        # 创建订单
        response = client.create_and_post_order(
            OrderArgs(
                token_id=market_info['token_id_yes'],
                price=0.50,
                size=10,
                side=BUY,
                order_type=OrderType.GTC,
            ),
            options={
                "tick_size": tick_size,
                "neg_risk": neg_risk,
            },
        )
        
        print(f"✅ 订单创建成功")
        print(f"   Order ID: {response.get('orderID', 'N/A')}")
        print(f"   Status: {response.get('status', 'N/A')}")
        
        return response
    except Exception as e:
        print(f"❌ 失败：{type(e).__name__}: {e}")
        return None


# ==================== 主函数 ====================

def main():
    """主测试流程"""
    print("\n" + "=" * 60)
    print("🔷 Polymarket CLOB API 测试")
    print(f"   时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Host: {HOST}")
    print(f"   Chain ID: {CHAIN_ID}")
    print("=" * 60)
    
    # 测试 1: 创建客户端
    client = test_client_creation()
    if not client:
        print("\n❌ 客户端创建失败，终止测试")
        return
    
    # 使用第一个测试市场
    market_info = TEST_MARKETS[0]
    
    # 测试 2-7: 公开 API 测试
    test_get_market(client, market_info)
    test_get_order_book(client, market_info)
    test_get_midpoint(client, market_info)
    test_get_market_orders(client, market_info)
    test_get_trades(client, market_info)
    test_get_markets(client)
    
    # 测试 8-9: 需要认证的测试
    print("\n" + "=" * 60)
    print("以下测试需要 POLYMARKET_PRIVATE_KEY 环境变量")
    print("=" * 60)
    
    trading_client = test_api_credentials_flow()
    if trading_client:
        test_create_order(trading_client, market_info)
    
    # ==================== 总结 ====================
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    print("\n📋 测试结果总结:")
    print("   ✅ 无认证 API: 市场查询、订单簿、价格、交易历史")
    print("   ⏳ 需要认证：下单、余额查询、用户信息")
    print("\n🔧 配置认证:")
    print("   1. 设置环境变量：export POLYMARKET_PRIVATE_KEY='your_key'")
    print("   2. 或在代码中传入私钥：ClobClient(host, key=private_key)")
    print("\n💰 充值后即可开始实盘交易!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
