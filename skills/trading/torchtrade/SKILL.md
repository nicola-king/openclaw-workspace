---
name: torchtrade-integration
version: 1.0.0
description: torchtrade-integration skill
category: trading
tags: []
author: 太一 AGI
created: 2026-04-07
---


# TorchTrade Integration - 量化交易集成

> 版本：v1.0 | 创建：2026-04-04 | 负责 Bot：素问

---

## 🎯 职责

**TorchTrade 量化交易框架集成**

- RuleBasedActor 规则执行器
- Binance K 线数据接入
- 策略回测与实盘交易

---

## 🔧 核心组件

| 文件 | 说明 |
|------|------|
| `rule_based_actor.py` | 规则驱动执行器 (6KB) |
| `requirements.txt` | Python 依赖 |
| `config.yaml` | 交易配置 |

---

## 📊 技术栈

- **框架**: TorchTrade
- **交易所**: Binance (现货/合约)
- **语言**: Python 3.12+
- **依赖**: torch, pandas, numpy, ccxt

---

## 🚀 使用示例

```python
from torchtrade_integration import RuleBasedActor

actor = RuleBasedActor(config='config.yaml')
actor.execute(signal='BUY', symbol='BTCUSDT', size=0.01)
```

---

## 📈 回测结果

| 策略 | 收益率 | 胜率 | 交易次数 |
|------|--------|------|---------|
| v2.1 (气象) | 0% | - | 0 |
| v3.0 (情绪增强) | +5.38% | 100% | 2 |

---

## 🔗 相关文档

- `constitution/directives/TURBOQUANT.md` - 智能分离协议
- `skills/zhiji/` - 知几量化策略

---

*创建：2026-04-04 10:08 | 素问 AGI*
