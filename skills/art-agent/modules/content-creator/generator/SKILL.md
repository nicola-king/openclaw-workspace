---
name: hot-topic-generator
version: 1.0.0
description: 热点生成引擎 - 全网热点采集/趋势分析/选题推荐/标题生成
category: content
tags: ['hot-topics', 'trending', 'content-generation', '热点，选题，趋势']
author: 太一 AGI
created: 2026-04-07
status: active
---

# Hot Topic Generator - 热点生成模块

> **版本**: 1.0.0 | **整合自**: hot-topic-generator
> **负责 Bot**: 山木 | **状态**: ✅ 已激活

---

## 📋 功能概述

热点选题生成器，整合全网热点数据，智能推荐内容选题。

**核心能力**:
- 热点数据采集（微博/知乎/小红书）
- 趋势分析（上升速度/讨论热度）
- 选题推荐（匹配度评分）
- 标题生成（AI 优化）
- 热点报告生成

---

## 🏗️ 架构设计

```
generator/
├── SKILL.md (本文件)
├── hot_topic.py (热点生成)
├── article.py (文章生成)
└── topic_db.py (话题数据库)
```

---

## 🎯 核心功能

### 1. 热点数据采集

| 平台 | 数据源 | 更新频率 |
|------|--------|---------|
| **微博** | 微博热搜 API | 每 10 分钟 |
| **知乎** | 知乎热榜 API | 每 30 分钟 |
| **小红书** | 模拟采集（无公开 API） | 每小时 |

**数据结构**:
```python
@dataclass
class HotTopic:
    id: str
    title: str
    platform: str
    heat_score: int
    trend: str  # 'rising', 'stable', 'falling'
    tags: List[str]
    url: str
    created_at: str
```

### 2. 趋势分析

| 趋势 | 说明 | 操作建议 |
|------|------|---------|
| 📈 **rising** | 上升中 | 立即跟进，24 小时内发布 |
| ➡️ **stable** | 稳定 | 选择性跟进，48 小时内 |
| 📉 **falling** | 下降 | 谨慎跟进，需独特角度 |

### 3. 选题推荐算法

**评分公式**:
```
总分 = 热度分 (60%) + 趋势分 (20%) + 匹配分 (20%)

热度分 = heat_score / 10000000 * 60
趋势分 = {'rising': 20, 'stable': 10, 'falling': 0}[trend]
匹配分 = len(话题标签 ∩ 垂直领域标签) / 垂直领域标签数 * 20
```

### 4. 标题生成模板

| 模板 | 示例 |
|------|------|
| 「如何评价 {topic}？」 | 「如何评价 AI 技术突破？」 |
| 「{topic} 全攻略」 | 「AI 技术突破全攻略」 |
| 「普通人如何通过 {topic} 改变命运？」 | 「普通人如何通过 AI 改变命运？」 |
| 「关于 {topic}，90% 的人都不知道的事」 | 「关于 AI，90% 的人都不知道的事」 |
| 「2026 年，{topic} 还值得做吗？」 | 「2026 年，AI 还值得做吗？」 |

---

## 🚀 使用方式

### Python API

```python
from skills.content_creator.generator import HotTopicGenerator

# 初始化
generator = HotTopicGenerator()

# 采集热点
weibo_topics = generator.fetch_weibo_hot()
zhihu_topics = generator.fetch_zhihu_hot()
xhs_topics = generator.fetch_xiaohongshu_hot()

# 保存热点
all_topics = weibo_topics + zhihu_topics + xhs_topics
generator.save_topics(all_topics)

# 获取推荐
recommendations = generator.get_recommendations(
    niche_tags=['AI', '副业', '理财', '工具', '成长'],
    limit=10
)

# 生成标题
for topic in recommendations[:5]:
    titles = generator.generate_titles(topic)
    print(f"话题：{topic.title}")
    print(f"推荐标题：{titles[0]}")
```

### CLI 命令

```bash
# 采集热点
content-creator generator fetch --platforms weibo,zhihu,xhs

# 获取推荐
content-creator generator recommend --tags "AI,副业，理财" --limit 10

# 生成标题
content-creator generator titles --topic "AI 技术突破" --count 10

# 生成热点报告
content-creator generator report --output reports/hot-topics.md
```

---

## 📊 热点报告示例

```markdown
# 热点选题报告

> 生成时间：2026-04-07 21:00
> 垂直领域：AI, 副业，理财，工具，成长

---

## 🔥 Top 10 热点

| 排名 | 平台 | 趋势 | 话题 | 热度 |
|------|------|------|------|------|
| 1 | 微博 | 📈 | AI 技术突破 | 9,500,000 |
| 2 | 小红书 | 📈 | AI 工具推荐 | 9,200,000 |
| 3 | 知乎 | 📈 | 如何评价 TimesFM | 8,900,000 |
| 4 | 微博 | ➡️ | 职场生存指南 | 8,200,000 |
| 5 | 小红书 | 📈 | 副业赚钱 | 8,500,000 |

---

## 💡 选题建议

### 📈 上升趋势话题

- **AI 技术突破**
  推荐标题：「AI 技术突破全攻略，看这一篇就够了」

- **副业赚钱**
  推荐标题：「普通人如何通过副业月入过万？」

---

## 📋 行动清单

1. 选择 2-3 个上升趋势话题
2. 使用推荐标题或 AI 优化
3. 24 小时内发布（热点时效性）
4. 追踪发布后数据（阅读/点赞/收藏）
```

---

## ⚠️ 注意事项

### 热点时效性

- ✅ **rising 趋势**: 24 小时内发布最佳
- ✅ **stable 趋势**: 48 小时内，需独特角度
- ✅ **falling 趋势**: 谨慎跟进，需差异化

### 平台限制

- ✅ 微博热搜：公开 API，需速率限制
- ✅ 知乎热榜：公开 API，有请求限制
- ✅ 小红书：无公开 API，使用模拟数据

### 内容合规

- ✅ 扫描敏感词
- ✅ 检查版权风险
- ✅ 避免争议性话题

---

## 📈 效果指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **热点覆盖率** | 跟进热点占总热点比例 | >30% |
| **时效性** | 热点出现到发布的时间 | <24h |
| **互动率** | 热点内容平均互动率 | >行业平均 50% |
| **爆款率** | 热点内容成为爆款的比例 | >10% |

---

## 📋 变更日志

### v1.0.0 (2026-04-07)
- ✅ 整合 hot-topic-generator
- ✅ 添加文章生成模块
- ✅ 统一热点报告格式

---

*维护：山木 AGI | Content Creator v1.0*
