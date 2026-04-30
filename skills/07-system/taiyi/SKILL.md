---
name: taiyi
version: 1.0.0
description: 太一 - AGI 执行总管与多 Bot 协调
category: other
tags: ['taiyi', 'agi', 'orchestrator']
author: 太一 AGI
created: 2026-04-07
---


# Taiyi - 太一 AGI 执行总管

> 版本：v1.0 | 创建：2026-04-03 | 负责 Bot：太一

---

## 🎯 职责

**AGI 执行总管**，统筹多 Bot 协作 + 任务调度 + 决策建议

---

## 🔧 使用命令

```bash
# 任务调度
python3 taiyi-orchestrator.py --task <任务描述>

# 多 Bot 协作
python3 taiyi-collaboration.py --bots zhiji,shanmu,suwen --task <任务>

# 决策建议
python3 taiyi-decision.py --context <上下文>
```

---

## 📁 目录结构

| 目录/文件 | 说明 |
|----------|------|
| `agent-diary.md` | Agent 日志 |
| `agent-friendliness.md` | Agent 友好度 |
| `night-learning/` | 夜间学习 |
| `orchestrator/` | 任务调度器 |

---

## 📊 输出格式

决策输出到 `memory/taiyi/` 目录

---

## 🔗 相关文档

- `SOUL.md` - 太一身份锚点
- `constitution/CONST-ROUTER.md` - 宪法路由器
- `constitution/directives/TURBOQUANT.md` - TurboQuant 记忆

---

*创建：2026-04-03 22:57 | 太一 AGI*
