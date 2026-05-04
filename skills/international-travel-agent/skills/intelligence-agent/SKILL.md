---
name: travel-intelligence-agent
version: 1.0.0
description: 旅游综合情报引擎 - 多平台搜索/权重评分/性价比排序/情感引导/大V博主
category: travel
tags: ['travel-intelligence', 'ranking', 'influencers', 'value-analysis', 'platform-search']
author: 太一 AGI
created: 2026-05-04
status: active
---

# 旅游综合情报引擎 v1.0

> 独立 Skill: 挂在旅游探路者 Agent 下

## 功能

| 能力 | 方法 | 说明 |
|------|------|------|
| 多平台搜索 | `search_all_platforms()` | 覆盖49个国内外旅游平台 |
| 权重评分 | `score_item()` | 价格/评分/位置/评论/独特性 加权 |
| 性价比排序 | `rank_by_value()` | (评分+情感)/价格 排序 |
| 情感引导 | `emotional_guide()` | 4档情感文案 |
| 价值分析 | `value_analysis()` | 预算友好度分析 |
| 大V/博主搜索 | `search_influencers()` | 44位大V·12平台 |
| 大V输出 | `format_influencers()` | 含粉丝/风格/链接/搜索 |

## 大V覆盖 (44位)

| 分类 | 平台 | 代表大V |
|------|------|---------|
| 🎬 旅游 | 抖音/B站/小红书/YouTube | 房琪kiki/MarkWiens |
| 📸 美学 | B站/抖音/Instagram | Thomas看看世界/Brandon Woelfel |
| 📜 历史 | B站/抖音/YouTube/Instagram | 中国国家地理/History Hit |
| 🏮 文化 | YouTube/穷游/马蜂窝 | 李子柒/Drew Binsky |

## 使用

```python
from intelligence_agent import TravelIntelligence

engine = TravelIntelligence("新加坡")

# 搜索平台
links = engine.search_all_platforms("酒店")

# 搜索大V
influencers = engine.search_influencers("新加坡旅游")
print(engine.format_influencers(influencers))

# 性价比排序
ranked = engine.recommend("hotel", hotels, budget=30000)
```

## 49个搜索平台

携程/飞猪/美团/去哪儿/同程/途牛/马蜂窝/穷游
小红书/抖音/B站/视频号/微博/大众点评
Booking/Agoda/Expedia/Kayak/Skyscanner
TripAdvisor/KLOOK/Viator/GetYourGuide
Google/YouTube/Instagram/Twitter/Facebook
Airbnb/Hostelworld/Rome2Rio/Omio/Trainline
Uber/Grab/Gojek/Lonely Planet/Wise/XE

---

*太一旅游探路者 v2.0 · 情报引擎子Skill*
