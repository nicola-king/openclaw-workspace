---
name: trade-travel-design
version: 1.0.0
description: 品牌设计引擎 - 将awesome-design-md的70个品牌设计规范应用到跨境贸易和旅游探路者
category: design
tags: ['brand', 'design-system', 'ui', 'marketing', 'cross-border-trade', 'travel']
author: 太一 AGI
status: active
---

# 品牌设计引擎 (Trade & Travel Design)

> 基于 VoltAgent/awesome-design-md (68.4K⭐) 的品牌设计智能应用层

## 能力

- **70 个品牌设计规范**：Apple、Stripe、Tesla、Airbnb、Binance、Ferrari...
- **跨境贸易场景**：品牌落地页、营销邮件、社媒帖子
- **旅游探路者场景**：旅行手册、行程单、攻略页面

## 使用方式

### CLI
```bash
cd /home/sayelf/.openclaw/workspace/skills/trade-travel-design
python3 design-engine.py list              # 列出70个品牌
python3 design-engine.py show stripe       # 查看Stripe设计规范
python3 design-engine.py trade stripe "Payment" "US-EU"  # 跨境贸易生成
python3 design-engine.py travel airbnb 大理                 # 旅游推广生成
```

### 场景推荐

| 场景 | 推荐品牌 |
|------|---------|
| 跨境贸易 - 高端品牌 | Apple, Tesla, Stripe, Ferrari |
| 跨境贸易 - 科技感 | Vercel, Linear, Notion, Cursor |
| 跨境贸易 - 金融感 | Stripe, Binance, Coinbase, Mastercard |
| 跨境贸易 - 电商 | Shopify, Airbnb, Nike, Zapier |
| 旅游探路者 - 酒店 | Airbnb, Starbucks, Nike |
| 旅游探路者 - 科技旅行 | Uber, Tesla, Vercel |
| 旅游探路者 - 奢华 | Ferrari, Lamborghini, BMW-M |

## 品牌设计规范存储

`notes/awesome-design-md/design-md/<brand>/DESIGN.md`
