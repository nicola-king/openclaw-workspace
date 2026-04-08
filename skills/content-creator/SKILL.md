---
name: content-creator
version: 1.0.0
description: 内容创作引擎 - 排期/优化/发布/生成一体化
category: content
tags: ['content', 'social-media', 'scheduler', 'publisher', 'seo', '内容创作，自媒体，排期，发布']
author: 太一 AGI
created: 2026-04-07
status: active
priority: P0
---


# Content Creator v1.0 - 统一内容创作引擎

> **版本**: 1.0.0 (整合版) | **创建**: 2026-04-07 | **更新**: 2026-04-07 08:30
> **负责 Bot**: 山木 | **状态**: ✅ 已激活

---

## 📋 功能概述

统一内容创作技能，整合 5 个相关技能为一体化引擎。

**整合内容**:
- ✅ content-scheduler → scheduler/ (内容排期)
- ✅ social-media-scheduler → scheduler/ (社媒排期)
- ✅ social-publisher → publisher/ (多平台发布)
- ✅ hot-topic-generator → generator/ (热点生成)
- ✅ geo-seo-optimizer → optimizer/ (GEO 优化)

**备份位置**: `skills/.backup/` 目录下保留原始技能副本

---

## 🏗️ 架构设计

```
content-creator/
├── SKILL.md (主入口)
├── scheduler/ (排期模块)
│   ├── content_calendar.py (内容日历)
│   ├── rotation.py (轮转策略)
│   └── social_scheduler.py (社媒排期)
├── optimizer/ (优化模块)
│   ├── geo_seo.py (GEO 优化)
│   └── viral_title.py (爆款标题)
├── publisher/ (发布模块)
│   ├── wechat.py (微信公众号)
│   ├── xiaohongshu.py (小红书)
│   └── twitter.py (Twitter)
└── generator/ (生成模块)
    ├── hot_topic.py (热点生成)
    └── article.py (文章生成)
```

---

## 🚀 使用方式

### Python API

```python
from skills.content_creator import ContentCreator

# 初始化
cc = ContentCreator()

# 内容排期
cc.scheduler.add_task(
    platform='xiaohongshu',
    content_type='note',
    scheduled_time='2026-04-07 21:00',
    topic='AI 工具推荐'
)

# 爆款标题生成
titles = cc.optimizer.generate_viral_titles(
    topic='太一 AGI 使用指南',
    platform='xiaohongshu',
    count=5
)

# 发布内容
result = cc.publisher.publish(
    platform='wechat',
    title='太一 v5.0 发布',
    content='<h1>...</h1>',
    images=['img1.png', 'img2.png']
)

# 热点追踪
trending = cc.generator.get_hot_topics(
    category='tech',
    limit=10
)
```

---

## 📊 模块说明

### 1. Scheduler Module - 排期

| 功能 | 说明 |
|------|------|
| **内容日历** | 规划月度/周度内容计划 |
| **轮转策略** | 避免连续发布相同格式 |
| **社媒排期** | 多平台定时发布 |
| **草稿管道** | idea→draft→ready→published |

### 2. Optimizer Module - 优化

| 功能 | 说明 |
|------|------|
| **GEO 优化** | 针对 AI 搜索引擎优化 (Perplexity/ChatGPT) |
| **爆款标题** | 生成高点击率标题 |
| **关键词优化** | SEO/GEO 关键词布局 |

### 3. Publisher Module - 发布

| 平台 | 功能 |
|------|------|
| **微信公众号** | 图文发布/草稿管理 |
| **小红书** | 笔记发布/话题标签 |
| **Twitter** | 推文发布/线程 |

### 4. Generator Module - 生成

| 功能 | 说明 |
|------|------|
| **热点生成** | 追踪全网热点话题 |
| **文章生成** | 基于大纲自动生成文章 |
| **文案创作** | 营销文案/产品描述 |

---

## 🎯 使用场景

### 场景 1: 内容排期

```python
# 规划本周内容
cc.scheduler.plan_week(
    week_start='2026-04-07',
    platforms=['wechat', 'xiaohongshu'],
    posts_per_day=2
)
```

### 场景 2: 爆款标题

```python
# 生成小红书爆款标题
titles = cc.optimizer.generate_viral_titles(
    topic='AI 工具推荐',
    platform='xiaohongshu',
    count=10
)
# 返回：['这 5 个 AI 工具让我效率翻倍！', '打工人必备！AI 神器合集', ...]
```

### 场景 3: GEO 优化

```python
# 优化文章用于 AI 搜索
optimized = cc.optimizer.geo_optimize(
    content='原始文章内容...',
    target_ai=['perplexity', 'chatgpt'],
    keywords=['太一 AGI', 'OpenClaw', '自动化']
)
```

### 场景 4: 多平台发布

```python
# 一键发布多平台
cc.publisher.publish_multi(
    content={
        'title': '太一 v5.0 发布',
        'body': '今天发布了...',
        'images': ['screenshot.png']
    },
    platforms=['wechat', 'xiaohongshu', 'twitter']
)
```

### 场景 5: 热点追踪

```python
# 获取今日热点
trending = cc.generator.get_hot_topics(
    category='tech',
    time_range='24h'
)
```

---

## 📈 内容策略

### 轮转规则

```yaml
rotation_rules:
  # 不连续发布相同格式
  no_repeat_format: true
  
  # 平台间隔
  platform_interval:
    wechat: 24h  # 公众号每天最多 1 篇
    xiaohongshu: 4h  # 小红书间隔 4 小时
    twitter: 1h  # Twitter 间隔 1 小时
  
  # 内容类型分布
  content_mix:
    educational: 40%
    promotional: 20%
    engaging: 30%
    trending: 10%
```

### 最佳发布时间

| 平台 | 时段 | 说明 |
|------|------|------|
| **微信公众号** | 20:00-22:00 | 晚间阅读高峰 |
| **小红书** | 12:00-14:00, 20:00-22:00 | 午休/晚间 |
| **Twitter** | 09:00-11:00, 21:00-23:00 | 早晚高峰 |

---

## 🔌 与共享层集成

```python
from skills.shared import SharedDatabase, EventBus, Events

# 记录发布
db = SharedDatabase.get_instance()
db.record_content_publish(
    platform='xiaohongshu',
    content_type='note',
    title='标题',
    scheduled_time='2026-04-07 21:00',
    actual_time='2026-04-07 21:00'
)

# 发布事件
event_bus = EventBus.get_instance()
event_bus.publish(Events.CONTENT_PUBLISHED, {
    'platform': 'xiaohongshu',
    'title': '标题'
})
```

---

## 📊 效果追踪

### 核心指标

| 指标 | 说明 |
|------|------|
| **发布频率** | 每日/周/月发布数量 |
| **互动率** | 点赞/评论/分享 |
| **增长率** | 粉丝增长 |
| **转化率** | 点击/关注转化 |

### 报表生成

```python
# 生成周报
report = cc.scheduler.generate_weekly_report(
    week_start='2026-04-01',
    platforms=['wechat', 'xiaohongshu']
)
```

---

## ⚠️ 注意事项

### 发布限制

- ✅ 微信公众号：每天最多 1 次群发
- ✅ 小红书：每小时最多 1 条笔记
- ✅ Twitter: API 速率限制

### 内容审核

- ✅ 发布前自动检查敏感词
- ✅ 图片版权检查
- ✅ 链接安全性检查

---

## 📋 变更日志

### v1.0.0 (2026-04-07)
- ✅ 整合 5 个内容相关技能
- ✅ 创建统一架构 scheduler/optimizer/publisher/generator
- ✅ 移除冗余技能目录

---

## 📚 相关文档

- [内容排期协议](../../constitution/content/SCHEDULING.md)
- [GEO 优化指南](../../docs/GEO-SEO.md)
- [多平台发布最佳实践](../../docs/MULTI-PLATFORM-PUBLISHING.md)

---

*维护：山木 AGI | Content Creator v1.0*
