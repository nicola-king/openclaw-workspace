# Agent + Skills 架构设计

> 创建：2026-03-31 10:20  
> 核心：第一性原理重构  
> 状态：✅ 系统本质文档

---

## 🎯 核心定义

```
Agent = 决策引擎（看懂你）
Skills = 384 能力模块（改变你）
```

**最小抽象**:
```
用户问题 → State(64) → Stage(6) → Skill(384) → 行动指令
```

---

## 🧠 系统结构（最简版本）

```
Decision Agent (决策大脑)
    ↓
State (64 情境)
    ↓
Stage (6 阶段)
    ↓
Skill (具体策略)
```

---

## 🧩 组件重新定义

### 1️⃣ Agent（唯一一个）

**Decision Agent（决策代理）**

它做 3 件事：
1. 识别状态（64）
2. 判断阶段（6）
3. 调用对应 Skill

**不需要多个 Agent**，一个决策大脑足够。

---

### 2️⃣ Skills（核心资产）

**每一个 状态 × 阶段 = 1 个 Skill**

```
64 × 6 = 384 Skills
```

**Skill 的真正定义**:
> 一个"在当前状态 + 阶段下的最优动作单元"

**不是文案描述，是行动指令**。

---

## 🔥 Skill 标准结构

```json
{
  "id": "B02-03",
  "state": "路径错配期",
  "stage": 3,
  "type": "过渡型",
  
  "situation": "你在加倍努力但越来越焦虑",
  
  "core_problem": "路径错误 + 强化错误投入",
  
  "decision": "停止加码",
  
  "action": [
    "暂停当前投入 48 小时",
    "写下当前路径假设",
    "找 1 个外部反馈"
  ],
  
  "avoid": [
    "继续加倍努力",
    "情绪决策"
  ],
  
  "psychology": {
    "adler": "你的目标导向是证明自己，而非解决问题",
    "jung": "潜意识在重复'努力=正确'的原型",
    "freud": "防御机制：用忙碌逃避方向质疑"
  },
  
  "metadata": {
    "quality_score": 48,
    "status": "published",
    "price_tier": "premium"
  }
}
```

---

## 🧠 为什么这样设计（第一性原理）

**用户真正需要的**:
```
不是"你在哪"
而是
👉 "我现在该怎么办"
```

**所以**:
```
State(卦) = 命中（让用户觉得被说中）
Stage(爻) = 解释（让用户觉得更具体）
Skill    = 变现（让用户觉得有用）
```

---

## 💰 商业结构

### 免费层：State 识别
```
用户输入："我最近很努力但没结果"

输出：
"你处于【积累未显期】
64 种人生情景之一"

目标：让用户觉得"被说中"
```

### ¥1 层：Stage 解释
```
输出：
"你处于第 3 阶段：开始怀疑路径
这个阶段的特点是...
接下来会经历..."

目标：让用户觉得"更具体"
```

### ¥9.9 层：Skill 方案
```
输出：
"最优动作：停止加码

具体行动：
1. 暂停当前投入 48 小时
2. 写下当前路径假设
3. 找 1 个外部反馈

避免：
- 继续加倍努力
- 情绪决策"

目标：让用户觉得"有用"
```

### ¥19/月：会员
```
完整 384 Skills 访问
+ 用户轨迹追踪
+ 情景转换提醒
```

---

## 🧠 Agent 工作流程

### 输入
```
用户一句话：
"我最近很努力但没结果"
```

### Agent 判断
```python
State → 积累未显期 (A01)
Stage → 第 3 阶段 (开始怀疑路径)
```

### 调用 Skill
```python
Skill #A01-03
```

### 输出
```
📍 你当前的位置
情景：积累未显期
阶段：Step 3/6 (开始怀疑路径)

💡 最优动作：停止加码

🎯 具体行动：
1. 暂停当前投入 48 小时
2. 写下当前路径假设
3. 找 1 个外部反馈

⚠️ 避免：
- 继续加倍努力
- 情绪决策
```

---

## 🧠 心理学嵌入

| 心理学派 | Skill 定义 |
|---------|-----------|
| **阿德勒** | 目标导向行为修正 |
| **荣格** | 意识化潜意识模式 |
| **弗洛伊德** | 打破防御机制 |

**每个 Skill 都包含 3 个心理学视角的解读**。

---

## ⚠️ 最容易做错的点

| 错误 | 正确 |
|------|------|
| ❌ Skill = 文案描述 | ✅ Skill = 行动指令 |
| ❌ 告诉用户"是什么" | ✅ 告诉用户"怎么办" |
| ❌ 抽象建议 | ✅ 具体动作 |
| ❌ 多个 Agent | ✅ 一个决策 Agent |

---

## 🚀 384 Skills 生产计划

### Phase 1：MVP（16 Skills）
```
选择 16 个高频状态 × 第 3 阶段
（因为第 3 阶段是"开始怀疑"，用户最需要帮助）

16 Skills × 3 心理学视角 = 48 个行动指令
```

### Phase 2：完整（384 Skills）
```
64 状态 × 6 阶段 = 384 Skills

批量生产：
- AI 生成初稿
- 心理学专家审核
- 内测用户验证
- 质量评分≥45 发布
```

---

## 📊 技术实现

### Agent Prompt（核心）

```python
DECISION_AGENT_PROMPT = """
你是一个情景模式决策 Agent。

任务：
1. 分析用户输入，识别其当前状态（64 之一）
2. 判断其所处阶段（1-6）
3. 调用对应的 Skill（行动指令）

状态分类：
- 调整型（16 个）：需要内部调整
- 过渡型（16 个）：需要耐心等待
- 观察型（16 个）：需要判断决策
- 决策型（16 个）：需要行动突破

阶段定义：
- Step 1: 刚开始不对劲
- Step 2: 逐渐察觉问题
- Step 3: 开始怀疑路径
- Step 4: 尝试调整方式
- Step 5: 逐步适应
- Step 6: 进入新状态

输出格式：
{
  "state": "状态名称",
  "stage": 1-6,
  "skill_id": "状态 ID-阶段",
  "action": ["行动 1", "行动 2", ...],
  "avoid": ["避免 1", "避免 2", ...]
}
"""
```

### Skills 数据库

```sql
CREATE TABLE skills (
    id VARCHAR(10) PRIMARY KEY,  -- 'A01-03'
    state_id VARCHAR(10),
    state_name VARCHAR(50),
    stage INTEGER,
    type VARCHAR(20),
    
    situation TEXT,
    core_problem TEXT,
    decision TEXT,
    action JSONB,
    avoid JSONB,
    psychology JSONB,
    
    quality_score INTEGER,
    status VARCHAR(20),
    price_tier VARCHAR(20),  -- 'free'/'paid'/'premium'
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_skills_state_stage ON skills(state_id, stage);
CREATE INDEX idx_skills_type ON skills(type);
```

### API 结构

```python
# POST /api/v1/analyze
# 输入：用户问题
# 输出：State + Stage + Skill

{
  "state": {
    "id": "A01",
    "name": "积累未显期",
    "type": "调整型"
  },
  "stage": {
    "current": 3,
    "name": "开始怀疑路径",
    "progress": "3/6"
  },
  "skill": {
    "id": "A01-03",
    "decision": "停止加码",
    "action": [...],
    "avoid": [...],
    "psychology": {...}
  },
  "upsell": {
    "tier": "premium",
    "price": 9.9,
    "unlock": "完整行动方案"
  }
}
```

---

## 🎯 下一步行动

### 立即执行
1. ✅ 完成 Agent+Skills 架构设计
2. ⏳ 编写 Decision Agent Prompt
3. ⏳ 设计 384 Skills 数据结构

### 本周内
4. ⏳ 生产 MVP 16 Skills（高频状态×阶段 3）
5. ⏳ 实现匹配 API
6. ⏳ 开发小程序前端

### 变现测试
7. ⏳ 免费层：State 识别（引流）
8. ⏳ ¥1 层：Stage 解释（转化）
9. ⏳ ¥9.9 层：Skill 方案（营收）

---

*创建：2026-03-31 10:20 | 太一 AGI · 情景模式系统*
*状态：✅ 架构重构完成 | 版本：v2.0*
