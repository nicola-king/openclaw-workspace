#!/usr/bin/env python3
"""简易 Markdown 转 HTML（无需外部依赖）"""
import re
import sys
from pathlib import Path

def md_to_html(md_text):
    """Markdown 转 HTML"""
    html = md_text
    
    # 标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 斜体
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 代码
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # 链接
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # 列表
    lines = html.split('\n')
    in_ul = False
    result = []
    for line in lines:
        if line.startswith('- '):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            result.append(f'<li>{line[2:]}</li>')
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if line.strip():
                result.append(f'<p>{line}</p>')
            else:
                result.append('')
    if in_ul:
        result.append('</ul>')
    
    html = '\n'.join(result)
    
    return html

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 simple-md2html.py <文件.md> [输出.html]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else md_file.replace('.md', '.html')
    
    md_path = Path(md_file)
    md_content = md_path.read_text(encoding='utf-8')
    
    html_content = md_to_html(md_content)
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{md_path.stem}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ color: #1E88E5; border-bottom: 2px solid #1E88E5; padding-bottom: 10px; }}
        h2 {{ color: #1E88E5; margin-top: 30px; }}
        h3 {{ color: #0D47A1; }}
        code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
        pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        ul {{ margin: 15px 0; padding-left: 30px; }}
        li {{ margin: 5px 0; }}
        a {{ color: #1E88E5; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(html_template, encoding='utf-8')
    
    print(f"✅ HTML 已生成：{output_file}")
    print(f"🌐 访问：file://{output_path.absolute()}")
