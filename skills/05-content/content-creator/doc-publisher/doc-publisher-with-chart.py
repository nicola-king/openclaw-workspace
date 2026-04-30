#!/usr/bin/env python3
"""
Doc Publisher 增强 - 支持图表自动插入
"""

import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

class DocPublisherWithChart:
    """支持图表的文档发布器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.output_dir = self.workspace / "published-docs"
        self.output_dir.mkdir(exist_ok=True)
    
    def publish_with_chart(self, md_file, chart_text, chart_type='flowchart', theme='default'):
        """发布带图表的文档"""
        print(f"📄 发布带图表的文档：{md_file}")
        
        # 1. 生成图表
        print(f"  步骤 1/4: 生成图表")
        
        # 导入 VisualAPI
        visual_api_path = Path(__file__).parent.parent / "visual-api" / "visual_api.py"
        sys.path.insert(0, str(visual_api_path.parent))
        from visual_api import VisualAPI
        
        api = VisualAPI()
        chart_result = api.create_visual_doc(chart_text, chart_type, theme)
        
        # 2. 读取原文档
        print(f"  步骤 2/4: 读取文档")
        md_path = Path(md_file)
        if not md_path.exists():
            print(f"❌ 文件不存在：{md_file}")
            return None
        
        md_content = md_path.read_text(encoding='utf-8')
        
        # 3. 插入图表
        print(f"  步骤 3/4: 插入图表")
        chart_section = f"\n\n## 流程图\n\n![流程图]({chart_result['styled_file']})\n"
        md_content += chart_section
        
        # 4. 发布增强文档
        print(f"  步骤 4/4: 发布文档")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"{md_path.stem}_with_chart_{timestamp}.md"
        output_file.write_text(md_content, encoding='utf-8')
        
        result = {
            'original_file': str(md_path),
            'enhanced_file': str(output_file),
            'chart_file': chart_result['styled_file'],
            'timestamp': timestamp
        }
        
        print(f"✅ 文档发布完成！")
        print(f"📄 增强文档：{result['enhanced_file']}")
        
        return result
    
    def batch_publish_with_charts(self, docs_config):
        """批量发布带图表的文档
        
        docs_config: list of dict
            [
                {
                    'md_file': 'file.md',
                    'chart_text': 'A→B→C',
                    'chart_type': 'flowchart',
                    'theme': 'default'
                },
                ...
            ]
        """
        print(f"📦 批量发布带图表的文档...")
        
        results = []
        for i, config in enumerate(docs_config, 1):
            print(f"\n[{i}/{len(docs_config)}] {config['md_file']}")
            result = self.publish_with_chart(
                config['md_file'],
                config['chart_text'],
                config.get('chart_type', 'flowchart'),
                config.get('theme', 'default')
            )
            if result:
                results.append(result)
        
        # 生成索引
        index_file = self._generate_batch_index(results)
        
        print(f"\n✅ 批量发布完成！")
        print(f"📄 索引：{index_file}")
        
        return results
    
    def _generate_batch_index(self, results):
        """生成批量发布索引"""
        index_file = self.output_dir / "index.html"
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>文档索引</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #1E88E5; }
        .doc-list { list-style: none; padding: 0; }
        .doc-item { background: white; padding: 20px; margin: 10px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .doc-item h3 { color: #1E88E5; margin-top: 0; }
        .doc-item a { color: #1E88E5; text-decoration: none; }
        .doc-item a:hover { text-decoration: underline; }
        .chart-preview { margin: 10px 0; }
        .chart-preview img { max-width: 100%; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>📄 文档索引</h1>
    <ul class="doc-list">
"""
        for result in results:
            enhanced = Path(result['enhanced_file'])
            chart = Path(result['chart_file'])
            html += f"""
        <li class="doc-item">
            <h3>{enhanced.stem}</h3>
            <p>原文档：<a href="{result['original_file']}">{result['original_file']}</a></p>
            <p>增强文档：<a href="{result['enhanced_file']}">{enhanced.name}</a></p>
            <div class="chart-preview">
                <p>图表预览：<a href="{result['chart_file']}">{chart.name}</a></p>
            </div>
        </li>
"""
        
        html += """    </ul>
</body>
</html>"""
        
        index_file.write_text(html, encoding='utf-8')
        return str(index_file)


def main():
    """主函数"""
    publisher = DocPublisherWithChart()
    
    if len(sys.argv) < 3:
        print("用法：python3 doc-publisher-with-chart.py <文档.md> \"图表描述\" [类型] [主题]")
        print("\n示例:")
        print('  python3 doc-publisher-with-chart.py "README.md" "开始→处理→结束"')
        print('  python3 doc-publisher-with-chart.py "README.md" "A→B→C" flowchart dark')
        sys.exit(1)
    
    md_file = sys.argv[1]
    chart_text = sys.argv[2]
    chart_type = sys.argv[3] if len(sys.argv) > 3 else 'flowchart'
    theme = sys.argv[4] if len(sys.argv) > 4 else 'default'
    
    result = publisher.publish_with_chart(md_file, chart_text, chart_type, theme)
    
    if result:
        print(f"\n🎉 完成！")
        print(f"📄 查看：{result['enhanced_file']}")


if __name__ == "__main__":
    main()
