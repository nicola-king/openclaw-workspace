#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO KPI 仪表板
版本：v1.0
创建：2026-04-20 21:16
功能：追踪和可视化 GEO 核心指标

基于 Kevin Indig 的 AI 专属 KPI 框架:
- Answer Share (答案份额)
- 提及频率
- 品牌可见度
- 情感倾向
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class KPIRecord:
    """KPI 记录"""
    date: str
    brand: str
    total_queries: int  # 总查询数
    mentioned_count: int  # 被提及次数
    mention_rate: float  # 提及率
    answer_share: float  # 答案份额
    positive_sentiment: int  # 正面情感数
    neutral_sentiment: int  # 中性情感数
    negative_sentiment: int  # 负面情感数
    earned_media_count: int  # Earned Media 数量
    owned_media_count: int  # Owned Media 数量
    top_sources: List[str]  # Top 引用来源


@dataclass
class KPITrend:
    """KPI 趋势"""
    metric: str
    current_value: float
    previous_value: float
    change: float  # 变化量
    change_percent: float  # 变化百分比
    trend: str  # up/down/stable


class GEOKPIDashboard:
    """GEO KPI 仪表板"""
    
    # KPI 目标值 (基于专家建议)
    KPI_TARGETS = {
        "mention_rate": 0.30,  # 30% 提及率
        "answer_share": 0.25,  # 25% 答案份额
        "positive_sentiment_ratio": 0.70,  # 70% 正面情感
        "earned_media_ratio": 0.50,  # 50% Earned Media
    }
    
    def __init__(self, brand: str, data_dir: Optional[str] = None):
        """
        初始化仪表板
        
        Args:
            brand: 品牌名称
            data_dir: 数据存储目录
        """
        self.brand = brand
        self.data_dir = Path(data_dir) if data_dir else Path.cwd() / "geo_kpi_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.records: List[KPIRecord] = []
        self._load_data()
    
    def _load_data(self):
        """加载历史数据"""
        data_file = self.data_dir / "kpi_records.json"
        
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.records = [
                    KPIRecord(**item) for item in data
                ]
            print(f"✅ 加载 {len(self.records)} 条 KPI 记录")
    
    def save_data(self):
        """保存数据"""
        data_file = self.data_dir / "kpi_records.json"
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(
                [asdict(record) for record in self.records],
                f, indent=2, ensure_ascii=False
            )
        
        print(f"💾 KPI 数据已保存：{data_file}")
    
    def add_record(
        self,
        total_queries: int,
        mentioned_count: int,
        answer_share: float,
        positive_sentiment: int,
        neutral_sentiment: int,
        negative_sentiment: int,
        earned_media_count: int,
        owned_media_count: int,
        top_sources: List[str],
        date: Optional[str] = None
    ) -> KPIRecord:
        """
        添加 KPI 记录
        
        Args:
            total_queries: 总查询数
            mentioned_count: 被提及次数
            answer_share: 答案份额
            positive_sentiment: 正面情感数
            neutral_sentiment: 中性情感数
            negative_sentiment: 负面情感数
            earned_media_count: Earned Media 数量
            owned_media_count: Owned Media 数量
            top_sources: Top 引用来源
            date: 日期 (默认今天)
            
        Returns:
            KPIRecord: 创建的记录
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        mention_rate = mentioned_count / total_queries if total_queries > 0 else 0.0
        
        record = KPIRecord(
            date=date,
            brand=self.brand,
            total_queries=total_queries,
            mentioned_count=mentioned_count,
            mention_rate=mention_rate,
            answer_share=answer_share,
            positive_sentiment=positive_sentiment,
            neutral_sentiment=neutral_sentiment,
            negative_sentiment=negative_sentiment,
            earned_media_count=earned_media_count,
            owned_media_count=owned_media_count,
            top_sources=top_sources,
        )
        
        self.records.append(record)
        self.records.sort(key=lambda r: r.date)
        self.save_data()
        
        print(f"✅ 添加 KPI 记录：{date} - 提及率 {mention_rate:.1%}")
        return record
    
    def calculate_trends(self) -> List[KPITrend]:
        """计算趋势"""
        if len(self.records) < 2:
            return []
        
        latest = self.records[-1]
        previous = self.records[-2]
        
        trends = []
        
        # 提及率趋势
        mention_rate_prev = previous.mention_rate
        mention_rate_change = latest.mention_rate - mention_rate_prev
        trends.append(KPITrend(
            metric="mention_rate",
            current_value=latest.mention_rate,
            previous_value=mention_rate_prev,
            change=mention_rate_change,
            change_percent=(mention_rate_change / mention_rate_prev * 100) if mention_rate_prev > 0 else 0,
            trend="up" if mention_rate_change > 0 else ("down" if mention_rate_change < 0 else "stable")
        ))
        
        # 答案份额趋势
        answer_share_prev = previous.answer_share
        answer_share_change = latest.answer_share - answer_share_prev
        trends.append(KPITrend(
            metric="answer_share",
            current_value=latest.answer_share,
            previous_value=answer_share_prev,
            change=answer_share_change,
            change_percent=(answer_share_change / answer_share_prev * 100) if answer_share_prev > 0 else 0,
            trend="up" if answer_share_change > 0 else ("down" if answer_share_change < 0 else "stable")
        ))
        
        # 情感比例趋势
        total_sentiment = latest.positive_sentiment + latest.neutral_sentiment + latest.negative_sentiment
        positive_ratio = latest.positive_sentiment / total_sentiment if total_sentiment > 0 else 0
        
        prev_total = previous.positive_sentiment + previous.neutral_sentiment + previous.negative_sentiment
        prev_positive_ratio = previous.positive_sentiment / prev_total if prev_total > 0 else 0
        
        sentiment_change = positive_ratio - prev_positive_ratio
        trends.append(KPITrend(
            metric="positive_sentiment_ratio",
            current_value=positive_ratio,
            previous_value=prev_positive_ratio,
            change=sentiment_change,
            change_percent=(sentiment_change / prev_positive_ratio * 100) if prev_positive_ratio > 0 else 0,
            trend="up" if sentiment_change > 0 else ("down" if sentiment_change < 0 else "stable")
        ))
        
        # Earned Media 比例趋势
        total_media = latest.earned_media_count + latest.owned_media_count
        earned_ratio = latest.earned_media_count / total_media if total_media > 0 else 0
        
        prev_total_media = previous.earned_media_count + previous.owned_media_count
        prev_earned_ratio = previous.earned_media_count / prev_total_media if prev_total_media > 0 else 0
        
        earned_change = earned_ratio - prev_earned_ratio
        trends.append(KPITrend(
            metric="earned_media_ratio",
            current_value=earned_ratio,
            previous_value=prev_earned_ratio,
            change=earned_change,
            change_percent=(earned_change / prev_earned_ratio * 100) if prev_earned_ratio > 0 else 0,
            trend="up" if earned_change > 0 else ("down" if earned_change < 0 else "stable")
        ))
        
        return trends
    
    def get_target_progress(self) -> Dict[str, Dict]:
        """获取目标进度"""
        if not self.records:
            return {}
        
        latest = self.records[-1]
        total_sentiment = latest.positive_sentiment + latest.neutral_sentiment + latest.negative_sentiment
        positive_ratio = latest.positive_sentiment / total_sentiment if total_sentiment > 0 else 0
        
        total_media = latest.earned_media_count + latest.owned_media_count
        earned_ratio = latest.earned_media_count / total_media if total_media > 0 else 0
        
        progress = {
            "mention_rate": {
                "current": latest.mention_rate,
                "target": self.KPI_TARGETS["mention_rate"],
                "progress": latest.mention_rate / self.KPI_TARGETS["mention_rate"],
            },
            "answer_share": {
                "current": latest.answer_share,
                "target": self.KPI_TARGETS["answer_share"],
                "progress": latest.answer_share / self.KPI_TARGETS["answer_share"],
            },
            "positive_sentiment_ratio": {
                "current": positive_ratio,
                "target": self.KPI_TARGETS["positive_sentiment_ratio"],
                "progress": positive_ratio / self.KPI_TARGETS["positive_sentiment_ratio"],
            },
            "earned_media_ratio": {
                "current": earned_ratio,
                "target": self.KPI_TARGETS["earned_media_ratio"],
                "progress": earned_ratio / self.KPI_TARGETS["earned_media_ratio"],
            },
        }
        
        return progress
    
    def generate_report(self) -> str:
        """生成报告"""
        if not self.records:
            return "暂无 KPI 数据"
        
        latest = self.records[-1]
        trends = self.calculate_trends()
        progress = self.get_target_progress()
        
        report_lines = [
            "=" * 60,
            f"📊 GEO KPI 仪表板 - {self.brand}",
            "=" * 60,
            f"最新数据：{latest.date}",
            "",
            "📈 核心指标:",
            f"  提及率：{latest.mention_rate:.1%} (目标：{self.KPI_TARGETS['mention_rate']:.0%})",
            f"  答案份额：{latest.answer_share:.1%} (目标：{self.KPI_TARGETS['answer_share']:.0%})",
            f"  正面情感：{latest.positive_sentiment}/{latest.positive_sentiment + latest.neutral_sentiment + latest.negative_sentiment}",
            f"  Earned Media: {latest.earned_media_count}/{latest.earned_media_count + latest.owned_media_count}",
            "",
        ]
        
        if trends:
            report_lines.append("📊 趋势:")
            for trend in trends:
                arrow = "📈" if trend.trend == "up" else ("📉" if trend.trend == "down" else "➡️")
                report_lines.append(
                    f"  {arrow} {trend.metric}: {trend.current_value:.1%} "
                    f"({trend.change:+.1%}, {trend.change_percent:+.1f}%)"
                )
            report_lines.append("")
        
        if progress:
            report_lines.append("🎯 目标进度:")
            for metric, data in progress.items():
                bar_length = int(min(data["progress"] * 20, 20))
                bar = "█" * bar_length + "░" * (20 - bar_length)
                report_lines.append(f"  {metric}: [{bar}] {data['progress']:.0%}")
            report_lines.append("")
        
        if latest.top_sources:
            report_lines.append("🔝 Top 引用来源:")
            for i, source in enumerate(latest.top_sources[:5], 1):
                report_lines.append(f"  {i}. {source}")
            report_lines.append("")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def print_dashboard(self):
        """打印仪表板"""
        report = self.generate_report()
        print(report)


def main():
    """示例用法"""
    dashboard = GEOKPIDashboard(brand="YourBrand")
    
    # 添加示例数据
    dashboard.add_record(
        total_queries=100,
        mentioned_count=25,
        answer_share=0.20,
        positive_sentiment=18,
        neutral_sentiment=5,
        negative_sentiment=2,
        earned_media_count=15,
        owned_media_count=10,
        top_sources=["forbes.com", "techcrunch.com", "reuters.com"],
    )
    
    # 打印仪表板
    dashboard.print_dashboard()


if __name__ == "__main__":
    main()
