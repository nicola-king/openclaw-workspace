#!/usr/bin/env python3
"""
设计卡片生成器 - 印证艺术设计系统效果

功能:
1. 生成多种设计风格的卡片
2. 展示东方/西方/中国元素融合
3. Markdown 格式输出
4. 可直接用于报告/文档

作者：太一 AGI
创建：2026-04-10
"""

import json
from pathlib import Path
from datetime import datetime

# 导入艺术设计系统
from artistic_design_system import (
    ArtisticDesignSystem,
    EASTERN_DESIGN,
    WESTERN_MASTERS,
    CHINESE_CLASSICAL,
    SCENE_CONFIGS
)

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"
CARDS_FILE = REPORTS_DIR / "design-cards-showcase.md"


def generate_card_header(title, subtitle, design_style):
    """生成卡片头部"""
    return f"""
```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  {title.center(63)}  ║
║  {subtitle.center(63)}  ║
║                                                               ║
║  设计风格：{design_style.center(51)}║
╚═══════════════════════════════════════════════════════════════╝
```
"""


def generate_eastern_card(region, content):
    """生成东方风格卡片"""
    region_data = EASTERN_DESIGN.get(region, {})
    
    # 获取区域特色
    colors = region_data.get('colors', {})
    layouts = region_data.get('layouts', {})
    principles = region_data.get('principles', {})
    
    # 选择代表色
    color_items = list(colors.items())[:3]
    color_line = " · ".join([f"{v['name']} ({v['hex']})" for k, v in color_items])
    
    # 选择布局
    layout_items = list(layouts.items())[:1]
    layout_name = layout_items[0][1]['name'] if layout_items else '未知'
    
    # 选择原则
    principle_items = list(principles.items())[:2]
    principle_line = " · ".join([v['name'] for k, v in principle_items])
    
    # 纹样装饰
    if region == 'japan':
        pattern = '🌸'
    elif region == 'taiwan':
        pattern = '🏮'
    elif region == 'hong_kong':
        pattern = '🌃'
    elif region == 'singapore':
        pattern = '🦁'
    elif region == 'thailand':
        pattern = '🛕'
    else:
        pattern = '✨'
    
    card = f"""
{pattern * 35}
{pattern}                                                           {pattern}
{pattern}  🎨 东方设计 · {region_data.get('name', region).upper()}                      {pattern}
{pattern}                                                           {pattern}
{pattern}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  {pattern}
{pattern}                                                           {pattern}
{pattern}  代表色彩                                                 {pattern}
{pattern}  {color_line[:60]}  {pattern}
{pattern}                                                           {pattern}
{pattern}  布局风格：{layout_name:<50}  {pattern}
{pattern}  设计原则：{principle_line[:50]:<50}  {pattern}
{pattern}                                                           {pattern}
{pattern}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  {pattern}
{pattern}                                                           {pattern}
{pattern}  {content[:60]:<60}  {pattern}
{pattern}  {content[60:120]:<60}  {pattern}
{pattern}                                                           {pattern}
{pattern}  灵感来源：{region} 东方美学                              {pattern}
{pattern}                                                           {pattern}
{pattern * 35}
"""
    
    return card


def generate_western_card(style, content):
    """生成西方风格卡片"""
    style_data = WESTERN_MASTERS.get(style, {})
    
    # 获取特色
    colors = style_data.get('colors', {})
    layouts = style_data.get('layouts', {})
    principles = style_data.get('principles', {})
    
    # 选择代表色
    color_items = list(colors.items())[:3]
    color_line = " · ".join([f"{v['name']} ({v['hex']})" for k, v in color_items])
    
    # 选择布局
    layout_items = list(layouts.items())[:1]
    layout_name = layout_items[0][1]['name'] if layout_items else '未知'
    
    # 选择原则
    principle_items = list(principles.items())[:2]
    principle_line = " · ".join([v['name'] for k, v in principle_items])
    
    # 大师信息
    masters = set()
    for item in list(colors.values()) + list(layouts.values()) + list(principles.values()):
        if 'master' in item:
            masters.add(item['master'])
    master_line = ", ".join(list(masters)[:2])
    
    card = f"""
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│  🎨 西方设计 · {style_data.get('name', style).upper()}                       │
│                                                               │
│  ───────────────────────────────────────────────────────────  │
│                                                               │
│  代表色彩                                                     │
│  {color_line[:60]}                           │
│                                                               │
│  布局风格：{layout_name:<50}                  │
│  设计大师：{master_line:<50}                  │
│  设计原则：{principle_line[:50]:<50}                  │
│                                                               │
│  ───────────────────────────────────────────────────────────  │
│                                                               │
│  {content[:60]:<60}  │
│  {content[60:120]:<60}                  │
│                                                               │
│  灵感来源：{style} 西方现代设计                              │
│                                                               │
└───────────────────────────────────────────────────────────────┘
"""
    
    return card


def generate_chinese_card(content):
    """生成中国风格卡片"""
    
    # 选择代表色
    color_items = list(CHINESE_CLASSICAL['colors'].items())[:4]
    color_line = " · ".join([f"{v['name']} ({v['hex']})" for k, v in color_items])
    
    # 选择纹样
    pattern_items = list(CHINESE_CLASSICAL['patterns'].items())[:4]
    pattern_line = " ".join([v['emoji'] for k, v in pattern_items])
    
    card = f"""
╭───────────────────────────────────────────────────────────────╮
│                                                               │
│  {pattern_line}  │
│  🎨 中国经典设计 · CHINESE CLASSICAL                          │
│  {pattern_line}  │
│                                                               │
│  ═══════════════════════════════════════════════════════════  │
│                                                               │
│  传统色彩                                                     │
│  {color_line[:60]}                     │
│                                                               │
│  传统纹样：云纹 · 莲花 · 竹子 · 山峦                          │
│  设计原则：天人合一 · 道法自然                                │
│                                                               │
│  ═══════════════════════════════════════════════════════════  │
│                                                               │
│  {content[:60]:<60}  │
│  {content[60:120]:<60}                  │
│                                                               │
│  灵感来源：中国传统美学                                      │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
"""
    
    return card


def generate_fusion_card(eastern_region, western_style, content):
    """生成融合风格卡片 (东方西方 80% + 中国 20%)"""
    
    # 东方元素
    eastern_data = EASTERN_DESIGN.get(eastern_region, {})
    eastern_colors = list(eastern_data.get('colors', {}).items())[:2]
    
    # 西方元素
    western_data = WESTERN_MASTERS.get(western_style, {})
    western_colors = list(western_data.get('colors', {}).items())[:2]
    
    # 中国元素
    chinese_patterns = list(CHINESE_CLASSICAL['patterns'].items())[:2]
    chinese_colors = list(CHINESE_CLASSICAL['colors'].items())[:2]
    
    card = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                               ┃
┃  🌸 设计卡片 · DESIGN CARD                     权重 80/20  ┃
┃                                                               ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                               ┃
┃  【东方西方 80%】                                             ┃
┃                                                               ┃
┃  🇯🇵 东方 ({eastern_region}):                                     ┃
┃     {', '.join([f"{v['name']}({v['hex']})" for k, v in eastern_colors])}
┃                                                               ┃
┃  🇪🇺 西方 ({western_style}):                                     ┃
┃     {', '.join([f"{v['name']}({v['hex']})" for k, v in western_colors])}
┃                                                               ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                               ┃
┃  【中国 20%】                                                 ┃
┃                                                               ┃
┃  🇨🇳 纹样：{' '.join([f"{v['emoji']}{v['name']}" for k, v in chinese_patterns])}
┃  🇨🇳 色彩：{', '.join([f"{v['name']}({v['hex']})" for k, v in chinese_colors])}
┃                                                               ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                               ┃
┃  {content[:65]:<65}  ┃
┃  {content[65:130]:<65}                  ┃
┃                                                               ┃
┃  设计原则：东方西方大师灵感 80% + 中国元素 20%                ┃
┃                                                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    
    return card


def generate_showcase():
    """生成设计卡片展示"""
    
    showcase = f"""# 🎨 艺术设计系统 - 卡片效果印证

> **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
> **系统**: 太一 AGI · 艺术设计系统  
> **原则**: 东方西方 80% + 中国 20%

---

## 📍 场景权重配置

| 场景 | 东方西方 | 中国 |
|------|---------|------|
"""
    
    for scene_key, scene_config in SCENE_CONFIGS.items():
        weight = scene_config['weight']
        showcase += f"| {scene_config['name']} | {weight['eastern_western']:.0%} | {weight['chinese']:.0%} |\n"
    
    showcase += """
---

## 🇯🇵🇹🇼🇭🇰🇸🇬🇹🇭 东方设计卡片

"""
    
    # 日本卡片
    showcase += generate_eastern_card(
        'japan',
        '禅意美学 · 侘寂之道 · 间 (Ma) 的留白艺术 · 渋い的低调优雅'
    )
    
    # 台湾卡片
    showcase += generate_eastern_card(
        'taiwan',
        '夜市文化 · 茶文化 · 庙宇文化 · 街头设计的活力与丰富'
    )
    
    # 香港卡片
    showcase += generate_eastern_card(
        'hong_kong',
        '霓虹文化 · 维港夜景 · 点心文化 · 现代都市的垂直美学'
    )
    
    # 新加坡卡片
    showcase += generate_eastern_card(
        'singapore',
        '花园城市 · 多元融合 · 生态和谐 · 现代规划与自然共生'
    )
    
    # 泰国卡片
    showcase += generate_eastern_card(
        'thailand',
        '佛教艺术 · 传统工艺 · 美食文化 · 华丽庄严的寺庙美学'
    )
    
    showcase += """
---

## 🇪🇺 西方设计卡片

"""
    
    # 包豪斯卡片
    showcase += generate_western_card(
        'bauhaus',
        '形式追随功能 · 少即是多 · 理性主义 · 现代设计的奠基者'
    )
    
    # 瑞士卡片
    showcase += generate_western_card(
        'swiss',
        '网格系统 · 秩序产生美 · 严谨专业 · 国际主义平面设计'
    )
    
    # 苹果卡片
    showcase += generate_western_card(
        'apple',
        '简约是终极的复杂 · 极致工艺 · 用户体验至上 · 科技与艺术结合'
    )
    
    # 材料设计卡片
    showcase += generate_western_card(
        'material',
        '数字世界的纸与墨 · 卡片层次 · 动画反馈 · 现代 UI 设计语言'
    )
    
    showcase += """
---

## 🇨🇳 中国经典设计卡片

"""
    
    showcase += generate_chinese_card(
        '天青色等烟雨 · 雨过天青云破处 · 传统色彩的意境之美 · 云纹莲花竹子山峦'
    )
    
    showcase += """
---

## 🌐 融合设计卡片 (东方西方 80% + 中国 20%)

"""
    
    # 融合卡片 1
    showcase += generate_fusion_card(
        'japan',
        'swiss',
        '学习报告设计 · 日本禅意 + 瑞士网格 · 留白与秩序的完美结合 · 现代学术美学'
    )
    
    # 融合卡片 2
    showcase += generate_fusion_card(
        'singapore',
        'apple',
        '商业报告设计 · 花园城市 + 苹果极简 · 生态与科技的融合 · 现代商务美学'
    )
    
    # 融合卡片 3
    showcase += generate_fusion_card(
        'hong_kong',
        'material',
        '技术文档设计 · 霓虹都市 + 材料设计 · 活力与层次的结合 · 现代技术美学'
    )
    
    showcase += f"""
---

## 📊 设计元素统计

### 东方设计元素
- **地区**: 5 个 (日本/台湾/香港/新加坡/泰国)
- **色彩**: 15+ 种
- **布局**: 5+ 种
- **原则**: 10+ 种

### 西方设计元素
- **风格**: 4 个 (包豪斯/瑞士/苹果/材料)
- **色彩**: 10+ 种
- **布局**: 4+ 种
- **原则**: 4+ 种

### 中国经典元素
- **色彩**: 5 种 (天青/朱砂/黛蓝/月白/墨色)
- **纹样**: 4 种 (云纹/莲花/竹子/山峦)
- **布局**: 2 种 (经典/双重)

### 总变化数
根据场景权重动态组合，**每份报告都是独特的融合艺术设计**!

---

## 🎯 设计原则

> **东方（台湾、香港、新加坡、日本、泰国等）西方设计大师的灵感占比 80%**

- 日本：禅意/侘寂/间美学/渋い
- 台湾：街头文化/茶文化/庙宇文化
- 香港：霓虹文化/都市美学/饮茶文化
- 新加坡：花园城市/多元融合/生态和谐
- 泰国：佛教艺术/传统工艺/美食文化
- 西方：包豪斯/瑞士/苹果/材料设计

> **中国元素占比 20%**

- 传统色彩体系
- 传统纹样寓意
- 传统布局美学

> **特殊情况下可以根据事件和场景进行调整**

- 传统节日：中国元素 +30%
- 国际活动：东方西方 +10%
- 场景感知：自动调整权重
- 用户偏好：学习优化

---

*卡片生成：太一 AGI · 艺术设计系统*  
*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    return showcase


def main():
    """主函数"""
    print("🎨 生成设计卡片展示...")
    print("="*60)
    print()
    
    # 生成展示
    showcase = generate_showcase()
    
    # 保存文件
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        f.write(showcase)
    
    print(f"✅ 设计卡片已生成")
    print(f"   文件：{CARDS_FILE}")
    print(f"   大小：{len(showcase)} 字符")
    print()
    
    # 打印预览
    print("📄 卡片预览 (前 2000 字符):")
    print("="*60)
    print(showcase[:2000] + "..." if len(showcase) > 2000 else showcase)
    print()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
