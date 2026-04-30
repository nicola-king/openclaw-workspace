---
name: cso-guide
description: Use when writing or editing skill descriptions, to optimize for agent discovery
---

# CSO 指南（Claude Search Optimization）

> **描述即陷阱：描述总结流程 → Agent 跳过正文 → 按描述执行（错误）**

---

## 🎯 核心原则

**描述的唯一目的：** 回答"我应该现在读这个技能吗？"

**不是：** 总结技能内容
**而是：** 描述触发条件

---

## ✅ 正确格式

```yaml
# ✅ GOOD: 只写触发条件
description: Use when [具体症状/场景/错误]

# ❌ BAD: 总结工作流程
description: Use when X - does A, then B, finally C
```

---

## 📊 对比案例

### 案例 1：TDD 技能

```yaml
# ❌ BAD: 总结流程
description: Use when implementing features - write test first, watch it fail, write minimal code, refactor

# 结果：Agent 读描述后认为"我知道了"→跳过正文→不按 TDD 执行

# ✅ GOOD: 只写触发
description: Use when implementing any feature or bugfix, before writing implementation code

# 结果：Agent 不知道具体怎么做→读正文→按 TDD 执行
```

### 案例 2：子代理开发

```yaml
# ❌ BAD: 总结流程
description: Use when executing plans - dispatches subagent per task with code review between tasks

# 结果：Agent 认为"review between tasks"=一次审查→跳过双阶段审查流程

# ✅ GOOD: 只写触发
description: Use when executing implementation plans with independent tasks in the current session

# 结果：Agent 读正文→发现双阶段审查→正确执行
```

### 案例 3：异步测试

```yaml
# ❌ BAD: 太抽象 + 技术特定
description: For async testing with setTimeout

# ✅ GOOD: 描述症状
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently
```

---

## 📝 描述检查清单

### 内容检查
- [ ] 以"Use when..."开头
- [ ] 只写触发条件，**不总结流程**
- [ ] 包含具体症状/场景/错误
- [ ] 第三人称（注入 system prompt）
- [ ] <100 词（越短越好）

### 关键词检查
- [ ] 包含错误消息（如"Hook timed out"）
- [ ] 包含症状（如"flaky", "hanging"）
- [ ] 包含同义词（如"timeout/hang/freeze"）
- [ ] 包含工具名（如实际命令、库名）

### 命名检查
- [ ] 用 active voice（动词开头）
- [ ] 用 gerunds（-ing 形式）
- [ ] 语义清晰（非 helper1/step2）

**示例：**
- ✅ `condition-based-waiting`
- ✅ `test-driven-development`
- ❌ `async-test-helpers`
- ❌ `skill-creation`

---

## 🚫 常见错误

### 错误 1：流程总结

```yaml
# ❌ BAD
description: Use when debugging - first reproduce, then isolate, then fix, then verify

# 问题：Agent 认为"我知道了"→跳过正文
```

### 错误 2：第一人称

```yaml
# ❌ BAD
description: I can help you with async tests when they're flaky

# 问题：注入 system prompt 时不协调
```

### 错误 3：技术特定但技能不特定

```yaml
# ❌ BAD
description: Use when tests use setTimeout/sleep and are flaky

# 问题：技能适用于所有 race conditions，不仅 setTimeout
```

### 错误 4：过于抽象

```yaml
# ❌ BAD
description: For better testing

# 问题：无触发条件，无法搜索
```

---

## 🔍 Token 效率技巧

### 技巧 1：引用 --help

```markdown
# ❌ BAD: 列举所有参数
search-conversations supports --text, --both, --after DATE, --before DATE, --limit N

# ✅ GOOD: 引用帮助
search-conversations supports multiple modes and filters. Run --help for details.
```

### 技巧 2：交叉引用

```markdown
# ❌ BAD: 重复流程
When searching, dispatch subagent with template...
[20 行重复指令]

# ✅ GOOD: 引用技能
Always use subagents. REQUIRED: Use [other-skill-name] for workflow.
```

### 技巧 3：压缩示例

```markdown
# ❌ BAD: 冗长示例 (42 词)
your human partner: "How did we handle authentication errors in React Router before?"
You: I'll search past conversations for React Router authentication patterns.
[Dispatch subagent with search query: "React Router authentication error handling 401"]

# ✅ GOOD: 最小示例 (20 词)
Partner: "How did we handle auth errors in React Router?"
You: Searching...
[Dispatch subagent → synthesis]
```

---

## 📈 验证方法

### 验证 1：描述测试

```
1. 只读描述，不看正文
2. 问：我知道怎么执行吗？
3. 如果"知道"→描述太详细→删减
4. 如果"不知道"→正确→保留
```

### 验证 2：搜索测试

```
1. 用问题关键词搜索技能
2. 问：这个描述匹配我的问题吗？
3. 如果不匹配→加关键词
```

### 验证 3：Token 计数

```bash
wc -w skills/{skill-name}/SKILL.md

# getting-started: <150 词
# frequently-loaded: <200 词
# other: <500 词
```

---

## 📊 CSO 优化前后对比

| 技能 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| TDD | 45 词，总结流程 | 12 词，只写触发 | -73% |
| 子代理开发 | 38 词，总结流程 | 14 词，只写触发 | -63% |
| 异步测试 | 22 词，技术特定 | 15 词，症状导向 | -32% |

---

## 💡 核心洞察

### 1. 描述是诱饵，不是说明书
> 描述的目的是让 Agent 读正文，不是替代正文

### 2. 知道感=跳过
> 描述总结流程 → Agent 认为"我知道了" → 跳过正文 → 执行错误

### 3. 未知感=阅读
> 描述只写触发 → Agent 不知道怎么做 → 读正文 → 执行正确

---

## 📄 相关文件

| 文件 | 用途 |
|------|------|
| `constitution/skills/TEST-FRAMEWORK.md` | 技能测试框架 |
| `skills/writing-skills/SKILL.md` | Superpowers 原版指南 |
| `reports/superpowers-learning-20260327.md` | 学习报告 |

---

*创建时间：2026-03-27 09:30 | 版本：v1.0 | 状态：✅ 生效中*

*「描述即诱饵，非说明书。触发清晰，流程隐之。」*
