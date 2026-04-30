#!/usr/bin/env python3
"""
知几-E 离线模拟盘 v3.0
使用本地气象数据生成模拟市场，无需 API

运行方式：
1. 手动：python3 zhiji-e-paper-trading-offline.py
2. Cron: 0 * * * * (每小时执行)
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

# 配置
DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"
STATE_FILE = '/tmp/zhiji-paper-state-offline.json'
LOG_FILE = '/home/nicola/.openclaw/workspace/logs/paper-trading-offline.log'
TRADES_FILE = '/home/nicola/.openclaw/workspace/logs/paper-trades-offline.jsonl'

CONFIG = {
    'initial_balance': 10000,
    'confidence_threshold': 0.60,
    'kelly_divisor': 3,
    'max_position_pct': 0.15,
    'daily_stop_loss': 0.10,
    'consecutive_loss_limit': 3,
    'loss_reduction_factor': 0.5,
    'low_liquidity_threshold': 2000,
    'high_liquidity_threshold': 10000,
}


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
        self.pending_trades = []  # 待结算交易
        
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
                    self.pending_trades = state.get('pending_trades', [])
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
            'trade_history': self.trade_history[-100:],
            'pending_trades': self.pending_trades[-50:],
            'last_update': datetime.now().isoformat()
        }
        
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    
    def reset_daily(self, current_date):
        """每日重置"""
        if self.last_trade_date != current_date:
            log(f"📅 新交易日：{current_date} | 昨日余额：${self.balance:.2f}")
            self.daily_pnl = 0.0
            self.last_trade_date = current_date
    
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
    
    def calculate_confidence(self, market_data: list) -> float:
        """置信度计算 (4 因子)"""
        if len(market_data) < 5:
            return 0.5
        
        closes = [d['close'] for d in market_data]
        
        trend = closes[-1] - closes[0]
        trend_score = 0.25 * np.tanh(trend * 50)
        
        returns = [closes[i+1] - closes[i] for i in range(len(closes)-1)]
        momentum = np.mean(returns[-3:]) if len(returns) >= 3 else 0
        momentum_score = 0.15 * np.tanh(momentum * 50)
        
        volatility = np.std(returns) if returns else 0
        volatility_score = -0.1 * volatility
        
        mean_price = np.mean(closes)
        deviation = (closes[-1] - mean_price) / mean_price if mean_price > 0 else 0
        mean_reversion_score = -0.1 * np.tanh(deviation * 100)
        
        confidence = 0.5 + trend_score + momentum_score + volatility_score + mean_reversion_score
        return float(np.clip(confidence, 0.1, 0.95))
    
    def decide(self, market: dict, state: PaperTradingState) -> dict:
        """策略决策"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        state.reset_daily(current_date)
        
        # 风控检查
        if state.daily_pnl <= -CONFIG['daily_stop_loss']:
            return {'bet': False, 'reason': '触发每日止损'}
        
        if state.consecutive_losses >= CONFIG['consecutive_loss_limit']:
            return {'bet': False, 'reason': f'连败{state.consecutive_losses}次保护'}
        
        liquidity = market.get('liquidity', 0)
        if liquidity < self.low_liquidity_threshold:
            return {'bet': False, 'reason': f'流动性过低 ({liquidity:.0f})'}
        
        # 生成市场价格序列
        current_price = market['yes_price']
        market_data = [
            {'close': current_price + (np.random.random() - 0.5) * 0.1}
            for _ in range(10)
        ]
        
        confidence = self.calculate_confidence(market_data)
        ev = confidence - current_price
        
        # 决策
        if confidence >= self.confidence_threshold and ev >= 0.05:
            base_stake = min(ev / self.kelly_divisor, self.max_position_pct)
            
            if state.consecutive_losses >= CONFIG['consecutive_loss_limit']:
                base_stake *= CONFIG['loss_reduction_factor']
            
            confidence_multiplier = 1.0 + (confidence - 0.5) * 0.5
            position_pct = base_stake * confidence_multiplier
            
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
            base_stake = min(-ev / self.kelly_divisor, self.max_position_pct)
            
            if state.consecutive_losses >= CONFIG['consecutive_loss_limit']:
                base_stake *= CONFIG['loss_reduction_factor']
            
            confidence_mult = 1.0 + ((1 - confidence) - 0.5) * 0.5
            position_pct = base_stake * confidence_mult
            
            return {
                'bet': True,
                'side': 'NO',
                'confidence': 1 - confidence,
                'ev': -ev,
                'position_pct': position_pct,
                'reason': '高置信度反向'
            }
        
        return {'bet': False, 'reason': '未达阈值'}


def log(message: str):
    """日志输出"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'a') as f:
        f.write(log_msg + '\n')


def load_weather_data():
    """加载气象数据"""
    if not Path(DB_PATH).exists():
        log(f"⚠️ 数据库不存在：{DB_PATH}")
        return []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date, city, temp_max, temp_min, precip_sum, weather_code
        FROM weather_forecasts
        WHERE date >= date('now', '-30 days')
        ORDER BY date
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{
        "date": row[0],
        "city": row[1],
        "temp_max": row[2],
        "temp_min": row[3],
        "precip_sum": row[4],
        "weather_code": row[5]
    } for row in rows]


def generate_markets(weather_data: list):
    """生成模拟市场"""
    markets = []
    
    for i, day_data in enumerate(weather_data[:-1]):
        base_temp = day_data["temp_max"]
        next_day = weather_data[i + 1]
        actual_temp = next_day["temp_max"]
        
        yes_prob = 0.5 + (base_temp - 20) * 0.015
        yes_prob = max(0.15, min(0.85, yes_prob))
        
        import random
        if random.random() < 0.3:
            liquidity = random.uniform(500, 2000)
        elif random.random() < 0.7:
            liquidity = random.uniform(2000, 10000)
        else:
            liquidity = random.uniform(10000, 50000)
        
        markets.append({
            "id": f"TEMP-{day_data['city']}-{day_data['date']}",
            "date": day_data["date"],
            "city": day_data["city"],
            "title": f"明天气温 > {base_temp:.1f}°C?",
            "yes_price": yes_prob,
            "no_price": 1 - yes_prob,
            "actual_outcome": "YES" if actual_temp > base_temp else "NO",
            "actual_temp": actual_temp,
            "threshold": base_temp,
            "liquidity": liquidity,
            "resolved": False
        })
    
    return markets


def check_pending_trades(state: PaperTradingState, weather_data: list):
    """检查待结算交易"""
    if not state.pending_trades:
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    weather_map = {w['date']: w for w in weather_data}
    
    settled = []
    
    for trade in state.pending_trades:
        trade_date = trade['market_date']
        
        # 检查是否已到期
        if trade_date in weather_map:
            actual = weather_map[trade_date]
            actual_outcome = "YES" if actual['temp_max'] > trade['threshold'] else "NO"
            
            if actual_outcome == trade['side']:
                profit = trade['stake'] / trade['price'] - trade['stake']
                result = 'WIN'
            else:
                profit = -trade['stake']
                result = 'LOSS'
            
            state.update(result, profit)
            settled.append(trade['id'])
            
            log(f"💰 交易结算：{trade['market_id']} → {result} ${profit:+.2f}")
    
    # 移除已结算
    state.pending_trades = [t for t in state.pending_trades if t['id'] not in settled]
    state.save()


def execute_trade(market: dict, signal: dict, state: PaperTradingState):
    """执行交易"""
    stake = signal['position_pct'] * state.balance
    
    trade_record = {
        'id': f"TRADE-{datetime.now().timestamp()}",
        'timestamp': datetime.now().isoformat(),
        'market_id': market['id'],
        'market_date': market['date'],
        'market_title': market['title'][:50],
        'side': signal['side'],
        'stake': stake,
        'price': market['yes_price'] if signal['side'] == 'YES' else market['no_price'],
        'threshold': market['threshold'],
        'confidence': signal['confidence'],
        'balance_after': state.balance - stake
    }
    
    state.pending_trades.append(trade_record)
    state.save()
    
    # 写入交易文件
    trades_path = Path(TRADES_FILE)
    with open(trades_path, 'a') as f:
        f.write(json.dumps(trade_record) + '\n')
    
    log(f"📝 下单：{market['title'][:30]} {signal['side']} ${stake:.2f} @ {trade_record['price']:.2f}")


def generate_report(state: PaperTradingState):
    """生成日报"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    win_rate = state.wins / state.total_trades if state.total_trades > 0 else 0
    total_return = (state.balance - CONFIG['initial_balance']) / CONFIG['initial_balance']
    pending_count = len(state.pending_trades)
    
    report = f"""# 知几-E 离线模拟盘日报

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
| 待结算 | {pending_count} 笔 |

---

## 📝 最近交易

"""
    
    for trade in state.trade_history[-5:]:
        emoji = '✅' if trade['result'] == 'WIN' else '❌'
        report += f"- {trade['timestamp'][:16]} {emoji} ${trade['profit']:+.2f} (余额：${trade['balance_after']:.2f})\n"
    
    if state.pending_trades:
        report += f"\n## ⏳ 待结算交易\n\n"
        for trade in state.pending_trades[-5:]:
            report += f"- {trade['market_title'][:30]} {trade['side']} ${trade['stake']:.2f} (到期：{trade['market_date']})\n"
    
    report += f"""
---

## 🛡️ 风控状态

- 每日止损：{'⚠️ 已触发' if state.daily_pnl <= -CONFIG['daily_stop_loss'] else '✅ 正常'}
- 连败保护：{'⚠️ 已触发' if state.consecutive_losses >= CONFIG['consecutive_loss_limit'] else '✅ 正常'}

---

*生成时间：{datetime.now().isoformat()}*
"""
    
    report_path = Path(f"/home/nicola/.openclaw/workspace/reports/paper-trading-offline-{today}.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    log(f"📝 日报已保存：{report_path}")


def main():
    """主程序"""
    log('╔══════════════════════════════════════════════════════════╗')
    log('║  知几-E 离线模拟盘 v3.0                                   ║')
    log('╚══════════════════════════════════════════════════════════╝')
    
    state = PaperTradingState()
    strategy = ZhijiEStrategyV3()
    
    log(f"💼 初始资金：${CONFIG['initial_balance']:,.2f}")
    log(f"📊 当前余额：${state.balance:,.2f}")
    log(f"📈 总交易数：{state.total_trades} | 待结算：{len(state.pending_trades)}")
    log('')
    
    # 加载气象数据
    log('📊 加载气象数据...')
    weather_data = load_weather_data()
    log(f'  ✅ {len(weather_data)} 条记录')
    
    if not weather_data:
        log('⚠️ 无气象数据，退出')
        return
    
    # 检查待结算交易
    log('⏳ 检查待结算交易...')
    check_pending_trades(state, weather_data)
    log('')
    
    # 生成市场
    log('📈 生成模拟市场...')
    markets = generate_markets(weather_data)
    log(f'  ✅ {len(markets)} 个市场')
    
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
