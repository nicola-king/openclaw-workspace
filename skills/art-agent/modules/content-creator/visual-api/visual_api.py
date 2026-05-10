#!/usr/bin/env python3
"""
Visual API - 视觉化统一 API
融合：Chart Generator + Doc Publisher + Design Agent
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# 导入相关模块
sys.path.insert(0, str(Path(__file__).parent.parent))

class VisualAPI:
    """视觉化统一 API"""
    
    def __init__(self):
        self.workspace = Path("/home/sayelf/.openclaw/workspace")
        self.output_dir = self.workspace / "visual-output"
        self.output_dir.mkdir(exist_ok=True)
    
    def create_visual_doc(self, text, chart_type='flowchart', theme='default'):
        """创建可视化文档"""
        print(f"🎨 创建可视化文档...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 生成图表
        print(f"  步骤 1/3: 生成图表 ({chart_type})")
        
        # 导入 ChartGenerator
        chart_gen_path = Path(__file__).parent.parent / "chart-generator" / "chart_generator.py"
        sys.path.insert(0, str(chart_gen_path.parent))
        from chart_generator import ChartGenerator
        
        generator = ChartGenerator()
        chart = generator.create_chart(text, chart_type)
        
        # 2. 优化样式
        print(f"  步骤 2/3: 优化样式 ({theme})")
        styled_html = self._optimize_style(chart['html_file'], theme)
        styled_file = self.output_dir / f"visual_{timestamp}.html"
        Path(styled_file).write_text(styled_html, encoding='utf-8')
        
        # 3. 准备发布
        print(f"  步骤 3/3: 准备发布")
        result = {
            'chart_file': chart['html_file'],
            'styled_file': str(styled_file),
            'mermaid_file': chart['mermaid_file'],
            'timestamp': timestamp
        }
        
        print(f"✅ 可视化文档已创建！")
        print(f"📄 样式优化：{result['styled_file']}")
        
        return result
    
    def _optimize_style(self, html_file, theme):
        """优化样式"""
        html_content = Path(html_file).read_text(encoding='utf-8')
        
        # 应用主题
        themes = {
            'default': '',
            'dark': '''
                <style>
                body { background: #1a1a2e; color: #eee; }
                .chart-container { background: #16213e; box-shadow: 0 2px 10px rgba(255,255,255,0.1); }
                .code-block { background: #0f3460; color: #eee; }
                </style>
            ''',
            'forest': '''
                <style>
                body { background: #f0f0f0; }
                .chart-container { background: white; border: 2px solid #43A047; }
                </style>
            ''',
            'neutral': '''
                <style>
                body { background: #f5f5f5; }
                .chart-container { background: white; }
                </style>
            ''',
        }
        
        theme_css = themes.get(theme, '')
        if theme_css:
            html_content = html_content.replace('</head>', f'{theme_css}</head>')
        
        return html_content
    
    def batch_create(self, contents, chart_type='flowchart'):
        """批量创建图表"""
        print(f"📦 批量创建图表...")
        
        results = []
        for i, (title, text) in enumerate(contents, 1):
            print(f"\n [{i}/{len(contents)}] {title}")
            result = self.create_visual_doc(text, chart_type)
            result['title'] = title
            results.append(result)
        
        # 生成索引
        index_html = self._generate_index(results)
        index_file = self.output_dir / "index.html"
        Path(index_file).write_text(index_html, encoding='utf-8')
        
        print(f"\n✅ 批量创建完成！")
        print(f"📄 索引：{index_file}")
        
        return results
    
    def _generate_index(self, results):
        """生成索引页面"""
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>图表索引</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #1E88E5; }
        .chart-list { list-style: none; padding: 0; }
        .chart-item { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .chart-item a { color: #1E88E5; text-decoration: none; }
        .chart-item a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>📊 图表索引</h1>
    <ul class="chart-list">
"""
        for result in results:
            title = result.get('title', '未命名')
            html += f'        <li class="chart-item"><a href="{result["styled_file"]}">{title}</a></li>\n'
        
        html += """    </ul>
</body>
</html>"""
        
        return html


def main():
    """主函数"""
    api = VisualAPI()
    
    if len(sys.argv) < 2:
        print("用法：python3 visual_api.py [选项] <文字描述>")
        print("\n选项:")
        print("  --type <类型>     图表类型 (flowchart/sequence/mindmap/gantt)")
        print("  --theme <主题>    样式主题 (default/dark/forest/neutral)")
        print("  --batch           批量模式")
        print("\n示例:")
        print('  python3 visual_api.py --type flowchart "开始→处理→结束"')
        print('  python3 visual_api.py --type mindmap --theme dark "主题 {子 1, 子 2}"')
        sys.exit(1)
    
    # 解析参数
    chart_type = 'flowchart'
    theme = 'default'
    text = sys.argv[-1]
    
    if '--type' in sys.argv:
        type_idx = sys.argv.index('--type')
        if type_idx + 1 < len(sys.argv):
            chart_type = sys.argv[type_idx + 1]
    
    if '--theme' in sys.argv:
        theme_idx = sys.argv.index('--theme')
        if theme_idx + 1 < len(sys.argv):
            theme = sys.argv[theme_idx + 1]
    
    # 创建可视化文档
    result = api.create_visual_doc(text, chart_type, theme)
    
    print(f"\n🎨 完成！")
    print(f"📄 查看：{result['styled_file']}")


if __name__ == "__main__":
    main()
