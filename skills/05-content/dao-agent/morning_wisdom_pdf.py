#!/usr/bin/env python3
"""
道 Agent - 晨间智慧推送 v2.0 (PDF 格式)
太一 AGI · 2026-04-18

更新:
- MD 格式 → PDF 格式
- 优化移动端阅读体验
- 方便传播分享
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime

# 导入 MD 转 PDF 转换器
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "07-system" / "md2pdf"))
from md2pdf import MDToPDFConverter

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DAO_OUTPUT_DIR = WORKSPACE / "skills/05-content/dao-agent/data/output"
PDF_OUTPUT_DIR = WORKSPACE / "wisdom-pdf"

# Telegram 配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_pdf_to_telegram(pdf_file, caption):
    """发送 PDF 到 Telegram
    
    Args:
        pdf_file: PDF 文件路径
        caption: 说明文字
    """
    print(f"📱 发送 PDF 到 Telegram")
    print(f"   文件：{pdf_file}")
    
    url = f"{TELEGRAM_API_URL}/sendDocument"
    
    try:
        with open(pdf_file, 'rb') as f:
            files = {'document': f}
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption,
                'parse_mode': 'Markdown',
            }
            
            response = requests.post(url, files=files, data=data, timeout=60)
            
            if response.status_code == 200:
                print(f"✅ PDF 发送成功")
                return True
            else:
                print(f"❌ 发送失败：{response.status_code}")
                print(f"响应：{response.text}")
                return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def generate_daily_wisdom():
    """生成每日智慧"""
    print(f"📿 生成道 Agent 晨间智慧")
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 读取 MD 文件
    md_file = DAO_OUTPUT_DIR / f"dao-{today}.md"
    if not md_file.exists():
        print(f"⚠️  MD 文件不存在：{md_file}")
        return None
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print(f"✅ 读取 MD 文件：{md_file}")
    
    # 转换为 PDF
    converter = MDToPDFConverter()
    pdf_file = md_file.with_suffix('.pdf')
    
    pdf_path = converter.convert(md_file, pdf_file)
    
    if pdf_path:
        print(f"✅ PDF 生成成功：{pdf_path}")
        return pdf_path
    else:
        print(f"❌ PDF 生成失败")
        return None


def send_morning_wisdom():
    """发送晨间智慧"""
    print("=" * 60)
    print("📿 道 Agent - 晨间智慧推送 v2.0 (PDF 格式)")
    print("=" * 60)
    
    # 生成智慧
    pdf_file = generate_daily_wisdom()
    if not pdf_file:
        return
    
    # 生成说明文字
    today = datetime.now().strftime('%Y-%m-%d')
    weekday = datetime.now().strftime('%A')
    caption = f"""📿 道 · 晨间智慧

📅 {today} {weekday}

🌅 一日之计在于晨
📖 每日智慧伴您行

太一 AGI · 道 Agent
"""
    
    # 发送 PDF
    send_pdf_to_telegram(pdf_file, caption)
    
    print("=" * 60)
    print("✅ 晨间智慧推送完成")


def main():
    """主函数"""
    send_morning_wisdom()


if __name__ == "__main__":
    main()
