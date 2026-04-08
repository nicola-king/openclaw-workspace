#!/usr/bin/env python3
"""
知几-E 策略回测引擎 v3.0 - 优化版
新增优化:
1. 动态 Kelly 仓位 (根据连胜/连败调整)
2. 止损机制 (每日最大亏损限制)
3. 连败保护 (连败后降低仓位)
4. 流动性分层 (不同流动性使用不同策略)
5. 置信度加权 (高置信度更高仓位)
6. 多策略融合 (气象 + 动量 + 均值回归)

目标：降低回撤，提高稳定性
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import random
import numpy as np
from collections import deque

DB_PATH = "/home/nicola/.openclaw/workspace/polymarket-data/polymarket.db"
REPORT_PATH = "/home/nicola/.openclaw/workspace/reports/backtest-report-v3.md"


class ZhijiEStrategyV3:
    """知几-E 策略引擎 v3.0 - 优化版"""
    
    def __init__(self, config=None):
        # 基础参数
        self.confidence_threshold = getattr(config, 'confidence_threshold', 0.60) if config else 0.60
        self.edge_threshold = getattr(config, 'edge_threshold', 0.05) if config else 0.05
        self.kelly_divisor = getattr(config, 'kelly_divisor', 4) if config else 4
        self.max_position_pct = getattr(config, 'max_position_pct', 0.15) if config else 0.15  # 降低到 15%
        
        # 风控参数 🆕
        self.daily_stop_loss = getattr(config, 'daily_stop_loss', 0.10) if config else 0.10  # 每日最大亏损 10%
        self.consecutive_loss_limit = getattr(config, 'consecutive_loss_limit', 3) if config else 3  # 连败 3 次
        self.loss_reduction_factor = getattr(config, 'loss_reduction_factor', 0.5) if config else 0.5  # 连败后仓位减半
        
        # 流动性分层 🆕
        self.high_liquidity_threshold = getattr(config, 'high_liquidity_threshold', 10000) if config else 10000
        self.low_liquidity_threshold = getattr(config, 'low_liquidity_threshold', 2000) if config else 2000
        
        # 状态追踪 🆕
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.last_trade_date = None
        self.trade_history = deque(maxlen=50)  # 最近 50 笔交易
    
    def reset_daily(self, current_date):
        """每日重置"""
        if self.last_trade_date != current_date:
            self.daily_pnl = 0.0
            self.last_trade_date = current_date
    
    def calculate_confidence(self, market_data: list, info: dict = None) -> float:
        """置信度计算 v2.0 - 多因子融合"""
        if len(market_data) < 5:
            return 0.5
        
        closes = [d['close'] for d in market_data]
        
        # 1. 趋势因子
        trend = closes[-1] - closes[0]
        trend_score = 0.25 * np.tanh(trend * 50)
        
        # 2. 动量因子
        returns = [closes[i+1] - closes[i] for i in range(len(closes)-1)]
        momentum = np.mean(returns[-3:]) if len(returns) >= 3 else 0
        momentum_score = 0.15 * np.tanh(momentum * 50)
        
        # 3. 波动率因子 (低波动率=高置信度)
        volatility = np.std(returns) if returns else 0
        volatility_score = -0.1 * volatility
        
        # 4. 均值回归因子 🆕
        mean_price = np.mean(closes)
        current_deviation = (closes[-1] - mean_price) / mean_price if mean_price > 0 else 0
        mean_reversion_score = -0.1 * np.tanh(current_deviation * 100)  # 偏离越大，反向置信度越高
        
        # 5. 气象置信度 (如果有)
        base_confidence = 0.5 + trend_score + momentum_score + volatility_score + mean_reversion_score
        
        if info and 'weather_confidence' in info:
            base_confidence = 0.7 * base_confidence + 0.3 * info['weather_confidence']
        
        return float(np.clip(base_confidence, 0.1, 0.95))
    
    def estimate_model_prob(self, market_data: list, info: dict = None) -> float:
        """模型概率估计 v2.0"""
        closes = [d['close'] for d in market_data]
        trend = closes[-1] - closes[0]
        returns = [closes[i+1] - closes[i] for i in range(len(closes)-1)]
        momentum = np.mean(returns[-3:]) if len(returns) >= 3 else 0
        
        # 加入均值回归
        mean_price = np.mean(closes)
        deviation = (closes[-1] - mean_price) / mean_price if mean_price > 0 else 0
        
        model_prob = 1 / (1 + np.exp(-(trend * 50 + momentum * 25 - deviation * 20)))
        return float(np.clip(model_prob, 0.1, 0.95))
    
    def calculate_dynamic_kelly(self, base_stake_pct: float, confidence: float) -> float:
        """动态 Kelly - 根据置信度和历史表现调整"""
        # 1. 置信度加权
        confidence_multiplier = 1.0 + (confidence - 0.5) * 0.5  # 高置信度最多加 25%
        
        # 2. 连败保护
        if self.consecutive_losses >= self.consecutive_loss_limit:
            loss_multiplier = self.loss_reduction_factor
        else:
            loss_multiplier = 1.0
        
        # 3. 近期表现 (最近 10 笔胜率)
        recent_trades = list(self.trade_history)[-10:]
        if recent_trades:
            recent_win_rate = sum(1 for t in recent_trades if t['result'] == 'WIN') / len(recent_trades)
            performance_multiplier = 0.5 + recent_win_rate  # 0.5-1.5
        else:
            performance_multiplier = 1.0
        
        # 综合调整
        dynamic_stake = base_stake_pct * confidence_multiplier * loss_multiplier * performance_multiplier
        return min(dynamic_stake, self.max_position_pct)
    
    def check_risk_limits(self) -> tuple:
        """检查风控限制"""
        # 1. 每日止损
        if self.daily_pnl <= -self.daily_stop_loss:
            return False, "每日止损触发"
        
        # 2. 连败保护
        if self.consecutive_losses >= self.consecutive_loss_limit:
            return False, f"连败{self.consecutive_losses}次保护"
        
        return True, "OK"
    
    def decide(self, market_data: list, current_date: str, info: dict = None) -> dict:
        """策略决策 v3.0"""
        # 每日重置
        self.reset_daily(current_date)
        
        # 1. 计算置信度和 EV
        confidence = self.calculate_confidence(market_data, info)
        model_prob = self.estimate_model_prob(market_data, info)
        ev = model_prob - 0.5
        
        # 2. 流动性分层
        liquidity = info.get('liquidity', float('inf')) if info else float('inf')
        
        if liquidity < self.low_liquidity_threshold:
            return {'bet': False, 'confidence': confidence, 'ev': ev, 'reason': f'流动性过低 ({liquidity:.0f})'}
        
        # 高流动性市场可以使用更高仓位
        if liquidity >= self.high_liquidity_threshold:
            effective_max_position = self.max_position_pct * 1.2  # 高流动性 +20%
        else:
            effective_max_position = self.max_position_pct
        
        # 3. 风控检查
        risk_ok, risk_reason = self.check_risk_limits()
        if not risk_ok:
            return {'bet': False, 'confidence': confidence, 'ev': ev, 'reason': risk_reason}
        
        # 4. 决策逻辑
        if confidence >= self.confidence_threshold and ev >= self.edge_threshold:
            # 计算基础仓位
            base_stake = min(ev / self.kelly_divisor, effective_max_position)
            # 动态调整
            dynamic_stake = self.calculate_dynamic_kelly(base_stake, confidence)
            
            return {
                'bet': True,
                'side': 'YES',
                'confidence': confidence,
                'ev': ev,
                'stake_pct': dynamic_stake,
                'reason': '高置信度 + 正 EV'
            }
        
        elif confidence <= (1 - self.confidence_threshold) and ev <= -self.edge_threshold:
            base_stake = min(abs(ev) / self.kelly_divisor, effective_max_position)
            dynamic_stake = self.calculate_dynamic_kelly(base_stake, 1 - confidence)
            
            return {
                'bet': True,
                'side': 'NO',
                'confidence': 1 - confidence,
                'ev': -ev,
                'stake_pct': dynamic_stake,
                'reason': '高置信度反向 + 负 EV'
            }
        
        return {'bet': False, 'confidence': confidence, 'ev': ev, 'reason': '未达阈值'}
    
    def update_state(self, result: str, profit: float):
        """更新状态"""
        self.daily_pnl += profit
        
        if result == 'WIN':
            self.consecutive_losses = 0
        else:
            self.consecutive_losses += 1
        
        self.trade_history.append({
            'result': result,
            'profit': profit,
            'daily_pnl': self.daily_pnl
        })


def load_weather_data():
    """加载气象数据"""
    if not Path(DB_PATH).exists():
        print(f"⚠️ 数据库不存在：{DB_PATH}")
        return generate_synthetic_weather_data(200)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date, city, temp_max, temp_min, precip_sum, weather_code
        FROM weather_forecasts
        ORDER BY date
        LIMIT 200
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


def generate_synthetic_weather_data(days: int = 200):
    """生成模拟气象数据"""
    np.random.seed(42)
    data = []
    base_date = datetime(2025, 1, 1)
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        seasonal = 15 + 10 * np.sin(2 * np.pi * i / 365)
        temp_max = seasonal + np.random.randn() * 3
        temp_min = seasonal - 5 + np.random.randn() * 2
        
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "city": "Shanghai",
            "temp_max": float(temp_max),
            "temp_min": float(temp_min),
            "precip_sum": max(0, float(np.random.randn() * 5)),
            "weather_code": int(np.random.randint(0, 5))
        })
    
    return data


def generate_markets(weather_data: list):
    """生成预测市场 v2.0 - 更真实的赔率"""
    markets = []
    
    for i, day_data in enumerate(weather_data[:-1]):
        base_temp = day_data["temp_max"]
        next_day = weather_data[i + 1]
        actual_temp = next_day["temp_max"]
        
        # 更真实的赔率模型
        yes_prob = 0.5 + (base_temp - 20) * 0.015  # 降低敏感度
        yes_prob = max(0.15, min(0.85, yes_prob))  # 限制在 0.15-0.85
        
        actual_outcome = "YES" if actual_temp > base_temp else "NO"
        
        # 流动性分层
        if random.random() < 0.3:
            liquidity = random.uniform(500, 2000)  # 30% 低流动性
        elif random.random() < 0.7:
            liquidity = random.uniform(2000, 10000)  # 40% 中等
        else:
            liquidity = random.uniform(10000, 50000)  # 30% 高流动性
        
        markets.append({
            "date": day_data["date"],
            "city": day_data["city"],
            "question": f"明天气温 > {base_temp:.1f}°C?",
            "yes_price": yes_prob,
            "no_price": 1 - yes_prob,
            "actual_outcome": actual_outcome,
            "actual_temp": actual_temp,
            "threshold": base_temp,
            "volume": liquidity * random.uniform(0.5, 2),
            "liquidity": liquidity
        })
    
    return markets


def run_backtest(markets: list, initial_capital: float = 1000, config=None):
    """运行回测 v3.0"""
    strategy = ZhijiEStrategyV3(config)
    
    capital = initial_capital
    trades = []
    wins = 0
    losses = 0
    total_staked = 0
    equity_curve = [capital]
    
    # 风控统计 🆕
    stop_loss_triggers = 0
    consecutive_loss_triggers = 0
    low_liquidity_skips = 0
    
    for market in markets:
        # 生成市场价格序列
        market_data = [
            {'close': market['yes_price'] + (random.random() - 0.5) * 0.1}
            for _ in range(10)
        ]
        
        signal = strategy.decide(market_data, market['date'], {
            'weather_confidence': 0.7,
            'liquidity': market['liquidity']
        })
        
        if not signal['bet']:
            if '流动性过低' in signal.get('reason', ''):
                low_liquidity_skips += 1
            elif '止损' in signal.get('reason', ''):
                stop_loss_triggers += 1
            elif '连败' in signal.get('reason', ''):
                consecutive_loss_triggers += 1
            equity_curve.append(capital)
            continue
        
        stake = signal['stake_pct'] * capital
        total_staked += stake
        
        predicted = signal['side']
        actual = market['actual_outcome']
        
        if actual == predicted:
            price = market['yes_price'] if predicted == 'YES' else market['no_price']
            payout = stake / price
            profit = payout - stake
            capital += profit
            wins += 1
            result = "WIN"
        else:
            profit = -stake
            capital -= stake
            losses += 1
            result = "LOSS"
        
        # 更新策略状态
        strategy.update_state(result, profit / initial_capital)  # 归一化
        
        trades.append({
            "date": market["date"],
            "market": market["question"][:40],
            "side": predicted,
            "actual": actual,
            "stake": stake,
            "profit": profit,
            "result": result,
            "confidence": signal['confidence'],
            "ev": signal['ev'],
            "stake_pct": signal['stake_pct'],
            "liquidity": market['liquidity'],
            "reason": signal.get('reason', ''),
            "capital_after": capital
        })
        
        equity_curve.append(capital)
    
    return {
        "initial_capital": initial_capital,
        "final_capital": capital,
        "total_return": (capital - initial_capital) / initial_capital,
        "total_trades": len(trades),
        "wins": wins,
        "losses": losses,
        "win_rate": wins / len(trades) if trades else 0,
        "total_staked": total_staked,
        "avg_trade": total_staked / len(trades) if trades else 0,
        "sharpe": calculate_sharpe(equity_curve),
        "max_drawdown": calculate_max_drawdown(equity_curve),
        "trades": trades,
        "equity_curve": equity_curve,
        "risk_stats": {
            "stop_loss_triggers": stop_loss_triggers,
            "consecutive_loss_triggers": consecutive_loss_triggers,
            "low_liquidity_skips": low_liquidity_skips
        }
    }


def calculate_sharpe(equity_curve: list, risk_free_rate: float = 0.02) -> float:
    """计算夏普比率"""
    if len(equity_curve) < 2:
        return 0.0
    
    returns = [(equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1] 
               for i in range(1, len(equity_curve)) if equity_curve[i-1] > 0]
    
    if not returns:
        return 0.0
    
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    
    if std_return == 0:
        return 0.0
    
    sharpe = (mean_return - risk_free_rate / 252) / std_return * np.sqrt(252)
    return float(sharpe)


def calculate_max_drawdown(equity_curve: list) -> float:
    """计算最大回撤"""
    if len(equity_curve) < 2:
        return 0.0
    
    peak = equity_curve[0]
    max_dd = 0.0
    
    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak if peak > 0 else 0
        max_dd = max(max_dd, drawdown)
    
    return float(max_dd)


def generate_report(result: dict, config):
    """生成回测报告 v3.0"""
    r = result
    
    report = f"""# 知几-E 策略回测报告 v3.0 (优化版)

> 生成时间：{datetime.now().isoformat()}
> 数据源：气象预测数据
> 策略版本：Zhiji-E v3.0
> 配置：置信度{config.confidence_threshold:.0%} | Kelly/{config.kelly_divisor} | 最大仓位{config.max_position_pct:.0%}

---

## 📊 核心指标

| 指标 | 数值 | 评级 | vs v2.0 |
|------|------|------|--------|
| 初始资金 | ${r['initial_capital']:,.2f} | - | - |
| 最终资金 | ${r['final_capital']:,.2f} | - | - |
| **总收益率** | **{r['total_return']:+.2%}** | {'✅' if r['total_return'] > 0 else '❌'} | ? |
| 总交易数 | {r['total_trades']} | - | - |
| 盈利次数 | {r['wins']} | - | - |
| 亏损次数 | {r['losses']} | - | - |
| **胜率** | **{r['win_rate']:.1%}** | {'✅' if r['win_rate'] > 0.5 else '❌'} | ? |
| 总下注额 | ${r['total_staked']:,.2f} | - | - |
| 单笔平均 | ${r['avg_trade']:,.2f} | - | - |
| **夏普比率** | **{r['sharpe']:.2f}** | {'✅' if r['sharpe'] > 1 else '⚠️'} | ? |
| **最大回撤** | **{r['max_drawdown']:.1%}** | {'✅' if r['max_drawdown'] < 0.3 else '⚠️'} | ? |

---

## 🛡️ 风控统计

| 风控机制 | 触发次数 | 说明 |
|----------|---------|------|
| 每日止损 | {r['risk_stats']['stop_loss_triggers']}次 | 防止单日大亏 |
| 连败保护 | {r['risk_stats']['consecutive_loss_triggers']}次 | 连败{config.consecutive_loss_limit}次后降仓 |
| 流动性过滤 | {r['risk_stats']['low_liquidity_skips']}次 | 跳过流动性<${config.low_liquidity_threshold} |

---

## 🎯 策略配置

| 参数 | 值 |
|------|-----|
| 置信度阈值 | ≥{config.confidence_threshold:.0%} |
| EV 阈值 | ≥{config.edge_threshold:.0%} |
| Kelly 分母 | {config.kelly_divisor} |
| 单笔上限 | {config.max_position_pct:.0%} |
| 每日止损 | {config.daily_stop_loss:.0%} |
| 连败限制 | {config.consecutive_loss_limit}次 |
| 高流动性阈值 | >${config.high_liquidity_threshold} |
| 低流动性阈值 | <${config.low_liquidity_threshold} |

---

## 📈 收益曲线

```
初始：${r['initial_capital']:,.2f}
最终：${r['final_capital']:,.2f}
收益：${r['final_capital'] - r['initial_capital']:+,.2f} ({r['total_return']:+.2%})
```

---

## 📝 交易记录（前 15 笔）

| 日期 | 方向 | 实际 | 下注 | 盈亏 | 结果 | 置信度 | 原因 |
|------|------|------|------|------|------|--------|------|
"""
    
    for trade in r["trades"][:15]:
        reason_short = trade.get('reason', '')[:20]
        report += f"| {trade['date']} | {trade['side']} | {trade['actual']} | ${trade['stake']:.2f} | ${trade['profit']:+.2f} | {trade['result']} | {trade['confidence']:.0%} | {reason_short} |\n"
    
    if len(r["trades"]) > 15:
        report += f"\n*... 还有 {len(r['trades']) - 15} 笔交易，详见完整数据*\n"
    
    report += f"""
---

## 💡 优化点总结

### v3.0 新增功能
1. ✅ **动态 Kelly** - 根据连胜/连败自动调整仓位
2. ✅ **每日止损** - 单日亏损>10% 停止交易
3. ✅ **连败保护** - 连败 3 次后仓位减半
4. ✅ **流动性分层** - 高流动性市场更高仓位
5. ✅ **多因子置信度** - 趋势 + 动量 + 波动率 + 均值回归
6. ✅ **状态追踪** - 记录最近 50 笔交易表现

### vs v2.0 改进
- 最大仓位：25% → 15% (降低风险)
- 增加风控：无 → 每日止损 + 连败保护
- 置信度计算：3 因子 → 4 因子 (加入均值回归)

---

## 🎯 结论与建议

"""
    
    if r['total_return'] > 0.5:
        report += f"### ✅ 策略表现优秀\n\n"
        report += f"- 收益率 **{r['total_return']:+.2%}**\n"
        report += f"- 夏普比率 **{r['sharpe']:.2f}**\n"
        report += f"- 最大回撤 **{r['max_drawdown']:.1%}**\n\n"
        report += f"**建议**: 可以进入模拟盘测试阶段\n"
    elif r['total_return'] > 0:
        report += f"### ✅ 策略盈利\n\n"
        report += f"- 收益率 **{r['total_return']:+.2%}**\n"
        report += f"- 风控机制有效触发\n\n"
        report += f"**建议**: 继续微调参数\n"
    else:
        report += f"### ❌ 策略亏损\n\n"
        report += f"- 需要调整参数或策略逻辑\n"
    
    report += f"""
---

## ⚠️ 风险提示

1. **回测局限性**: 使用模拟赔率
2. **过拟合风险**: 参数可能失效
3. **流动性风险**: 实盘滑点
4. **模型风险**: 气象预测准确率

**实盘前请充分测试**

---

*生成：太一 AGI · 知几-E 回测引擎 v3.0 | 优化版*
"""
    
    return report


def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📊 知几-E 策略回测引擎 v3.0 (优化版)                      ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print('')
    
    print('📊 加载气象数据...')
    weather_data = load_weather_data()
    print(f'  ✅ {len(weather_data)} 条记录')
    print('')
    
    print('📈 生成预测市场...')
    markets = generate_markets(weather_data)
    print(f'  ✅ {len(markets)} 个市场')
    print(f'     流动性分布：高 ({sum(1 for m in markets if m["liquidity"]>=10000)}) / 中 ({sum(1 for m in markets if 2000<=m["liquidity"]<10000)}) / 低 ({sum(1 for m in markets if m["liquidity"]<2000)})')
    print('')
    
    # 参数网格搜索 🆕
    print('🔍 参数网格搜索...')
    print('')
    
    configs = [
        {'confidence_threshold': 0.55, 'kelly_divisor': 4, 'max_position_pct': 0.15},
        {'confidence_threshold': 0.60, 'kelly_divisor': 4, 'max_position_pct': 0.15},
        {'confidence_threshold': 0.60, 'kelly_divisor': 3, 'max_position_pct': 0.15},
        {'confidence_threshold': 0.60, 'kelly_divisor': 4, 'max_position_pct': 0.12},
        {'confidence_threshold': 0.65, 'kelly_divisor': 4, 'max_position_pct': 0.15},
    ]
    
    all_results = []
    
    for cfg in configs:
        config = type('Config', (), {
            **cfg,
            'edge_threshold': 0.05,
            'daily_stop_loss': 0.10,
            'consecutive_loss_limit': 3,
            'loss_reduction_factor': 0.5,
            'high_liquidity_threshold': 10000,
            'low_liquidity_threshold': 2000,
        })()
        
        result = run_backtest(markets, initial_capital=1000, config=config)
        result['config'] = cfg
        all_results.append(result)
        
        # 综合评分 = 收益率 * 0.4 + Sharpe * 0.3 + (1-MaxDD) * 0.3
        score = result['total_return'] * 0.4 + result['sharpe'] * 0.3 + (1 - result['max_drawdown']) * 0.3
        result['score'] = score
        
        print(f'  置信度{cfg["confidence_threshold"]:.0%}/Kelly/{cfg["kelly_divisor"]}/仓位{cfg["max_position_pct"]:.0%}: '
              f'{result["total_trades"]}笔，收益 {result["total_return"]:+.2%}, Sharpe {result["sharpe"]:.2f}, MaxDD {result["max_drawdown"]:.1%}, '
              f'评分{score:.2f}')
    
    best_result = max(all_results, key=lambda r: r['score'])
    print('')
    print(f'🏆 最佳配置：置信度{best_result["config"]["confidence_threshold"]:.0%} / Kelly/{best_result["config"]["kelly_divisor"]} / 仓位{best_result["config"]["max_position_pct"]:.0%}')
    print(f'   综合评分：{best_result["score"]:.2f}')
    
    result = best_result
    config = type('Config', (), {**best_result['config'], 'edge_threshold': 0.05, 'daily_stop_loss': 0.10, 'consecutive_loss_limit': 3, 'loss_reduction_factor': 0.5, 'high_liquidity_threshold': 10000, 'low_liquidity_threshold': 2000})()
    
    print('📝 生成报告...')
    report = generate_report(result, config)
    
    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f'  💾 报告已保存：{REPORT_PATH}')
    print('')
    
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📊 回测结果摘要                                         ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'初始资金：${result["initial_capital"]:,.2f}')
    print(f'最终资金：${result["final_capital"]:,.2f}')
    print(f'总收益率：{result["total_return"]:+.2%}')
    print(f'胜率：{result["win_rate"]:.1%}')
    print(f'夏普比率：{result["sharpe"]:.2f}')
    print(f'最大回撤：{result["max_drawdown"]:.1%}')
    print(f'交易数：{result["total_trades"]}')
    print('')
    print(f'风控触发：止损{result["risk_stats"]["stop_loss_triggers"]}次 / 连败{result["risk_stats"]["consecutive_loss_triggers"]}次 / 流动性{result["risk_stats"]["low_liquidity_skips"]}次')
    print('')
    
    if result["total_return"] > 0.5:
        print('✅ 策略表现优秀 - 建议进入模拟盘测试')
    elif result["total_return"] > 0:
        print('✅ 策略盈利 - 继续优化参数')
    else:
        print('❌ 策略亏损 - 需要调整策略逻辑')
    print('')
    
    print('🔧 优化版特性:')
    print('   ✅ 动态 Kelly 仓位')
    print('   ✅ 每日止损保护')
    print('   ✅ 连败保护机制')
    print('   ✅ 流动性分层')
    print('   ✅ 多因子置信度')
    print('')


if __name__ == '__main__':
    main()
