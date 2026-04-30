#!/usr/bin/env python3
"""
发送 PDF 文件到 Telegram
用法：python3 send-pdf-to-telegram.py <pdf 文件>
"""

import os
import sys
import requests
from pathlib import Path

# Telegram Bot 配置
BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
CHAT_ID = "7073481596"

def send_pdf(pdf_file):
    """发送 PDF 文件到 Telegram"""
    pdf_path = Path(pdf_file)
    
    if not pdf_path.exists():
        print(f"❌ 文件不存在：{pdf_file}")
        return False
    
    print(f"📄 发送 PDF: {pdf_path.name}")
    print(f"📊 文件大小：{pdf_path.stat().st_size / 1024:.1f} KB")
    
    # Telegram API URL
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    # 发送文件
    try:
        with open(pdf_path, 'rb') as f:
            files = {'document': f}
            data = {
                'chat_id': CHAT_ID,
                'caption': f"📄 {pdf_path.name}\n\nOpenClaw 案例融合方案（Design Agent 优化版）\n\n✅ PDF 格式，可直接打开阅读\n📊 528 KB | A4 尺寸 | 彩色打印优化",
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, files=files, data=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print(f"✅ PDF 发送成功！")
                    print(f"📱 Telegram 会话中可直接点击打开")
                    return True
                else:
                    print(f"❌ 发送失败：{result}")
                    return False
            else:
                print(f"❌ HTTP 错误：{response.status_code}")
                print(f"响应：{response.text}")
                return False
                
    except Exception as e:
        print(f"❌ 异常：{e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 send-pdf-to-telegram.py <pdf 文件>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    success = send_pdf(pdf_file)
    sys.exit(0 if success else 1)
