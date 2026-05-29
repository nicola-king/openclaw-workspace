---
name: trading-agents
version: 1.0.0
description: 太一多智能体交易引擎 — TradingAgents (80K⭐) 融合版
category: trading
tags: ['trading', 'finance', 'multi-agent', 'llm', 'trading-agents', 'gmgn', 'polymarket', 'quant']
author: 太一 AGI
created: 2026-05-29
status: active
trigger: 当需要交易分析/市场研究/选股/策略回测/投资决策时自动路由
---

# 📈 太一多智能体交易引擎

> 基于 TauricResearch/TradingAgents (80K⭐) + KylinMountain/TradingAgents-AShare (OpenClaw集成)
> 融合GMGN链上数据 + Polymarket预测市场

---

## 🧠 智能调度规则

| 用户说 | 路由 | 说明 |
|--------|------|------|
| "分析/研究这个币/股票" | trading-agents:analyze | 多Agent多维度分析 |
| "交易/买卖信号" | trading-agents:signal | Agent辩论→交易决策 |
| "市场/大盘怎么看" | trading-agents:market | 宏观情绪+板块分析 |
| "回测这个策略" | trading-agents:backtest | 历史数据验证 |
| "投研报告" | trading-agents:research | 机构级分析报告 |
| "风控/仓位/止损" | trading-agents:risk | 风险管理决策 |
| "GMGN/链上数据" | gmgn:query | 走GMGN Bot查链上 |
| "Polymarket/预测" | polymarket:analyze | 预测市场分析 |

### 自动识别特征

```
"分析" + 代币/股票名 → TradingAgents 多Agent分析
"买/卖" + 信号 → Agent辩论决策
"风险/仓位" → 风控Agent
"链上" → GMGN集成
"预测市场" → Polymarket集成
```

---

## 🏗 架构（参考 TradingAgents）

```
用户请求
    │
    ├─ 分析Agent (基本面/技术面/情绪面)
    ├─ 辩论引擎 (多Agent对抗式讨论)
    ├─ 决策层 (加权投票→BUY/SELL/HOLD)
    ├─ 风控层 (仓位/止损/风险评分)
    └─ 执行层 (GMGN/Polymarket/exchange)
```

### 7大Agent角色（TradingAgents 多智能体）

| Agent | 职责 | 分析维度 |
|-------|------|---------|
| 📊 技术分析师 | 图表/指标/趋势 | MA/RSI/MACD/Bollinger |
| 📰 新闻分析师 | 舆情/消息面 | 新闻情感/事件驱动 |
| 📈 基本面分析师 | 估值/财报/链上数据 | PE/PB/Tokenomics |
| 🧠 宏观分析师 | 宏观经济/政策 | 利率/通胀/政策 |
| ⚡ 情绪分析师 | 市场情绪/FOMO/FUD | 社交媒体/资金流向 |
| 🔒 风控官 | 风险管理 | 仓位/止损/黑天鹅 |
| 🎯 决策官 | 综合裁决 | 加权投票→最终信号 |

---

## 🔌 调用方式

```python
from skills.trading_agents.engine import (
    analyze,         # 多Agent分析
    debate,          # Agent辩论
    signal,          # 交易信号
    backtest,        # 回测
    risk_check,      # 风控
    report,          # 投研报告
    check,           # 系统检测
)
```

### 一键命令

```
/交易 "分析BTC"
/交易 debate "SOL vs ETH 哪个更好"
/交易 signal "现在适合买什么"
/交易 risk "当前仓位风险评估"
/交易 backtest "突破MA20买入策略"
/交易 report "BTC周报"
```

---

## 🔗 相关资源

- TradingAgents: https://github.com/TauricResearch/TradingAgents (80K⭐)
- AShare OpenClaw版: https://github.com/KylinMountain/TradingAgents-AShare (457⭐)
- MCP Mode: https://github.com/guangxiangdebizi/TradingAgents-MCPmode (310⭐)
- Telegram Bot: https://github.com/IvanWng97/TradingAgents-Telegram (42⭐)
- Polymarket Paper: https://github.com/agent-next/polymarket-paper-trader (341⭐)
- GMGN: gmgn.ai (已接入)
