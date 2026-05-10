#!/bin/bash
# 下载前端依赖（CDN → 本地）
set -e

DIR="$(cd "$(dirname "$0")/../frontend" && pwd)"
VENDOR="$DIR/vendor"
mkdir -p "$VENDOR"

echo "📦 下载前端依赖到 $VENDOR"

# React
curl -sL -o "$VENDOR/react.production.min.js" \
  "https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js" &
curl -sL -o "$VENDOR/react-dom.production.min.js" \
  "https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js" &

# React Flow (xyflow)
curl -sL -o "$VENDOR/xyflow.css" \
  "https://cdn.jsdelivr.net/npm/@xyflow/react@12.5.0/dist/style.css" &
curl -sL -o "$VENDOR/xyflow.umd.js" \
  "https://cdn.jsdelivr.net/npm/@xyflow/react@12.5.0/umd/index.js" &

wait

echo "✅ 下载完成"
ls -lh "$VENDOR/"
