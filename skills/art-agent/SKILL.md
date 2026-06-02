---
name: art-agent
version: 3.0.0
description: 太一美学引擎 v3.0 - 统一艺术 Agent + 智能调度 + 自进化
category: creativity
tags: ['art', 'design', 'visual', 'brand', 'aesthetics', 'evolution', 'dispatch']
author: 太一 AGI
created: 2026-04-24
updated: 2026-05-08
status: active
---

# 🎨 Art Agent v3.0 — 统一艺术智能体

> **版本**: 3.0.0
> **架构**: 统一调度引擎 + 20 专业模块 + 自进化闭环

---

## 🏗 架构总览

```
用户请求 ("用星巴克风格美化这个报告")
       │
       ▼
┌──────────────────────────────────────────────┐
│  统一调度引擎 (dispatcher.py)                 │
│                                              │
│  智能路由 (关键词 → 任务类型 → 模块)          │
│  调度拓扑生成 (dispatch-viz)                  │
│  自进化学习 (self-evolution)                  │
│  调度历史统计                                │
└──────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│  路由表                                       │
│                                              │
│  BRAND     → brand-studio  (品牌工作室)       │
│  DESIGN    → design-agent  (设计 Agent)       │
│  VISUAL    → chart-generator (可视化)          │
│  CONTENT   → content-creator (内容创作)        │
│  FILTER    → aesthetic-filter (美学过滤)       │
│  NARRATIVE → visual-narrative (视觉叙事)      │
│  WORKFLOW  → dispatch-viz (拓扑可视化)        │
│  EVOLVE    → self-evolution (自进化)          │
│  SONG      → song-aesthetics   (宋式美学引擎)    │
└──────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│  自进化闭环                                    │
│                                              │
│  每次调度 → 记录 → 学习 → 优化路由 → 下次更好  │
│  宪法学习 (Elon五步/负熵/冰山/第一性/二阶)     │
└──────────────────────────────────────────────┘
```

---

## 🧩 模块清单 (19个)

### 美学核心
| 模块 | 功能 | 状态 |
|------|------|:----:|
| **aesthetic-filter** | 美学过滤器（格式/风格/视觉/审校） | ✅ v1.1 |
| **aesthetic-scorer** | 多维度美学评分（含宋式美学维度） | ✅ v2.0 |
| **aesthetics-engine** | 美学引擎 | ✅ v1.0 |
| **song-aesthetics** | 宋式美学引擎（九特征评估/设计令牌/CSS生成） | ✅ v1.0 |

### 艺术创作
| 模块 | 功能 | 状态 |
|------|------|:----:|
| **taiyi-artisan** | 太一艺境（艺术创作） | ✅ v1.0 |
| **taiyi-design** | 太一设计系统 | ✅ v1.0 |
| **brand-studio** | 品牌工作室（58品牌规格） | ✅ v1.0 |
| **brand-guardian** | 品牌守护者 | ✅ v1.0 |
| **content-creator** | 内容创作（排期/优化/发布） | ✅ v1.0 |
| **design-agent** | 设计 Agent | ✅ v1.0 |

### UI/UX
| 模块 | 功能 | 状态 |
|------|------|:----:|
| **ui-designer** | UI 设计器 | ✅ v1.0 |
| **ux-writer** | UX 写作助手 | ✅ v1.0 |
| **design-system** | 设计系统 | ✅ v1.0 |

### 可视化
| 模块 | 功能 | 状态 |
|------|------|:----:|
| **chart-generator** | 图表生成 | ✅ v1.0 |
| **card-generator** | 卡片生成 | ✅ v1.0 |
| **3d-generator** | 3D 生成 | ✅ v1.0 |
| **visual-workflow** | 可视化工作流 | ✅ v1.0 |
| **visual-api** | 视觉 API | ✅ v1.0 |
| **visual-narrative** | 视觉叙事 | ✅ v1.0 |

### 调度 & 进化
| 模块 | 功能 | 状态 |
|------|------|:----:|
| **dispatcher (本层)** | 统一调度引擎 | ✅ v3.0 |
| **dispatch-viz** | 调度拓扑可视化 | ✅ v1.0 |
| **self-evolution** | 自进化（宪法学习/技能结晶） | ✅ v1.0 |

---

## 🚀 使用方式

### CLI
```bash
# 直接调度
python3 dispatcher.py "用星巴克风格美化这份报告"

# 指定品牌
python3 dispatcher.py "生成 Apple 风格的卡片"
```

### Python API
```python
from dispatcher import ArtDispatcher

dispatch = ArtDispatcher()

# 智能路由 - 自动识别任务类型
result = dispatch.dispatch("用星巴克风格美化咖啡店选址报告")
# → 自动路由到 brand-studio 模块

result = dispatch.dispatch("生成图表展示数据对比")
# → 自动路由到 chart-generator 模块

# 查看调度统计
stats = dispatch.get_stats()
print(stats["total_dispatch"], stats["success_rate"])
```

---

## 🔄 自进化闭环

```
调度执行
    │
    ▼
记录 (timestamp/domain/duration/status)
    │
    ▼
学习 (宪法规则 + 历史模式)
    │
    ▼
优化 (路由权重/模块选择/参数微调)
    │
    ▼
下次调度更好
```

当前宪法学习规则：8 条 (CONST-001~005, STRAT-001~003)
进化维度：7 维 (质量/效率/覆盖/准确率/成本/用户反馈/创新)

---

## 📊 品牌库 (58个)

已集成 58 个品牌 CSS 设计规范，可直接调用：
Apple / Nike / Starbucks / Ruixing / Figma / Notion / Linear
Binance / Claude / Cursor / MongoDB / Mistral / Cohere
Airbnb / Framer / Pinterest / Playstation / Ferrari / BMW
...

---

## 🖨 渲染策略集成

> 遵循 `constitution/rules/RENDERING-PRINCIPLES.md`

art-agent 所有可视化模块生成 PDF 时，使用统一 `shared/render_engine`：

### 渲染引擎选择矩阵

| 模块 | 引擎 | 备注 |
|------|------|------|
| chart-generator | WeasyPrint | 图表报告 PDF |
| card-generator | WeasyPrint | 风格卡片 PDF |
| brand-studio | WeasyPrint | 品牌规范文档 PDF |
| dispatch-viz | WeasyPrint | 调度拓扑图 PDF |
| 其他 | WeasyPrint | 默认中文渲染 |

### render-engine API

```python
from shared.render_engine import render, verify_pdf, health_check

# 一键渲染 + 验证
result = render(
    body_html="<h1>标题</h1><p>正文</p>",
    output_path="/tmp/output.pdf",
    css="h1 { color: #1a3c7a; }",
    content_type="chinese",
    verify_keywords=["知几", "山木"],
)
# {'status':'ok', 'path':'...', 'size':12345, 'verify':{'valid':True}}

# 手动验证
report = verify_pdf("output.pdf", keywords=["关键字段"])
```

### 渲染铁律
1. 中文多页文档 → WeasyPrint 首选
2. 不允许 fpdf2 + .ttc 字体（静默渲染异常）
3. 生成后必须 pdftotext 验证关键字段
4. 字体用 NotoSansCJK-Regular.ttc（绝对路径 file:///）
5. 页边距 20mm 安全值

---

## 📁 文件结构

```
art-agent/
├── dispatcher.py            ← 统一调度引擎 (v3.0)
├── SKILL.md                 ← 本文件
├── manifest.json            ← 模块清单
│
├── modules/ (20个)
│   ├── shared/              ← 共享模块
│   │   ├── __init__.py
│   │   └── render_engine.py ← 统一渲染引擎 (v1.0)
│   ├── aesthetic-filter/    ← 美学过滤器
│   ├── aesthetic-scorer/    ← 美学评分
│   ├── aesthetics-engine/   ← 美学引擎
│   ├── brand-studio/        ← 品牌工作室
│   ├── brand-guardian/      ← 品牌守护者
│   ├── taiyi-artisan/       ← 艺术创作
│   ├── taiyi-design/        ← 设计系统
│   ├── design-agent/        ← 设计 Agent
│   ├── design-system/       ← 设计系统
│   ├── ui-designer/         ← UI 设计
│   ├── ux-writer/           ← UX 写作
│   ├── content-creator/     ← 内容创作
│   ├── chart-generator/     ← 图表 PDF (v1.1.0 渲染增强)
│   ├── card-generator/      ← 卡片 PDF (v1.1.0 渲染增强)
│   ├── 3d-generator/        ← 3D
│   ├── visual-workflow/     ← 工作流
│   ├── visual-api/          ← 视觉 API
│   ├── visual-narrative/    ← 视觉叙事
│   ├── dispatch-viz/        ← 拓扑可视化
│   └── self-evolution/      ← 自进化
│
├── core/
├── deploy/
└── docs/
```

---

*太一 Art Agent v3.0 · 统一艺术智能体*
*创建时间：2026-05-08 | 更新：2026-05-08*
*架构: 统一调度 + 20 模块(含shared) + 自进化闭环*
*渲染: WeasyPrint + shared/render-engine (遵循 RENDERING-PRINCIPLES.md)*

---

## ⚖️ 美学原则（常驻）

### 智能风格匹配（Aesthetic Intelligence）
> 除客户明确指定风格外，art-agent 根据文档内容智能自动化匹配品牌风格。

```
客户说："用星巴克风格" → 按指定执行
客户说："出一份报告"    → 自动分析内容匹配最佳风格
客户说："用BMW风格"    → 按指定执行
客户说："分析这个"      → 自动匹配
```

**匹配规则（按优先级）：**
| 内容关键词 | 匹配风格 | 适用场景 |
|-----------|---------|---------|
| 钢结构/建筑/工程/施工 | BMW 蓝白工程风 | 工业/制造/基建 |
| 中东/沙特/基建/能源 | HashiCorp/IBM 专业风 | 能源/基础设施 |
| 跨境贸易/外贸/出口 | Binance 黄黑金融风 | 贸易/金融分析 |
| 咖啡/餐饮/消费 | Starbucks 绿 | 餐饮/消费品牌 |
| 科技/AI/软件 | NVIDIA/Cursor 科技风 | 科技/软件方案 |
| 设计/品牌/艺术 | Figma/Apple 极简风 | 创意/品牌方案 |
| 旅游/酒店 | Airbnb 温暖风 | 旅游/住宿 |

**铁律：**
1. 客户指定风格 → 绝对服从
2. 客户未指定 → 智能匹配，不询问
3. 匹配置信度低 → 默认 Binance 风格（最通用的报告风格）
4. 不重复询问、不冗余确认
```

