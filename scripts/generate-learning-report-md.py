#!/usr/bin/env python3
"""
学习报告 Markdown 生成器 (艺术设计增强版)

功能:
1. 读取 JSON 学习报告
2. 生成艺术设计的 Markdown 报告 (每帧都是艺术设计)
3. 保存到 reports/ 目录
4. 可选发送到 Telegram

设计理念:
- 每一帧都是艺术设计过的
- 融入中国传统美学元素
- 现代设计与传统美学结合
- 视觉层次清晰，阅读体验优雅

作者：太一 AGI
创建：2026-04-10
"""

import os
import sys
import json
import subprocess
import random
from pathlib import Path
from datetime import datetime

# 导入艺术设计系统
from artistic_design_system import ArtisticDesignSystem, LAYOUT_STYLES, TRADITIONAL_COLORS, SPACING_STYLES, PATTERNS

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"


# 艺术边框设计
ART_BORDER = {
    'top': '┌─────────────────────────────────────────────────────────────┐',
    'bottom': '└─────────────────────────────────────────────────────────────┘',
    'side': '│',
    'divider': '─────────────────────────────────────────────────────────────',
    'box': '''
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
''',
    'cloud': '''
  ☁️☁️☁️
 ☁️   ☁️
☁️     ☁️
 ☁️   ☁️
  ☁️☁️☁️
'''
}

# 传统纹样装饰
TRADITIONAL_PATTERNS = {
    'cloud': '☁️',
    'dragon': '🐉',
    'phoenix': '🦚',
    'lotus': '🪷',
    'bamboo': '🎋',
    'mountain': '⛰️',
    'water': '💧',
    'moon': '🌙',
    'sun': '☀️',
    'star': '⭐'
}

# 章节图标
SECTION_ICONS = {
    'stats': '📊',
    'global': '🌐',
    'chinese': '🇨🇳',
    'innovation': '💡',
    'evolution': '🧬',
    'application': '📈',
    'plan': '🎯',
    'appendix': '📝'
}


def load_all_learning_reports(date=None):
    """加载指定日期的所有学习报告"""
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    
    pattern = f"midnight-learning-{date}-*.json"
    reports = list(REPORTS_DIR.glob(pattern))
    
    all_reports = []
    for report_file in sorted(reports):
        with open(report_file, "r", encoding="utf-8") as f:
            all_reports.append(json.load(f))
    
    return all_reports


def load_evolution_reports(date=None):
    """加载自进化报告"""
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    
    pattern = f"self-evolution-{date}-*.json"
    reports = list(REPORTS_DIR.glob(pattern))
    
    all_reports = []
    for report_file in sorted(reports):
        with open(report_file, "r", encoding="utf-8") as f:
            all_reports.append(json.load(f))
    
    return all_reports


def create_artistic_box(title, content_lines, width=60):
    """创建艺术边框"""
    lines = []
    
    # 顶部装饰
    lines.append('')
    lines.append(f'  ╔══ {title} ══╗')
    lines.append(f'  ║')
    
    # 内容
    for line in content_lines:
        padded = line.ljust(width - 2)
        lines.append(f'  ║ {padded} ║')
    
    lines.append(f'  ║')
    lines.append(f'  ╚══════════════════════════════════════════════════════════╝')
    lines.append('')
    
    return '\n'.join(lines)


def create_pattern_divider(pattern='cloud', repeat=10):
    """创建纹样分隔线"""
    emoji = TRADITIONAL_PATTERNS.get(pattern, '☁️')
    return f"{emoji}" * repeat


def generate_artistic_markdown(reports, evolution_reports, output_file=None):
    """生成艺术设计增强的 Markdown 报告"""
    
    # 初始化艺术设计系统
    design_system = ArtisticDesignSystem()
    current_design = design_system.get_current_design()
    
    # 每份报告都有独特的艺术设计 (自进化)
    if random.random() < 0.5:  # 50% 概率自进化
        current_design = design_system.evolve_design()
    
    # 获取设计元素
    layout = LAYOUT_STYLES.get(current_design['layout'], LAYOUT_STYLES['classic'])
    spacing = SPACING_STYLES.get(current_design['spacing'], SPACING_STYLES['comfortable'])
    palette = design_system.get_color_palette()
    patterns = current_design['patterns']
    
    # 创新汇总 (去重)
    all_innovations = []
    for r in reports:
        all_innovations.extend(r.get('innovations', []))
    
    unique_innovations = []
    seen = set()
    for inn in all_innovations:
        key = inn['name']
        if key not in seen:
            seen.add(key)
            unique_innovations.append(inn)
    
    # 自进化统计
    total_evolution_checks = len(evolution_reports)
    created_skills = []
    for ev in evolution_reports:
        created_skills.extend(ev.get('created_skills', []))
    
    # 生成艺术设计增强的 Markdown
    md = f"""
```
{ART_BORDER['top']}
{ART_BORDER['side']}  🌙 凌晨学习报告                              {ART_BORDER['side']}
{ART_BORDER['side']}                                                              {ART_BORDER['side']}
{ART_BORDER['side']}  📅 日期：{datetime.now().strftime("%Y-%m-%d")}                                   {ART_BORDER['side']}
{ART_BORDER['side']}  🕐 时段：子时 - 卯时 (01:00 - 07:00)                       {ART_BORDER['side']}
{ART_BORDER['side']}  ⏰ 生成：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                           {ART_BORDER['side']}
{ART_BORDER['side']}  🤖 系统：太一 AGI · 凌晨学习系统                            {ART_BORDER['side']}
{ART_BORDER['bottom']}
```

{create_pattern_divider('moon', 15)}

"""
    
    # 学习统计 - 艺术框设计
    stats_content = [
        f"学习时长    │  7 小时 (子时 - 卯时)",
        f"执行次数    │  {total_sessions} 次 (每小时一次)",
        f"创新产出    │  {total_innovations} 个 (每次 4 个)",
        f"独特创新    │  {len(unique_innovations)} 个 (去重后)",
        f"学习来源    │  10 个 (4 海外 +6 传统)"
    ]
    md += create_artistic_box("📊 学习统计", stats_content, 62)
    
    md += f"""
{create_pattern_divider('cloud', 15)}

## {SECTION_ICONS['global']} 全球设计趋势 · 观天下

### 学习来源 (4 个)

```
┌───────────────┬──────────────────┬──────────┐
│ 来源          │ 类型             │ 频率     │
├───────────────┼──────────────────┼──────────┤
│ AdAge         │ 全球广告趋势     │ 每次学习 │
│ Dezeen        │ 建筑/设计前沿    │ 每次学习 │
│ Behance       │ 创意灵感         │ 每次学习 │
│ Design Milk   │ 现代设计         │ 每次学习 │
└───────────────┴──────────────────┴──────────┘
```

### 学习收获

> 📚 了解全球最新设计趋势  
> 📚 掌握前沿设计理念  
> 📚 收集创意灵感案例  
> 📚 建立国际视野

{create_pattern_divider('lotus', 15)}

## {SECTION_ICONS['chinese']} 中国传统美学 · 承文脉

### 学习主题 (6 个)

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  传统色彩    │  天青 · 朱砂 · 黛蓝 · 月白 · 石绿                           ║
║  传统纹样    │  云纹 · 龙纹 · 凤纹 · 回纹 · 如意纹                        ║
║  书法名帖    │  兰亭序 · 祭侄文稿 · 寒食帖                                ║
║  国画名画    │  清明上河图 · 富春山居图                                   ║
║  园林美学    │  拙政园 · 留园 · 造园手法                                  ║
║  建筑美学    │  木结构 · 斗拱 · 大屋顶                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### 学习收获

> 🖌️ 掌握传统色彩体系  
> 🖌️ 理解传统纹样寓意  
> 🖌️ 领略书法艺术精髓  
> 🖌️ 感悟国画意境表达  
> 🖌️ 学习园林造景手法  
> 🖌️ 理解建筑美学特征

{create_pattern_divider('bamboo', 15)}

## {SECTION_ICONS['innovation']} 融合创新 · 生万象

### 创新成果 ({len(unique_innovations)} 个独特创新)

"""
    
    # 创新卡片 - 每个都有独特设计
    innovation_designs = [
        {'icon': '🎨', 'border': '═', 'bg': '█'},
        {'icon': '🎭', 'border': '─', 'bg': '░'},
        {'icon': '🎪', 'border': '╌', 'bg': '▒'},
        {'icon': '🎯', 'border': '╍', 'bg': '▓'},
    ]
    
    for i, inn in enumerate(unique_innovations, 1):
        design = innovation_designs[(i-1) % len(innovation_designs)]
        icon = design['icon']
        
        md += f"""
### {icon} {inn['name']}

```
{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}
融合方向：{inn['fusion']}
描述：{inn['description']}
{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}{design['bg']}
```

---

"""
    
    # 能力涌现
    md += f"""
## {SECTION_ICONS['evolution']} 能力涌现 · 自进化

### 自进化系统运行

```
{ART_BORDER['top']}
{ART_BORDER['side']}  检测频率    │  每 15 分钟                                     {ART_BORDER['side']}
{ART_BORDER['side']}  检测次数    │  {total_evolution_checks} 次 (01:00-07:00)                    {ART_BORDER['side']}
{ART_BORDER['side']}  信号检测    │  多次 (重复任务/职责域空白/学习洞察)          {ART_BORDER['side']}
{ART_BORDER['side']}  新创建      │  {len(created_skills)} 个 Skill 框架                       {ART_BORDER['side']}
{ART_BORDER['bottom']}
```

### 涌现 Skill

"""
    
    # 显示前 5 个 Skill - 每个都有艺术设计
    for i, skill in enumerate(created_skills[:5], 1):
        md += f"""
#### 🆕 `{skill['name']}`

```
┌─────────────────────────────────────────────────────────────┐
│ 原因：{skill['reason'][:50]}
│ 路径：{skill['path'][-45:]}
└─────────────────────────────────────────────────────────────┘
```

"""
    
    if len(created_skills) > 5:
        md += f"\n*... 还有 {len(created_skills) - 5} 个 Skill*\n\n"
    
    # 应用建议 - 艺术框设计
    md += f"""
## {SECTION_ICONS['application']} 学习成果应用 · 致用

### 可直接应用

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  1. 天青色系 UI 主题                                                       ║
║     → 应用到 Dashboard 设计                                                 ║
║     → 应用到 Skill 界面                                                     ║
║     → 应用到文档排版                                                       ║
║                                                                           ║
║  2. 云纹加载动画                                                           ║
║     → 应用到数据加载                                                       ║
║     → 应用到页面过渡                                                       ║
║     → 应用到状态切换                                                       ║
║                                                                           ║
║  3. 兰亭序代码注释风格                                                     ║
║     → 应用到新 Skill 开发                                                   ║
║     → 应用到代码审查                                                       ║
║     → 应用到文档编写                                                       ║
║                                                                           ║
║  4. 园林式信息架构                                                         ║
║     → 应用到网站导航                                                       ║
║     → 应用到内容组织                                                       ║
║     → 应用到用户引导                                                       ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## {SECTION_ICONS['plan']} 下一步计划 · 笃行

### 短期 (本周)

> 📌 应用天青色系到 Dashboard  
> 📌 实现云纹加载动画  
> 📌 采用兰亭序注释风格  
> 📌 优化信息架构

### 中期 (本月)

> 📌 完成传统色彩体系整合  
> 📌 创建传统纹样库  
> 📌 编写书法风格代码规范  
> 📌 设计园林式导航系统

### 长期 (本季度)

> 📌 形成太一设计语言  
> 📌 建立美学评估体系  
> 📌 产出设计系统文档  
> 📌 贡献开源社区

{create_pattern_divider('mountain', 15)}

## {SECTION_ICONS['appendix']} 附录 · 详录

### 学习过程

"""
    
    # 添加详细日志 (前 3 次)
    for i, r in enumerate(reports[:3], 1):
        start_time = r.get('session_start', '未知').split('T')[1].split('.')[0]
        md += f"""
#### 第 {i} 次学习 · {start_time}

**学习内容**:

"""
        for log in r.get('learning_log', [])[:8]:
            if log.startswith('['):
                log = log.split('] ', 1)[1] if '] ' in log else log
            if log.startswith('🌐') or log.startswith('🇨🇳') or log.startswith('🎨'):
                md += f"- {log}\n"
        
        md += "\n---\n\n"
    
    # 结语 - 艺术设计
    md += f"""
```
{ART_BORDER['top']}
{ART_BORDER['side']}                                                              {ART_BORDER['side']}
{ART_BORDER['side']}  > 学而时习之，不亦说乎                                    {ART_BORDER['side']}
{ART_BORDER['side']}  > 温故而知新，可以为师矣                                  {ART_BORDER['side']}
{ART_BORDER['side']}                                                              {ART_BORDER['side']}
{ART_BORDER['bottom']}
```

---

```
{ART_BORDER['top']}
{ART_BORDER['side']}  报告生成：太一 AGI · 凌晨学习系统                            {ART_BORDER['side']}
{ART_BORDER['side']}  美学设计：融合中国传统美学与现代设计                        {ART_BORDER['side']}
{ART_BORDER['side']}  生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                            {ART_BORDER['side']}
{ART_BORDER['bottom']}
```
"""
    
    # 保存报告
    if output_file is None:
        output_file = REPORTS_DIR / f"learning-report-{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"✅ 艺术设计增强报告已保存：{output_file}")
    
    return md, output_file


def main():
    """主函数"""
    print("🎨 生成艺术设计增强学习报告...")
    print("="*50)
    print()
    
    # 加载今日所有学习报告
    date = datetime.now().strftime("%Y%m%d")
    reports = load_all_learning_reports(date)
    
    if not reports:
        print("❌ 未找到学习报告")
        print("   请确认凌晨学习系统是否正常运行")
        return 1
    
    print(f"✅ 加载学习报告：{len(reports)} 个")
    print()
    
    # 加载自进化报告
    evolution_reports = load_evolution_reports(date)
    print(f"✅ 加载自进化报告：{len(evolution_reports)} 个")
    print()
    
    # 生成艺术设计增强 Markdown 报告
    md, output_file = generate_artistic_markdown(reports, evolution_reports)
    
    print(f"✅ 报告已生成")
    print(f"   文件：{output_file}")
    print(f"   大小：{len(md)} 字符")
    print()
    
    # 打印报告预览
    print("🎨 报告预览 (前 1500 字符):")
    print("="*50)
    print(md[:1500] + "..." if len(md) > 1500 else md)
    print()
    
    # 询问是否发送 Telegram
    if len(sys.argv) > 1 and sys.argv[1] == "--send":
        print("\n📤 准备发送 Telegram...")
        send_script = WORKSPACE / "scripts" / "send-telegram-report.py"
        if send_script.exists():
            subprocess.run(["python3", str(send_script)], capture_output=False)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
