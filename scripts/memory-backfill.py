#!/usr/bin/env python3
"""
记忆回填系统 (Memory Backfill)

功能:
1. 选择性回填历史记忆到核心层
2. 从 daily notes 提炼决策/任务/洞察
3. 更新 memory/core.md
4. 生成回填报告

灵感来源：OpenClaw v2026.4.9 REM Backfill

作者：太一 AGI
创建：2026-04-10
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
CORE_FILE = MEMORY_DIR / "core.md"
RESIDUAL_FILE = MEMORY_DIR / "residual.md"
REPORTS_DIR = WORKSPACE / "reports"


def parse_daily_note(file_path):
    """解析每日笔记，提取结构化内容"""
    if not file_path.exists():
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
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
    
    return extracted


def load_core_memory():
    """加载核心记忆"""
    if not CORE_FILE.exists():
        return {'sections': {}, 'last_updated': None}
    
    with open(CORE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 简单解析核心记忆结构
    core = {
        'sections': {
            'decisions': [],
            'tasks': [],
            'insights': [],
            'emergence': [],
            'constitution': []
        },
        'last_updated': None
    }
    
    # 提取最后更新时间
    date_match = re.search(r'最后更新：(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        core['last_updated'] = date_match.group(1)
    
    return core


def backfill_date_range(start_date, end_date, dry_run=False):
    """回填指定日期范围的记忆"""
    
    backfilled = {
        'decisions': [],
        'tasks': [],
        'insights': [],
        'emergence': [],
        'constitution': [],
        'files_processed': 0,
        'files_skipped': 0
    }
    
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        daily_file = MEMORY_DIR / f"{date_str}.md"
        
        if daily_file.exists():
            parsed = parse_daily_note(daily_file)
            if parsed:
                for key in ['decisions', 'tasks', 'insights', 'emergence', 'constitution']:
                    backfilled[key].extend([
                        {'date': date_str, 'content': c}
                        for c in parsed[key]
                    ])
                backfilled['files_processed'] += 1
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
| 宪法修订 | {len(backfilled['constitution'])} |

---

## 📋 回填内容

### 决策 (Decisions)

"""
    
    for item in backfilled['decisions'][:10]:  # 限制显示前 10 条
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
    print()
    
    # 生成报告
    report_file = REPORTS_DIR / f"memory-backfill-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    generate_backfill_report(backfilled, report_file)
    
    print(f"📄 回填报告：{report_file}")
    print()
    
    # 打印摘要
    print("📋 回填摘要 (前 5 条):")
    print("-"*60)
    
    if backfilled['decisions']:
        print("\n【决策】")
        for item in backfilled['decisions'][:5]:
            print(f"  {item['date']}: {item['content'][:60]}...")
    
    if backfilled['insights']:
        print("\n【洞察】")
        for item in backfilled['insights'][:5]:
            print(f"  {item['date']}: {item['content'][:60]}...")
    
    if backfilled['emergence']:
        print("\n【能力涌现】")
        for item in backfilled['emergence'][:5]:
            print(f"  {item['date']}: {item['content'][:60]}...")
    
    print()
    print("✅ 记忆回填完成 - 可审查后手动更新 core.md")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
