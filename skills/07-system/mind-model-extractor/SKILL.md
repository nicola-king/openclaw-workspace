---
name: mind-model-extractor
version: 1.0.0
description: 心智模型提取 - 从对话历史识别用户思维框架
category: core
tags: ['mind-model', 'extraction', 'cognitive', 'user-modeling']
author: 太一 AGI (灵感：女娲 Skill)
created: 2026-04-09
status: active
priority: P1
---

# 🧠 Mind Model Extractor - 心智模型提取 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-09  
> **灵感**: [女娲 Skill](https://github.com/alchaincyf/nuwa-skill)  
> **核心功能**: 从对话历史识别用户心智模型·决策启发式·表达 DNA

---

## 🎯 核心功能

### 1. 心智模型识别 ✅

从用户对话中提取思维框架:
- 逆向思维 ("反过来会怎样？")
- 第一性原理 ("物理极限是多少？")
- 二阶思维 ("然后呢？")
- 概率思维 ("期望值是多少？")

### 2. 决策启发式提取 ✅

从用户历史决策中提取经验法则:
- 优先级规则
- 风险评估方式
- 选择标准

### 3. 表达 DNA 分析 ✅

分析用户表达习惯:
- 常用词汇/句式
- 语气风格
- 回复长度偏好

---

## 🚀 使用方式

```python
from skills.mind_model_extractor.extractor import MindModelExtractor

# 初始化
extractor = MindModelExtractor()

# 分析对话历史
models = extractor.extract_mind_models(conversation_history)

# 提取决策启发式
heuristics = extractor.extract_heuristics(decision_history)

# 分析表达 DNA
dna = extractor.analyze_expression_dna(messages)

# 生成用户心智档案
profile = extractor.generate_profile()
```

---

## 📊 输出格式

```json
{
  "mind_models": [
    {
      "name": "第一性原理",
      "description": "从基本原理推导，不类比",
      "examples": ["这个事的物理极限是什么？", "抛开现有方案，最优解是什么？"],
      "frequency": 0.8
    }
  ],
  "decision_heuristics": [
    {
      "name": "成本优先",
      "rule": "在质量相当时选择成本最低的",
      "examples": ["选便宜的那个就行"],
      "confidence": 0.9
    }
  ],
  "expression_dna": {
    "style": "极简黑客风",
    "avg_length": 50,
    "common_phrases": ["✅", "🚀", "SAYELF"],
    "tone": "直接/高效"
  }
}
```

---

## 🔗 集成

- ✅ 用户模型 (user-model.json)
- ✅ Hermes 学习循环
- ✅ Brain/Hands 架构

---

*创建：2026-04-09 20:53 | 太一 AGI | 灵感：女娲 Skill*
