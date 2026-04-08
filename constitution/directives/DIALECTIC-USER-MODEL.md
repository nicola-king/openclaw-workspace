# 辩证用户建模协议 (Dialectic User Model)

> 版本：v1.0 | 创建：2026-04-08  
> 灵感：[Hermes Agent Honcho](https://github.com/plastic-labs/honcho)  
> 状态：✅ 激活 | 优先级：P0

---

## 🎯 核心原则

**用户模型是动态演化的，不是静态文件**

传统用户模型 (如 SOUL.md/USER.md) 是静态的，无法捕捉用户的成长、变化和多面性。

辩证用户建模通过以下方式增强:
1. **多面性** - 用户在不同场景下展现不同侧面
2. **演化性** - 用户模型随时间持续更新
3. **辩证性** - 捕捉用户的矛盾、成长、转变

---

## 🏗️ 用户模型架构

### 三层模型

```
用户模型
├── 核心层 (Core) - 稳定特质
│   ├── 价值观
│   ├── 长期目标
│   └── 基本偏好
│
├── 情境层 (Contextual) - 场景相关
│   ├── 工作模式
│   ├── 学习模式
│   ├── 社交模式
│   └── 创造模式
│
└── 演化层 (Evolutionary) - 动态变化
    ├── 近期关注
    ├── 技能成长
    ├── 认知转变
    └── 未来自我
```

---

## 📋 数据收集

### 显式数据

| 来源 | 内容 | 更新频率 |
|------|------|---------|
| USER.md | 基本信息 | 按需 |
| SOUL.md | Bot 人格 | 按需 |
| 直接对话 | 偏好/目标 | 实时 |

### 隐式数据

| 来源 | 内容 | 提取方式 |
|------|------|---------|
| 任务历史 | 兴趣领域 | 模式分析 |
| 决策记录 | 价值取向 | 决策树分析 |
| 反馈记录 | 满意度 | 情感分析 |
| 时间分配 | 优先级 | 时间线分析 |

---

## 🔄 更新机制

### 实时更新

```python
# 每次对话后
def update_user_model(interaction):
    # 提取新信息
    new_traits = extract_traits(interaction)
    
    # 更新情境层
    if new_traits:
        user_model.contextual.update(new_traits)
    
    # 检测重大变化
    if detect_significant_change(new_traits):
        # 触发核心层审议
        trigger_core_review(new_traits)
```

### 定期审议

| 频率 | 审议内容 | 输出 |
|------|---------|------|
| 每日 | 近期关注变化 | daily_attention_update |
| 每周 | 兴趣领域演化 | weekly_interest_shift |
| 每月 | 目标进展评估 | monthly_goal_progress |
| 每季 | 核心价值观审议 | quarterly_core_review |

---

## 📊 用户模型文件格式

### memory/user-model.json

```json
{
  "version": "1.0",
  "updated_at": "2026-04-08T23:30:00+08:00",
  
  "core": {
    "values": ["负熵", "效率", "艺术化存在"],
    "long_term_goals": ["AGI 实现", "知识传承"],
    "basic_preferences": {
      "communication_style": "极简黑客风",
      "decision_making": "第一性原理",
      "learning_style": "费曼技巧"
    }
  },
  
  "contextual": {
    "work_mode": {
      "focus_hours": "09:00-12:00, 14:00-18:00",
      "preferred_tools": ["CLI", "Python", "Git"],
      "collaboration_style": "异步优先"
    },
    "learning_mode": {
      "current_topics": ["AGI 架构", "链上交易", "可视化"],
      "learning_pace": "密集型",
      "preferred_format": "实践驱动"
    }
  },
  
  "evolutionary": {
    "recent_attention": ["Hermes Agent 集成", "Dashboard 部署"],
    "skill_growth": ["太一体系完善", "多 Bot 协作"],
    "cognitive_shifts": ["从静态记忆→动态学习循环"],
    "future_self": {
      "3_months": "完整的 AGI 执行框架",
      "6_months": "多实例协同网络",
      "1_year": "自主进化能力"
    }
  },
  
  "change_log": [
    {
      "date": "2026-04-08",
      "type": "cognitive_shift",
      "description": "集成 Hermes 学习循环理念",
      "impact": "从被动记忆→主动技能创建"
    }
  ]
}
```

---

## 🔧 与太一体系集成

### 宪法增强

**负熵法则修订**:
```markdown
原：废话=不输出
增：废话=不输出 + 用户模型更新=必须
```

**ASK-PROTOCOL 增强**:
```markdown
新增追问维度:
- 用户目标变化
- 兴趣领域转移
- 认知模式演化
```

### 记忆架构增强

```yaml
原:
  - core.md (核心记忆)
  - residual.md (残差细节)
  - MEMORY.md (长期固化)
  - YYYY-MM-DD.md (原始日志)

增强:
  + user-model.json (辩证用户模型)
  + user-change-log.md (变化日志)
```

### HEARTBEAT.md 增强

```markdown
## 👤 用户模型状态

| 维度 | 状态 | 最后更新 |
|------|------|---------|
| 核心层 | ✅ 稳定 | 2026-04-08 |
| 情境层 | 🟡 工作中 | 实时 |
| 演化层 | 🟢 活跃 | 实时 |

### 近期关注
- Hermes Agent 集成
- Dashboard 部署
- 地理感知路由

### 待确认变化
- [ ] 学习循环优先级
- [ ] 技能创建自动化程度
```

---

## 📈 应用场景

### 场景 1: 个性化推荐

```python
# 基于用户模型推荐任务
def recommend_tasks():
    model = load_user_model()
    
    # 匹配当前关注
    if "Hermes Agent" in model.evolutionary.recent_attention:
        return [
            "集成 Hermes 学习循环",
            "研究 Honcho 用户建模",
            "对比 OpenClaw vs Hermes"
        ]
```

### 场景 2: 决策支持

```python
# 基于用户价值观辅助决策
def support_decision(options):
    model = load_user_model()
    
    # 按价值观排序选项
    ranked = rank_by_values(options, model.core.values)
    
    return {
        "recommendation": ranked[0],
        "rationale": f"符合{model.core.values[0]}原则"
    }
```

### 场景 3: 成长追踪

```python
# 追踪用户成长
def track_growth():
    model = load_user_model()
    
    return {
        "skills_gained": model.evolutionary.skill_growth,
        "cognitive_shifts": model.evolutionary.cognitive_shifts,
        "progress_to_future_self": calculate_progress(
            model.evolutionary.future_self
        )
    }
```

---

## ⚠️ 隐私保护

### 数据边界

- ✅ 用户明确分享的信息可记录
- ❌ 不推断敏感信息 (政治/宗教/健康等)
- ❌ 不跨会话泄露给第三方
- ✅ 用户可随时查看/修改/删除模型

### 透明度

每次重大更新时通知用户:
```
👤 检测到用户模型变化

变化类型：认知转变
内容：从"静态记忆"→"动态学习循环"
影响：技能创建自动化

[确认] [修改] [跳过]
```

---

## 📚 参考资料

- [Hermes Agent Honcho](https://github.com/plastic-labs/honcho)
- [辩证思维](https://zh.wikipedia.org/wiki/辩证法)
- [用户建模最佳实践](https://www.usermodeling.org/)

---

*创建：2026-04-08 23:30 | 太一 AGI | 灵感：Hermes Agent Honcho*
