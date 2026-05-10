#!/usr/bin/env python3
"""
Auto Visual Workflow - 自动可视化工作流
智能分析内容并自动推荐和生成图表
"""

import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

class AutoVisualWorkflow:
    """自动可视化工作流"""
    
    def __init__(self):
        self.workspace = Path("/home/sayelf/.openclaw/workspace")
        self.output_dir = self.workspace / "auto-visual"
        self.output_dir.mkdir(exist_ok=True)
        
        # 图表类型关键词
        self.chart_keywords = {
            'flowchart': ['流程', '步骤', '过程', '→', '然后', '接着'],
            'sequence': ['时序', '消息', '通信', '交互', '->'],
            'mindmap': ['结构', '层次', '包含', '分为', '{}'],
            'gantt': ['时间', '阶段', '计划', '进度', '月', '周'],
        }
    
    def process_content(self, content):
        """处理内容并自动可视化"""
        print(f"🤖 自动可视化工作流启动...")
        
        # 1. 分析内容
        print(f"  步骤 1/5: 分析内容")
        analysis = self.analyze_content(content)
        
        # 2. 推荐图表类型
        print(f"  步骤 2/5: 推荐图表类型")
        chart_type = self.recommend_chart_type(analysis)
        
        # 3. 提取图表文字
        print(f"  步骤 3/5: 提取图表文字")
        chart_text = self.extract_chart_text(content)
        
        # 4. 生成图表
        print(f"  步骤 4/5: 生成图表")
        
        # 导入 VisualAPI
        visual_api_path = Path(__file__).parent.parent / "visual-api" / "visual_api.py"
        sys.path.insert(0, str(visual_api_path.parent))
        from visual_api import VisualAPI
        
        api = VisualAPI()
        chart = api.create_visual_doc(chart_text, chart_type)
        
        # 5. 生成报告
        print(f"  步骤 5/5: 生成报告")
        report = self.generate_report(analysis, chart_type, chart)
        
        return {
            'analysis': analysis,
            'chart_type': chart_type,
            'chart_text': chart_text,
            'chart': chart,
            'report': report
        }
    
    def analyze_content(self, content):
        """分析内容"""
        return {
            'length': len(content),
            'has_time_sequence': any(kw in content for kw in ['然后', '接着', '随后', '阶段']),
            'has_hierarchy': any(kw in content for kw in ['包含', '分为', '下属', '结构']),
            'has_timeline': any(kw in content for kw in ['时间', '计划', '进度', '月', '周']),
            'has_process': any(kw in content for kw in ['流程', '步骤', '过程']),
            'has_communication': any(kw in content for kw in ['消息', '通信', '交互']),
            'paragraphs': content.count('\n\n') + 1,
            'sentences': content.count('。') + content.count('.')
        }
    
    def recommend_chart_type(self, analysis):
        """推荐图表类型"""
        scores = {
            'flowchart': 0,
            'sequence': 0,
            'mindmap': 0,
            'gantt': 0,
        }
        
        if analysis['has_process']:
            scores['flowchart'] += 3
        if analysis['has_time_sequence']:
            scores['flowchart'] += 2
            scores['sequence'] += 2
        if analysis['has_hierarchy']:
            scores['mindmap'] += 3
        if analysis['has_timeline']:
            scores['gantt'] += 3
        if analysis['has_communication']:
            scores['sequence'] += 3
        
        # 返回得分最高的
        chart_type = max(scores, key=scores.get)
        
        print(f"  💡 推荐：{chart_type} (得分：{scores[chart_type]})")
        
        return chart_type
    
    def extract_chart_text(self, content):
        """提取图表文字"""
        # 简单实现：提取包含箭头的行
        lines = content.split('\n')
        chart_lines = []
        
        for line in lines:
            if '→' in line or '->' in line:
                chart_lines.append(line.strip())
        
        if chart_lines:
            return ' '.join(chart_lines)
        
        # 如果没有箭头，尝试提取关键句子
        sentences = content.replace('。', '\n').replace('.', '\n').split('\n')
        key_sentences = [s.strip() for s in sentences if len(s.strip()) > 5 and len(s.strip()) < 50]
        
        if key_sentences:
            return ' → '.join(key_sentences[:5])
        
        return content[:100]
    
    def generate_report(self, analysis, chart_type, chart):
        """生成报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"report_{timestamp}.md"
        
        report = f"""# 📊 自动可视化报告

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 内容分析

- 长度：{analysis['length']} 字符
- 段落数：{analysis['paragraphs']}
- 句子数：{analysis['sentences']}

### 特征检测

| 特征 | 检测结果 |
|------|----------|
| 时间序列 | {'✅' if analysis['has_time_sequence'] else '❌'} |
| 层次结构 | {'✅' if analysis['has_hierarchy'] else '❌'} |
| 时间线 | {'✅' if analysis['has_timeline'] else '❌'} |
| 流程 | {'✅' if analysis['has_process'] else '❌'} |
| 通信交互 | {'✅' if analysis['has_communication'] else '❌'} |

## 推荐结果

- **推荐图表类型**: {chart_type}
- **图表文件**: {chart['styled_file']}
- **Mermaid 文件**: {chart.get('mermaid_file', 'N/A')}

## 图表预览

![图表]({chart['styled_file']})

---

*太一 AGI · 自动可视化工作流*
"""
        
        report_file.write_text(report, encoding='utf-8')
        
        return {
            'file': str(report_file),
            'timestamp': timestamp
        }
    
    def batch_process(self, content_list):
        """批量处理"""
        print(f"📦 批量处理内容...")
        
        results = []
        for i, content in enumerate(content_list, 1):
            print(f"\n[{i}/{len(content_list)}] 处理内容 {i}")
            result = self.process_content(content)
            results.append(result)
        
        # 生成总索引
        index_file = self._generate_batch_index(results)
        
        print(f"\n✅ 批量处理完成！")
        print(f"📄 索引：{index_file}")
        
        return results
    
    def _generate_batch_index(self, results):
        """生成批量处理索引"""
        index_file = self.output_dir / "batch_index.html"
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>批量可视化索引</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #1E88E5; }
        .result-list { list-style: none; padding: 0; }
        .result-item { background: white; padding: 20px; margin: 10px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .result-item h3 { color: #1E88E5; margin-top: 0; }
        .chart-type { display: inline-block; background: #4CAF50; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; }
        .result-item a { color: #1E88E5; text-decoration: none; }
        .result-item a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>📊 批量可视化索引</h1>
    <ul class="result-list">
"""
        for i, result in enumerate(results, 1):
            html += f"""
        <li class="result-item">
            <h3>内容 {i}</h3>
            <span class="chart-type">{result['chart_type']}</span>
            <p>图表：<a href="{result['chart']['styled_file']}">查看</a></p>
            <p>报告：<a href="{result['report']['file']}">查看</a></p>
        </li>
"""
        
        html += """    </ul>
</body>
</html>"""
        
        index_file.write_text(html, encoding='utf-8')
        return str(index_file)


def main():
    """主函数"""
    workflow = AutoVisualWorkflow()
    
    if len(sys.argv) < 2:
        print("用法：python3 auto_visual_workflow.py <文字内容>")
        print("\n示例:")
        print('  python3 auto_visual_workflow.py "需求分析→方案设计→开发实现→测试验证→部署上线"')
        sys.exit(1)
    
    content = sys.argv[1] if len(sys.argv) == 2 else ' '.join(sys.argv[1:])
    
    result = workflow.process_content(content)
    
    print(f"\n🎉 完成！")
    print(f"📊 图表类型：{result['chart_type']}")
    print(f"📄 图表：{result['chart']['styled_file']}")
    print(f"📝 报告：{result['report']['file']}")


if __name__ == "__main__":
    main()
