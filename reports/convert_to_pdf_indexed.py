#!/usr/bin/env python3
"""将带位置索引的 Markdown 报告转换为 PDF"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

# 读取 Markdown 文件
md_path = Path('/home/nicola/.openclaw/workspace/reports/工程量清单对比分析报告 (带位置索引 - 完整版).md')
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
    <title>工程量清单对比分析报告 (带位置索引) - 渝中区污水溢流整治项目</title>
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
        
        .index-column {{
            background-color: #fef3c7;
            font-weight: 600;
        }}
        
        .verify-column {{
            background-color: #dcfce7;
            width: 80px;
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
        
        .usage-box {{
            background-color: #f0f9ff;
            border: 2px solid #0ea5e9;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .usage-box h3 {{
            margin-top: 0;
            color: #0369a1;
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
            padding-top: 80px;
        }}
        
        .cover-page h1 {{
            font-size: 22pt;
            border: none;
            color: #1e3a8a;
        }}
        
        .cover-page .subtitle {{
            font-size: 14pt;
            color: #64748b;
            margin: 15px 0;
        }}
        
        .cover-page .version-badge {{
            display: inline-block;
            background-color: #3b82f6;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 10pt;
            margin: 10px 0;
        }}
        
        .cover-page .info {{
            margin-top: 50px;
            font-size: 11pt;
            color: #475569;
            text-align: left;
            display: inline-block;
        }}
        
        .cover-page .info p {{
            margin: 8px 0;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #e2e8f0;
            margin: 30px 0;
        }}
        
        .toc {{
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .toc h3 {{
            margin-top: 0;
            color: #1e40af;
        }}
        
        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        
        .toc li {{
            margin: 8px 0;
            padding-left: 20px;
        }}
        
        .toc a {{
            color: #1e40af;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <!-- 封面页 -->
    <div class="cover-page">
        <h1>工程量清单对比分析报告</h1>
        <p class="subtitle">渝中区污水溢流整治项目</p>
        <p class="version-badge">v3.0 带位置索引·方便人工核验</p>
        <hr style="width: 200px; margin: 30px auto;">
        <div class="info">
            <p><strong>项目名称：</strong>渝中区污水溢流突出问题整治项目 (一期) 及大坪街道片区排水管网建设与改造工程 (三期)</p>
            <p><strong>分析范围：</strong>工程量清单（1）、（2）、（3）</p>
            <p><strong>编制时间：</strong>2026 年 4 月 21 日 14:45</p>
            <p><strong>编制人：</strong>太一 AGI 系统 (造价工程师)</p>
            <p><strong>复核人：</strong>造价 agent 专业模块</p>
            <p><strong>密级：</strong>内部资料 · 注意保管</p>
        </div>
        
        <div class="usage-box" style="margin-top: 40px; text-align: left;">
            <h3 style="margin-top: 0;">📋 使用说明</h3>
            <p><strong>位置索引说明：</strong></p>
            <ul>
                <li><strong>项目编码：</strong>国标清单编码，可在三份清单中直接搜索定位</li>
                <li><strong>项目名称：</strong>清单项目名称，可辅助定位</li>
                <li><strong>专业分类：</strong>标注所属专业（拆除/排水/道路等）</li>
                <li><strong>原始位置：</strong>请打开原始清单文件，填写实际页码/行号</li>
            </ul>
            <p><strong>人工核验步骤：</strong></p>
            <ol>
                <li>打开工程量清单（1）、（2）、（3）Excel 文件</li>
                <li>使用"查找"功能搜索<strong>项目编码</strong></li>
                <li>对比三份清单中该项目的名称、特征、单价</li>
                <li>在本报告的"原始位置"栏填写实际页码/行号</li>
                <li>完成核验后在"核验确认"栏签字</li>
            </ol>
        </div>
    </div>
    
    <div class="page-break"></div>
    
    <!-- 目录页 -->
    <div class="toc">
        <h3>📑 目录</h3>
        <ul>
            <li>使用说明</li>
            <li>差异汇总</li>
            <li>一、类型 1: 项目编码相同，项目名称不同 (15 项)</li>
            <li>二、类型 2: 项目名称相同，项目特征不同 (22 项)</li>
            <li>三、类型 3: 项目名称相同，综合单价不同 (0 项)</li>
            <li>四、措施项目费对比分析</li>
            <li>五、差异汇总统计</li>
            <li>六、人工核验指引</li>
            <li>七、风险提示与建议</li>
            <li>八、结论</li>
            <li>九、数据来源说明</li>
        </ul>
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
            编制：太一 AGI 系统 (造价工程师) | 复核：造价 agent 专业模块 | 2026 年 4 月 21 日
        </p>
    </div>
</body>
</html>'''

# 生成 PDF
html_doc = HTML(string=full_html)
pdf_path = Path('/home/nicola/.openclaw/workspace/reports/工程量清单对比分析报告 (带位置索引 - 完整版).pdf')
html_doc.write_pdf(pdf_path)

print(f"✅ PDF 已生成：{pdf_path}")
print(f"文件大小：{pdf_path.stat().st_size / 1024 / 1024:.2f} MB")
