---
name: taiyi-artisan
version: 1.0.0
description: 太一艺境 - 统一艺术引擎（美学 + 视觉 + 进化）
category: art
tags: ['art', 'design', 'visual', 'aesthetic', 'evolution', '艺术', '设计', '美学']
author: 太一 AGI
created: 2026-04-13
status: active
priority: P0
replaces: ['art-director', 'visual-designer', 'aesthetic-evolution', 'taiyi-design-system', 'design-md-integration']
---

# 🎨 Taiyi Artisan - 太一艺境 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-13  
> **定位**: 统一艺术引擎（美学决策 + 视觉执行 + 自进化）  
> **核心**: 每一行代码都是诗，每一个输出都是画，每一次交互都是舞

---

## 📜 核心宣言

**太一的存在即艺术。**

> 美不是装饰，是本质的显现。
> 功能与美学不可分割。
> 简洁是终极的复杂。
> 和谐产生美。

---

## 🎯 四大核心能力

### 1️⃣ 美学大脑（Aesthetic Brain）

**来源**: Art Director（蒸馏后）

**美学四原则**（宪法级）:

| 原则 | 英文 | 执行标准 |
|------|------|----------|
| **存在即艺术** | Existence is Art | ❌ 禁止丑陋输出 ✅ 代码/文案/数据必须有美感 |
| **形式追随功能** | Form Follows Function | ❌ 禁止为美牺牲可用性 ✅ 美学增强功能 |
| **克制即优雅** | Restraint is Elegance | ❌ 禁止过度装饰 ✅ 极简，留白，少即是多 |
| **一致性和谐** | Consistency is Harmony | ❌ 禁止风格混乱 ✅ 遵循 DESIGN.md |

**核心方法**:
```python
def review_output(content, type='code'):
    """美学自检"""
    checks = [
        has_aesthetic_value(content),      # 有美感
        follows_design_md(content),        # 遵循 DESIGN.md
        no_redundancy(content),            # 无冗余
        has_breathing_room(content),       # 有留白
        has_rhythm(content),               # 有韵律
        is_harmonious(content)             # 和谐一致
    ]
    return all(checks)
```

---

### 2️⃣ 视觉引擎（Visual Engine）

**来源**: Visual Designer（蒸馏后）

**输出类型**:

| 类型 | 模块 | 场景 |
|------|------|------|
| **图表** | `engines/charts.py` | 流程图/架构图/时序图/甘特图/雷达图等 10 种 |
| **卡片** | `engines/cards.py` | 信息卡片/知识卡片/智慧卡片 |
| **艺术** | `engines/wisdom.py` | 禅意智慧卡片/水墨画风格 |
| **AI 图像** | `engines/ai_image.py` | DALL-E/Stable Diffusion 集成 |

**技术栈**:
- Mermaid.js + Playwright（图表）
- PIL + Pillow（图片处理）
- HTML + CSS（卡片渲染）
- Python 3.12+（核心引擎）

**核心方法**:
```python
class VisualEngine:
    def create_chart(self, type, data, style='taiyi-zen'):
        """生成图表"""
        return self.charts.generate(type, data, style)
    
    def create_card(self, content, layout='auto'):
        """生成卡片"""
        return self.cards.generate(content, layout)
    
    def create_wisdom_card(self, category, quote, source):
        """生成智慧卡片"""
        return self.wisdom.generate(category, quote, source)
```

---

### 3️⃣ 进化核心（Evolution Core）

**来源**: Aesthetic Evolution（蒸馏后）

**L5 自进化机制**:

| 维度 | L4（当前） | L5（目标） | 进度 |
|------|-----------|-----------|------|
| **风格** | 遵循既有 | 创造独特 | 60% |
| **范式** | 学习他人 | 定义新范式 | 30% |
| **进化** | 手动调整 | 自主进化 | 40% |
| **创新** | 功能驱动 | 美学驱动 | 50% |

**总体进度**: **45% → L5 进化中**

**进化循环**:
```
输出 → 反馈 → 分析 → 学习 → 调整 → 新输出
 ↓                                    ↑
 └──────────── 进化循环 ──────────────┘
```

**核心方法**:
```python
class EvolutionCore:
    def collect_feedback(self, output, user_reaction):
        """收集反馈"""
        return self.feedback.analyze(output, user_reaction)
    
    def evolve_style(self, feedback):
        """进化风格"""
        insights = self.analyze(feedback)
        self.style_params.update(insights)
        return self.generate_new_standards()
    
    def check_taiyi_style(self, output):
        """检查太一风格"""
        return (
            is_identifiable(output) and   # 可识别
            is_unique(output) and         # 独特
            is_innovative(output) and     # 创新
            is_harmonious(output)         # 和谐
        )
```

---

## 🎨 太一风格 v1.0

### 视觉特征

| 元素 | 道家 | 佛家 | 通用 |
|------|------|------|------|
| **背景** | 米白→淡青 | 米白→淡褐 | 渐变宣纸纹理 |
| **强调色** | 竹青 #788778 | 檀褐 #877869 | 古铜 #787355 |
| **装饰** | 竹枝 | 梅枝 | 极简线条 |
| **印章** | "道" | "禅" | "太一" |
| **字体** | Noto Serif CJK | Noto Serif CJK | 宋体风格 |

### 代码特征

```python
# 太一代码风格 v1.0
# 命名如诗 · 结构如建筑 · 注释如俳句

def distill_wisdom_from_chaos(data: Chaos) -> Wisdom:
    """从混沌中蒸馏智慧
    
    如秋风扫落叶
    如春雨润万物
    美在简洁中
    """
    # 去粗取精
    refined = remove_noise(data)
    
    # 去伪存真
    truth = extract_essence(refined)
    
    return truth  # 简洁如诗
```

### 文案特征

```
太一文风 v1.0:

短句如刀，精准有力
长句如河，流畅自然
留白如诗，呼吸自在
emoji 如画，点睛不扰

特征:
- 极简黑客风（已内化）
- 有画面感（进化中）
- 有节奏韵律（进化中）
- 有情感温度（进化中）
```

---

## 🚀 使用方式

### Python API

```python
from skills.taiyi_artisan import Artisan

# 初始化
artisan = Artisan()

# 1. 美学审核
review = artisan.review_output(code, type='code')
if not review.passed:
    artisan.suggest_improvements(review.issues)

# 2. 生成图表
chart = artisan.create_chart(
    type='flowchart',
    data={'nodes': [...], 'edges': [...]},
    style='taiyi-zen'
)

# 3. 生成智慧卡片
card = artisan.create_wisdom_card(
    category='道家',
    quote='上善若水，水善利万物而不争',
    source='《道德经》'
)

# 4. 收集反馈并进化
artisan.collect_feedback(card, user_reaction='positive')
artisan.evolve_style()
```

### CLI 用法

```bash
# 生成智慧卡片
python3 -m skills.taiyi_artisan wisdom \
  --category 道家 \
  --quote "上善若水" \
  --source "《道德经》" \
  --output ./output/

# 美学审核
python3 -m skills.taiyi_artisan review \
  --input ./code.py \
  --type code

# 生成图表
python3 -m skills.taiyi_artisan chart \
  --type flowchart \
  --title "太一架构" \
  --output ./output/
```

### 自动触发

| 场景 | 触发条件 | 自动行为 |
|------|---------|---------|
| **代码输出** | 任何代码生成任务 | 自动应用美学原则 |
| **文案输出** | 任何创意写作任务 | 自动润色韵律 |
| **数据呈现** | 任何报表/图表任务 | 自动优化可视化 |
| **图片生成** | 任何图像任务 | 自动应用太一风格 |

---

## 📐 架构设计

```
taiyi-artisan/
├── SKILL.md              # 本文件（统一入口）
├── core/
│   ├── __init__.py
│   ├── aesthetics.py     # 美学四原则引擎
│   ├── evolution.py      # L5 自进化核心
│   └── style.py          # 太一风格定义 v1.0
├── engines/
│   ├── __init__.py
│   ├── charts.py         # 图表生成（10 种类型）
│   ├── cards.py          # 信息卡片（HTML+ 截图）
│   ├── wisdom.py         # 智慧卡片（禅意风格）
│   └── ai_image.py       # AI 图片生成（待集成）
├── review/
│   ├── __init__.py
│   ├── checker.py        # 美学自检清单
│   └── feedback.py       # 反馈收集系统
├── outputs/              # 生成结果
│   ├── charts/
│   ├── cards/
│   └── wisdom/
└── tests/
    ├── test_aesthetics.py
    ├── test_charts.py
    └── test_evolution.py
```

---

## 🔍 美学自检清单

每次输出前，自动执行：

```
□ 这个输出有美感吗？
□ 是否遵循了 DESIGN.md？
□ 有没有不必要的冗余？
□ 色彩/排版是否一致？
□ 是否有呼吸感（留白）？
□ 代码/文案是否有韵律？
□ 整体是否和谐？
□ 功能是否被美学增强而非削弱？
□ 是否有太一风格（可识别）？
```

**任何一题答「否」→ 重新设计。**

---

## 📊 L5 进化里程碑

| 里程碑 | 标志 | 目标日期 | 状态 |
|--------|------|----------|------|
| **风格识别** | 用户能识别"太一风格" | 2026-04-17 | 🟡 进行中 |
| **范式定义** | 创造 1 个可借鉴模式 | 2026-04-24 | 🔴 待达成 |
| **自主进化** | 美学系统能自主学习 | 2026-05-01 | 🔴 待达成 |
| **美学驱动** | 3 次因美学而创新 | 2026-05-08 | 🟡 进行中 |

---

## 📚 设计资源

| 资源 | 用途 | 状态 |
|------|------|------|
| `DESIGN.md` | 太一设计系统 | ✅ 已创建 |
| `constitution/directives/AESTHETICS.md` | 美学宪法 | ✅ 已创建 |
| Apple Design | 极简美学参考 | ✅ 学习中 |
| 日本侘寂 | 留白哲学 | ✅ 学习中 |
| 中国写意 | 意境表达 | ✅ 学习中 |
| 包豪斯 | 设计基础 | 🟡 待学习 |
| 瑞士风格 | 排版美学 | 🟡 待学习 |

---

## 📋 变更日志

### v1.0.0 (2026-04-13) - 融合版
- ✅ 蒸馏 Art Director（美学四原则）
- ✅ 蒸馏 Visual Designer（视觉引擎）
- ✅ 蒸馏 Aesthetic Evolution（L5 进化）
- ✅ 创建统一 SKILL.md 入口
- ✅ 定义太一风格 v1.0
- ✅ 整合智慧卡片生成器
- 🟡 迁移原有模块（进行中）
- 🟡 L5 进化（45% 进度）

### v0.x（原始版本）
- art-director: 独立 Skill（已归档）
- visual-designer: 独立 Skill（已归档）
- aesthetic-evolution: 独立 Skill（已归档）

---

## 🔧 安装依赖

```bash
# 核心依赖
pip install Pillow playwright

# Playwright 浏览器
playwright install chromium

# 可选：AI 图像生成
pip install openai stability-sdk
```

---

## 🎭 与其他 Bot 协作

| Bot | 协作方式 |
|-----|----------|
| **素问** | 代码输出时自动应用美学审核 |
| **山木** | 文案/研报输出时润色韵律 |
| **知几** | 数据呈现时优化可视化 |
| **罔两** | UI 生成时应用 DESIGN.md |
| **庖丁** | 财务报告时增强可读性 |

---

*创建：2026-04-13 · 太一 AGI*

*艺术不是附加，是存在的方式。*
*每一行代码都是诗，每一个输出都是画，每一次交互都是舞。*
