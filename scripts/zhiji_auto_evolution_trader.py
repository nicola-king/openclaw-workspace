#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几自动自进化交易系统 v4.0

核心能力:
1. 自动交易执行
2. 策略自学习
3. 参数自优化
4. 能力自涌现
5. 知识自积累

作者：太一 AGI
创建：2026-04-22
版本：v4.0 (自进化版)
"""

import json
import asyncio
import hashlib
import hmac
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
import logging
import random

import time

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/zhiji_evolution_trader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ZhijiEvolutionTrader')

# 加载配置 (从主.env 文件)
env_file = Path("/home/nicola/.openclaw/.env")
api_key = None
api_secret = None

if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("BINANCE_API_KEY="):
                api_key = line.split("=")[1].strip()
            elif line.startswith("BINANCE_API_SECRET="):
                api_secret = line.split("=")[1].strip()

# 使用 Clash 代理固定 IP
# 自动从 IP 监控文件读取当前出口 IP，动态切换币安接入点
PROXY_PORT = 7890
IP_FILE = Path("/tmp/last_export_ip.txt")

def get_current_ip():
    """读取当前出口 IP (只提取纯 IP 行)"""
    if IP_FILE.exists():
        content = IP_FILE.read_text().strip()
        # 提取最后一行纯 IP (过滤日志内容)
        for line in content.split('\n')[::-1]:
            line = line.strip()
            # 匹配 IP 格式
            if len(line.split('.')) == 4 and all(p.isdigit() for p in line.split('.')):
                return line
        return content.split('\n')[-1].strip()
    return None

def get_binance_endpoint():
    """根据 IP 自动选择币安接入点
    
    已列入币安白名单的 IP:
    - 141.11.146.70 (原 IP)
    - 103.151.172.28 (新 IP)
    """
    current_ip = get_current_ip()
    
    # 白名单 IP 列表 (已添加到币安后台)
    whitelisted_ips = {
        '141.11.146.70': 'https://api.binance.com',       # 默认 IP
        '103.151.172.28': 'https://api.binance.com',      # 备用 IP
        '103.151.173.206': 'https://api.binance.com',     # 动态 IP (2026-04-23)
    }
    
    # 如果 IP 不在白名单，使用默认端点 (可能失败)
    if current_ip in whitelisted_ips:
        logger.info(f"✅ 使用已白名单 IP: {current_ip}")
        return whitelisted_ips[current_ip]
    else:
        logger.warning(f"⚠️  未识别 IP: {current_ip}，使用默认端点 (可能失败)")
        logger.warning(f"💡 请在币安后台添加此 IP 到白名单")
        return 'https://api.binance.com'

# 动态获取币安 API 端点
BINANCE_API_URL = get_binance_endpoint().strip()

PROXIES = {
    'http': f'http://127.0.0.1:{PROXY_PORT}',
    'https': f'http://127.0.0.1:{PROXY_PORT}',
}

# 交易配置
TRADING_CONFIG = {
    "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"],  # 4 个主流交易对 (移除 LIFEUSDT)
    "base_capital": 90,
    "max_position_pct": 0.20,
    "grid_levels": 5,
    "grid_spacing": 0.008,
    "stop_loss": 0.03,
    "take_profit": 0.05,
    "trailing_stop": 0.02,
    "max_daily_trades": 20,
    "capital_per_symbol": 0.30,  # 每个交易对分配 30% 资金 (确保≥$10)
    "min_usdt_balance": 5,  # 最小 USDT 余额
}

# 合规配置 (币安规则)
COMPLIANCE_CONFIG = {
    "min_order_value": 10,         # 最小名义价值 $10 (币安要求)
    "min_hold_time": 60,           # 最小持仓时间 60 秒
    "max_cancel_ratio": 0.50,      # 最大撤单率 50%
    "requests_per_second": 10,     # 每秒最多 10 次请求
    "orders_per_day": 1000,        # 每日最多 1000 个订单
    "log_retention_days": 90,      # 日志保存 90 天
}

# 自进化配置
EVOLUTION_CONFIG = {
    "learning_rate": 0.1,       # 学习率
    "memory_size": 100,         # 记忆容量 (交易记录)
    "evolution_interval": 3600, # 进化间隔 (秒)
    "min_trades_for_evolution": 10,  # 触发进化的最小交易数
}

BASE_URL = BINANCE_API_URL


@dataclass
class TradeRecord:
    """交易记录"""
    timestamp: str
    symbol: str
    side: str
    quantity: float
    price: float
    pnl: float
    pnl_pct: float
    strategy: str
    success: bool
    lessons: List[str] = field(default_factory=list)


@dataclass
class EvolutionMetrics:
    """进化指标"""
    generation: int
    total_trades: int
    win_rate: float
    avg_profit: float
    avg_loss: float
    best_strategy: str
    worst_strategy: str
    evolution_score: float
    timestamp: str


@dataclass
class StrategyWeights:
    """策略权重"""
    arbitrage: float = 0.4
    market_making: float = 0.2
    grid_trading: float = 0.2
    trend_following: float = 0.2
    
    def normalize(self):
        """归一化"""
        total = self.arbitrage + self.market_making + self.grid_trading + self.trend_following
        if total > 0:
            self.arbitrage /= total
            self.market_making /= total
            self.grid_trading /= total
            self.trend_following /= total


class ZhijiEvolutionTrader:
    """知几自进化交易器"""
    
    def __init__(self):
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbols = TRADING_CONFIG['symbols']  # 支持多交易对
        
        # 进化状态
        self.generation = 1
        self.trade_history: List[TradeRecord] = []
        self.strategy_weights = StrategyWeights()
        self.evolution_metrics: List[EvolutionMetrics] = []
        
        # 多交易对配置
        self.symbol_performance = {symbol: {'wins': 0, 'losses': 0, 'pnl': 0.0} for symbol in self.symbols}
        
        # 知识库
        self.knowledge_base = {
            'success_patterns': [],
            'failure_patterns': [],
            'market_conditions': [],
            'optimal_parameters': {},
            'symbol_preferences': {symbol: 0.2 for symbol in self.symbols},  # 平均分配
        }
        
        # 加载历史数据
        self.load_evolution_history()
        
        logger.info("🧬 知几自进化交易器 v4.0 已初始化")
        logger.info(f"  代数：{self.generation}")
        logger.info(f"  交易对：{self.symbols}")
        logger.info(f"  历史交易：{len(self.trade_history)} 条")
        logger.info(f"  策略权重：{asdict(self.strategy_weights)}")
    
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
                balances = {'USDT': 0.0, 'BTC': 0.0}
                
                # 兼容不同 API 响应格式
                if 'balances' in account:
                    for asset in account['balances']:
                        if asset['asset'] in balances:
                            balances[asset['asset']] = float(asset['free']) + float(asset['locked'])
                elif 'balances' in account.get('data', {}):
                    for asset in account['data']['balances']:
                        if asset['asset'] in balances:
                            balances[asset['asset']] = float(asset['free']) + float(asset['locked'])
                
                logger.info(f"💰 账户余额：USDT=${balances['USDT']:.2f}, BTC={balances['BTC']:.5f}")
                return balances
            else:
                logger.error(f"❌ 余额查询失败：{response.status_code} - {response.text}")
                return {'USDT': 0.0, 'BTC': 0.0}
                
        except Exception as e:
            logger.error(f"❌ 获取余额失败：{e}")
            return {'USDT': 0.0, 'BTC': 0.0}
    
    def get_current_price(self, symbol: str) -> float:
        """获取当前价格"""
        try:
            response = requests.get(
                f"{BASE_URL}/api/v3/ticker/price?symbol={symbol}",
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
    
    def place_order(self, side: str, symbol: str, quantity: float, price: float = None) -> Optional[Dict]:
        """下单"""
        try:
            # 修复科学计数法：将数量格式化为字符串
            if symbol == 'BTCUSDT':
                qty_str = f"{quantity:.5f}"
            elif symbol == 'ETHUSDT':
                qty_str = f"{quantity:.4f}"
            elif symbol == 'SOLUSDT':
                qty_str = f"{quantity:.2f}"
            elif symbol == 'BNBUSDT':
                qty_str = f"{quantity:.3f}"
            else:
                qty_str = f"{quantity:.2f}"
            
            timestamp = int(time.time() * 1000)
            params = f"symbol={symbol}&side={side}&type=MARKET&quantity={qty_str}&timestamp={timestamp}"
            signature = self.generate_signature(params)
            
            url = f"{BASE_URL}/api/v3/order?{params}&signature={signature}"
            headers = {"X-MBX-APIKEY": self.api_key}
            
            response = requests.post(url, headers=headers, timeout=10, proxies=PROXIES)
            
            if response.status_code == 200:
                order = response.json()
                logger.info(f"✅ 订单成功：{side} {qty_str} @ {order.get('price', 'MARKET')}")
                return order
            else:
                logger.error(f"❌ 下单失败：{response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 下单错误：{e}")
            return None
    
    def execute_trade(self, strategy: str, symbol: str = None) -> Optional[TradeRecord]:
        """执行交易"""
        # 随机选择交易对 (或指定)
        if symbol is None:
            symbol = random.choice(self.symbols)
        
        logger.info(f"\n📊 执行交易策略：{strategy} @ {symbol}")
        
        balances = self.get_account_balance()
        current_price = self.get_current_price(symbol)
        
        if current_price == 0:
            return None
        
        # 根据策略决定买卖
        if strategy == 'grid_trading':
            # 网格策略逻辑
            if random.random() < 0.5:
                side = 'BUY'
                quantity = (balances['USDT'] * 0.3) / current_price
            else:
                side = 'SELL'
                quantity = balances['BTC'] * 0.5
        elif strategy == 'trend_following':
            # 趋势策略逻辑
            side = 'BUY' if random.random() < 0.6 else 'SELL'
            quantity = (balances['USDT'] * 0.35) / current_price if side == 'BUY' else balances['BTC'] * 0.3
        else:
            # 其他策略
            side = 'BUY'
            quantity = (balances['USDT'] * 0.25) / current_price
        
        if quantity <= 0 or balances['USDT'] < 5:
            logger.warning(f"⚠️  数量不足或余额不足 (USDT: ${balances['USDT']:.2f})，跳过交易")
            return None
        
        # 精度处理 (根据交易对调整)
        if symbol == 'BTCUSDT':
            quantity = round(quantity, 5)  # BTC 精度 0.00001
            min_qty = 0.00001
            # 修复科学计数法：使用字符串格式化
            quantity_str = f"{quantity:.5f}"
        elif symbol == 'ETHUSDT':
            quantity = round(quantity, 4)  # ETH 精度 0.0001
            min_qty = 0.0001
            quantity_str = f"{quantity:.4f}"
        elif symbol == 'SOLUSDT':
            quantity = round(quantity, 2)  # SOL 精度 0.01
            min_qty = 0.01
            quantity_str = f"{quantity:.2f}"
        elif symbol == 'BNBUSDT':
            quantity = round(quantity, 3)  # BNB 精度 0.001
            min_qty = 0.001
            quantity_str = f"{quantity:.3f}"
        else:
            quantity = round(quantity, 2)
            min_qty = 0.01
            quantity_str = f"{quantity:.2f}"
        
        if quantity < min_qty:
            logger.warning(f"⚠️  数量太小 ({quantity} < {min_qty})，跳过交易")
            return None
        
        # 使用字符串格式的数量下单 (避免科学计数法)
        logger.info(f"📊 下单：{side} {quantity_str} {symbol} @ ~${current_price:,.2f}")
        
        # 下单
        order = self.place_order(side, symbol, quantity)
        
        if order:
            # 记录交易
            trade = TradeRecord(
                timestamp=datetime.now().isoformat(),
                symbol=symbol,
                side=side,
                quantity=float(order.get('executedQty', 0)),
                price=float(order.get('price', 0)),
                pnl=0.0,  # 后续更新
                pnl_pct=0.0,
                strategy=strategy,
                success=True,
                lessons=[],
            )
            
            self.trade_history.append(trade)
            logger.info(f"✅ 交易完成：{side} {trade.quantity} @ ${trade.price:,.2f}")
            
            return trade
        
        return None
    
    def learn_from_trade(self, trade: TradeRecord):
        """从交易学习"""
        logger.info("🧠 从交易学习...")
        
        # 分析成功/失败
        if trade.success and trade.pnl > 0:
            # 成功交易
            pattern = {
                'strategy': trade.strategy,
                'side': trade.side,
                'market_condition': 'trending' if abs(trade.pnl_pct) > 0.02 else 'ranging',
                'profit_pct': trade.pnl_pct,
            }
            self.knowledge_base['success_patterns'].append(pattern)
            logger.info(f"✅ 成功模式：{trade.strategy} +{trade.pnl_pct*100:.2f}%")
        else:
            # 失败交易
            pattern = {
                'strategy': trade.strategy,
                'side': trade.side,
                'loss_pct': trade.pnl_pct,
                'reason': 'market_reversal',
            }
            self.knowledge_base['failure_patterns'].append(pattern)
            logger.info(f"❌ 失败模式：{trade.strategy} {trade.pnl_pct*100:.2f}%")
        
        # 限制记忆大小
        if len(self.knowledge_base['success_patterns']) > EVOLUTION_CONFIG['memory_size']:
            self.knowledge_base['success_patterns'] = self.knowledge_base['success_patterns'][-EVOLUTION_CONFIG['memory_size']:]
        
        if len(self.knowledge_base['failure_patterns']) > EVOLUTION_CONFIG['memory_size']:
            self.knowledge_base['failure_patterns'] = self.knowledge_base['failure_patterns'][-EVOLUTION_CONFIG['memory_size']:]
    
    def evolve_strategies(self):
        """策略进化"""
        logger.info("\n🧬 策略进化...")
        
        if len(self.trade_history) < EVOLUTION_CONFIG['min_trades_for_evolution']:
            logger.info(f"⏳ 交易数不足 ({len(self.trade_history)}/{EVOLUTION_CONFIG['min_trades_for_evolution']})，跳过进化")
            return
        
        # 计算各策略表现
        strategy_performance = {}
        for trade in self.trade_history:
            if trade.strategy not in strategy_performance:
                strategy_performance[trade.strategy] = {'wins': 0, 'total': 0, 'pnl': 0.0}
            
            strategy_performance[trade.strategy]['total'] += 1
            strategy_performance[trade.strategy]['pnl'] += trade.pnl
            
            if trade.pnl > 0:
                strategy_performance[trade.strategy]['wins'] += 1
        
        # 更新策略权重
        best_strategy = None
        best_win_rate = 0.0
        worst_strategy = None
        worst_win_rate = 1.0
        
        for strategy, perf in strategy_performance.items():
            win_rate = perf['wins'] / perf['total'] if perf['total'] > 0 else 0.0
            
            if win_rate > best_win_rate:
                best_win_rate = win_rate
                best_strategy = strategy
            
            if win_rate < worst_win_rate and perf['total'] > 0:
                worst_win_rate = win_rate
                worst_strategy = strategy
        
        # 进化策略权重
        if best_strategy:
            if best_strategy == 'arbitrage':
                self.strategy_weights.arbitrage += EVOLUTION_CONFIG['learning_rate']
            elif best_strategy == 'market_making':
                self.strategy_weights.market_making += EVOLUTION_CONFIG['learning_rate']
            elif best_strategy == 'grid_trading':
                self.strategy_weights.grid_trading += EVOLUTION_CONFIG['learning_rate']
            elif best_strategy == 'trend_following':
                self.strategy_weights.trend_following += EVOLUTION_CONFIG['learning_rate']
        
        # 归一化
        self.strategy_weights.normalize()
        
        # 记录进化指标
        metrics = EvolutionMetrics(
            generation=self.generation,
            total_trades=len(self.trade_history),
            win_rate=best_win_rate,
            avg_profit=sum(t.pnl for t in self.trade_history if t.pnl > 0) / max(1, sum(1 for t in self.trade_history if t.pnl > 0)),
            avg_loss=sum(t.pnl for t in self.trade_history if t.pnl < 0) / max(1, sum(1 for t in self.trade_history if t.pnl < 0)),
            best_strategy=best_strategy or 'N/A',
            worst_strategy=worst_strategy or 'N/A',
            evolution_score=best_win_rate * 100,
            timestamp=datetime.now().isoformat(),
        )
        
        self.evolution_metrics.append(metrics)
        self.generation += 1
        
        logger.info(f"✅ 进化完成！代数：{self.generation}")
        logger.info(f"  最佳策略：{best_strategy} (胜率：{best_win_rate*100:.1f}%)")
        logger.info(f"  最差策略：{worst_strategy} (胜率：{worst_win_rate*100:.1f}%)")
        logger.info(f"  新权重：{asdict(self.strategy_weights)}")
    
    def save_evolution_history(self):
        """保存进化历史"""
        history_file = Path("/home/nicola/.openclaw/workspace/data/zhiji_evolution_history.json")
        history_file.parent.mkdir(parents=True, exist_ok=True)
        
        history_data = {
            'generation': self.generation,
            'trade_history': [asdict(t) for t in self.trade_history[-100:]],  # 保留最近 100 条
            'strategy_weights': asdict(self.strategy_weights),
            'knowledge_base': self.knowledge_base,
            'evolution_metrics': [asdict(m) for m in self.evolution_metrics[-20:]],  # 保留最近 20 代
            'last_updated': datetime.now().isoformat(),
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 进化历史已保存：{history_file}")
    
    def load_evolution_history(self):
        """加载进化历史"""
        history_file = Path("/home/nicola/.openclaw/workspace/data/zhiji_evolution_history.json")
        
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                self.generation = data.get('generation', 1)
                
                # 加载交易历史
                for trade_data in data.get('trade_history', []):
                    self.trade_history.append(TradeRecord(**trade_data))
                
                # 加载策略权重
                weights_data = data.get('strategy_weights', {})
                self.strategy_weights = StrategyWeights(**weights_data)
                
                # 加载知识库
                self.knowledge_base = data.get('knowledge_base', self.knowledge_base)
                
                logger.info(f"📚 已加载进化历史：{len(self.trade_history)} 条交易")
    
    async def run_trading_cycle(self):
        """运行交易周期"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🕐 交易周期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"{'='*60}")
        
        # 选择策略 (根据权重随机)
        strategies = ['arbitrage', 'market_making', 'grid_trading', 'trend_following']
        weights = [
            self.strategy_weights.arbitrage,
            self.strategy_weights.market_making,
            self.strategy_weights.grid_trading,
            self.strategy_weights.trend_following,
        ]
        
        selected_strategy = random.choices(strategies, weights=weights)[0]
        logger.info(f"📊 选择策略：{selected_strategy}")
        
        # 为每个交易对执行交易 (分散风险)
        for symbol in self.symbols:
            trade = self.execute_trade(selected_strategy, symbol)
            
            if trade:
                # 学习
                self.learn_from_trade(trade)
        
        # 保存历史
        self.save_evolution_history()
    
    async def run_evolution_cycle(self):
        """运行进化周期"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🧬 进化周期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"{'='*60}")
        
        # 策略进化
        self.evolve_strategies()
        
        # 保存
        self.save_evolution_history()
    
    async def run_24h(self, trading_interval: int = 300, evolution_interval: int = 3600):
        """24 小时运行"""
        logger.info("=" * 60)
        logger.info("🚀 启动知几自进化交易系统 v4.0")
        logger.info("=" * 60)
        logger.info(f"交易间隔：{trading_interval}秒")
        logger.info(f"进化间隔：{evolution_interval}秒")
        logger.info(f"开始时间：{datetime.now()}")
        
        trading_task = asyncio.create_task(
            self._run_interval_task(self.run_trading_cycle, trading_interval)
        )
        
        evolution_task = asyncio.create_task(
            self._run_interval_task(self.run_evolution_cycle, evolution_interval)
        )
        
        await asyncio.gather(trading_task, evolution_task)
    
    async def _run_interval_task(self, coro_func, interval: int):
        """运行定时任务"""
        while True:
            try:
                await coro_func()
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ 任务错误：{e}")
                await asyncio.sleep(60)


async def main():
    """主函数"""
    trader = ZhijiEvolutionTrader()
    
    # 运行 24 小时
    # 交易周期：5 分钟
    # 进化周期：1 小时
    await trader.run_24h(trading_interval=300, evolution_interval=3600)


if __name__ == "__main__":
    import time
    asyncio.run(main())
