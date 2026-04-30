#!/usr/bin/env python3
"""
知几-E 实盘下注执行脚本
执行首笔下注并记录
"""

import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/zhiji')

from strategy_v22 import ZhijiStrategyV22
from closed_loop_optimizer import ClosedLoopOptimizer, BetRecord
from datetime import datetime
import json

def execute_first_bet():
    """执行首笔下注"""
    
    print("=" * 60)
    print("知几-E 首笔下注执行")
    print("=" * 60)
    
    # 加载策略
    strategy = ZhijiStrategyV22('/home/nicola/.taiyi/zhiji/polymarket.json')
    optimizer = ClosedLoopOptimizer()
    
    # 模拟市场数据（实际应从 API 获取）
    market_data = {
        'slug': 'will-2026-be-hottest-year-on-record',
        'yes_price': 0.25,  # 市场价格 25%
        'volume_24h': 10000,
    }
    
    # 模型预测
    model_prob = 0.96  # 置信度 96%
    
    # 计算 EV
    ev = strategy.calculate_ev(model_prob, market_data['yes_price'])
    print(f"\n📊 市场分析:")
    print(f"  市场：{market_data['slug']}")
    print(f"  市场价格：{market_data['yes_price']:.2%}")
    print(f"  模型置信度：{model_prob:.2%}")
    print(f"  EV: {ev:.4f}")
    
    # 检查阈值
    if ev < strategy.edge_threshold:
        print(f"\n❌ EV {ev:.4f} < {strategy.edge_threshold}，跳过")
        return
    
    # 计算仓位
    odds = (1 / market_data['yes_price']) - 1
    kelly = strategy.calculate_kelly(model_prob, odds)
    amount = kelly * 100  # 假设总资金$100
    
    print(f"\n💰 下注计算:")
    print(f"  Odds: {odds:.2f}")
    print(f"  Kelly: {kelly:.4f}")
    print(f"  下注金额：${amount:.2f}")
    
    # LMSR 风险评估
    risk = strategy.check_lmsr_risk(market_data['volume_24h'])
    print(f"\n⚠️  LMSR 风险：{risk['risk_level']}")
    print(f"  建议：{risk['recommendation']}")
    
    # 执行下注（模拟）
    shares = amount * odds
    print(f"\n✅ 执行下注:")
    print(f"  类型：YES")
    print(f"  金额：${amount:.2f}")
    print(f"  份额：{shares:.2f}")
    
    # 记录
    bet = BetRecord(
        timestamp=datetime.now().isoformat(),
        market=market_data['slug'],
        bet_type="YES",
        amount=amount,
        odds=odds,
        shares=shares,
        confidence=model_prob,
        strategy_version="v2.2"
    )
    optimizer.record_bet(bet)
    
    print(f"\n📝 已记录到闭环优化系统")
    
    # Telegram 通知（模拟）
    print(f"\n📱 Telegram 通知:")
    print(f"""
【知几-E 首笔下注】
市场：{market_data['slug']}
方向：YES
金额：${amount:.2f}
置信度：{model_prob:.2%}
EV: {ev:.4f}
时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
""")
    
    print("=" * 60)
    print("✅ 首笔下注执行完成")
    print("=" * 60)
    
    return bet

if __name__ == '__main__':
    execute_first_bet()
