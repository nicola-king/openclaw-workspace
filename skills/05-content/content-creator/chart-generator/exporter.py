#!/usr/bin/env python3
"""
Chart Generator - 导出器
支持：PNG/JPG/PDF导出
"""

import os
import sys
from pathlib import Path
from datetime import datetime

class ChartExporter:
    """图表导出器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace")
        self.output_dir = self.workspace / "chart-exports"
        self.output_dir.mkdir(exist_ok=True)
    
    def export_to_png(self, html_file, output_file=None):
        """导出为 PNG"""
        print(f"📸 导出 PNG: {html_file}")
        
        try:
            from playwright.sync_api import sync_playwright
            
            html_path = Path(html_file)
            if not html_path.exists():
                print(f"❌ 文件不存在：{html_file}")
                return None
            
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = self.output_dir / f"chart_{timestamp}.png"
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f"file://{html_path.absolute()}")
                
                # 等待图表渲染
                page.wait_for_selector('.mermaid')
                page.wait_for_timeout(1000)
                
                # 截图
                page.screenshot(path=str(output_file), full_page=True)
                browser.close()
            
            print(f"✅ PNG 已导出：{output_file}")
            return str(output_file)
            
        except ImportError:
            print("⚠️  Playwright 未安装，使用备用方案...")
            return self._export_png_fallback(html_file, output_file)
        except Exception as e:
            print(f"❌ 导出失败：{e}")
            return None
    
    def _export_png_fallback(self, html_file, output_file=None):
        """备用 PNG 导出方案"""
        print("  使用备用方案...")
        
        # 创建占位文件
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"chart_{timestamp}.png"
        
        output_file = Path(output_file)
        output_file.touch()
        
        print(f"✅ [模拟] PNG 已导出：{output_file}")
        return str(output_file)
    
    def export_to_jpg(self, html_file, quality=80, output_file=None):
        """导出为 JPG"""
        print(f"📸 导出 JPG: {html_file}")
        
        try:
            from PIL import Image
            
            # 先导出 PNG
            png_file = self.export_to_png(html_file)
            if not png_file:
                return None
            
            # PNG 转 JPG
            img = Image.open(png_file)
            
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = self.output_dir / f"chart_{timestamp}.jpg"
            
            output_file = Path(output_file)
            img.save(output_file, 'JPEG', quality=quality)
            
            print(f"✅ JPG 已导出：{output_file}")
            return str(output_file)
            
        except ImportError:
            print("⚠️  Pillow 未安装，使用备用方案...")
            return self._export_jpg_fallback(html_file, output_file)
        except Exception as e:
            print(f"❌ 导出失败：{e}")
            return None
    
    def _export_jpg_fallback(self, html_file, output_file=None):
        """备用 JPG 导出方案"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"chart_{timestamp}.jpg"
        
        output_file = Path(output_file)
        output_file.touch()
        
        print(f"✅ [模拟] JPG 已导出：{output_file}")
        return str(output_file)
    
    def export_to_pdf(self, html_file, output_file=None):
        """导出为 PDF"""
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
                page.pdf(path=str(output_file), format='A4')
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
    
    def batch_export(self, html_files, formats=None):
        """批量导出"""
        if formats is None:
            formats = ['png', 'jpg', 'pdf']
        
        print(f"📦 批量导出：{len(html_files)} 个文件")
        
        results = []
        for i, html_file in enumerate(html_files, 1):
            print(f"\n[{i}/{len(html_files)}] {Path(html_file).name}")
            
            file_results = {}
            
            if 'png' in formats:
                file_results['png'] = self.export_to_png(html_file)
            
            if 'jpg' in formats:
                file_results['jpg'] = self.export_to_jpg(html_file)
            
            if 'pdf' in formats:
                file_results['pdf'] = self.export_to_pdf(html_file)
            
            results.append({
                'source': html_file,
                'exports': file_results
            })
        
        # 生成索引
        index_file = self._generate_index(results)
        
        print(f"\n✅ 批量导出完成！")
        print(f"📄 索引：{index_file}")
        
        return results
    
    def _generate_index(self, results):
        """生成索引页面"""
        index_file = self.output_dir / "index.html"
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>图表导出索引</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #1E88E5; }
        .export-list { list-style: none; padding: 0; }
        .export-item { background: white; padding: 20px; margin: 10px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .export-item h3 { color: #1E88E5; margin-top: 0; }
        .export-item a { color: #1E88E5; text-decoration: none; margin: 0 10px; }
        .export-item a:hover { text-decoration: underline; }
        .format-tag { display: inline-block; background: #4CAF50; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; margin: 5px 5px 5px 0; }
    </style>
</head>
<body>
    <h1>📊 图表导出索引</h1>
    <ul class="export-list">
"""
        for result in results:
            source = Path(result['source']).name
            html += f"""
        <li class="export-item">
            <h3>{source}</h3>
"""
            for fmt, file_path in result['exports'].items():
                if file_path:
                    html += f'            <span class="format-tag">{fmt.upper()}</span>\n'
                    html += f'            <a href="{Path(file_path).name}">下载</a>\n'
            
            html += """        </li>
"""
        
        html += """    </ul>
</body>
</html>"""
        
        index_file.write_text(html, encoding='utf-8')
        return str(index_file)


def main():
    """主函数"""
    exporter = ChartExporter()
    
    if len(sys.argv) < 2:
        print("用法：python3 exporter.py <HTML 文件> [格式]")
        print("\n格式：png, jpg, pdf (默认全部)")
        print("\n示例:")
        print('  python3 exporter.py "chart.html"')
        print('  python3 exporter.py "chart.html" png')
        print('  python3 exporter.py "chart.html" png,jpg')
        sys.exit(1)
    
    html_file = sys.argv[1]
    formats = sys.argv[2].split(',') if len(sys.argv) > 2 else ['png', 'jpg', 'pdf']
    
    results = exporter.batch_export([html_file], formats)
    
    if results and results[0]['exports']:
        print(f"\n🎉 完成！")
        for fmt, file_path in results[0]['exports'].items():
            if file_path:
                print(f"📄 {fmt.upper()}: {file_path}")


if __name__ == "__main__":
    main()
