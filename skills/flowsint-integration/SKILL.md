---
name: flowsint-integration
version: 1.0.0
description: flowsint-integration skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Flowsint Integration - Flowsint 情报集成

> 版本：v1.0 | 创建：2026-03-30 | 更新：2026-04-03 | 负责 Bot：罔两

---

## 🎯 职责

**集成 Flowsint OSINT 情报系统**，提供开源情报数据采集和分析能力

---

## 🔧 使用命令

```bash
# 采集情报
python3 flowsint-collector.py --keyword <关键词>

# 分析报告
python3 flowsint-analyzer.py --report
```

---

## 📊 输出格式

情报数据存入 `memory/flowsint/` 目录

---

## ⚠️ 状态

**当前**: 🟡 待配置 API Key

**下一步**:
1. 获取 Flowsint API Key
2. 配置 `config.py`
3. 测试数据采集

---

*创建：2026-04-03 22:50 | 太一 AGI*
