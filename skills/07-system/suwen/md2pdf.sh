#!/bin/bash
# md2pdf - Markdown 转 PDF（增强版）
# 支持多种渲染方式
# 用法：md2pdf.sh input.md [output.pdf]

set -e

INPUT="$1"
OUTPUT="$2"

if [ -z "$INPUT" ]; then
    echo "用法：md2pdf.sh input.md [output.pdf]"
    exit 1
fi

if [ -z "$OUTPUT" ]; then
    OUTPUT="${INPUT%.md}.pdf"
fi

if [ ! -f "$INPUT" ]; then
    echo "❌ 文件不存在：$INPUT"
    exit 1
fi

echo "📄 转换中：$INPUT -> $OUTPUT"

# 步骤 1: Markdown 转 HTML
HTML_FILE="${INPUT%.md}.html"
echo "步骤 1/3: Markdown -> HTML"

python3 << PYTHON
import markdown2
import sys

md_file = "$INPUT"
html_file = "$HTML_FILE"

with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code', 'toc'])

html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw 案例融合方案</title>
    <style>
        @page {
            size: A4;
            margin: 25mm;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 25mm;
        }
        h1 {
            color: #1E88E5;
            border-bottom: 3px solid #1E88E5;
            padding-bottom: 15px;
            font-size: 24pt;
            page-break-before: always;
        }
        h1:first-of-type {
            page-break-before: avoid;
        }
        h2 {
            color: #1E88E5;
            margin-top: 30px;
            font-size: 18pt;
            page-break-after: avoid;
        }
        h3 {
            color: #0D47A1;
            font-size: 14pt;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background: #1E88E5;
            color: white;
        }
        tr:nth-child(even) {
            background: #f9f9f9;
        }
        .card {
            border: 2px solid #1E88E5;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            background: #f9f9f9;
            page-break-inside: avoid;
        }
        @media print {
            body { padding: 0; }
            a { text-decoration: none; color: #333; }
        }
    </style>
</head>
<body>
''' + html_content + '''
</body>
</html>'''

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"✅ HTML 已生成：{html_file}")
PYTHON

# 步骤 2: 尝试多种方式生成 PDF
echo "步骤 2/3: HTML -> PDF"

# 方式 1: Chrome/Chromium headless
if command -v google-chrome &> /dev/null; then
    echo "使用 Google Chrome..."
    google-chrome --headless --disable-gpu --print-to-pdf="$OUTPUT" "$HTML_FILE" 2>/dev/null && SUCCESS=1
elif command -v chromium &> /dev/null; then
    echo "使用 Chromium..."
    chromium --headless --disable-gpu --print-to-pdf="$OUTPUT" "$HTML_FILE" 2>/dev/null && SUCCESS=1
elif command -v chromium-browser &> /dev/null; then
    echo "使用 Chromium-browser..."
    chromium-browser --headless --disable-gpu --print-to-pdf="$OUTPUT" "$HTML_FILE" 2>/dev/null && SUCCESS=1
else
    SUCCESS=0
fi

# 方式 2: 如果 Chrome 不可用，提示用户手动打印
if [ "$SUCCESS" = "0" ]; then
    echo "⚠️  Chrome/Chromium 未安装"
    echo ""
    echo "📝 请手动生成 PDF:"
    echo "   1. 打开 $HTML_FILE"
    echo "   2. Ctrl+P (打印)"
    echo "   3. 选择'另存为 PDF'"
    echo "   4. 保存为 $OUTPUT"
    echo ""
    echo "✅ HTML 文件已优化打印，可直接使用"
else
    if [ -f "$OUTPUT" ]; then
        SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
        echo "✅ PDF 已生成：$OUTPUT ($SIZE)"
    else
        echo "❌ PDF 生成失败"
        exit 1
    fi
fi
