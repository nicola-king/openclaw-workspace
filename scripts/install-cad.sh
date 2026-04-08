#!/bin/bash
# CAD 工具安装脚本
# 执行：bash /home/nicola/.openclaw/workspace/scripts/install-cad.sh

set -e

echo "🔧 开始安装 CAD 工具..."

# 更新包列表
echo "📦 更新包列表..."
sudo apt update

# 安装 LibreCAD (2D)
echo "📐 安装 LibreCAD (2D CAD)..."
sudo apt install -y librecad

# 安装 FreeCAD (3D)
echo "🏗️ 安装 FreeCAD (3D CAD)..."
sudo apt install -y freecad

# 验证安装
echo "✅ 验证安装..."
librecad --version || echo "⚠️ LibreCAD 版本检测失败"
freecad --version || echo "⚠️ FreeCAD 版本检测失败"

# ODA File Converter 下载
echo "📥 准备 ODA File Converter 下载..."
echo "请访问：https://www.opendesign.com/guestfiles/oda_file_converter"
echo "下载 Ubuntu 版本并解压到 /opt/oda-converter/"

echo ""
echo "🎉 CAD 工具安装完成！"
echo ""
echo "下一步："
echo "1. 打开 LibreCAD: librecad"
echo "2. 打开 FreeCAD: freecad"
echo "3. 下载 ODA File Converter 用于 DWG→DXF 批量转换"
