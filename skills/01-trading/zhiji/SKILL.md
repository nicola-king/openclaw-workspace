---
name: zhiji
version: 2.0.0
description: 知几 - 统一量化交易调度引擎 (整合币安/GMGN/Polymarket)
category: trading
tags: ['zhiji', 'quant', 'strategy', 'polymarket', 'gmgn', 'binance', 'unified']
author: 太一 AGI
created: 2026-04-07
updated: 2026-04-22 13:00
---


# Zhiji - 知几统一量化交易调度引擎

> 版本：v2.0 (整合版) | 更新：2026-04-22 | 负责 Bot：知几

---

## 🎯 职责

**统一量化交易调度与执行**，整合:
- Polymarket 预测市场 (知几-E 策略)
- GMGN 链上交易
- 币安交易所 (现货/合约)

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────┐
│            知几统一交易调度器 v2.0                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │              策略信号生成层                      │   │
│  │  知几-E (Polymarket) | GMGN | 币安 Agent        │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │              资金分配层                          │   │
│  │  根据信号置信度/策略权重动态分配                 │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │              统一执行层                          │   │
│  │  Polymarket 执行器 | GMGN 执行器 | 币安执行器    │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │              风控监控层                          │   │
│  │  仓位管理 | 止损检查 | 性能监控 | 自进化学习    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 使用命令

```bash
# 运行统一调度器
python3 unified_trading_scheduler.py

# 查看交易信号
python3 unified_trading_scheduler.py --signals

# 查看资金分配
python3 unified_trading_scheduler.py --allocation

# 查看持仓
python3 paper_trading_monitor.py

# 查看性能报告
python3 unified_trading_scheduler.py --report
```

---

## 📁 目录结构

| 目录/文件 | 说明 |
|----------|------|
| `unified_trading_scheduler.py` | 统一调度器 (核心) |
| `hybrid_strategy.py` | 混合策略引擎 v3.0 |
| `strategy_v22.py` | 6 公式增强版策略 |
| `binance-trading/` | 币安交易模块 |
| `gmgn/` | GMGN 交易模块 |
| `polymarket/` | Polymarket 交易模块 |
| `sentiment/` | 情绪分析 |
| `self_evolution_zhiji_agent.py` | 自进化 Agent |

---

## 📊 资金分配策略

### 默认配置

| 平台 | 分配比例 | 策略重点 |
|------|---------|---------|
| **Polymarket** | 30% | 套利 + 做市 |
| **GMGN** | 30% | 链上交易 |
| **币安** | 30% | 现货/合约 |
| **保留现金** | 10% | 风险缓冲 |

### 动态调整

根据信号置信度自动调整:
```python
# 高置信度信号 (>80%)
allocation = 0.8  # 最多 80% 资金

# 中置信度信号 (60-80%)
allocation = 0.5  # 最多 50% 资金

# 低置信度信号 (<60%)
allocation = 0.2  # 最多 20% 资金
```

---

## ⚠️ 风控配置

```python
RISK_CONFIG = {
    # 仓位限制
    "max_position_per_trade": 0.25,    # 单笔最大 25%
    "max_total_exposure": 0.80,         # 总敞口 80%
    "max_concentration_per_platform": 0.30,  # 单平台最大 30%
    
    # 止损配置
    "hard_stop_loss": 0.10,             # 硬止损 10%
    "daily_stop_loss": 0.05,            # 日止损 5%
    "max_drawdown": 0.15,               # 最大回撤 15%
    
    # 策略权重
    "arbitrage": 0.4,                   # 套利 40%
    "market_making": 0.2,               # 做市 20%
    "trend_following": 0.2,             # 趋势 20%
    "grid_trading": 0.2,                # 网格 20%
}
```

---

## 📈 预期性能

| 指标 | 目标 | 说明 |
|------|------|------|
| **月收益率** | 15-30% | 多平台组合 |
| **最大回撤** | <15% | 严格风控 |
| **胜率** | >60% | 策略优化 |
| **夏普比率** | >2.5 | 风险调整后收益 |
| **自动化率** | >95% | 几乎无需人工 |

---

## 🔗 相关文档

- `constitution/workflows/QUANT-TRADING.md` - 量化交易工作流
- `constitution/directives/TURBOQUANT.md` - TurboQuant 记忆
- `Binance_Trading_Agent_Complete.md` - 币安 Agent 代码包
- `Zhiji_Trading_Strategy_Complete.md` - 知几策略代码包

---

*创建：2026-04-03 22:57 | 更新：2026-04-22 13:00 | 太一 AGI*
