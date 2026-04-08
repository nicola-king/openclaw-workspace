#!/usr/bin/env python3
"""调试置信度和 EV 计算 - v1.1"""

import sys
from pathlib import Path
import numpy as np

workspace = Path(__file__).parent.parent
sys.path.insert(0, str(workspace / "skills" / "torchtrade-integration"))

from rule_based_actor import ZhijiEStrategy, ZhijiEActorConfig

config = ZhijiEActorConfig(confidence_threshold=0.55, edge_threshold=0.05)
strategy = ZhijiEStrategy(config)

print("=" * 60)
print("置信度 + EV 调试 (v1.1)")
print("=" * 60)
print()

# 1. 强上涨趋势
print("[测试 1] 强上涨趋势 (10%)")
strong_uptrend = np.linspace(1, 1.10, 10).reshape(-1, 1) * np.ones((10, 5))
confidence = strategy._calculate_confidence(strong_uptrend)
model_prob = strategy._estimate_model_prob(strong_uptrend)
ev = model_prob - 0.5
print(f"置信度：{confidence:.4f} (阈值={strategy.confidence_threshold})")
print(f"模型概率：{model_prob:.4f}")
print(f"EV: {ev:.4f} (阈值={strategy.edge_threshold})")
print(f"决策：{'✅ 买入' if confidence >= 0.55 and ev >= 0.05 else '❌ 观望'}")
print()

# 2. 完整决策
print("[测试 2] 完整决策")
account_state = np.array([10000, 0, 0, 1, 0, 0], dtype=np.float32)
action, position_size, conf = strategy.decide(account_state, strong_uptrend)
print(f"动作：{action} (0=持有，1=买入，2=卖出)")
print(f"仓位：{position_size:.2f} USDT")
print(f"置信度：{conf:.4f}")
print()

print("=" * 60)
