---
name: social-publisher
version: 1.0.0
description: 多平台发布引擎 - 微信公众号/小红书/知乎/抖音一键发布
category: content
tags: ['publisher', 'social-media', 'wechat', 'xiaohongshu', 'zhihu', 'douyin', '发布，多平台']
author: 太一 AGI
created: 2026-04-07
status: active
---

# Social Publisher - 多平台发布模块

> **版本**: 1.0.0 | **整合自**: social-publisher
> **负责 Bot**: 山木 | **状态**: ✅ 已激活

---

## 📋 功能概述

多平台内容发布引擎，一键将 Markdown 内容转换为各平台原生格式并发布。

**核心能力**:
- 内容格式转换（Markdown → 各平台格式）
- 多平台发布（微信/小红书/知乎/抖音）
- 预览模式（发布前查看效果）
- 安全模拟（默认不真实发布）
- 图片支持（需 API 凭证）

---

## 🏗️ 架构设计

```
publisher/
├── SKILL.md (本文件)
├── social_publisher.py (发布引擎)
├── wechat.py (微信公众号)
├── xiaohongshu.py (小红书)
├── zhihu.py (知乎)
└── douyin.py (抖音)
```

---

## 🎯 核心功能

### 1. 平台格式转换

| 平台 | 转换规则 |
|------|---------|
| **微信公众号** | 标题加下划线，列表转圆点，加粗转【】标记 |
| **小红书** | 分段清晰，标签前置，emoji 优化，移动端阅读友好 |
| **知乎** | 保留 Markdown 语法，支持代码块和表格 |
| **抖音** | 文案简短化，话题标签前置，<100 字 |

### 2. 发布模式

| 模式 | 说明 | 使用场景 |
|------|------|---------|
| **模拟模式** (默认) | 仅展示格式化效果，不发送网络请求 | 测试、预览 |
| **Dry-run** | 检查配置完整性，不发布 | 配置验证 |
| **真实发布** | 调用平台 API 实际发布 | 需完整 API 凭证 |

### 3. 支持平台

| 平台 | 状态 | API 需求 |
|------|------|---------|
| **微信公众号** | ✅ 支持 | AppID + AppSecret |
| **小红书** | ✅ 支持 | AppID + AppSecret + Access Token |
| **知乎** | ✅ 支持 | ClientID + ClientSecret + Access Token |
| **抖音** | ✅ 支持 | AppKey + AppSecret + Access Token |

---

## 🚀 使用方式

### Python API

```python
from skills.content_creator.publisher import SocialPublisher

# 初始化
publisher = SocialPublisher()

# 格式化内容
wechat_content = publisher.format_wechat(
    title='我的标题',
    content='# 正文内容\n- 列表 1\n- 列表 2',
    images=['img1.jpg', 'img2.jpg']
)

# 发布到多平台
result = publisher.publish_multi(
    title='太一 v5.0 发布',
    content='今天发布了...',
    images=['screenshot.png'],
    platforms=['wechat', 'xiaohongshu']
)

# 仅预览格式化效果
preview = publisher.preview(
    title='标题',
    content='正文',
    platforms=['wechat', 'xiaohongshu', 'zhihu', 'douyin']
)
```

### CLI 命令

```bash
# 预览各平台格式化效果
content-creator publisher format \
  --title "我的标题" \
  --content "正文内容" \
  --platforms wechat,xiaohongshu,zhihu,douyin

# 模拟发布
content-creator publisher publish \
  --title "标题" \
  --content "正文" \
  --images "img1.jpg,img2.jpg" \
  --platforms wechat,xiaohongshu \
  --dry-run

# 真实发布（需配置 API）
content-creator publisher publish \
  --title "标题" \
  --content "正文" \
  --images "img1.jpg" \
  --platforms wechat,zhihu
```

---

## 📊 格式转换示例

### 输入 Markdown
```markdown
# 一级标题
## 二级标题
- 列表项 1
- 列表项 2
**加粗文本**
```

### 微信公众号输出
```
【标题】
一级标题

【正文】
一级标题
====================

• 列表项 1
• 列表项 2
【加粗文本】
```

### 小红书输出
```
【标题】
✨ 一级标题 ✨

【正文】
1. 列表项 1

2. 列表项 2

【话题】
#生活记录 #分享 #好物推荐
```

### 知乎输出
```markdown
# 一级标题

## 二级标题

- 列表项 1
- 列表项 2
**加粗文本**
```

### 抖音输出
```
【文案】
列表项 1 列表项 2 加粗文本

【标题】
一级标题

【话题】
#短视频 #推荐 #热门
```

---

## 🔐 配置方式

### 环境变量（推荐）

```bash
# 微信公众号
export WECHAT_APPID="your_appid"
export WECHAT_APPSECRET="your_appsecret"

# 小红书
export XIAOHONGSHU_APP_ID="your_app_id"
export XIAOHONGSHU_APP_SECRET="your_app_secret"
export XIAOHONGSHU_ACCESS_TOKEN="your_access_token"

# 知乎
export ZHIHU_CLIENT_ID="your_client_id"
export ZHIHU_CLIENT_SECRET="your_client_secret"
export ZHIHU_ACCESS_TOKEN="your_access_token"

# 抖音
export DOUYIN_APP_KEY="your_app_key"
export DOUYIN_APP_SECRET="your_app_secret"
export DOUYIN_ACCESS_TOKEN="your_access_token"
```

### 配置文件

`~/.openclaw/secrets/social-publisher.json`:
```json
{
  "wechat": {"appid": "...", "appsecret": "..."},
  "xiaohongshu": {"app_id": "...", "app_secret": "...", "access_token": "..."},
  "zhihu": {"client_id": "...", "client_secret": "...", "access_token": "..."},
  "douyin": {"app_key": "...", "app_secret": "...", "access_token": "..."}
}
```

---

## ⚠️ 安全限制

- ✅ 模拟模式下不发送任何网络请求
- ✅ 凭证从环境变量读取，不记录到日志
- ✅ 真实 API 调用时使用 HTTPS
- ✅ 支持 dry-run 模式用于安全测试
- ✅ 微信公众号：每天最多 1 次群发
- ✅ 小红书：每小时最多 1 条笔记

---

## 📈 效果指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **发布成功率** | 成功发布/总发布 | >99% |
| **格式准确率** | 格式正确/总发布 | 100% |
| **平均发布时间** | 单平台发布耗时 | <5 秒 |
| **多平台同步** | 同时发布平台数 | 2-4 个 |

---

## 📋 变更日志

### v1.0.0 (2026-04-07)
- ✅ 整合 social-publisher
- ✅ 统一多平台格式转换
- ✅ 添加安全模拟模式

---

*维护：山木 AGI | Content Creator v1.0*
