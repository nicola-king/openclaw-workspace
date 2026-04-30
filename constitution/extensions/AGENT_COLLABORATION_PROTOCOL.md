# 🤖 太一多 Agent 协作协议

> **版本**: v1.0  
> **生效时间**: 2026-04-15 21:50  
> **参考**: TradingAgents 多智能体组团模式  
> **核心**: 一元总控 + 三元组团 + 一键决策

---

## 📜 协议总则

### 第一条：架构原则

太一系统采用**一元总控 + 三元组团**架构：

```
太一 (总控) → 工具 Bot 组团 (3 个智能体) → 一键决策 → 自动执行
```

### 第二条：组团标准

每个任务组团必须包含三个角色：

| 角色 | 职责 | 输出 |
|------|------|------|
| **分析 Bot** | 数据收集、分析洞察、方案建议 | 分析报告 |
| **执行 Bot** | 方案实施、文件处理、API 调用 | 执行结果 |
| **验证 Bot** | 结果验证、质量把控、合规审查 | 验证报告 |

### 第三条：一键决策

用户只需发出一次指令，系统自动完成：
```
任务接收 → 智能分发 → 多 Bot 协作 → 结果汇总 → 交付用户
```

---

## 🏗️ 组团规范

### 标准组团结构

```yaml
team_structure:
  coordinator:
    name: 太一
    role: 总控
    responsibilities:
      - 任务接收与理解
      - 智能体调度与分发
      - 结果汇总与整合
      - 最终决策与输出
  
  members:
    - role: 分析 Bot
      responsibilities:
        - 数据收集与整理
        - 信息分析与洞察
        - 方案建议与推荐
      
    - role: 执行 Bot
      responsibilities:
        - 方案实施与操作
        - 文件生成与处理
        - API 调用与交互
      
    - role: 验证 Bot
      responsibilities:
        - 结果验证与检查
        - 质量把控与测试
        - 反馈优化建议
```

### 工作流标准

```yaml
workflow:
  - step: 1
    agent: analyzer
    action: analyze
    output: analysis_report
    
  - step: 2
    agent: executor
    action: execute
    depends_on: 1
    output: execution_result
    
  - step: 3
    agent: validator
    action: validate
    depends_on: 2
    output: validation_report
    
  - step: 4
    agent: coordinator
    action: summarize
    depends_on: 3
    output: final_deliverable
```

---

## 📋 现有组团清单

### 1. 跨境贸易 Agent 组团

**任务类型**: `analysis`

**组团结构**:
```
太一 (总控)
  ↓
├─ 市场分析师 (Market Analyst)
├─ 客户开发师 (Business Developer)
└─ 报告生成师 (Report Generator)
```

**工作流**:
```
1. 市场调研 → 2. 客户验证 → 3. 报告生成 → 4. 汇总发送
```

**效率**: 12-36 倍提升

---

### 2. 图表生成 Agent 组团

**任务类型**: `creation`

**组团结构**:
```
太一 (总控)
  ↓
├─ 智能解析师 (Smart Parser)
├─ 图表生成师 (Chart Generator)
└─ 导出验证师 (Export Validator)
```

**工作流**:
```
1. 文字解析 → 2. 图表生成 → 3. 多格式导出 → 4. 质量验证
```

**效率**: 600 倍提升

---

### 3. 内容创作 Agent 组团

**任务类型**: `creation`

**组团结构**:
```
太一 (总控)
  ↓
├─ 灵感收集师 (Idea Collector)
├─ 内容创作师 (Content Creator)
└─ 发布运营师 (Publish Manager)
```

**工作流**:
```
1. 热点追踪 → 2. 内容创作 → 3. 多平台发布 → 4. 效果分析
```

---

### 4. 交易 Agent 组团

**任务类型**: `trading`

**组团结构**:
```
太一 (总控)
  ↓
├─ 市场分析师 (Market Analyst)
├─ 策略执行师 (Strategy Executor)
└─ 交易验证师 (Trade Validator)
```

**工作流**:
```
1. 行情分析 → 2. 信号生成 → 3. 执行交易 → 4. 成交验证
```

---

### 5. 语音 Agent 组团

**任务类型**: `execution`

**组团结构**:
```
太一 (总控)
  ↓
├─ 语音识别师 (Speech Recognizer)
├─ 命令执行师 (Command Executor)
└─ 反馈验证师 (Feedback Validator)
```

**工作流**:
```
1. 语音识别 → 2. 意图理解 → 3. 命令执行 → 4. 语音反馈
```

---

## 🔧 实施指南

### 创建新组团

**步骤 1: 定义任务类型**

在 `constitution/extensions/multi-agent-collaboration-framework.md` 中添加：

```yaml
task_types:
  new_task_type:
    description: 任务描述
    agents: [analyzer, executor, validator]
    workflow: [step1, step2, step3, step4]
```

**步骤 2: 配置 Agent**

在 `skills/` 目录下创建对应 Bot 的技能文件：

```
skills/07-system/new-task-agent/
├── SKILL.md
├── analyzer.py
├── executor.py
└── validator.py
```

**步骤 3: 注册组团**

在 `taiyi-multi-agent/multi_agent_team.py` 中注册：

```python
self.task_configs['new_task_type'] = {
    'description': '新任务类型',
    'agents': ['analyzer', 'executor', 'validator'],
    'workflow': ['analyze', 'execute', 'validate', 'summarize']
}
```

**步骤 4: 测试验证**

```python
from multi_agent_team import MultiAgentTeam

team = MultiAgentTeam(task_type='new_task_type')
result = team.execute("测试任务描述")
```

---

## 📊 质量门禁

### 验证标准

每个组团必须通过以下验证：

| 验证项 | 标准 | 检测方法 |
|--------|------|----------|
| **功能完整性** | 3 个角色齐全 | 代码审查 |
| **工作流正确** | 依赖关系正确 | 单元测试 |
| **错误处理** | 自动重试≥3 次 | 异常测试 |
| **质量保证** | 验证 Bot 必须通过 | 集成测试 |
| **文档完整** | README + 使用示例 | 文档审查 |

### 性能指标

| 指标 | 目标值 | 检测方法 |
|------|--------|----------|
| **响应时间** | <1 分钟 | 性能测试 |
| **成功率** | >95% | 监控统计 |
| **效率提升** | >10 倍 | 对比测试 |
| **用户满意度** | >90% | 用户反馈 |

---

##  错误处理

### 标准错误处理流程

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

### 错误代码规范

```python
ERROR_CODES = {
    'ANALYZER_001': '数据收集失败',
    'EXECUTOR_001': '文件操作失败',
    'VALIDATOR_001': '质量验证失败',
    'COORDINATOR_001': '任务分发失败'
}
```

---

## 📈 监控指标

### 实时监控

```yaml
metrics:
  - name: 任务完成率
    formula: 完成任务数 / 总任务数
    target: ">95%"
    
  - name: 平均响应时间
    formula: 总耗时 / 任务数
    target: "<1 分钟"
    
  - name: 错误率
    formula: 错误任务数 / 总任务数
    target: "<5%"
    
  - name: 用户满意度
    formula: 好评数 / 总评价数
    target: ">90%"
```

### 日报生成

每日 23:00 自动生成组团工作日报：

```markdown
# 多 Agent 协作日报

## 今日统计
- 总任务数：X
- 完成率：X%
- 平均响应时间：X 分钟

## 组团表现
- 跨境贸易组团：X 任务
- 图表生成组团：X 任务
- 内容创作组团：X 任务

## 异常情况
- 错误任务：X
- 主要原因：...

## 优化建议
- ...
```

---

## 🎯 演进路线

### 阶段 1: 标准化 (当前)

```
✅ 定义组团架构
✅ 明确角色职责
✅ 建立通信协议
✅ 实现错误处理
```

### 阶段 2: 模块化 (2026-04)

```
⏳ 创建通用 Agent 模板
⏳ 实现可复用组件
⏳ 建立技能库
⏳ 文档标准化
```

### 阶段 3: 自动化 (2026-05)

```
⏳ 一键组团功能
⏳ 自动任务分发
⏳ 智能调度优化
⏳ 自学习改进
```

### 阶段 4: 智能化 (2026-06)

```
⏳ 动态组团 (根据任务自动调整)
⏳ 自我优化 (从历史学习)
⏳ 预测性执行 (提前准备)
⏳ 人机协作增强
```

---

## 📝 附录

### A. 通信协议

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

### B. 任务状态机

```
pending → running → completed
    ↓         ↓
    └────→ failed
```

### C. 快速参考

**创建组团**:
```python
from multi_agent_team import MultiAgentTeam
team = MultiAgentTeam(task_type='analysis')
```

**执行任务**:
```python
result = team.execute("任务描述")
```

**查看状态**:
```python
status = team.get_status()
```

---

*太一 AGI · 多 Agent 协作协议 v1.0 · 2026-04-15 21:50*

**📜 本协议自生效时间起执行，所有新 Agent 必须遵循此协议组团工作！**
