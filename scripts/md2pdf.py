#!/usr/bin/env python3
"""
Markdown 转 PDF 生成器
使用 reportlab 生成专业 PDF 报告
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import re

# 注册中文字体（使用系统字体）
font_paths = [
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]

registered_font = False
for font_path in font_paths:
    try:
        pdfmetrics.registerFont(TTFont('Chinese', font_path))
        registered_font = True
        break
    except:
        continue

def create_pdf(md_file, pdf_file):
    """从 Markdown 创建 PDF"""
    
    # 读取 Markdown 文件
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建 PDF 文档
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 样式
    styles = getSampleStyleSheet()
    
    # 中文字体样式
    if registered_font:
        font_name = 'Chinese'
    else:
        font_name = 'Helvetica'
    
    title_style = ParagraphStyle(
        'ChineseTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=18,
        leading=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading1_style = ParagraphStyle(
        'ChineseH1',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=16,
        leading=20,
        spaceAfter=12,
        spaceBefore=20
    )
    
    heading2_style = ParagraphStyle(
        'ChineseH2',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        leading=18,
        spaceAfter=10,
        spaceBefore=15
    )
    
    heading3_style = ParagraphStyle(
        'ChineseH3',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=12,
        leading=16,
        spaceAfter=8,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        'ChineseNormal',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=14,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'ChineseCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        spaceAfter=6,
        textColor=colors.darkgreen
    )
    
    # 构建内容
    story = []
    
    # 标题
    story.append(Paragraph("重庆/西南海关集成式房屋出口退税政策研究报告", title_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"调研时间：{datetime.now().strftime('%Y-%m-%d')}", normal_style))
    story.append(Paragraph("调研范围：重庆海关、西南海关、国家税务总局", normal_style))
    story.append(Spacer(1, 0.5*cm))
    
    # 解析 Markdown 内容
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # 标题
        if line.startswith('## '):
            story.append(Paragraph(line[3:].strip(), heading1_style))
            i += 1
        elif line.startswith('### '):
            story.append(Paragraph(line[4:].strip(), heading2_style))
            i += 1
        elif line.startswith('#### '):
            story.append(Paragraph(line[5:].strip(), heading3_style))
            i += 1
        # 代码块
        elif line.startswith('```'):
            code_content = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_content.append(lines[i])
                i += 1
            if code_content:
                code_text = '<br/>'.join(code_content)
                story.append(Paragraph(code_text, code_style))
            i += 1
        # 表格
        elif line.startswith('|') and '---' not in line:
            table_data = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                if '---' in lines[i]:
                    i += 1
                    continue
                row = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                table_data.append(row)
                i += 1
            if table_data:
                table = Table(table_data, colWidths=[4*cm, 6*cm, 3*cm, 5*cm])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), font_name),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('FONTNAME', (0, 1), (-1, -1), font_name),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                story.append(table)
                story.append(Spacer(1, 0.3*cm))
        # 普通段落
        elif line and not line.startswith('-') and not line.startswith('*') and not line.startswith('['):
            # 清理 Markdown 格式
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            clean_line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line)
            clean_line = re.sub(r'`([^`]+)`', r'\1', clean_line)
            story.append(Paragraph(clean_line, normal_style))
            i += 1
        else:
            i += 1
    
    # 构建 PDF
    doc.build(story)
    print(f"✅ PDF 已生成：{pdf_file}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        create_pdf(sys.argv[1], sys.argv[2])
    else:
        print("用法：python3 md2pdf.py <input.md> <output.pdf>")
