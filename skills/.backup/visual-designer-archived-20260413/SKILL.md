---
name: visual-designer
version: 1.0.0
description: 视觉设计引擎 - 图表/信息卡片/艺术生成
category: visual
tags: ['visual', 'chart', 'design', 'image', 'art', '可视化，设计，图表，图片']
author: 太一 AGI
created: 2026-04-07
status: active
priority: P0
---

# Visual Designer v1.0 - 统一视觉设计引擎

> **版本**: 1.0.0 (整合版) | **创建**: 2026-04-07  
> **负责 Bot**: 山木 | **状态**: ✅ 已激活

---

## 📋 功能概述

统一视觉设计技能，整合 4 个相关技能。

**整合内容**:
- ✅ ppt-chart-generator → `charts/` (图表生成)
- ✅ qiaomu-info-card-designer → `cards/` (信息卡片)
- ⚪ ascii-art → `art/` (ASCII 艺术 - 待整合)
- ⚪ image-generator → `art/` (AI 图片生成 - 待整合)

**独立保留**: unsplash-image (图片搜索工具)

---

## 🏗️ 架构设计

```
visual-designer/
├── SKILL.md (主入口)
├── charts/ (图表模块)
│   ├── chart_generator.py (PPT 图表生成器)
│   ├── charts_config.json (图表配置)
│   ├── README.md (使用说明)
│   └── output/ (输出目录)
├── cards/ (卡片模块)
│   ├── scripts/ (脚本：截图/分割)
│   ├── references/ (设计规范：design-spec.md)
│   ├── assets/ (素材资源)
│   └── output/ (输出目录)
└── art/ (艺术模块)
    ├── ascii.py (ASCII 艺术 - 待添加)
    └── ai_image.py (AI 图片生成 - 待添加)
```

---

## 🚀 使用方式

### Python API

```python
# 图表生成
from skills.visual_designer.charts.chart_generator import ChartGenerator

generator = ChartGenerator(output_dir="./output")
generator.create_flowchart(
    title="太一 AGI 架构图",
    nodes=["太一", "知几", "山木", "素问"],
    edges=[("太一", "知几"), ("太一", "山木"), ("太一", "素问")],
    output_name="taiyi-architecture"
)

# 信息卡片
# 通过 CLI 或脚本调用 qiaomu 流程
```

### CLI 用法

```bash
# 生成流程图
cd skills/visual-designer/charts
python3 chart_generator.py flowchart \
  --title "太一 AGI 架构" \
  --nodes "太一，知几，山木，素问" \
  --edges "太一→知几，太一→山木，太一→素问" \
  --output "./output/architecture.png"

# 生成信息卡片 (qiaomu 流程)
# 通过山木 Bot 触发，自动调用 cards/scripts/
```

---

## 📊 模块说明

### 1. Charts Module - 图表

**位置**: `skills/visual-designer/charts/`

**核心功能**:
- 10 种专业图表类型（流程图/架构图/时序图/甘特图/雷达图等）
- 输出格式：PNG (1920x1080) + HTML (可交互) + SVG (矢量可编辑)
- Mermaid.js 本地渲染，Playwright 截图

**技术栈**:
- Python 3.10+
- Playwright (Chromium)
- Mermaid.js (本地打包)

**文件结构**:
```
charts/
├── chart_generator.py (核心类：ChartGenerator)
├── charts_config.json (批量生成配置)
├── README.md (详细文档)
└── output/ (生成结果)
```

**支持的图表类型**:
1. 流程图 (Flowchart)
2. 架构图 (Architecture Diagram)
3. 时序图 (Sequence Diagram)
4. 甘特图 (Gantt Chart)
5. 雷达图 (Radar Chart)
6. 桑基图 (Sankey Diagram)
7. ER 图 (Entity Relationship)
8. 组织架构图 (Org Chart)
9. 思维导图 (Mind Map)
10. 数据看板 (Dashboard)

### 2. Cards Module - 信息卡片

**位置**: `skills/visual-designer/cards/`

**核心功能**:
- 杂志质感 HTML 信息卡片
- 自动 URL 内容抓取 (arXiv/X/微信公众号)
- 智能内容提炼 (4-6 个核心要点)
- Playwright 自动截图 (1200px @2x)
- 超长内容自动分割 (可选)

**工作流**:
```
输入 (文本/URL)
    ↓
Step 0: URL 内容抓取 (r.jina.ai/arXiv HTML)
    ↓
Step 1: 提炼核心信息 (主标题 +4-6 要点 + 金句)
    ↓
Step 2: 分析布局 (低/中/高密度)
    ↓
Step 3: 生成 HTML (Swiss International 风格)
    ↓
Step 4: Playwright 截图 (PNG @2x)
    ↓
Step 5: 超长分割 (可选，默认不执行)
    ↓
输出：~/乔木新知识库/60-69 素材/65 附件库/info-cards/
```

**设计规范**:
- 卡片宽度：600px (默认) / 480px / 900px
- 背景色：`#f5f3ed`
- 字体：Swiss International Style
- 输出：1200px @2x (Retina)

**文件结构**:
```
cards/
├── scripts/
│   ├── fetch_content.py (URL 抓取)
│   ├── generate_card.py (HTML 生成)
│   ├── screenshot.py (Playwright 截图)
│   └── split_card.py (超长分割)
├── references/
│   └── design-spec.md (视觉规范)
├── assets/ (字体/图标/模板)
└── output/ (生成结果)
```

### 3. Art Module - 艺术 (待整合)

**位置**: `skills/visual-designer/art/`

**计划整合**:
- ASCII 艺术生成
- AI 图片生成 (DALL-E/Stable Diffusion)
- 风格迁移

---

## 🎯 使用场景

### 场景 1: 研报图表生成

```python
# 山木研报生成器集成
from skills.visual_designer.charts.chart_generator import ChartGenerator

def generate_report_charts(report_data):
    generator = ChartGenerator(output_dir="./reports/charts")
    
    # 生成架构图
    generator.create_flowchart(
        title=report_data["title"],
        nodes=report_data["components"],
        edges=report_data["relationships"],
        output_name=f"{report_data['id']}-architecture"
    )
    
    return generator.output_files
```

### 场景 2: 论文/文章信息卡片

```bash
# 用户输入：生成这张卡片 https://arxiv.org/abs/2603.25694
# 自动流程：
# 1. 抓取 arXiv HTML 全文
# 2. 提炼核心发现 (主标题 +5 要点 + 金句)
# 3. 生成杂志风格 HTML
# 4. Playwright 截图 → 1200px PNG
# 5. 保存到 ~/乔木新知识库/60-69 素材/65 附件库/info-cards/
```

### 场景 3: 项目进度甘特图

```python
generator.create_gantt_chart(
    title="Q2 项目计划",
    tasks=[
        {"name": "需求分析", "start": "2026-04-01", "end": "2026-04-07"},
        {"name": "开发实现", "start": "2026-04-08", "end": "2026-04-21"},
        {"name": "测试上线", "start": "2026-04-22", "end": "2026-04-28"},
    ],
    output_name="q2-timeline"
)
```

---

## 🔌 与共享层集成

```python
from skills.shared import SharedDatabase, EventBus, Events

# 记录设计操作
db = SharedDatabase.get_instance()
db.record_visual_design(
    type='flowchart',
    style='mermaid',
    output='architecture.png',
    duration_ms=2500
)

# 发布事件
event_bus = EventBus.get_instance()
event_bus.publish(Events.VISUAL_CREATED, {
    'type': 'flowchart',
    'output': 'architecture.png',
    'module': 'charts'
})
```

---

## 📋 变更日志

### v1.0.0 (2026-04-07) - 整合版
- ✅ 备份原始技能到 `skills/.backup/`
- ✅ 合并 ppt-chart-generator → `charts/`
- ✅ 合并 qiaomu-info-card-designer → `cards/`
- ✅ 创建统一 SKILL.md 入口
- ⚪ ascii-art 待整合到 `art/`
- ⚪ image-generator 待整合到 `art/`

### v0.x (原始版本)
- ppt-chart-generator: 独立技能
- qiaomu-info-card-designer: 独立技能

---

## 📚 相关文档

- [图表生成器详细文档](charts/README.md)
- [信息卡片设计规范](cards/references/design-spec.md)
- [山木研报生成器](../shanmu-reporter/SKILL.md)

---

## 🔧 安装依赖

```bash
# Playwright (图表 + 卡片都需要)
pip install playwright
playwright install chromium

# 可选：PIL (图片处理)
pip install Pillow
```

---

*维护：山木 AGI | Visual Designer v1.0 | 最后更新：2026-04-07*
