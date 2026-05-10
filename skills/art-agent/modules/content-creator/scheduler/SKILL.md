---
name: content-scheduler
version: 1.0.0
description: 内容排期引擎 - 日历规划/轮转策略/草稿管道
category: content
tags: ['calendar', 'schedule', 'rotation', 'content', '排期，日历，轮转']
author: 太一 AGI
created: 2026-04-07
status: active
---

# Content Scheduler - 内容排期模块

> **版本**: 1.0.0 | **整合自**: content-scheduler + social-media-scheduler
> **负责 Bot**: 山木 | **状态**: ✅ 已激活

---

## 📋 功能概述

内容排期与规划引擎，整合了两个核心技能：
- ✅ **content-scheduler**: 内容轮转、草稿管道、发布追踪
- ✅ **social-media-scheduler**: 社媒日历、平台优化、内容支柱

**核心能力**:
- 内容日历规划（周/月度）
- 智能轮转策略（避免格式疲劳）
- 草稿状态管道（idea→draft→ready→published）
- 多平台排期优化
- 发布频率控制

---

## 🏗️ 架构设计

```
scheduler/
├── SKILL.md (本文件)
├── content_calendar.py (内容日历)
├── rotation.py (轮转策略)
├── social_scheduler.py (社媒排期)
└── draft_pipeline.py (草稿管道)
```

---

## 🎯 核心功能

### 1. 内容轮转引擎

**轮转规则**: 永不连续发布相同格式的内容

| 类型 | 用途 | 示例 |
|------|------|------|
| **Hot Take** | 吸引注意 + 引发讨论 | "Prompt engineering isn't a skill." |
| **Thread** | 展示专业度，建立信任 | 3 部分拆解为什么 X 失败 |
| **Question** | 驱动回复，了解受众 | "A or B? 选一个。" |
| **Visual** | 停止滑动，获得收藏 | 引用卡片、数据可视化 |
| **Story/BIP** | 建立连接 | "第 5 天：$0 收入。我学到了..." |

**追踪器 JSON**:
```json
{
  "types": ["hot-take", "thread", "question", "visual", "story"],
  "nextType": "question",
  "todayCount": 1,
  "maxPerDay": 4,
  "history": [
    {
      "date": "2026-04-07",
      "type": "hot-take",
      "title": "Stop asking ChatGPT nicely",
      "status": "published",
      "notes": "2 小时内 87 次展示"
    }
  ]
}
```

### 2. 草稿管道

| 状态 | 规则 |
|------|------|
| `idea` | 可无限期存放 |
| `draft` | **7 天限制** - 编辑或删除 |
| `ready` | 48 小时内发布，否则过期 |
| `published` | 添加表现备注 |

### 3. 发布频率指南

| 情况 | 频率 | 原因 |
|------|------|------|
| 0 粉丝 | 2-4 次/天 | 没人知道你存在时需要量 |
| <1K 粉丝 | 1-2 次/天 | 一致性 > 量 |
| 1K+ 粉丝 | 4-7 次/周 | 质量 > 频率 |
|  Newsletter | 1-2 次/周 | 尊重收件箱 |

### 4. 社媒平台优化

| 平台 | 风格 | 最佳实践 |
|------|------|---------|
| **Twitter/X** | 简洁有力，<280 字符 | 钩子优先，线程友好 |
| **LinkedIn** | 专业，故事性 | 段落分隔，1300 字符最佳 |
| **Instagram** | 视觉优先 | 换行，20-30 标签放评论 |
| **小红书** | 治愈系，emoji | 分段清晰，标签前置 |
| **微信公众号** | 深度长文 | 标题加粗，列表圆点 |

---

## 🚀 使用方式

### Python API

```python
from skills.content_creator.scheduler import ContentScheduler

# 初始化
scheduler = ContentScheduler()

# 添加内容任务
scheduler.add_task(
    platform='xiaohongshu',
    content_type='note',
    scheduled_time='2026-04-07 21:00',
    topic='AI 工具推荐',
    content_type_rotation='visual'
)

# 获取下周排期
calendar = scheduler.plan_week(
    week_start='2026-04-07',
    platforms=['wechat', 'xiaohongshu'],
    posts_per_day=2
)

# 检查轮转状态
next_type = scheduler.get_next_rotation_type()
print(f"下次应该发布：{next_type}")

# 草稿管道管理
scheduler.draft_pipeline.move('draft-123', 'draft', 'ready')
```

### CLI 命令

```bash
# 查看本周日历
content-creator scheduler calendar --week 2026-04-07

# 获取下次轮转类型
content-creator scheduler rotation --next

# 查看草稿状态
content-creator scheduler drafts --status draft

# 生成周报
content-creator scheduler report --weekly
```

---

## 📊 互动模式洞察

基于真实数据的发现：

1. **"A or B?" > "What do you think?"** - 选项式问题获得 3 倍回复
2. **前 10 个字决定一切** - 不要浪费在"这是一个关于...的线程"
3. **链接损害触达** - 每个平台都降权外部链接，最多 1/4 帖子带链接
4. **格式疲劳真实存在** - 连续 3 天单推文格式，互动下降 40%
5. **早晨=展示，晚间=互动** - 热帖 AM，问题 PM
6. **3 帖规则**: 连续 3 帖失败，改变一个变量

---

## ⚠️ 安全限制

- ✅ 设置 `maxPerDay` 并在发布前检查
- ✅ 扫描草稿中的隐私信息
- ✅ 归档而非删除 - 将无效草稿移到 `archived` 状态
- ✅ 微信公众号：每天最多 1 次群发
- ✅ 小红书：每小时最多 1 条笔记

---

## 📈 效果追踪

### 核心指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **发布频率** | 每日/周/月发布数量 | 一致性 |
| **互动率** | 点赞/评论/分享 | >5% |
| **增长率** | 粉丝增长 | 周增长>3% |
| **轮转合规** | 格式轮转执行率 | 100% |

---

## 📋 变更日志

### v1.0.0 (2026-04-07)
- ✅ 整合 content-scheduler 和 social-media-scheduler
- ✅ 统一轮转策略和草稿管道
- ✅ 添加多平台排期优化

---

*维护：山木 AGI | Content Creator v1.0*
