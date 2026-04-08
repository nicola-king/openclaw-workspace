---
name: agent-swap
version: 1.0.0
description: agent-swap skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Agent Swap Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 太一
> **状态**: ✅ 已激活 | **优先级**: P4-04

---

## 📋 功能概述

提供动态切换 Agent 模型能力，支持运行时模型切换。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `agent list` | 列出模型 | `agent list` |
| `agent switch` | 切换模型 | `agent switch --model qwen3.5-plus` |
| `agent status` | 当前模型 | `agent status` |
| `agent benchmark` | 性能测试 | `agent benchmark --task coding` |
| `agent cost` | 成本对比 | `agent cost --models qwen,gemini,claude` |

---

## 🤖 支持模型

| 模型 | 提供商 | 适用场景 | 成本 |
|------|--------|---------|------|
| qwen3.5-plus | 百炼 | 通用 | ¥ |
| qwen3-coder | 百炼 | 代码 | ¥ |
| gemini-2.5-pro | Google | 长文本 | $ |
| claude-3.5 | Anthropic | 推理 | $$ |
| gpt-4o | OpenAI | 多模态 | $$ |

---

## 📝 使用示例

### 示例 1: 查看当前模型

```bash
# 太一，当前用什么模型？
agent status
```

**输出**:
```
当前模型：qwen3.5-plus
- 提供商：百炼
- Context: 131K
- 成本：¥0.01/1K tokens
```

### 示例 2: 切换模型

```bash
# 太一，切换到 Gemini 处理长文档
agent switch --model gemini-2.5-pro
```

### 示例 3: 模型对比

```bash
# 太一，对比各模型成本
agent cost --models qwen3.5-plus,gemini-2.5-pro,claude-3.5-sonnet
```

---

*创建时间：2026-04-03 09:35 | 太一 | 太一 AGI v5.0*
