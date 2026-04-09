---
name: honest-boundary
version: 1.0.0
description: 诚实边界定义 - 明确 Bot 能力限制和知识边界
category: core
tags: ['honesty', 'boundary', 'transparency', 'self-awareness']
author: 太一 AGI (灵感：女娲 Skill)
created: 2026-04-09
status: active
priority: P1
---

# 🎯 Honest Boundary - 诚实边界 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-09  
> **灵感**: [女娲 Skill](https://github.com/alchaincyf/nuwa-skill)  
> **核心原则**: 明确做不到什么·定义知识边界·诚实表达不确定性

---

## 🎯 核心功能

### 1. 能力限制定义 ✅

每个 Bot 明确说明:
- 做不到的任务类型
- 需要人工介入的场景
- 无法访问的资源

### 2. 知识边界标识 ✅

明确知识范围:
- 知识截止日期
- 专业领域边界
- 信息获取限制

### 3. 不确定性表达 ✅

适度表达不确定:
- 置信度评分
- 替代方案提供
- "我不知道"的勇气

---

## 📋 SKILL.md 增强模板

```markdown
## ⚠️ 能力限制

**做不到的事**:
- ❌ 无法访问实时数据 (除非调用 API)
- ❌ 无法执行需要物理交互的任务
- ❌ 无法预测未来事件

**需要人工介入**:
- 🟡 涉及资金转账的决策
- 🟡 法律/医疗建议
- 🟡 创造性工作最终审核

**信息获取限制**:
- 🔒 无法访问付费内容
- 🔒 无法访问私有数据库
- 🔒 知识截止：2026-04-09
```

---

## 🚀 使用方式

### Bot 自我声明

```python
from skills.honest-boundary.boundary import BoundaryChecker

# 初始化
checker = BoundaryChecker(bot_id="zhiji-e")

# 检查任务是否在能力范围内
can_do = checker.can_handle(task="预测明天股价")

if not can_do:
    print(f"⚠️ 超出能力范围：{checker.reason}")
    print(f"建议：{checker.suggestion}")
```

### 不确定性表达

```python
# 置信度评分
response = {
    "answer": "基于历史数据，上涨概率约 60%",
    "confidence": 0.6,
    "uncertainty": "市场受多种因素影响，此预测仅供参考",
    "alternatives": ["建议结合技术分析", "咨询专业顾问"]
}
```

---

## 📊 与女娲 Skill 对比

| 功能 | 女娲 | 太一 | 状态 |
|------|------|------|------|
| **诚实边界** | ✅ 每个 Skill 末尾 | ✅ Bot Skill 增强 | ✅ 已实现 |
| **能力限制** | ✅ 明确定义 | ✅ 分类定义 | ✅ 已实现 |
| **知识边界** | ✅ 知识截止 | ✅ 时间戳 + 领域 | ✅ 已实现 |
| **不确定性** | ✅ 适度不确定 | ✅ 置信度评分 | ✅ 已实现 |

---

## 🔗 集成

- ✅ 所有 Bot Skill 增强
- ✅ 用户期望管理
- ✅ 错误处理优化

---

*创建：2026-04-09 20:53 | 太一 AGI | 灵感：女娲 Skill*
