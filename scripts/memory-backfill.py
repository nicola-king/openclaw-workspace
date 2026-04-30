#!/usr/bin/env python3
"""
记忆回填系统 (Memory Backfill)

功能:
1. 选择性回填历史记忆到核心层
2. 从 daily notes 提炼决策/任务/洞察
3. 集成 Knowledge Extractor 自动提炼
4. 更新 memory/core.md
5. 生成回填报告

灵感来源：OpenClaw v2026.4.9 REM Backfill

作者：太一 AGI
创建：2026-04-10
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加 knowledge-extractor 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "knowledge-extractor"))

try:
    from models import KnowledgeAbstract
    from extractor import KnowledgeExtractor
    KNOWLEDGE_EXTRACTOR_AVAILABLE = True
except ImportError:
    print("⚠️  Knowledge Extractor 未加载，使用基础模式")
    KNOWLEDGE_EXTRACTOR_AVAILABLE = False

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
CORE_FILE = MEMORY_DIR / "core.md"
RESIDUAL_FILE = MEMORY_DIR / "residual.md"
REPORTS_DIR = WORKSPACE / "reports"


def parse_daily_note(file_path):
    """解析每日笔记，提取结构化内容"""
    if not file_path.exists():
        return None, None
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 使用 Knowledge Extractor 提取 (如果可用)
    knowledge_data = None
    if KNOWLEDGE_EXTRACTOR_AVAILABLE:
        try:
            extractor = KnowledgeExtractor()
            abstract = extractor.extract(str(file_path))
            knowledge_data = {
                'source': str(file_path),
                'summary': abstract.summary,
                'entities': [e.name for e in abstract.entities[:10]],
                'tags': list(abstract.tags)[:10]
            }
        except Exception as e:
            print(f"⚠️  Knowledge Extractor 提取失败：{e}")
    
    # 提取各类标记
    patterns = {
        'decisions': r'【 (?:决策 |Decision) 】\s*\n(.*?)(?=【|$)',
        'tasks': r'【 (?:任务 |Task) 】\s*\n(.*?)(?=【|$)',
        'insights': r'【 (?:洞察 |Insight) 】\s*\n(.*?)(?=【|$)',
        'emergence': r'【 (?:能力涌现 |Emergence) 】\s*\n(.*?)(?=【|$)',
        'constitution': r'【 (?:宪法修订 |Constitution) 】\s*\n(.*?)(?=【|$)',
    }
    
    extracted = {
        'date': file_path.stem,
        'decisions': [],
        'tasks': [],
        'insights': [],
        'emergence': [],
        'constitution': []
    }
    
    for key, pattern in patterns.items():
        matches = re.findall(pattern, content, re.DOTALL)
        extracted[key] = [m.strip() for m in matches if m.strip()]
    
    return extracted, knowledge_data


def backfill_date_range(start_date, end_date, dry_run=False):
    """回填指定日期范围的记忆"""
    
    backfilled = {
        'decisions': [],
        'tasks': [],
        'insights': [],
        'emergence': [],
        'constitution': [],
        'files_processed': 0,
        'files_skipped': 0,
        'knowledge_abstracts': 0,
        'knowledge_data': []
    }
    
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        daily_file = MEMORY_DIR / f"{date_str}.md"
        
        if daily_file.exists():
            parsed, knowledge_data = parse_daily_note(daily_file)
            if parsed:
                for key in ['decisions', 'tasks', 'insights', 'emergence', 'constitution']:
                    backfilled[key].extend([
                        {'date': date_str, 'content': c}
                        for c in parsed[key]
                    ])
                backfilled['files_processed'] += 1
            
            if knowledge_data:
                backfilled['knowledge_abstracts'] += 1
                backfilled['knowledge_data'].append(knowledge_data)
            else:
                backfilled['files_skipped'] += 1
        else:
            backfilled['files_skipped'] += 1
        
        current += timedelta(days=1)
    
    return backfilled


def generate_backfill_report(backfilled, output_file):
    """生成回填报告"""
    
    report = f"""# 🧠 记忆回填报告

> **执行时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
> **系统**: 太一 AGI · 记忆回填系统  
> **灵感**: OpenClaw v2026.4.9 REM Backfill  
> **增强**: Knowledge Extractor 自动提炼

---

## 📊 回填统计

| 指标 | 数值 |
|------|------|
| 处理文件 | {backfilled['files_processed']} |
| 跳过文件 | {backfilled['files_skipped']} |
| 决策提炼 | {len(backfilled['decisions'])} |
| 任务提炼 | {len(backfilled['tasks'])} |
| 洞察提炼 | {len(backfilled['insights'])} |
| 能力涌现 | {len(backfilled['emergence'])} |
| 知识抽象 | {backfilled['knowledge_abstracts']} |

---

## 📋 回填内容

### 决策 (Decisions)

"""
    
    for item in backfilled['decisions'][:10]:
        report += f"- **{item['date']}**: {item['content'][:100]}...\n"
    
    if len(backfilled['decisions']) > 10:
        report += f"\n*... 还有 {len(backfilled['decisions']) - 10} 条决策*\n"
    
    report += """
### 任务 (Tasks)

"""
    
    for item in backfilled['tasks'][:10]:
        report += f"- **{item['date']}**: {item['content'][:100]}...\n"
    
    if len(backfilled['tasks']) > 10:
        report += f"\n*... 还有 {len(backfilled['tasks']) - 10} 个任务*\n"
    
    report += """
### 洞察 (Insights)

"""
    
    for item in backfilled['insights'][:10]:
        report += f"- **{item['date']}**: {item['content'][:100]}...\n"
    
    if len(backfilled['insights']) > 10:
        report += f"\n*... 还有 {len(backfilled['insights']) - 10} 条洞察*\n"
    
    report += """
### 能力涌现 (Emergence)

"""
    
    for item in backfilled['emergence'][:10]:
        report += f"- **{item['date']}**: {item['content'][:100]}...\n"
    
    if len(backfilled['emergence']) > 10:
        report += f"\n*... 还有 {len(backfilled['emergence']) - 10} 个能力涌现*\n"
    
    # Knowledge Abstracts 部分
    if backfilled['knowledge_data']:
        report += """
### 知识抽象 (Knowledge Abstracts)

"""
        for kd in backfilled['knowledge_data'][:5]:
            report += f"- **{kd['source']}**: {kd['summary'][:100]}...\n"
    
    report += f"""
---

## 📝 下一步

1. 审查回填内容
2. 手动确认重要决策/洞察
3. 更新 memory/core.md
4. 清理重复/过时内容

---

*报告生成：太一 AGI · 记忆回填系统*  
*执行时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    return output_file


def main():
    """主函数"""
    print("🧠 记忆回填系统 - Memory Backfill")
    print("="*60)
    print()
    
    if KNOWLEDGE_EXTRACTOR_AVAILABLE:
        print("✅ Knowledge Extractor 已集成")
    else:
        print("⚠️  Knowledge Extractor 未加载")
    print()
    
    # 默认回填最近 7 天
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    print(f"📅 回填日期范围：{start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')}")
    print()
    
    # 执行回填
    print("🔄 执行回填...")
    backfilled = backfill_date_range(start_date, end_date)
    
    print(f"✅ 回填完成")
    print(f"   处理文件：{backfilled['files_processed']}")
    print(f"   跳过文件：{backfilled['files_skipped']}")
    print(f"   决策提炼：{len(backfilled['decisions'])}")
    print(f"   任务提炼：{len(backfilled['tasks'])}")
    print(f"   洞察提炼：{len(backfilled['insights'])}")
    print(f"   能力涌现：{len(backfilled['emergence'])}")
    print(f"   知识抽象：{backfilled['knowledge_abstracts']}")
    print()
    
    # 生成报告
    report_file = REPORTS_DIR / f"memory-backfill-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    generate_backfill_report(backfilled, report_file)
    
    print(f"📄 回填报告：{report_file}")
    print()
    
    print("✅ 记忆回填完成 - 可审查后手动更新 core.md")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
