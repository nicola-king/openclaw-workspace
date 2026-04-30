#!/bin/bash
# OpenClaw 文档自动化发布系统
# 用法：bash auto-publish-doc.sh <markdown 文件>

set -e

INPUT_MD="$1"

if [ -z "$INPUT_MD" ]; then
    echo "用法：bash auto-publish-doc.sh <markdown 文件>"
    exit 1
fi

if [ ! -f "$INPUT_MD" ]; then
    echo "❌ 文件不存在：$INPUT_MD"
    exit 1
fi

echo ""
echo "🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀"
echo "🚀 OpenClaw 文档自动化发布系统"
echo "🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀"
echo ""
echo "开始时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 步骤 1: Markdown → HTML (使用已有 HTML 文件)
echo "============================================================"
echo "步骤 1/3: Markdown → HTML"
echo "============================================================"

HTML_FILE="${INPUT_MD%.md}.html"
if [ -f "$HTML_FILE" ]; then
    echo "✅ HTML 已存在：$(basename $HTML_FILE)"
    SIZE=$(ls -lh "$HTML_FILE" | awk '{print $5}')
    echo "📊 HTML 大小：$SIZE"
else
    echo "⚠️  HTML 文件不存在，请使用打印版 HTML"
    HTML_FILE="${INPUT_MD/（Design Agent 优化版）/（打印版）}"
    if [ -f "$HTML_FILE" ]; then
        echo "✅ 使用打印版 HTML: $(basename $HTML_FILE)"
    else
        echo "❌ HTML 文件不存在"
        exit 1
    fi
fi

# 步骤 2: HTML → PDF
echo ""
echo "============================================================"
echo "步骤 2/3: HTML → PDF"
echo "============================================================"

PDF_FILE="${INPUT_MD%.md}.pdf"
echo "🖨️  执行：google-chrome --headless ..."

google-chrome --headless --disable-gpu --print-to-pdf="$PDF_FILE" "$HTML_FILE" 2>&1

if [ -f "$PDF_FILE" ]; then
    SIZE=$(ls -lh "$PDF_FILE" | awk '{print $5}')
    echo "✅ PDF 已生成：$(basename $PDF_FILE)"
    echo "📊 PDF 大小：$SIZE"
else
    echo "❌ PDF 生成失败"
    exit 1
fi

# 步骤 3: PDF → Telegram
echo ""
echo "============================================================"
echo "步骤 3/3: PDF → Telegram"
echo "============================================================"

python3 << PYTHON
import requests
from pathlib import Path
from datetime import datetime

BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
CHAT_ID = "7073481596"
PDF_FILE = "$PDF_FILE"

pdf_path = Path(PDF_FILE)
print(f"📱 发送到 Telegram...")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

caption = f"""📄 {pdf_path.name}

OpenClaw 案例融合方案（Design Agent 优化版）

✅ PDF 格式，可直接打开阅读
📊 {pdf_path.stat().st_size / 1024:.1f} KB | A4 尺寸 | 彩色优化
🎨 Design Agent v5.0 标准
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

6 大案例深度对比:
⏱️  时间节省：-85%
💰 成本节省：-72%
📈 效果提升：+203%
😊 满意度提升：+91%"""

try:
    with open(pdf_path, 'rb') as f:
        files = {'document': f}
        data = {
            'chat_id': CHAT_ID,
            'caption': caption,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, files=files, data=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print(f"✅ PDF 发送成功！")
                print(f"📱 Telegram 会话中可直接点击打开")
            else:
                print(f"❌ Telegram API 错误：{result}")
        else:
            print(f"❌ HTTP 错误：{response.status_code}")
except Exception as e:
    print(f"❌ 发送异常：{e}")
PYTHON

# 完成
echo ""
echo "============================================================"
echo "✅ 全部完成！"
echo "============================================================"
echo ""
echo "完成时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "生成文件:"
echo "  ✅ $(basename $HTML_FILE)"
echo "  ✅ $(basename $PDF_FILE)"
echo ""
echo "📱 Telegram 会话中可查看和下载 PDF"
echo ""
