---
skill: polymarket
version: 1.0.0
author: 太一
created: 2026-03-20
updated: 2026-04-04
status: stable
triggers: ['Polymarket', '预测市场', '下注', '交易执行', 'prediction market', 'betting']
permissions: ['exec', 'web_fetch', 'message']
max_context_tokens: 4000
priority: 1
description: Polymarket 预测市场数据获取与交易执行
tags: ['trading', 'prediction', 'crypto']
config: {'require_approval': True, 'max_bet_usd': 100}
category: trading
---



# Polymarket 技能

## 功能
- 获取市场列表和价格
- 分析市场机会
- 执行交易（需岖丁授权）

## 使用方式
- 由知几调用：获取数据、分析机会
- 由岖丁调用：执行交易

## 依赖
- POLYMARKET_API_KEY（配置于 agents.zhiji.env）
- POLYCLAW_PRIVATE_KEY（配置于 agents.paoding.env）
- Chainstack Polygon RPC
