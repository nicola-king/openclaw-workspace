#!/usr/bin/env python3
"""
Markdown to PDF converter
Using markdown2 + pdfkit (wkhtmltopdf)
"""

import markdown2
import sys
from pathlib import Path

def convert_md_to_pdf(md_file, pdf_file=None):
    """Convert Markdown to PDF"""
    md_path = Path(md_file)
    
    if not md_path.exists():
        print(f"❌ 文件不存在：{md_file}")
        return False
    
    if pdf_file is None:
        pdf_file = str(md_path.with_suffix('.pdf'))
    
    # Read Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown2.markdown(md_content, extras=['tables', 'toc', 'fenced-code'])
    
    # Add HTML template
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw 案例融合方案</title>
    <style>
        @page {{
            size: A4;
            margin: 25mm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 25mm;
        }}
        h1 {{
            color: #1E88E5;
            border-bottom: 3px solid #1E88E5;
            padding-bottom: 15px;
            font-size: 24pt;
            page-break-before: always;
        }}
        h1:first-of-type {{
            page-break-before: avoid;
        }}
        h2 {{
            color: #1E88E5;
            margin-top: 30px;
            font-size: 18pt;
        }}
        h3 {{
            color: #0D47A1;
            font-size: 14pt;
        }}
        h4 {{
            color: #333;
            font-size: 12pt;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", Courier, monospace;
        }}
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            page-break-inside: auto;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #1E88E5;
            color: white;
        }}
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        blockquote {{
            border-left: 4px solid #1E88E5;
            margin: 20px 0;
            padding-left: 20px;
            color: #666;
        }}
        .card {{
            border: 2px solid #1E88E5;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            background: #f9f9f9;
        }}
        .card-title {{
            color: #1E88E5;
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        @media print {{
            body {{
                padding: 0;
            }}
            h1 {{
                page-break-before: always;
            }}
            a {{
                text-decoration: none;
                color: #333;
            }}
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # Save HTML
    html_file = str(md_path.with_suffix('.html'))
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"✅ HTML 已生成：{html_file}")
    print(f"📝 请使用浏览器打开并打印为 PDF:")
    print(f"   1. 打开 {html_file}")
    print(f"   2. Ctrl+P (打印)")
    print(f"   3. 选择'另存为 PDF'")
    print(f"   4. 设置：A4, 双面，彩色")
    print(f"   5. 保存")
    
    # Try to use pdfkit if available
    try:
        import pdfkit
        pdfkit.from_string(html_template, pdf_file)
        print(f"✅ PDF 已生成：{pdf_file}")
        return True
    except ImportError:
        print(f"⚠️  pdfkit 未安装，请使用浏览器打印 HTML 文件生成 PDF")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 convert-md-to-pdf.py <markdown 文件> [PDF 文件名]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_md_to_pdf(md_file, pdf_file)
