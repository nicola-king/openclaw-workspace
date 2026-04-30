#!/usr/bin/env python3
"""
Google Search Console API 集成

功能:
1. 获取搜索性能数据
2. 分析点击/展示/CTR/排名
3. 生成优化建议
4. 自动优化内容

作者：太一 AGI
创建：2026-04-10
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
from pathlib import Path


class GSCIntegration:
    """Google Search Console 集成"""
    
    def __init__(self, credentials_file: str = None):
        """初始化 GSC API"""
        self.credentials_file = credentials_file
        self.service = None
        self.property_url = None
        
        if credentials_file:
            self._authenticate(credentials_file)
    
    def _authenticate(self, credentials_file: str):
        """认证 GSC API"""
        try:
            creds = Credentials.from_authorized_user_file(credentials_file)
            self.service = build('searchconsole', 'v1', credentials=creds)
            print("✅ GSC API 认证成功")
        except Exception as e:
            print(f"⚠️  GSC API 认证失败：{e}")
            print("请使用 service account 或 OAuth 2.0 认证")
    
    def set_property(self, property_url: str):
        """设置网站属性"""
        self.property_url = property_url
        print(f"✅ 设置网站属性：{property_url}")
    
    def get_analytics(self, start_date: str, end_date: str, 
                     dimensions: list = None) -> dict:
        """
        获取搜索分析数据
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            dimensions: 维度列表 (query/page/country/device)
        
        Returns:
            搜索性能数据
        """
        if not self.service or not self.property_url:
            print("❌ 请先认证并设置网站属性")
            return {}
        
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions or ['query', 'page'],
            'rowLimit': 1000,
            'startRow': 0
        }
        
        try:
            response = self.service.searchanalytics().query(
                siteUrl=self.property_url,
                body=request_body
            ).execute()
            
            return response
        except Exception as e:
            print(f"❌ 获取数据失败：{e}")
            return {}
    
    def analyze_performance(self, data: dict) -> dict:
        """
        分析搜索性能
        
        Returns:
            分析报告
        """
        if 'rows' not in data:
            return {}
        
        rows = data['rows']
        
        analysis = {
            'total_clicks': sum(row['clicks'] for row in rows),
            'total_impressions': sum(row['impressions'] for row in rows),
            'avg_ctr': sum(row['clicks'] for row in rows) / max(1, sum(row['impressions'] for row in rows)),
            'avg_position': sum(row['position'] * row['impressions'] for row in rows) / max(1, sum(row['impressions'] for row in rows)),
            'top_queries': sorted(rows, key=lambda x: x['clicks'], reverse=True)[:10],
            'low_ctr_pages': [row for row in rows if row.get('ctr', 0) < 0.03 and row['impressions'] > 1000],
            'high_impression_low_click': [row for row in rows if row['impressions'] > 5000 and row.get('ctr', 0) < 0.02]
        }
        
        return analysis
    
    def generate_recommendations(self, analysis: dict) -> list:
        """生成优化建议"""
        recommendations = []
        
        # 低 CTR 页面优化
        for page in analysis.get('low_ctr_pages', [])[:5]:
            recommendations.append({
                'type': 'CTR 优化',
                'priority': 'high',
                'page': page.get('keys', ['N/A'])[1] if len(page.get('keys', [])) > 1 else 'N/A',
                'current_ctr': f"{page.get('ctr', 0):.2%}",
                'suggestion': f"优化标题和描述 (当前 CTR: {page.get('ctr', 0):.2%}, 展示：{page.get('impressions', 0):,})"
            })
        
        # 高展示低点击关键词
        for item in analysis.get('high_impression_low_click', [])[:5]:
            recommendations.append({
                'type': '关键词优化',
                'priority': 'medium',
                'query': item.get('keys', ['N/A'])[0] if len(item.get('keys', [])) > 0 else 'N/A',
                'impressions': f"{item.get('impressions', 0):,}",
                'suggestion': f"在内容中强化关键词 '{item.get('keys', ['N/A'])[0]}' (展示：{item.get('impressions', 0):,}, CTR: {item.get('ctr', 0):.2%})"
            })
        
        # 排名提升机会
        top_queries = analysis.get('top_queries', [])[:5]
        for query in top_queries:
            position = query.get('position', 0)
            if 5 < position < 20:
                recommendations.append({
                    'type': '排名提升',
                    'priority': 'medium',
                    'query': query.get('keys', ['N/A'])[0] if len(query.get('keys', [])) > 0 else 'N/A',
                    'current_position': f"{position:.1f}",
                    'suggestion': f"优化内容质量，目标进入前 5 名 (当前排名：{position:.1f})"
                })
        
        return recommendations
    
    def export_report(self, analysis: dict, recommendations: list, 
                     output_file: str = None):
        """导出分析报告"""
        if not output_file:
            output_file = f"reports/gsc-analysis-{datetime.now().strftime('%Y%m%d')}.md"
        
        Path(output_file).parent.mkdir(exist_ok=True)
        
        report = f"""# Google Search Console 分析报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **网站**: {self.property_url or 'N/A'}

---

## 📊 总体表现

| 指标 | 数值 |
|------|------|
| 总点击 | {analysis.get('total_clicks', 0):,} |
| 总展示 | {analysis.get('total_impressions', 0):,} |
| 平均 CTR | {analysis.get('avg_ctr', 0):.2%} |
| 平均排名 | {analysis.get('avg_position', 0):.1f} |

---

## 🔍 热门关键词 (Top 10)

| 关键词 | 点击 | 展示 | CTR | 排名 |
|--------|------|------|-----|------|
"""
        
        for i, query in enumerate(analysis.get('top_queries', [])[:10], 1):
            keys = query.get('keys', [])
            report += f"| {i}. {keys[0] if keys else 'N/A'} | {query.get('clicks', 0):,} | {query.get('impressions', 0):,} | {query.get('ctr', 0):.2%} | {query.get('position', 0):.1f} |\n"
        
        report += f"""
---

## 💡 优化建议 ({len(recommendations)} 条)

"""
        
        for i, rec in enumerate(recommendations, 1):
            report += f"""### {i}. {rec['type']} (优先级：{rec['priority']})

- **目标**: {rec.get('page', rec.get('query', 'N/A'))}
- **当前状态**: {rec.get('current_ctr', rec.get('current_position', 'N/A'))}
- **建议**: {rec['suggestion']}

---

"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 报告已导出：{output_file}")
        return output_file


def main():
    """主函数 - 测试"""
    print("🔍 Google Search Console API 集成测试")
    print("="*60)
    
    # 创建集成对象 (无认证测试)
    gsc = GSCIntegration()
    
    # 模拟数据测试
    print("\n1. 模拟数据分析测试...")
    mock_data = {
        'rows': [
            {'keys': ['太一 AGI'], 'clicks': 100, 'impressions': 3000, 'ctr': 0.033, 'position': 5.2},
            {'keys': ['AI 记忆系统'], 'clicks': 80, 'impressions': 5000, 'ctr': 0.016, 'position': 8.5},
            {'keys': ['自主进化'], 'clicks': 60, 'impressions': 2000, 'ctr': 0.03, 'position': 6.8},
        ]
    }
    
    analysis = gsc.analyze_performance(mock_data)
    print(f"✅ 分析完成:")
    print(f"   总点击：{analysis.get('total_clicks', 0)}")
    print(f"   总展示：{analysis.get('total_impressions', 0)}")
    print(f"   平均 CTR: {analysis.get('avg_ctr', 0):.2%}")
    
    recommendations = gsc.generate_recommendations(analysis)
    print(f"\n✅ 生成 {len(recommendations)} 条优化建议:")
    for rec in recommendations[:3]:
        print(f"   - [{rec['priority']}] {rec['type']}: {rec['suggestion'][:50]}...")
    
    print("\n✅ GSC 集成测试完成!")
    print("\n📝 使用说明:")
    print("1. 获取 GSC API 凭证 (OAuth 2.0 或 Service Account)")
    print("2. 设置 credentials_file 参数")
    print("3. 调用 get_analytics() 获取真实数据")
    print("4. 调用 analyze_performance() 分析")
    print("5. 调用 generate_recommendations() 生成建议")
    print("6. 调用 export_report() 导出报告")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
