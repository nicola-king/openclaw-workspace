---
name: notion-db
version: 1.0.0
description: notion-db skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Notion Database Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 罔两
> **状态**: ✅ 已激活 | **优先级**: P2-02

---

## 📋 功能概述

提供 Notion 数据库 CRUD 操作能力，支持页面/数据库/属性管理。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `notion pages create` | 创建页面 | `notion pages create --parent <db_id> --properties {...}` |
| `notion pages get` | 获取页面 | `notion pages get <page_id>` |
| `notion pages update` | 更新页面 | `notion pages update <page_id> --properties {...}` |
| `notion pages delete` | 删除页面 | `notion pages delete <page_id>` |
| `notion databases query` | 查询数据库 | `notion databases query <db_id> --filter {...}` |
| `notion databases get` | 获取数据库 | `notion databases get <db_id>` |
| `notion blocks append` | 添加内容块 | `notion blocks append <page_id> --blocks [...]` |

---

## 📝 使用示例

### 示例 1: 查询数据库

```bash
# 太一，查询任务数据库中所有未完成的任务
notion databases query <db_id> --filter '{"property":"Status","select":{"equals":"Not Started"}}'
```

### 示例 2: 创建新页面

```bash
# 太一，在任务数据库创建新任务
notion pages create --parent <db_id> --properties '{
  "Name": {"title": [{"text": {"content": "New Task"}}]},
  "Status": {"select": {"name": "Not Started"}},
  "Due Date": {"date": {"start": "2026-04-10"}}
}'
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `notion pages/databases get`
- [x] `notion databases query`
- [x] `notion pages create` (非归档数据库)

### 需要确认的操作
- [ ] `notion pages delete`
- [ ] `notion pages update` (归档数据库)

---

*创建时间：2026-04-03 09:22 | 罔两 | 太一 AGI v5.0*
