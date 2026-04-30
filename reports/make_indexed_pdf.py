#!/usr/bin/env python3
import markdown
from weasyprint import HTML
from pathlib import Path

md_path = Path('/home/nicola/.openclaw/workspace/reports/工程量清单对比分析报告 (带位置索引 - 完整版).md')
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'], output_format='html5')

full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>工程量清单对比分析报告 (带位置索引)</title>
    <style>
        @page {{ size: A4; margin: 2.5cm; }}
        body {{ font-family: "Microsoft YaHei", sans-serif; line-height: 1.6; font-size: 10.5pt; }}
        h1 {{ font-size: 18pt; color: #1a1a1a; border-bottom: 3px solid #2563eb; padding-bottom: 10px; text-align: center; }}
        h2 {{ font-size: 14pt; color: #1e40af; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; }}
        h3 {{ font-size: 12pt; color: #1e3a8a; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 9pt; }}
        th {{ background-color: #3b82f6; color: white; padding: 10px 8px; text-align: left; border: 1px solid #1e40af; }}
        td {{ padding: 8px; border: 1px solid #cbd5e1; }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        .verify-column {{ background-color: #dcfce7; width: 80px; }}
        blockquote {{ border-left: 4px solid #3b82f6; margin: 15px 0; padding: 10px 15px; background-color: #eff6ff; }}
        .warning {{ background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px 15px; margin: 15px 0; }}
        .danger {{ background-color: #fee2e2; border-left: 4px solid #ef4444; padding: 12px 15px; margin: 15px 0; }}
        .page-break {{ page-break-before: always; }}
        .cover-page {{ text-align: center; padding-top: 100px; }}
        .cover-page h1 {{ font-size: 22pt; border: none; color: #1e3a8a; }}
    </style>
</head>
<body>
    <div class="cover-page">
        <h1>工程量清单对比分析报告</h1>
        <p style="font-size: 14pt; color: #64748b;">渝中区污水溢流整治项目</p>
        <p style="display: inline-block; background-color: #3b82f6; color: white; padding: 5px 15px; border-radius: 20px; font-size: 10pt;">v3.0 带位置索引·方便人工核验</p>
        <hr style="width: 200px; margin: 30px auto; border-top: 2px solid #e2e8f0;">
        <div style="text-align: left; display: inline-block; font-size: 11pt; color: #475569;">
            <p><strong>项目名称：</strong>渝中区污水溢流突出问题整治项目 (一期) 及大坪街道片区排水管网建设与改造工程 (三期)</p>
            <p><strong>编制时间：</strong>2026 年 4 月 21 日 14:45</p>
            <p><strong>编制人：</strong>太一 AGI 系统 (造价工程师)</p>
            <p><strong>复核人：</strong>造价 agent 专业模块</p>
            <p><strong>密级：</strong>内部资料 · 注意保管</p>
        </div>
    </div>
    <div class="page-break"></div>
    {html_content}
</body>
</html>'''

html_doc = HTML(string=full_html)
pdf_path = Path('/home/nicola/.openclaw/workspace/reports/工程量清单对比分析报告 (带位置索引 - 完整版).pdf')
html_doc.write_pdf(pdf_path)
print(f'✅ PDF 已生成：{pdf_path}')
print(f'文件大小：{pdf_path.stat().st_size / 1024 / 1024:.2f} MB')
