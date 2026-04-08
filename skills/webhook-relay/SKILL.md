---
name: webhook-relay
version: 1.0.0
description: webhook-relay skill
category: tools
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Webhook Relay Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 罔两
> **状态**: ✅ 已激活 | **优先级**: P2-06

---

## 📋 功能概述

提供 Webhook 接收/转发/处理能力，支持 GitHub/Slack/Stripe 等常见服务。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `webhook server start` | 启动服务 | `webhook server start --port 8080` |
| `webhook route create` | 创建路由 | `webhook route create --path /github --handler github-handler.sh` |
| `webhook route list` | 列出路由 | `webhook route list` |
| `webhook route delete` | 删除路由 | `webhook route delete --path /github` |
| `webhook logs` | 查看日志 | `webhook logs --path /github --lines 50` |
| `webhook forward` | 转发请求 | `webhook forward --from /github --to https://api.example.com` |

---

## 📝 使用示例

### 示例 1: 启动 Webhook 服务器

```bash
# 太一，启动 Webhook 服务器监听 8080 端口
webhook server start --port 8080
```

### 示例 2: 创建 GitHub 路由

```bash
# 太一，创建 GitHub webhook 路由
webhook route create --path "/github" --handler "/home/nicola/.openclaw/workspace/scripts/github-webhook-handler.sh"
```

### 示例 3: 查看 Webhook 日志

```bash
# 太一，查看最近 50 条 GitHub webhook 请求
webhook logs --path "/github" --lines 50
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `webhook route list`
- [x] `webhook logs`
- [x] `webhook server start` (端口>1024)

### 需要确认的操作
- [ ] `webhook route create` (敏感路径)
- [ ] `webhook forward` (外部 URL)
- [ ] `webhook server start` (端口<1024)

---

*创建时间：2026-04-03 09:26 | 罔两 | 太一 AGI v5.0*
