---
name: search-agent
description: 太一穿透式搜索 Agent — 三层穿透·四步提取·动态国家识别·智能自动化
version: 1.0.0
author: 太一 AGI
created: 2026-05-08
updated: 2026-05-08
status: active
category: search
tags: ['search', 'penetrating', 'scraping', 'intelligence', 'automation']
---

# 🔍 太一穿透式搜索 Agent

> **三层穿透 · 四步提取 · 动态国家识别 · 智能自动化**

---

## 🏗 架构

```
用户指令: "查中东折叠房屋买家"
         │
         ▼
┌──────────────────────────────────────────────┐
│  search_automation.py (智能识别层)            │
│  自动识别国家 → 生成搜索计划 → 调度引擎      │
└──────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│  penetrating_search.py (穿透执行层)           │
│                                              │
│  Layer 1: cloudscraper + 50+UA指纹轮换       │
│  Layer 2: Chrome for Testing 头渲染          │
│  Layer 3: 代理自动切换 (Clash↔直连)          │
└──────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│  四步提取                                     │
│  ① 搜到 → ② 爬取 → ③ 验证(5项) → ④ 入库    │
└──────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│  跨贸 Agent 管道                              │
│  BuyerIntel → IntelligenceHub → ReportEngine  │
│  → art-agent美化 → PDF → Telegram            │
└──────────────────────────────────────────────┘
```

---

## 🧩 核心能力

### 三层穿透
| 等级 | 方法 | 适用 |
|:----:|:----|:----|
| 🟢 L1 | cloudscraper + 50+UA轮换 | 普通网站 |
| 🟡 L2 | Chrome for Testing 头渲染 | JS挑战/SPA/Cloudflare |
| 🔴 L3 | 代理切换(Clash↔直连) + 智能重试 | CAPTCHA/封IP |

### 四步提取
```
搜到 → 多引擎搜索(DDG/Bing/Google/SearXNG)
  ↓
爬到 → 穿透式抓取所有关联页面
  ↓
验证 → 5项验证(官网/电话/邮箱/LinkedIn/第三方)
  ↓
入库 → BuyerIntel → IntelligenceHub → 报告
```

### 动态国家识别 (7国)
| 国家 | 自动识别 | 搜索策略 | 认证要求 |
|:----|:--------:|:--------|:--------:|
| 🇸🇦 沙特 | KSA/Saudi/沙特 | 阿拉伯语搜索+Etimad招标 | SASO |
| 🇦🇪 阿联酋 | UAE/Dubai | 英语搜索+etenders.ae | ESMA |
| 🇮🇶 伊拉克 | Iraq/伊拉克 | 英语+UNDP搜索 | — |
| 🇶🇦 卡塔尔 | Qatar/卡塔尔 | 英语搜索 | QSAS |
| 🇦🇺 澳洲 | Australia/澳洲 | 英语搜索+prefabAUS | NCC/CodeMark |
| 🇺🇸 美国 | USA/美国 | 英语搜索+sam.gov | ASTM/IBC |
| 🇨🇳 中国 | China/中国 | 中文搜索+阿里巴巴 | ISO/CE |

---

## 🚀 使用方式

### 单一公司穿透搜索
```bash
python3 scripts/penetrating_search.py company "Afco Steel"
# → 官网/邮箱/电话/LinkedIn/置信度
```

### 批量买家搜索
```bash
python3 scripts/penetrating_search.py buyers "foldable house" "Saudi"
# → 搜10个买家 + 每个穿透式提取联系方式
```

### 智能自动化扫描
```bash
python3 scripts/search_automation.py sweep "foldable house" "Saudi"
# → 自动识别沙特 → 7个搜索词 → 穿透提取 → 入库

python3 scripts/search_automation.py monitor
# → 全量监控7国×3产品 = 21组合
```

### 跨贸管道集成
```bash
# BuyerIntel → IntelligenceHub → ReportEngine → art-agent → PDF → Telegram
```

---

## 🔧 依赖

| 组件 | 路径 | 说明 |
|:-----|:-----|:-----|
| penetrating_search.py | `scripts/penetrating_search.py` | 穿透式搜索核(422行) |
| search_automation.py | `scripts/search_automation.py` | 智能自动化引擎(420行) |
| shared_search_service.py | `skills/shared-search-agent/` | 共享搜索服务(600+行) |
| scraper_v4.py | `scripts/scraper_v4.py` | 自适应爬虫(663行) |
| Chrome for Testing | `/home/sayelf/.local/bin/chrome-for-testing` | 浏览器渲染(242MB) |

---

## 📊 支持的命令

| 命令 | 功能 | 输出 |
|:-----|:-----|:-----|
| `company <公司名>` | 穿透搜索单个公司 | 联系方式+置信度 |
| `buyers <产品> <地区>` | 批量搜索买家 | 买家列表+联系方式 |
| `sweep <产品> [国家]` | 智能扫描市场 | 完整报告+推荐 |
| `monitor` | 全量监控 | 多市场汇总 |
| `countries` | 查看支持国家 | 国家列表+认证要求 |

---

## 🔄 自进化

每次搜索执行后：
1. 记录搜索结果和命中率
2. 优化搜索关键词权重
3. 更新国家数据库
4. 学习反爬策略

---

*太一穿透式搜索 Agent v1.0 · 三层穿透·四步提取·智能自动化*
