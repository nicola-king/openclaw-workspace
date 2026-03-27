# 知几-E 免费自动化发布方案

> 免费开源优先，自动化优先

---

## 核心原则

1. **免费优先** - 不用付费 API
2. **开源优先** - 用开源工具
3. **自动化优先** - 减少人工操作

---

## 方案对比

| 方案 | 成本 | 自动化 | 推荐度 |
|------|------|--------|--------|
| **X API v2** | $100/月 | ✅ 完全自动 | ❌ 不推荐 |
| **IFTTT/Zapier** | 免费/月 | 🟡 半自动 | 🟡 备选 |
| **GitHub Actions** | 免费 | ✅ 自动 | ✅ 推荐 |
| **Telegram 推送** | 免费 | ✅ 自动 | ✅ 推荐 |
| **手动发布** | 免费 | ❌ 手动 | 🟡 过渡 |

---

## 推荐方案：GitHub Actions + Telegram

### 架构

```
知几-E 生成内容
    ↓
保存到 x-posts/
    ↓
GitHub Actions 检测
    ↓
浏览器自动化发布
    ↓
Telegram 通知
```

### 优势

- ✅ 完全免费
- ✅ 完全自动化
- ✅ 开源可审计
- ✅ 无需 X API

### 实现

**1. GitHub Action 配置**

```yaml
name: Auto Post to X

on:
  push:
    paths:
      - 'x-posts/**'

jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Post to X
        run: |
          # 使用浏览器自动化发布
          python3 scripts/post-to-x.py
```

**2. 浏览器自动化**

使用 Playwright 或 Selenium:
```python
from playwright.sync_api import sync_playwright

def post_to_x(content):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://twitter.com/home")
        # 登录 + 发布逻辑
        browser.close()
```

---

## 当前方案（过渡期）

### 自动保存 + Telegram 推送

**流程：**
1. 知几-E 生成内容
2. 保存到 `~/.taiyi/zhiji/x-posts/`
3. 同时推送到 Telegram 频道
4. 你从 Telegram 复制发布

**优势：**
- ✅ 免费
- ✅ 半自动
- ✅ 即时通知

**待优化：**
- 🟡 需手动复制
- 🟡 需手动发布

---

## 下一步

### 阶段 1：Telegram 推送（今日完成）
- ✅ 自动保存到 x-posts/
- ✅ 推送到 Telegram 频道
- 🟡 你复制发布

### 阶段 2：GitHub Actions（本周完成）
- 🟡 配置 GitHub Action
- 🟡 浏览器自动化发布
- ✅ 完全自动

### 阶段 3：多平台分发（下周完成）
- 🟡 X 平台
- 🟡 Mastodon
- 🟡 Bluesky
- 🟡 微博

---

## 发布内容模板

### 08:00 早报
```
【加密早报 · 03/24】

隔夜热点：
• BTC $70,500 (+2.3%)
• ETH $2,155 (+1.8%)
• Polymarket 24h 交易量 $50M

今日关注：
• 美联储讲话 (20:00)
• 美国 GDP 数据 (21:30)

知几-E 策略运行中

#Polymarket #量化交易 #BTC
```

### 10:00 信号
```
🟢【交易信号 · 10:00】

市场：BTC 涨跌
方向：多
置信度：96%
优势：4.5%

#Polymarket #交易信号
```

### 18:00 日报
```
✅【交易日报 · 03/24】

今日交易：5 笔
总盈亏：+$25.50 (+2.5%)
胜率：80%

知几-E 自动执行中

#量化交易 #收益报告
```

---

*太一 · 2026 年 3 月 24 日*

*「免费开源优先，自动化优先」*
