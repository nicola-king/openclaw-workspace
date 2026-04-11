#!/usr/bin/env python3
"""
📊 微信公众号数据追踪 Dashboard

功能:
- 阅读量统计
- 分享量统计
- 点赞量统计
- 转化率分析
- ROI 计算

作者：太一 AGI
创建：2026-04-11
"""

import json
from pathlib import Path
from datetime import datetime, timedelta


class WechatMetricsDashboard:
    """微信公众号数据 Dashboard"""
    
    def __init__(self):
        """初始化 Dashboard"""
        self.metrics_dir = Path("/home/nicola/.openclaw/workspace/content")
        
        print("📊 微信公众号数据 Dashboard 已初始化")
        print()
    
    def load_metrics(self, date: str = None) -> list:
        """加载指定日期数据"""
        if not date:
            date = datetime.now().strftime("%Y%m%d")
        
        metrics_file = self.metrics_dir / f"wechat-metrics-{date}.json"
        
        if not metrics_file.exists():
            print(f"⚠️  数据文件不存在：{metrics_file}")
            return []
        
        with open(metrics_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_report(self, begin_date: str = None, end_date: str = None) -> dict:
        """生成数据报告"""
        if not begin_date:
            begin_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
        
        if not end_date:
            end_date = datetime.now().strftime("%Y%m%d")
        
        print(f"📊 生成数据报告：{begin_date} ~ {end_date}")
        
        # 汇总所有数据
        all_metrics = []
        for i in range(8):  # 7 天数据
            date = (datetime.strptime(begin_date, "%Y%m%d") + timedelta(days=i)).strftime("%Y%m%d")
            if date > end_date:
                break
            
            metrics = self.load_metrics(date)
            all_metrics.extend(metrics)
        
        # 计算汇总
        total_read = sum(m.get('int_page_read_count', 0) for m in all_metrics)
        total_share = sum(m.get('share_count', 0) for m in all_metrics)
        total_like = sum(m.get('user_like_count', 0) for m in all_metrics)
        
        report = {
            "period": f"{begin_date} ~ {end_date}",
            "articles_count": len(all_metrics),
            "total_read_count": total_read,
            "total_share_count": total_share,
            "total_like_count": total_like,
            "avg_read_count": total_read / len(all_metrics) if all_metrics else 0,
            "conversion_rate": self._calculate_conversion_rate(total_read, total_share),
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def _calculate_conversion_rate(self, reads: int, shares: int) -> float:
        """计算转化率"""
        if reads == 0:
            return 0.0
        return (shares / reads) * 100
    
    def export_report(self, report: dict, output_file: str):
        """导出报告"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 报告已导出：{output_file}")
    
    def print_dashboard(self, report: dict):
        """打印 Dashboard"""
        print("\n" + "="*60)
        print("📊 微信公众号数据 Dashboard")
        print("="*60)
        print(f"\n统计周期：{report['period']}")
        print(f"文章数量：{report['articles_count']} 篇")
        print(f"\n总阅读量：{report['total_read_count']:,}")
        print(f"总分享量：{report['total_share_count']:,}")
        print(f"总点赞量：{report['total_like_count']:,}")
        print(f"\n平均阅读：{report['avg_read_count']:,.0f}")
        print(f"转化率：{report['conversion_rate']:.2f}%")
        print(f"\n生成时间：{report['generated_at']}")
        print("="*60)


def main():
    """主函数"""
    print("="*60)
    print("📊 微信公众号数据 Dashboard")
    print("="*60)
    
    dashboard = WechatMetricsDashboard()
    
    # 生成报告
    print("\n1. 生成数据报告...")
    report = dashboard.generate_report()
    
    # 打印 Dashboard
    dashboard.print_dashboard(report)
    
    # 导出报告
    print("\n2. 导出报告...")
    today = datetime.now().strftime("%Y%m%d")
    output_file = f"/home/nicola/.openclaw/workspace/content/wechat-report-{today}.json"
    dashboard.export_report(report, output_file)
    
    print("\n✅ 微信公众号数据 Dashboard 测试完成!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
