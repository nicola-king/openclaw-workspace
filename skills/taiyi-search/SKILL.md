---
name: taiyi-search
description: 太一统一搜索引擎（唯一搜索入口）— 蒸馏合并自 AnySearch + shared-search + search-agent
version: 2.0.0
author: 太一 AGI
tags: [search, web, intelligence, anysearch, vertical-search, penetrating-search]
trigger: 当 Agent 需要搜索信息、查证事实、提取网页内容时，默认且唯一的搜索工具
---

# 🔍 太一统一搜索引擎

蒸馏合并自：`anysearch-skill`（统一搜索API）+ `shared-search-agent`（缓存路由）+ `search-agent`（穿透方法论）

## 一键使用

```
帮我搜 "xxx"
查一下 xxx 的最新消息
提取这个链接的内容 xxx
搜一下 xxx 领域的最新动态
```

## 能力矩阵

| 能力 | 命令 | 说明 |
|------|------|------|
| **通用搜索** | `search(query, max, freshness)` | 任意关键词，支持时效筛选 |
| **批量穿透** | `deep_search([q1,q2...])` | 多角度聚合搜索 |
| **URL提取** | `extract_url(url)` | 获取完整页面内容 |
| **垂直搜索** | `search(query, domain, sub_domain)` | 23个垂直领域 |
| **国家解析** | `resolve_country("沙特")` | 国家名称→代码 |
| **搜索链接** | `gen_search_links("battery","australia")` | 多平台搜索URL |
| **搜索统计** | `stats.summary()` | 近7天搜索量 |

## 垂直领域

tech finance academic legal business ip security education health religion geo environment energy ugc code fashion travel home ecommerce gaming film music

## 后端

- 默认：AnySearch API（匿名访问，无限额）
- 缓存：1小时自动缓存
- 零外部依赖，零配置

## 直接调用

```python
from skills.taiyi_search.taiyi_anysearch import search, deep_search, extract_url, resolve_country
r = search("AI Agent 2026", max_results=10)
for item in r["results"]:
    print(item["title"], "→", item["url"])
```
