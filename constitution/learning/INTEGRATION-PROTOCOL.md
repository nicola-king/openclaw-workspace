# 太一体系 · 学习整合自动化协议

> 创建时间：2026-03-29 21:18
> 原则：学习面向太一体系，智能评估 → 自动分配到宪法/Agent/Skill 三层
> 版本：v1.0

---

## 🎯 核心原则

### 学习整合三层架构

```
学习输入 → 太一智能评估 → 自动分配到最适合层面

┌─────────────────────────────────────────────────────────┐
│                    太一体系                              │
├─────────────────────────────────────────────────────────┤
│  第一层：宪法层 (Constitution)                           │
│  - 价值基石 / 核心原则 / 协作规程                        │
│  - 适用：系统性/跨 Agent/长期指导原则                    │
│                                                         │
│  第二层：Agent 层 (Agent Framework)                      │
│  - Agent 架构 / 协作模式 / 执行框架                       │
│  - 适用：特定 Agent 能力/多 Agent 协作/执行方法            │
│                                                         │
│  第三层：Skill 层 (Skill Module)                         │
│  - 具体技能 / 工具函数 / 数据模块                        │
│  - 适用：单一功能/可复用模块/技术实现                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 太一智能评估算法

### 评估维度

| 维度 | 选项 | 权重 |
|------|------|------|
| **scope (范围)** | system / agent / single | 40% |
| **impact (影响)** | long_term / mid_term / short_term | 30% |
| **reusability (复用)** | cross_agent / single_agent / single_function | 30% |

### 决策规则

```python
def evaluate_learning(learning_content):
    """太一智能评估学习来源应融入哪个层面"""
    
    # 评估维度
    scope = detect_scope(learning_content)      # system/agent/single
    impact = detect_impact(learning_content)    # long/mid/short
    reusability = detect_reusability(learning_content)  # cross/single/function
    
    # 决策树
    if scope == 'system' and impact == 'long_term':
        return 'CONSTITUTION'
    elif reusability == 'cross_agent' or scope == 'agent':
        return 'AGENT_FRAMEWORK'
    else:
        return 'SKILL_MODULE'
```

### 评估示例

| 学习来源 | scope | impact | reusability | 决策 |
|---------|-------|--------|-------------|------|
| 麦肯锡工作方法 | system | long_term | cross_agent | **宪法层** |
| TradingAgents | agent | mid_term | cross_agent | **Agent 层** |
| Claude Bot 套利 | agent | mid_term | single_agent | **Agent 层 (知几)** |
| Polymarket 数据 | single | short_term | single_function | **Skill 层** |

---

## 📚 学习整合流程

### Step 1: 学习输入

```
外部学习材料 (截图/文章/文档/代码)
  ↓
太一接收
```

### Step 2: 智能评估

```
太一分析:
- 内容范围：系统/Agent/单一功能？
- 影响时长：长期/中期/短期？
- 复用性：跨 Agent/单 Agent/单功能？
  ↓
自动决策：宪法层 / Agent 层 / Skill 层
```

### Step 3: 自动分配

```
宪法层 → constitution/
  ├── axiom/ (价值基石)
  ├── directives/ (指导原则)
  ├── skills/ (技能协议)
  └── collaboration/ (协作规程)

Agent 层 → constitution/extensions/ 或 skills/{agent-name}/
  ├── 太一架构
  ├── 知几交易框架
  ├── 山木内容框架
  └── ...

Skill 层 → skills/{category}/
  ├── trading/ (交易技能)
  ├── data/ (数据技能)
  ├── content/ (内容技能)
  └── ...
```

### Step 4: 文档归档

```
守藏吏自动归档:
1. 创建学习文档
2. 标注来源/日期/核心洞察
3. 关联到对应层面文档
4. 更新学习索引
```

### Step 5: 执行追踪

```
罔两自动追踪:
1. 记录学习整合时间
2. 追踪执行进度
3. 收集反馈数据
4. 优化评估算法
```

---

## 📁 文档结构

### 宪法层文档

```
constitution/
├── axiom/
│   └── VALUE-FOUNDATION.md (价值基石)
├── directives/
│   ├── NEGENTROPY.md (负熵法则)
│   ├── OBSERVER.md (观察者协议)
│   ├── SELF-LOOP.md (自驱动闭环)
│   ├── ASK-PROTOCOL.md (追问协议)
│   ├── TURBOQUANT.md (智能分离)
│   └── AI-GUIDANCE.md (AI 引导框架) 🆕
├── skills/
│   └── MODEL-ROUTING.md (模型调度)
├── collaboration/
│   ├── COLLABORATION.md (多 Bot 协作)
│   └── DELEGATION.md (任务委派)
└── learning/
    ├── AGENT-MATCHING.md (Agent 匹配) 🆕
    └── INTEGRATION-PROTOCOL.md (本文档) 🆕
```

### Agent 层文档

```
constitution/extensions/
├── TAIYI-FRAMEWORK.md (太一架构)
├── ZHIJI-FRAMEWORK.md (知几交易框架)
├── SHANMU-FRAMEWORK.md (山木内容框架)
├── SUWEN-FRAMEWORK.md (素问技术框架)
├── WANGLIANG-FRAMEWORK.md (罔两数据框架)
├── PAODING-FRAMEWORK.md (庖丁预算框架)
├── YI-FRAMEWORK.md (羿信号框架)
└── SHOUZANGLI-FRAMEWORK.md (守藏吏管家框架)
```

### Skill 层文档

```
skills/
├── trading/
│   ├── arbitrage-mindset.md (套利思维)
│   ├── polymarket-tracker.py (大户追踪)
│   └── math-decision.py (数学化决策)
├── data/
│   ├── transparency.py (数据透明化)
│   └── user-behavior.py (用户行为分析)
├── content/
│   ├── viral-headlines.py (爆点句创作)
│   └── agent-showcase.py (技能展示)
├── today-stage/ (今日情景 Agent)
│   ├── 384 Skills
│   └── 文档体系
└── ...
```

---

## 📊 学习整合案例

### 案例 1: 麦肯锡工作方法

**学习输入**: AI 需要系统框架引导
**太一评估**:
- scope: system (影响所有 Agent)
- impact: long_term (长期指导原则)
- reusability: cross_agent (所有 Agent 都适用)

**决策**: **宪法层**
**融入文档**: `constitution/directives/AI-GUIDANCE.md`
**执行**: 所有 Agent 提示词框架优化

---

### 案例 2: TradingAgents

**学习输入**: 多 Agent 协作 + 内部辩论
**太一评估**:
- scope: agent (Agent 架构层)
- impact: mid_term (中期影响)
- reusability: cross_agent (多 Agent 参考)

**决策**: **Agent 层**
**融入文档**: `constitution/COLLABORATION.md`
**执行**: 太一 5 Agent 协作框架

---

### 案例 3: Claude Bot 套利

**学习输入**: 套利思维 + 数学化决策
**太一评估**:
- scope: agent (知几交易 Agent)
- impact: mid_term (中期策略)
- reusability: single_agent (主要适用于知几)

**决策**: **Agent 层 (知几)**
**融入文档**: `constitution/extensions/ZHIJI-FRAMEWORK.md`
**执行**: Polymarket 套利策略优化

---

### 案例 4: Polymarket 数据透明化

**学习输入**: 上帝视角财务审计
**太一评估**:
- scope: single (具体功能)
- impact: short_term (短期实现)
- reusability: single_function (单一技能)

**决策**: **Skill 层**
**融入文档**: `skills/data/polymarket-tracker.py`
**执行**: 大户追踪脚本

---

## 🚀 自动化实现

### 太一评估脚本

```python
#!/usr/bin/env python3
# constitution/learning/evaluator.py

class LearningEvaluator:
    """太一学习整合评估器"""
    
    def __init__(self):
        self.layers = {
            'CONSTITUTION': 'constitution/',
            'AGENT_FRAMEWORK': 'constitution/extensions/',
            'SKILL_MODULE': 'skills/'
        }
    
    def evaluate(self, learning_content: dict) -> dict:
        """评估学习来源应融入哪个层面"""
        
        # 提取特征
        features = self.extract_features(learning_content)
        
        # 智能决策
        layer = self.decide_layer(features)
        
        # 生成执行计划
        plan = self.generate_plan(layer, learning_content)
        
        return {
            'layer': layer,
            'target_path': self.layers[layer],
            'plan': plan
        }
    
    def extract_features(self, content: dict) -> dict:
        """提取评估特征"""
        return {
            'scope': self.detect_scope(content),
            'impact': self.detect_impact(content),
            'reusability': self.detect_reusability(content)
        }
    
    def decide_layer(self, features: dict) -> str:
        """决策树"""
        if features['scope'] == 'system' and features['impact'] == 'long_term':
            return 'CONSTITUTION'
        elif features['reusability'] == 'cross_agent':
            return 'AGENT_FRAMEWORK'
        else:
            return 'SKILL_MODULE'
```

### 守藏吏归档脚本

```bash
#!/bin/bash
# constitution/learning/archive.sh

# 自动归档学习文档
LEARNING_NAME=$1
LAYER=$2
CONTENT=$3

case $LAYER in
  "CONSTITUTION")
    TARGET="constitution/learning/"
    ;;
  "AGENT_FRAMEWORK")
    TARGET="constitution/extensions/"
    ;;
  "SKILL_MODULE")
    TARGET="skills/"
    ;;
esac

# 创建文档
cat > "${TARGET}${LEARNING_NAME}.md" << EOF
# ${LEARNING_NAME}

来源：${CONTENT[source]}
日期：$(date +%Y-%m-%d)
核心洞察：${CONTENT[insight]}
...
EOF

echo "学习文档已归档到 ${TARGET}"
```

---

## 📈 学习整合指标

| 指标 | 目标值 | 当前值 |
|------|--------|--------|
| **学习输入** | 持续 | 5 个来源 |
| **评估准确率** | >90% | 待追踪 |
| **整合速度** | <1 小时 | ~30 分钟 |
| **执行率** | >80% | 待追踪 |
| **反馈收集** | 持续 | 待实现 |

---

## 🎯 下一步行动

### 太一 (总管)

- [ ] 实现学习评估算法
- [ ] 创建宪法层文档 (AI-GUIDANCE.md)
- [ ] 优化 Agent 层框架文档

### 守藏吏 (管家)

- [ ] 实现自动归档脚本
- [ ] 维护学习索引
- [ ] 追踪执行进度

### 罔两 (数据)

- [ ] 收集学习整合数据
- [ ] 分析评估准确率
- [ ] 优化决策算法

---

## 💡 宪法原则应用

**负熵法则**:
- ✅ 学习自动分类 → 增加系统秩序
- ✅ 文档规范归档 → 避免信息混乱

**价值基石**:
- ✅ 实用价值：快速定位学习内容
- ✅ 进化价值：持续优化评估算法

**观察者协议**:
- 🔄 自动化：监听学习输入 → 自动评估 → 自动归档

---

*创建时间：2026-03-29 21:18*
*太一体系 · 学习整合自动化协议 v1.0*
