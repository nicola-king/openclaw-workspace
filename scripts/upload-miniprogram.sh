#!/bin/bash
# 微信小程序上传脚本
# 使用：./upload-miniprogram.sh [版本号] [备注]

set -e

PROJECT_DIR="/home/nicola/.openclaw/workspace/miniprogram"
VERSION=${1:-"1.0.0"}
REMARK=${2:-"心景·MindScape v${VERSION} - 看清你正在经历什么"}
APPID="wx720a4c489fec9df3"

echo "🚀 开始上传小程序..."
echo "   AppID: $APPID"
echo "   版本：$VERSION"
echo "   备注：$REMARK"
echo "   目录：$PROJECT_DIR"
echo ""

cd "$PROJECT_DIR"

# 使用 miniprogram-ci 上传
npx miniprogram-ci \
  --project-path "$PROJECT_DIR" \
  --appid "$APPID" \
  --version "$VERSION" \
  --desc "$REMARK" \
  --upload \
  --qrcode-format image \
  --output-dir "/tmp/miniprogram-upload"

echo ""
echo "✅ 上传成功!"
echo "📱 二维码已保存到：/tmp/miniprogram-upload/upload.qrcode.jpg"
echo ""
echo "下一步:"
echo "1. 打开微信开发者工具"
echo "2. 扫描上方二维码确认上传"
echo "3. 在微信公众平台提交审核"
