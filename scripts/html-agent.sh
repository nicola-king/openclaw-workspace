#!/bin/bash
# html-anything Agent 驱动渲染（Phase 2）
# 使用本地 coding agent（OpenClaw）将 Markdown 渲染为设计级 HTML
# 消耗 token 但效果最佳 — 适用于高价值内容
#
# 用法:
#   ./html-agent.sh <template-id> <input.md> [output.html]
#   ./html-agent.sh agent <template-id> <input.md> [output.html]
#
# 模板列表:
#   文章类: article-magazine, blog-post, digital-eguide
#   卡片类: card-xiaohongshu, card-twitter
#   文档类: doc-kami-parchment, docs-page, eng-runbook
#   数据类: data-report, finance-report
#   幻灯类: deck-swiss-international, deck-guizang-editorial, deck-pitch, deck-tech-sharing
#   海报类: magazine-poster, poster-hero
#   原型类: saas-landing, pricing-page, waitlist-page

AGENT="${1:-openclaw}"
TEMPLATE_ID="${2:-doc-kami-parchment}"
INPUT_FILE="${3:-/dev/stdin}"
OUTPUT_FILE="${4:-/dev/stdout}"
PORT="${HTML_ANYTHING_PORT:-3777}"

# 使用说明
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  sed -n '3,18p' "$0"
  exit 0
fi

# 读取输入内容
CONTENT=$(cat "$INPUT_FILE")

# 调用 convert API（SSE 流式输出）
echo "🎨 Agent: $AGENT | 模板: $TEMPLATE_ID" >&2
echo "⏳ 生成中..." >&2

# 收集 SSE 事件中的 HTML
HTML=$(curl -s "http://localhost:$PORT/api/convert" \
  -X POST \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "
import json, sys
d = {
    'agent': '$AGENT',
    'templateId': '$TEMPLATE_ID',
    'content': open('$INPUT_FILE').read() if '$INPUT_FILE' != '/dev/stdin' else '$(cat)',
    'format': 'markdown'
}
d['content'] = """$(cat "$INPUT_FILE")"""
print(json.dumps(d))
")" 2>/dev/null | python3 -c "
import sys
html_parts = []
for line in sys.stdin:
    line = line.strip()
    if line.startswith('event: delta'):
        # Read next data line
        data_line = next(sys.stdin, '').strip()
        if data_line.startswith('data: '):
            import json
            try:
                d = json.loads(data_line[6:])
                if d.get('type') == 'delta':
                    html_parts.append(d.get('text', ''))
            except:
                pass
    elif line.startswith('data: {\"type\":\"done\"'):
        break
sys.stdout.write(''.join(html_parts))
")

if [ -z "$HTML" ]; then
  echo "❌ 生成失败，无输出" >&2
  exit 1
fi

# 验证是否是有效 HTML
if echo "$HTML" | head -1 | grep -q "^<!DOCTYPE html>\|<html"; then
  echo "$HTML" > "$OUTPUT_FILE"
  echo "✅ $AGENT → $TEMPLATE_ID → $OUTPUT_FILE ($(wc -c < "$OUTPUT_FILE") bytes)" >&2
  exit 0
else
  echo "❌ 输出不是有效 HTML: $(echo "$HTML" | head -3)" >&2
  echo "$HTML" > "$OUTPUT_FILE"
  exit 1
fi
