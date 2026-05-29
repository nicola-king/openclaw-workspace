---
name: taiyi-search
description: 太一统一搜索引擎（唯一搜索入口）— 蒸馏合并自 AnySearch + shared-search + search-agent + Scrapling
version: 2.1.0
author: 太一 AGI
tags: [search, web, intelligence, anysearch, vertical-search, penetrating-search, scrapling, anti-bot]
trigger: 当 Agent 需要搜索信息、查证事实、提取网页内容时，默认且唯一的搜索工具
---

# 🔍 太一统一搜索引擎 v2.1 — Scrapling 集成

蒸馏合并自：`anysearch-skill`（统一搜索API）+ `shared-search-agent`（缓存路由）+ `search-agent`（穿透方法论）+ `D4Vinci/Scrapling ⭐54K`（反爬绕过+智能提取）

## 一键使用

```
帮我搜 "xxx"
查一下 xxx 的最新消息
提取这个链接的内容 xxx
搜一下 xxx 领域的最新动态
把这个反爬的网页内容弄出来 —— 会自调用 Scrapling 绕过
```

## 能力矩阵

| 能力 | 命令 | 说明 |
|------|------|------|
| **通用搜索** | `search(query, max, freshness)` | 任意关键词，支持时效筛选 |
| **批量穿透** | `deep_search([q1,q2...])` | 多角度聚合搜索 |
| **URL提取** | `extract_url(url)` | 获取完整页面内容（含 Scrapling 自动降级） |
| **Scrapling 智能抓取** | `scrapling_fetch(url)` | 自动路由反爬绕过 |
| **元素提取** | `extract_elements(html, css/xpath)` | CSS/XPATH 从源码提取 |
| **自适应提取** | `adaptive_extract(html, target_text)` | 文本定位 + 自动 CSS 选择器生成 |
| **批量采集** | `batch_fetch([url1, url2...])` | 并发批量抓取 |
| **垂直搜索** | `search(query, domain, sub_domain)` | 23个垂直领域 |
| **国家解析** | `resolve_country("沙特")` | 国家名称→代码 |
| **搜索链接** | `gen_search_links("battery","australia")` | 多平台搜索URL |
| **搜索统计** | `stats.summary()` | 近7天搜索量 |

## 🤖 10层永不放弃抓取链路（100%命中目标）

### 抓取链路

```
用户说"提取这个页面内容"
    │
    ├── L1: AnySearch CLI          — 零成本搜索API
    ├── L2: web_fetch (OpenClaw)    — 原生工具
    ├── L3: requests + Clash 代理   — 透明代理请求
    ├── L4: Scrapling Fetcher       — 基本HTTP
    ├── L5: Scrapling StealthyFetcher — Cloudflare绕过 ⚡
    ├── L6: cloudscraper            — 另一套CF绕过
    ├── L7: Scrapling DynamicFetcher — JS渲染
    ├── L8: Playwright 无头浏览器    — 完整浏览器指纹
    ├── L9: Google Cache / Wayback   — 缓存快照
    └── L10: Playwright + Clash代理  — 终极反封锁 🏆
```

**层级越高，成功率越高，但时间成本也越高。**

### 智能策略路由

| 策略 | 链路 | 适用场景 |
|------|------|---------|
| `auto` | L1→L3→L4→...→L10 | 未知站点，自动试探 |
| `stealth` | 跳过L1-L4，L5起手 | reuters/bloomberg/zoominfo 等已知反爬 |
| `dynamic` | L7起手 | facebook/amazon 等 JS 动态站点 |
| `nuclear` | L1→L2→L3→...→L10 | 必须搞到，不计成本 |

### 策略选择（内置自动规则）

```
reuters.com       → stealth  (反爬已知)
bloomberg.com     → stealth  (反爬已知)
linkedin.com      → stealth  (反爬已知)
facebook.com      → dynamic  (JS渲染)
amazon.com        → dynamic  (JS渲染)
example.com       → auto     (未知,逐步降级)
```

### 调用方式

```python
from skills.taiyi_search.taiyi_anysearch import (
    search, extract_url, scrapling_fetch,
    extract_elements, adaptive_extract, batch_fetch
)

# === 提取URL ===

# 自动路由（推荐日常用）
r = extract_url("https://reuters.com/technology")
# → 检测到 reuters.com → 自动走 stealth 链路

# 显式指定策略
r = extract_url("https://some-unknown-site.com", strategy="nuclear")
# → 10层全部试一遍，不死不休

# === 直接 Scrapling 调用 ===

# 自动
r = scrapling_fetch("https://bloomberg.com/markets")

# 反爬强制
r = scrapling_fetch("https://crunchbase.com", strategy="stealth")

# 核弹模式
r = scrapling_fetch("https://gov-site-that-hates-bots.gov", strategy="nuclear")

# === 元素提取 ===
r = extract_elements(html_text, css_selector="article h2")
r = adaptive_extract(html, target_text="价格")

# === 批量抓取 ===
results = batch_fetch(["url1", "url2", "url3"])
```

### 返回值格式

```python
{
    "content": "...",          # 页面内容
    "fetcher": "scrapling_stealth",  # 成功的那一层
    "chain_attempts": 3,       # 总共尝试了多少层
    "time_ms": 2250,           # 耗时
    "strategy": "auto|stealth|dynamic|nuclear",
    "debug": ["basic→try", "stealth→try", "✅stealth_success:2250ms"]
}
```

## 后端

- 搜索：AnySearch API（匿名访问，无限额）
- 抓取：10层链路（requests→scrapling→cloudscraper→playwright→cache→proxy）
- 代理：Clash (127.0.0.1:7890)
- 缓存：1小时自动缓存

## 安装 / 更新

```bash
pip install -U scrapling cloudscraper playwright
playwright install chromium
```

## 直接调用

```python
from skills.taiyi_search.taiyi_anysearch import search, extract_url

# 搜索
r = search("AI Agent 2026", max_results=10)

# 10层提取
r = extract_url("https://reuters.com/technology", strategy="nuclear")
print(r.get("content", "")[:1000])
print(f"成功链路: {r.get('fetcher')}, 尝试: {r.get('chain_attempts')}层")
```
