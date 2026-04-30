#!/bin/bash
# Markdown to PDF conversion script
# Using different methods based on available tools

INPUT_FILE="$1"
OUTPUT_FILE="${INPUT_FILE%.md}.pdf"

echo "Converting $INPUT_FILE to PDF..."

# Method 1: Try pandoc with wkhtmltopdf
if command -v pandoc &> /dev/null && command -v wkhtmltopdf &> /dev/null; then
    echo "Using pandoc + wkhtmltopdf..."
    pandoc "$INPUT_FILE" -o "$OUTPUT_FILE" \
        --from markdown \
        --toc \
        --pdf-engine wkhtmltopdf \
        --variable geometry:margin=25mm \
        --variable fontsize=12pt \
        --variable documentclass=article
    echo "✓ PDF created: $OUTPUT_FILE"
    exit 0
fi

# Method 2: Try pandoc with prince
if command -v pandoc &> /dev/null && command -v prince &> /dev/null; then
    echo "Using pandoc + prince..."
    pandoc "$INPUT_FILE" -o "$OUTPUT_FILE" \
        --from markdown \
        --toc \
        --pdf-engine prince \
        --variable margin=25mm \
        --variable fontsize=12pt
    echo "✓ PDF created: $OUTPUT_FILE"
    exit 0
fi

# Method 3: Try markdown-pdf (Node.js)
if command -v markdown-pdf &> /dev/null; then
    echo "Using markdown-pdf..."
    markdown-pdf "$INPUT_FILE" -o "$OUTPUT_FILE"
    echo "✓ PDF created: $OUTPUT_FILE"
    exit 0
fi

# Method 4: Create HTML for browser print
echo "Creating HTML for browser print..."
cat > "${INPUT_FILE%.md}.html" << HTMLEOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw 案例融合方案</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 25mm;
            color: #333;
        }
        h1 { color: #1E88E5; border-bottom: 2px solid #1E88E5; padding-bottom: 10px; }
        h2 { color: #1E88E5; margin-top: 30px; }
        h3 { color: #0D47A1; }
        code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #1E88E5; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        blockquote { border-left: 4px solid #1E88E5; margin: 20px 0; padding-left: 20px; color: #666; }
        @media print {
            body { padding: 0; }
            a { text-decoration: none; color: #333; }
        }
    </style>
</head>
<body>
$(cat "$INPUT_FILE" | sed 's/```html/```/g' | sed 's/```css/```/g')
</body>
</html>
HTMLEOF

echo "✓ HTML created: ${INPUT_FILE%.md}.html"
echo "  Please open in browser and print to PDF (Ctrl+P → Save as PDF)"
