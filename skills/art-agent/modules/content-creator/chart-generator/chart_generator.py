#!/usr/bin/env python3
"""
Chart Generator - 图表自动生成
支持：流程图/时序图/思维导图/信息图
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

class ChartGenerator:
    """图表生成器"""
    
    def __init__(self):
        self.workspace = Path("/home/sayelf/.openclaw/workspace")
        self.output_dir = self.workspace / "charts"
        self.output_dir.mkdir(exist_ok=True)
    
    def parse_text_to_mermaid(self, text, chart_type='flowchart'):
        """解析文字为 Mermaid 语法"""
        
        if chart_type == 'flowchart':
            return self._parse_flowchart(text)
        elif chart_type == 'sequence':
            return self._parse_sequence(text)
        elif chart_type == 'mindmap':
            return self._parse_mindmap(text)
        elif chart_type == 'gantt':
            return self._parse_gantt(text)
        else:
            return self._parse_flowchart(text)
    
    def _parse_flowchart(self, text):
        """解析流程图"""
        # 简单解析：A→B→C
        nodes = re.split(r'[→→]', text)
        
        mermaid = "flowchart TD\n"
        for i in range(len(nodes) - 1):
            mermaid += f"    {nodes[i].strip()} --> {nodes[i+1].strip()}\n"
        
        return mermaid
    
    def _parse_sequence(self, text):
        """解析时序图"""
        # 简单解析：A->B: 消息
        lines = text.split('\n')
        
        mermaid = "sequenceDiagram\n"
        for line in lines:
            if '->' in line:
                parts = line.split('->')
                if len(parts) == 2:
                    sender = parts[0].strip()
                    rest = parts[1].split(':', 1)
                    if len(rest) == 2:
                        receiver = rest[0].strip()
                        message = rest[1].strip()
                        mermaid += f"    {sender}->>{receiver}: {message}\n"
        
        return mermaid
    
    def _parse_mindmap(self, text):
        """解析思维导图"""
        # 简单解析：根 {子 1, 子 2}
        mermaid = "mindmap\n"
        
        # 递归解析
        def parse_node(text, indent=0):
            result = ""
            if '{' in text:
                parts = text.split('{', 1)
                root = parts[0].strip()
                children_str = parts[1].rstrip('}')
                children = [c.strip() for c in children_str.split(',')]
                
                result += " " * indent + root + "\n"
                for child in children:
                    result += parse_node(child, indent + 2)
            else:
                result += " " * indent + text.strip() + "\n"
            return result
        
        mermaid += parse_node(text)
        return mermaid
    
    def _parse_gantt(self, text):
        """解析甘特图"""
        # 简单解析：任务 1:2024-01-01, 10d
        lines = text.split('\n')
        
        mermaid = "gantt\n"
        mermaid += "    dateFormat  YYYY-MM-DD\n"
        mermaid += "    axisFormat  %m-%d\n"
        
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                if len(parts) == 2:
                    task = parts[0].strip()
                    rest = parts[1].split(',')
                    if len(rest) == 2:
                        start = rest[0].strip()
                        duration = rest[1].strip()
                        mermaid += f"    {task} :{start}, {duration}\n"
        
        return mermaid
    
    def create_chart(self, text, chart_type='flowchart', output_format='png'):
        """创建图表"""
        print(f"📊 生成图表：{chart_type}")
        
        # 解析为 Mermaid
        mermaid_code = self.parse_text_to_mermaid(text, chart_type)
        print(f"✅ Mermaid 语法生成")
        
        # 保存 Mermaid 文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mermaid_file = self.output_dir / f"chart_{timestamp}.mmd"
        mermaid_file.write_text(mermaid_code, encoding='utf-8')
        print(f"✅ Mermaid 已保存：{mermaid_file}")
        
        # 生成 HTML 预览
        html_content = self._generate_html_preview(mermaid_code, chart_type)
        html_file = self.output_dir / f"chart_{timestamp}.html"
        html_file.write_text(html_content, encoding='utf-8')
        print(f"✅ HTML 已保存：{html_file}")
        
        return {
            'mermaid_file': str(mermaid_file),
            'html_file': str(html_file),
            'mermaid_code': mermaid_code
        }
    
    def _generate_html_preview(self, mermaid_code, chart_type):
        """生成 HTML 预览"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图表预览 - {chart_type}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        h1 {{
            color: #1E88E5;
            border-bottom: 2px solid #1E88E5;
            padding-bottom: 10px;
        }}
        .code-block {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            overflow-x: auto;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>📊 图表预览 - {chart_type}</h1>
    
    <div class="chart-container">
        <div class="mermaid">
{mermaid_code}
        </div>
    </div>
    
    <h2>Mermaid 代码</h2>
    <div class="code-block"><pre>{mermaid_code}</pre></div>
    
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>"""


def main():
    """主函数"""
    generator = ChartGenerator()
    
    if len(sys.argv) < 2:
        print("用法：python3 chart_generator.py [选项] <文字描述>")
        print("\n选项:")
        print("  --type <类型>  图表类型 (flowchart/sequence/mindmap/gantt)")
        print("\n示例:")
        print('  python3 chart_generator.py --type flowchart "开始→处理→结束"')
        print('  python3 chart_generator.py --type sequence "A->B: 消息"')
        print('  python3 chart_generator.py --type mindmap "主题 {子 1, 子 2}"')
        sys.exit(1)
    
    # 解析参数
    chart_type = 'flowchart'
    text = sys.argv[-1]
    
    if '--type' in sys.argv:
        type_idx = sys.argv.index('--type')
        if type_idx + 1 < len(sys.argv):
            chart_type = sys.argv[type_idx + 1]
    
    # 生成图表
    result = generator.create_chart(text, chart_type)
    
    print(f"\n✅ 图表生成完成！")
    print(f"📄 Mermaid: {result['mermaid_file']}")
    print(f"🌐 HTML: {result['html_file']}")


if __name__ == "__main__":
    main()
