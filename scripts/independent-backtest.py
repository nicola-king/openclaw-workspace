#!/usr/bin/env python3
"""
独立回测框架 - 不依赖 TorchTrade 环境
创建时间：2026-04-04
用途：使用 RuleBasedActor 运行独立回测
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np

workspace = Path(__file__).parent.parent
sys.path.insert(0, str(workspace / "skills" / "torchtrade-integration"))

from rule_based_actor import RuleBasedActor, ZhijiEActorConfig


def generate_mock_data(n_bars=500, trend=0.0):
    """生成模拟 K 线数据 - 增强趋势"""
    np.random.seed(42)
    
    # 基础价格
    base_price = 67000
    
    # 生成价格序列 (降低波动，增强趋势)
    returns = np.random.randn(n_bars) * 0.0005 + trend / n_bars  # 0.05% 波动 + 趋势
    prices = base_price * (1 + returns).cumprod()
    
    # 生成 OHLCV
    data = []
    for i in range(n_bars):
        open_price = prices[i] * (1 + np.random.randn() * 0.0005)
        high_price = max(prices[i], open_price) * (1 + abs(np.random.randn()) * 0.001)
        low_price = min(prices[i], open_price) * (1 - abs(np.random.randn()) * 0.001)
        close_price = prices[i]
        volume = np.random.randint(100, 1000)
        
        data.append({
            'timestamp': datetime.now() - timedelta(hours=n_bars-i),
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })
    
    return data


def extract_observation(data, i, window=10):
    """提取观测数据 - 修复归一化问题"""
    if i < window:
        return None
    
    # 获取窗口数据
    window_data = data[i-window:i]
    
    # 构建 OHLCV 矩阵
    ohlcv = np.array([
        [d['open'], d['high'], d['low'], d['close'], d['volume']]
        for d in window_data
    ], dtype=np.float32)
    
    # 归一化：使用最近价格作为基准，保留相对变化
    base_price = ohlcv[-1, 3]  # 用最后一个收盘价归一化
    ohlcv[:, :4] /= base_price
    ohlcv[:, :4] -= 1.0  # 转换为收益率形式 (0 附近)
    ohlcv[:, 4] /= 1000  # 成交量归一化
    
    return ohlcv


def run_backtest(data, initial_cash=10000):
    """运行回测"""
    # 创建 Actor (阈值适应归一化 + 随机数据)
    config = ZhijiEActorConfig(
        confidence_threshold=0.50,  # 中性阈值
        edge_threshold=0.005,       # EV > 0.5%
        kelly_divisor=4,
        max_position_pct=0.25,
    )
    actor = RuleBasedActor(config)
    
    # 初始化
    cash = initial_cash
    position = 0.0
    position_value = 0.0
    trades = []
    portfolio_values = []
    
    # 运行回测
    for i in range(len(data)):
        current_price = data[i]['close']
        
        # 提取观测
        observation_data = extract_observation(data, i)
        if observation_data is None:
            continue
        
        observation = {
            'account_state': np.array([cash, position_value, 0, 1, 0, 0], dtype=np.float32),
            'market_data_1Hour_10': observation_data,
        }
        
        # 获取动作
        action_output = actor.get_action(observation)
        action = action_output['action'].item()
        target_position = action_output['position_size']
        confidence = action_output['confidence']
        
        # 调试：前 5 笔交易打印日志
        if len(trades) < 5 and i % 50 == 0:
            print(f"Bar {i}: 价格={current_price:.2f}, 动作={action}, 目标仓位={target_position:.2f}, 置信度={confidence:.4f}")
        
        # 执行交易
        if action == 1 and target_position > 0:  # 买入
            # 计算可买数量
            trade_value = min(target_position, cash)
            if trade_value > 10:  # 最小交易金额
                shares = trade_value / current_price
                cash -= trade_value
                position += shares
                position_value = position * current_price
                
                trades.append({
                    'type': 'BUY',
                    'price': current_price,
                    'shares': shares,
                    'value': trade_value,
                    'confidence': confidence,
                    'bar': i
                })
        
        elif action == 2 and position > 0:  # 卖出
            # 全平
            trade_value = position * current_price
            cash += trade_value
            position = 0
            position_value = 0
            
            trades.append({
                'type': 'SELL',
                'price': current_price,
                'shares': 0,
                'value': trade_value,
                'confidence': confidence,
                'bar': i
            })
        
        # 更新持仓价值
        position_value = position * current_price
        
        # 记录组合价值
        portfolio_value = cash + position_value
        portfolio_values.append({
            'bar': i,
            'timestamp': data[i]['timestamp'],
            'price': current_price,
            'cash': cash,
            'position_value': position_value,
            'portfolio_value': portfolio_value,
            'return_pct': (portfolio_value - initial_cash) / initial_cash * 100
        })
    
    return {
        'initial_cash': initial_cash,
        'final_cash': cash,
        'final_position_value': position_value,
        'final_portfolio_value': cash + position_value,
        'total_return': (cash + position_value - initial_cash) / initial_cash * 100,
        'num_trades': len(trades),
        'trades': trades,
        'portfolio_values': portfolio_values
    }


def generate_report(results, data):
    """生成回测报告"""
    report = []
    report.append("# 独立回测报告 - RuleBasedActor")
    report.append("")
    report.append(f"> 回测时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"> 数据条数：{len(data)}")
    report.append("")
    
    report.append("## 📊 核心指标")
    report.append("")
    report.append("| 指标 | 值 |")
    report.append("|------|-----|")
    report.append(f"| 初始资金 | ${results['initial_cash']:,.2f} |")
    report.append(f"| 最终资金 | ${results['final_portfolio_value']:,.2f} |")
    report.append(f"| 总收益 | {results['total_return']:.2f}% |")
    report.append(f"| 交易次数 | {results['num_trades']} |")
    report.append("")
    
    report.append("## 📈 交易记录")
    report.append("")
    if results['trades']:
        report.append("| 类型 | 价格 | 数量 | 金额 | 置信度 |")
        report.append("|------|------|------|------|--------|")
        for trade in results['trades'][:10]:  # 显示前 10 笔
            report.append(f"| {trade['type']} | ${trade['price']:.2f} | {trade['shares']:.4f} | ${trade['value']:.2f} | {trade['confidence']:.2f} |")
    else:
        report.append("*无交易*")
    report.append("")
    
    report.append("## 💡 分析")
    report.append("")
    if results['total_return'] > 0:
        report.append("✅ 正收益 - 策略有效")
    elif results['total_return'] > -5:
        report.append("🟡 小幅亏损 - 需调优参数")
    else:
        report.append("❌ 显著亏损 - 需重新设计策略")
    report.append("")
    
    if results['num_trades'] == 0:
        report.append("⚠️  无交易 - 可能原因:")
        report.append("- 置信度阈值过高")
        report.append("- EV 阈值过高")
        report.append("- 市场数据特征不足")
    report.append("")
    
    return "\n".join(report)


def main():
    """主函数"""
    print("=" * 60)
    print("独立回测框架 - RuleBasedActor")
    print("=" * 60)
    print()
    
    # 生成测试数据
    print("[1/4] 生成模拟数据...")
    data_uptrend = generate_mock_data(n_bars=500, trend=0.10)  # 10% 上涨
    print(f"    ✅ 生成 500 条 K 线 (10% 上涨趋势)")
    print()
    
    # 运行回测
    print("[2/4] 运行回测...")
    results = run_backtest(data_uptrend, initial_cash=10000)
    print(f"    ✅ 回测完成")
    print()
    
    # 生成报告
    print("[3/4] 生成报告...")
    report = generate_report(results, data_uptrend)
    print()
    
    # 保存报告
    print("[4/4] 保存报告...")
    report_path = workspace / "reports" / "rule-based-actor-backtest.md"
    report_path.write_text(report, encoding='utf-8')
    print(f"    ✅ 报告已保存：{report_path}")
    print()
    
    # 打印报告
    print("=" * 60)
    print(report)
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    main()
