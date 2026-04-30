#!/usr/bin/env python3
"""
每周质量趋势分析报告
太一 AGI · 2026-04-17

功能：
- 分析 monitoring/task-quality-log.json 数据
- 生成每周质量趋势报告
- 识别高频问题脚本
- 提供改进建议
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
QUALITY_LOG = WORKSPACE / "monitoring" / "task-quality-log.json"
REPORTS_DIR = WORKSPACE / "reports" / "quality"


def load_quality_logs(days=7):
    """加载最近 N 天的质量日志"""
    if not QUALITY_LOG.exists():
        return []
    
    with open(QUALITY_LOG, "r", encoding="utf-8") as f:
        logs = json.load(f)
    
    # 过滤最近 N 天的数据
    cutoff = datetime.now() - timedelta(days=days)
    recent_logs = []
    for log in logs:
        try:
            log_time = datetime.fromisoformat(log["timestamp"])
            if log_time >= cutoff:
                recent_logs.append(log)
        except:
            continue
    
    return recent_logs


def analyze_quality_trends(logs):
    """分析质量趋势"""
    if not logs:
        return None
    
    # 按脚本统计
    script_stats = defaultdict(lambda: {"total": 0, "fixed": 0, "failed": 0})
    
    # 按类型统计
    issue_type_stats = defaultdict(int)
    
    # 按时间统计（每天）
    daily_stats = defaultdict(int)
    
    # 自动修复统计
    auto_fix_stats = {"total": 0, "success": 0, "failed": 0}
    
    for log in logs:
        script = log.get("script", "unknown")
        issue_type = log.get("issue_type", "unknown")
        severity = log.get("severity", "unknown")
        timestamp = log.get("timestamp", "")
        
        # 脚本统计
        script_stats[script]["total"] += 1
        
        # 问题类型统计
        issue_type_stats[issue_type] += 1
        
        # 每日统计
        if timestamp:
            day = timestamp[:10]  # YYYY-MM-DD
            daily_stats[day] += 1
        
        # 自动修复统计
        auto_fix = log.get("auto_fix", {})
        if auto_fix:
            auto_fix_stats["total"] += 1
            if auto_fix.get("status") == "fixed":
                auto_fix_stats["success"] += 1
                script_stats[script]["fixed"] += 1
            else:
                auto_fix_stats["failed"] += 1
                script_stats[script]["failed"] += 1
    
    return {
        "total_issues": len(logs),
        "script_stats": dict(script_stats),
        "issue_type_stats": dict(issue_type_stats),
        "daily_stats": dict(sorted(daily_stats.items())),
        "auto_fix_stats": auto_fix_stats,
        "period": f"{min(daily_stats.keys()) if daily_stats else 'N/A'} ~ {max(daily_stats.keys()) if daily_stats else 'N/A'}"
    }


def generate_report(analysis):
    """生成质量趋势报告"""
    if not analysis:
        return "# 质量趋势报告\n\n本周无质量问题记录。"
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# 定时任务质量趋势周报

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
统计周期：{analysis['period']}

---

## 📊 总体指标

| 指标 | 数值 |
|------|------|
| 总问题数 | {analysis['total_issues']} |
| 涉及脚本数 | {len(analysis['script_stats'])} |
| 自动修复成功率 | {analysis['auto_fix_stats']['success']}/{analysis['auto_fix_stats']['total']} ({analysis['auto_fix_stats']['success']*100//analysis['auto_fix_stats']['total'] if analysis['auto_fix_stats']['total'] > 0 else 0}%) |

---

## 📈 每日趋势

| 日期 | 问题数 | 趋势 |
|------|--------|------|
"""
    
    # 每日趋势
    prev_count = None
    for date, count in analysis['daily_stats'].items():
        trend = "➡️" if prev_count is None else ("📈" if count > prev_count else ("📉" if count < prev_count else "➡️"))
        report += f"| {date} | {count} | {trend} |\n"
        prev_count = count
    
    report += f"""
---

## 🔧 脚本问题排行

| 脚本 | 总问题 | 已修复 | 修复失败 | 修复率 |
|------|--------|--------|----------|--------|
"""
    
    # 脚本排行（按问题数降序）
    sorted_scripts = sorted(
        analysis['script_stats'].items(),
        key=lambda x: x[1]['total'],
        reverse=True
    )
    
    for script, stats in sorted_scripts:
        fix_rate = f"{stats['fixed']*100//stats['total']}%" if stats['total'] > 0 else "N/A"
        report += f"| {script} | {stats['total']} | {stats['fixed']} | {stats['failed']} | {fix_rate} |\n"
    
    report += f"""
---

## 🏷️ 问题类型分布

| 问题类型 | 数量 | 占比 |
|------|------|------|
"""
    
    # 问题类型分布
    sorted_types = sorted(
        analysis['issue_type_stats'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    for issue_type, count in sorted_types:
        percentage = count * 100 // analysis['total_issues']
        report += f"| {issue_type} | {count} | {percentage}% |\n"
    
    report += f"""
---

## 💡 改进建议

"""
    
    # 生成改进建议
    recommendations = []
    
    # 高频问题脚本
    if sorted_scripts:
        top_script = sorted_scripts[0]
        if top_script[1]['total'] >= 3:
            recommendations.append(f"1. **优先修复 {top_script[0]}** - 本周出现 {top_script[1]['total']} 次问题，建议检查脚本逻辑")
    
    # 修复率低
    low_fix_scripts = [
        (script, stats) for script, stats in sorted_scripts
        if stats['total'] > 0 and stats['fixed'] / stats['total'] < 0.5
    ]
    if low_fix_scripts:
        recommendations.append(f"2. **关注修复率低的脚本** - {', '.join([s[0] for s in low_fix_scripts])} 修复率低于 50%")
    
    # 自动修复成功率
    if analysis['auto_fix_stats']['total'] > 0:
        fix_success_rate = analysis['auto_fix_stats']['success'] * 100 // analysis['auto_fix_stats']['total']
        if fix_success_rate < 80:
            recommendations.append(f"3. **优化自动修复机制** - 当前成功率 {fix_success_rate}%，目标 80%+")
    
    if not recommendations:
        recommendations.append("✅ 本周质量状况良好，无特别改进建议")
    
    report += "\n".join(recommendations)
    
    report += f"""

---

## 📝 原始数据

- 数据来源：`monitoring/task-quality-log.json`
- 记录总数：{analysis['total_issues']} 条
- 统计脚本：`scripts/weekly-quality-report.py`

---

*太一 AGI · 定时任务质量监控 · 周报自动生成*
"""
    
    return report


def main():
    """主函数"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📊 开始生成质量趋势周报...")
    
    # 加载最近 7 天数据
    print("  📁 加载最近 7 天质量日志...")
    logs = load_quality_logs(days=7)
    print(f"  找到 {len(logs)} 条记录")
    
    # 分析趋势
    print("  📈 分析质量趋势...")
    analysis = analyze_quality_trends(logs)
    
    # 生成报告
    print("  📝 生成报告...")
    report = generate_report(analysis)
    
    # 保存报告
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / f"weekly-quality-report-{datetime.now().strftime('%Y%m%d')}.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"  ✅ 报告已保存：{report_file}")
    
    # 打印报告摘要
    print(f"\n📊 报告摘要:")
    if analysis:
        print(f"  总问题数：{analysis['total_issues']}")
        print(f"  涉及脚本：{len(analysis['script_stats'])}")
        print(f"  自动修复成功率：{analysis['auto_fix_stats']['success']}/{analysis['auto_fix_stats']['total']}")
    else:
        print("  本周无质量问题记录 ✅")
    
    print(f"\n✅ 质量趋势周报生成完成！")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
