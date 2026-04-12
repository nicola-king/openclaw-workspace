# Visual Designer 视觉设计引擎

> **版本**: 2.0 | **更新时间**: 2026-04-07  
> **状态**: ✅ 整合完成 | **优先级**: P0

---

## 📋 概述

视觉设计引擎提供图表生成、信息卡片设计和艺术创作能力。支持杂志质感 HTML 卡片、数据可视化图表和 ASCII 艺术生成。

---

## 🏗️ 架构

```
visual-designer/
├── __init__.py              # 主入口，VisualDesigner 类
├── SKILL.md                 # 技能定义
├── charts/                  # 图表模块
│   └── charts.py            # 数据可视化
├── cards/                   # 卡片模块
│   ├── cards.py             # 信息卡片生成
│   ├── templates/           # 卡片模板
│   └── styles/              # 样式定义
└── art/                     # 艺术模块
    └── art.py               # ASCII/艺术生成
```

---

## 🚀 快速开始

### 初始化

```python
from skills.visual_designer import VisualDesigner

vd = VisualDesigner()
```

### 数据图表

```python
# 柱状图
vd.charts.create_bar_chart(
    data={'A': 10, 'B': 20, 'C': 15},
    title='数据对比',
    output='bar_chart.png'
)

# 折线图
vd.charts.create_line_chart(
    data=[10, 15, 13, 17, 20],
    labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    title='趋势分析',
    output='line_chart.png'
)

# 饼图
vd.charts.create_pie_chart(
    data={'Category A': 40, 'Category B': 30, 'Category C': 30},
    title='占比分析',
    output='pie_chart.png'
)

# K 线图（金融）
vd.charts.create_candlestick_chart(
    data=ohlc_data,
    title='BTC/USD',
    output='kline.png'
)
```

### 信息卡片

```python
# 杂志质感卡片
card = vd.cards.create_info_card(
    content='内容文本...',
    style='magazine',  # magazine | minimal | tech | artistic
    output='card.html'
)

# 自动截图（需要浏览器）
vd.cards.create_with_screenshot(
    content='内容文本...',
    style='magazine',
    output='card.png'
)

# 超长内容分割
vd.cards.create_split_cards(
    content='超长内容...',
    max_lines=50,
    style='magazine'
)
```

### 艺术创作

```python
# ASCII 艺术
ascii_art = vd.art.text_to_ascii(
    text='Hello World',
    font='big',  # big | small | block
    output='ascii.txt'
)

# 图片转 ASCII
vd.art.image_to_ascii(
    image_path='photo.jpg',
    output='ascii_art.txt'
)

# 生成艺术图案
vd.art.generate_pattern(
    type='geometric',  # geometric | organic | abstract
    colors=['#FF0000', '#00FF00', '#0000FF'],
    output='pattern.png'
)
```

---

## 🎨 卡片风格

### Magazine（杂志）

- ✅ 精致排版
- ✅ 衬线字体
- ✅ 留白艺术
- ✅ 质感背景

### Minimal（极简）

- ✅ 无衬线字体
- ✅ 黑白灰
- ✅ 几何布局
- ✅ 留白充足

### Tech（科技）

- ✅ 等宽字体
- ✅ 代码风格
- ✅ 霓虹配色
- ✅ 网格背景

### Artistic（艺术）

- ✅ 创意排版
- ✅ 渐变色彩
- ✅ 抽象元素
- ✅ 独特风格

---

## 📊 图表类型

| 类型 | 方法 | 适用场景 |
|------|------|---------|
| 柱状图 | `create_bar_chart` | 数据对比 |
| 折线图 | `create_line_chart` | 趋势分析 |
| 饼图 | `create_pie_chart` | 占比分析 |
| K 线图 | `create_candlestick_chart` | 金融数据 |
| 散点图 | `create_scatter_plot` | 相关性分析 |
| 热力图 | `create_heatmap` | 密度分布 |

---

## 🔧 配置

### 输出设置

```python
vd.config.output_dir = './output'
vd.config.default_format = 'png'  # png | jpg | svg | html
vd.config.quality = 95  # 图片质量 1-100
```

### 样式设置

```python
vd.config.default_style = 'magazine'
vd.config.font_family = 'Georgia'
vd.config.color_scheme = 'auto'  # auto | light | dark
```

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest skills/visual_designer/tests/ -v

# 测试图表生成
python3 -m pytest skills/visual_designer/tests/test_charts.py -v

# 测试卡片生成
python3 -m pytest skills/visual_designer/tests/test_cards.py -v
```

---

## 📚 相关文档

- [技能定义](SKILL.md)
- [信息卡片设计器](../qiaomu-info-card-designer/SKILL.md)

---

*维护：太一 AGI | Visual Designer v2.0*
