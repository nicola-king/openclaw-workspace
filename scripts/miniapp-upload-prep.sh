#!/bin/bash
# 微信小程序上传准备脚本
# 用途：准备上传材料清单

echo "========================================"
echo "微信小程序上传准备清单"
echo "========================================"

WORKSPACE="/home/nicola/.openclaw/workspace"
MINIAPP_DIR="$WORKSPACE/frontend-miniprogram"
UPLOAD_DIR="$WORKSPACE/uploads/miniapp"

# 创建上传目录
mkdir -p "$UPLOAD_DIR"

echo ""
echo "📁 检查必需文件..."

# 检查核心文件
files=(
    "app.js"
    "app.json"
    "project.config.json"
    "sitemap.json"
)

for file in "${files[@]}"; do
    if [ -f "$MINIAPP_DIR/$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (缺失)"
    fi
done

echo ""
echo "📄 检查页面目录..."

pages=(
    "pages/index"
    "pages/test"
    "pages/result"
    "pages/skill-detail"
    "pages/profile"
)

for page in "${pages[@]}"; do
    if [ -d "$MINIAPP_DIR/$page" ]; then
        count=$(ls "$MINIAPP_DIR/$page"/*.wxml 2>/dev/null | wc -l)
        echo "✅ $page ($count 文件)"
    else
        echo "❌ $page (缺失)"
    fi
done

echo ""
echo "🖼️  检查图片资源..."

# 检查必需图片
images=(
    "logo.png"
    "splash.png"
)

for img in "${images[@]}"; do
    if [ -f "$MINIAPP_DIR/$img" ]; then
        echo "✅ $img"
    else
        echo "⚠️  $img (需要创建)"
    fi
done

echo ""
echo "📊 统计信息..."
echo "总文件数：$(find "$MINIAPP_DIR" -type f | wc -l)"
echo "总大小：$(du -sh "$MINIAPP_DIR" | cut -f1)"

echo ""
echo "========================================"
echo "下一步："
echo "1. 创建缺失的图片资源"
echo "2. 安装微信开发者工具 CLI"
echo "3. 执行上传命令"
echo "========================================"
