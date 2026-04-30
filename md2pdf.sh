#!/bin/bash
# md2pdf - Markdown 转 PDF（增强版）
# 用法：bash md2pdf.sh input.md [output.pdf]

INPUT="$1"
OUTPUT="$2"

if [ -z "$INPUT" ]; then
    echo "用法：bash md2pdf.sh input.md [output.pdf]"
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

python3 -c "
import markdown2
md_file = '$INPUT'
html_file = '$HTML_FILE'
with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()
html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code', 'toc'])
html_template = '''<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
    <meta charset=\"UTF-8\">
    <title>OpenClaw 案例融合方案</title>
    <style>
        @page { size: A4; margin: 25mm; }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; max-width: 210mm; margin: 0 auto; padding: 25mm; }
        h1 { color: #1E88E5; border-bottom: 3px solid #1E88E5; padding-bottom: 15px; font-size: 24pt; page-break-before: always; }
        h1:first-of-type { page-break-before: avoid; }
        h2 { color: #1E88E5; margin-top: 30px; font-size: 18pt; }
        h3 { color: #0D47A1; font-size: 14pt; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #1E88E5; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        .card { border: 2px solid #1E88E5; border-radius: 10px; padding: 20px; margin: 20px 0; background: #f9f9f9; page-break-inside: avoid; }
    </style>
</head>
<body>
''' + html_content + '''
</body>
</html>'''
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_template)
print('✅ HTML 已生成：' + html_file)
"

# 步骤 2: HTML -> PDF (Chrome headless)
echo "步骤 2/3: HTML -> PDF"
google-chrome --headless --disable-gpu --print-to-pdf="$OUTPUT" "$HTML_FILE" 2>/dev/null

# 步骤 3: 检查结果
if [ -f "$OUTPUT" ]; then
    SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
    echo "✅ PDF 已生成：$OUTPUT ($SIZE)"
    echo "步骤 3/3: 完成！"
else
    echo "❌ PDF 生成失败"
    exit 1
fi
