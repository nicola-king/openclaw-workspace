---
name: airtable-sync
version: 1.0.0
description: airtable-sync skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Airtable Sync Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 罔两
> **状态**: ✅ 已激活 | **优先级**: P2-03

---

## 📋 功能概述

提供 Airtable 表格数据同步能力，支持 CRUD 操作和批量导入导出。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `airtable list` | 列出记录 | `airtable list --base <base_id> --table <table_name>` |
| `airtable get` | 获取记录 | `airtable get --base <base_id> --table <table_name> --id <record_id>` |
| `airtable create` | 创建记录 | `airtable create --base <base_id> --table <table_name> --fields {...}` |
| `airtable update` | 更新记录 | `airtable update --base <base_id> --table <table_name> --id <record_id> --fields {...}` |
| `airtable delete` | 删除记录 | `airtable delete --base <base_id> --table <table_name> --ids [...]` |
| `airtable import` | 导入 CSV | `airtable import --base <base_id> --table <table_name> --file data.csv` |
| `airtable export` | 导出 CSV | `airtable export --base <base_id> --table <table_name> --output data.csv` |

---

## 📝 使用示例

### 示例 1: 列出记录

```bash
# 太一，列出 CRM 表中的所有客户
airtable list --base <base_id> --table "Customers" --max-records 100
```

### 示例 2: 创建记录

```bash
# 太一，添加新客户到 CRM
airtable create --base <base_id> --table "Customers" --fields '{
  "Name": "John Doe",
  "Email": "john@example.com",
  "Status": "Active"
}'
```

### 示例 3: 导出为 CSV

```bash
# 太一，导出所有客户数据
airtable export --base <base_id> --table "Customers" --output customers.csv
```

---

## ⚠️ 安全限制

### 自动执行的操作
- [x] `airtable list/get`
- [x] `airtable create`
- [x] `airtable export`

### 需要确认的操作
- [ ] `airtable delete`
- [ ] `airtable update` (批量)

---

*创建时间：2026-04-03 09:23 | 罔两 | 太一 AGI v5.0*
