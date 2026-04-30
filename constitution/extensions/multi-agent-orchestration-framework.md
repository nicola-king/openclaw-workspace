# 太一系统多 Agent 协作框架 (阶段 3)

> **版本**: v1.0  
> **创建时间**: 2026-04-15 22:21  
> **模式**: 一元总控 + 三元组团 + 一键决策

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────┐
│              太一 (总控 Agent)                    │
│   任务分发 · 结果汇总 · 最终决策 · 质量把控        │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│            工具 Bot 组团 (3 个智能体)              │
│  ┌──────────  ┌──────────┐  ┌──────────┐       │
│  │ 分析 Bot  │  │ 执行 Bot  │  │ 验证 Bot  │       │
│  └──────────┘  └──────────┘  └──────────       │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│              一键决策 · 自动执行                   │
└─────────────────────────────────────────────────┘
```

---

## 👥 组团清单

| 组团 ID | 名称 | 效率提升 | 状态 |
|--------|------|----------|------|
| cross-border-trade | 跨境贸易组团 | 12-36 倍 | ✅ 已配置 |
| chart-generator | 图表生成组团 | 600 倍 | ✅ 已配置 |
| content-creator | 内容创作组团 | 15-30 倍 | ✅ 已配置 |
| trading-decision | 交易决策组团 | 自动决策 | ✅ 已配置 |
| voice-processing | 语音处理组团 | 10-20 倍 | ✅ 已配置 |

---

## 📋 组团配置

### 跨境贸易组团 (cross-border-trade)

**协调器**: taiyi

**成员**:
- analyzer: cross-border-trade-agent (市场分析)
- executor: cross-border-trade-agent (客户开发)
- validator: quality-validator (报告验证)

**工作流**: analyze → execute → validate → summarize

**效率提升**: 12-36 倍

---

### 图表生成组团 (chart-generator)

**协调器**: taiyi

**成员**:
- parser: chart-generator (智能解析)
- generator: chart-generator (图表生成)
- exporter: chart-generator (多格式导出)

**工作流**: parse → generate → export → validate

**效率提升**: 600 倍

---

### 内容创作组团 (content-creator)

**协调器**: taiyi

**成员**:
- researcher: content-creator (灵感收集)
- creator: content-creator (内容创作)
- publisher: doc-publisher (发布运营)

**工作流**: research → create → publish → track

**效率提升**: 15-30 倍

---

### 交易决策组团 (trading-decision)

**协调器**: taiyi

**成员**:
- analyst: zhiji (市场分析)
- strategist: zhiji (策略生成)
- executor: binance-trading-agent (交易执行)

**工作流**: analyze → strategy → execute → verify

**效率提升**: 自动决策

---

### 语音处理组团 (voice-processing)

**协调器**: taiyi

**成员**:
- recognizer: taiyi-voice-agent (语音识别)
- executor: taiyi-voice-agent (命令执行)
- feedback: taiyi-voice-agent (语音反馈)

**工作流**: recognize → execute → feedback

**效率提升**: 10-20 倍

---


## 🔌 通信协议

### 消息格式

```json
{
  "message_id": "unique_id",
  "from": "agent_name",
  "to": "agent_name",
  "type": "task|result|error|query",
  "content": {
    "task_id": "task_uuid",
    "action": "action_name",
    "data": {},
    "status": "pending|running|completed|failed"
  },
  "timestamp": "ISO8601"
}
```

### 任务状态机

```
pending → running → completed
    ↓         ↓
    └────→ failed
```

---

## ⚠️ 错误处理

### 标准流程

```
错误发生
    ↓
记录错误日志
    ↓
自动重试 (最多 3 次)
    ↓
重试失败 → 降级方案
    ↓
通知太一总控
    ↓
用户反馈 (如必要)
```

### 错误代码

```python
ERROR_CODES = {
    'ANALYZER_001': '数据收集失败',
    'EXECUTOR_001': '文件操作失败',
    'VALIDATOR_001': '质量验证失败',
    'COORDINATOR_001': '任务分发失败'
}
```

---

## 📊 监控指标

| 指标 | 目标值 | 检测方法 |
|------|--------|----------|
| 任务完成率 | >95% | 监控统计 |
| 平均响应时间 | <1 分钟 | 性能测试 |
| 错误率 | <5% | 监控统计 |
| 用户满意度 | >90% | 用户反馈 |

---

## 🚀 使用方式

### Python API

```python
from multi_agent_orchestrator import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()

# 创建组团
orchestrator.create_all_teams()

# 执行任务
result = orchestrator.execute(
    team_id='cross-border-trade',
    task='分析重庆与锐动力的海外客户'
)
```

### 命令行

```bash
python3 multi_agent_orchestrator.py --team cross-border-trade --task "任务描述"
```

---

## 📁 文件结构

```
agent-teams/
├── cross-border-trade.json
├── chart-generator.json
├── content-creator.json
├── trading-decision.json
└── voice-processing.json
```

---

*太一 AGI · 多 Agent 协作框架 v1.0 · 2026-04-15 22:21*
