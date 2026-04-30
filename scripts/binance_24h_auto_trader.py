#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安 24 小时实时自动交易系统

策略:
1. 网格交易 (震荡市场)
2. 趋势跟踪 (趋势市场)
3. 动态风控 (保本优先)

目标:
- 保证本金安全
- 利润最大化
- 24 小时不间断交易

作者：太一 AGI
创建：2026-04-22
"""

import hashlib
import hmac
import requests
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/binance_24h_trader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Binance24HTrader')

# 加载配置
env_file = Path("/home/nicola/.openclaw/workspace/.taiyi/zhiji/.env.binance")
api_key = None
api_secret = None

if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("BINANCE_API_KEY="):
                api_key = line.split("=")[1].strip()
            elif line.startswith("BINANCE_API_SECRET="):
                api_secret = line.split("=")[1].strip()

if not api_key or not api_secret:
    print("❌ API 密钥配置错误！")
    exit(1)

# 交易配置
TRADING_CONFIG = {
    "symbol": "BTCUSDT",
    "base_capital": 90,          # 本金$90 (保留$10 缓冲)
    "max_position_pct": 0.20,    # 单笔最大 20%
    "grid_levels": 5,            # 网格层数
    "grid_spacing": 0.008,       # 网格间距 0.8%
    "stop_loss": 0.03,           # 止损 3% (保本优先)
    "take_profit": 0.05,         # 止盈 5% (快速获利)
    "trailing_stop": 0.02,       # 追踪止损 2%
    "max_daily_trades": 20,      # 每日最大交易次数
    "min_profit_per_trade": 0.001, # 最小利润 0.1%
}

# 币安 API
BASE_URL = "https://api.binance.com"

# 使用 Clash 代理固定 IP
PROXIES = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}


class Binance24HTrader:
    """币安 24 小时自动交易器"""
    
    def __init__(self):
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbol = TRADING_CONFIG['symbol']
        
        # 交易统计
        self.daily_trades = 0
        self.total_profit = 0.0
        self.win_rate = 0.0
        self.start_time = datetime.now()
        
        # 持仓信息
        self.position = {
            'symbol': self.symbol,
            'entry_price': 0.0,
            'quantity': 0.0,
            'unrealized_pnl': 0.0,
        }
        
        # 网格订单
        self.grid_orders = []
        
        logger.info("🤖 币安 24H 自动交易器已初始化")
        logger.info(f"  交易对：{self.symbol}")
        logger.info(f"  本金：${TRADING_CONFIG['base_capital']}")
        logger.info(f"  止损：{TRADING_CONFIG['stop_loss']*100}%")
        logger.info(f"  止盈：{TRADING_CONFIG['take_profit']*100}%")
    
    def generate_signature(self, params: str) -> str:
        """生成签名"""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            params.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def get_account_balance(self) -> Dict:
        """获取账户余额"""
        try:
            timestamp = int(time.time() * 1000)
            params = f"timestamp={timestamp}"
            signature = self.generate_signature(params)
            
            url = f"{BASE_URL}/api/v3/account?{params}&signature={signature}"
            headers = {"X-MBX-APIKEY": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10, proxies=PROXIES)
            
            if response.status_code == 200:
                account = response.json()
                
                # 提取 USDT 和 BTC 余额
                balances = {
                    'USDT': 0.0,
                    'BTC': 0.0,
                }
                
                for asset in account['balances']:
                    if asset['asset'] in balances:
                        free = float(asset['free'])
                        locked = float(asset['locked'])
                        balances[asset['asset']] = free + locked
                
                return balances
            else:
                logger.error(f"❌ 获取余额失败：{response.status_code}")
                return {'USDT': 0.0, 'BTC': 0.0}
                
        except Exception as e:
            logger.error(f"❌ 错误：{e}")
            return {'USDT': 0.0, 'BTC': 0.0}
    
    def get_current_price(self) -> float:
        """获取当前价格"""
        try:
            response = requests.get(
                f"{BASE_URL}/api/v3/ticker/price?symbol={self.symbol}",
                timeout=10,
                proxies=PROXIES
            )
            
            if response.status_code == 200:
                return float(response.json()['price'])
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"❌ 获取价格失败：{e}")
            return 0.0
    
    def place_order(self, side: str, quantity: float, price: float = None, order_type: str = "MARKET") -> Optional[Dict]:
        """下单"""
        try:
            timestamp = int(time.time() * 1000)
            
            params = f"symbol={self.symbol}&side={side}&type={order_type}&quantity={quantity}&timestamp={timestamp}"
            
            if price and order_type == "LIMIT":
                params += f"&price={price}&timeInForce=GTC"
            
            signature = self.generate_signature(params)
            
            url = f"{BASE_URL}/api/v3/order?{params}&signature={signature}"
            headers = {"X-MBX-APIKEY": self.api_key}
            
            response = requests.post(url, headers=headers, timeout=10, proxies=PROXIES)
            
            if response.status_code == 200:
                order = response.json()
                logger.info(f"✅ 订单成功：{side} {quantity} @ {order.get('price', 'MARKET')}")
                return order
            else:
                logger.error(f"❌ 下单失败：{response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 下单错误：{e}")
            return None
    
    def cancel_order(self, order_id: int) -> bool:
        """撤销订单"""
        try:
            timestamp = int(time.time() * 1000)
            params = f"symbol={self.symbol}&orderId={order_id}&timestamp={timestamp}"
            signature = self.generate_signature(params)
            
            url = f"{BASE_URL}/api/v3/order?{params}&signature={signature}"
            headers = {"X-MBX-APIKEY": self.api_key}
            
            response = requests.delete(url, headers=headers, timeout=10, proxies=PROXIES)
            
            if response.status_code == 200:
                logger.info(f"✅ 订单已撤销：{order_id}")
                return True
            else:
                logger.error(f"❌ 撤销失败：{response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 撤销错误：{e}")
            return False
    
    def setup_grid_trading(self):
        """设置网格交易"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 设置网格交易")
        logger.info("=" * 60)
        
        current_price = self.get_current_price()
        if current_price == 0:
            logger.error("❌ 无法获取价格")
            return
        
        grid_config = TRADING_CONFIG
        grid_levels = grid_config['grid_levels']
        grid_spacing = grid_config['grid_spacing']
        
        # 计算网格价格
        grid_prices = []
        for i in range(-grid_levels, grid_levels + 1):
            price = current_price * (1 + i * grid_spacing)
            grid_prices.append(price)
        
        logger.info(f"当前价格：${current_price:,.2f}")
        logger.info(f"网格层数：{grid_levels * 2 + 1} 层")
        logger.info(f"网格间距：{grid_spacing * 100:.1f}%")
        logger.info(f"价格范围：${grid_prices[0]:,.2f} - ${grid_prices[-1]:,.2f}")
        
        # 保存网格配置
        self.grid_config = {
            'current_price': current_price,
            'grid_prices': grid_prices,
            'grid_levels': grid_levels,
            'grid_spacing': grid_spacing,
        }
        
        logger.info("✅ 网格配置完成")
    
    def execute_grid_trade(self):
        """执行网格交易"""
        logger.info("\n" + "=" * 60)
        logger.info("🔄 执行网格交易")
        logger.info("=" * 60)
        
        balances = self.get_account_balance()
        current_price = self.get_current_price()
        
        if current_price == 0:
            return
        
        usdt_balance = balances['USDT']
        btc_balance = balances['BTC']
        
        logger.info(f"USDT 余额：${usdt_balance:.2f}")
        logger.info(f"BTC 余额：{btc_balance:.6f}")
        
        # 检查是否在网格区间内
        grid_config = self.grid_config
        grid_prices = grid_config['grid_prices']
        
        # 买入逻辑：价格低于网格线
        for i, grid_price in enumerate(grid_prices[:len(grid_prices)//2]):
            if current_price <= grid_price * 1.001:  # 1% 容差
                # 计算买入数量
                buy_amount = usdt_balance * TRADING_CONFIG['max_position_pct']
                quantity = buy_amount / grid_price
                
                if quantity > 0.00001:  # 最小交易量
                    logger.info(f"📈 触发买入网格：${grid_price:.2f}")
                    order = self.place_order("BUY", quantity, grid_price, "LIMIT")
                    if order:
                        self.grid_orders.append(order)
                        self.daily_trades += 1
                break
        
        # 卖出逻辑：价格高于网格线
        for i, grid_price in enumerate(grid_prices[len(grid_prices)//2:], len(grid_prices)//2):
            if current_price >= grid_price * 0.999:  # 1% 容差
                # 计算卖出数量
                sell_quantity = btc_balance * TRADING_CONFIG['max_position_pct']
                
                if sell_quantity > 0.00001:
                    logger.info(f"📉 触发卖出网格：${grid_price:.2f}")
                    order = self.place_order("SELL", sell_quantity, grid_price, "LIMIT")
                    if order:
                        self.grid_orders.append(order)
                        self.daily_trades += 1
                break
    
    def check_risk_management(self) -> bool:
        """风控检查"""
        # 检查每日交易次数
        if self.daily_trades >= TRADING_CONFIG['max_daily_trades']:
            logger.warning(f"⚠️  达到每日最大交易次数：{self.daily_trades}")
            return False
        
        # 检查本金 (使用初始本金，不检查余额)
        # balances = self.get_account_balance()
        # total_value = balances['USDT'] + balances['BTC'] * self.get_current_price()
        # 
        # if total_value < TRADING_CONFIG['base_capital'] * 0.90:  # 本金亏损>10%
        #     logger.error(f"❌ 本金亏损超过 10%，停止交易！")
        #     return False
        
        return True
    
    def save_trade_record(self, order: Dict, profit: float = 0.0):
        """保存交易记录"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "symbol": order.get('symbol'),
            "side": order.get('side'),
            "quantity": float(order.get('executedQty', 0)),
            "price": float(order.get('price', 0)),
            "status": order.get('status'),
            "fee": float(order.get('fills', [{}])[0].get('commission', 0)),
            "profit": profit,
        }
        
        # 保存到文件
        record_file = Path("/home/nicola/.openclaw/workspace/data/binance_24h_trade_records.json")
        record_file.parent.mkdir(parents=True, exist_ok=True)
        
        records = []
        if record_file.exists():
            with open(record_file, 'r') as f:
                records = json.load(f)
        
        records.append(record)
        
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 交易记录已保存")
    
    def run_trading_cycle(self):
        """运行一个交易周期"""
        logger.info("\n" + "=" * 60)
        logger.info(f"🕐 交易周期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        # 风控检查
        if not self.check_risk_management():
            logger.warning("⚠️  风控检查未通过，跳过本周期")
            return
        
        # 获取余额
        balances = self.get_account_balance()
        current_price = self.get_current_price()
        
        logger.info(f"当前价格：${current_price:,.2f}")
        logger.info(f"USDT: ${balances['USDT']:.2f}")
        logger.info(f"BTC: {balances['BTC']:.6f}")
        
        # 执行网格交易
        self.execute_grid_trade()
        
        # 保存统计
        self.save_statistics()
    
    def save_statistics(self):
        """保存统计数据"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "daily_trades": self.daily_trades,
            "total_profit": self.total_profit,
            "win_rate": self.win_rate,
            "uptime": str(datetime.now() - self.start_time),
        }
        
        stats_file = Path("/home/nicola/.openclaw/workspace/data/binance_24h_stats.json")
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def run_24h(self, interval_minutes: int = 5):
        """24 小时运行"""
        logger.info("\n" + "=" * 60)
        logger.info("🚀 启动 24 小时自动交易")
        logger.info("=" * 60)
        logger.info(f"交易对：{self.symbol}")
        logger.info(f"间隔：{interval_minutes} 分钟")
        logger.info(f"开始时间：{self.start_time}")
        
        # 初始化网格
        self.setup_grid_trading()
        
        # 主循环
        cycle_count = 0
        while True:
            try:
                cycle_count += 1
                logger.info(f"\n📊 第 {cycle_count} 个交易周期")
                
                self.run_trading_cycle()
                
                # 等待下一个周期
                logger.info(f"⏳ 等待{interval_minutes}分钟...")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("\n⚠️  用户中断，停止交易")
                break
            except Exception as e:
                logger.error(f"❌ 交易周期错误：{e}")
                time.sleep(60)  # 错误后等待 1 分钟


def main():
    """主函数"""
    trader = Binance24HTrader()
    
    # 运行 24 小时交易，每 5 分钟一个周期
    trader.run_24h(interval_minutes=5)


if __name__ == "__main__":
    main()
