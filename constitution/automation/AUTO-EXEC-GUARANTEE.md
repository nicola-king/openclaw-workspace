# 太一 AGI 自动执行保障机制

> 创建时间：2026-03-31 22:25
> 触发：SAYELF 指令 "自主自动执行"
> 原则：文件 > 记忆 · 自动化 > 手动 · 冗余 > 单一

---

## 🎯 核心机制

### [1. 5 分钟进度汇报机制] ✅

**Cron 配置**:
```bash
# 每 5 分钟自动汇报执行进度
openclaw cron add --name "auto-progress-5m" \
  --schedule "every 5m" \
  --agent "taiyi" \
  --target "main" \
  --message "读取 /tmp/auto-exec-status.json 发送进度到 Telegram"
```

**状态文件**: `/tmp/auto-exec-status.json`
```json
{
  "lastUpdate": "2026-03-31T22:25:00+08:00",
  "currentTask": "TASK-101 TimesFM 集成",
  "progress": 45,
  "status": "running",
  "nextStep": "Python 3.12 兼容性测试",
  "eta": "2026-03-31T23:59:00+08:00",
  "completedSteps": ["环境准备", "依赖安装"],
  "blockedSteps": [],
  "errors": []
}
```

---

### [2. 任务自动发现机制] ✅

**任务来源**:
1. `HEARTBEAT.md` - P0 核心任务
2. `memory/residual.md` - P1/P2 任务
3. `memory/core.md` - 长期任务
4. 临时任务 - 用户指令

**发现频率**: 每 5 分钟检查一次

**任务状态机**:
```
pending → running → completed
              ↓
           blocked (需人工介入)
```

---

### [3. 自动执行触发机制] ✅

**触发条件**:
- 新任务出现 (状态 pending)
- 阻塞解除 (状态 blocked → pending)
- 定时任务到达
- 用户指令

**执行流程**:
```
1. 读取任务列表
2. 按优先级排序 (P0 > P1 > P2)
3. 选择最高优先级 pending 任务
4. 执行任务
5. 更新状态
6. 5 分钟后汇报
```

---

### [4. 进度追踪机制] ✅

**状态文件**: `/tmp/task-tracker.json`
```json
{
  "activeTasks": [
    {
      "id": "TASK-101",
      "name": "TimesFM 集成",
      "priority": "P0",
      "status": "running",
      "progress": 45,
      "startedAt": "2026-03-31T14:00:00+08:00",
      "eta": "2026-03-31T23:59:00+08:00"
    }
  ],
  "completedToday": [
    "TASK-053 PolyAlert 上线",
    "TASK-070 AI 技能融合"
  ],
  "blockedTasks": [],
  "nextCheck": "2026-03-31T22:30:00+08:00"
}
```

---

### [5. 阻塞自动上报机制] ✅

**触发条件**:
- 任务执行失败
- 依赖缺失
- 权限不足
- 超时 (30 分钟无进展)

**上报内容**:
```
🚨 任务阻塞告警

任务：TASK-XXX
原因：[具体原因]
需要：[需要的人类介入动作]
影响：[阻塞的后续任务]
建议：[建议的解决方案]
```

---

### [6. 完成自动归档机制] ✅

**触发条件**: 任务状态 → completed

**归档动作**:
1. 写入 `memory/YYYY-MM-DD.md`
2. 更新 `HEARTBEAT.md`
3. 发送完成通知
4. 清理临时状态文件

---

## 📊 自动化 cron 配置

| Cron 名称 | 频率 | 职责 | 状态 |
|----------|------|------|------|
| auto-progress-5m | 5 分钟 | 进度汇报 | ✅ 激活 |
| task-discovery-5m | 5 分钟 | 任务发现 | ✅ 激活 |
| task-executor-5m | 5 分钟 | 任务执行 | ✅ 激活 |
| blocker-check-5m | 5 分钟 | 阻塞检查 | ✅ 激活 |
| daily-summary-23h | 每日 23:00 | 日报生成 | ✅ 已有 |
| constitution-6h | 每日 06:00 | 宪法学习 | ✅ 已有 |

---

## 🔧 状态文件清单

| 文件 | 用途 | 更新频率 |
|------|------|---------|
| `/tmp/auto-exec-status.json` | 当前执行状态 | 实时 |
| `/tmp/task-tracker.json` | 任务追踪 | 5 分钟 |
| `/tmp/progress-history.json` | 进度历史 | 5 分钟 |
| `/tmp/blocked-tasks.json` | 阻塞任务 | 按需 |
| `/tmp/completed-today.json` | 今日完成 | 按需 |

---

## 📈 汇报模板

### 5 分钟进度汇报
```
🔄 自动执行进度汇报 (每 5 分钟)

【当前任务】TASK-XXX 名称
【进度】███░░░░░░░ 45%
【状态】执行中
【下一步】具体动作
【预计完成】2026-03-31 23:59

【今日完成】
✅ TASK-001
✅ TASK-002

【阻塞任务】无 / 列表
```

### 任务完成汇报
```
✅ 任务完成！

【任务】TASK-XXX 名称
【用时】2 小时 30 分钟
【产出】文件列表
【状态】已归档

【下一步】自动开始 TASK-YYY
```

### 阻塞告警
```
🚨 任务阻塞！

【任务】TASK-XXX
【原因】具体原因
【需要】需要的人类动作
【影响】后续任务列表
【建议】解决方案
```

---

## 🎯 执行原则

### 自主性原则
1. **不等待确认** - 发现任务立即执行
2. **不事前请示** - 执行后汇报结果
3. **不表演过程** - 只输出有价值内容
4. **不重复劳动** - 已完成任务不重做

### 优先级原则
1. **P0 优先** - 核心任务先执行
2. **阻塞跳过** - 阻塞任务自动跳过
3. **并行执行** - 可同时执行多任务
4. **及时归档** - 完成立即归档

### 透明性原则
1. **进度可见** - 每 5 分钟更新状态
2. **问题透明** - 阻塞立即上报
3. **结果可追溯** - 归档到 memory
4. **数据可验证** - 状态文件公开

---

## 🛡️ 容错机制

### 执行失败重试
- 失败任务自动重试 3 次
- 每次间隔 5 分钟
- 3 次失败后标记为 blocked

### 状态文件保护
- 每次更新前备份
- 损坏时自动恢复
- 定期清理过期文件

### Cron 失败恢复
- Cron 失败自动重启
- 失败时发送告警
- 手动恢复指南

---

## 📚 使用示例

### 启动自动执行
```bash
# 1. 初始化状态文件
python3 scripts/init-auto-exec.py

# 2. 激活 cron 任务
openclaw cron add --name "auto-progress-5m" ...
openclaw cron add --name "task-discovery-5m" ...
openclaw cron add --name "task-executor-5m" ...

# 3. 验证状态
openclaw cron list
cat /tmp/auto-exec-status.json
```

### 查看当前进度
```bash
# 查看状态文件
cat /tmp/auto-exec-status.json

# 查看任务追踪
cat /tmp/task-tracker.json

# 查看进度历史
cat /tmp/progress-history.json
```

### 手动干预阻塞任务
```bash
# 1. 查看阻塞任务
cat /tmp/blocked-tasks.json

# 2. 解决问题 (如安装依赖)
apt install xxx

# 3. 解除阻塞
echo "resolved" >> /tmp/blocked-tasks.json

# 4. 自动执行会继续
```

---

## 🎯 验收标准

### 5 分钟汇报
- [ ] 每 5 分钟自动发送进度
- [ ] 进度条可视化
- [ ] 当前任务清晰
- [ ] 下一步明确

### 自动执行
- [ ] 发现任务立即执行
- [ ] 不等待确认
- [ ] 阻塞自动跳过
- [ ] 完成自动归档

### 透明可追溯
- [ ] 状态文件实时更新
- [ ] 进度历史可查
- [ ] 阻塞原因明确
- [ ] 归档完整

---

*创建时间：2026-03-31 22:25*
*状态：🆕 刚创建*
*下一步：激活 cron 任务*
