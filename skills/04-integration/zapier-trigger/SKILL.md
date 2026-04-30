---
name: zapier-trigger
version: 1.0.0
description: zapier-trigger skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Zapier Trigger Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 罔两
> **状态**: ✅ 已激活 | **优先级**: P2-04

---

## 📋 功能概述

提供 Zapier 自动化触发能力，支持触发 Zaps 和管理工作流。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `zapier trigger` | 触发 Zap | `zapier trigger --zap-id <id> --data {...}` |
| `zapier zaps list` | 列出 Zaps | `zapier zaps list` |
| `zapier zaps get` | 获取 Zap 详情 | `zapier zaps get <zap_id>` |
| `zapier zaps enable` | 启用 Zap | `zapier zaps enable <zap_id>` |
| `zapier zaps disable` | 禁用 Zap | `zapier zaps disable <zap_id>` |
| `zapier executions list` | 列出执行记录 | `zapier executions list --zap-id <id>` |

---

## 📝 使用示例

### 示例 1: 触发 Zap

```bash
# 太一，触发新客户通知 Zap
zapier trigger --zap-id <zap_id> --data '{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "deal_value": 5000
}'
```

### 示例 2: 列出所有 Zaps

```bash
# 太一，列出所有启用的 Zaps
zapier zaps list --status enabled
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `zapier zaps list/get`
- [x] `zapier executions list`
- [x] `zapier trigger` (非关键 Zaps)

### 需要确认的操作
- [ ] `zapier zaps enable/disable`
- [ ] `zapier trigger` (关键业务 Zaps)

---

*创建时间：2026-04-03 09:24 | 罔两 | 太一 AGI v5.0*
