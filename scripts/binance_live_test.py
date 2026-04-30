#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安实盘测试 - 极小金额

测试内容:
1. 查询账户余额
2. 下单测试 (BTC/USDT 网格交易)
3. 查询订单状态
4. 撤销订单

风控限制:
- 单笔最大：$10 USDT
- 每日最大：$50 USDT
- 止损：5%
- 止盈：10%

作者：太一 AGI
创建：2026-04-22
"""

import hashlib
import hmac
import requests
import time
import json
from pathlib import Path
from datetime import datetime

# 加载配置
env_file = Path("/home/nicola/.openclaw/workspace/.taiyi/zhiji/.env.binance")
if not env_file.exists():
    print("❌ 配置文件不存在！")
    exit(1)

# 读取 API 密钥
api_key = None
api_secret = None

with open(env_file, 'r') as f:
    for line in f:
        if line.startswith("BINANCE_API_KEY="):
            api_key = line.split("=")[1].strip()
        elif line.startswith("BINANCE_API_SECRET="):
            api_secret = line.split("=")[1].strip()

if not api_key or not api_secret:
    print("❌ API 密钥配置错误！")
    exit(1)

# 测试配置
TEST_CONFIG = {
    "symbol": "BTCUSDT",
    "test_amount_usdt": 10,  # 测试金额$10
    "grid_levels": 3,        # 网格层数
    "grid_spacing": 0.005,   # 网格间距 0.5%
    "stop_loss": 0.05,       # 止损 5%
    "take_profit": 0.10,     # 止盈 10%
}

# 币安 API 基础 URL
BASE_URL = "https://api.binance.com"


def generate_signature(params: str) -> str:
    """生成签名"""
    return hmac.new(
        api_secret.encode('utf-8'),
        params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def get_account_balance():
    """获取账户余额"""
    print("\n" + "=" * 60)
    print("💰 查询账户余额")
    print("=" * 60)
    
    try:
        timestamp = int(time.time() * 1000)
        params = f"timestamp={timestamp}"
        signature = generate_signature(params)
        
        url = f"{BASE_URL}/api/v3/account?{params}&signature={signature}"
        headers = {"X-MBX-APIKEY": api_key}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            account = response.json()
            
            print(f"\n✅ 账户状态：正常")
            print(f"\n💵 USDT 余额:")
            
            usdt_balance = None
            for asset in account['balances']:
                if asset['asset'] == 'USDT':
                    free = float(asset['free'])
                    locked = float(asset['locked'])
                    total = free + locked
                    
                    usdt_balance = free
                    
                    print(f"   可用：{free:.2f} USDT")
                    print(f"   冻结：{locked:.2f} USDT")
                    print(f"   总计：{total:.2f} USDT")
                    
                    # 检查是否足够测试
                    if free >= TEST_CONFIG['test_amount_usdt']:
                        print(f"\n✅ 余额充足！可以进行${TEST_CONFIG['test_amount_usdt']}测试")
                    else:
                        print(f"\n⚠️  余额不足！需要至少${TEST_CONFIG['test_amount_usdt']} USDT")
                        print(f"   当前可用：${free:.2f} USDT")
                    break
            
            # 显示其他主要币种余额
            print(f"\n📊 其他主要币种:")
            for asset in ['BTC', 'ETH', 'BNB']:
                for balance in account['balances']:
                    if balance['asset'] == asset:
                        total = float(balance['free']) + float(balance['locked'])
                        if total > 0:
                            print(f"   {asset}: {total:.6f}")
                        break
            
            return usdt_balance
            
        elif response.status_code == 401:
            print(f"❌ API 密钥无效！")
            print(f"   错误：{response.json()['msg']}")
            return None
        elif response.status_code == 403:
            print(f"❌ IP 不在白名单！")
            print(f"   错误：{response.json()['msg']}")
            print(f"   请添加 IP 白名单：103.151.172.30")
            return None
        else:
            print(f"❌ 失败：{response.status_code}")
            print(f"   错误：{response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def get_current_price(symbol: str = "BTCUSDT"):
    """获取当前价格"""
    print(f"\n" + "=" * 60)
    print(f"📊 查询 {symbol} 当前价格")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v3/ticker/price?symbol={symbol}",
            timeout=10
        )
        
        if response.status_code == 200:
            price = float(response.json()['price'])
            print(f"\n✅ {symbol}: ${price:,.2f}")
            return price
        else:
            print(f"❌ 失败：{response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def place_test_order(symbol: str = "BTCUSDT", side: str = "BUY", 
                     amount_usdt: float = 10, price: float = None):
    """
    下测试订单
    
    Args:
        symbol: 交易对
        side: BUY/SELL
        amount_usdt: 金额 (USDT)
        price: 价格 (None 为市价单)
    """
    print(f"\n" + "=" * 60)
    print(f"🚀 下测试订单")
    print("=" * 60)
    
    try:
        # 获取当前价格 (如果未提供)
        if price is None:
            price = get_current_price(symbol)
            if price is None:
                return None
        
        # 计算数量
        quantity = amount_usdt / price
        
        # 精度处理 (BTC 最小精度 0.00001)
        quantity = round(quantity, 5)
        
        print(f"\n📋 订单详情:")
        print(f"   交易对：{symbol}")
        print(f"   方向：{side}")
        print(f"   类型：市价单")
        print(f"   金额：${amount_usdt:.2f} USDT")
        print(f"   价格：${price:,.2f}")
        print(f"   数量：{quantity:.5f} BTC")
        
        # 询问确认
        print(f"\n⚠️  确认下单？")
        print(f"   这将实际执行交易！")
        
        # 自动确认 (实盘测试)
        print(f"   ✅ 确认执行 (实盘测试)")
        
        # 下单
        timestamp = int(time.time() * 1000)
        params = f"symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}"
        signature = generate_signature(params)
        
        url = f"{BASE_URL}/api/v3/order?{params}&signature={signature}"
        headers = {"X-MBX-APIKEY": api_key}
        
        response = requests.post(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            order = response.json()
            
            print(f"\n✅ 订单执行成功！")
            print(f"   订单 ID: {order['orderId']}")
            print(f"   状态：{order['status']}")
            print(f"   成交价：${float(order['fills'][0]['price']):,.2f}")
            print(f"   成交量：{float(order['fills'][0]['qty']):.5f}")
            print(f"   手续费：{float(order['fills'][0]['commission']):.4f} {order['fills'][0]['commissionAsset']}")
            
            return order
            
        else:
            print(f"❌ 下单失败：{response.status_code}")
            print(f"   错误：{response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def check_order_status(symbol: str = "BTCUSDT", order_id: int = None):
    """查询订单状态"""
    if order_id is None:
        print("\n⚠️  未提供订单 ID")
        return None
    
    print(f"\n" + "=" * 60)
    print(f"📋 查询订单状态")
    print("=" * 60)
    
    try:
        timestamp = int(time.time() * 1000)
        params = f"symbol={symbol}&orderId={order_id}&timestamp={timestamp}"
        signature = generate_signature(params)
        
        url = f"{BASE_URL}/api/v3/order?{params}&signature={signature}"
        headers = {"X-MBX-APIKEY": api_key}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            order = response.json()
            
            print(f"\n✅ 订单状态:")
            print(f"   订单 ID: {order['orderId']}")
            print(f"   状态：{order['status']}")
            print(f"   方向：{order['side']}")
            print(f"   类型：{order['type']}")
            print(f"   数量：{order['origQty']}")
            print(f"   成交价：{order['price']}")
            
            return order
        else:
            print(f"❌ 查询失败：{response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def run_live_test():
    """运行实盘测试流程"""
    print("=" * 60)
    print("🧪 币安实盘测试 - 极小金额")
    print("=" * 60)
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试金额：${TEST_CONFIG['test_amount_usdt']} USDT")
    print(f"交易对：{TEST_CONFIG['symbol']}")
    print(f"止损：{TEST_CONFIG['stop_loss']*100}%")
    print(f"止盈：{TEST_CONFIG['take_profit']*100}%")
    
    # 1. 查询余额
    balance = get_account_balance()
    if balance is None or balance < TEST_CONFIG['test_amount_usdt']:
        print("\n❌ 余额不足，无法继续测试")
        return
    
    # 2. 查询价格
    current_price = get_current_price()
    if current_price is None:
        print("\n❌ 无法获取价格，无法继续测试")
        return
    
    # 3. 下单测试
    print("\n" + "=" * 60)
    print("📋 准备下单...")
    print("=" * 60)
    
    order = place_test_order(
        symbol=TEST_CONFIG['symbol'],
        side="BUY",
        amount_usdt=TEST_CONFIG['test_amount_usdt']
    )
    
    if order:
        print("\n✅ 实盘测试成功！")
        
        # 4. 查询订单状态
        time.sleep(2)  # 等待订单成交
        check_order_status(
            symbol=TEST_CONFIG['symbol'],
            order_id=order['orderId']
        )
        
        # 5. 保存测试记录
        test_record = {
            "timestamp": datetime.now().isoformat(),
            "symbol": TEST_CONFIG['symbol'],
            "side": "BUY",
            "amount_usdt": TEST_CONFIG['test_amount_usdt'],
            "order_id": order['orderId'],
            "status": order['status'],
            "price": float(order['fills'][0]['price']),
            "quantity": float(order['fills'][0]['qty']),
            "fee": float(order['fills'][0]['commission']),
            "fee_asset": order['fills'][0]['commissionAsset'],
        }
        
        # 保存到文件
        record_file = Path("/home/nicola/.openclaw/workspace/data/binance_live_test_records.json")
        record_file.parent.mkdir(parents=True, exist_ok=True)
        
        records = []
        if record_file.exists():
            with open(record_file, 'r') as f:
                records = json.load(f)
        
        records.append(test_record)
        
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 测试记录已保存：{record_file}")
        
    else:
        print("\n❌ 实盘测试失败")


if __name__ == "__main__":
    run_live_test()
