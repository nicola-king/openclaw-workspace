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

from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"
CARDS_FILE = REPORTS_DIR / "design-cards-showcase.md"


# ═══════════════════════════════════════════════════════════
# 东方设计元素
# ═══════════════════════════════════════════════════════════

EASTERN_DESIGN = {
    'japan': {
        'name': '日本',
        'colors': {
            'sakura_pink': {'name': '樱花粉', 'hex': '#FFB7C5'},
            'matcha_green': {'name': '抹茶绿', 'hex': '#7D8447'},
            'indigo_blue': {'name': '靛蓝', 'hex': '#1E3A5F'}
        },
        'principles': ['间 (Ma)', '侘寂', '渋い']
    },
    'taiwan': {
        'name': '台湾',
        'colors': {
            'night_market': {'name': '夜市红', 'hex': '#E74C3C'},
            'tea_green': {'name': '乌龙茶绿', 'hex': '#6B8E23'},
            'temple_gold': {'name': '庙宇金', 'hex': '#FFD700'}
        },
        'principles': ['街头文化', '茶文化', '庙宇文化']
    },
    'hong_kong': {
        'name': '香港',
        'colors': {
            'neon_pink': {'name': '霓虹粉', 'hex': '#FF1493'},
            'harbor_blue': {'name': '维港蓝', 'hex': '#4682B4'},
            'dim_sum_gold': {'name': '点心金', 'hex': '#FFA500'}
        },
        'principles': ['霓虹文化', '都市美学', '饮茶文化']
    },
    'singapore': {
        'name': '新加坡',
        'colors': {
            'merlion_gold': {'name': '鱼尾狮金', 'hex': '#FFD700'},
            'garden_green': {'name': '花园绿', 'hex': '#228B22'},
            'orchid_purple': {'name': '胡姬紫', 'hex': '#9370DB'}
        },
        'principles': ['花园城市', '多元融合', '生态和谐']
    },
    'thailand': {
        'name': '泰国',
        'colors': {
            'temple_gold': {'name': '寺庙金', 'hex': '#FFD700'},
            'silk_purple': {'name': '泰丝紫', 'hex': '#8B008B'},
            'food_orange': {'name': '泰餐橙', 'hex': '#FF8C00'}
        },
        'principles': ['佛教艺术', '传统工艺', '美食文化']
    }
}


# ═══════════════════════════════════════════════════════════
# 西方大师设计元素
# ═══════════════════════════════════════════════════════════

WESTERN_MASTERS = {
    'bauhaus': {
        'name': '包豪斯',
        'colors': {
            'red': {'name': '包豪斯红', 'hex': '#E03C31'},
            'blue': {'name': '包豪斯蓝', 'hex': '#00A3E0'},
            'yellow': {'name': '包豪斯黄', 'hex': '#FFD700'}
        },
        'masters': ['Walter Gropius', 'Kandinsky'],
        'principles': ['形式追随功能', '少即是多']
    },
    'swiss': {
        'name': '瑞士',
        'colors': {
            'red': {'name': '瑞士红', 'hex': '#FF0000'},
            'black': {'name': '瑞士黑', 'hex': '#000000'}
        },
        'masters': ['Josef Müller-Brockmann'],
        'principles': ['网格系统', '秩序产生美']
    },
    'apple': {
        'name': '苹果',
        'colors': {
            'gray': {'name': '苹果灰', 'hex': '#8E8E93'},
            'white': {'name': '苹果白', 'hex': '#FFFFFF'},
            'silver': {'name': '苹果银', 'hex': '#C0C0C0'}
        },
        'masters': ['Jony Ive'],
        'principles': ['简约是终极的复杂']
    },
    'material': {
        'name': '材料设计',
        'colors': {
            'blue': {'name': '材料蓝', 'hex': '#2196F3'},
            'teal': {'name': '材料青', 'hex': '#009688'}
        },
        'masters': ['Google Design'],
        'principles': ['数字世界的纸与墨']
    }
}


# ═══════════════════════════════════════════════════════════
# 中国经典设计元素
# ═══════════════════════════════════════════════════════════

CHINESE_CLASSICAL = {
    'colors': {
        'sky_blue': {'name': '天青', 'hex': '#87CEEB', 'era': '宋'},
        'cinnabar': {'name': '朱砂', 'hex': '#E60000', 'era': '汉'},
        'indigo': {'name': '黛蓝', 'hex': '#4A5C8C', 'era': '唐'},
        'moon_white': {'name': '月白', 'hex': '#D6ECF0', 'era': '明'},
        'ink': {'name': '墨色', 'hex': '#2C2C2C', 'era': '先秦'}
    },
    'patterns': {
        'cloud': {'name': '云纹', 'emoji': '☁️'},
        'lotus': {'name': '莲花', 'emoji': '🪷'},
        'bamboo': {'name': '竹子', 'emoji': '🎋'},
        'mountain': {'name': '山峦', 'emoji': '⛰️'}
    }
}


# ═══════════════════════════════════════════════════════════
# 场景权重配置
# ═══════════════════════════════════════════════════════════

SCENE_WEIGHTS = {
    '学习报告': {'eastern_western': 0.80, 'chinese': 0.20},
    '技术文档': {'eastern_western': 0.90, 'chinese': 0.10},
    '艺术报告': {'eastern_western': 0.70, 'chinese': 0.30},
    '商业报告': {'eastern_western': 0.85, 'chinese': 0.15},
    '创意作品': {'eastern_western': 0.75, 'chinese': 0.25}
}


def generate_header():
    """生成头部"""
    return f"""
```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🎨 艺术设计系统 - 卡片效果印证                            ║
║     DESIGN SYSTEM - CARD SHOWCASE                             ║
║                                                               ║
║     生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                            ║
║     系统：太一 AGI · 艺术设计系统                              ║
║     原则：东方西方 80% + 中国 20%                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```
"""


def generate_scene_weight_table():
    """生场场景权重表"""
    table = """
## 📍 场景权重配置

| 场景 | 东方西方 | 中国 |
|------|---------|------|
"""
    for scene, weight in SCENE_WEIGHTS.items():
        table += f"| {scene} | {weight['eastern_western']:.0%} | {weight['chinese']:.0%} |\n"
    
    return table


def generate_eastern_card(region):
    """生成东方风格卡片"""
    data = EASTERN_DESIGN.get(region, {})
    
    colors = list(data.get('colors', {}).values())[:3]
    color_line = " · ".join([f"{c['name']}({c['hex']})" for c in colors])
    
    principles = data.get('principles', [])[:3]
    principle_line = " · ".join(principles)
    
    patterns = {'japan': '🌸', 'taiwan': '🏮', 'hong_kong': '🌃', 'singapore': '🦁', 'thailand': '🛕'}
    pattern = patterns.get(region, '✨')
    
    card = f"""
{pattern * 32}
{pattern}  🎨 东方设计 · {data.get('name', region).upper():<20}                      {pattern}
{pattern}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  {pattern}
{pattern}                                                           {pattern}
{pattern}  代表色彩                                                 {pattern}
{pattern}  {color_line:<60}  {pattern}
{pattern}                                                           {pattern}
{pattern}  设计原则：{principle_line:<50}  {pattern}
{pattern}                                                           {pattern}
{pattern}  灵感来源：{region} 东方美学                              {pattern}
{pattern}                                                           {pattern}
{pattern * 32}
"""
    return card


def generate_western_card(style):
    """生成西方风格卡片"""
    data = WESTERN_MASTERS.get(style, {})
    
    colors = list(data.get('colors', {}).values())[:3]
    color_line = " · ".join([f"{c['name']}({c['hex']})" for c in colors])
    
    masters = data.get('masters', [])[:2]
    master_line = ", ".join(masters)
    
    principles = data.get('principles', [])[:2]
    principle_line = " · ".join(principles)
    
    card = f"""
┌───────────────────────────────────────────────────────────────┐
│  🎨 西方设计 · {data.get('name', style).upper():<20}                       │
│                                                               │
│  ───────────────────────────────────────────────────────────  │
│                                                               │
│  代表色彩：{color_line:<50}                  │
│                                                               │
│  设计大师：{master_line:<50}                  │
│  设计原则：{principle_line:<50}                  │
│                                                               │
│  ───────────────────────────────────────────────────────────  │
│                                                               │
│  灵感来源：{style} 西方现代设计                              │
│                                                               │
└───────────────────────────────────────────────────────────────┘
"""
    return card


def generate_chinese_card():
    """生成中国风格卡片"""
    colors = list(CHINESE_CLASSICAL['colors'].values())[:5]
    color_line = " · ".join([f"{c['name']}({c['hex']})" for c in colors])
    
    patterns = list(CHINESE_CLASSICAL['patterns'].values())
    pattern_line = " ".join([f"{p['emoji']}{p['name']}" for p in patterns])
    
    card = f"""
╭───────────────────────────────────────────────────────────────╮
│  {pattern_line}  │
│  🎨 中国经典设计 · CHINESE CLASSICAL                          │
│  {pattern_line}  │
│                                                               │
│  ═══════════════════════════════════════════════════════════  │
│                                                               │
│  传统色彩：{color_line:<50}                     │
│                                                               │
│  传统纹样：云纹 · 莲花 · 竹子 · 山峦                          │
│  设计原则：天人合一 · 道法自然                                │
│                                                               │
│  ═══════════════════════════════════════════════════════════  │
│                                                               │
│  灵感来源：中国传统美学                                      │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
"""
    return card


def generate_fusion_card(eastern_region, western_style):
    """生成融合风格卡片 (东方西方 80% + 中国 20%)"""
    
    eastern_data = EASTERN_DESIGN.get(eastern_region, {})
    eastern_colors = list(eastern_data.get('colors', {}).values())[:2]
    eastern_principles = eastern_data.get('principles', [])[:2]
    
    western_data = WESTERN_MASTERS.get(western_style, {})
    western_colors = list(western_data.get('colors', {}).values())[:2]
    western_masters = western_data.get('masters', [])[:1]
    western_principles = western_data.get('principles', [])[:1]
    
    chinese_patterns = list(CHINESE_CLASSICAL['patterns'].values())[:2]
    chinese_colors = list(CHINESE_CLASSICAL['colors'].values())[:2]
    
    eastern_color_str = ', '.join([f"{c['name']}({c['hex']})" for c in eastern_colors])
    western_color_str = ', '.join([f"{c['name']}({c['hex']})" for c in western_colors])
    chinese_pattern_str = ' '.join([f"{p['emoji']}{p['name']}" for p in chinese_patterns])
    chinese_color_str = ', '.join([f"{c['name']}({c['hex']})" for c in chinese_colors])
    
    card = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🌸 融合设计卡片 · FUSION CARD                   权重 80/20  ┃
┃                                                               ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                               ┃
┃  【东方西方 80%】                                             ┃
┃                                                               ┃
┃  🇯🇵 东方 ({eastern_region}):                                     ┃
┃     色彩：{eastern_color_str:<52}     ┃
┃     原则：{', '.join(eastern_principles):<52}     ┃
┃                                                               ┃
┃  🇪🇺 西方 ({western_style}):                                     ┃
┃     色彩：{western_color_str:<52}     ┃
┃     大师：{', '.join(western_masters):<52}     ┃
┃     原则：{', '.join(western_principles):<52}     ┃
┃                                                               ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                               ┃
┃  【中国 20%】                                                 ┃
┃                                                               ┃
┃  🇨🇳 纹样：{chinese_pattern_str:<54}     ┃
┃  🇨🇳 色彩：{chinese_color_str:<54}     ┃
┃                                                               ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                               ┃
┃  设计案例：{eastern_region}+{western_style}+ 中国                              ┃
┃  应用场景：学习报告/商业文档/创意作品                        ┃
┃                                                               ┃
┃  设计原则：东方西方大师灵感 80% + 中国元素 20%                ┃
┃                                                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    return card


def generate_statistics():
    """生成统计信息"""
    return """
## 📊 设计元素统计

### 东方设计元素
- **地区**: 5 个 (日本/台湾/香港/新加坡/泰国)
- **色彩**: 15+ 种
- **原则**: 10+ 种

### 西方设计元素
- **风格**: 4 个 (包豪斯/瑞士/苹果/材料)
- **色彩**: 10+ 种
- **大师**: 5+ 位
- **原则**: 4+ 种

### 中国经典元素
- **色彩**: 5 种 (天青/朱砂/黛蓝/月白/墨色)
- **纹样**: 4 种 (云纹/莲花/竹子/山峦)
- **原则**: 2 种 (天人合一/道法自然)

### 总变化数
根据场景权重动态组合，**每份报告都是独特的融合艺术设计**!
"""


def generate_principles():
    """生成设计原则"""
    return """
## 🎯 设计原则

> **东方（台湾、香港、新加坡、日本、泰国等）西方设计大师的灵感占比 80%**

- 🇯🇵 日本：禅意/侘寂/间 (Ma)/渋い
- 🇹🇼 台湾：街头文化/茶文化/庙宇文化
- 🇭🇰 香港：霓虹文化/都市美学/饮茶文化
- 🇸🇬 新加坡：花园城市/多元融合/生态和谐
- 🇹🇭 泰国：佛教艺术/传统工艺/美食文化
- 🇪🇺 西方：包豪斯/瑞士/苹果/材料设计

> **中国元素占比 20%**

- 🇨🇳 传统色彩体系
- 🇨🇳 传统纹样寓意
- 🇨🇳 传统布局美学

> **特殊情况下可以根据事件和场景进行调整**

- 传统节日：中国元素 +30%
- 国际活动：东方西方 +10%
- 场景感知：自动调整权重
- 用户偏好：学习优化
"""


def generate_showcase():
    """生成完整展示"""
    
    showcase = f"""# 🎨 艺术设计系统 - 卡片效果印证

> **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
> **系统**: 太一 AGI · 艺术设计系统  
> **原则**: 东方西方 80% + 中国 20%

---

{generate_header()}

---

{generate_scene_weight_table()}

---

## 🇯🇵🇹🇼🇭🇰🇸🇬🇹🇭 东方设计卡片

"""
    
    # 东方卡片
    for region in ['japan', 'taiwan', 'hong_kong', 'singapore', 'thailand']:
        showcase += generate_eastern_card(region)
    
    showcase += """
---

## 🇪🇺 西方设计卡片

"""
    
    # 西方卡片
    for style in ['bauhaus', 'swiss', 'apple', 'material']:
        showcase += generate_western_card(style)
    
    showcase += """
---

## 🇨🇳 中国经典设计卡片

"""
    
    showcase += generate_chinese_card()
    
    showcase += """
---

## 🌐 融合设计卡片 (东方西方 80% + 中国 20%)

"""
    
    # 融合卡片
    fusion_pairs = [
        ('japan', 'swiss', '学习报告'),
        ('singapore', 'apple', '商业报告'),
        ('hong_kong', 'material', '技术文档')
    ]
    
    for eastern, western, usage in fusion_pairs:
        showcase += f"### {usage}: {eastern} + {western}\n\n"
        showcase += generate_fusion_card(eastern, western)
        showcase += "\n"
    
    showcase += generate_statistics()
    showcase += generate_principles()
    
    showcase += f"""
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
    CARDS_FILE.parent.mkdir(exist_ok=True)
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
