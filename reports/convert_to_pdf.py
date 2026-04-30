#!/usr/bin/env python3
"""将 Markdown 报告转换为 PDF"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

# 读取 Markdown 文件
md_path = Path('/home/nicola/.openclaw/workspace/reports/工程量清单对比分析报告 (完整版).md')
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# 转换为 HTML
html_content = markdown.markdown(
    md_content,
    extensions=['tables', 'fenced_code', 'toc', 'nl2br'],
    output_format='html5'
)

# 添加完整的 HTML 结构和样式
full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>工程量清单对比分析报告 - 渝中区污水溢流整治项目</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm;
            @bottom-right {{
                content: "第 " counter(page) " 页，共 " counter(pages) " 页";
                font-size: 9pt;
                color: #666;
            }}
            @bottom-left {{
                content: "渝中区污水溢流整治项目";
                font-size: 9pt;
                color: #666;
            }}
        }}
        
        body {{
            font-family: "Noto Sans SC", "Source Han Sans SC", "Microsoft YaHei", sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 10.5pt;
        }}
        
        h1 {{
            font-size: 18pt;
            color: #1a1a1a;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        h2 {{
            font-size: 14pt;
            color: #1e40af;
            border-bottom: 2px solid #3b82f6;
            padding-bottom: 8px;
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        
        h3 {{
            font-size: 12pt;
            color: #1e3a8a;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        h4 {{
            font-size: 11pt;
            color: #1e293b;
            margin-top: 15px;
            margin-bottom: 8px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 9pt;
        }}
        
        th {{
            background-color: #3b82f6;
            color: white;
            padding: 10px 8px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #1e40af;
        }}
        
        td {{
            padding: 8px;
            border: 1px solid #cbd5e1;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}
        
        tr:hover {{
            background-color: #e0f2fe;
        }}
        
        strong {{
            font-weight: 600;
        }}
        
        em {{
            font-style: italic;
        }}
        
        blockquote {{
            border-left: 4px solid #3b82f6;
            margin: 15px 0;
            padding: 10px 15px;
            background-color: #eff6ff;
            color: #1e3a8a;
        }}
        
        code {{
            background-color: #f1f5f9;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
            font-size: 9pt;
        }}
        
        .header-info {{
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .header-info p {{
            margin: 5px 0;
            font-size: 10pt;
        }}
        
        .warning {{
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12px 15px;
            margin: 15px 0;
            color: #92400e;
        }}
        
        .danger {{
            background-color: #fee2e2;
            border-left: 4px solid #ef4444;
            padding: 12px 15px;
            margin: 15px 0;
            color: #991b1b;
        }}
        
        .success {{
            background-color: #dcfce7;
            border-left: 4px solid #22c55e;
            padding: 12px 15px;
            margin: 15px 0;
            color: #166534;
        }}
        
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        .cover-page {{
            text-align: center;
            padding-top: 100px;
        }}
        
        .cover-page h1 {{
            font-size: 24pt;
            border: none;
            color: #1e3a8a;
        }}
        
        .cover-page .subtitle {{
            font-size: 14pt;
            color: #64748b;
            margin: 20px 0;
        }}
        
        .cover-page .info {{
            margin-top: 60px;
            font-size: 11pt;
            color: #475569;
        }}
        
        .cover-page .info p {{
            margin: 8px 0;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #e2e8f0;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <!-- 封面页 -->
    <div class="cover-page">
        <h1>工程量清单对比分析报告</h1>
        <p class="subtitle">渝中区污水溢流整治项目</p>
        <hr style="width: 200px; margin: 40px auto;">
        <div class="info">
            <p><strong>项目名称：</strong>渝中区污水溢流整治项目</p>
            <p><strong>分析范围：</strong>工程量清单（1）、（2）、（3）</p>
            <p><strong>编制时间：</strong>2026 年 4 月 21 日</p>
            <p><strong>编制人：</strong>太一 AGI 系统 (工程造价咨询专家)</p>
            <p><strong>密级：</strong>内部资料 · 注意保管</p>
            <p><strong>版本：</strong>v2.0</p>
        </div>
    </div>
    
    <div class="page-break"></div>
    
    <!-- 正文内容 -->
    {html_content}
    
    <!-- 封底 -->
    <div class="page-break"></div>
    <div style="text-align: center; padding-top: 200px; color: #64748b;">
        <p style="font-size: 10pt;">--- 报告结束 ---</p>
        <p style="font-size: 9pt; margin-top: 30px;">
            本报告仅供内部决策参考，不构成法律意见。<br>
            重大事项建议咨询专业律师或造价咨询机构。
        </p>
        <p style="font-size: 8pt; margin-top: 50px; color: #94a3b8;">
            编制：太一 AGI 系统 | 2026 年 4 月 21 日
        </p>
    </div>
</body>
</html>'''

# 生成 PDF
html_doc = HTML(string=full_html)
pdf_path = Path('/home/nicola/.openclaw/workspace/reports/工程量清单对比分析报告 (完整版).pdf')
html_doc.write_pdf(pdf_path)

print(f"✅ PDF 已生成：{pdf_path}")
print(f"文件大小：{pdf_path.stat().st_size / 1024 / 1024:.2f} MB")
