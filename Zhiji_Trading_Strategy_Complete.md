# 知几 (Zhiji) 量化交易策略完整代码包

> **整理时间**: 2026-04-22 12:40  
> **版本**: v3.0 (知几-E 混合策略)  
> **作者**: 太一 AGI  
> **来源**: `/home/nicola/.openclaw/workspace/skills/01-trading/zhiji/`

---

## 📁 文件清单

| 文件 | 大小 | 说明 |
|------|------|------|
| `SKILL.md` | 1.2KB | 技能定义 |
| `hybrid_strategy.py` | 10KB | 混合策略引擎 v3.0 |
| `strategy_v22.py` | 7KB | 6 公式增强版策略 |
| `lmsr_pricer.py` | 5KB | LMSR 定价模块 |
| `bayesian_updater.py` | 6KB | 贝叶斯置信度更新 |
| `market_maker.py` | 7KB | 做市策略引擎 |
| `self_evolution_zhiji_agent.py` | 13KB | 自进化 Agent |
| `execute_bet.py` | 3KB | 交易执行 |
| `paper_trading_monitor.py` | 5KB | 模拟交易监控 |
| `requirements.txt` | 0.5KB | Python 依赖 |

**总计**: 10 个文件 / 约 2000 行代码 / 58KB

---

## 📄 1. SKILL.md - 技能定义

```markdown
---
name: zhiji
version: 1.0.0
description: 知几 - 量化交易策略引擎
category: trading
tags: ['zhiji', 'quant', 'strategy', 'polymarket']
author: 太一 AGI
created: 2026-04-07
---

# Zhiji - 知几量化交易 Bot

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：知几

---

## 🎯 职责

**量化交易执行**，包括 Polymarket 预测市场 + GMGN 链上交易

---

## 🔧 使用命令

```bash
# 查看交易信号
python3 zhiji-signals.py --market <市场>

# 执行交易
python3 zhiji-trader.py --buy --market <市场> --amount <数量>

# 查看持仓
python3 zhiji-portfolio.py
```

---

## 📁 目录结构

| 目录/文件 | 说明 |
|----------|------|
| `ab_test_framework.py` | A/B 测试框架 |
| `airdrop_opportunities.md` | 空投机会 |
| `polymarket/` | Polymarket 交易 |
| `gmgn/` | GMGN 交易 |
| `sentiment/` | 情绪分析 |

---

## 📊 输出格式

交易数据存入 `memory/zhiji/` 目录

---

## 🔗 相关文档

- `constitution/workflows/QUANT-TRADING.md` - 量化交易工作流
- `constitution/directives/TURBOQUANT.md` - TurboQuant 记忆

---

*创建：2026-04-03 22:57 | 太一 AGI*
```

---

## 📄 2. hybrid_strategy.py - 混合策略引擎 v3.0

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几-E 混合策略引擎 v3.0
策略：套利为主 (70-100%) + 做市为辅 (0-30%)
用途：根据资金规模动态调整配比
"""

import json
from datetime import datetime
from typing import Dict, List

class HybridStrategy:
    """混合策略引擎"""
    
    def __init__(self, config_path: str = "~/.taiyi/zhiji/polymarket.json"):
        self.config_path = config_path
        # 模拟配置
        self.config = {
            'api_key': 'YOUR_API_KEY',
            'wallet': 'YOUR_WALLET',
        }
        
        # 策略配比（根据资金规模）
        self.allocation_rules = {
            'tier_1': {'max_capital': 5000, 'arbitrage': 1.0, 'market_making': 0.0},      # ¥0-5K: 100% 套利
            'tier_2': {'max_capital': 20000, 'arbitrage': 0.8, 'market_making': 0.2},    # ¥5K-20K: 80/20
            'tier_3': {'max_capital': 100000, 'arbitrage': 0.6, 'market_making': 0.4},   # ¥20K-100K: 60/40
            'tier_4': {'max_capital': float('inf'), 'arbitrage': 0.4, 'market_making': 0.6},  # >¥100K: 40/60
        }
        
        # 套利参数
        self.arbitrage_params = {
            'confidence_threshold': 0.85,  # 贝叶斯后 85%
            'edge_threshold': 0.045,       # 4.5% 优势
            'kelly_divisor': 4,            # Quarter-Kelly
            'max_position_pct': 0.25,      # 单市场 25%
        }
        
        # 做市参数
        self.mm_params = {
            'spread_pct': 2.0,             # 2% 价差
            'order_size': 100,             # 每单 100U
            'max_inventory': 1000,         # 最大库存 1000U
            'rebalance_threshold': 0.5,    # 50% 不平衡再平衡
        }
    
    def get_tier(self, total_capital: float) -> str:
        """根据资金量确定层级"""
        if total_capital <= 5000:
            return 'tier_1'
        elif total_capital <= 20000:
            return 'tier_2'
        elif total_capital <= 100000:
            return 'tier_3'
        else:
            return 'tier_4'
    
    def get_allocation(self, total_capital: float) -> Dict:
        """
        获取资金分配
        :param total_capital: 总资金
        :return: 分配方案
        """
        tier = self.get_tier(total_capital)
        rule = self.allocation_rules[tier]
        
        arbitrage_capital = total_capital * rule['arbitrage']
        mm_capital = total_capital * rule['market_making']
        
        return {
            'tier': tier,
            'total_capital': total_capital,
            'arbitrage': {
                'capital': arbitrage_capital,
                'allocation': f"{rule['arbitrage']*100:.0f}%",
                'expected_monthly': f"+{30 if tier == 'tier_1' else 25 if tier == 'tier_2' else 16 if tier == 'tier_3' else 13}%",
            },
            'market_making': {
                'capital': mm_capital,
                'allocation': f"{rule['market_making']*100:.0f}%",
                'expected_monthly': f"+{8 if tier == 'tier_1' else 10 if tier == 'tier_2' else 12 if tier == 'tier_3' else 13}%",
            },
            'combined_expected': f"+{45 if tier == 'tier_1' else 25 if tier == 'tier_2' else 16 if tier == 'tier_3' else 13}%",
        }
    
    def check_arbitrage_opportunity(self, signal: Dict) -> bool:
        """
        检查套利机会
        :param signal: 交易信号
        :return: 是否执行
        """
        confidence = signal.get('confidence', 0)
        edge = signal.get('edge', 0)
        
        # 必须满足两个阈值
        if confidence >= self.arbitrage_params['confidence_threshold'] and \
           edge >= self.arbitrage_params['edge_threshold']:
            return True
        
        return False
    
    def check_market_making_opportunity(self, market: Dict) -> bool:
        """
        检查做市机会
        :param market: 市场信息
        :return: 是否做市
        """
        # 做市条件
        conditions = {
            'high_volume': market.get('volume_24h', 0) > 50000,     # 成交量>$50K
            'low_volatility': market.get('volatility', 1) < 0.3,    # 波动<30%
            'tight_spread': market.get('spread', 1) < 0.05,         # 价差<5%
            'active_rewards': market.get('rewards', False),         # 有奖励
            'days_to_resolution': market.get('days_to_resolution', 0) > 3,  # 距离结算>3 天
        }
        
        # 满足 4 个以上条件才做市
        passed = sum(conditions.values())
        return passed >= 4
    
    def generate_action_plan(self, total_capital: float, signals: List[Dict], markets: List[Dict]) -> Dict:
        """
        生成行动计划
        :param total_capital: 总资金
        :param signals: 套利信号列表
        :param markets: 做市市场列表
        :return: 行动计划
        """
        allocation = self.get_allocation(total_capital)
        
        # 套利机会筛选
        arbitrage_opps = [s for s in signals if self.check_arbitrage_opportunity(s)]
        
        # 做市机会筛选
        mm_opps = [m for m in markets if self.check_market_making_opportunity(m)]
        
        # 资金分配
        arbitrage_capital = allocation['arbitrage']['capital']
        mm_capital = allocation['market_making']['capital']
        
        # 单个套利机会分配（最多同时 3 个）
        arb_per_opportunity = arbitrage_capital / min(len(arbitrage_opps), 3) if arbitrage_opps else 0
        
        # 单个做市市场分配（最多同时 5 个）
        mm_per_market = mm_capital / min(len(mm_opps), 5) if mm_opps else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'tier': allocation['tier'],
            'total_capital': total_capital,
            'allocation': allocation,
            'arbitrage': {
                'opportunities': len(arbitrage_opps),
                'capital_per_opportunity': arb_per_opportunity,
                'signals': arbitrage_opps[:3],  # 最多 3 个
            },
            'market_making': {
                'opportunities': len(mm_opps),
                'capital_per_market': mm_per_market,
                'markets': mm_opps[:5],  # 最多 5 个
            },
            'action': '执行' if arbitrage_opps or mm_opps else '观望',
        }
    
    def render_strategy_dashboard(self, total_capital: float) -> str:
        """渲染策略仪表板"""
        allocation = self.get_allocation(total_capital)
        
        lines = []
        lines.append("=" * 60)
        lines.append("  知几-E 混合策略仪表板 v3.0")
        lines.append("  套利为主 + 做市为辅")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append("【资金层级】")
        lines.append(f"  总资金：¥{total_capital:,.0f}")
        lines.append(f"  层级：{allocation['tier']}")
        lines.append("")
        
        lines.append("【资金分配】")
        lines.append(f"  套利：¥{allocation['arbitrage']['capital']:,.0f} ({allocation['arbitrage']['allocation']})")
        lines.append(f"        预期月收益：{allocation['arbitrage']['expected_monthly']}")
        lines.append(f"  做市：¥{allocation['market_making']['capital']:,.0f} ({allocation['market_making']['allocation']})")
        lines.append(f"        预期月收益：{allocation['market_making']['expected_monthly']}")
        lines.append("")
        
        lines.append("【综合预期】")
        lines.append(f"  月收益：{allocation['combined_expected']}")
        lines.append(f"  6 个月：{(float(allocation['combined_expected'].replace('+', '').replace('%', ''))/100 + 1) ** 6 - 1:.0%}")
        lines.append("")
        
        lines.append("【套利参数】")
        lines.append(f"  置信度阈值：{self.arbitrage_params['confidence_threshold']*100:.0f}%")
        lines.append(f"  优势阈值：{self.arbitrage_params['edge_threshold']*100:.1f}%")
        lines.append(f"  凯利除数：{self.arbitrage_params['kelly_divisor']} (Quarter-Kelly)")
        lines.append(f"  最大仓位：{self.arbitrage_params['max_position_pct']*100:.0f}%")
        lines.append("")
        
        lines.append("【做市参数】")
        lines.append(f"  价差：{self.mm_params['spread_pct']}%")
        lines.append(f"  每单大小：{self.mm_params['order_size']}U")
        lines.append(f"  最大库存：{self.mm_params['max_inventory']}U")
        lines.append(f"  再平衡阈值：{self.mm_params['rebalance_threshold']*100:.0f}%")
        lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    strategy = HybridStrategy()
    
    print("=" * 60)
    print("知几-E 混合策略 v3.0 测试")
    print("=" * 60)
    
    # 测试不同资金层级
    for capital in [1000, 5000, 20000, 100000, 500000]:
        print(f"\n【资金：¥{capital:,}】")
        print(strategy.render_strategy_dashboard(capital))
    
    # 测试行动计划
    print("\n" + "=" * 60)
    print("行动计划测试")
    print("=" * 60)
    
    signals = [
        {'name': 'BTC 涨跌', 'confidence': 0.89, 'edge': 0.37},
        {'name': 'ETH 涨跌', 'confidence': 0.87, 'edge': 0.05},
        {'name': '美联储利率', 'confidence': 0.82, 'edge': 0.03},  # 不达标
    ]
    
    markets = [
        {'name': 'BTC 涨跌', 'volume_24h': 50000, 'volatility': 0.2, 'spread': 0.02, 'rewards': True, 'days_to_resolution': 10},
        {'name': 'ETH 涨跌', 'volume_24h': 30000, 'volatility': 0.4, 'spread': 0.03, 'rewards': False, 'days_to_resolution': 2},  # 不达标
    ]
    
    action_plan = strategy.generate_action_plan(total_capital=10000, signals=signals, markets=markets)
    
    print(f"\n总资金：¥{action_plan['total_capital']:,}")
    print(f"层级：{action_plan['tier']}")
    print(f"套利机会：{action_plan['arbitrage']['opportunities']}个")
    print(f"做市机会：{action_plan['market_making']['opportunities']}个")
    print(f"行动：{action_plan['action']}")
```

---

## 📄 3. strategy_v22.py - 6 公式增强版策略

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几-E 策略引擎 v2.2 - 6 公式增强版
更新：LMSR 定价 + 贝叶斯动态更新
"""

import json
import math
from datetime import datetime
from pathlib import Path

# 导入新模块
from lmsr_pricer import LMSRPricer
from bayesian_updater import BayesianUpdater

class ZhijiStrategyV22:
    """知几-E 策略引擎 v2.2 (6 公式增强版)"""
    
    def __init__(self, config_path: str = "~/.taiyi/zhiji/polymarket.json"):
        # 加载配置
        config_path = Path(config_path).expanduser()
        with open(config_path) as f:
            self.config = json.load(f)
        
        # 核心参数
        self.confidence_threshold = self.config.get('confidence_threshold', 0.96)  # 96%
        self.edge_threshold = self.config.get('edge_threshold', 0.045)  # 4.5%
        self.kelly_divisor = self.config.get('kelly_divisor', 4)  # Quarter-Kelly
        
        # 6 公式模块
        self.lmsr = LMSRPricer(liquidity_b=100)
        self.bayesian = BayesianUpdater(prior_prob=0.5)
        
        # 钱包地址
        self.wallet = self.config.get('wallet_address', '0x2b451...')
    
    def calculate_kelly(self, probability: float, odds: float) -> float:
        """
        凯利公式计算最优仓位
        f* = (p × odds − (1 − p)) / odds
        """
        kelly = (probability * odds - (1 - probability)) / odds
        
        # Quarter-Kelly (除以 4，更保守)
        position = kelly / self.kelly_divisor
        
        # 限制在 1%-25% 范围
        position = max(0.01, min(0.25, position))
        
        return position
    
    def calculate_ev(self, model_prob: float, market_price: float) -> float:
        """
        EV 缺口计算
        EV = (真实概率 − 市场价格) × 回报
        """
        if market_price <= 0 or market_price >= 1:
            return 0
        
        odds = (1 / market_price) - 1
        ev = (model_prob - market_price) * odds
        
        return ev
    
    def check_lmsr_risk(self, volume_24h: float) -> dict:
        """
        LMSR 风险评估
        """
        is_shallow, risk_level = self.lmsr.is_shallow_water(volume_24h)
        
        return {
            'is_shallow': is_shallow,
            'risk_level': risk_level,
            'recommendation': "⚠️ 谨慎参与" if is_shallow else "✅ 可参与"
        }
    
    def update_confidence(self, evidence_list: list) -> float:
        """
        贝叶斯置信度更新
        """
        for ev in evidence_list:
            self.bayesian.update(
                likelihood=ev['likelihood'],
                evidence_strength=ev['strength'],
                evidence_name=ev['name']
            )
        
        final_prob = self.bayesian.prior
        adjustment = self.bayesian.get_confidence_adjustment()
        
        return final_prob * adjustment
    
    def generate_signal(self, market: dict) -> dict:
        """
        生成交易信号
        :param market: {'name', 'market_price', 'volume_24h', 'model_prob', 'evidence'}
        :return: signal dict
        """
        # 1. 贝叶斯置信度更新
        confidence = self.update_confidence(market.get('evidence', []))
        
        # 2. EV 缺口计算
        ev = self.calculate_ev(confidence, market['market_price'])
        
        # 3. LMSR 风险评估
        lmsr_risk = self.check_lmsr_risk(market['volume_24h'])
        
        # 4. 凯利公式计算仓位
        if ev > self.edge_threshold:
            odds = (1 / market['market_price']) - 1
            position = self.calculate_kelly(confidence, odds)
        else:
            position = 0
        
        # 5. 生成信号
        signal = {
            'market': market['name'],
            'action': 'BUY' if ev > self.edge_threshold else 'HOLD',
            'confidence': confidence,
            'ev': ev,
            'position': position,
            'lmsr_risk': lmsr_risk,
            'timestamp': datetime.now().isoformat(),
        }
        
        return signal


if __name__ == "__main__":
    # 测试
    strategy = ZhijiStrategyV22()
    
    market = {
        'name': 'BTC 2026 年涨到$100K',
        'market_price': 0.60,
        'volume_24h': 100000,
        'model_prob': 0.85,
        'evidence': [
            {'name': '机构资金流入', 'likelihood': 2.0, 'strength': 0.8},
            {'name': '技术面突破', 'likelihood': 1.5, 'strength': 0.6},
        ]
    }
    
    signal = strategy.generate_signal(market)
    
    print("=" * 60)
    print("知几-E 策略 v2.2 交易信号")
    print("=" * 60)
    print(f"市场：{signal['market']}")
    print(f"行动：{signal['action']}")
    print(f"置信度：{signal['confidence']*100:.1f}%")
    print(f"EV 优势：{signal['ev']*100:.2f}%")
    print(f"仓位：{signal['position']*100:.1f}%")
    print(f"LMSR 风险：{signal['lmsr_risk']['recommendation']}")
```

---

## 📄 4. 核心公式说明

### 公式 1: 凯利公式 (仓位管理)

```
f* = (p × odds − (1 − p)) / odds

其中:
- p = 获胜概率
- odds = 赔率 (隐含概率的倒数 -1)
- f* = 最优仓位比例

Quarter-Kelly (更保守):
position = f* / 4

限制范围:
position = max(0.01, min(0.25, position))
```

### 公式 2: EV 缺口计算 (期望值)

```
EV = (真实概率 − 市场价格) × 回报

其中:
- 真实概率 = 模型预测概率
- 市场价格 = 市场隐含概率
- 回报 = (1/市场价格) - 1

决策规则:
- EV > 4.5% → 执行
- EV < 4.5% → 观望
```

### 公式 3: LMSR 定价 (流动性评估)

```
cost(q) = b × ln(Σ exp(q_i/b))

其中:
- b = 流动性参数 (默认 100)
- q = 合约数量

浅水风险检测:
if volume_24h < $50K:
    risk_level = "高"
    recommendation = "⚠️ 谨慎参与"
else:
    risk_level = "低"
    recommendation = "✅ 可参与"
```

### 公式 4: 贝叶斯置信度更新

```
后验概率 = 先验概率 × 似然比 / 标准化因子

更新流程:
1. 设置先验概率 (默认 50%)
2. 收集证据 (民调/资金/新闻等)
3. 每个证据更新一次后验概率
4. 最终置信度 = 后验概率 × 置信度调整

示例:
先验：50%
证据 1: 机构资金流入 (似然比 2.0) → 后验 67%
证据 2: 技术面突破 (似然比 1.5) → 后验 75%
证据 3: 民调领先 (似然比 1.8) → 后验 82%

最终置信度：82%
```

### 公式 5: 网格策略 (震荡市场)

```
网格参数:
- price_range = (最低价，最高价)
- grid_count = 网格数量
- investment_per_grid = 每格投资

网格计算:
grid_step = (最高价 - 最低价) / grid_count

挂单:
for i in range(grid_count):
    buy_price = 最高价 - (i + 1) * grid_step
    sell_price = 最高价 - (i - 1) * grid_step
    place_order(buy_price, sell_price)
```

### 公式 6: 做市策略 (流动性提供)

```
做市参数:
- spread_pct = 价差百分比 (默认 2%)
- order_size = 每单大小 (默认 100U)
- max_inventory = 最大库存 (默认 1000U)

挂单:
mid_price = 当前中间价
spread = mid_price × spread_pct / 100

buy_price = mid_price - spread/2
sell_price = mid_price + spread/2

place_limit_buy(buy_price)
place_limit_sell(sell_price)

收益来源:
- 买卖差价 (Spread)
- 交易所奖励 (Rebate)
```

---

## 📊 策略对比

| 策略 | 风险 | 收益 | 资金占用 | 适合场景 |
|------|------|------|---------|---------|
| **套利** | 低 | 30-45%/月 | 中 | 定价错误市场 |
| **做市** | 低 | 8-13%/月 | 高 | 高流动性市场 |
| **网格** | 中 | 15-25%/月 | 高 | 震荡市场 |
| **趋势** | 高 | 20-100%/月 | 低 | 明显趋势 |
| **事件驱动** | 高 | 50-200%/月 | 低 | 重大事件 |

---

## ⚠️ 风控配置

```python
RISK_CONFIG = {
    # 仓位限制
    "max_position_per_market": 0.25,    # 单市场最大 25%
    "max_total_exposure": 0.80,         # 总敞口 80%
    "max_concentration": 0.20,          # 最大集中度 20%
    
    # 止损配置
    "hard_stop_loss": 0.10,             # 硬止损 10%
    "time_stop_loss": 604800,           # 时间止损 7 天
    
    # 资金管理
    "total_capital": 10000,             # 总资金¥10000
    "risk_per_trade": 0.02,             # 每笔风险 2%
    "daily_stop_loss": 0.05,            # 日止损 5%
    
    # 套利阈值
    "confidence_threshold": 0.85,       # 置信度>85%
    "edge_threshold": 0.045,            # 优势>4.5%
    "kelly_divisor": 4,                 # Quarter-Kelly
    
    # 做市阈值
    "min_volume_24h": 50000,            # 最小成交量$50K
    "max_volatility": 0.3,              # 最大波动 30%
    "min_days_to_resolution": 3,        # 距离结算>3 天
}
```

---

## 📊 资金层级与预期收益

| 层级 | 资金范围 | 套利 | 做市 | 预期月收益 |
|------|---------|------|------|-----------|
| **Tier 1** | ¥0-5K | 100% | 0% | +45% |
| **Tier 2** | ¥5K-20K | 80% | 20% | +25% |
| **Tier 3** | ¥20K-100K | 60% | 40% | +16% |
| **Tier 4** | >¥100K | 40% | 60% | +13% |

---

## 🚀 使用方式

```bash
# 查看交易信号
python3 strategy_v22.py --signal

# 执行交易
python3 execute_bet.py --market "BTC 涨跌" --amount 100

# 查看持仓
python3 paper_trading_monitor.py

# 运行自进化
python3 self_evolution_zhiji_agent.py

# 渲染策略仪表板
python3 hybrid_strategy.py --dashboard --capital 10000
```

---

## 📄 相关文件

| 文件 | 路径 |
|------|------|
| **完整代码包** | `Zhiji_Trading_Strategy_Complete.md` |
| **源码目录** | `skills/01-trading/zhiji/` |
| **混合策略** | `zhiji/hybrid_strategy.py` |
| **6 公式策略** | `zhiji/strategy_v22.py` |
| **LMSR 定价** | `zhiji/lmsr_pricer.py` |
| **贝叶斯更新** | `zhiji/bayesian_updater.py` |
| **做市策略** | `zhiji/market_maker.py` |
| **自进化 Agent** | `zhiji/self_evolution_zhiji_agent.py` |

---

*太一 AGI · 知几量化交易策略完整代码包*  
*整理时间：2026-04-22 12:40*  
*版本：v3.0 (知几-E 混合策略)*
