---
name: wangliang
version: 1.0.0
description: 王良 - 知识库搜索与问答
category: data
tags: ['wangliang', 'knowledge', 'search']
author: 太一 AGI
created: 2026-04-07
---


# Wangliang - 罔两数据采集 Bot

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：罔两

---

## 🎯 职责

**数据采集 + CEO 视角分析**，包括网页爬虫/API 调用/数据分析

---

## 🔧 使用命令

```bash
# 数据采集
python3 wangliang-collector.py --source <数据源> --output <输出文件>

# 数据分析
python3 wangliang-analyzer.py --input <数据文件> --report

# 高价值发现
python3 wangliang-high-value.py --keyword <关键词>
```

---

## 📁 目录结构

| 目录/文件 | 说明 |
|----------|------|
| `cross-border/` | 跨境数据 |
| `data/` | 采集数据 |
| `high-value-discovery/` | 高价值发现 |

---

## 📊 输出格式

数据输出到 `memory/wangliang/` 目录

---

## 🔗 相关文档

- `constitution/workflows/DATA-COLLECTION.md` - 数据采集工作流

---

*创建：2026-04-03 22:57 | 太一 AGI*
