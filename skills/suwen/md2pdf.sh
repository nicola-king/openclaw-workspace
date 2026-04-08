#!/bin/bash
# md2pdf - Markdown 转 PDF（支持图片）
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

# 使用 Chrome headless 模式生成 PDF
google-chrome --headless --disable-gpu --print-to-pdf="$OUTPUT" "$INPUT" 2>/dev/null

if [ -f "$OUTPUT" ]; then
    SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
    echo "✅ PDF 已生成：$OUTPUT ($SIZE)"
else
    echo "❌ PDF 生成失败"
    exit 1
fi
