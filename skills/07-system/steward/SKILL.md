---
name: steward
version: 1.0.0
description: steward skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Steward - 守藏吏管家 Bot

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：守藏吏

---

## 🎯 职责

**系统资源管理 + 健康度监控 + 技能管理**

---

## 🔧 使用命令

```bash
# 系统自检
./scripts/self-check.sh --quick

# 技能健康检查
./skills/smart-skills-manager/scripts/health-check.sh --all

# 技能安装
./skills/smart-skills-manager/scripts/install-skill.sh clawhub <skill-name>
```

---

## 📁 目录结构

| 目录/文件 | 说明 |
|----------|------|
| `collaboration-scorer/` | 协作评分器 |
| `confirmation-monitor/` | 确认监控器 |
| `intervention-monitor/` | 干预监控器 |
| `stage-verification/` | 阶段验证器 |

---

## 📊 输出格式

日志输出到 `logs/` 目录

---

## 🔗 相关文档

- `constitution/guarantees/SELF-HEAL.md` - 自愈系统
- `constitution/guarantees/CRON-GUARANTEE.md` - Cron 保障
- `skills/smart-skills-manager/SKILL.md` - 技能管理器

---

*创建：2026-04-03 22:57 | 太一 AGI*
