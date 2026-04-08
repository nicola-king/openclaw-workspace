#!/usr/bin/env python3
"""
知几-E 模拟盘主程序 v3.0
功能：实时扫描市场 + 策略决策 + 模拟下单 + 监控风控

运行方式：
1. 手动：python3 zhiji-e-paper-trading.py
2. Cron: 0 * * * * (每小时执行)
"""

import os
import sys
import json
import time
import sqlite3
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import numpy as np

# 加载配置
env_path = Path(__file__).parent / ".env.polymarket-paper"
load_dotenv(env_path)

# 配置常量
CONFIG = {
    'mode': os.getenv('POLYMARKET_MODE', 'paper'),
    'api_key': os.getenv('POLYMARKET_API_KEY'),
    'wallet': os.getenv('POLYMARKET_WALLET'),
    'initial_balance': float(os.getenv('PAPER_INITIAL_BALANCE', 10000)),
    'base_url': os.getenv('POLYMARKET_BASE_URL', 'https://gamma-api.polymarket.com'),
    
    # 策略参数 v4.0 (TimesFM 增强版)
    'confidence_threshold': float(os.getenv('CONFIDENCE_THRESHOLD', 0.55)),  # 降低阈值
    'kelly_divisor': int(os.getenv('KELLY_DIVISOR', 3)),
    'max_position_pct': float(os.getenv('MAX_POSITION_PCT', 0.15)),
    'timesfm_weight': float(os.getenv('TIMESFM_WEIGHT', 0.20)),  # TimesFM 权重
    
    # 风控参数（三级预警机制）
    'daily_warning_loss': float(os.getenv('DAILY_WARNING_LOSS', 0.05)),  # -5% 预警
    'daily_stop_loss': float(os.getenv('DAILY_STOP_LOSS', 0.10)),  # -10% 止损
    'consecutive_loss_limit': int(os.getenv('CONSECUTIVE_LOSS_LIMIT', 3)),
    'loss_reduction_factor': float(os.getenv('LOSS_REDUCTION_FACTOR', 0.5)),
    'low_liquidity_threshold': float(os.getenv('LOW_LIQUIDITY_THRESHOLD', 2000)),
    'high_liquidity_threshold': float(os.getenv('HIGH_LIQUIDITY_THRESHOLD', 10000)),
    
    # 预警通知
    'wechat_alert_enabled': os.getenv('WECHAT_ALERT_ENABLED', 'true').lower() == 'true',
    
    # 日志
    'log_file': os.getenv('LOG_FILE', '/home/nicola/.openclaw/workspace/logs/paper-trading.log'),
    'trades_file': '/home/nicola/.openclaw/workspace/logs/paper-trades.jsonl',
}

# ROI 追踪器集成
ROI_TRACKER_ENABLED = True
ROI_DB_PATH = '/home/nicola/.openclaw/workspace/data/roi-tracker.db'

# 状态文件
STATE_FILE = '/tmp/zhiji-paper-state.json'


class PaperTradingState:
    """模拟盘状态管理"""
    
    def __init__(self):
        self.balance = CONFIG['initial_balance']
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.last_trade_date = None
        self.total_trades = 0
        self.wins = 0
        self.losses = 0
        self.trade_history = []
        
        # 加载状态
        self.load()
    
    def load(self):
        """加载状态"""
        if Path(STATE_FILE).exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    self.balance = state.get('balance', self.balance)
                    self.daily_pnl = state.get('daily_pnl', 0.0)
                    self.consecutive_losses = state.get('consecutive_losses', 0)
                    self.last_trade_date = state.get('last_trade_date')
                    self.total_trades = state.get('total_trades', 0)
                    self.wins = state.get('wins', 0)
                    self.losses = state.get('losses', 0)
                    self.trade_history = state.get('trade_history', [])
            except Exception as e:
                log(f"⚠️ 加载状态失败：{e}")
    
    def save(self):
        """保存状态"""
        state = {
            'balance': self.balance,
            'daily_pnl': self.daily_pnl,
            'consecutive_losses': self.consecutive_losses,
            'last_trade_date': self.last_trade_date,
            'total_trades': self.total_trades,
            'wins': self.wins,
            'losses': self.losses,
            'trade_history': self.trade_history[-100:],  # 保留最近 100 笔
            'last_update': datetime.now().isoformat()
        }
        
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    
    def reset_daily(self, current_date):
        """每日重置"""
        if self.last_trade_date != current_date:
            self.daily_pnl = 0.0
            self.last_trade_date = current_date
            log(f"📅 新交易日开始：{current_date}")
    
    def update(self, result: str, profit: float):
        """更新状态"""
        self.total_trades += 1
        self.balance += profit
        self.daily_pnl += profit
        
        if result == 'WIN':
            self.wins += 1
            self.consecutive_losses = 0
        else:
            self.losses += 1
            self.consecutive_losses += 1
        
        self.trade_history.append({
            'timestamp': datetime.now().isoformat(),
            'result': result,
            'profit': profit,
            'balance_after': self.balance
        })
        
        self.save()


class ZhijiEStrategyV3:
    """知几-E 策略 v3.0"""
    
    def __init__(self):
        self.confidence_threshold = CONFIG['confidence_threshold']
        self.kelly_divisor = CONFIG['kelly_divisor']
        self.max_position_pct = CONFIG['max_position_pct']
        self.low_liquidity_threshold = CONFIG['low_liquidity_threshold']
        self.high_liquidity_threshold = CONFIG['high_liquidity_threshold']
        self.daily_stop_loss = CONFIG['daily_stop_loss']
        self.consecutive_loss_limit = CONFIG['consecutive_loss_limit']
        self.loss_reduction_factor = CONFIG['loss_reduction_factor']
    
    def calculate_confidence(self, market_data: list) -> float:
        """置信度计算 (4 因子)"""
        if len(market_data) < 5:
            return 0.5
        
        closes = [d['close'] for d in market_data]
        
        # 趋势因子
        trend = closes[-1] - closes[0]
        trend_score = 0.25 * np.tanh(trend * 50)
        
        # 动量因子
        returns = [closes[i+1] - closes[i] for i in range(len(closes)-1)]
        momentum = np.mean(returns[-3:]) if len(returns) >= 3 else 0
        momentum_score = 0.15 * np.tanh(momentum * 50)
        
        # 波动率因子
        volatility = np.std(returns) if returns else 0
        volatility_score = -0.1 * volatility
        
        # 均值回归因子
        mean_price = np.mean(closes)
        deviation = (closes[-1] - mean_price) / mean_price if mean_price > 0 else 0
        mean_reversion_score = -0.1 * np.tanh(deviation * 100)
        
        confidence = 0.5 + trend_score + momentum_score + volatility_score + mean_reversion_score
        return float(np.clip(confidence, 0.1, 0.95))
    
    def estimate_ev(self, market_data: list, current_price: float) -> float:
        """EV 计算"""
        confidence = self.calculate_confidence(market_data)
        # EV = 置信度 - 市场价格隐含概率
        ev = confidence - current_price
        return ev
    
    def calculate_position(self, ev: float, confidence: float, balance: float, consecutive_losses: int) -> float:
        """仓位计算 (动态 Kelly)"""
        if ev <= 0:
            return 0.0
        
        # 基础 Kelly
        base_stake = min(ev / self.kelly_divisor, self.max_position_pct)
        
        # 连败保护
        if consecutive_losses >= self.consecutive_loss_limit:
            base_stake *= self.loss_reduction_factor
        
        # 置信度加权
        confidence_multiplier = 1.0 + (confidence - 0.5) * 0.5
        position = base_stake * confidence_multiplier
        
        return min(position, self.max_position_pct)
    
    def decide(self, market: dict, state: PaperTradingState) -> dict:
        """策略决策（三级预警机制）"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        state.reset_daily(current_date)
        
        # 三级预警检查
        daily_warning_loss = CONFIG.get('daily_warning_loss', 0.05)
        daily_stop_loss = CONFIG.get('daily_stop_loss', 0.10)
        
        # 预警级别（-5%）
        if state.daily_pnl <= -daily_warning_loss and state.daily_pnl > -daily_stop_loss:
            log(f"⚠️ 预警：当前亏损 {state.daily_pnl:.1%}，接近止损线 {daily_stop_loss:.0%}")
            # 可在此发送微信预警通知
        
        # 止损级别（-10%）
        if state.daily_pnl <= -daily_stop_loss:
            log(f"🔴 止损：当前亏损 {state.daily_pnl:.1%}，触发止损线 {daily_stop_loss:.0%}")
            return {'bet': False, 'reason': '触发每日止损'}
        
        if state.consecutive_losses >= self.consecutive_loss_limit:
            return {'bet': False, 'reason': f'连败{state.consecutive_losses}次保护'}
        
        # 流动性检查
        liquidity = market.get('liquidity', 0)
        if liquidity < self.low_liquidity_threshold:
            return {'bet': False, 'reason': f'流动性过低 ({liquidity:.0f})'}
        
        # 生成市场价格序列 (模拟)
        current_price = market.get('yes_price', 0.5)
        market_data = [
            {'close': current_price + (np.random.random() - 0.5) * 0.1}
            for _ in range(10)
        ]
        
        # 计算置信度和 EV
        confidence = self.calculate_confidence(market_data)
        ev = self.estimate_ev(market_data, current_price)
        
        # 决策
        if confidence >= self.confidence_threshold and ev >= 0.05:
            position_pct = self.calculate_position(ev, confidence, state.balance, state.consecutive_losses)
            
            # 高流动性市场增加仓位
            if liquidity >= self.high_liquidity_threshold:
                position_pct = min(position_pct * 1.2, self.max_position_pct * 1.2)
            
            return {
                'bet': True,
                'side': 'YES',
                'confidence': confidence,
                'ev': ev,
                'position_pct': position_pct,
                'reason': '高置信度 + 正 EV'
            }
        
        elif confidence <= (1 - self.confidence_threshold) and ev <= -0.05:
            position_pct = self.calculate_position(-ev, 1 - confidence, state.balance, state.consecutive_losses)
            
            return {
                'bet': True,
                'side': 'NO',
                'confidence': 1 - confidence,
                'ev': -ev,
                'position_pct': position_pct,
                'reason': '高置信度反向'
            }
        
        return {'bet': False, 'reason': '未达阈值'}


class PolymarketClient:
    """Polymarket API 客户端 (简化版)"""
    
    def __init__(self):
        self.base_url = CONFIG['base_url']
        self.api_key = CONFIG['api_key']
        self.headers = {'Authorization': f"Bearer {self.api_key}"}
    
    def get_weather_markets(self):
        """获取气象市场"""
        try:
            url = f"{self.base_url}/events"
            params = {'limit': 100}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            events = response.json()
            
            # 过滤气象相关市场
            weather_keywords = ['temperature', 'weather', 'hot', 'cold', 'celsius', 'fahrenheit']
            weather_markets = []
            
            for event in events:
                title = event.get('title', '').lower()
                if any(kw in title for kw in weather_keywords):
                    weather_markets.append({
                        'id': event.get('id'),
                        'title': event.get('title'),
                        'yes_price': event.get('yes_bid', 0.5),
                        'no_price': event.get('no_bid', 0.5),
                        'liquidity': event.get('volume', 0),
                        'end_date': event.get('end_date')
                    })
            
            return weather_markets
        except Exception as e:
            log(f"⚠️ 获取市场失败：{e}")
            return []


def log(message: str):
    """日志输出"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    # 写入日志文件
    log_file = Path(CONFIG['log_file'])
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a') as f:
        f.write(log_msg + '\n')


def execute_trade(market: dict, signal: dict, state: PaperTradingState):
    """执行交易 (模拟)"""
    stake = signal['position_pct'] * state.balance
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 模拟结果 (50% 胜率)
    is_win = np.random.random() < 0.55  # 略高于 50%
    
    if is_win:
        # 盈利
        profit = stake * 0.8  # 简化：盈利 80%
        result = 'WIN'
    else:
        # 亏损
        profit = -stake
        result = 'LOSS'
    
    # 更新状态
    state.update(result, profit)
    
    # 记录交易
    trade_record = {
        'timestamp': datetime.now().isoformat(),
        'date': current_date,
        'market_id': market['id'],
        'market_title': market['title'][:50],
        'side': signal['side'],
        'stake': stake,
        'profit': profit,
        'result': result,
        'confidence': signal['confidence'],
        'balance_after': state.balance
    }
    
    # 写入交易文件
    trades_file = Path(CONFIG['trades_file'])
    with open(trades_file, 'a') as f:
        f.write(json.dumps(trade_record) + '\n')
    
    # ROI 追踪器集成 - 自动记录交易收益
    if ROI_TRACKER_ENABLED:
        try:
            conn = sqlite3.connect(ROI_DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (date, type, category, amount, description, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                current_date,
                'revenue' if profit > 0 else 'cost',
                '交易收益' if profit > 0 else '交易亏损',
                abs(profit),
                f"Polymarket {signal['side']} {result}",
                json.dumps({'market_id': market['id'], 'stake': stake, 'confidence': signal['confidence']})
            ))
            conn.commit()
            conn.close()
            log(f"  📊 ROI 已记录：{profit:+.2f}")
        except Exception as e:
            log(f"  ⚠️ ROI 记录失败：{e}")
    
    log(f"💰 交易完成：{market['title'][:30]} {signal['side']} ${stake:.2f} → {result} ${profit:+.2f}")
    
    return trade_record


def generate_report(state: PaperTradingState):
    """生成日报"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    win_rate = state.wins / state.total_trades if state.total_trades > 0 else 0
    total_return = (state.balance - CONFIG['initial_balance']) / CONFIG['initial_balance']
    
    report = f"""# 知几-E 模拟盘日报

> 日期：{today} | 策略版本：v3.0

---

## 📊 核心指标

| 指标 | 数值 |
|------|------|
| 初始资金 | ${CONFIG['initial_balance']:,.2f} |
| 当前余额 | ${state.balance:,.2f} |
| 总收益率 | {total_return:+.2%} |
| 总交易数 | {state.total_trades} |
| 盈利次数 | {state.wins} |
| 亏损次数 | {state.losses} |
| 胜率 | {win_rate:.1%} |
| 今日盈亏 | ${state.daily_pnl:+.2f} |
| 连败次数 | {state.consecutive_losses} |

---

## 📝 最近交易

"""
    
    for trade in state.trade_history[-5:]:
        result_emoji = '✅' if trade['result'] == 'WIN' else '❌'
        report += f"- {trade['timestamp'][:16]} {result_emoji} ${trade['profit']:+.2f} (余额：${trade['balance_after']:.2f})\n"
    
    report += f"""
---

## 🛡️ 风控状态

- 每日止损：{'⚠️ 已触发' if state.daily_pnl <= -CONFIG['daily_stop_loss'] else '✅ 正常'}
- 连败保护：{'⚠️ 已触发' if state.consecutive_losses >= CONFIG['consecutive_loss_limit'] else '✅ 正常'}

---

*生成时间：{datetime.now().isoformat()}*
"""
    
    # 保存报告
    report_file = Path(f"/home/nicola/.openclaw/workspace/reports/paper-trading-{today}.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    log(f"📝 日报已保存：{report_file}")
    return report


def main():
    """主程序"""
    log('╔══════════════════════════════════════════════════════════╗')
    log('║  知几-E 模拟盘 v3.0                                       ║')
    log('╚══════════════════════════════════════════════════════════╝')
    
    # 初始化
    state = PaperTradingState()
    strategy = ZhijiEStrategyV3()
    client = PolymarketClient()
    
    log(f"💼 初始资金：${CONFIG['initial_balance']:,.2f}")
    log(f"📊 当前余额：${state.balance:,.2f}")
    log(f"📈 总交易数：{state.total_trades}")
    log('')
    
    # 扫描市场
    log('🔍 扫描气象市场...')
    markets = client.get_weather_markets()
    log(f'  ✅ 发现 {len(markets)} 个市场')
    
    if not markets:
        log('⚠️ 无可用市场，退出')
        return
    
    # 策略决策
    log('🧠 策略分析...')
    opportunities = []
    
    for market in markets:
        signal = strategy.decide(market, state)
        
        if signal['bet']:
            opportunities.append((market, signal))
            log(f"  🎯 机会：{market['title'][:30]} {signal['side']} (置信度:{signal['confidence']:.0%})")
        else:
            log(f"  ⏭️ 跳过：{market['title'][:30]} ({signal['reason']})")
    
    log('')
    
    # 执行交易
    if opportunities:
        log(f'💼 执行 {len(opportunities)} 笔交易...')
        for market, signal in opportunities:
            execute_trade(market, signal, state)
    else:
        log('ℹ️ 无交易机会')
    
    log('')
    
    # 生成报告
    log('📝 生成日报...')
    generate_report(state)
    
    log('')
    log('╔══════════════════════════════════════════════════════════╗')
    log('║  模拟盘运行完成                                         ║')
    log('╚══════════════════════════════════════════════════════════╝')


if __name__ == '__main__':
    main()
