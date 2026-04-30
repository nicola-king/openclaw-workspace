---
name: gumroad
version: 1.0.0
description: gumroad skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Gumroad - Gumroad 数字产品销售

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：庖丁

---

## 🎯 职责

**Gumroad 数字产品上架与销售管理**

---

## 🔧 使用命令

```bash
# 创建产品
python3 gumroad-create.py --name <产品名> --price <价格>

# 查看销售数据
python3 gumroad-stats.py

# 更新产品
python3 gumroad-update.py --product <ID> --field <字段> --value <值>
```

---

## 📊 输出格式

产品销售数据存入 `memory/gumroad/` 目录

---

## ⚠️ 状态

**当前**: 🟡 待配置 API Key

**已有产品**:
- 《OpenClaw 快速入门指南》- https://chuanxi.gumroad.com/l/qdxnm

**下一步**:
1. 获取 Gumroad API Key
2. 配置认证
3. 批量上架技能产品

---

*创建：2026-04-03 22:50 | 太一 AGI*
