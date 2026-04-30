---
name: hermes-learning-loop
version: 1.0.0
description: 自进化学习循环 - 自动技能创建/运行时优化/知识持久化
category: core
tags: ['learning', 'skill-creation', 'self-improvement', 'memory', 'evolution']
author: 太一 AGI (集成自 Hermes Agent)
created: 2026-04-08
status: active
priority: P0
---

# 🧠 Hermes Learning Loop - 自进化学习循环 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-08  
> **灵感**: [NousResearch Hermes Agent](https://github.com/NousResearch/hermes-agent)  
> **状态**: ✅ 激活 | **优先级**: P0  
> **核心原则**: 从经验创建技能·使用中自我改进·定期持久化知识

---

## 🎯 核心功能

### 1. 自动技能创建 ✅

**触发条件** (满足任一即触发):
- 同类任务重复出现 ≥ 3 次
- 任务复杂度超过阈值 (步骤 > 5 或 耗时 > 10 分钟)
- 用户明确请求"记住这个"或"创建技能"
- 发现新的职责域超出已有 Bot 能力

**创建流程**:
```
任务完成
    ↓
[1] 检查是否满足触发条件
    ├─ 是 → 继续
    └─ 否 → 记录到待观察列表
    ↓
[2] 提取任务模式
    ├─ 输入/输出分析
    ├─ 关键步骤提取
    ├─ 依赖识别
    └─ 边界条件定义
    ↓
[3] 生成 Skill 框架
    ├─ SKILL.md (职责/命令/示例)
    ├─ 核心实现 (.py/.sh)
    ├─ 配置模板
    └─ 测试用例
    ↓
[4] 太一审阅批准
    ├─ 批准 → 安装到 skills/
    ├─ 修改 → 返回步骤 3
    └─ 拒绝 → 记录原因
    ↓
[5] 热重载 + 写入记忆
    ├─ openclaw gateway reload
    ├─ 写入 memory/YYYY-MM-DD.md [能力涌现]
    └─ 更新 HEARTBEAT.md
```

**输出格式**:
```markdown
【能力涌现 · YYYY-MM-DD HH:mm】
新技能：{skill-name}
触发条件：{trigger_reason}
职责：{responsibilities}
批准人：太一 AGI
状态：✅ 已安装
```

---

### 2. 技能运行时优化 ✅

**优化时机**:
- 技能执行失败时
- 用户反馈不满意时
- 检测到更优实现模式时
- 依赖更新时

**优化策略**:
```yaml
失败自愈:
  - 记录错误上下文
  - 分析失败原因
  - 生成修复方案
  - 自动应用或请求批准

性能优化:
  - 监控执行时间
  - 识别瓶颈步骤
  - 提出优化建议
  - A/B 测试新版本

用户反馈学习:
  - 收集显式反馈 (好评/差评)
  - 分析隐式反馈 (重复修改/跳过)
  - 调整技能行为
  - 更新技能文档
```

**优化记录**:
```markdown
# 技能变更日志

## v1.1.0 (2026-04-08)
- 修复：处理边界情况 X
- 优化：执行速度提升 40%
- 新增：支持 Y 场景

## v1.0.0 (2026-04-08)
- 初始版本
```

---

### 3. 知识持久化 Nudge ✅

**Nudge 时机**:
- 会话结束前 (context > 80%)
- 每日 23:00 定时
- 检测到重要洞察时
- 用户请求"记住这个"时

**Nudge 流程**:
```
检测到需要持久化的内容
    ↓
[1] 分类内容类型
    ├─ [决策] - 重要决定
    ├─ [任务] - 待办事项
    ├─ [洞察] - 学习心得
    ├─ [能力涌现] - 新技能
    ├─ [宪法修订] - 规则变更
    └─ [元目·待发布] - 对外内容
    ↓
[2] 选择存储位置
    ├─ 短期 → memory/YYYY-MM-DD.md
    ├─ 中期 → memory/core.md / residual.md
    └─ 长期 → MEMORY.md
    ↓
[3] 生成压缩摘要
    ├─ 提取关键信息
    ├─ 去除冗余上下文
    └─ 格式化存储
    ↓
[4] 写入文件 + Git 提交
    ├─ git add
    ├─ git commit -m "[memory] ..."
    └─ git push (如有远程)
```

**Nudge 提示**:
```
🧠 检测到重要洞察，是否持久化？

内容：{summary}
建议存储：{target_file}
标签：[洞察]

[确认] [修改] [跳过]
```

---

### 4. 跨会话语义搜索 ✅

**搜索能力**:
- FTS5 全文索引 (SQLite)
- LLM 语义理解
- 跨文件关联检索
- 时间线追溯

**搜索接口**:
```python
from skills.hermes_learning_loop.memory_search import MemorySearch

searcher = MemorySearch()

# 关键词搜索
results = searcher.search("知几-E 策略", limit=10)

# 语义搜索
results = searcher.semantic_search("上次提到的套利方法")

# 时间范围搜索
results = searcher.search_by_date(
    query="预算支出",
    start="2026-04-01",
    end="2026-04-08"
)

# 带标签搜索
results = searcher.search_by_tag(
    tags=["[决策]", "[能力涌现]"],
    limit=5
)
```

**搜索结果格式**:
```markdown
📚 搜索结果："知几-E 策略" (找到 5 条)

1. [2026-04-06] 知几-E v40 部署
   标签：[决策] [能力涌现]
   摘要：部署知几-E v40，新增风险控制模块...
   位置：memory/2026-04-06.md:45

2. [2026-04-05] 知几-E 策略回测
   标签：[任务]
   摘要：完成 v39 策略回测，夏普比率 2.3...
   位置：memory/2026-04-05.md:23

...
```

---

## 🏗️ 架构设计

```
hermes-learning-loop/
├── SKILL.md (本文档)
├── loop/ (学习循环核心)
│   ├── skill_creator.py (技能创建)
│   ├── skill_optimizer.py (技能优化)
│   └── nudge_manager.py (知识持久化)
├── search/ (搜索模块)
│   ├── fts5_index.py (FTS5 索引)
│   ├── semantic_search.py (语义搜索)
│   └── memory_search.py (统一接口)
├── models/ (数据模型)
│   ├── skill.py (技能定义)
│   ├── memory_entry.py (记忆条目)
│   └── nudge.py (Nudge 定义)
└── tests/ (测试)
    └── test_learning_loop.py
```

---

## 🚀 使用方式

### 自动触发 (默认)

学习循环自动运行，无需手动干预：
- 任务完成后自动评估是否创建技能
- 技能执行失败时自动优化
- 会话结束时自动持久化

### 手动触发

```python
from skills.hermes_learning_loop.loop.skill_creator import SkillCreator
from skills.hermes_learning_loop.loop.nudge_manager import NudgeManager

# 手动创建技能
creator = SkillCreator()
creator.create_from_task(
    task_id="TASK-123",
    reason="同类任务第 3 次出现"
)

# 手动持久化
nudge = NudgeManager()
nudge.persist(
    content="重要洞察内容",
    type="[洞察]",
    target="memory/core.md"
)
```

### CLI 命令

```bash
# 查看待处理的学习机会
hermes-loop pending

# 手动触发技能创建
hermes-loop create-skill --task TASK-123

# 查看技能优化历史
hermes-loop skill-history --name skill-name

# 搜索记忆
hermes-loop search "关键词" --limit 10

# 查看 Nudge 历史
hermes-loop nudge-history --days 7
```

---

## 📊 与太一体系集成

### 宪法增强

**负熵法则修订**:
```markdown
原：废话=不输出
增：重复任务=创建技能
```

**能力涌现机制修订**:
```markdown
原：太一主动提议新建 Skill
增：学习循环自动检测 + 太一审阅批准
```

### 记忆架构增强

**TurboQuant 记忆 2.0**:
```yaml
原架构:
  - core.md (80% 核心)
  - residual.md (20% 细节)
  - MEMORY.md (长期固化)
  - YYYY-MM-DD.md (原始日志)

增强:
  + FTS5 索引 (自动构建)
  + 语义向量 (可选)
  + 跨文件关联
  + 时间线索引
```

### HEARTBEAT.md 增强

```markdown
## 🧠 学习循环状态

| 指标 | 数值 |
|------|------|
| 待创建技能 | 2 个 |
| 待优化技能 | 1 个 |
| 待持久化洞察 | 5 条 |
| 本周技能创建 | 3 个 |
| 本周技能优化 | 7 次 |
```

---

## 📋 验收标准

| 指标 | 基线 | 目标 | 当前 |
|------|------|------|------|
| **技能创建自动化** | 0% | >80% | 🟡 待实现 |
| **技能优化响应** | 手动 | <5 分钟 | 🟡 待实现 |
| **Nudge 准确率** | N/A | >90% | 🟡 待测试 |
| **搜索召回率** | N/A | >85% | 🟡 待测试 |

---

## 🔗 相关文档

- [Hermes Agent 原文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [能力涌现协议](../../constitution/directives/SELF-LOOP.md)
- [记忆架构](../../memory/README.md)
- [TurboQuant 压缩](../../constitution/directives/TURBOQUANT.md)

---

## 📝 变更日志

### v1.0.0 (2026-04-08)
- ✅ 初始版本
- ✅ 集成 Hermes Agent 学习循环理念
- ✅ 适配太一体系架构

---

*创建：2026-04-08 23:30 | 太一 AGI | 灵感：NousResearch Hermes Agent*
