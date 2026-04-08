#!/usr/bin/env python3
"""调试回测数据流"""

import sys
from pathlib import Path
import numpy as np

workspace = Path(__file__).parent.parent
sys.path.insert(0, str(workspace / "skills" / "torchtrade-integration"))

from rule_based_actor import RuleBasedActor, ZhijiEActorConfig

# 生成数据
np.random.seed(42)
base_price = 67000
returns = np.random.randn(500) * 0.001 + 0.10/500  # 10% 趋势
prices = base_price * (1 + returns).cumprod()

# 构建 OHLCV
data = []
for i in range(500):
    data.append({
        'open': prices[i] * 0.999,
        'high': prices[i] * 1.002,
        'low': prices[i] * 0.998,
        'close': prices[i],
        'volume': 500
    })

# 提取观测 (回测逻辑)
def extract_observation(data, i, window=10):
    if i < window:
        return None
    window_data = data[i-window:i]
    ohlcv = np.array([
        [d['open'], d['high'], d['low'], d['close'], d['volume']]
        for d in window_data
    ], dtype=np.float32)
    ohlcv[:, :4] /= ohlcv[0, 3]
    ohlcv[:, 4] /= 1000
    return ohlcv

# 测试第 100 条数据
obs = extract_observation(data, 100)
print(f"观测形状：{obs.shape}")
print(f"收盘价范围：{obs[:, 3].min():.4f} - {obs[:, 3].max():.4f}")
print(f"趋势：{(obs[-1, 3] - obs[0, 3]) / obs[0, 3]:.4f}")

# 创建 Actor
config = ZhijiEActorConfig(confidence_threshold=0.55, edge_threshold=0.05)
actor = RuleBasedActor(config)

# 测试决策
observation = {
    'account_state': np.array([10000, 0, 0, 1, 0, 0], dtype=np.float32),
    'market_data_1Hour_10': obs,
}

action_output = actor.get_action(observation)
print(f"\n动作：{action_output['action'].item()}")
print(f"仓位：{action_output['position_size']:.2f}")
print(f"置信度：{action_output['confidence']:.4f}")
