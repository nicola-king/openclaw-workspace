#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Markdown/CSV 报告转换为 PDF
使用 reportlab 库生成专业 PDF 报告
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import csv
import os

# 注册中文字体
try:
    pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
    pdfmetrics.registerFont(TTFont('SimHei', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
except:
    try:
        pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'))
        pdfmetrics.registerFont(TTFont('SimHei', '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'))
    except:
        print("⚠️ 未找到中文字体，使用默认字体")

def create_title_page(doc, title, subtitle=""):
    """创建封面页"""
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5276'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='SimHei'
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.grey,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='SimSun'
    )
    
    story = []
    story.append(Spacer(1, 8*cm))
    story.append(Paragraph(title, title_style))
    if subtitle:
        story.append(Paragraph(subtitle, subtitle_style))
    story.append(Spacer(1, 2*cm))
    
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.darkgrey,
        alignment=TA_CENTER,
        fontName='SimSun'
    )
    story.append(Paragraph("编制时间：2026-03-31", info_style))
    story.append(Paragraph("编制人：太一 AGI 系统 (工程造价咨询专家)", info_style))
    story.append(Paragraph("密级：内部资料 · 注意保管", info_style))
    
    doc.build(story)

def create_csv_pdf(csv_file, pdf_file, title):
    """将 CSV 文件转换为 PDF"""
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                           rightMargin=1*cm, leftMargin=1*cm,
                           topMargin=1.5*cm, bottomMargin=1.5*cm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a5276'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='SimHei'
    )
    
    # 读取 CSV
    data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    
    if not data:
        return
    
    # 创建 PDF
    story = []
    
    # 标题
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.3*cm))
    
    # 表格
    table = Table(data, repeatRows=1)
    
    # 表格样式
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]
    table.setStyle(TableStyle(table_style))
    
    story.append(table)
    
    # 页脚
    story.append(Spacer(1, 1*cm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName='SimSun'
    )
    story.append(Paragraph(f"第 1 页 / 共 1 页 · 编制时间：2026-03-31 · 太一 AGI 系统", footer_style))
    
    doc.build(story)
    print(f"  ✅ {pdf_file}")

def create_md_pdf(md_file, pdf_file, title):
    """将 Markdown 文件转换为 PDF (简化版)"""
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                           rightMargin=1.5*cm, leftMargin=1.5*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a5276'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='SimHei'
    )
    
    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#2874a6'),
        spaceAfter=15,
        spaceBefore=20,
        fontName='SimHei'
    )
    
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#3498db'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='SimHei'
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        fontName='SimSun',
        alignment=TA_JUSTIFY
    )
    
    # 读取 Markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    story = []
    
    # 标题
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.5*cm))
    
    # 简单解析 Markdown
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('>'):
            continue
        
        if line.startswith('# '):
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph(line[2:], heading1_style))
        elif line.startswith('## '):
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph(line[3:], heading2_style))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], normal_style))
        elif line.startswith('|') and '---' not in line:
            # 表格行
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if cells:
                table = Table([cells], colWidths=[4*cm]*len(cells))
                table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                story.append(table)
        elif line.startswith('- ') or line.startswith('* '):
            story.append(Paragraph(f"• {line[2:]}", normal_style))
        elif len(line) > 10:
            story.append(Paragraph(line, normal_style))
        
        story.append(Spacer(1, 0.1*cm))
    
    # 页脚
    story.append(Spacer(1, 1*cm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName='SimSun'
    )
    story.append(Paragraph(f"编制时间：2026-03-31 · 太一 AGI 系统", footer_style))
    
    doc.build(story)
    print(f"  ✅ {pdf_file}")

if __name__ == '__main__':
    print("=" * 80)
    print("生成 PDF 报告文件...")
    print("=" * 80)
    
    reports_dir = '/home/nicola/.openclaw/workspace/reports'
    os.chdir(reports_dir)
    
    # 1. 合同文件汇总表
    print("\n1. 合同文件汇总表.pdf")
    create_csv_pdf('合同文件汇总表.csv', '合同文件汇总表.pdf', '合同文件汇总表')
    
    # 2. 招标文件 vs 主合同冲突分析表
    print("2. 招标文件 vs 主合同冲突分析表.pdf")
    create_csv_pdf('招标文件 vs 主合同冲突分析表.csv', '招标文件 vs 主合同冲突分析表.pdf', '招标文件 vs 主合同冲突分析表')
    
    # 3. 工程量清单差异明细表
    print("3. 工程量清单差异明细表.pdf")
    create_csv_pdf('37 项差异汇总表.csv', '工程量清单差异明细表.pdf', '工程量清单 37 项差异明细表')
    
    # 4. 降本增效策略表
    print("4. 降本增效策略表.pdf")
    create_csv_pdf('降本增效策略表.csv', '降本增效策略表.pdf', '降本增效策略表')
    
    # 5. 措施项目优化表
    print("5. 措施项目优化表.pdf")
    create_csv_pdf('措施项目优化表.csv', '措施项目优化表.pdf', '措施项目优化表')
    
    # 6. 行动计划表
    print("6. 行动计划表.pdf")
    create_csv_pdf('行动计划表.csv', '行动计划表.pdf', '行动计划表')
    
    # 7. 安全文明施工费 vs 围挡费专项分析
    print("7. 安全文明施工费 vs 围挡费专项分析.pdf")
    create_md_pdf('安全文明施工费 vs 围挡费专项分析.md', '安全文明施工费 vs 围挡费专项分析.pdf', 
                  '安全文明施工费 vs 现场施工围挡费专项分析报告')
    
    # 8. 工程量清单 37 项差异明细表 (完整版)
    print("8. 工程量清单 37 项差异明细表 (完整版).pdf")
    create_md_pdf('工程量清单 37 项差异明细表.md', '工程量清单 37 项差异明细表 (完整版).pdf',
                  '工程量清单 37 项差异明细表')
    
    print("\n" + "=" * 80)
    print("✅ 所有 PDF 文件生成完成！")
    print("=" * 80)
    
    # 列出所有 PDF
    print("\nPDF 文件列表:")
    import subprocess
    result = subprocess.run(['ls', '-lh', '*.pdf'], capture_output=True, text=True, shell=True, cwd=reports_dir)
    print(result.stdout)
