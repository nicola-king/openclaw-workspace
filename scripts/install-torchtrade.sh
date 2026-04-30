#!/bin/bash
# TorchTrade Phase 1 - 环境搭建脚本
# 创建时间：2026-04-04
# 用途：安装 TorchTrade + 依赖，创建虚拟环境

set -e

echo "======================================"
echo "TorchTrade Phase 1 - 环境搭建"
echo "======================================"
echo ""

# 配置
PYTHON_VERSION="3.11"
VENV_DIR="/home/nicola/.openclaw/workspace/venv/torchtrade"
WORKSPACE="/home/nicola/.openclaw/workspace"

# 检查 Python 版本
echo "[1/6] 检查 Python 版本..."
python3 --version || { echo "❌ Python3 未安装"; exit 1; }

# 创建虚拟环境
echo "[2/6] 创建虚拟环境 ($VENV_DIR)..."
rm -rf "$VENV_DIR"
python3 -m venv "$VENV_DIR"
echo "✅ 虚拟环境创建完成"

# 激活虚拟环境
echo "[3/6] 激活虚拟环境..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip

# 安装 PyTorch (CPU 版本，如需 GPU 请修改)
echo "[4/6] 安装 PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 安装 TorchRL
echo "[5/6] 安装 TorchRL..."
pip install torchrl

# 安装 Gymnasium
echo "[6/6] 安装 Gymnasium..."
pip install gymnasium

# 尝试安装 TorchTrade (从 GitHub)
echo "[7/7] 安装 TorchTrade (从 GitHub)..."
pip install git+https://github.com/TorchTrade/torchtrade.git || {
    echo "⚠️ TorchTrade 安装失败，可能仓库不存在或需要认证"
    echo "📝 手动安装步骤："
    echo "   1. git clone https://github.com/TorchTrade/torchtrade.git"
    echo "   2. cd torchtrade"
    echo "   3. pip install -e ."
}

# 验证安装
echo ""
echo "======================================"
echo "验证安装"
echo "======================================"
python3 -c "import torch; print(f'✅ PyTorch: {torch.__version__}')"
python3 -c "import torchrl; print(f'✅ TorchRL: {torchrl.__version__}')"
python3 -c "import gymnasium; print(f'✅ Gymnasium: {gymnasium.__version__}')"

# 尝试导入 TorchTrade
python3 -c "import torchtrade; print(f'✅ TorchTrade: 已安装')" 2>/dev/null || {
    echo "⚠️ TorchTrade: 未安装 (可能仓库不可访问)"
}

echo ""
echo "======================================"
echo "环境搭建完成"
echo "======================================"
echo ""
echo "激活环境：source $VENV_DIR/bin/activate"
echo "退出环境：deactivate"
echo ""
