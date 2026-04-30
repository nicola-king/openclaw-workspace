---
name: meta-learner
type: agent
version: 1.0.0
description: 元学习器 Agent - 教 AI 如何学习
category: meta
tags: ['meta-learning', 'skill-acquisition', 'learning-strategy', 'optimization']
author: 太一 AGI (能力涌现·自主进化)
created: 2026-04-09
status: active
priority: P0
---

# 🧠 元学习器 Agent - 教 AI 如何学习 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-09  
> **能力涌现**: 太一体系自进化创建  
> **定位**: 学习策略优化·技能获取加速·元认知  
> **核心理念**: "学会如何学习"

---

## 🎯 核心功能

### 1. 学习策略优化 ✅

**策略库**:
- 费曼学习法
- 刻意练习
- 间隔重复
- 知识树构建
- 类比迁移

**优化逻辑**:
```
分析学习任务
    ↓
匹配最优策略
    ↓
生成学习计划
    ↓
执行 + 监控
    ↓
策略调整
```

---

### 2. 技能获取加速 ✅

**加速方法**:
- 先学核心 20%
- 建立知识框架
- 实践驱动学习
- 即时反馈循环

---

### 3. 元认知监控 ✅

**监控内容**:
- 理解程度评估
- 记忆强度检测
- 迁移能力测试
- 学习盲点识别

---

### 4. 学习资源推荐 ✅

**推荐依据**:
- 当前水平
- 学习风格
- 目标技能
- 可用时间

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────┐
│              元学习器 Agent                      │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐              │
│  │ 策略库      │  │ 评估器      │              │
│  │ Strategies  │  │ Evaluator   │              │
│  └─────────────┘  └─────────────┘              │
│  ┌─────────────┐  ┌─────────────┐              │
│  │ 计划生成器  │  │ 推荐引擎    │              │
│  │ Planner     │  │ Recommender │              │
│  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────┘
```

---

## 🚀 使用方式

```python
from agents.meta_learner.learner import MetaLearner

# 初始化
learner = MetaLearner()

# 生成学习计划
plan = learner.create_learning_plan(
    skill="Python 数据分析",
    current_level="beginner",
    target_level="intermediate",
    available_hours=20
)

# 推荐学习资源
resources = learner.recommend_resources(
    skill="Python 数据分析",
    learning_style="visual"
)

# 评估理解程度
assessment = learner.assess_understanding(
    topic="Pandas DataFrame",
    quiz_score=0.8
)
```

---

## ⚠️ 能力限制

**做不到的事**:
- ❌ 无法替代实际学习
- ❌ 无法保证学习效果
- ❌ 无法访问外部课程

---

*创建：2026-04-09 21:20 | 太一 AGI · 能力涌现自主进化*
