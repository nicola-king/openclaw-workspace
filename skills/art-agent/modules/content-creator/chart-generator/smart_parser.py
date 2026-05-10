#!/usr/bin/env python3
"""
Chart Generator - 智能解析器
增强文字解析能力
"""

import re
from pathlib import Path

class SmartParser:
    """智能文字解析器"""
    
    def __init__(self):
        self.keywords = {
            'sequence': ['然后', '接着', '随后', '->', '→'],
            'hierarchy': ['包含', '分为', '下属', '上级', '{}'],
            'timeline': ['阶段', '时间', '日期', '月', '年'],
            'process': ['流程', '步骤', '过程', '→'],
        }
    
    def parse_to_chart(self, text):
        """智能解析文字为图表"""
        # 1. 分析文本结构
        analysis = self.analyze_text(text)
        
        # 2. 识别图表类型
        chart_type = self.identify_chart_type(analysis)
        
        # 3. 提取节点和关系
        nodes, edges = self.extract_nodes_edges(text)
        
        # 4. 生成 Mermaid
        mermaid = self.generate_mermaid(nodes, edges, chart_type)
        
        return {
            'chart_type': chart_type,
            'mermaid': mermaid,
            'analysis': analysis
        }
    
    def analyze_text(self, text):
        """分析文本"""
        return {
            'has_sequence': any(kw in text for kw in self.keywords['sequence']),
            'has_hierarchy': any(kw in text for kw in self.keywords['hierarchy']),
            'has_timeline': any(kw in text for kw in self.keywords['timeline']),
            'has_process': any(kw in text for kw in self.keywords['process']),
            'length': len(text),
            'complexity': self._calculate_complexity(text)
        }
    
    def identify_chart_type(self, analysis):
        """识别图表类型"""
        if analysis['has_timeline']:
            return 'gantt'
        elif analysis['has_sequence']:
            return 'sequence'
        elif analysis['has_hierarchy']:
            return 'mindmap'
        else:
            return 'flowchart'
    
    def extract_nodes_edges(self, text):
        """提取节点和边"""
        # 简单实现：按箭头分割
        if '→' in text:
            parts = text.split('→')
            nodes = [p.strip() for p in parts]
            edges = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
        elif '->' in text:
            parts = text.split('->')
            nodes = [p.strip() for p in parts]
            edges = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
        else:
            nodes = [text.strip()]
            edges = []
        
        return nodes, edges
    
    def generate_mermaid(self, nodes, edges, chart_type):
        """生成 Mermaid 代码"""
        if chart_type == 'flowchart':
            mermaid = "flowchart TD\n"
            for src, dst in edges:
                mermaid += f"    {src} --> {dst}\n"
        elif chart_type == 'sequence':
            mermaid = "sequenceDiagram\n"
            for src, dst in edges:
                mermaid += f"    {src}->>{dst}: 消息\n"
        elif chart_type == 'mindmap':
            mermaid = "mindmap\n"
            for node in nodes:
                mermaid += f"    {node}\n"
        elif chart_type == 'gantt':
            mermaid = "gantt\n    dateFormat  YYYY-MM-DD\n"
            for i, node in enumerate(nodes):
                mermaid += f"    {node} :2024-01-{i+1:02d}, 10d\n"
        else:
            mermaid = "flowchart TD\n"
            for src, dst in edges:
                mermaid += f"    {src} --> {dst}\n"
        
        return mermaid
    
    def _calculate_complexity(self, text):
        """计算复杂度"""
        if len(text) < 20:
            return 'simple'
        elif len(text) < 100:
            return 'medium'
        else:
            return 'complex'


def main():
    """测试"""
    parser = SmartParser()
    
    test_texts = [
        "开始→处理→结束",
        "A->B: 消息 1\nB->C: 消息 2",
        "主题 {子 1, 子 2, 子 3}",
        "阶段 1: 需求分析\n阶段 2: 开发\n阶段 3: 测试",
    ]
    
    for text in test_texts:
        print(f"\n输入：{text}")
        result = parser.parse_to_chart(text)
        print(f"类型：{result['chart_type']}")
        print(f"Mermaid:\n{result['mermaid']}")


if __name__ == "__main__":
    main()
