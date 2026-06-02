# 宋式美学模块 v1.0.0

## 概述
宋式美学九大特征嵌入太一系统：**留白·朴素·自然·通透·淡雅·精致·含蓄·禅意·有序**

## 架构位置
`art-agent/modules/song-aesthetics/`

## 文件结构
```
song-aesthetics/
├── config.json          ← 模块配置
├── design-tokens.json   ← 完整设计令牌（色彩/字体/间距/构图/动效）
├── core.py              ← 评估引擎 + CSS 生成 + CLI
└── SKILL.md             ← 本文件
```

## 使用方式

### CLI
```bash
# 评估内容是否符合宋式美学
python3 core.py --text "你的内容..."

# 生成 CSS custom properties
python3 core.py --css

# 输出完整设计令牌
python3 core.py --tokens

# 根据上下文建议构图方案
python3 core.py --composition "文章"
```

### Python API
```python
from song_aesthetics import SongAestheticsEngine

engine = SongAestheticsEngine()

# 评估内容
report = engine.evaluate("你的内容...")
# → {total_score, level, dimensions: {留白:{score,detail}, ...}}

# 生成设计决策
decisions = engine.generate_design_decisions()
# → {color_palette, typography, spacing, composition, prohibitions}

# 生成CSS
css = engine.generate_css(":root")
```

## 联动脉络

### 与 aesthetic-filter 联动
- 所有输出经过 aesthetic-filter 后 → song-aesthetics 二次验证
- 验证未通过（等级<A）→ 自动调整留白/色彩/排版

### 与 scoring-engine 联动
- 在 scoring-engine 中新增 SongAestheticsScorer
- 占全新第七维度，权重 0.10

### 与 dispatcher 联动
- dispatcher 路由表新增 "宋式"/"宋"/"song" → TaskDomain.SONG

## 九特征评分规则摘要

| 特征 | 扣分项 | 加分项 |
|------|--------|--------|
| 留白 | 空白<15% / 段落>500字 | 空白25-40% |
| 朴素 | 装饰过多/Emoji>30/标题层级>4 | 最少装饰 |
| 自然 | 夸张词汇/句式重复 | 长短句交替 |
| 通透 | 段落>400字/无标题 | 多级标题/列表 |
| 淡雅 | !!!/😱🔥/加粗>8处 | 克制表达 |
| 精致 | 缺句号/标点混用/列表不统一 | 格式规范 |
| 含蓄 | 绝对性词汇过多/我>10次 | 分寸感词汇 |
| 禅意 | 功利词汇/对称 | 节奏变化/非对称 |
| 有序 | 标题跳级/无H1 | 连续层级/清晰结构 |

## 设计令牌使用
完整设计令牌在 `design-tokens.json`，涵盖：
- 色彩体系（天青主色、黛色辅色、9种功能色、禁用色）
- 字体体系（Serif标题 + Sans正文）
- 间距体系（4px→48px 递进 + 黄金比例留白）
- 构图体系（枯山水/手卷/双屏/册页 4种模式）
- 边框阴影（极细边、纸质感、<12%透明度）
- 图像滤镜（song_filter/ink_wash）
- 动效（慢柔自然、无弹跳）
- 九特征→CSS映射表（每条特征转成具体CSS规则）
- 完整禁止清单（10条）
