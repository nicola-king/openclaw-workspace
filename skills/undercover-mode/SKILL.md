---
name: undercover-mode
version: 1.0.0
description: undercover-mode skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Undercover Mode Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 太一
> **状态**: ✅ 已激活 | **优先级**: P3-03

---

## 📋 功能概述

提供隐身模式，低 profile 执行任务，减少通知和日志输出。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `undercover enable` | 启用隐身 | `undercover enable --duration 1h` |
| `undercover disable` | 禁用隐身 | `undercover disable` |
| `undercover status` | 查看状态 | `undercover status` |
| `undercover execute` | 隐身执行 | `undercover execute --command "git push"` |

---

## 📝 使用示例

### 示例 1: 启用隐身模式

```bash
# 太一，启用隐身模式 1 小时
undercover enable --duration 1h
```

**输出**:
```
🥷 隐身模式已启用 (60 分钟)
- 通知：静默
- 日志：最小化
- 状态：隐藏
```

### 示例 2: 隐身执行命令

```bash
# 太一，隐身推送代码
undercover execute --command "git push origin main"
```

### 示例 3: 禁用隐身模式

```bash
# 太一，退出隐身模式
undercover disable
```

**输出**:
```
😊 隐身模式已禁用
- 通知：正常
- 日志：详细
- 状态：可见
```

---

## ⚙️ 隐身模式特性

| 特性 | 正常模式 | 隐身模式 |
|------|---------|---------|
| 消息通知 | ✅ 发送 | ❌ 静默 |
| 日志详细 | ✅ 完整 | ⚠️ 最小化 |
| 状态显示 | ✅ 在线 | ❌ 隐藏 |
| 执行确认 | ✅ 需要 | ❌ 跳过 |
| 错误报告 | ✅ 详细 | ⚠️ 摘要 |

---

*创建时间：2026-04-03 09:29 | 太一 | 太一 AGI v5.0*
