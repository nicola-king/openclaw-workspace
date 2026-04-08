# Auto-Exec Skill - 智能自动执行引擎

> 🆕 创建时间：2026-04-01 | 版本：v1.0 | 状态：✅ 已激活

---

## 🎯 概述

将原有的智能自动化脚本升级为标准化 OpenClaw Skill，提供：
- **状态管理** - 统一的执行状态追踪
- **任务发现** - 自动从 HEARTBEAT.md 和 memory 文件发现任务
- **进度汇报** - 每 5 分钟自动生成进度报告
- **阻塞检测** - 自动识别并上报阻塞任务

---

## 📦 模块结构

```
skills/auto-exec/
├── SKILL.md          # Skill 定义文档
├── __init__.py       # 模块导出
├── core.py           # 核心引擎（状态管理 + 任务发现）
├── reporter.py       # 进度汇报生成器
├── report.py         # Cron 汇报脚本
└── test.py           # 测试套件
```

---

## 🔧 安装

Skill 已创建，无需额外安装。验证：

```bash
cd ~/.openclaw/workspace/skills/auto-exec
python3 test.py
```

---

## 📖 使用

### Python API

```python
from auto_exec import AutoExecStatus, TaskDiscovery, ProgressReporter

# 状态管理
engine = AutoExecStatus()
status = engine.get_status()
engine.update_status(progress=50, nextStep="执行中")

# 任务发现
discovery = TaskDiscovery()
tasks = discovery.discover()

# 进度汇报
reporter = ProgressReporter()
report = reporter.generate_report()
```

### 命令行

```bash
# 查看状态
python3 -c "from auto_exec import status; print(status())"

# 发现任务
python3 -c "from auto_exec import discover_tasks; print(discover_tasks())"

# 生成汇报
python3 skills/auto-exec/report.py
```

### Cron 集成

原有的 15 个 Cron 任务已统一使用 taiyi 账号发送，无需修改。

如需添加新的自动汇报：

```bash
openclaw cron add \
  --name "auto-progress-5m" \
  --schedule "*/5 * * * *" \
  --agent "taiyi" \
  --command "python3 ~/.openclaw/workspace/skills/auto-exec/report.py"
```

---

## 📊 状态文件

| 文件 | 用途 | 大小 |
|------|------|------|
| `/tmp/auto-exec-status.json` | 当前执行状态 | ~1KB |
| `/tmp/task-tracker.json` | 任务追踪 | ~2KB |
| `/tmp/progress-history.json` | 进度历史 | ~5KB |
| `/tmp/blocked-tasks.json` | 阻塞任务 | ~1KB |

---

## 🛡️ 容错机制

1. **自动重试** - 执行失败自动重试 3 次
2. **状态恢复** - 状态文件损坏自动重建
3. **阻塞跳过** - 阻塞任务自动跳过并上报
4. **日志持久化** - 所有操作写入日志文件

---

## 📝 日志

- 执行日志：`/tmp/openclaw/auto-exec.log`
- 汇报日志：`/tmp/openclaw/auto-exec-report.log`
- 状态变更：写入 `memory/YYYY-MM-DD.md`

---

## 🧪 测试

```bash
cd ~/.openclaw/workspace/skills/auto-exec
python3 test.py
```

预期输出：
```
==================================================
Auto-Exec Skill 功能测试
==================================================
📊 测试状态引擎...
  ✅ 状态读取正常：idle
  ✅ 状态更新正常：50%
  ✅ 任务设置正常：TEST-001
  ✅ 步骤完成标记正常

🔍 测试任务发现...
  ✅ 发现 3 个任务
  示例：TASK-050: 知几首笔下注 [P0]

📝 测试汇报生成...
  ✅ 汇报生成正常 (350 字符)

🔄 自动执行进度汇报
...

==================================================
测试结果：3 通过，0 失败
==================================================
```

---

## 🔄 升级记录

### v1.0 (2026-04-01)
- ✅ 创建标准化 Skill 结构
- ✅ 迁移原有脚本功能
- ✅ 添加测试套件
- ✅ 集成 Cron 系统
- ✅ 统一使用 taiyi 账号发送

---

## 📚 相关文档

- 宪法：`constitution/automation/AUTO-EXEC-GUARANTEE.md`
- 状态管理：`core.py`
- 汇报生成：`reporter.py`
- 测试套件：`test.py`

---

*创建：2026-04-01 | 太一 AGI | 智能自动化架构*
