# 辩证用户建模协议 (Dialectic User Model)

> 版本：v2.0 | 更新：2026-04-08  
> 灵感：Hermes Agent Honcho + 太一记忆系统  
> 状态：✅ 激活 | 优先级：P0-03

---

## 🎯 核心原则

**用户模型是动态演化的，不是静态文件**

传统用户模型 (如 SOUL.md/USER.md) 是静态的，无法捕捉用户的成长、变化、多面性。

辩证用户建模通过以下方式增强：
1. **多面性** - 用户在不同场景下展现不同侧面
2. **演化性** - 用户模型随时间持续更新
3. **辩证性** - 捕捉用户的矛盾、成长、转变
4. **自动学习** - 每次对话后自动更新

---

## 🏗️ 用户模型架构

### 三层模型

```
用户模型 (memory/user-model.json)
├── 核心层 (Core) - 稳定特质
│   ├── values: 核心价值观
│   ├── long_term_goals: 长期目标
│   └── basic_preferences: 基本偏好
│       ├── communication_style: 沟通风格
│       ├── decision_making: 决策方式
│       ├── learning_style: 学习风格
│       └── work_rhythm: 工作节奏
│
├── 情境层 (Contextual) - 场景相关
│   ├── work_mode: 工作模式
│   │   ├── focus_hours: 专注时间
│   │   ├── preferred_tools: 常用工具
│   │   ├── collaboration_style: 协作风格
│   │   └── current_projects: 当前项目
│   ├── learning_mode: 学习模式
│   │   ├── current_topics: 学习主题
│   │   ├── learning_pace: 学习节奏
│   │   ├── preferred_format: 偏好格式
│   │   └── recent_insights: 最近洞察
│   └── creation_mode: 创造模式
│       ├── output_types: 输出类型
│       ├── quality_standard: 质量标准
│       └── iteration_style: 迭代风格
│
└── 演化层 (Evolutionary) - 动态变化
    ├── recent_attention: 近期关注
    ├── skill_growth: 技能成长
    ├── cognitive_shifts: 认知转变
    ├── future_self: 未来自我投射
    └── change_log: 变更日志
```

---

## 🔄 更新机制

### 自动更新（每次对话后）

```python
def update_user_model(session_log, current_model):
    """从对话中自动更新用户模型"""
    
    # 1. 提取新信息
    new_info = extract_user_info(session_log)
    
    # 2. 检测认知转变
    shifts = detect_cognitive_shifts(session_log, current_model)
    
    # 3. 更新情境层
    current_model['contextual'] = merge_contextual(
        current_model['contextual'],
        new_info['contextual']
    )
    
    # 4. 更新演化层
    if shifts:
        current_model['evolutionary']['cognitive_shifts'].extend(shifts)
        current_model['change_log'].append({
            'date': datetime.now().isoformat(),
            'type': 'cognitive_shift',
            'description': summarize_shifts(shifts),
            'impact': assess_impact(shifts),
            'related_files': extract_related_files(session_log)
        })
    
    # 5. 更新近期关注
    current_model['evolutionary']['recent_attention'] = \
        extract_recent_attention(session_log)
    
    # 6. 更新时间戳
    current_model['updated_at'] = datetime.now().isoformat()
    
    return current_model
```

### 手动更新（SAYELF 明确说明）

```
# SAYELF: 「我最近开始关注 X」
→ 更新 evolutionary.recent_attention

# SAYELF: 「我的决策方式变了，现在更倾向于 Y」
→ 更新 core.basic_preferences.decision_making
→ 记录到 change_log

# SAYELF: 「未来 3 个月我想实现 Z」
→ 更新 evolutionary.future_self.3_months
```

---

## 🧠 认知转变检测

### 转变类型

| 类型 | 识别模式 | 示例 |
|------|----------|------|
| **价值观转变** | 「我觉得 X 更重要了」 | 从效率→艺术 |
| **学习风格** | 「我现在更喜欢 Y 方式」 | 理论→实践 |
| **决策方式** | 「我决定用 Z 方法」 | 直觉→数据驱动 |
| **工作节奏** | 「我发现这个时间更高效」 | 分散→深度工作 |
| **工具偏好** | 「X 工具比 Y 好用」 | 手动→自动化 |

### 检测算法

```python
def detect_cognitive_shifts(session_log, current_model):
    """检测认知转变"""
    shifts = []
    
    # 模式 1: 明确陈述
    patterns = [
        r'我觉得 (.*?) 更重要',
        r'我现在 (.*?) 以前',
        r'我发现 (.*?) 更有效',
        r'我决定 (.*?) 不再'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, session_log)
        for match in matches:
            shifts.append({
                'type': classify_shift(match),
                'evidence': match,
                'confidence': 0.8
            })
    
    # 模式 2: 行为变化
    behavior_changes = detect_behavior_changes(session_log, current_model)
    shifts.extend(behavior_changes)
    
    return shifts
```

---

## 📊 当前用户模型 (2026-04-08 更新)

```json
{
  "version": "2.0",
  "updated_at": "2026-04-08T23:30:00+08:00",
  
  "core": {
    "values": ["负熵", "效率", "艺术化存在", "第一性原理"],
    "long_term_goals": ["AGI 实现", "知识传承", "太一体系完善"],
    "basic_preferences": {
      "communication_style": "极简黑客风",
      "decision_making": "第一性原理",
      "learning_style": "费曼技巧",
      "work_rhythm": "深度工作优先"
    }
  },
  
  "contextual": {
    "work_mode": {
      "focus_hours": "09:00-12:00, 14:00-18:00, 22:00-23:00",
      "preferred_tools": ["CLI", "Python", "Git", "OpenClaw"],
      "collaboration_style": "异步优先",
      "current_projects": ["太一 AGI 系统", "地理感知路由", "可视化 Dashboard"]
    },
    "learning_mode": {
      "current_topics": ["AGI 架构", "链上交易", "可视化", "Hermes Agent"],
      "learning_pace": "密集型",
      "preferred_format": "实践驱动",
      "recent_insights": ["自进化学习循环", "辩证用户建模"]
    },
    "creation_mode": {
      "output_types": ["技能", "宪法", "Dashboard", "文档"],
      "quality_standard": "生产就绪",
      "iteration_style": "快速原型→完善"
    }
  },
  
  "evolutionary": {
    "recent_attention": [
      "Hermes Agent 集成",
      "Dashboard 部署",
      "地理感知路由 v2.0",
      "Crontab 定时任务",
      "自学习机制"
    ],
    "skill_growth": [
      "太一体系完善",
      "多 Bot 协作",
      "自进化学习循环",
      "语义搜索",
      "技能自动生成"
    ],
    "cognitive_shifts": [
      "从静态记忆→动态学习循环",
      "从手动技能创建→自动能力涌现",
      "从单一模型→多模型路由",
      "从功能优先→功能 + 艺术并重"
    ],
    "future_self": {
      "1_month": "完整的 Hermes 学习循环集成",
      "3_months": "自主技能创建和优化能力",
      "6_months": "多实例协同网络",
      "1_year": "AGI 自主进化框架"
    }
  },
  
  "change_log": [
    {
      "date": "2026-04-08",
      "type": "cognitive_shift",
      "description": "集成 Hermes Agent 学习循环理念，启动 P0 级自动化增强",
      "impact": "从被动记忆→主动技能创建，从静态用户模型→辩证动态建模",
      "related_files": [
        "skills/auto-skill-generator/SKILL.md",
        "skills/semantic-search/SKILL.md",
        "constitution/directives/DIALECTIC-USER-MODEL.md"
      ]
    }
  ]
}
```

---

## 🎯 使用示例

### 示例 1: 自动学习

```
# 对话后自动更新
session_log = """
SAYELF: 我最近开始关注 Hermes Agent 的自学习机制
SAYELF: 我觉得太一也应该有类似的自动技能生成能力
SAYELF: 艺术性很重要，但效率也不能牺牲
"""

→ 更新 recent_attention: ["Hermes Agent", "自学习机制"]
→ 检测 cognitive_shift: "效率 vs 艺术平衡"
→ 记录 change_log
```

### 示例 2: 查询用户模型

```
# 用户：SAYELF 最近关注什么？

太一查询 user-model.json:
→ 返回 evolutionary.recent_attention
→ 附加认知转变历史

结果：
📊 SAYELF 最近关注 (2026-04-08 更新)：
- Hermes Agent 集成
- Dashboard 部署
- 地理感知路由 v2.0
- 自学习机制

🧠 最近认知转变：
- 从静态记忆→动态学习循环
- 从手动技能创建→自动能力涌现
```

### 示例 3: 个性化响应

```python
# 根据用户模型调整响应风格
def tailor_response(response, user_model):
    """根据用户偏好调整响应"""
    
    if user_model['core']['basic_preferences']['communication_style'] == '极简黑客风':
        response = minimize_politeness(response)
        response = remove_redundancy(response)
    
    if user_model['contextual']['learning_mode']['preferred_format'] == '实践驱动':
        response = add_examples(response)
        response = add_code_snippets(response)
    
    return response
```

---

## 📋 与现有系统集成

### 记忆系统

```
memory/core.md → 提取核心记忆 → 更新 user-model.json
memory/YYYY-MM-DD.md → 提取原始日志 → 检测认知转变
MEMORY.md → 长期记忆 → 更新 core 层
```

### 技能系统

```
skills/auto-skill-generator → 学习技能创建偏好 → 更新 contextual.creation_mode
skills/semantic-search → 搜索历史 → 更新 recent_attention
```

### HEARTBEAT.md

```
心跳检查 → 读取 user-model.json → 个性化响应
任务完成 → 更新 recent_attention
```

---

## 🎯 成功标准

| 指标 | 目标值 | 时间 |
|------|--------|------|
| **更新及时性** | 每次对话后 | 1 周 |
| **认知转变检测准确率** | ≥80% | 2 周 |
| **SAYELF 满意度** | ≥4/5 | 2 周 |
| **个性化响应准确率** | ≥90% | 1 个月 |

---

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `memory/user-model.json` | 用户模型数据 |
| `SOUL.md` | Bot 人格定义 |
| `USER.md` | 用户基本信息 |
| `memory/core.md` | 核心记忆 |
| `constitution/directives/OBSERVER.md` | 观察者协议 |

---

*用户模型不是画像，是成长的记录。太一与 SAYELF 共同演化。*
