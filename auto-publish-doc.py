#!/usr/bin/env python3
"""
OpenClaw 文档自动化发布系统
功能：Markdown → HTML → PDF → Telegram 全自动发布
用法：python3 auto-publish-doc.py <markdown 文件>
"""

import os
import sys
import requests
import markdown2
from pathlib import Path
from datetime import datetime

# Telegram Bot 配置
BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
CHAT_ID = "7073481596"

class AutoPublishDoc:
    """文档自动化发布系统"""
    
    def __init__(self, md_file):
        self.md_path = Path(md_file)
        self.html_path = self.md_path.with_suffix('.html')
        self.pdf_path = self.md_path.with_suffix('.pdf')
        
        if not self.md_path.exists():
            raise FileNotFoundError(f"❌ 文件不存在：{md_file}")
        
        print(f"📄 输入文件：{self.md_path.name}")
        print(f"📊 文件大小：{self.md_path.stat().st_size / 1024:.1f} KB")
    
    def step1_md_to_html(self):
        """步骤 1: Markdown → HTML"""
        print("\n" + "="*60)
        print("步骤 1/3: Markdown → HTML")
        print("="*60)
        
        try:
            with open(self.md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code', 'toc'])
            
            html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw 案例融合方案</title>
    <style>
        @page {{ size: A4; margin: 25mm; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 210mm;
            margin: 0 auto;
            padding: 25mm;
            color: #333;
            background: white;
        }}
        h1 {{
            color: #1E88E5;
            border-bottom: 3px solid #1E88E5;
            padding-bottom: 15px;
            font-size: 24pt;
            page-break-before: always;
        }}
        h1:first-of-type {{ page-break-before: avoid; }}
        h2 {{ color: #1E88E5; margin-top: 30px; font-size: 18pt; page-break-after: avoid; }}
        h3 {{ color: #0D47A1; font-size: 14pt; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; page-break-inside: auto; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #1E88E5; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .card {{
            border: 2px solid #1E88E5;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            background: #f9f9f9;
            page-break-inside: avoid;
        }}
        .card-title {{ color: #1E88E5; font-size: 16pt; font-weight: bold; margin-bottom: 15px; }}
        @media print {{ body {{ padding: 0; }} a {{ text-decoration: none; color: #333; }} }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
            
            with open(self.html_path, 'w', encoding='utf-8') as f:
                f.write(html_template)
            
            print(f"✅ HTML 已生成：{self.html_path.name}")
            print(f"📊 HTML 大小：{self.html_path.stat().st_size / 1024:.1f} KB")
            return True
            
        except Exception as e:
            print(f"❌ HTML 生成失败：{e}")
            return False
    
    def step2_html_to_pdf(self):
        """步骤 2: HTML → PDF (Chrome Headless)"""
        print("\n" + "="*60)
        print("步骤 2/3: HTML → PDF")
        print("="*60)
        
        import subprocess
        
        try:
            cmd = [
                'google-chrome',
                '--headless',
                '--disable-gpu',
                f'--print-to-pdf={self.pdf_path}',
                str(self.html_path)
            ]
            
            print(f"🖨️  执行：google-chrome --headless ...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if self.pdf_path.exists():
                size = self.pdf_path.stat().st_size / 1024
                print(f"✅ PDF 已生成：{self.pdf_path.name}")
                print(f"📊 PDF 大小：{size:.1f} KB")
                return True
            else:
                print(f"❌ PDF 生成失败：{result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ PDF 生成超时")
            return False
        except Exception as e:
            print(f"❌ PDF 生成异常：{e}")
            return False
    
    def step3_send_telegram(self):
        """步骤 3: PDF → Telegram"""
        print("\n" + "="*60)
        print("步骤 3/3: PDF → Telegram")
        print("="*60)
        
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            
            caption = f"""📄 {self.pdf_path.name}

OpenClaw 案例融合方案（Design Agent 优化版）

✅ PDF 格式，可直接打开阅读
📊 {self.pdf_path.stat().st_size / 1024:.1f} KB | A4 尺寸 | 彩色优化
🎨 Design Agent v5.0 标准
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

6 大案例深度对比:
⏱️  时间节省：-85%
💰 成本节省：-72%
📈 效果提升：+203%
😊 满意度提升：+91%"""
            
            with open(self.pdf_path, 'rb') as f:
                files = {'document': f}
                data = {
                    'chat_id': CHAT_ID,
                    'caption': caption,
                    'parse_mode': 'Markdown'
                }
                
                print(f"📱 发送到 Telegram...")
                response = requests.post(url, files=files, data=data, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('ok'):
                        print(f"✅ PDF 发送成功！")
                        print(f"📱 Telegram 会话中可直接点击打开")
                        return True
                    else:
                        print(f"❌ Telegram API 错误：{result}")
                        return False
                else:
                    print(f"❌ HTTP 错误：{response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ 发送异常：{e}")
            return False
    
    def run(self):
        """执行完整流程"""
        print("\n" + "🚀"*30)
        print("🚀 OpenClaw 文档自动化发布系统")
        print("🚀"*30)
        print(f"\n开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        steps = [
            ("Markdown → HTML", self.step1_md_to_html),
            ("HTML → PDF", self.step2_html_to_pdf),
            ("PDF → Telegram", self.step3_send_telegram),
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            if step_func():
                success_count += 1
            else:
                print(f"\n❌ {step_name} 失败，终止流程")
                return False
        
        print("\n" + "="*60)
        print("✅ 全部完成！")
        print("="*60)
        print(f"\n完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"成功步骤：{success_count}/{len(steps)}")
        print(f"\n生成文件:")
        print(f"  ✅ {self.html_path.name} ({self.html_path.stat().st_size / 1024:.1f} KB)")
        print(f"  ✅ {self.pdf_path.name} ({self.pdf_path.stat().st_size / 1024:.1f} KB)")
        print(f"\n📱 Telegram 会话中可查看和下载 PDF")
        
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 auto-publish-doc.py <markdown 文件>")
        print("\n示例:")
        print("  python3 auto-publish-doc.py 'OpenClaw 案例融合方案（Design Agent 优化版）.md'")
        sys.exit(1)
    
    md_file = sys.argv[1]
    
    try:
        publisher = AutoPublishDoc(md_file)
        success = publisher.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 启动失败：{e}")
        sys.exit(1)
