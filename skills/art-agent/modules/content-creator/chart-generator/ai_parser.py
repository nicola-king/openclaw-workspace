#!/usr/bin/env python3
"""
Chart Generator - AI 智能解析
支持：LLM 文字理解、复杂场景生成
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class AIParser:
    """AI 智能解析器"""
    
    def __init__(self):
        self.workspace = Path("/home/sayelf/.openclaw/workspace")
        self.output_dir = self.workspace / "chart-ai-exports"
        self.output_dir.mkdir(exist_ok=True)
    
    def parse_natural_language(self, text):
        """解析自然语言为图表"""
        print(f"🤖 AI 解析：{text[:50]}...")
        
        # 简单规则解析（临时实现）
        # 实际应集成 LLM
        
        result = {
            'chart_type': self._identify_chart_type(text),
            'nodes': self._extract_nodes(text),
            'edges': self._extract_edges(text),
            'style': self._recommend_style(text)
        }
        
        # 生成 Mermaid
        mermaid = self._generate_mermaid(result)
        
        return {
            'analysis': result,
            'mermaid': mermaid
        }
    
    def _identify_chart_type(self, text):
        """识别图表类型"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['流程', '步骤', '过程', '→']):
            return 'flowchart'
        elif any(kw in text_lower for kw in ['时序', '消息', '通信']):
            return 'sequence'
        elif any(kw in text_lower for kw in ['结构', '层次', '包含']):
            return 'mindmap'
        elif any(kw in text_lower for kw in ['时间', '计划', '进度']):
            return 'gantt'
        else:
            return 'flowchart'
    
    def _extract_nodes(self, text):
        """提取节点"""
        # 简单实现：按标点分割
        import re
        nodes = re.split(r'[，。,.→→]', text)
        return [n.strip() for n in nodes if len(n.strip()) > 0][:10]
    
    def _extract_edges(self, text):
        """提取边"""
        # 简单实现：顺序连接
        nodes = self._extract_nodes(text)
        edges = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
        return edges
    
    def _recommend_style(self, text):
        """推荐样式"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['技术', '代码', 'tech']):
            return 'tech'
        elif any(kw in text_lower for kw in ['商务', '专业']):
            return 'professional'
        elif any(kw in text_lower for kw in ['创意', '艺术']):
            return 'creative'
        else:
            return 'professional'
    
    def _generate_mermaid(self, result):
        """生成 Mermaid"""
        chart_type = result['chart_type']
        nodes = result['nodes']
        edges = result['edges']
        
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
        else:
            mermaid = "flowchart TD\n"
            for src, dst in edges:
                mermaid += f"    {src} --> {dst}\n"
        
        return mermaid
    
    def batch_parse(self, texts):
        """批量解析"""
        print(f"📦 批量 AI 解析：{len(texts)} 个文本")
        
        results = []
        for i, text in enumerate(texts, 1):
            print(f"\n[{i}/{len(texts)}] {text[:30]}...")
            result = self.parse_natural_language(text)
            results.append(result)
        
        return results


def main():
    """主函数"""
    parser = AIParser()
    
    if len(sys.argv) < 2:
        print("用法：python3 ai_parser.py <文字描述>")
        print("\n示例:")
        print('  python3 ai_parser.py "项目管理流程：需求分析→方案设计→开发实现→测试验证→部署上线"')
        sys.exit(1)
    
    text = ' '.join(sys.argv[1:])
    result = parser.parse_natural_language(text)
    
    print(f"\n🎉 完成！")
    print(f"📊 图表类型：{result['analysis']['chart_type']}")
    print(f"🎨 推荐样式：{result['analysis']['style']}")
    print(f"📝 Mermaid:\n{result['mermaid']}")


if __name__ == "__main__":
    main()
