---
name: browser-harness
description: 浏览器搜索引擎 — 基于 OpenClaw Browser 的 JS 渲染搜索，处理 API 搜不到的动态内容
version: 1.0.0
author: 太一 AGI
created: 2026-05-11
status: active
category: search
tags: ['browser', 'search', 'chrome', 'headless', 'js-rendering']
---

# 🌐 浏览器搜索引擎 (Browser Harness)

> 当 `web_search` / `web_fetch` / 穿透搜索都搜不到时 → 开浏览器真实渲染

---

## 📐 架构

```
Agent 调用
    │
    ▼
┌──────────────────────────────────────────┐
│  browser_search.py (浏览器搜索引擎)       │
│                                          │
│  策略:                                    │
│  ┌──────────┐  ┌─────────────┐          │
│  │ 轻量搜索  │  │ 深度搜索     │          │
│  │ (snapshot)│  │ (navigate+   │          │
│  │          │  │  scroll+act) │          │
│  └──────────┘  └─────────────┘          │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  OpenClaw Browser Plugin (CDP/Playwright) │
│  Chrome for Testing 131                  │
│  headless → snapshot → click/type        │
└──────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────┐
│  shared-search-agent 缓存 + 统一返回      │
└──────────────────────────────────────────┘
```

---

## 🚀 能力

| 模式 | 速度 | 反爬 | 适用场景 |
|:----|:----|:----|:--------|
| **轻量** | ~3s | 🌟🌟 | 搜 Google/Bing/DuckDuckGo，取链接 |
| **深度** | ~8s | 🌟🌟🌟🌟 | 搜 LinkedIn/JS 挑战/SPA 站 |
| **抓取** | ~5s | 🌟🌟🌟 | 渲染 JS 页面后提取内容 |
| **登录态** | ~15s | 🌟🌟🌟🌟🌟 | 需登录的搜索（Twitter/Crunchbase） |

## 🧩 使用的 OpenClaw 内置工具

```python
# OpenClaw browser tool (CDP/Playwright)
browser(tool="snapshot")      # 获取页面 AI 快照 + ref
browser(tool="navigate")       # 导航到 URL
browser(tool="act", kind="click", ref="12")  # 点击元素
browser(tool="act", kind="type", ref="23", value="query")  # 输入
browser(tool="screenshot")     # 截屏（调试用）
```

---

## 🔗 集成共享搜索

在 `shared-search-agent` 中以回退模式注入：

```python
# 当非浏览器搜索失败时，自动升级到浏览器搜索
result = browser_harness.search(query="xxx", engine="google")
```

---

## 📂 文件结构

```
browser-harness/
├── SKILL.md                    # 本文件
└── browser_search.py          # 浏览器搜索引擎实现
```
