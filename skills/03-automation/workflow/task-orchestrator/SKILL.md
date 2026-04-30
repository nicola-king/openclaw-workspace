---
name: task-orchestrator
version: 1.0.0
description: task-orchestrator skill
category: infrastructure
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Task Orchestrator - 智能任务编排 Skills

> **版本**: 1.0.0 | **负责 Bot**: 太一 (Taiyi) | **创建时间**: 2026-04-03 | **License**: MIT

---

## 🎯 职责定位

**Task Orchestrator** 是 **太一 AGI 专属的智能任务编排引擎**，由太一直接管理和使用。

**核心职责**: 负责任务从分解到验收的完整闭环，确保 **SAYELF 交给太一的所有任务** 都能落地执行并有成果汇报。

```
SAYELF → 太一 → Task Orchestrator → 分解→分配→分发→执行→验收→汇报
```

**归属**: 太一 (Taiyi) — 其他 Bot 仅作为任务执行者，不使用此 Skills

---

## 🔄 核心流程

### 阶段 1: 任务分解 (Decomposition)

**触发**: SAYELF 下达任务给太一

**输入**: 自然语言任务描述
**输出**: 结构化任务清单
**执行者**: 太一 (通过 Task Orchestrator)

**处理逻辑**:
1. 识别任务类型 (技术/内容/数据/交易)
2. 拆解为子任务 (依赖关系、优先级)
3. 估算工作量 (时间/成本)
4. 定义验收标准

**触发词**:
- "分解任务..."
- "规划..."
- "安排..."
- "智能自动化..."

---

### 阶段 2: 智能分配 (Allocation)

**输入**: 任务清单
**输出**: Bot 任务映射
**执行者**: 太一 (通过 Task Orchestrator)

**分配策略**:
| 任务类型 | 负责 Bot | 协作 Bot |
|---------|---------|---------|
| 技术开发 | 素问 | 太一 |
| 内容创作 | 山木 | 太一 |
| 数据采集 | 罔两 | 太一 |
| 量化交易 | 知几 | 羿 |
| 监控追踪 | 羿 | 知几 |
| 资源配置 | 守藏吏 | 太一 |
| 成本核算 | 庖丁 | 太一 |

**分配规则**:
- 单一职责：每个任务有且仅有一个主责 Bot
- 协作机制：跨域任务指定协作 Bot
- 负载均衡：避免单 Bot 过载

**权限**: 仅太一有权分配任务给其他 Bot

---

### 阶段 3: 分发送达 (Dispatch)

**输入**: Bot 任务映射
**输出**: 任务委派单
**执行者**: 太一 (通过 Task Orchestrator)

**交付物**:
- `agents/{bot}/inbox/TASK-DISPATCH-{timestamp}.md`
- 标准化委派单格式
- 明确截止时间和验收标准

**送达确认**:
- Bot 需在 5 分钟内确认接收
- 超时未确认 → 自动提醒
- 10 分钟未确认 → 太一介入

**权限**: 仅太一有权分发任务

---

### 阶段 4: 执行追踪 (Tracking)

**输入**: 任务执行状态
**输出**: 实时进度报告
**执行者**: 太一 (通过 Task Orchestrator 自动追踪)

**追踪机制**:
- **频率**: 每 30 分钟自动检查
- **方式**: 扫描 `agents/{bot}/outbox/` 汇报文件
- **状态**: 待开始/执行中/已完成/已阻塞

**智能自动化**: 无需人工干预，自动扫描 + 自动报告

---

### 阶段 5: 成果验收 (Validation)

**输入**: Bot 交付成果
**输出**: 验收报告
**执行者**: 太一 (通过 Task Orchestrator)

**验收标准**:
1. **完整性**: 所有交付物齐全
2. **质量**: 符合预定义标准
3. **时效**: 在截止时间前完成
4. **文档**: 报告/说明完整

**验收流程**:
```
Bot 提交 → 自动检查 → 太一审阅 → 通过/返工
```

**权限**: 仅太一有权验收并决定返工

---

### 阶段 6: 汇报归档 (Reporting)

**输入**: 验收通过成果
**输出**: 归档报告
**执行者**: 太一 (通过 Task Orchestrator 自动汇报)

**归档位置**:
- `reports/task-{id}-report.md`
- `memory/{bot}/task-{id}.md`
- `HEARTBEAT.md` 更新

**智能自动化**: 自动汇总 → 自动归档 → 自动向 SAYELF 汇报

**汇报内容**:
- 任务概述
- 执行过程
- 产出统计
- 经验总结

---

## 🚨 纠偏机制

### 触发条件

| 异常类型 | 触发条件 | 响应动作 |
|---------|---------|---------|
| 未确认 | 分发后 10 分钟未确认 | 太一介入 |
| 进度滞后 | 落后计划 30 分钟 | 自动提醒 |
| 进度滞后 | 落后计划 1 小时 | 太一协调资源 |
| 进度滞后 | 落后计划 2 小时 | 重新分配 |
| 阻塞 | Bot 上报阻塞 | 太一协调/降级 |
| 质量不达标 | 验收未通过 | 返工/协助 |
| 超时 | 超过截止时间 | 降级处理 + 总结 |

### 纠偏流程

```
检测异常 → 分级告警 → 介入处理 → 记录原因 → 优化策略
```

### 告警级别

| 级别 | 颜色 | 响应时间 | 处理人 |
|------|------|---------|-------|
| P0 | 🔴 | 立即 | 太一 |
| P1 | 🟡 | 15 分钟 | 太一 |
| P2 | 🔵 | 30 分钟 | 自动处理 |

---

## 📁 文件结构

```
skills/task-orchestrator/
├── SKILL.md                  # 本文件
├── orchestrator.py           # 核心编排引擎
├── task-tracker.py           # 执行追踪器
├── validator.py              # 成果验收器
├── reporter.py               # 汇报生成器
├── correction.py             # 纠偏机制
├── scripts/
│   ├── dispatch-task.sh      # 任务分发脚本
│   ├── check-progress.sh     # 进度检查脚本
│   └── generate-report.sh    # 报告生成脚本
├── templates/
│   ├── task-dispatch.md      # 任务委派单模板
│   ├── progress-report.md    # 进度报告模板
│   └── validation-report.md  # 验收报告模板
├── clawhub.yaml              # ClawHub 配置
└── README.md                 # 使用说明
```

---

## 🛠️ 使用方法

### CLI 调用 (太一专用)

```bash
# 任务分解
python3 orchestrator.py decompose "开发一个网页爬虫"

# 任务分发
python3 orchestrator.py dispatch --task TASK-XXX --bot suwen

# 进度检查
python3 task-tracker.py check --task TASK-XXX

# 成果验收
python3 validator.py validate --task TASK-XXX

# 生成报告
python3 reporter.py generate --task TASK-XXX --output reports/
```

### 自然语言触发 (SAYELF → 太一)

```
"分解这个任务：..."
"分配任务给素问：..."
"检查 TASK-XXX 进度"
"验收 TASK-XXX 成果"
"智能自动化执行..."
```

### 智能自动化模式

**Cron 定时任务**: 每 30 分钟自动执行
```bash
bash scripts/orchestrator-cron.sh
```

**自动执行**:
- ✅ 自动扫描各 Bot 进度
- ✅ 自动检测异常
- ✅ 自动发送提醒
- ✅ 自动生成报告
- ✅ 自动向 SAYELF 汇报

---

## 📊 监控指标

| 指标 | 目标 | 计算方式 |
|------|------|---------|
| 任务分解准确率 | ≥95% | 正确分解/总任务 |
| 分配合理率 | ≥90% | Bot 反馈合理/总分配 |
| 送达确认率 | 100% | 确认接收/总分发 |
| 执行完成率 | ≥85% | 按时完成/总任务 |
| 验收通过率 | ≥90% | 一次通过/总验收 |
| 纠偏及时率 | ≥95% | 及时处理/总异常 |

---

## 🔒 安全限制

### 自动执行 (太一可直接执行)
- ✅ 任务分解
- ✅ 分发送达
- ✅ 进度检查
- ✅ 报告生成
- ✅ 自动提醒
- ✅ 异常检测
- ✅ **Cron 保护检查** (每 30 分钟)
- ✅ **禁用任务告警** (立即)

### 需 SAYELF 确认 (太一需请示)
- ⚠️ 任务重新分配
- ⚠️ 截止时间调整
- ⚠️ 资源追加
- ⚠️ 任务降级/取消
- ⚠️ **Cron 任务永久禁用**

### 权限说明
- **Task Orchestrator 仅太一可使用**
- 其他 Bot 仅作为任务执行者，无权调用此 Skills
- **Cron 修改必须经过太一审批**
- **所有变更自动审计记录**

---

## 📝 汇报格式

### 进度汇报 (每 30 分钟)

```markdown
【任务编排汇报 · {timestamp}】

📊 任务总览
- 进行中：X 个
- 已完成：X 个
- 已阻塞：X 个
- 滞后：X 个

⚠️ 异常情况
- {异常描述}

🎯 下一步
- {行动计划}
```

### 完成汇报 (任务结束)

```markdown
【任务完成汇报 · TASK-XXX】

✅ 任务概述
- 描述：...
- 负责 Bot: ...
- 耗时：X 小时

📦 产出统计
- 文件：X 个 / ~XKB
- 代码：X 行
- 文档：X 页

📈 质量评估
- 完整性：⭐⭐⭐⭐⭐
- 时效性：⭐⭐⭐⭐⭐
- 文档化：⭐⭐⭐⭐⭐

📁 归档位置
- `reports/task-XXX-report.md`
```

---

## 🎯 验收标准

### 功能验收
- [ ] 任务分解准确率 ≥95%
- [ ] 分发送达率 100%
- [ ] 进度追踪延迟 <5 分钟
- [ ] 纠偏响应时间 <10 分钟

### 文档验收
- [ ] SKILL.md 完整
- [ ] README.md 清晰
- [ ] 模板齐全
- [ ] 示例充分

### 集成验收
- [ ] 与太一自然语言集成
- [ ] 与 Bot inbox/outbox 集成
- [ ] 与 HEARTBEAT 集成
- [ ] 与监控脚本集成

---

## 📚 相关文档

- `constitution/directives/DELEGATION.md` - 委派协议
- `constitution/workflows/README.md` - 工作流框架
- `HEARTBEAT.md` - 核心待办
- `scripts/bot-task-monitor.sh` - Bot 任务监控

---

## 👑 归属声明

**Task Orchestrator 是太一 (Taiyi) 的专属工具**

- **所有者**: 太一 (Taiyi)
- **使用者**: 仅太一
- **汇报对象**: SAYELF
- **调度范围**: 所有 8 Bot (太一/知几/山木/素问/罔两/庖丁/羿/守藏吏)

**其他 Bot 角色**: 任务执行者，无权使用 Task Orchestrator

---

*Task Orchestrator v1.0.0 | 太一 AGI 智能任务编排引擎 | 归属：太一 (Taiyi)*
