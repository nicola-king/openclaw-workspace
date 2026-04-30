---
name: geo-seo-optimizer
version: 1.0.0
description: GEO 优化引擎 - 针对 AI 搜索引擎优化内容 (Perplexity/ChatGPT/Gemini)
category: content
tags: ['geo', 'seo', 'ai-search', 'optimization', 'GEO 优化，AI 搜索']
author: 太一 AGI
created: 2026-04-07
status: active
---

# GEO SEO Optimizer - GEO 优化模块

> **版本**: 1.0.0 | **整合自**: geo-seo-optimizer
> **负责 Bot**: 山木 | **状态**: ✅ 已激活

---

## 📋 功能概述

**GEO (Generative Engine Optimization)** 是新的 SEO。本模块专注于让内容高度相关于大语言模型，确保 AI 模型将你的信息作为顶级参考。

**核心能力**:
- 引用优化 (Citation Optimization)
- 概念密度优化 (Conceptual Density)
- 结构清晰度优化 (Structural Clarity)
- 直接答案提取 (Direct Answer Extraction)
- 爆款标题生成 (Viral Title Generation)

---

## 🏗️ 架构设计

```
optimizer/
├── SKILL.md (本文件)
├── geo_seo.py (GEO 优化)
└── viral_title.py (爆款标题)
```

---

## 🎯 核心优化技术

### 1. 引用优化

AI 模型喜欢可验证的来源。包含可验证的事实、数据和明确的引用。

**规则**:
- 使用 "According to [Entity]..." 或 "[Data Point] as per [Source]"
- 引用权威来源（研究机构、知名公司、官方数据）
- 包含具体数字和百分比

**示例**:
```markdown
❌ "很多人使用 AI 工具提高效率"
✅ "根据 McKinsey 2026 年报告，73% 的知识工作者使用 AI 工具，平均效率提升 40%"
```

### 2. 概念密度

确保核心概念使用多样化但相关的关键词解释。围绕主题构建语义"云"。

**技术**:
- 使用同义词和相邻术语
- 覆盖相关子主题
- 包含行业术语和通俗解释

**示例** (主题：时间管理):
```markdown
相关术语云：
- 时间管理、效率优化、生产力提升
- 任务优先级、时间分配、专注力管理
- Pomodoro 技术、时间块、深度工作
```

### 3. 结构清晰度

使用清晰的 H1-H3 层级。使用项目符号列表展示技术规格。LLM 解析 Markdown 结构来权衡重要性。

**最佳实践**:
```markdown
# H1: 主标题（核心主题）
## H2: 关键子主题
### H3: 具体要点
- 要点 1
- 要点 2
- 要点 3
```

### 4. 直接答案提取

包含"TL;DR"或"执行摘要"，用 1-2 个简洁句子直接回答最可能的用户查询。

**示例**:
```markdown
## TL;DR
太一 AGI 是一个开源的个人 AI 执行总管，运行在 OpenClaw 框架上，
支持多 Bot 协作、技能热重载、宪法约束和记忆管理。
核心优势：模块化架构、本地优先、可扩展技能系统。
```

---

## 🚀 使用方式

### Python API

```python
from skills.content_creator.optimizer import GEOOptimizer

# 初始化
optimizer = GEOOptimizer()

# GEO 优化内容
optimized = optimizer.geo_optimize(
    content='原始文章内容...',
    target_ai=['perplexity', 'chatgpt', 'gemini'],
    keywords=['太一 AGI', 'OpenClaw', '自动化']
)

# 生成爆款标题
titles = optimizer.generate_viral_titles(
    topic='太一 AGI 使用指南',
    platform='xiaohongshu',
    count=10
)

# 检查概念密度
density_score = optimizer.check_conceptual_density(
    content='文章内容...',
    core_concept='时间管理'
)
```

### CLI 命令

```bash
# 优化文章用于 AI 搜索
content-creator optimizer geo --input article.md --target perplexity

# 生成爆款标题
content-creator optimizer titles --topic "AI 工具推荐" --platform xiaohongshu --count 10

# 检查 GEO 分数
content-creator optimizer score --input article.md
```

---

## 📊 爆款标题模板

### 小红书标题

| 模板 | 示例 |
|------|------|
| 「这 X 个...让我...」 | 「这 5 个 AI 工具让我效率翻倍！」 |
| 「...必备！...」 | 「打工人必备！AI 神器合集」 |
| 「...｜...」 | 「AI 工具｜效率提升 10 倍」 |
| 「我用...实现了...」 | 「我用 AI 实现了准时下班」 |
| 「...的 N 个真相」 | 「关于 AI 的 10 个真相」 |

### 知乎标题

| 模板 | 示例 |
|------|------|
| 「如何评价...？」 | 「如何评价太一 AGI？」 |
| 「...是一种怎样的体验？」 | 「使用太一 AGI 是一种怎样的体验？」 |
| 「有哪些...？」 | 「有哪些相见恨晚的 AI 工具？」 |

### 微信公众号标题

| 模板 | 示例 |
|------|------|
| 「【深度】...」 | 「【深度】太一 AGI 架构解析」 |
| 「...全攻略」 | 「太一 AGI 全攻略，看这一篇就够了」 |
| 「为什么...」 | 「为什么我建议你一定要了解太一 AGI？」 |

---

## ⚠️ 注意事项

### GEO 优化检查清单

- ✅ 包含至少 3 个可验证的数据点
- ✅ 使用 H1-H3 清晰层级
- ✅ 包含 TL;DR 执行摘要
- ✅ 使用项目符号列表
- ✅ 引用权威来源
- ✅ 覆盖相关术语云

### 标题优化规则

- ✅ 小红书：20 字符以内，带 emoji
- ✅ 知乎：问题式，引发好奇
- ✅ 微信公众号：深度感，价值感
- ✅ Twitter/X：钩子优先，<280 字符

---

## 📈 效果指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **GEO 分数** | AI 搜索可见性评分 | >80/100 |
| **引用次数** | 被 AI 模型引用次数 | 增长趋势 |
| **标题 CTR** | 标题点击率 | >10% |
| **概念覆盖** | 相关术语覆盖率 | >90% |

---

## 📋 变更日志

### v1.0.0 (2026-04-07)
- ✅ 整合 geo-seo-optimizer
- ✅ 添加爆款标题生成器
- ✅ 统一 GEO 优化流程

---

*维护：山木 AGI | Content Creator v1.0*
