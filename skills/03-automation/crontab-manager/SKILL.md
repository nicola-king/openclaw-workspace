---
name: crontab-manager
version: 1.0.0
description: crontab-manager skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Crontab Manager Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 守藏吏
> **状态**: ✅ 已激活 | **优先级**: P2-05

---

## 📋 功能概述

提供定时任务管理能力，支持创建/编辑/删除/监控 Cron 任务。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `crontab -l` | 列出任务 | `crontab -l` |
| `crontab -e` | 编辑任务 | `crontab -e` |
| `crontab -r` | 删除任务 | `crontab -r` |
| `crontab install` | 安装任务 | `crontab install tasks.cron` |
| `cron status` | 查看状态 | `cron status <task_name>` |
| `cron logs` | 查看日志 | `cron logs <task_name> --lines 50` |
| `cron enable` | 启用任务 | `cron enable <task_name>` |
| `cron disable` | 禁用任务 | `cron disable <task_name>` |

---

## 📝 使用示例

### 示例 1: 创建每日备份任务

```bash
# 太一，创建每日 02:00 备份任务
crontab install <<EOF
0 2 * * * /home/nicola/.openclaw/workspace/scripts/daily-backup.sh >> /var/log/backup.log 2>&1
EOF
```

### 示例 2: 查看任务状态

```bash
# 太一，查看备份任务的执行状态
cron status daily-backup
cron logs daily-backup --lines 20
```

### 示例 3: 临时禁用任务

```bash
# 太一，临时禁用备份任务
cron disable daily-backup
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `crontab -l`
- [x] `cron status/logs`
- [x] `crontab install` (用户目录脚本)

### 需要确认的操作
- [ ] `crontab -r` (删除所有)
- [ ] `crontab install` (系统级任务)
- [ ] `cron enable/disable` (关键任务)

---

*创建时间：2026-04-03 09:25 | 守藏吏 | 太一 AGI v5.0*
