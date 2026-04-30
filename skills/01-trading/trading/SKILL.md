---
name: trading
version: 1.0.0
description: 交易引擎 - 币安/Polymarket/TorchTrade 统一封装
category: trading
tags: ['trading', 'binance', 'polymarket', 'crypto', '交易，币安，预测市场']
author: 太一 AGI
created: 2026-04-07
status: active
priority: P1
---


# Trading v1.0 - 统一交易引擎

> **版本**: 1.0.0 (整合版) | **创建**: 2026-04-07
> **负责 Bot**: 知几 | **状态**: ✅ 已激活

---

## 📋 功能概述

统一交易技能，整合 3 个交易平台。

**整合内容**:
- ✅ binance-trader → binance/
- ✅ polymarket → polymarket/
- ✅ torchtrade-integration → torchtrade/

**独立保留**:
- zhiji (知几策略 Bot)
- zhiji-sentiment (情绪分析)
- portfolio-tracker (组合追踪)

---

## 🏗️ 架构设计

```
trading/
├── SKILL.md (主入口)
├── binance/ (币安)
│   ├── client.py
│   └── strategies.py
├── polymarket/ (Polymarket)
│   ├── client.py
│   └── strategies.py
└── torchtrade/ (TorchTrade)
    └── integration.py
```

---

## ⚠️ 金融执行警告

所有交易操作涉及真实资金:
- ✅ 必须用户明确确认
- ✅ 记录交易日志
- ✅ 设置风控限制

---

## 📋 变更日志

### v1.0.0 (2026-04-07)
- ✅ 整合 3 个交易技能
- ✅ 统一交易接口
- ✅ 保留 zhiji/portfolio-tracker 独立

---

*维护：知几 AGI | Trading v1.0*
