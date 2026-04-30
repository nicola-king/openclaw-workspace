#!/usr/bin/env python3
"""
Design Agent - 样式优化器
优化图表样式和主题
"""

import os
import sys
from pathlib import Path
from datetime import datetime

class StyleOptimizer:
    """样式优化器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.output_dir = self.workspace / "styled-charts"
        self.output_dir.mkdir(exist_ok=True)
        
        # 主题配置
        self.themes = {
            'default': {
                'primaryColor': '#1E88E5',
                'secondaryColor': '#0D47A1',
                'backgroundColor': '#FFFFFF',
                'fontFamily': 'Arial, sans-serif',
                'borderRadius': '5px',
            },
            'dark': {
                'primaryColor': '#64B5F6',
                'secondaryColor': '#1976D2',
                'backgroundColor': '#1A1A2E',
                'fontFamily': 'Arial, sans-serif',
                'borderRadius': '5px',
            },
            'forest': {
                'primaryColor': '#4CAF50',
                'secondaryColor': '#2E7D32',
                'backgroundColor': '#F1F8E9',
                'fontFamily': 'Arial, sans-serif',
                'borderRadius': '10px',
            },
            'neutral': {
                'primaryColor': '#424242',
                'secondaryColor': '#757575',
                'backgroundColor': '#FAFAFA',
                'fontFamily': 'Helvetica, Arial, sans-serif',
                'borderRadius': '0px',
            },
            'tech': {
                'primaryColor': '#00E5FF',
                'secondaryColor': '#00B8D4',
                'backgroundColor': '#000000',
                'fontFamily': 'Courier New, monospace',
                'borderRadius': '3px',
            },
            'creative': {
                'primaryColor': '#FF6B6B',
                'secondaryColor': '#4ECDC4',
                'backgroundColor': '#FFF7F0',
                'fontFamily': 'Comic Sans MS, cursive',
                'borderRadius': '15px',
            },
        }
    
    def optimize_chart(self, chart_file, theme='default'):
        """优化图表样式"""
        print(f"🎨 优化图表样式：{chart_file}")
        
        # 1. 读取 Mermaid
        chart_path = Path(chart_file)
        if chart_path.suffix == '.mmd':
            mermaid = chart_path.read_text(encoding='utf-8')
        elif chart_path.suffix == '.html':
            # 从 HTML 提取 Mermaid
            html_content = chart_path.read_text(encoding='utf-8')
            mermaid = self._extract_mermaid(html_content)
        else:
            print(f"❌ 不支持的文件格式：{chart_file}")
            return None
        
        # 2. 应用主题
        print(f"  应用主题：{theme}")
        themed_mermaid = self.apply_theme(mermaid, theme)
        
        # 3. 优化色彩
        print(f"  优化色彩")
        colored_mermaid = self.optimize_colors(themed_mermaid, theme)
        
        # 4. 生成优化后的 HTML
        print(f"  生成 HTML")
        html_content = self.generate_html(colored_mermaid, theme)
        
        # 5. 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"styled_{timestamp}.html"
        output_file.write_text(html_content, encoding='utf-8')
        
        print(f"✅ 样式优化完成！")
        print(f"📄 输出：{output_file}")
        
        return {
            'styled_file': str(output_file),
            'theme': theme,
            'mermaid': colored_mermaid
        }
    
    def apply_theme(self, mermaid, theme_name):
        """应用主题"""
        theme = self.themes.get(theme_name, self.themes['default'])
        
        # 添加 Mermaid 初始化配置
        config = f"""%%{{
  init: {{
    'theme': 'base',
    'themeVariables': {{
      'primaryColor': '{theme['primaryColor']}',
      'primaryBorderColor': '{theme['primaryColor']}',
      'primaryTextColor': '#fff',
      'secondaryColor': '{theme['secondaryColor']}',
      'secondaryBorderColor': '{theme['secondaryColor']}',
      'secondaryTextColor': '#fff',
      'tertiaryColor': '{theme['primaryColor']}',
      'tertiaryBorderColor': '{theme['primaryColor']}',
      'lineColor': '{theme['secondaryColor']}',
      'fontFamily': '{theme['fontFamily']}',
    }}
  }}
}}%%
"""
        return config + mermaid
    
    def optimize_colors(self, mermaid, theme_name):
        """优化色彩"""
        # 这里可以实现更复杂的色彩优化逻辑
        # 例如：基于内容情感分析推荐色彩
        return mermaid
    
    def generate_html(self, mermaid, theme_name):
        """生成 HTML"""
        theme = self.themes.get(theme_name, self.themes['default'])
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>样式优化的图表 - {theme_name}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: {theme['fontFamily']};
            background: {theme['backgroundColor']};
            color: #333;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: {theme['borderRadius']};
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            margin: 20px 0;
        }}
        h1 {{
            color: {theme['primaryColor']};
            border-bottom: 3px solid {theme['primaryColor']};
            padding-bottom: 15px;
        }}
        .code-block {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: {theme['borderRadius']};
            font-family: monospace;
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid #ddd;
        }}
        .theme-info {{
            background: {theme['primaryColor']};
            color: white;
            padding: 15px;
            border-radius: {theme['borderRadius']};
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>📊 样式优化的图表</h1>
    
    <div class="theme-info">
        <strong>主题：</strong> {theme_name} | 
        <strong>主色：</strong> {theme['primaryColor']} | 
        <strong>字体：</strong> {theme['fontFamily']}
    </div>
    
    <div class="chart-container">
        <div class="mermaid">
{mermaid}
        </div>
    </div>
    
    <h2>Mermaid 代码</h2>
    <div class="code-block"><pre>{mermaid}</pre></div>
    
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'base',
            themeVariables: {{
                primaryColor: '{theme['primaryColor']}',
                primaryBorderColor: '{theme['primaryColor']}',
                secondaryColor: '{theme['secondaryColor']}',
                lineColor: '{theme['secondaryColor']}',
                fontFamily: '{theme['fontFamily']}',
            }}
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def _extract_mermaid(self, html_content):
        """从 HTML 提取 Mermaid 代码"""
        import re
        match = re.search(r'<div class="mermaid">\s*(.*?)\s*</div>', html_content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def batch_optimize(self, chart_files, themes=None):
        """批量优化"""
        if themes is None:
            themes = ['default', 'dark', 'forest', 'tech']
        
        print(f"📦 批量优化样式...")
        
        results = []
        for chart_file in chart_files:
            for theme in themes:
                print(f"\n优化：{Path(chart_file).name} - {theme}")
                result = self.optimize_chart(chart_file, theme)
                if result:
                    results.append(result)
        
        # 生成索引
        index_file = self._generate_index(results)
        
        print(f"\n✅ 批量优化完成！")
        print(f"📄 索引：{index_file}")
        
        return results
    
    def _generate_index(self, results):
        """生成索引页面"""
        index_file = self.output_dir / "index.html"
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>样式优化索引</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #1E88E5; }
        .chart-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .chart-item { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .chart-item h3 { color: #1E88E5; margin-top: 0; }
        .chart-item a { color: #1E88E5; text-decoration: none; }
        .chart-item a:hover { text-decoration: underline; }
        .theme-tag { display: inline-block; background: #1E88E5; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>🎨 样式优化索引</h1>
    <div class="chart-list">
"""
        for result in results:
            theme = result.get('theme', 'default')
            html += f"""
        <div class="chart-item">
            <h3>{Path(result['styled_file']).stem}</h3>
            <span class="theme-tag">{theme}</span>
            <p><a href="{result['styled_file']}">查看图表</a></p>
        </div>
"""
        
        html += """    </div>
</body>
</html>"""
        
        index_file.write_text(html, encoding='utf-8')
        return str(index_file)


def main():
    """主函数"""
    optimizer = StyleOptimizer()
    
    if len(sys.argv) < 2:
        print("用法：python3 style_optimizer.py <图表文件> [主题]")
        print("\n可用主题：default, dark, forest, neutral, tech, creative")
        print("\n示例:")
        print('  python3 style_optimizer.py "chart.mmd" dark')
        print('  python3 style_optimizer.py "chart.html" tech')
        sys.exit(1)
    
    chart_file = sys.argv[1]
    theme = sys.argv[2] if len(sys.argv) > 2 else 'default'
    
    result = optimizer.optimize_chart(chart_file, theme)
    
    if result:
        print(f"\n🎉 完成！")
        print(f"📄 查看：{result['styled_file']}")


if __name__ == "__main__":
    main()
