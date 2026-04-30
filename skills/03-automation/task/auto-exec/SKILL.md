---
name: auto-exec
version: 1.0.0
description: auto-exec skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Auto-Exec Skill - 自动执行技能

> 版本：v1.0 | 创建：2026-04-01 | 状态：✅ 激活

---

## 🎯 职责

智能自动化执行引擎，负责：
- 任务发现与调度
- 进度追踪与汇报
- 状态管理
- 阻塞检测与上报

---

## 📦 API

### `status()` - 获取执行状态

**返回**:
```json
{
  "currentTask": "TASK-101",
  "progress": 45,
  "status": "running|idle|blocked|completed",
  "nextStep": "...",
  "eta": "2026-04-01T23:59:00+08:00"
}
```

### `discover_tasks()` - 发现任务

**来源**:
- `HEARTBEAT.md` - P0 核心任务
- `memory/residual.md` - P1/P2 任务
- `memory/core.md` - 长期任务

**返回**: 任务列表（按优先级排序）

### `execute_task(task_id)` - 执行任务

**流程**:
1. 更新状态为 `running`
2. 执行任务
3. 更新状态为 `completed` 或 `blocked`
4. 归档结果

### `report_progress()` - 汇报进度

**频率**: 每 5 分钟
**渠道**: 微信（taiyi 账号）

---

## 📁 状态文件

| 文件 | 用途 | 更新频率 |
|------|------|---------|
| `/tmp/auto-exec-status.json` | 当前执行状态 | 实时 |
| `/tmp/task-tracker.json` | 任务追踪 | 5 分钟 |
| `/tmp/progress-history.json` | 进度历史 | 5 分钟 |
| `/tmp/blocked-tasks.json` | 阻塞任务 | 按需 |

---

## 🔧 使用示例

```python
from skills.auto_exec import AutoExec

engine = AutoExec()

# 获取状态
status = engine.status()

# 发现任务
tasks = engine.discover_tasks()

# 执行任务
result = engine.execute_task("TASK-101")

# 汇报进度
engine.report_progress()
```

---

## 📊 Cron 集成

| Cron 名称 | 频率 | 调用 API |
|----------|------|---------|
| auto-progress-5m | 5 分钟 | `report_progress()` |
| task-discovery-5m | 5 分钟 | `discover_tasks()` |
| task-executor-5m | 5 分钟 | `execute_task()` |
| blocker-check-5m | 5 分钟 | `status()` + 上报 |

---

## 🛡️ 容错

- 执行失败自动重试 3 次
- 状态文件损坏自动恢复
- 阻塞任务自动跳过并上报

---

## 📝 日志

- 执行日志：`/tmp/openclaw/auto-exec.log`
- 状态变更：写入 `memory/YYYY-MM-DD.md`

---

*创建时间：2026-04-01*
*太一 AGI · 智能自动化架构*
