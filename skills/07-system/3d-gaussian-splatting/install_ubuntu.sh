#!/bin/bash
# Ubuntu 工控机 3D 高斯泼溅自动安装脚本
# 太一 AGI · 2026-04-18

set -e

WORKSPACE="/home/nicola/.openclaw/workspace/3d-gaussian-splatting"
BRUSH_DIR="$WORKSPACE/brush"

echo "=========================================="
echo "🐧 Ubuntu 3D 高斯泼溅自动安装"
echo "=========================================="
echo ""

# 检查系统
echo "📊 检查系统..."
if [ ! -f /etc/os-release ]; then
    echo "❌ 非 Linux 系统，请手动安装"
    exit 1
fi

source /etc/os-release
if [[ "$ID" != "ubuntu" ]]; then
    echo "⚠️  非 Ubuntu 系统，可能不兼容"
fi

echo "✅ 系统：$NAME $VERSION"
echo ""

# 创建目录
echo "📁 创建目录..."
mkdir -p "$WORKSPACE"
mkdir -p "$WORKSPACE/test/photos"
mkdir -p "$WORKSPACE/test/output"
echo "✅ 目录已创建：$WORKSPACE"
echo ""

# 安装依赖
echo "🔧 安装系统依赖..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git ffmpeg libeigen3-dev libboost-all-dev wget
echo "✅ 系统依赖已安装"
echo ""

# 检查 NVIDIA GPU
echo "🎮 检查 NVIDIA GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU 已检测到"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    USE_CUDA=true
else
    echo "⚠️  未检测到 NVIDIA GPU，将使用 CPU 模式"
    USE_CUDA=false
fi
echo ""

# 安装 NVIDIA 驱动 (如需要)
if [ "$USE_CUDA" = true ]; then
    echo "🔧 检查 NVIDIA 驱动..."
    if ! dpkg -l | grep -q nvidia-driver; then
        echo "  安装 NVIDIA 驱动..."
        sudo apt install -y nvidia-driver-535 nvidia-cuda-toolkit
        echo "✅ NVIDIA 驱动已安装"
    else
        echo "✅ NVIDIA 驱动已安装"
    fi
    echo ""
fi

# 克隆 Brush
echo "📦 克隆 Brush..."
if [ -d "$BRUSH_DIR" ]; then
    echo "⚠️  Brush 已存在，跳过克隆"
else
    git clone https://github.com/ArthurBrussee/brush.git "$BRUSH_DIR"
    echo "✅ Brush 已克隆"
fi
echo ""

# 创建虚拟环境
echo "🐍 创建 Python 虚拟环境..."
cd "$BRUSH_DIR"
if [ -d "venv" ]; then
    echo "⚠️  虚拟环境已存在"
else
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
fi

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip

# 安装 PyTorch
echo "🔥 安装 PyTorch..."
if [ "$USE_CUDA" = true ]; then
    echo "  安装 CUDA 版本..."
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
else
    echo "  安装 CPU 版本..."
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
fi
echo "✅ PyTorch 已安装"
echo ""

# 安装 Brush 依赖
echo "📦 安装 Brush 依赖..."
pip install -r requirements.txt
pip install opencv-python-headless pycolmap
echo "✅ Brush 依赖已安装"
echo ""

# 验证安装
echo "✅ 验证安装..."
if python brush.py --help &> /dev/null; then
    echo "✅ Brush 安装成功"
else
    echo "❌ Brush 安装失败"
    exit 1
fi

# 测试 CUDA
if [ "$USE_CUDA" = true ]; then
    echo "🔥 测试 CUDA..."
    if python -c "import torch; assert torch.cuda.is_available()" &> /dev/null; then
        echo "✅ CUDA 可用"
    else
        echo "⚠️  CUDA 不可用"
    fi
fi
echo ""

# 创建测试脚本
echo "📝 创建测试脚本..."
cat > "$WORKSPACE/test_brush.sh" << 'EOF'
#!/bin/bash
# Brush 测试脚本

cd /home/nicola/.openclaw/workspace/3d-gaussian-splatting/brush
source venv/bin/activate

echo "🎨 开始 3D 重建测试..."
python brush.py reconstruct \
  --input ../test/photos \
  --output ../test/output \
  --format ply

echo "✅ 测试完成！"
echo "输出：../test/output/"
EOF

chmod +x "$WORKSPACE/test_brush.sh"
echo "✅ 测试脚本已创建：$WORKSPACE/test_brush.sh"
echo ""

# 完成
echo "=========================================="
echo "🎊 安装完成！"
echo "=========================================="
echo ""
echo "📂 安装目录：$BRUSH_DIR"
echo "📁 测试目录：$WORKSPACE/test"
echo "📝 测试脚本：$WORKSPACE/test_brush.sh"
echo ""
echo "🚀 下一步:"
echo "  1. 手机拍照 (20-50 张)"
echo "  2. 传输到：$WORKSPACE/test/photos/"
echo "  3. 运行测试：$WORKSPACE/test_brush.sh"
echo "  4. 查看结果：$WORKSPACE/test/output/"
echo ""
echo "💡 提示:"
echo "  • 激活虚拟环境：cd $BRUSH_DIR && source venv/bin/activate"
echo "  • 运行 Brush: python brush.py --help"
echo "  • 查看文档：cat $WORKSPACE/UBUNTU_INSTALL_GUIDE.md"
echo ""
