#!/bin/bash
#
# 重庆 18 定额配套文件下载脚本
#
# 功能:
# 1. 从百度网盘下载定额文件
# 2. 解压到目标目录
# 3. 集成到系统
#
# 作者：太一 AGI
# 创建：2026-04-10
#

set -e

# 配置
TARGET_DIR="/home/nicola/.openclaw/workspace/skills/civil-engineering-cost/data/chongqing_18_quota"
TEMP_DIR="/tmp/chongqing_quota_download"
BAIDU_PATH="/apps/重庆 18 定额配套文件"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# 创建目录
log "创建目标目录..."
mkdir -p "$TARGET_DIR"
mkdir -p "$TEMP_DIR"
success "目录已创建"

# 检查 bypy
log "检查 bypy 工具..."
if ! command -v bypy &> /dev/null; then
    error "bypy 未安装，请先安装：pip install bypy"
fi
success "bypy 已安装"

# 检查百度网盘登录
log "检查百度网盘登录状态..."
bypy info > /dev/null 2>&1
if [ $? -ne 0 ]; then
    warn "百度网盘未登录，请先运行：bypy info"
    warn "按提示完成登录"
    exit 1
fi
success "百度网盘已登录"

# 搜索文件
log "搜索重庆 18 定额文件..."
BAIDU_FILES=$(bypy search 重庆 18 定额 2>&1 | grep -v "HTTP_PROXY" | grep -v "Nothing found" || echo "")

if [ -z "$BAIDU_FILES" ]; then
    warn "未找到'重庆 18 定额'文件"
    warn "请手动在百度网盘中查找并下载"
    warn "下载地址：https://pan.baidu.com/"
    echo ""
    echo "搜索关键词:"
    echo "  - 重庆 18 定额配套文件"
    echo "  - 重庆 2018 市政定额"
    echo "  - 重庆市市政工程计价定额"
    echo ""
    echo "下载后保存到：$TARGET_DIR"
    exit 0
fi

success "找到文件:"
echo "$BAIDU_FILES"

# 下载文件
log "开始下载文件..."
cd "$TEMP_DIR"

# 尝试下载
bypy download "$BAIDU_PATH" . 2>&1 | tee /tmp/bypy_download.log

if [ $? -eq 0 ]; then
    success "下载完成"
else
    warn "下载失败，请检查网络连接或百度网盘账号"
    exit 1
fi

# 移动文件到目标目录
log "移动文件到目标目录..."
mv "$TEMP_DIR"/* "$TARGET_DIR/" 2>/dev/null || true
success "文件已移动"

# 解压文件 (如果是压缩包)
log "检查并解压文件..."
cd "$TARGET_DIR"

for file in *.zip *.7z *.rar; do
    if [ -f "$file" ]; then
        log "解压 $file..."
        case "$file" in
            *.zip)
                unzip -o "$file"
                ;;
            *.7z)
                7z x "$file"
                ;;
            *.rar)
                unrar x "$file"
                ;;
        esac
        success "$file 解压完成"
    fi
done

# 统计文件
log "统计文件..."
FILE_COUNT=$(ls "$TARGET_DIR" | wc -l)
TOTAL_SIZE=$(du -sh "$TARGET_DIR" | cut -f1)

success "下载完成!"
echo ""
echo "================================"
echo "  重庆 18 定额配套文件下载完成"
echo "================================"
echo ""
echo "目标目录：$TARGET_DIR"
echo "文件数量：$FILE_COUNT 个"
echo "总大小：$TOTAL_SIZE"
echo ""
echo "文件列表:"
ls -lh "$TARGET_DIR"
echo ""

# 清理临时目录
log "清理临时目录..."
rm -rf "$TEMP_DIR"
success "临时目录已清理"

echo ""
success "所有操作完成！"
echo ""
echo "下一步:"
echo "  1. 验证文件完整性"
echo "  2. 系统自动集成定额数据"
echo "  3. 测试造价计算功能"
echo ""

exit 0
