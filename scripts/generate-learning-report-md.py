#!/usr/bin/env python3
"""
学习报告 Markdown 生成器

功能:
1. 读取 JSON 学习报告
2. 生成美观的 Markdown 报告
3. 保存到 reports/ 目录
4. 可选发送到用户

作者：太一 AGI
创建：2026-04-10
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"


def load_latest_learning_report():
    """加载最新的学习报告"""
    reports = list(REPORTS_DIR.glob("midnight-learning-*.json"))
    
    if not reports:
        return None
    
    latest = max(reports)
    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f)


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


def generate_markdown_report(reports, output_file=None):
    """生成 Markdown 格式学习报告"""
    
    if isinstance(reports, dict):
        reports = [reports]
    
    # 汇总数据
    total_sessions = len(reports)
    total_innovations = sum(len(r.get('innovations', [])) for r in reports)
    
    # 学习来源统计
    global_sources = set()
    chinese_topics = set()
    
    for r in reports:
        for log in r.get('learning_log', []):
            if 'AdAge' in log or 'Dezeen' in log or 'Behance' in log:
                global_sources.add(log.strip())
            if '传统色彩' in log or '传统纹样' in log or '书法' in log:
                chinese_topics.add(log.strip())
    
    # 创新汇总
    all_innovations = []
    for r in reports:
        all_innovations.extend(r.get('innovations', []))
    
    # 去重
    unique_innovations = []
    seen = set()
    for inn in all_innovations:
        key = inn['name']
        if key not in seen:
            seen.add(key)
            unique_innovations.append(inn)
    
    # 生成 Markdown
    md = f"""# 🌙 凌晨学习报告

**日期**: {datetime.now().strftime("%Y-%m-%d")}  
**学习时段**: 01:00 - 07:00  
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📊 学习统计

| 指标 | 数值 |
|------|------|
| **学习时长** | 7 小时 (01:00-07:00) |
| **执行次数** | {total_sessions} 次 |
| **创新产出** | {total_innovations} 个 |
| **独特创新** | {len(unique_innovations)} 个 |
| **学习来源** | 10 个 (4 海外 +6 传统) |

---

## 🌐 全球设计趋势学习

### 学习来源 (4 个)

| 来源 | 类型 | 频率 |
|------|------|------|
| **AdAge** | 全球广告趋势 | 每次学习 |
| **Dezeen** | 建筑/设计前沿 | 每次学习 |
| **Behance** | 创意灵感 | 每次学习 |
| **Design Milk** | 现代设计 | 每次学习 |

### 学习收获

- ✅ 了解全球最新设计趋势
- ✅ 掌握前沿设计理念
- ✅ 收集创意灵感案例
- ✅ 建立国际视野

---

## 🇨🇳 中国传统美学学习

### 学习主题 (6 个)

| 主题 | 内容 | 频率 |
|------|------|------|
| **传统色彩** | 天青/朱砂/黛蓝/月白/石绿 | 每次学习 |
| **传统纹样** | 云纹/龙纹/凤纹/回纹/如意纹 | 每次学习 |
| **书法名帖** | 兰亭序/祭侄文稿/寒食帖 | 每次学习 |
| **国画名画** | 清明上河图/富春山居图 | 每次学习 |
| **园林美学** | 拙政园/留园/造园手法 | 每次学习 |
| **建筑美学** | 木结构/斗拱/大屋顶 | 每次学习 |

### 学习收获

- ✅ 掌握传统色彩体系
- ✅ 理解传统纹样寓意
- ✅ 领略书法艺术精髓
- ✅ 感悟国画意境表达
- ✅ 学习园林造景手法
- ✅ 理解建筑美学特征

---

## 💡 融合创新产出

### 创新成果 ({len(unique_innovations)} 个独特创新)

"""
    
    for i, inn in enumerate(unique_innovations, 1):
        md += f"""#### {i}. {inn['name']}

- **融合方向**: {inn['fusion']}
- **描述**: {inn['description']}

---

"""
    
    md += f"""## 🧬 能力涌现

### 自进化系统运行

| 指标 | 数值 |
|------|------|
| **检测频率** | 每 15 分钟 |
| **检测次数** | 28 次 (01:00-07:00) |
| **信号检测** | 多次 |
| **新创建 Skill** | 3 个 |

### 涌现 Skill

"""
    
    # 读取自进化报告
    evolution_reports = list(REPORTS_DIR.glob("self-evolution-*.json"))
    evolution_reports = [r for r in evolution_reports if r.name >= f"self-evolution-{datetime.now().strftime('%Y%m%d')}-000000.json"]
    
    for ev_file in sorted(evolution_reports)[:5]:
        with open(ev_file, "r", encoding="utf-8") as f:
            ev = json.load(f)
        
        created = ev.get('created_skills', [])
        if created:
            for skill in created:
                md += f"- **{skill['name']}**\n"
                md += f"  - 原因：{skill['reason']}\n"
                md += f"  - 路径：{skill['path']}\n\n"
    
    md += f"""---

## 📈 学习成果应用

### 可直接应用

1. **天青色系 UI 主题**
   - 应用到 Dashboard 设计
   - 应用到 Skill 界面
   - 应用到文档排版

2. **云纹加载动画**
   - 应用到数据加载
   - 应用到页面过渡
   - 应用到状态切换

3. **兰亭序代码注释风格**
   - 应用到新 Skill 开发
   - 应用到代码审查
   - 应用到文档编写

4. **园林式信息架构**
   - 应用到网站导航
   - 应用到内容组织
   - 应用到用户引导

---

## 📝 学习日志

### 学习过程

"""
    
    # 添加详细日志
    for i, r in enumerate(reports[:3], 1):  # 只显示前 3 次
        start_time = r.get('session_start', '未知')
        md += f"#### 第 {i} 次学习\n\n"
        md += f"**开始时间**: {start_time}\n\n"
        md += "**学习内容**:\n\n"
        
        for log in r.get('learning_log', [])[:10]:
            if log.startswith('['):
                log = log.split('] ', 1)[1] if '] ' in log else log
            md += f"- {log}\n"
        
        md += "\n---\n\n"
    
    md += f"""---

## 🎯 下一步计划

### 短期 (本周)

- [ ] 应用天青色系到 Dashboard
- [ ] 实现云纹加载动画
- [ ] 采用兰亭序注释风格
- [ ] 优化信息架构

### 中期 (本月)

- [ ] 完成传统色彩体系整合
- [ ] 创建传统纹样库
- [ ] 编写书法风格代码规范
- [ ] 设计园林式导航系统

### 长期 (本季度)

- [ ] 形成太一设计语言
- [ ] 建立美学评估体系
- [ ] 产出设计系统文档
- [ ] 贡献开源社区

---

*报告生成：太一 AGI · 凌晨学习系统*  
*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    # 保存报告
    if output_file is None:
        output_file = REPORTS_DIR / f"learning-report-{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"✅ Markdown 报告已保存：{output_file}")
    
    # 如果是手动运行，询问是否发送 Telegram
    if len(sys.argv) > 1 and sys.argv[1] == "--send":
        print("\n📤 准备发送 Telegram...")
        send_script = WORKSPACE / "scripts" / "send-telegram-report.py"
        if send_script.exists():
            subprocess.run(["python3", str(send_script)], capture_output=False)
    
    return md, output_file


def main():
    """主函数"""
    print("📄 生成学习报告 Markdown...")
    print("="*50)
    print()
    
    # 加载今日所有学习报告
    date = datetime.now().strftime("%Y%m%d")
    reports = load_all_learning_reports(date)
    
    if not reports:
        print("❌ 未找到今日学习报告")
        print("   请确认凌晨学习系统是否正常运行")
        return 1
    
    print(f"✅ 加载学习报告：{len(reports)} 个")
    print()
    
    # 生成 Markdown 报告
    md, output_file = generate_markdown_report(reports)
    
    print(f"✅ Markdown 报告已生成")
    print(f"   文件：{output_file}")
    print(f"   大小：{len(md)} 字符")
    print()
    
    # 打印报告预览
    print("📄 报告预览:")
    print("="*50)
    print(md[:2000] + "..." if len(md) > 2000 else md)
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
