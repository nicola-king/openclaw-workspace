#!/usr/bin/env python3
# scripts/model-usage-stats.py

"""
太一模型使用统计

功能:
1. 读取模型使用日志
2. 生成每日/每周/每月统计
3. 计算 Token 节省率
4. 输出统计报告

使用:
    python3 scripts/model-usage-stats.py --daily
    python3 scripts/model-usage-stats.py --weekly
    python3 scripts/model-usage-stats.py --monthly
"""

import os
import re
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

# 配置
USAGE_LOG = os.path.expanduser("~/.openclaw/workspace/memory/model-usage-today.md")
STATS_DIR = os.path.expanduser("~/.openclaw/workspace/reports")

def parse_usage_log(filepath: str) -> List[Dict]:
    """解析使用日志"""
    entries = []
    
    if not os.path.exists(filepath):
        return entries
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # 格式：- 2026-03-30 21:00 | local | chat | 500 tokens
            match = re.match(r'-\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\d+)\s*tokens', line)
            if match:
                entries.append({
                    "timestamp": match.group(1),
                    "model": match.group(2),
                    "task_type": match.group(3),
                    "tokens": int(match.group(4)),
                })
    
    return entries

def generate_stats(entries: List[Dict], period: str = "daily") -> Dict:
    """生成统计"""
    stats = {
        "total_calls": 0,
        "total_tokens": 0,
        "by_model": defaultdict(lambda: {"calls": 0, "tokens": 0}),
        "by_task": defaultdict(lambda: {"calls": 0, "tokens": 0}),
        "localization_rate": 0.0,
        "estimated_cost": 0.0,
    }
    
    # 成本估算 (每 1K tokens)
    cost_per_1k = {
        "local": 0.0,
        "standard": 0.05,
        "advanced": 0.10,
    }
    
    for entry in entries:
        model = entry["model"]
        tokens = entry["tokens"]
        task_type = entry["task_type"]
        
        stats["total_calls"] += 1
        stats["total_tokens"] += tokens
        
        stats["by_model"][model]["calls"] += 1
        stats["by_model"][model]["tokens"] += tokens
        
        stats["by_task"][task_type]["calls"] += 1
        stats["by_task"][task_type]["tokens"] += tokens
        
        # 成本估算
        stats["estimated_cost"] += (tokens / 1000) * cost_per_1k.get(model, 0.05)
    
    # 本地化率
    if stats["total_calls"] > 0:
        local_calls = stats["by_model"]["local"]["calls"]
        stats["localization_rate"] = local_calls / stats["total_calls"] * 100
    
    return stats

def format_report(stats: Dict, period: str) -> str:
    """格式化报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"# 模型使用统计 · {period}\n\n"
    report += f"**生成时间**: {now}\n\n"
    
    report += "## 📊 总览\n\n"
    report += f"| 指标 | 数值 |\n"
    report += f"|------|------|\n"
    report += f"| 总调用次数 | {stats['total_calls']} |\n"
    report += f"| 总 Token 数 | {stats['total_tokens']:,} |\n"
    report += f"| 估算成本 | ¥{stats['estimated_cost']:.2f} |\n"
    report += f"| 本地化率 | {stats['localization_rate']:.1f}% |\n\n"
    
    report += "## 🤖 按模型统计\n\n"
    report += "| 模型 | 调用次数 | Token 数 | 占比 |\n"
    report += "|------|---------|---------|------|\n"
    
    for model, data in sorted(stats["by_model"].items()):
        pct = data["calls"] / stats["total_calls"] * 100 if stats["total_calls"] > 0 else 0
        report += f"| {model} | {data['calls']} | {data['tokens']:,} | {pct:.1f}% |\n"
    
    report += "\n## 📋 按任务类型统计\n\n"
    report += "| 任务类型 | 调用次数 | Token 数 |\n"
    report += "|---------|---------|---------|\n"
    
    for task, data in sorted(stats["by_task"].items()):
        report += f"| {task} | {data['calls']} | {data['tokens']:,} |\n"
    
    report += "\n## 🎯 优化建议\n\n"
    
    if stats["localization_rate"] < 40:
        report += f"- ⚠️  本地化率 {stats['localization_rate']:.1f}% < 40% 目标，建议增加本地模型使用\n"
    else:
        report += f"- ✅ 本地化率 {stats['localization_rate']:.1f}% 达标 (>40%)\n"
    
    if stats["estimated_cost"] > 10:
        report += f"- ⚠️  成本较高 (¥{stats['estimated_cost']:.2f})，建议优化\n"
    else:
        report += f"- ✅ 成本合理 (¥{stats['estimated_cost']:.2f})\n"
    
    return report

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="太一模型使用统计")
    parser.add_argument("--daily", action="store_true", help="生成每日统计")
    parser.add_argument("--weekly", action="store_true", help="生成每周统计")
    parser.add_argument("--monthly", action="store_true", help="生成每月统计")
    args = parser.parse_args()
    
    # 确定周期
    if args.daily:
        period = "daily"
    elif args.weekly:
        period = "weekly"
    elif args.monthly:
        period = "monthly"
    else:
        period = "daily"  # 默认每日
    
    print("=" * 60)
    print(f"📊 太一模型使用统计 · {period}")
    print("=" * 60)
    
    # 解析日志
    entries = parse_usage_log(USAGE_LOG)
    
    if not entries:
        print("⚠️  无使用记录")
        print(f"日志文件：{USAGE_LOG}")
        return
    
    print(f"\n📝 读取 {len(entries)} 条使用记录")
    
    # 生成统计
    stats = generate_stats(entries, period)
    
    # 格式化报告
    report = format_report(stats, period)
    
    # 输出
    print("\n" + report)
    
    # 保存到文件
    output_file = os.path.join(STATS_DIR, f"model-usage-{period}-{datetime.now().strftime('%Y%m%d')}.md")
    os.makedirs(STATS_DIR, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存到：{output_file}")

if __name__ == '__main__':
    main()
