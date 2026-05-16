#!/bin/bash
# html-anything CLI 集成脚本
# 用法: ./html2.sh <template-id> <input.md> [output.html]
# 将 Markdown 内容渲染为设计的 HTML 页面（零 token 成本，静态模板）

DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE_ID="${1:-doc-kami-parchment}"
INPUT_FILE="${2:-/dev/stdin}"
OUTPUT_FILE="${3:-/dev/stdout}"
PORT="${HTML_ANYTHING_PORT:-3777}"

# 读取输入内容（转为单行 JSON > 安全）
CONTENT=$(cat "$INPUT_FILE" | python3 -c "
import sys,json
text = sys.stdin.read()
print(json.dumps(text))
")

# 调用 preview API（静态渲染，不需要 agent）
RESPONSE=$(curl -s "http://localhost:$PORT/api/templates/$TEMPLATE_ID/preview" \
  -H "Content-Type: application/json" \
  -d "{\"content\":$CONTENT}" 2>/dev/null)

# 检查是否成功
if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print('html' in d)" 2>/dev/null | grep -q True; then
  echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['html'])" > "$OUTPUT_FILE"
  echo "✅ $TEMPLATE_ID → $OUTPUT_FILE" >&2
  exit 0
else
  echo "❌ 渲染失败: $(echo $RESPONSE | head -200)" >&2
  exit 1
fi
