# Task Orchestrator - 智能任务编排引擎

> **版本**: 1.0.0 | **太一 AGI v5.0** | **License**: MIT

---

## 🎯 简介

Task Orchestrator 是太一 AGI 的**智能任务编排引擎**，负责任务从分解到验收的完整闭环：

```
任务分解 → 智能分配 → 分发送达 → 执行追踪 → 成果验收 → 汇报归档 → 纠偏机制
```

---

## 🚀 快速开始

### 任务分解

```bash
python3 orchestrator.py decompose "开发一个网页爬虫"
```

### 任务分发

```bash
python3 orchestrator.py dispatch suwen
```

### 进度追踪

```bash
python3 task-tracker.py scan
```

### 成果验收

```bash
python3 validator.py validate suwen TASK-20260403-1312-DEV-001
```

### 纠偏检测

```bash
python3 correction.py detect
```

### 生成报告

```bash
python3 orchestrator.py summary
```

---

## 📁 文件结构

```
skills/task-orchestrator/
├── SKILL.md           # Skills 定义
├── orchestrator.py    # 核心编排引擎
├── task-tracker.py    # 执行追踪器
├── validator.py       # 成果验收器
├── correction.py      # 纠偏机制
├── clawhub.yaml       # ClawHub 配置
└── README.md          # 本文件
```

---

## 🔄 核心流程

### 1. 任务分解 (Decomposition)

将自然语言任务拆解为结构化子任务：

```python
from orchestrator import TaskOrchestrator

orchestrator = TaskOrchestrator()
subtasks = orchestrator.decompose("开发一个网页爬虫")
# 输出：[{"id": "TASK-xxx", "description": "...", "type": "development", ...}]
```

### 2. 智能分配 (Allocation)

根据 Bot 职责域自动分配：

| 任务类型 | 负责 Bot |
|---------|---------|
| development | suwen |
| content | shanmu |
| data | wangliang |
| trading | zhiji |
| monitoring | yi |
| resource | shoucangli |
| cost | paoding |

### 3. 分发送达 (Dispatch)

创建标准化任务委派单：

```python
dispatch_file = orchestrator.dispatch("suwen", subtasks, deadline="今日 18:00")
# 输出：~/.openclaw/agents/suwen/inbox/TASK-DISPATCH-xxx.md
```

### 4. 执行追踪 (Tracking)

每 30 分钟自动检查进度：

```python
from task-tracker import TaskTracker

tracker = TaskTracker()
progress = tracker.scan_all_bots()
```

### 5. 成果验收 (Validation)

验证交付成果质量：

```python
from validator import TaskValidator

validator = TaskValidator()
result = validator.validate("suwen", "TASK-xxx")
# 输出：{"status": "passed", "score": 0.9, ...}
```

### 6. 纠偏机制 (Correction)

检测并处理异常：

```python
from correction import CorrectionMechanism

correction = CorrectionMechanism()
anomalies = correction.detect_anomalies()
for a in anomalies:
    correction.handle_anomaly(a)
```

---

## 📊 监控指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 任务分解准确率 | ≥95% | - |
| 分配合理率 | ≥90% | - |
| 送达确认率 | 100% | - |
| 执行完成率 | ≥85% | - |
| 验收通过率 | ≥90% | - |
| 纠偏及时率 | ≥95% | - |

---

## 🛠️ 集成

### 与 Bot inbox/outbox 集成

- **分发**: `~/.openclaw/agents/{bot}/inbox/TASK-DISPATCH-*.md`
- **汇报**: `~/.openclaw/agents/{bot}/outbox/*.md`

### 与 HEARTBEAT 集成

定期生成汇总报告到 `HEARTBEAT.md`

### 与监控脚本集成

```bash
# 添加到 cron
*/30 * * * * python3 /home/nicola/.openclaw/workspace/skills/task-orchestrator/task-tracker.py scan
```

---

## 🔒 安全限制

### 自动执行
- ✅ 任务分解
- ✅ 分发送达
- ✅ 进度检查
- ✅ 报告生成

### 需确认
- ⚠️ 任务重新分配
- ⚠️ 截止时间调整
- ⚠️ 资源追加
- ⚠️ 任务降级/取消

---

## 📝 示例

### 完整工作流

```bash
# 1. 分解任务
python3 orchestrator.py decompose "开发 CAD 服务部署脚本"

# 2. 分发任务
python3 orchestrator.py dispatch suwen

# 3. 追踪进度
python3 task-tracker.py scan

# 4. 验收成果
python3 validator.py report suwen TASK-xxx

# 5. 生成汇总
python3 orchestrator.py summary
```

---

## 🎯 最佳实践

1. **任务描述清晰**: 包含目标、交付物、截止时间
2. **及时确认**: Bot 收到任务后 5 分钟内确认
3. **定期汇报**: 每 30 分钟更新进度
4. **阻塞早报**: 遇到阻塞立即上报
5. **验收标准明确**: 提前定义验收条件

---

## 📚 相关文档

- `SKILL.md` - Skills 详细定义
- `clawhub.yaml` - ClawHub 配置
- `constitution/directives/DELEGATION.md` - 委派协议

---

*Task Orchestrator v1.0.0 | 太一 AGI 智能任务编排引擎*
