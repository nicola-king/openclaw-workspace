---
name: browser-automation
version: 2.0.0
description: 智能浏览器自动化 - Playwright 网页导航/交互/截图/数据采集/平台适配器
category: browser
tags: ['playwright', 'browser', 'automation', 'screenshot', 'crawl', 'adapter', '网页，浏览器，截图，爬虫，适配器']
author: 太一 AGI
created: 2026-04-03
updated: 2026-04-07
status: active
priority: P0
---


# Browser Automation Skill v2.0

> **版本**: 2.0.0 (整合版) | **创建时间**: 2026-04-03 | **整合时间**: 2026-04-07
> **负责 Bot**: 素问 | **状态**: ✅ 已激活 | **优先级**: P0

---

## 📋 功能概述

提供智能浏览器自动化能力，基于 Playwright 实现网页导航、交互、截图、数据采集等功能。

**v2.0 整合内容**:
- ✅ 合并 `browser-adapter` 为子模块 `adapters/`
- ✅ 统一核心引擎 `core/`
- ✅ 工具函数 `utils/`
- ✅ 支持平台适配器模式（Polymarket/微信/小红书等）

---

## 🏗️ 架构设计

```
browser-automation/
├── SKILL.md (主入口)
├── core/ (核心引擎)
│   ├── browser_automation.py (Playwright 封装)
│   └── browser-cli.sh (CLI 工具)
├── adapters/ (平台适配器)
│   ├── polymarket_adapter.py (Polymarket 交易)
│   ├── wechat_adapter.py (微信公众号)
│   └── xiaohongshu_adapter.py (小红书)
└── utils/ (工具函数)
    └── test_adapters.py (测试工具)
```

---

## 🛠️ 可用命令

### 基础导航

| 命令 | 功能 | 示例 |
|------|------|------|
| `browser open` | 打开网页 | `browser open https://example.com` |
| `browser close` | 关闭浏览器 | `browser close` |
| `browser navigate` | 导航到新页面 | `browser navigate https://google.com` |
| `browser back` | 后退 | `browser back` |
| `browser forward` | 前进 | `browser forward` |
| `browser refresh` | 刷新页面 | `browser refresh` |

### 页面交互

| 命令 | 功能 | 示例 |
|------|------|------|
| `browser click` | 点击元素 | `browser click "#login-btn"` |
| `browser fill` | 填写表单 | `browser fill "#username" "admin"` |
| `browser select` | 选择下拉 | `browser select "#country" "CN"` |
| `browser check` | 勾选复选框 | `browser check "#agree"` |
| `browser hover` | 悬停元素 | `browser hover ".menu"` |
| `browser scroll` | 滚动页面 | `browser scroll --down 500` |

### 截图与媒体

| 命令 | 功能 | 示例 |
|------|------|------|
| `browser screenshot` | 页面截图 | `browser screenshot --full-page` |
| `browser element-shot` | 元素截图 | `browser element-shot ".hero"` |
| `browser pdf` | 保存 PDF | `browser pdf --output page.pdf` |
| `browser video` | 录制视频 | `browser video --start/--stop` |

### 数据采集

| 命令 | 功能 | 示例 |
|------|------|------|
| `browser text` | 提取文本 | `browser text ".article-content"` |
| `browser html` | 获取 HTML | `browser html --selector "#main"` |
| `browser attribute` | 获取属性 | `browser attribute "img" "src"` |
| `browser links` | 提取链接 | `browser links --domain example.com` |
| `browser images` | 提取图片 | `browser images --download` |
| `browser table` | 提取表格 | `browser table "#data-table"` |

### 高级功能

| 命令 | 功能 | 示例 |
|------|------|------|
| `browser wait` | 等待元素 | `browser wait --selector ".loaded"` |
| `browser eval` | 执行 JS | `browser eval "document.title"` |
| `browser inject` | 注入脚本 | `browser inject script.js` |
| `browser cookie` | 管理 Cookie | `browser cookie --get/--set` |
| `browser storage` | 本地存储 | `browser storage --get key` |
| `browser network` | 网络监控 | `browser network --log` |

### 平台适配器

| 命令 | 功能 | 示例 |
|------|------|------|
| `browser adapter polymarket` | Polymarket 交易 | `browser adapter polymarket bet --market NYC-TEMP --outcome YES --amount 5` |
| `browser adapter wechat` | 公众号发布 | `browser adapter wechat publish --title "标题" --content "内容"` |
| `browser adapter xiaohongshu` | 小红书发布 | `browser adapter xiaohongshu note --title "标题" --images img1.png,img2.png` |

---

## 🚀 使用示例

### 示例 1: 打开网页并截图

```bash
# 太一，打开 GitHub 并截图
browser open https://github.com
browser screenshot --full-page --output github.png
```

### 示例 2: 登录操作

```bash
# 太一，登录 Twitter
browser open https://twitter.com/login
browser fill "#username" "myuser"
browser fill "#password" "mypass"
browser click "#login-btn"
browser wait --selector ".timeline"
browser screenshot --output logged-in.png
```

### 示例 3: 数据采集

```bash
# 太一，抓取 Hacker News 标题
browser open https://news.ycombinator.com
browser text ".titleline > a" --all
browser links ".titleline > a" --output links.json
```

### 示例 4: Polymarket 下注（适配器）

```bash
# 太一，在 Polymarket 下注
browser adapter polymarket bet --market "NYC-TEMP-2026" --outcome "YES" --amount 5
```

### 示例 5: 公众号发布（适配器）

```bash
# 太一，发布公众号文章
browser adapter wechat publish --title "太一 AGI v4.0" --content "<h1>内容...</h1>"
```

### 示例 6: 小红书发布（适配器）

```bash
# 太一，发布小红书笔记
browser adapter xiaohongshu note --title "太一使用指南" --content "今天发现了..." --images image1.png,image2.png
```

---

## 🔧 核心 API

### Playwright 封装

```python
from skills.browser_automation.core.browser_automation import BrowserAutomation

# 初始化
ba = BrowserAutomation(headless=False)
ba.start()

# 导航
ba.open('https://example.com')

# 交互
ba.click('#button')
ba.fill('#input', 'value')

# 截图
ba.screenshot('output.png', full_page=True)

# 提取数据
text = ba.text('.content')
html = ba.html('#main')

# 执行 JS
result = ba.eval('document.title')

# 关闭
ba.close()
```

### 平台适配器

```python
from skills.browser_automation.adapters.polymarket_adapter import PolymarketAdapter
from skills.browser_automation.core.browser_automation import BrowserAutomation

# 初始化浏览器
ba = BrowserAutomation()
ba.start()

# 初始化适配器
adapter = PolymarketAdapter(ba)

# 下注
result = await adapter.place_bet(
    market='NYC-TEMP-2026',
    outcome='YES',
    amount=5
)

# 查询余额
balance = await adapter.get_balance()
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] 打开公开网页
- [x] 截图/提取文本
- [x] 执行只读 JS
- [x] 导航/刷新

### 需要确认的操作
- [ ] 填写密码/敏感信息
- [ ] 点击支付/购买按钮
- [ ] 下载文件
- [ ] 执行写操作 JS
- [ ] 修改 Cookie/Storage
- [ ] 平台交易操作（Polymarket 下注等）

---

## 🎯 触发词

| 触发词 | 优先级 |
|--------|--------|
| 打开浏览器 | P0 |
| 截图网页 | P0 |
| 抓取数据 | P1 |
| 自动登录 | P1 |
| 测试网页 | P2 |
| 监控页面 | P2 |
| Polymarket 下注 | P1 |
| 发布公众号 | P1 |
| 发布小红书 | P1 |

---

## 📊 性能优化

### 无头模式
```bash
# 生产环境使用无头模式
browser open https://example.com --headless
```

### 缓存策略
```bash
# 启用缓存加速
browser open https://example.com --cache
```

### 会话复用
```bash
# 复用本地浏览器会话（绕过登录）
browser open https://example.com --user-data-dir=/home/nicola/.config/google-chrome
```

---

## 🧪 测试用例

```bash
# 测试 1: 打开网页
browser open https://example.com

# 测试 2: 截图
browser screenshot --output /tmp/test.png

# 测试 3: 提取标题
browser eval "document.title"

# 测试 4: 点击交互
browser click "#click-me"

# 测试 5: 等待元素
browser wait --selector ".loaded"

# 测试 6: 适配器测试
python3 skills/browser-automation/utils/test_adapters.py

# 清理
browser close
```

---

## 📚 相关文档

- [Playwright 官方文档](https://playwright.dev)
- [浏览器自动化最佳实践](../../docs/BROWSER-AUTOMATION.md)
- [网页爬虫指南](../../docs/WEB-SCRAPING.md)
- [平台适配器开发指南](../../docs/ADAPTER-DEVELOPMENT.md)

---

## 🔄 变更日志

### v2.0.0 (2026-04-07)
- ✅ 合并 `browser-adapter` 为子模块
- ✅ 创建统一架构 `core/` + `adapters/` + `utils/`
- ✅ 新增平台适配器支持

### v1.0.0 (2026-04-03)
- ✅ 初始版本：Playwright 封装

---

*创建时间：2026-04-03 | 整合时间：2026-04-07 | 素问 | 太一 AGI v5.0*
