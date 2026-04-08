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
