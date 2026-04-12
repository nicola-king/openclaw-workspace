---
name: cost-tracker
version: 1.0.0
description: cost-tracker skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Cost Tracker Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 庖丁
> **状态**: ✅ 已激活 | **优先级**: P4-05

---

## 📋 功能概述

提供实时 API 成本追踪能力，支持多平台成本分析和预算告警。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `cost status` | 当前成本 | `cost status --today` |
| `cost report` | 成本报告 | `cost report --period week` |
| `cost breakdown` | 分类明细 | `cost breakdown --by model` |
| `cost budget` | 预算设置 | `cost budget --set 100 --currency CNY` |
| `cost alert` | 告警配置 | `cost alert --threshold 80 --action notify` |
| `cost predict` | 成本预测 | `cost predict --days 30` |

---

## 📊 成本追踪

| 平台 | API | 单价 | 今日用量 | 今日成本 |
|------|-----|------|---------|---------|
| 百炼 | qwen3.5-plus | ¥0.01/1K | 50K | ¥0.50 |
| Google | gemini-2.5-pro | 免费 | 100K | $0.00 |
| OpenAI | gpt-4o | $0.01/1K | 0 | $0.00 |

---

## 📝 使用示例

### 示例 1: 查看今日成本

```bash
# 太一，今天花了多少 API 成本？
cost status --today
```

**输出**:
```
📊 今日成本报告 (2026-04-03)
━━━━━━━━━━━━━━━━━━━━━━
百炼 (qwen3.5-plus): ¥0.50
Google (gemini):     $0.00
OpenAI (gpt-4o):     $0.00
━━━━━━━━━━━━━━━━━━━━━━
总计：¥0.50 (~$0.07)
预算：¥100.00
剩余：¥99.50 (99.5%)
```

### 示例 2: 周成本报告

```bash
# 太一，生成周成本报告
cost report --period week
```

### 示例 3: 设置预算告警

```bash
# 太一，设置预算告警，超过 80% 时通知我
cost budget --set 100 --currency CNY
cost alert --threshold 80 --action wechat-notify
```

---

## 🚨 告警级别

| 级别 | 阈值 | 动作 |
|------|------|------|
| 提醒 | 50% | 日志记录 |
| 警告 | 80% | 微信通知 |
| 严重 | 95% | 微信 + 暂停 |
| 超支 | 100% | 暂停 API |

---

*创建时间：2026-04-03 09:36 | 庖丁 | 太一 AGI v5.0*
