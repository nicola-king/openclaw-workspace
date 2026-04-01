#!/usr/bin/env python3
"""
回测引擎 v1.0
功能：历史数据回测策略表现
输出：夏普比率/最大回撤/胜率等指标
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, symbol: str = 'ETHUSDT', initial_capital: float = 1000):
        self.symbol = symbol
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = []
        self.trades = []
        
        # 策略参数
        self.confidence_threshold = 0.70
        self.take_profit_pct = 0.10
        self.stop_loss_pct = -0.05
    
    def fetch_klines(self, start_date: str, end_date: str, interval: str = '1h') -> list:
        """获取历史 K 线数据"""
        print(f'📊 获取 {self.symbol} 历史数据：{start_date} → {end_date}')
        
        klines = []
        start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
        end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)
        
        url = 'https://api.binance.com/api/v3/klines'
        
        current_ts = start_ts
        while current_ts < end_ts:
            params = {
                'symbol': self.symbol,
                'interval': interval,
                'startTime': current_ts,
                'endTime': end_ts,
                'limit': 1000
            }
            
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if not data:
                break
            
            klines.extend(data)
            current_ts = data[-1][0] + 1
        
        print(f'  获取 {len(klines)} 根 K 线')
        return klines
    
    def calculate_indicators(self, klines: list) -> dict:
        """计算技术指标"""
        closes = [float(k[4]) for k in klines]
        highs = [float(k[2]) for k in klines]
        lows = [float(k[3]) for k in klines]
        
        # 简化版指标计算
        indicators = {
            'MA20': self.sma(closes, 20),
            'MA60': self.sma(closes, 60),
            'RSI': self.rsi(closes, 14),
            'highest_20': [max(lows[max(0,i-19):i+1]) for i in range(len(closes))],
            'lowest_20': [min(lows[max(0,i-19):i+1]) for i in range(len(closes))]
        }
        
        return indicators
    
    def sma(self, data: list, period: int) -> list:
        """简单移动平均"""
        result = []
        for i in range(len(data)):
            if i < period - 1:
                result.append(None)
            else:
                result.append(sum(data[i-period+1:i+1]) / period)
        return result
    
    def rsi(self, data: list, period: int = 14) -> list:
        """RSI 指标"""
        result = []
        for i in range(len(data)):
            if i < period:
                result.append(50)
            else:
                gains = []
                losses = []
                for j in range(i-period+1, i+1):
                    change = data[j] - data[j-1]
                    if change > 0:
                        gains.append(change)
                        losses.append(0)
                    else:
                        gains.append(0)
                        losses.append(abs(change))
                
                avg_gain = sum(gains) / period
                avg_loss = sum(losses) / period
                
                if avg_loss == 0:
                    result.append(100)
                else:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                    result.append(rsi)
        
        return result
    
    def generate_signals(self, klines: list, indicators: dict) -> list:
        """生成交易信号"""
        signals = []
        closes = [float(k[4]) for k in klines]
        
        for i in range(60, len(closes)):
            # 简单策略：MA 金叉 + RSI 超卖
            ma20 = indicators['MA20'][i]
            ma60 = indicators['MA60'][i]
            rsi = indicators['RSI'][i]
            
            if ma20 and ma60 and ma20 > ma60 and rsi < 40:
                signals.append({
                    'index': i,
                    'type': 'BUY',
                    'price': closes[i],
                    'time': klines[i][0]
                })
            elif ma20 and ma60 and ma20 < ma60 and rsi > 60:
                signals.append({
                    'index': i,
                    'type': 'SELL',
                    'price': closes[i],
                    'time': klines[i][0]
                })
        
        print(f'  生成 {len(signals)} 个交易信号')
        return signals
    
    def run_backtest(self, klines: list, signals: list) -> dict:
        """运行回测"""
        capital = self.initial_capital
        position = None
        trades = []
        equity_curve = [capital]
        
        closes = [float(k[4]) for k in klines]
        
        for signal in signals:
            idx = signal['index']
            price = signal['price']
            
            if signal['type'] == 'BUY' and position is None:
                # 开仓
                quantity = capital / price
                position = {
                    'type': 'BUY',
                    'price': price,
                    'quantity': quantity,
                    'index': idx
                }
            
            elif signal['type'] == 'SELL' and position is not None:
                # 平仓
                entry_price = position['price']
                pnl_pct = (price - entry_price) / entry_price
                
                capital *= (1 + pnl_pct)
                
                trades.append({
                    'entry_price': entry_price,
                    'exit_price': price,
                    'pnl_pct': pnl_pct,
                    'entry_time': klines[position['index']][0],
                    'exit_time': klines[idx][0]
                })
                
                position = None
        
        # 计算回测指标
        if trades:
            pnl_pcts = [t['pnl_pct'] for t in trades]
            wins = [p for p in pnl_pcts if p > 0]
            losses = [p for p in pnl_pcts if p <= 0]
            
            total_return = (capital - self.initial_capital) / self.initial_capital
            win_rate = len(wins) / len(trades) if trades else 0
            avg_win = sum(wins) / len(wins) if wins else 0
            avg_loss = sum(losses) / len(losses) if losses else 0
            profit_factor = abs(sum(wins) / sum(losses)) if losses and sum(losses) != 0 else 0
            
            # 最大回撤
            peak = self.initial_capital
            max_drawdown = 0
            for trade in trades:
                peak *= (1 + max(0, trade['pnl_pct']))
                drawdown = (peak - capital) / peak
                max_drawdown = min(max_drawdown, -drawdown)
            
            # 夏普比率（简化）
            if len(pnl_pcts) > 1:
                import statistics
                sharpe = statistics.mean(pnl_pcts) / statistics.stdev(pnl_pcts) if statistics.stdev(pnl_pcts) > 0 else 0
            else:
                sharpe = 0
            
            return {
                'initial_capital': self.initial_capital,
                'final_capital': capital,
                'total_return': total_return,
                'total_return_pct': f'{total_return:.2%}',
                'trade_count': len(trades),
                'win_count': len(wins),
                'loss_count': len(losses),
                'win_rate': win_rate,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'max_drawdown': max_drawdown,
                'sharpe_ratio': sharpe,
                'trades': trades
            }
        
        return {'error': '无交易记录'}
    
    def generate_report(self, results: dict, output_path: str):
        """生成回测报告"""
        report = f"""# 回测报告 - {self.symbol}

## 📊 回测概览

| 指标 | 值 |
|------|-----|
| 初始资金 | ${results['initial_capital']:.2f} |
| 最终资金 | ${results['final_capital']:.2f} |
| 总收益 | {results['total_return_pct']} |
| 交易次数 | {results['trade_count']} |
| 胜率 | {results['win_rate']:.1%} |

## 📈 详细指标

| 指标 | 值 |
|------|-----|
| 平均盈利 | {results['avg_win']:.2%} |
| 平均亏损 | {results['avg_loss']:.2%} |
| 盈亏比 | {results['profit_factor']:.2f} |
| 夏普比率 | {results['sharpe_ratio']:.2f} |
| 最大回撤 | {results['max_drawdown']:.2%} |

## 💡 策略评估

"""
        if results['sharpe_ratio'] > 1.5:
            report += "✅ **夏普比率优秀** (>1.5)，策略风险调整后收益良好\n\n"
        elif results['sharpe_ratio'] > 1.0:
            report += "🟡 **夏普比率良好** (>1.0)，策略可接受\n\n"
        else:
            report += "❌ **夏普比率偏低**，需优化策略参数\n\n"
        
        if results['win_rate'] > 0.6:
            report += "✅ **胜率优秀** (>60%)，策略预测准确\n\n"
        elif results['win_rate'] > 0.5:
            report += "🟡 **胜率良好** (>50%)，策略有效\n\n"
        else:
            report += "❌ **胜率偏低**，需优化入场信号\n\n"
        
        report += f"\n---\n*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f'📝 报告已保存：{output_path}')


def main():
    """主函数"""
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📊 回测引擎 v1.0                                         ║')
    print('║  太一 AGI · 币安交易策略                                  ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    
    # 创建回测引擎
    engine = BacktestEngine(symbol='ETHUSDT', initial_capital=1000)
    
    # 获取历史数据（最近 30 天）
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    klines = engine.fetch_klines(start_date, end_date)
    
    if len(klines) < 100:
        print('❌ 数据不足，无法回测')
        return
    
    # 计算指标
    print('📈 计算技术指标...')
    indicators = engine.calculate_indicators(klines)
    
    # 生成信号
    print('🔔 生成交易信号...')
    signals = engine.generate_signals(klines, indicators)
    
    if not signals:
        print('❌ 无交易信号，无法回测')
        return
    
    # 运行回测
    print('🚀 运行回测...')
    results = engine.run_backtest(klines, signals)
    
    if 'error' in results:
        print(f'❌ 回测失败：{results["error"]}')
        return
    
    # 生成报告
    print('📝 生成回测报告...')
    output_path = '/home/nicola/.openclaw/workspace/reports/backtest-ethusdt-30d.md'
    engine.generate_report(results, output_path)
    
    # 打印结果
    print('')
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📊 回测结果                                              ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'  初始资金：${results["initial_capital"]:.2f}')
    print(f'  最终资金：${results["final_capital"]:.2f}')
    print(f'  总收益：  {results["total_return_pct"]}')
    print(f'  交易次数：{results["trade_count"]}')
    print(f'  胜率：    {results["win_rate"]:.1%}')
    print(f'  夏普比率：{results["sharpe_ratio"]:.2f}')
    print(f'  最大回撤：{results["max_drawdown"]:.2%}')
    print('')


if __name__ == '__main__':
    main()
