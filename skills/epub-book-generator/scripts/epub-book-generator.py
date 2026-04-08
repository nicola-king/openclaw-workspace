#!/usr/bin/env python3
# epub-book-generator - Markdown 转 EPUB 电子书生成器 v1.0
# 用法：python3 epub-book-generator.py <input.md> [output.epub] [options]

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 依赖检查
try:
    import markdown
    from jinja2 import Template
    import pypandoc
except ImportError as e:
    print(f"❌ 缺少依赖：{e}")
    print("请运行：pip install -r requirements.txt")
    sys.exit(1)

# 配置
DEFAULT_COVER_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <style>
        body {{ text-align: center; margin: 0; padding: 0; }}
        .cover {{ height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
        h1 {{ font-size: 2em; color: #333; margin-bottom: 0.5em; }}
        p {{ font-size: 1em; color: #666; }}
    </style>
</head>
<body>
    <div class="cover">
        <h1>{title}</h1>
        <p>{author}</p>
        <p>{date}</p>
    </div>
</body>
</html>
"""

CSS_TEMPLATE = """
body {
    font-family: "Georgia", serif;
    line-height: 1.6;
    margin: 5%;
    padding: 0;
    color: #333;
}
h1, h2, h3, h4, h5, h6 {
    font-family: "Helvetica", sans-serif;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #1a1a1a;
}
h1 { font-size: 2em; border-bottom: 2px solid #eee; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 0.3em; }
p { margin: 1em 0; text-align: justify; }
blockquote {
    margin: 1em 2em;
    padding: 0.5em 1em;
    border-left: 3px solid #ddd;
    color: #666;
    font-style: italic;
}
code {
    background-color: #f4f4f4;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: "Courier New", monospace;
    font-size: 0.9em;
}
pre {
    background-color: #f4f4f4;
    padding: 1em;
    overflow-x: auto;
    border-radius: 5px;
}
pre code {
    background: none;
    padding: 0;
}
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}
a {
    color: #0066cc;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
.table-of-contents {
    margin: 2em 0;
    padding: 1em;
    background-color: #f9f9f9;
    border-radius: 5px;
}
.table-of-contents ul {
    list-style-type: none;
    padding-left: 0;
}
.table-of-contents li {
    margin: 0.5em 0;
}
"""

class EpubBookGenerator:
    """EPUB 电子书生成器"""
    
    def __init__(self, input_path: str, output_path: str = None, metadata: dict = None):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path) if output_path else self._default_output_path()
        self.metadata = metadata or {}
        self.temp_dir = Path.home() / ".openclaw" / "workspace" / "temp" / "epub"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
    def _default_output_path(self) -> Path:
        """生成默认输出路径"""
        return self.input_path.with_suffix('.epub')
    
    def _extract_metadata(self, md_content: str) -> dict:
        """从 Markdown 提取元数据（支持 YAML Frontmatter）"""
        metadata = {
            'title': self.input_path.stem,
            'author': 'Unknown',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'language': 'zh-CN'
        }
        
        # 检查 YAML Frontmatter
        if md_content.startswith('---'):
            try:
                import yaml
                frontmatter_end = md_content.find('---', 3)
                if frontmatter_end > 0:
                    frontmatter = md_content[3:frontmatter_end].strip()
                    yaml_data = yaml.safe_load(frontmatter)
                    if yaml_data:
                        metadata.update({k: v for k, v in yaml_data.items() if v})
            except ImportError:
                pass
        
        # 从内容提取标题
        lines = md_content.split('\n')
        for line in lines:
            if line.startswith('# ') and 'title' not in self.metadata:
                metadata['title'] = line[2:].strip()
                break
        
        # 用户提供的 metadata 优先级最高
        metadata.update(self.metadata)
        return metadata
    
    def _convert_markdown_to_html(self, md_content: str) -> str:
        """将 Markdown 转换为 HTML"""
        # 使用 markdown 库转换
        html_body = markdown.markdown(
            md_content,
            extensions=[
                'extra',
                'codehilite',
                'toc',
                'tables',
                'fenced_code',
                'meta'
            ]
        )
        
        # 添加 CSS
        full_html = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{self.metadata.get('title', 'EPUB Book')}</title>
    <style>
{CSS_TEMPLATE}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""
        return full_html
    
    def _generate_cover(self) -> str:
        """生成封面 HTML"""
        template = Template(DEFAULT_COVER_TEMPLATE)
        return template.render(
            title=self.metadata.get('title', 'Untitled'),
            author=self.metadata.get('author', 'Unknown'),
            date=self.metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
        )
    
    def generate(self) -> bool:
        """生成 EPUB 电子书"""
        print(f"📖 开始生成 EPUB...")
        print(f"   输入：{self.input_path}")
        print(f"   输出：{self.output_path}")
        
        # 检查输入文件
        if not self.input_path.exists():
            print(f"❌ 输入文件不存在：{self.input_path}")
            return False
        
        # 读取 Markdown 内容
        md_content = self.input_path.read_text(encoding='utf-8')
        
        # 提取元数据
        self.metadata = self._extract_metadata(md_content)
        print(f"   标题：{self.metadata['title']}")
        print(f"   作者：{self.metadata['author']}")
        
        # 转换为 HTML
        html_content = self._convert_markdown_to_html(md_content)
        
        # 生成封面
        cover_html = self._generate_cover()
        
        # 保存临时文件
        content_html_path = self.temp_dir / "content.html"
        cover_html_path = self.temp_dir / "cover.html"
        content_html_path.write_text(html_content, encoding='utf-8')
        cover_html_path.write_text(cover_html, encoding='utf-8')
        
        # 使用 pypandoc 转换为 EPUB
        try:
            print("   正在转换格式...")
            pypandoc.convert_file(
                str(content_html_path),
                'epub',
                outputfile=str(self.output_path),
                extra_args=[
                    '--epub-cover-image', str(cover_html_path),
                    '--epub-title', self.metadata['title'],
                    '--epub-author', self.metadata['author'],
                    '--epub-language', self.metadata.get('language', 'zh-CN'),
                    '--toc', '--toc-depth=3'
                ]
            )
            print(f"✅ EPUB 生成成功：{self.output_path}")
            print(f"   文件大小：{self.output_path.stat().st_size / 1024:.1f} KB")
            return True
        except Exception as e:
            print(f"❌ 转换失败：{e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='Markdown 转 EPUB 电子书生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 epub-book-generator.py book.md
  python3 epub-book-generator.py book.md output.epub
  python3 epub-book-generator.py book.md -o output.epub --title "我的书" --author "作者名"
        """
    )
    
    parser.add_argument('input', help='输入 Markdown 文件路径')
    parser.add_argument('output', nargs='?', help='输出 EPUB 文件路径（可选）')
    parser.add_argument('-o', '--output-file', dest='output_opt', help='输出 EPUB 文件路径')
    parser.add_argument('-t', '--title', help='书籍标题')
    parser.add_argument('-a', '--author', help='作者名称')
    parser.add_argument('-l', '--language', default='zh-CN', help='语言（默认：zh-CN）')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    # 准备元数据
    metadata = {}
    if args.title:
        metadata['title'] = args.title
    if args.author:
        metadata['author'] = args.author
    if args.language:
        metadata['language'] = args.language
    
    # 确定输出路径
    output_path = args.output_opt or args.output
    
    # 生成 EPUB
    generator = EpubBookGenerator(args.input, output_path, metadata)
    success = generator.generate()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
