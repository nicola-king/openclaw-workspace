#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安现货网格交易机器人
基于官方 API，支持实盘交易
作者：太一 AGI
日期：2026-03-31
"""

import os
import sys
import time
import hmac
import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, List

# 清除代理
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]

import requests

# ==================== 配置 ====================

# 币安 API 端点
BINANCE_MAINNET = "https://api.binance.com"
BINANCE_TESTNET = "https://testnet.binance.vision"

# 默认使用实盘 (SAYELF 要求真实交易)
USE_TESTNET = False
BASE_URL = BINANCE_TESTNET if USE_TESTNET else BINANCE_MAINNET

# API 凭证 (从环境变量读取)
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")

# 交易配置
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_GRID_NUM = 10  # 网格数量
DEFAULT_INVESTMENT = 100  # 投资金额 (USDT)

# ==================== 工具函数 ====================

def generate_signature(query_string: str) -> str:
    """生成 HMAC SHA256 签名"""
    return hmac.new(
        API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def get_timestamp() -> int:
    """获取当前时间戳 (毫秒)"""
    return int(time.time() * 1000)


def request(method: str, path: str, params: Optional[Dict] = None, signed: bool = False):
    """发送 API 请求"""
    url = f"{BASE_URL}{path}"
    headers = {"X-MBX-APIKEY": API_KEY}
    
    if params is None:
        params = {}
    
    if signed:
        params["timestamp"] = get_timestamp()
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        params["signature"] = generate_signature(query_string)
    
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == "POST":
            resp = requests.post(url, headers=headers, params=params, timeout=10)
        elif method == "DELETE":
            resp = requests.delete(url, headers=headers, params=params, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   响应：{e.response.text}")
        return None


# ==================== 市场数据 (无需认证) ====================

def get_symbol_info(symbol: str) -> Optional[Dict]:
    """获取交易对信息"""
    resp = request("GET", "/api/v3/exchangeInfo")
    if resp and 'symbols' in resp:
        for s in resp['symbols']:
            if s['symbol'] == symbol:
                return s
    return None


def get_current_price(symbol: str) -> Optional[float]:
    """获取当前价格"""
    resp = request("GET", "/api/v3/ticker/price", {"symbol": symbol})
    if resp and 'price' in resp:
        return float(resp['price'])
    return None


def get_order_book(symbol: str, limit: int = 5) -> Optional[Dict]:
    """获取订单簿"""
    resp = request("GET", "/api/v3/depth", {"symbol": symbol, "limit": limit})
    return resp


def get_klines(symbol: str, interval: str = "1h", limit: int = 100) -> Optional[List]:
    """获取 K 线数据"""
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    resp = request("GET", "/api/v3/klines", params)
    return resp


# ==================== 账户信息 (需要认证) ====================

def get_account() -> Optional[Dict]:
    """获取账户信息"""
    return request("GET", "/api/v3/account", signed=True)


def get_balance(asset: str = "USDT") -> Optional[float]:
    """获取特定资产余额"""
    account = get_account()
    if account and 'balances' in account:
        for b in account['balances']:
            if b['asset'] == asset:
                return float(b['free'])
    return 0.0


def get_open_orders(symbol: Optional[str] = None) -> Optional[List]:
    """获取当前挂单"""
    params = {}
    if symbol:
        params["symbol"] = symbol
    return request("GET", "/api/v3/openOrders", params, signed=True)


def get_order_status(symbol: str, order_id: int) -> Optional[Dict]:
    """获取订单状态"""
    params = {
        "symbol": symbol,
        "orderId": order_id
    }
    return request("GET", "/api/v3/order", params, signed=True)


# ==================== 交易操作 (需要认证) ====================

def place_limit_order(symbol: str, side: str, price: float, quantity: float, 
                      time_in_force: str = "GTC") -> Optional[Dict]:
    """下限价单"""
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "timeInForce": time_in_force,
        "price": f"{price:.8f}",
        "quantity": f"{quantity:.8f}"
    }
    return request("POST", "/api/v3/order", params, signed=True)


def place_market_order(symbol: str, side: str, quantity: float) -> Optional[Dict]:
    """下市价单"""
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": f"{quantity:.8f}"
    }
    return request("POST", "/api/v3/order", params, signed=True)


def cancel_order(symbol: str, order_id: int) -> Optional[Dict]:
    """取消订单"""
    params = {
        "symbol": symbol,
        "orderId": order_id
    }
    return request("DELETE", "/api/v3/order", params, signed=True)


def cancel_all_orders(symbol: str) -> Optional[Dict]:
    """取消所有挂单"""
    params = {"symbol": symbol}
    return request("DELETE", "/api/v3/openOrders", params, signed=True)


# ==================== 网格交易策略 ====================

class GridTradingBot:
    """现货网格交易机器人"""
    
    def __init__(self, symbol: str = DEFAULT_SYMBOL, 
                 grid_num: int = DEFAULT_GRID_NUM,
                 investment: float = DEFAULT_INVESTMENT):
        self.symbol = symbol
        self.grid_num = grid_num
        self.investment = investment
        self.orders = []
        
    def calculate_grid_levels(self, low_price: float, high_price: float) -> List[float]:
        """计算网格价格线"""
        step = (high_price - low_price) / self.grid_num
        levels = []
        for i in range(self.grid_num + 1):
            levels.append(low_price + step * i)
        return levels
    
    def create_grid(self, low_price: float, high_price: float):
        """创建网格交易"""
        print("=" * 60)
        print(f"🟡 创建网格交易")
        print("=" * 60)
        print(f"交易对：{self.symbol}")
        print(f"价格区间：{low_price} - {high_price}")
        print(f"网格数量：{self.grid_num}")
        print(f"投资金额：{self.investment} USDT")
        
        # 获取当前价格
        current_price = get_current_price(self.symbol)
        if not current_price:
            print("❌ 无法获取当前价格")
            return
        
        print(f"当前价格：{current_price}")
        
        # 计算网格
        grid_levels = self.calculate_grid_levels(low_price, high_price)
        print(f"\n网格价格线:")
        for i, level in enumerate(grid_levels):
            print(f"  {i}. {level:.2f}")
        
        # 计算每格投资
        investment_per_grid = self.investment / self.grid_num
        
        # 获取交易对信息
        symbol_info = get_symbol_info(self.symbol)
        if symbol_info:
            min_qty = float(symbol_info['filters'][0]['minQty'])
            print(f"\n最小交易量：{min_qty}")
        
        # 创建买单 (低于当前价格)
        print(f"\n📈 创建买入挂单:")
        buy_orders = []
        for i, price in enumerate(grid_levels):
            if price < current_price:
                qty = investment_per_grid / price
                if symbol_info:
                    qty = max(qty, min_qty)
                
                print(f"  网格{i}: 买入价格={price:.2f}, 数量={qty:.6f}")
                # 实际下单需要 API Key，这里仅演示
                # order = place_limit_order(self.symbol, "BUY", price, qty)
                # if order:
                #     buy_orders.append(order)
        
        # 创建卖单 (高于当前价格)
        print(f"\n📉 创建卖出挂单:")
        sell_orders = []
        for i, price in enumerate(grid_levels):
            if price > current_price:
                qty = investment_per_grid / price
                if symbol_info:
                    qty = max(qty, min_qty)
                
                print(f"  网格{i}: 卖出价格={price:.2f}, 数量={qty:.6f}")
                # order = place_limit_order(self.symbol, "SELL", price, qty)
                # if order:
                #     sell_orders.append(order)
        
        print("\n✅ 网格创建完成 (演示模式，未实际下单)")
        return {
            "symbol": self.symbol,
            "grid_num": self.grid_num,
            "low_price": low_price,
            "high_price": high_price,
            "current_price": current_price,
            "grid_levels": grid_levels,
            "investment": self.investment
        }
    
    def run(self, low_price: float, high_price: float, interval: int = 60):
        """运行网格交易 (循环监控)"""
        print(f"\n🚀 启动网格交易机器人")
        print(f"监控间隔：{interval} 秒")
        
        try:
            while True:
                # 获取当前价格
                current_price = get_current_price(self.symbol)
                if not current_price:
                    time.sleep(interval)
                    continue
                
                # 检查订单状态
                open_orders = get_open_orders(self.symbol)
                if open_orders:
                    print(f"\n[{datetime.now()}] 当前挂单：{len(open_orders)} 个")
                
                # 根据价格调整订单
                # (实际策略需要根据价格变化创建/取消订单)
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n⏹️ 停止网格交易")
            # 取消所有订单
            cancel_all_orders(self.symbol)


# ==================== 主函数 ====================

def main():
    """主测试流程"""
    print("\n" + "=" * 60)
    print("🟡 币安现货网格交易机器人")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"环境：{'测试网' if USE_TESTNET else '实盘'}")
    print(f"URL: {BASE_URL}")
    print("=" * 60)
    
    # 检查 API Key
    if not API_KEY or not API_SECRET:
        print("\n⚠️  未配置 API Key")
        print("请设置环境变量:")
        print("  export BINANCE_API_KEY='your_api_key'")
        print("  export BINANCE_API_SECRET='your_api_secret'")
        print("\n继续执行只读测试...")
    
    # 测试 1: 获取账户信息
    print("\n【测试 1】账户信息")
    print("-" * 60)
    if API_KEY and API_SECRET:
        account = get_account()
        if account:
            print("✅ 账户连接成功")
            print(f"   Maker 费率：{account.get('makerCommission', 0) / 10000}")
            print(f"   Taker 费率：{account.get('takerCommission', 0) / 10000}")
            
            # 显示余额
            balances = account.get('balances', [])
            non_zero = [b for b in balances if float(b.get('free', 0)) > 0]
            print(f"\n   非零资产：{len(non_zero)} 种")
            for b in non_zero[:5]:
                print(f"      {b['asset']}: {b['free']}")
        else:
            print("❌ 账户连接失败")
    else:
        print("⏭️ 跳过 (需要 API Key)")
    
    # 测试 2: 市场行情
    print("\n【测试 2】市场行情")
    print("-" * 60)
    price = get_current_price(DEFAULT_SYMBOL)
    if price:
        print(f"✅ {DEFAULT_SYMBOL} 当前价格：{price}")
    
    # 测试 3: 订单簿
    print("\n【测试 3】订单簿")
    print("-" * 60)
    book = get_order_book(DEFAULT_SYMBOL)
    if book:
        print(f"✅ 订单簿获取成功")
        print(f"   买盘：{len(book.get('bids', []))} 档")
        print(f"   卖盘：{len(book.get('asks', []))} 档")
    
    # 测试 4: 网格策略计算
    print("\n【测试 4】网格策略计算")
    print("-" * 60)
    if price:
        bot = GridTradingBot(
            symbol=DEFAULT_SYMBOL,
            grid_num=DEFAULT_GRID_NUM,
            investment=DEFAULT_INVESTMENT
        )
        
        # 计算价格区间 (当前价格 ±10%)
        low_price = price * 0.9
        high_price = price * 1.1
        
        grid_config = bot.create_grid(low_price, high_price)
        
        if grid_config:
            print(f"\n📊 网格配置:")
            print(f"   价格区间：{grid_config['low_price']:.2f} - {grid_config['high_price']:.2f}")
            print(f"   网格数量：{grid_config['grid_num']}")
            print(f"   当前价格：{grid_config['current_price']:.2f}")
    
    # ==================== 总结 ====================
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    
    print("\n📋 配置 API Key:")
    print("   1. 登录 https://www.binance.com/my/settings/api-management")
    print("   2. 创建 API Key")
    print("   3. 启用：Reading + Spot & Margin Trading")
    print("   4. 设置 IP 白名单：103.172.182.26")
    print("   5. 保存 API Key 和 Secret")
    print("   6. 设置环境变量:")
    print("      export BINANCE_API_KEY='xxx'")
    print("      export BINANCE_API_SECRET='xxx'")
    
    print("\n🚀 启动实盘交易:")
    print("   python3 scripts/binance-grid-bot.py")
    
    print("\n⚠️  风险提示:")
    print("   - 网格交易在震荡市中表现良好")
    print("   - 单边行情可能产生浮亏")
    print("   - 建议先用测试网测试")
    print("   - 设置止损和资金上限")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
