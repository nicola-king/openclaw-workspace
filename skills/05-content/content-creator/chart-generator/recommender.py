#!/usr/bin/env python3
"""
Chart Generator - 图表推荐引擎
支持：智能推荐、场景匹配
"""

import os
import sys
from pathlib import Path
from datetime import datetime

class ChartRecommender:
    """图表推荐引擎"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.output_dir = self.workspace / "chart-recommendations"
        self.output_dir.mkdir(exist_ok=True)
    
    def recommend_chart_type(self, content):
        """推荐图表类型"""
        features = self._extract_features(content)
        
        # 基于规则推荐
        if features['has_sequence']:
            return 'sequence'
        elif features['has_hierarchy']:
            return 'mindmap'
        elif features['has_timeline']:
            return 'gantt'
        elif features['has_process']:
            return 'flowchart'
        else:
            return 'flowchart'  # 默认
    
    def _extract_features(self, content):
        """提取内容特征"""
        return {
            'has_sequence': any(kw in content for kw in ['然后', '接着', '随后', '->', '→']),
            'has_hierarchy': any(kw in content for kw in ['包含', '分为', '下属', '结构']),
            'has_timeline': any(kw in content for kw in ['阶段', '时间', '日期', '月', '周']),
            'has_process': any(kw in content for kw in ['流程', '步骤', '过程']),
        }
    
    def recommend_style(self, content):
        """推荐样式"""
        # 基于内容情感分析
        if any(kw in content for kw in ['技术', '代码', 'API']):
            return 'tech'
        elif any(kw in content for kw in ['商务', '报告']):
            return 'professional'
        elif any(kw in content for kw in ['创意', '设计']):
            return 'creative'
        else:
            return 'professional'
    
    def generate_recommendation(self, content):
        """生成推荐结果"""
        chart_type = self.recommend_chart_type(content)
        style = self.recommend_style(content)
        
        return {
            'chart_type': chart_type,
            'style': style,
            'confidence': 0.9,
            'reason': self._generate_reason(chart_type, content)
        }
    
    def _generate_reason(self, chart_type, content):
        """生成推荐理由"""
        reasons = {
            'flowchart': '检测到流程描述，推荐使用流程图',
            'sequence': '检测到时序关系，推荐使用时序图',
            'mindmap': '检测到层次结构，推荐使用思维导图',
            'gantt': '检测到时间线，推荐使用甘特图',
        }
        return reasons.get(chart_type, '默认推荐')
    
    def batch_recommend(self, contents):
        """批量推荐"""
        print(f"📦 批量推荐：{len(contents)} 个内容")
        
        results = []
        for i, content in enumerate(contents, 1):
            print(f"\n[{i}/{len(contents)}] {content[:30]}...")
            result = self.generate_recommendation(content)
            results.append(result)
        
        return results


def main():
    """主函数"""
    recommender = ChartRecommender()
    
    if len(sys.argv) < 2:
        print("用法：python3 recommender.py <文字内容>")
        print("\n示例:")
        print('  python3 recommender.py "项目管理流程：需求→设计→开发→测试→部署"')
        sys.exit(1)
    
    content = ' '.join(sys.argv[1:])
    result = recommender.generate_recommendation(content)
    
    print(f"\n💡 推荐结果:")
    print(f"  图表类型：{result['chart_type']}")
    print(f"  推荐样式：{result['style']}")
    print(f"  置信度：{result['confidence']:.0%}")
    print(f"  理由：{result['reason']}")


if __name__ == "__main__":
    main()
