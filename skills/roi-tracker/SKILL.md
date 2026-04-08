---
name: roi-tracker
version: 1.0.0
description: roi-tracker skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


#!/usr/bin/env python3
"""
ROI 追踪器 v1.0
灵感来源：ai-marketing-skills / Single Brain 团队

功能：
1. 收入/成本自动追踪
2. ROI 计算与分析
3. 自动报告生成
4. 趋势预测

用途：
- 技能市场收入追踪
- Polymarket 交易 ROI
- 内容创作 ROI
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np


@dataclass
class Transaction:
    """交易记录"""
    id: int
    date: str
    type: str  # 'revenue' or 'cost'
    category: str
    amount: float
    description: str
    metadata: dict


@dataclass
class ROIReport:
    """ROI 报告"""
    period: str
    total_revenue: float
    total_cost: float
    net_profit: float
    roi: float
    roi_percentage: str
    breakdown: dict
    trend: str


class ROITracker:
    """ROI 追踪器"""
    
    def __init__(self, db_path: str = "/home/nicola/.openclaw/workspace/data/roi-tracker.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roi_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_start TEXT NOT NULL,
                period_end TEXT NOT NULL,
                total_revenue REAL NOT NULL,
                total_cost REAL NOT NULL,
                net_profit REAL NOT NULL,
                roi REAL NOT NULL,
                breakdown TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_transaction(
        self,
        type: str,
        category: str,
        amount: float,
        description: str = "",
        date: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> int:
        """
        添加交易记录
        
        Args:
            type: 'revenue' 或 'cost'
            category: 分类（例如：'技能销售'、'交易收益'、'服务器成本'）
            amount: 金额
            description: 描述
            date: 日期（默认今天）
            metadata: 元数据（JSON）
        
        Returns:
            交易 ID
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions (date, type, category, amount, description, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            date,
            type,
            category,
            amount,
            description,
            json.dumps(metadata) if metadata else None
        ))
        
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return transaction_id
    
    def get_period_summary(
        self,
        start_date: str,
        end_date: str
    ) -> ROIReport:
        """
        获取期间汇总
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
        
        Returns:
            ROIReport: ROI 报告
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 收入汇总
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE type = 'revenue' AND date BETWEEN ? AND ?
            GROUP BY category
        """, (start_date, end_date))
        revenue_breakdown = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 成本汇总
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE type = 'cost' AND date BETWEEN ? AND ?
            GROUP BY category
        """, (start_date, end_date))
        cost_breakdown = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        # 计算总计
        total_revenue = sum(revenue_breakdown.values())
        total_cost = sum(cost_breakdown.values())
        net_profit = total_revenue - total_cost
        
        # 计算 ROI
        roi = (net_profit / total_cost * 100) if total_cost > 0 else float('inf')
        roi_pct = f"{roi:+.1f}%" if roi != float('inf') else "N/A"
        
        # 趋势判断
        if roi > 100:
            trend = "🚀 优秀"
        elif roi > 50:
            trend = "✅ 良好"
        elif roi > 0:
            trend = "🟡 盈利"
        elif roi > -50:
            trend = "🟠 亏损"
        else:
            trend = "🔴 严重亏损"
        
        return ROIReport(
            period=f"{start_date} ~ {end_date}",
            total_revenue=total_revenue,
            total_cost=total_cost,
            net_profit=net_profit,
            roi=roi,
            roi_percentage=roi_pct,
            breakdown={
                'revenue': revenue_breakdown,
                'cost': cost_breakdown
            },
            trend=trend
        )
    
    def generate_report(
        self,
        start_date: str,
        end_date: str,
        save_to_db: bool = True
    ) -> str:
        """
        生成 ROI 报告
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            save_to_db: 是否保存到数据库
        
        Returns:
            格式化报告文本
        """
        report_data = self.get_period_summary(start_date, end_date)
        
        report = f"""# ROI 追踪报告

**期间**: {report_data.period}  
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 核心指标

| 指标 | 金额 |
|------|------|
| 总收入 | ¥{report_data.total_revenue:,.2f} |
| 总成本 | ¥{report_data.total_cost:,.2f} |
| 净利润 | ¥{report_data.net_profit:,.2f} |
| **ROI** | **{report_data.roi_percentage}** |
| 状态 | **{report_data.trend}** |

---

## 💰 收入明细

"""
        
        if report_data.breakdown['revenue']:
            report += "| 分类 | 金额 | 占比 |\n"
            report += "|------|------|------|\n"
            for category, amount in sorted(report_data.breakdown['revenue'].items(), key=lambda x: -x[1]):
                pct = amount / report_data.total_revenue * 100 if report_data.total_revenue > 0 else 0
                report += f"| {category} | ¥{amount:,.2f} | {pct:.1%} |\n"
        else:
            report += "*无收入记录*\n"
        
        report += "\n## 💸 成本明细\n\n"
        
        if report_data.breakdown['cost']:
            report += "| 分类 | 金额 | 占比 |\n"
            report += "|------|------|------|\n"
            for category, amount in sorted(report_data.breakdown['cost'].items(), key=lambda x: -x[1]):
                pct = amount / report_data.total_cost * 100 if report_data.total_cost > 0 else 0
                report += f"| {category} | ¥{amount:,.2f} | {pct:.1%} |\n"
        else:
            report += "*无成本记录*\n"
        
        report += f"""
---

## 📈 趋势分析

"""
        
        # 获取前一周期的数据进行对比
        prev_start = (datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
        prev_end = (datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        
        prev_report = self.get_period_summary(prev_start, prev_end)
        
        if prev_report.total_revenue > 0:
            revenue_change = (report_data.total_revenue - prev_report.total_revenue) / prev_report.total_revenue * 100
            report += f"- **收入变化**: {revenue_change:+.1f}% (vs 前 7 天)\n"
        
        if prev_report.total_cost > 0:
            cost_change = (report_data.total_cost - prev_report.total_cost) / prev_report.total_cost * 100
            report += f"- **成本变化**: {cost_change:+.1f}% (vs 前 7 天)\n"
        
        if prev_report.total_cost > 0:
            roi_change = report_data.roi - prev_report.roi
            report += f"- **ROI 变化**: {roi_change:+.1f}pp (vs 前 7 天)\n"
        
        report += f"""
---

## 💡 建议

"""
        
        if report_data.roi > 100:
            report += "✅ **表现优秀** - 考虑扩大投入，复制成功模式\n"
        elif report_data.roi > 50:
            report += "✅ **表现良好** - 保持稳定，优化高 ROI 项目\n"
        elif report_data.roi > 0:
            report += "🟡 **微利状态** - 分析成本结构，寻找优化空间\n"
        else:
            report += "🔴 **亏损状态** - 立即审查成本，暂停低效项目\n"
        
        # 保存到数据库
        if save_to_db:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO roi_reports (period_start, period_end, total_revenue, total_cost, net_profit, roi, breakdown)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                start_date,
                end_date,
                report_data.total_revenue,
                report_data.total_cost,
                report_data.net_profit,
                report_data.roi,
                json.dumps(report_data.breakdown)
            ))
            
            conn.commit()
            conn.close()
        
        return report


# ============== 使用示例 ==============

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  💰 ROI 追踪器 v1.0                                       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    tracker = ROITracker()
    
    # 示例：添加交易记录
    print("📝 添加示例交易记录...")
    print()
    
    today = datetime.now().strftime("%Y-%m-%d")
    last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # 收入
    tracker.add_transaction(
        type='revenue',
        category='技能销售',
        amount=500,
        description='付费技能收入',
        date=today
    )
    
    tracker.add_transaction(
        type='revenue',
        category='交易收益',
        amount=1200,
        description='Polymarket 收益',
        date=today
    )
    
    # 成本
    tracker.add_transaction(
        type='cost',
        category='服务器',
        amount=100,
        description='VPS 月租',
        date=last_week
    )
    
    tracker.add_transaction(
        type='cost',
        category='API 费用',
        amount=50,
        description='百炼 API',
        date=last_week
    )
    
    print("  ✅ 已添加 4 条交易记录")
    print()
    
    # 生成报告
    print("📊 生成 ROI 报告...")
    print()
    
    report = tracker.generate_report(
        start_date=last_week,
        end_date=today
    )
    
    print(report)
