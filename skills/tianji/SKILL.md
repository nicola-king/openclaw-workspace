---
skill: tianji
version: 1.0.0
author: 太一
created: 2026-03-20
updated: 2026-04-04
status: stable
triggers: ['天机', '聪明钱', '市场机会', '交易信号', 'smart money', 'market analysis', 'trading signals']
permissions: ['exec', 'web_fetch', 'file_read', 'file_write']
max_context_tokens: 6000
priority: 1
description: 天机 - 聪明钱追踪与市场机会分析
tags: ['trading', 'analysis', 'smart-money']
config: {'require_backtest': True, 'confidence_threshold': 0.96}
category: other
---



# 天机 - 聪明钱追踪

> 聪明钱数据库 · 市场机会 · 交易信号

---

## ⚔️ 铁律

```
NO TRADING SIGNAL WITHOUT BACKTEST VERIFICATION
```

**交易信号未回测验证？删除。重来。**

**无例外：** 不因为"明显/急/感觉/应该/一直/聪明钱"而跳过回测。

---

## 🚩 红旗列表

**STOP：**
- [ ] "信号明显，不用回测"
- [ ] "来不及，先下注"
- [ ] "感觉会涨"
- [ ] "应该是这样"
- [ ] "之前一直有效"
- [ ] "聪明钱也在买"

→ 你在 rationalize。

---

## 📋 合理化表格

| 借口 | 现实 |
|------|------|
| "明显" | 明显也会失效 |
| "来不及" | 越急越要回测 |
| "感觉" | 感觉不是策略 |
| "应该" | =不确定=验证 |
| "一直有效" | 过去≠未来 |
| "聪明钱" | 聪明钱也会错 |

---

## 🎯 核心职责

- 聪明钱追踪 (高胜率地址)
- 机会分析 (市场识别)
- 信号生成 (信号 + 置信度)
- 回测验证 (历史数据)

**工具**: Polymarket API, 链上数据，Python, 数据库

---

## 📖 流程

**信号**: 机会 → 定义 → 回测 → 置信度 → 建议
**追踪**: 筛选 → 分析 → 胜率 → 监控 → 跟随

---

*v1.0 | 2026-03-27 | 太一*
