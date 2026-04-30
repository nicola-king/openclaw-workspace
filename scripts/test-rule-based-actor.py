#!/usr/bin/env python3
"""
RuleBasedActor 集成测试
创建时间：2026-04-04
用途：测试 RuleBasedActor + SequentialTradingEnv 集成
"""

import sys
from pathlib import Path

workspace = Path(__file__).parent.parent
sys.path.insert(0, str(workspace))

def test_rule_based_actor():
    """测试 RuleBasedActor"""
    print("=" * 60)
    print("RuleBasedActor 集成测试")
    print("=" * 60)
    print()
    
    # 添加导入路径
    sys.path.insert(0, str(workspace / "skills" / "torchtrade-integration"))
    
    from rule_based_actor import (
        RuleBasedActor,
        ZhijiEStrategy,
        ZhijiEActorConfig
    )
    import numpy as np
    
    # 测试 1: Actor 创建
    print("[测试 1] Actor 创建")
    print("-" * 40)
    config = ZhijiEActorConfig()
    actor = RuleBasedActor(config)
    print(f"✅ Actor 创建成功")
    print(f"   配置：confidence={config.confidence_threshold}, edge={config.edge_threshold}")
    print()
    
    # 测试 2: 策略决策 - 随机数据
    print("[测试 2] 策略决策 (随机数据)")
    print("-" * 40)
    np.random.seed(42)
    observation = {
        'account_state': np.array([10000, 0, 0, 1, 0, 0], dtype=np.float32),
        'market_data_1Hour_10': np.random.randn(10, 5).astype(np.float32) * 0.01 + 1,
    }
    
    action_output = actor.get_action(observation)
    print(f"   动作：{action_output['action'].item()}")
    print(f"   仓位：{action_output['position_size']:.2f} USDT")
    print(f"   置信度：{action_output['confidence']:.4f}")
    print(f"   原因：{action_output['metadata']['decision_reason']}")
    print()
    
    # 测试 2b: 策略决策 - 强上涨趋势
    print("[测试 2b] 策略决策 (强上涨趋势 10%)")
    print("-" * 40)
    # 创建强上涨趋势数据 (10% 涨幅)
    strong_uptrend = np.linspace(1, 1.10, 10).reshape(-1, 1) * np.ones((10, 5))
    observation['market_data_1Hour_10'] = strong_uptrend.astype(np.float32)
    
    action_output = actor.get_action(observation)
    print(f"   动作：{action_output['action'].item()}")
    print(f"   仓位：{action_output['position_size']:.2f} USDT")
    print(f"   置信度：{action_output['confidence']:.4f}")
    print(f"   原因：{action_output['metadata']['decision_reason']}")
    print()
    
    # 测试 3: 策略决策 - 上涨趋势
    print("[测试 3] 策略决策 (上涨趋势)")
    print("-" * 40)
    # 创建上涨趋势数据
    trend_data = np.linspace(1, 1.05, 10).reshape(-1, 1) * np.ones((10, 5))
    observation['market_data_1Hour_10'] = trend_data.astype(np.float32)
    
    action_output = actor.get_action(observation)
    print(f"   动作：{action_output['action'].item()}")
    print(f"   仓位：{action_output['position_size']:.2f} USDT")
    print(f"   置信度：{action_output['confidence']:.4f}")
    print(f"   原因：{action_output['metadata']['decision_reason']}")
    print()
    
    # 测试 4: 策略决策 - 下跌趋势
    print("[测试 4] 策略决策 (下跌趋势)")
    print("-" * 40)
    # 创建下跌趋势数据
    downtrend_data = np.linspace(1.05, 1, 10).reshape(-1, 1) * np.ones((10, 5))
    observation['market_data_1Hour_10'] = downtrend_data.astype(np.float32)
    
    action_output = actor.get_action(observation)
    print(f"   动作：{action_output['action'].item()}")
    print(f"   仓位：{action_output['position_size']:.2f} USDT")
    print(f"   置信度：{action_output['confidence']:.4f}")
    print(f"   原因：{action_output['metadata']['decision_reason']}")
    print()
    
    # 测试 5: 浅水区检测
    print("[测试 5] 浅水区检测")
    print("-" * 40)
    observation_with_info = {
        'account_state': np.array([10000, 0, 0, 1, 0, 0], dtype=np.float32),
        'market_data_1Hour_10': trend_data.astype(np.float32),
    }
    info_shallow = {'liquidity': 30}  # 浅水区
    
    action_output = actor.get_action(observation_with_info, info=info_shallow)
    print(f"   流动性：30 (浅水阈值=50)")
    print(f"   动作：{action_output['action'].item()}")
    print(f"   原因：{action_output['metadata']['decision_reason']}")
    print()
    
    # 测试 6: 已有仓位
    print("[测试 6] 已有仓位 (持有逻辑)")
    print("-" * 40)
    observation_with_position = {
        'account_state': np.array([9000, 1000, 50, 1, 0, 0], dtype=np.float32),  # position=1000
        'market_data_1Hour_10': trend_data.astype(np.float32),
    }
    
    action_output = actor.get_action(observation_with_position)
    print(f"   现金：9000, 仓位：1000, PnL: 50")
    print(f"   动作：{action_output['action'].item()}")
    print(f"   原因：{action_output['metadata']['decision_reason']}")
    print()
    
    print("=" * 60)
    print("✅ 所有测试完成")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    test_rule_based_actor()
