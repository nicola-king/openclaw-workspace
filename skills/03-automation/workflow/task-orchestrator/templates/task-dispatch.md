# 📬 {BOT_EMOJI} {BotName} - 任务委派单

> **分发时间**: {TIMESTAMP} | **派发者**: 太一 | **优先级**: {PRIORITY}

---

## 🎯 任务列表

{TASK_ITEMS}

---

## 📤 汇报要求

**汇报位置**: `~/.openclaw/agents/{bot}/outbox/`

**汇报格式**:
```markdown
【{bot}汇报 · TASK-XXX】
时间：YYYY-MM-DD HH:mm
状态：✅ 完成 / 🟡 执行中 / 🔴 阻塞
产出：文件列表
阻塞：无/具体原因
```

---

## ⏱️ 时间节点

| 时间 | 事件 |
|------|------|
| **{DISPATCH_TIME}** | 任务分发 |
| **{CONFIRM_DEADLINE}** | 确认截止 (+5 分钟) |
| **{COMPLETION_DEADLINE}** | 完成截止 |

---

## 🚨 纠偏机制

### 自动检测
- 10 分钟未确认 → 自动提醒
- 30 分钟进度滞后 → 告警
- 1 小时进度滞后 → 太一介入
- 2 小时进度滞后 → 重新分配

### 阻塞上报
如遇阻塞，立即写入 outbox:
`BLOCKED-{TASK_ID}.md`

---

*{BotName}收到请回复确认！*

---

*Task Orchestrator v1.0 | 太一 AGI*
