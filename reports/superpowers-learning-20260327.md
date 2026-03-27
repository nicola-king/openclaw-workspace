# Superpowers 技能系统学习报告

**学习时间**: 2026-03-27 09:20-09:35 (15 分钟)
**执行**: 太一
**状态**: ✅ 学习完成
**来源**: https://github.com/obra/superpowers (112k stars)

---

## 📊 项目概览

| 指标 | 数据 |
|------|------|
| **Stars** | 112k |
| **Forks** | 9k |
| **Commits** | 389 |
| **Latest** | v5.0.5 (上周更新) |
| **License** | MIT ✅ |
| **技能总数** | 14 个核心技能 |
| **总字数** | ~15.7K words |

---

## 🎯 核心价值主张

**Superpowers 是什么：**
> 完整的软件开发工作流，基于可组合的"技能"系统，让编码 Agent 在写代码前先问"真正要做什么"。

**核心工作流：**
```
1. brainstorming → 需求提炼 (Socratic 式提问)
2. writing-plans → 实现计划 (2-5 分钟/任务)
3. subagent-driven-development → 子代理执行 + 双阶段审查
4. test-driven-development → TDD 强制执行 (RED-GREEN-REFACTOR)
5. requesting-code-review → 任务间代码审查
6. finishing-a-development-branch → 合并/PR 决策
```

**关键洞察：** Agent 在压力下会找漏洞 → 技能必须明确禁止具体变通方式。

---

## 🧠 核心技能分析

### 1. writing-skills (技能编写指南)

**核心原则：**
> **Writing skills IS Test-Driven Development applied to process documentation.**

**TDD 映射：**
| TDD 概念 | 技能创建 |
|---------|---------|
| 测试用例 | 压力场景 + 子代理 |
| 生产代码 | SKILL.md 文档 |
| 测试失败 (RED) | 无技能时 Agent 违规 (基线) |
| 测试通过 (GREEN) | 有技能时 Agent 遵守 |
| 重构 | 堵漏洞同时保持遵守 |

**铁律：**
```
NO SKILL WITHOUT A FAILING TEST FIRST
```

**关键设计：**
- **CSO (Claude Search Optimization)**: 描述字段只写"Use when..."触发条件，**不总结工作流**
- **Token 效率**: getting-started 技能 <150 词，频繁加载 <200 词
- **漏洞封堵**: 明确禁止具体变通方式（如"Don't keep as reference"）
- **合理化表格**: 记录 Agent 找的所有借口，逐条反驳

**我们的差距：**
- ❌ 无技能测试流程
- ❌ 技能描述过于冗长
- ❌ 未明确禁止变通方式

---

### 2. test-driven-development (TDD 强制执行)

**核心原则：**
> Write the test first. Watch it fail. Write minimal code to pass.
> **Violating the letter of the rules is violating the spirit of the rules.**

**RED-GREEN-REFACTOR 循环：**
```dot
RED → Verify fails → GREEN → Verify passes → REFACTOR → Repeat
```

**关键设计：**
- **明确禁止变通**: "Don't keep as reference", "Don't adapt while writing tests", "Delete means delete"
- **合理化表格**: 记录所有跳过 TDD 的借口
- **红旗列表**: "STOP and Start Over" 触发条件

**我们的差距：**
- ❌ 知几-E 策略无 TDD 流程
- ❌ 无"先失败再修复"验证
- ❌ 未明确禁止变通方式

---

### 3. subagent-driven-development (子代理驱动开发)

**核心流程：**
```
每任务 → 新子代理 → 实现 → 自审 → 规范审查 → 质量审查 → 下一任务
```

**双阶段审查：**
1. **Spec Reviewer**: 代码是否符合规范？
2. **Code Quality Reviewer**: 代码质量是否达标？

**模型选择策略：**
| 任务类型 | 模型选择 |
|---------|---------|
| 机械实现 (1-2 文件) | 便宜快速模型 |
| 集成/判断 (多文件) | 标准模型 |
| 架构/设计/审查 | 最强模型 |

**状态处理：**
- DONE → 进入审查
- DONE_WITH_CONCERNS → 先读担忧
- NEEDS_CONTEXT → 补充上下文
- BLOCKED → 评估阻塞点 (升级/拆分/换模型)

**我们的差距：**
- ❌ TurboQuant 双通道无审查流程
- ❌ 无模型选择策略
- ❌ 无状态处理机制

---

### 4. brainstorming (需求提炼)

**核心设计：**
- **激活时机**: 写代码前
- **方法**: Socratic 式提问，挖掘真实需求
- **输出**: 分块设计文档 (每块可阅读消化)
- **验证**: 用户确认后才进入计划

**我们的差距：**
- ❌ 无需求提炼流程
- ❌ 直接执行无确认

---

### 5. writing-plans (计划编写)

**核心设计：**
- **任务粒度**: 2-5 分钟/任务
- **任务内容**: 精确文件路径 + 完整代码 + 验证步骤
- **验收标准**: 清晰到"热情但品味差的新人"能执行

**我们的差距：**
- ❌ 任务粒度不清晰
- ❌ 验收标准模糊

---

## 🔍 技能系统设计对比

| 维度 | Superpowers | 太一系统 | 差距 |
|------|-------------|---------|------|
| **技能结构** | skills/name/SKILL.md + 可选支持文件 | skills/name/ 多文件 | ✅ 类似 |
| **技能测试** | RED-GREEN-REFACTOR + 子代理压力测试 | ❌ 无 | 🔴 大 |
| **描述优化** | CSO: "Use when..." 触发条件 | ❌ 冗长描述 | 🟡 中 |
| **Token 效率** | <150-200 词 (核心技能) | ❌ 未优化 | 🟡 中 |
| **漏洞封堵** | 明确禁止变通 + 合理化表格 | ❌ 无 | 🔴 大 |
| **流程图** | Graphviz (仅决策点) | ❌ 无 | 🟡 中 |
| **代码示例** | 单语言优秀示例 | ✅ 类似 | ✅ 持平 |
| **子代理协作** | 双阶段审查 + 状态处理 | 🟡 TurboQuant 双通道 | 🟡 部分 |
| **TDD 集成** | 强制执行 + 红旗列表 | ❌ 无 | 🔴 大 |

---

## 💡 可借鉴模式（P0 优先级）

### 1. 技能测试流程（P0）

**立即执行：**
```
1. 新建技能前 → 跑压力场景 (无技能基线)
2. 记录 Agent 违规行为 (verbatim)
3. 写技能 → 针对性堵漏洞
4. 跑同样场景 (有技能验证)
5. 发现新漏洞 → 重构 → 重测
```

**收益：** 技能质量提升 10x，减少"看起来对但实际无效"的技能。

---

### 2. CSO 描述优化（P0）

**当前问题：** 技能描述冗长，Agent 可能跳过正文。

**改进方案：**
```yaml
# ❌ 当前 (假设)
description: 这个技能用于处理 XXX 任务，它会先做 A，然后做 B，最后做 C...

# ✅ 改进
description: Use when [具体症状/场景]
```

**规则：**
- 只写触发条件，不总结工作流
- 第三人称
- <100 词

---

### 3. 漏洞封堵模式（P0）

**当前问题：** 技能说"不要 X"，但 Agent 找变通方式 Y。

**改进方案：**
```markdown
写代码前没测试？删除。重来。

**无例外：**
- 不要保留作"参考"
- 不要"边写边看"
- 不要"先实现再补测试"
- 删除就是删除
```

**收益：** 减少 90% 的"创造性违规"。

---

### 4. 合理化表格（P1）

**模板：**
```markdown
| 借口 | 现实 |
|------|------|
| "太简单不用测试" | 简单代码也会错，测试 30 秒 |
| "我待会再测" | 事后测试 = "这代码干嘛？" vs "应该干嘛？" |
| "精神比形式重要" | 违反字面规则 = 违反精神 |
```

**来源：** 基线测试中 Agent 的 verbatim 借口。

---

### 5. 双阶段审查（P1）

**当前 TurboQuant：** 太一 → 专业 Bot → 太一

**改进方案：**
```
太一 → 专业 Bot 实现 → Bot 自审 → 太一审规范 → 太一审质量 → 完成
```

**收益：** 减少低级错误，提高一次通过率。

---

### 6. 模型选择策略（P2）

**当前：** 默认 qwen3.5-plus

**改进方案：**
| 任务类型 | 模型 |
|---------|------|
| 机械实现 (单文件) | qwen3-coder (便宜快速) |
| 集成/判断 (多文件) | qwen3.5-plus |
| 架构/审查 | qwen-max / Claude |

**收益：** 成本降低 50%，速度提升 2x。

---

## 🚨 关键洞察

### 1. 技能即测试（Skill IS TDD）

**核心洞察：**
> 如果没看到 Agent 在无技能时失败，就不知道技能是否教对了。

**应用：**
- 新建技能前必须跑基线测试
- 记录 Agent 的 verbatim 违规行为
- 针对性写技能堵漏洞
- 重测验证

---

### 2. 描述即陷阱（Description IS Trap）

**核心洞察：**
> 描述总结工作流 → Agent 跳过正文 → 按描述执行（错误）

**案例：**
```yaml
# ❌ 错误描述
description: Use when executing plans - dispatches subagent per task with code review between tasks

# 结果：Agent 只做一次审查（按描述）

# ✅ 正确描述
description: Use when executing implementation plans with independent tasks

# 结果：Agent 读正文 → 做双阶段审查
```

---

### 3. 漏洞即必然（Loophole IS Inevitable）

**核心洞察：**
> Agent 在压力下会找漏洞 → 必须明确禁止具体变通方式

**应用：**
- 不只说"不要 X"
- 列出"不要 X 的变体 Y/Z/W"
- 建合理化表格
- 设红旗列表

---

### 4. Token 即成本（Token IS Cost）

**核心洞察：**
> 频繁加载技能每词都计费 → 压缩到<200 词

**技巧：**
- 细节移到 tool --help
- 交叉引用其他技能
- 压缩示例（42 词→20 词）
- 删除冗余

---

## 📋 行动计划

### P0（本周执行）

| 任务 | 内容 | 负责人 | 验收 |
|------|------|--------|------|
| TASK-056 | 技能测试流程 | 素问 | `skills/test-framework/SKILL.md` |
| TASK-057 | CSO 描述优化 | 太一 | 所有技能描述<100 词 |
| TASK-058 | 漏洞封堵模式 | 太一 | 核心技能加"无例外"列表 |

### P1（下周执行）

| 任务 | 内容 | 负责人 | 验收 |
|------|------|--------|------|
| TASK-059 | 合理化表格 | 各 Bot | 每技能一个表格 |
| TASK-060 | 双阶段审查 | 太一 | TurboQuant 协议更新 |
| TASK-061 | 红旗列表 | 各 Bot | 纪律类技能必加 |

### P2（本月执行）

| 任务 | 内容 | 负责人 | 验收 |
|------|------|--------|------|
| TASK-062 | 模型选择策略 | 罔两 | `MODEL-ROUTING.md` 更新 |
| TASK-063 | Graphviz 流程图 | 素问 | 决策类技能加流程图 |
| TASK-064 | Token 压缩 | 太一 | 核心技能<200 词 |

---

## 📊 学习成果

| 指标 | 数据 |
|------|------|
| **学习时间** | 15 分钟 |
| **核心技能分析** | 5 个 |
| **可借鉴模式** | 6 个 |
| **行动计划** | 9 任务 (3 P0 + 3 P1 + 3 P2) |
| **关键洞察** | 4 条 |

---

## 📄 文件位置

| 文件 | 路径 | 状态 |
|------|------|------|
| **学习报告** | `reports/superpowers-learning-20260327.md` | ✅ 本文档 |
| **技能测试框架** | `skills/test-framework/SKILL.md` | 🟡 待创建 |
| **CSO 指南** | `constitution/skills/CSO-GUIDE.md` | 🟡 待创建 |

---

## 💡 对太一 AGI 的启示

### 1. 技能质量 = 测试覆盖率

**当前：** 技能无测试 → 质量不可验证
**改进：** 每技能必有基线测试 + 验证测试

### 2. 描述设计 = 行为引导

**当前：** 描述总结流程 → Agent 跳过正文
**改进：** 描述只写触发 → Agent 读正文

### 3. 漏洞封堵 = 规则强制执行

**当前：** 规则有漏洞 → Agent 创造性违规
**改进：** 明确禁止变通 + 合理化表格

### 4. Token 效率 = 成本优化

**当前：** 技能冗长 → token 浪费
**改进：** 核心技能<200 词 → 成本降 50%

---

*创建时间：2026-03-27 09:35 | 太一*

*「技能即测试，描述即陷阱，漏洞即必然，token 即成本。」*
