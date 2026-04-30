#!/usr/bin/env python3
"""
ROI 周报自动化脚本
执行：每周一 09:00 自动运行
功能：生成上周 ROI 报告 + 发送微信/邮件
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

ROI_DB_PATH = "/home/nicola/.openclaw/workspace/data/roi-tracker.db"
REPORT_DIR = "/home/nicola/.openclaw/workspace/reports/roi-weekly"

def get_last_week_dates():
    """获取上周日期范围"""
    today = datetime.now()
    # 上周一
    last_monday = today - timedelta(days=today.weekday() + 7)
    # 上周日
    last_sunday = last_monday + timedelta(days=6)
    
    return last_monday.strftime("%Y-%m-%d"), last_sunday.strftime("%Y-%m-%d")

def generate_weekly_report(start_date, end_date):
    """生成周报"""
    conn = sqlite3.connect(ROI_DB_PATH)
    cursor = conn.cursor()
    
    # 收入汇总
    cursor.execute("""
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM transactions
        WHERE type = 'revenue' AND date BETWEEN ? AND ?
        GROUP BY category
        ORDER BY total DESC
    """, (start_date, end_date))
    revenue_data = cursor.fetchall()
    
    # 成本汇总
    cursor.execute("""
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM transactions
        WHERE type = 'cost' AND date BETWEEN ? AND ?
        GROUP BY category
        ORDER BY total DESC
    """, (start_date, end_date))
    cost_data = cursor.fetchall()
    
    # 交易记录
    cursor.execute("""
        SELECT date, type, category, amount, description
        FROM transactions
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
        LIMIT 20
    """, (start_date, end_date))
    recent_transactions = cursor.fetchall()
    
    conn.close()
    
    # 计算总计
    total_revenue = sum(row[2] for row in revenue_data)
    total_cost = sum(row[2] for row in cost_data)
    net_profit = total_revenue - total_cost
    roi = (net_profit / total_cost * 100) if total_cost > 0 else float('inf')
    
    # 状态判断
    if roi > 100:
        status = "🚀 优秀"
    elif roi > 50:
        status = "✅ 良好"
    elif roi > 0:
        status = "🟡 盈利"
    elif roi > -50:
        status = "🟠 亏损"
    else:
        status = "🔴 严重亏损"
    
    # 生成报告
    report = f"""# ROI 周报

**期间**: {start_date} ~ {end_date}  
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 核心指标

| 指标 | 金额 | 状态 |
|------|------|------|
| 总收入 | ¥{total_revenue:,.2f} | {len(revenue_data)} 笔 |
| 总成本 | ¥{total_cost:,.2f} | {len(cost_data)} 笔 |
| 净利润 | ¥{net_profit:,.2f} | - |
| **ROI** | **{roi:+.1f}%** | **{status}** |

---

## 💰 收入明细

| 分类 | 金额 | 笔数 | 占比 |
|------|------|------|------|
"""
    
    for category, amount, count in revenue_data:
        pct = amount / total_revenue * 100 if total_revenue > 0 else 0
        report += f"| {category} | ¥{amount:,.2f} | {count} | {pct:.1%} |\n"
    
    if not revenue_data:
        report += "*无收入记录*\n"
    
    report += f"""
---

## 💸 成本明细

| 分类 | 金额 | 笔数 | 占比 |
|------|------|------|------|
"""
    
    for category, amount, count in cost_data:
        pct = amount / total_cost * 100 if total_cost > 0 else 0
        report += f"| {category} | ¥{amount:,.2f} | {count} | {pct:.1%} |\n"
    
    if not cost_data:
        report += "*无成本记录*\n"
    
    report += f"""
---

## 📝 最近交易（Top 20）

| 日期 | 类型 | 分类 | 金额 | 描述 |
|------|------|------|------|------|
"""
    
    for date, type_, category, amount, desc in recent_transactions:
        type_icon = "💰" if type_ == 'revenue' else "💸"
        report += f"| {date} | {type_icon} | {category} | ¥{amount:,.2f} | {desc} |\n"
    
    # 对比分析
    prev_start = (datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    prev_end = (datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(ROI_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'revenue' AND date BETWEEN ? AND ?
    """, (prev_start, prev_end))
    prev_revenue = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'cost' AND date BETWEEN ? AND ?
    """, (prev_start, prev_end))
    prev_cost = cursor.fetchone()[0] or 0
    
    conn.close()
    
    revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else float('inf')
    cost_change = ((total_cost - prev_cost) / prev_cost * 100) if prev_cost > 0 else float('inf')
    
    report += f"""
---

## 📈 趋势对比（vs 前 7 天）

| 指标 | 本周 | 上周 | 变化 |
|------|------|------|------|
| 收入 | ¥{total_revenue:,.2f} | ¥{prev_revenue:,.2f} | {revenue_change:+.1f}% |
| 成本 | ¥{total_cost:,.2f} | ¥{prev_cost:,.2f} | {cost_change:+.1f}% |
| 净利润 | ¥{net_profit:,.2f} | ¥{prev_revenue - prev_cost:,.2f} | {(net_profit - (prev_revenue - prev_cost)) / (prev_revenue - prev_cost) * 100 if (prev_revenue - prev_cost) != 0 else float('inf'):+.1f}% |

---

## 💡 建议

"""
    
    if roi > 100:
        report += "✅ **表现优秀** - 考虑扩大投入，复制成功模式\n"
        report += "- 分析高 ROI 项目，加大资源倾斜\n"
        report += "- 总结成功经验，形成标准化流程\n"
    elif roi > 50:
        report += "✅ **表现良好** - 保持稳定，优化高 ROI 项目\n"
        report += "- 关注收入占比最高的项目\n"
        report += "- 控制成本增长\n"
    elif roi > 0:
        report += "🟡 **微利状态** - 分析成本结构，寻找优化空间\n"
        report += "- 审查高成本项目\n"
        report += "- 提升高毛利业务收入占比\n"
    else:
        report += "🔴 **亏损状态** - 立即审查成本，暂停低效项目\n"
        report += "- 列出亏损最严重的 3 个项目\n"
        report += "- 制定止损计划\n"
    
    return report

def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  📊 ROI 周报自动生成                                      ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # 获取日期范围
    start_date, end_date = get_last_week_dates()
    print(f"📅 报告期间：{start_date} ~ {end_date}")
    print()
    
    # 生成报告
    print("📝 生成周报...")
    report = generate_weekly_report(start_date, end_date)
    
    # 保存报告
    report_path = Path(REPORT_DIR) / f"roi-weekly-{start_date}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存：{report_path}")
    print()
    
    # 打印摘要
    print("📊 报告摘要:")
    print("-" * 60)
    # 提取核心指标
    lines = report.split('\n')
    for i, line in enumerate(lines):
        if '总收入' in line or '总成本' in line or '净利润' in line or '**ROI**' in line:
            print(line.strip())
    print("-" * 60)
    print()
    
    print("✅ 周报生成完成")

if __name__ == '__main__':
    main()
