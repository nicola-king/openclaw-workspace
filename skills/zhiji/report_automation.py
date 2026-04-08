#!/usr/bin/env python3
"""
知几-E 报告自动化
日报/周报/月报 + 实时告警
"""

import json
from datetime import datetime
from typing import Dict, List
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DailyReport:
    """日报"""
    date: str
    total_bets: int
    wins: int
    losses: int
    win_rate: float
    total_profit: float
    roi: float
    best_bet: str
    worst_bet: str

@dataclass
class WeeklyReport:
    """周报"""
    week: str
    total_bets: int
    total_profit: float
    avg_daily_profit: float
    best_day: str
    worst_day: str
    strategy_changes: List[str]

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_path: str = "~/.taiyi/zhiji/reports"):
        self.output_path = Path(output_path).expanduser()
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def generate_daily(self, bets: List[Dict]) -> DailyReport:
        """生成日报"""
        if not bets:
            return None
        
        wins = sum(1 for b in bets if b['profit'] > 0)
        losses = len(bets) - wins
        total_profit = sum(b['profit'] for b in bets)
        total_amount = sum(b['amount'] for b in bets)
        
        best = max(bets, key=lambda x: x['profit'])
        worst = min(bets, key=lambda x: x['profit'])
        
        report = DailyReport(
            date=datetime.now().strftime('%Y-%m-%d'),
            total_bets=len(bets),
            wins=wins,
            losses=losses,
            win_rate=wins/len(bets),
            total_profit=total_profit,
            roi=total_profit/total_amount if total_amount else 0,
            best_bet=best['market'],
            worst_bet=worst['market']
        )
        
        self._save_report(report)
        return report
    
    def generate_weekly(self, daily_reports: List[DailyReport]) -> WeeklyReport:
        """生成周报"""
        if not daily_reports:
            return None
        
        total_bets = sum(r.total_bets for r in daily_reports)
        total_profit = sum(r.total_profit for r in daily_reports)
        
        best_day = max(daily_reports, key=lambda x: x.total_profit)
        worst_day = min(daily_reports, key=lambda x: x.total_profit)
        
        report = WeeklyReport(
            week=datetime.now().strftime('%Y-W%W'),
            total_bets=total_bets,
            total_profit=total_profit,
            avg_daily_profit=total_profit/len(daily_reports),
            best_day=best_day.date,
            worst_day=worst_day.date,
            strategy_changes=[]
        )
        
        self._save_report(report)
        return report
    
    def format_daily(self, report: DailyReport) -> str:
        """格式化日报"""
        return f"""
【知几-E 日报 · {report.date}】

📊 交易统计
━━━━━━━━━━━━━━━━
总下注：{report.total_bets}笔
盈利：{report.wins}笔 | 亏损：{report.losses}笔
胜率：{report.win_rate:.1%}

💰 收益统计
━━━━━━━━━━━━━━━━
总盈利：${report.total_profit:.2f}
ROI: {report.roi:.2%}

🏆 最佳/最差
━━━━━━━━━━━━━━━━
最佳：{report.best_bet}
最差：{report.worst_bet}

💡 建议
━━━━━━━━━━━━━━━━
{self._generate_advice(report)}

━━━━━━━━━━━━━━━━
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    def format_weekly(self, report: WeeklyReport) -> str:
        """格式化周报"""
        return f"""
【知几-E 周报 · {report.week}】

📊 周统计
━━━━━━━━━━━━━━━━
总下注：{report.total_bets}笔
总盈利：${report.total_profit:.2f}
日均盈利：${report.avg_daily_profit:.2f}

📈 最佳/最差日
━━━━━━━━━━━━━━━━
最佳：{report.best_day}
最差：{report.worst_day}

🔄 策略调整
━━━━━━━━━━━━━━━━
{chr(10).join(report.strategy_changes) if report.strategy_changes else '无'}

━━━━━━━━━━━━━━━━
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    def _generate_advice(self, report: DailyReport) -> str:
        """生成建议"""
        if report.win_rate > 0.6:
            return "✅ 表现优秀，保持当前策略"
        elif report.win_rate < 0.4:
            return "⚠️ 胜率偏低，建议提高置信度阈值"
        elif report.roi < 0:
            return "⚠️ ROI 为负，建议降低下注比例"
        else:
            return "✅ 表现稳定，继续执行"
    
    def _save_report(self, report):
        """保存报告"""
        filename = f"report_{report.date if hasattr(report, 'date') else report.week}.json"
        path = self.output_path / filename
        with open(path, 'w') as f:
            from dataclasses import asdict
            json.dump(asdict(report), f, indent=2)

class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self.alerts = []
    
    def check_alerts(self, performance: Dict) -> List[str]:
        """检查告警"""
        alerts = []
        
        # ROI 告警
        if performance.get('roi', 0) < -0.10:
            alerts.append("🚨 ROI < -10%，触发告警")
        
        # 胜率告警
        if performance.get('win_rate', 0.5) < 0.35:
            alerts.append("🚨 胜率 < 35%，触发告警")
        
        # 回撤告警
        if performance.get('drawdown', 0) > 0.20:
            alerts.append("🚨 回撤 > 20%，触发告警")
        
        return alerts
    
    def send_alert(self, alert: str, channel: str = 'telegram'):
        """发送告警"""
        print(f"[{channel}] {alert}")
        self.alerts.append({
            'timestamp': datetime.now().isoformat(),
            'alert': alert,
            'channel': channel
        })

# 测试
if __name__ == '__main__':
    generator = ReportGenerator()
    alerter = AlertManager()
    
    print("=" * 60)
    print("知几-E 报告自动化")
    print("=" * 60)
    
    # 模拟数据
    bets = [
        {'market': 'BTC', 'profit': 10.0, 'amount': 20.0},
        {'market': 'ETH', 'profit': -5.0, 'amount': 20.0},
        {'market': 'Weather', 'profit': 15.0, 'amount': 20.0},
    ]
    
    # 生成日报
    daily = generator.generate_daily(bets)
    print("\n📰 日报预览:")
    print(generator.format_daily(daily))
    
    # 告警测试
    print("\n🚨 告警测试:")
    perf = {'roi': -0.15, 'win_rate': 0.33, 'drawdown': 0.25}
    alerts = alerter.check_alerts(perf)
    for alert in alerts:
        alerter.send_alert(alert)
    
    print("\n✅ 报告自动化就绪")
    print("=" * 60)
