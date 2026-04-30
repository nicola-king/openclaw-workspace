#!/usr/bin/env python3
"""
MD 转 PDF 转换器
太一 AGI · 2026-04-18

功能:
- Markdown 转 PDF
- 支持中文
- 美化样式
- 适合移动端阅读
"""

import os
from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle


class MDToPDFConverter:
    """MD 转 PDF 转换器"""
    
    def __init__(self):
        # 注册中文字体
        font_dir = Path("/usr/share/fonts/truetype/noto")
        if font_dir.exists():
            for font_file in font_dir.glob("*.ttf"):
                try:
                    pdfmetrics.registerFont(TTFont("Noto", str(font_file)))
                    self.chinese_font = "Noto"
                    break
                except:
                    continue
        else:
            # 备用字体
            self.chinese_font = "Helvetica"
        
        # 样式配置
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """设置样式"""
        # 标题样式
        self.styles.add(ParagraphStyle(
            name='ChineseTitle',
            parent=self.styles['Heading1'],
            fontName=self.chinese_font,
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=30,
            alignment=1,  # 居中
        ))
        
        # 副标题样式
        self.styles.add(ParagraphStyle(
            name='ChineseSubtitle',
            parent=self.styles['Heading2'],
            fontName=self.chinese_font,
            fontSize=16,
            textColor=colors.HexColor('#16213e'),
            spaceAfter=20,
            spaceBefore=10,
        ))
        
        # 正文样式
        self.styles.add(ParagraphStyle(
            name='ChineseNormal',
            parent=self.styles['Normal'],
            fontName=self.chinese_font,
            fontSize=12,
            textColor=colors.HexColor('#333333'),
            leading=20,  # 行距
            spaceAfter=10,
        ))
        
        # 引用样式
        self.styles.add(ParagraphStyle(
            name='ChineseQuote',
            parent=self.styles['Normal'],
            fontName=self.chinese_font,
            fontSize=14,
            textColor=colors.HexColor('#0f3460'),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=15,
            spaceBefore=15,
            borderLeftWidth=3,
            borderLeftColor=colors.HexColor('#e94560'),
        ))
        
        # 日期样式
        self.styles.add(ParagraphStyle(
            name='ChineseDate',
            parent=self.styles['Normal'],
            fontName=self.chinese_font,
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            alignment=2,  # 右对齐
            spaceAfter=20,
        ))
    
    def convert(self, md_file, output_pdf=None):
        """转换 MD 为 PDF
        
        Args:
            md_file: Markdown 文件路径
            output_pdf: 输出 PDF 路径 (可选)
        
        Returns:
            pdf_path: PDF 文件路径
        """
        md_path = Path(md_file)
        if not md_path.exists():
            print(f"❌ 文件不存在：{md_file}")
            return None
        
        # 生成输出路径
        if output_pdf is None:
            output_pdf = md_path.with_suffix('.pdf')
        
        print(f"📄 转换 MD 为 PDF")
        print(f"   输入：{md_file}")
        print(f"   输出：{output_pdf}")
        
        # 读取 MD 内容
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 解析 MD 内容
        story = self._parse_markdown(md_content)
        
        # 创建 PDF
        doc = SimpleDocTemplate(
            str(output_pdf),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )
        
        doc.build(story)
        
        print(f"✅ PDF 生成成功：{output_pdf}")
        return str(output_pdf)
    
    def _parse_markdown(self, content):
        """解析 Markdown 内容
        
        Args:
            content: Markdown 内容
        
        Returns:
            story: PDF 元素列表
        """
        story = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.3*cm))
                continue
            
            # 标题 (#)
            if line.startswith('# '):
                title = line[2:]
                story.append(Paragraph(title, self.styles['ChineseTitle']))
                story.append(Spacer(1, 0.5*cm))
            
            # 副标题 (##)
            elif line.startswith('## '):
                subtitle = line[3:]
                story.append(Paragraph(subtitle, self.styles['ChineseSubtitle']))
                story.append(Spacer(1, 0.3*cm))
            
            # 引用 (>)
            elif line.startswith('>'):
                quote = line[1:].strip()
                story.append(Paragraph(quote, self.styles['ChineseQuote']))
                story.append(Spacer(1, 0.3*cm))
            
            # 普通文本
            else:
                # 处理简单格式
                text = line.replace('**', '').replace('*', '')
                story.append(Paragraph(text, self.styles['ChineseNormal']))
        
        return story
    
    def create_wisdom_card(self, wisdom_type, content, date=None):
        """创建智慧卡片 PDF
        
        Args:
            wisdom_type: 智慧类型 (dao/wu)
            content: 智慧内容
            date: 日期 (可选)
        
        Returns:
            pdf_path: PDF 文件路径
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 创建临时 MD 文件
        md_content = f"""# {"📿 道 · 晨间智慧" if wisdom_type == "dao" else "🌙 悟 · 晚间智慧"}

**{date}**

---

{content}

---

太一 AGI · {"道 Agent" if wisdom_type == "dao" else "悟 Agent"}
"""
        
        # 保存 MD
        output_dir = Path("/home/nicola/.openclaw/workspace") / "wisdom-pdf"
        output_dir.mkdir(exist_ok=True)
        
        md_file = output_dir / f"{wisdom_type}-{date}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # 转换为 PDF
        pdf_file = output_dir / f"{wisdom_type}-{date}.pdf"
        return self.convert(md_file, pdf_file)


def main():
    """主函数"""
    print("=" * 60)
    print("📄 MD 转 PDF 转换器")
    print("太一 AGI · 2026-04-18")
    print("=" * 60)
    
    converter = MDToPDFConverter()
    
    # 示例：转换道 Agent 智慧
    dao_md = "/home/nicola/.openclaw/workspace/skills/05-content/dao-agent/data/output/dao-20260418.md"
    if Path(dao_md).exists():
        converter.convert(dao_md)
    
    # 示例：转换悟 Agent 智慧
    wu_md = "/home/nicola/.openclaw/workspace/skills/05-content/wu-agent/data/output/wu-20260417.md"
    if Path(wu_md).exists():
        converter.convert(wu_md)


if __name__ == "__main__":
    main()
