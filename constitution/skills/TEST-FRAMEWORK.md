---
name: test-framework
description: Use when creating new skills or editing existing skills, before deployment
---

# 技能测试框架（TDD for Skills）

> **Writing skills IS Test-Driven Development applied to process documentation.**
> 
> 核心原则：如果没看到 Agent 在无技能时失败，就不知道技能是否教对了。

---

## 📋 铁律

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

**无例外：**
- 不因为"简单"而跳过
- 不因为"参考文档"而跳过
- 不因为"时间紧"而跳过
- 不因为"我有信心"而跳过

**违反 = 删除技能，重来。**

---

## 🔄 RED-GREEN-REFACTOR 循环

```dot
digraph skill_tdd {
    rankdir=LR;
    
    red [label="RED\n跑压力场景 (无技能)", shape=box, style=filled, fillcolor="#ffcccc"];
    verify_red [label="记录违规行为", shape=diamond];
    green [label="GREEN\n写技能堵漏洞", shape=box, style=filled, fillcolor="#ccffcc"];
    verify_green [label="跑同样场景 (有技能)", shape=diamond];
    refactor [label="REFACTOR\n加合理化表格", shape=box, style=filled, fillcolor="#ccccff"];
    done [label="部署", shape=ellipse];

    red -> verify_red;
    verify_red -> green [label="记录 verbatim"];
    green -> verify_green;
    verify_green -> refactor [label="遵守"];
    verify_green -> green [label="违规→加 counter"];
    refactor -> done [label="无新漏洞"];
}
```

---

## 🔴 RED 阶段：跑基线测试

### Step 1: 设计压力场景

**压力类型（至少组合 3 种）：**

| 压力 | 示例 |
|------|------|
| **时间压力** | "这个很急，5 分钟内搞定" |
| **沉没成本** | "我已经写了一半代码，你帮我补测试" |
| **权威压力** | "我老板说这个功能不用测试" |
| **复杂度压力** | "这个逻辑太复杂了，测试写不出来" |
| **疲劳压力** | "我们已经改了 10 次了，差不多行了" |

### Step 2: 无技能运行

```bash
# 清空相关技能
mv ~/.openclaw/workspace/skills/{skill-name} ~/.openclaw/workspace/skills/{skill-name}.bak

# 跑压力场景
[用子代理或手动模拟场景]
```

### Step 3: 记录违规行为

**必须 verbatim 记录：**
- Agent 的原话
- 使用的合理化借口
- 跳过的步骤
- 变通方式

**记录模板：**
```markdown
### 基线行为（无技能）

**压力场景**: [描述]

**Agent 行为**:
1. [具体行为 1]
2. [具体行为 2]

**合理化借口 (verbatim)**:
- "[原话 1]"
- "[原话 2]"

**违规类型**:
- [ ] 跳过关键步骤
- [ ] 创造性违规
- [ ] 精神>形式论
- [ ] 例外论
```

---

## 🟢 GREEN 阶段：写技能堵漏洞

### Step 1: 针对性写技能

**基于基线测试发现：**
- 每个违规行为 → 对应禁止条款
- 每个合理化借口 → 对应反驳
- 每个变通方式 → 明确禁止

### Step 2: 必须包含的模块

```markdown
## 铁律
[核心规则，不可违反]

## 无例外
[明确禁止的变通方式，至少 5 条]

## 合理化表格
| 借口 | 现实 |
|------|------|
| [verbatim 借口 1] | [反驳 1] |
| [verbatim 借口 2] | [反驳 2] |

## 红旗列表
**STOP and Start Over 当：**
- [红旗 1]
- [红旗 2]
- [红旗 3]
```

### Step 3: CSO 优化

```yaml
# ✅ 正确格式
name: skill-name-with-hyphens
description: Use when [具体症状/场景]
```

**规则：**
- 只写触发条件，**不总结工作流**
- 第三人称
- <100 词
- 包含关键词（错误消息、症状、工具名）

---

## 🟡 REFACTOR 阶段：验证 + 堵漏

### Step 1: 有技能运行

```bash
# 恢复技能
mv ~/.openclaw/workspace/skills/{skill-name}.bak ~/.openclaw/workspace/skills/{skill-name}

# 跑同样场景
[用同样压力场景测试]
```

### Step 2: 验证遵守

**检查清单：**
- [ ] Agent 遵守核心规则
- [ ] Agent 未使用变通方式
- [ ] Agent 未找新借口

### Step 3: 发现新漏洞

**如果 Agent 找到新漏洞：**
1. 记录新合理化借口
2. 在技能中加明确 counter
3. 重测直到无新漏洞

**迭代次数：** 通常 3-5 轮

---

## 📊 合理化表格模板

```markdown
| 借口 | 现实 |
|------|------|
| "太简单不用测试" | 简单代码也会错，测试 30 秒 |
| "我待会再测" | 事后测试 = "这代码干嘛？" vs "应该干嘛？" |
| "精神比形式重要" | 违反字面规则 = 违反精神 |
| "这次不一样" | 每次都觉得不一样，所以每次都错 |
| "我已经手动测过了" | 手动测试不可重复，不是测试 |
| "客户急着要" | 客户更急着要正确的东西 |
| "测试写不出来" | 测试写不出来说明需求不清楚 |
```

**来源：** 基线测试中 Agent 的 verbatim 借口。

---

## 🚩 红旗列表模板

```markdown
## 红旗列表 - STOP and Start Over

**出现以下任何一条，立即删除代码，重来：**

- [ ] 代码写在前，测试在后
- [ ] "我手动测过了"
- [ ] "测试只是形式"
- [ ] "这次情况特殊"
- [ ] "我先实现再补测试"
- [ ] "这个功能不重要"
- [ ] "时间来不及了"

**所有这些都意味着：你在 rationalize，不是在执行。**
```

---

## ✅ 部署清单

### RED 阶段
- [ ] 设计 3+ 压力场景
- [ ] 跑无技能基线测试
- [ ] 记录 verbatim 违规行为
- [ ] 记录合理化借口

### GREEN 阶段
- [ ] 技能名用 hyphens（无括号/特殊字符）
- [ ] YAML frontmatter (name + description <1024 字符)
- [ ] 描述以"Use when..."开头
- [ ] 描述只写触发条件，不总结流程
- [ ] 核心规则（铁律）
- [ ] 无例外列表（至少 5 条）
- [ ] 合理化表格（基于基线测试）
- [ ] 红旗列表
- [ ] 一个优秀示例（单语言）

### REFACTOR 阶段
- [ ] 跑有技能验证测试
- [ ] 确认 Agent 遵守
- [ ] 发现新漏洞→加 counter
- [ ] 重测直到无新漏洞（通常 3-5 轮）
- [ ] Token 压缩（核心技能<200 词）

### 部署
- [ ] git commit + push
- [ ] 考虑 PR 贡献（如通用技能）

---

## 📈 质量指标

| 指标 | 目标 | 测量方式 |
|------|------|---------|
| **基线违规数** | ≥3 | RED 阶段记录 |
| **迭代次数** | 3-5 轮 | REFACTOR 阶段计数 |
| **最终遵守率** | 100% | 最后一轮验证 |
| **新漏洞发现** | 0 | 连续 2 轮无新漏洞 |
| **Token 数** | <200 | wc -w SKILL.md |

---

## 💡 核心洞察

### 1. 技能即测试
> 如果没看到失败，就不知道是否教对了。

### 2. 描述即陷阱
> 描述总结流程 → Agent 跳过正文 → 按描述执行（错误）

### 3. 漏洞即必然
> Agent 在压力下必找漏洞 → 必须明确禁止具体变通

### 4. Token 即成本
> 频繁加载技能每词都计费 → 压缩到<200 词

---

## 📄 相关文件

| 文件 | 用途 |
|------|------|
| `skills/writing-skills/SKILL.md` | Superpowers 原版指南 |
| `reports/superpowers-learning-20260327.md` | 学习报告 |
| `constitution/skills/CSO-GUIDE.md` | CSO 优化指南（待创建） |

---

*创建时间：2026-03-27 09:25 | 版本：v1.0 | 状态：✅ 生效中*

*「无测试，不技能。漏洞必现，堵之以明文。」*
