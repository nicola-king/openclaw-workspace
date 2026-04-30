---
name: slack-notify
version: 1.0.0
description: slack-notify skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Slack Notify Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 山木
> **状态**: ✅ 已激活 | **优先级**: P2-01

---

## 📋 功能概述

提供 Slack 消息推送能力，支持频道/线程/文件/表情反应等操作。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `slack send` | 发送消息 | `slack send --channel #general --text "Hello"` |
| `slack send-thread` | 回复线程 | `slack send-thread --channel #general --thread-ts 123.456 --text "Reply"` |
| `slack upload` | 上传文件 | `slack upload --channel #general --file report.pdf` |
| `slack react` | 表情反应 | `slack react --channel #general --ts 123.456 --emoji "+1"` |
| `slack channels` | 列出频道 | `slack channels` |
| `slack history` | 查看历史 | `slack history --channel #general --limit 10` |

---

## 📝 使用示例

### 示例 1: 发送消息到频道

```bash
# 太一，发送消息到 #general 频道
slack send --channel "#general" --text "🚀 新版本已部署！"
```

### 示例 2: 上传文件

```bash
# 太一，上传报告到 #reports 频道
slack upload --channel "#reports" --file ./weekly-report.pdf --initial-comment "周报请查收"
```

### 示例 3: 线程回复

```bash
# 太一，回复这条消息的线程
slack send-thread --channel "#general" --thread-ts "1234567890.123456" --text "收到，正在处理"
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `slack send` (公开频道)
- [x] `slack react`
- [x] `slack channels/history`

### 需要确认的操作
- [ ] `slack send` (私人群组)
- [ ] `slack upload` (大文件 >10MB)
- [ ] `slack send` (@channel/@here)

---

*创建时间：2026-04-03 09:21 | 山木 | 太一 AGI v5.0*
