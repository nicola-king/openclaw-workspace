---
name: marketplace
version: 1.0.0
description: marketplace skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Marketplace - 技能市场集成

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：守藏吏

---

## 🎯 职责

**OpenClaw 技能市场集成**，支持技能发现/安装/更新/分享

---

## 🔧 使用命令

```bash
# 搜索技能
clawhub search <keyword>

# 安装技能
clawhub install <skill-name>

# 更新技能
clawhub update <skill-name>

# 发布技能
clawhub publish <skill-path>
```

---

## 📊 输出格式

技能市场数据存入 `memory/marketplace/` 目录

---

## ⚠️ 状态

**当前**: 🟡 待配置 clawhub CLI

**下一步**:
1. 安装 clawhub CLI: `npm install -g clawhub`
2. 配置认证
3. 测试技能发布流程

---

*创建：2026-04-03 22:50 | 太一 AGI*
