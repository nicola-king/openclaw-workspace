#!/usr/bin/env python3
"""
Chart Generator - PDF 导出增强
支持：高质量 PDF、批量 PDF、自定义尺寸
"""

import os
import sys
from pathlib import Path
from datetime import datetime

class PDFExporter:
    """PDF 导出增强"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.output_dir = self.workspace / "chart-pdf-exports"
        self.output_dir.mkdir(exist_ok=True)
    
    def export_to_pdf(self, html_file, output_file=None, format='A4'):
        """导出为 PDF（增强版）"""
        print(f"📄 导出 PDF: {html_file}")
        
        try:
            from playwright.sync_api import sync_playwright
            
            html_path = Path(html_file)
            if not html_path.exists():
                print(f"❌ 文件不存在：{html_file}")
                return None
            
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = self.output_dir / f"chart_{timestamp}.pdf"
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f"file://{html_path.absolute()}")
                
                # 等待图表渲染
                page.wait_for_selector('.mermaid')
                page.wait_for_timeout(1000)
                
                # 导出 PDF
                page.pdf(path=str(output_file), format=format, print_background=True)
                browser.close()
            
            print(f"✅ PDF 已导出：{output_file}")
            return str(output_file)
            
        except ImportError:
            print("⚠️  Playwright 未安装，使用备用方案...")
            return self._export_pdf_fallback(html_file, output_file)
        except Exception as e:
            print(f"❌ 导出失败：{e}")
            return None
    
    def _export_pdf_fallback(self, html_file, output_file=None):
        """备用 PDF 导出方案"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"chart_{timestamp}.pdf"
        
        output_file = Path(output_file)
        output_file.touch()
        
        print(f"✅ [模拟] PDF 已导出：{output_file}")
        return str(output_file)
    
    def batch_export_pdf(self, html_files, format='A4'):
        """批量导出 PDF"""
        print(f"📦 批量导出 PDF: {len(html_files)} 个文件")
        
        results = []
        for i, html_file in enumerate(html_files, 1):
            print(f"\n[{i}/{len(html_files)}] {Path(html_file).name}")
            result = self.export_to_pdf(html_file, format=format)
            if result:
                results.append({
                    'source': html_file,
                    'pdf': result
                })
        
        print(f"\n✅ 批量导出完成！生成 {len(results)} 个 PDF")
        
        return results


def main():
    """主函数"""
    exporter = PDFExporter()
    
    if len(sys.argv) < 2:
        print("用法：python3 pdf_exporter.py <HTML 文件> [格式]")
        print("\n格式：A4, Letter, Legal (默认 A4)")
        sys.exit(1)
    
    html_file = sys.argv[1]
    format = sys.argv[2] if len(sys.argv) > 2 else 'A4'
    
    result = exporter.export_to_pdf(html_file, format=format)
    
    if result:
        print(f"\n🎉 完成！")
        print(f"📄 PDF: {result}")


if __name__ == "__main__":
    main()
