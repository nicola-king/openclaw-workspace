---
name: yijing
version: 1.0.0
description: yijing skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Yijing - 易经决策技能

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：太一

---

## 🎯 职责

**易经占卜决策辅助**，提供传统智慧的现代应用

---

## 🔧 使用命令

```bash
# 起卦
python3 yijing-divination.py --question <问题>

# 解卦
python3 yijing-interpret.py --hexagram <卦象>

# 查看历史
python3 yijing-history.py --date <日期>
```

---

## 📁 目录结构

| 目录/文件 | 说明 |
|----------|------|
| `agent/` | 易经 Agent |
| `data/` | 卦象数据 |
| `interpretations/` | 解卦模板 |

---

## 📊 输出格式

占卜结果存入 `memory/yijing/` 目录

---

*创建：2026-04-03 22:57 | 太一 AGI*
