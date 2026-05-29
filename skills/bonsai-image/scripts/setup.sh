#!/bin/bash
# Bonsai Image 4B — 一键安装配置脚本
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "🌲 Bonsai Image 4B — 安装配置"
echo "══════════════════════════════"

# 1. 硬件检测
echo ""
echo "📡 硬件检测..."
HAS_GPU=false
HAS_NVIDIA=false
HAS_APPLE_SILICON=false

if command -v nvidia-smi &>/dev/null; then
    echo "  ✅ NVIDIA GPU 检测到"
    HAS_GPU=true
    HAS_NVIDIA=true
elif [[ "$(uname)" == "Darwin" ]] && [[ "$(uname -m)" == "arm64" ]]; then
    echo "  ✅ Apple Silicon 检测到"
    HAS_GPU=true
    HAS_APPLE_SILICON=true
else
    echo "  ⚠️ 未检测到 GPU，仅支持 CPU 推理（较慢）"
fi

# 2. 依赖安装
echo ""
echo "📦 依赖检查..."

install_pytorch=false
if python3 -c "import torch" 2>/dev/null; then
    TORCH_VER=$(python3 -c "import torch; print(torch.__version__)")
    echo "  ✅ PyTorch $TORCH_VER"
else
    echo "  ❌ PyTorch 未安装"
    install_pytorch=true
fi

if $HAS_APPLE_SILICON; then
    if python3 -c "import mlx.core" 2>/dev/null; then
        echo "  ✅ MLX"
    else
        echo "  ⚡ 安装 MLX..."
        pip install mlx -q
    fi
fi

if $install_pytorch; then
    echo "  ⚡ 安装 PyTorch..."
    if $HAS_NVIDIA; then
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124 -q
    else
        pip install torch torchvision -q
    fi
fi

# 3. Bonsai 依赖
pip install transformers diffusers sentencepiece accelerate -q 2>/dev/null

# 4. 模型下载
echo ""
echo "📥 模型下载..."

DEMO_DIR="/tmp/bonsai-demo"
MODEL_TARGET="$SCRIPT_DIR/../models/bonsai"

if [ -d "$MODEL_TARGET" ] && [ "$(ls -A "$MODEL_TARGET" 2>/dev/null)" ]; then
    echo "  ✅ 模型已下载 ($MODEL_TARGET)"
else
    echo "  ⚡ 克隆 Bonsai-Image-Demo..."
    if [ -d "$DEMO_DIR/.git" ]; then
        echo "     已存在, 更新中..."
        cd "$DEMO_DIR" && git pull
    else
        git clone https://github.com/PrismML-Eng/Bonsai-Image-Demo.git "$DEMO_DIR"
    fi

    echo "  ⚡ 运行 setup.sh..."
    cd "$DEMO_DIR"
    bash setup.sh 2>&1 | tail -3

    echo "  ⚡ 下载模型权重 (ternary)..."
    bash scripts/download_model.sh ternary 2>&1 | tail -3

    echo "  🔗 创建软链接到 workspace..."
    mkdir -p "$(dirname "$MODEL_TARGET")"
    ln -sfn "$DEMO_DIR/models" "$MODEL_TARGET"

    echo "  ✅ 模型下载完成"
fi

# 5. 验证
echo ""
echo "🧪 验证..."
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, '$WORKSPACE_DIR')
from skills.bonsai_image.bonsai import check_hardware, info
print(check_hardware())
print()
import json
d = json.loads(info())
print(f'模型: {d[\"model\"]}')
print(f'许可: {d[\"license\"]}')
print(f'变体: ternary {d[\"variants\"][\"ternary\"][\"size_gb\"]}GB / binary {d[\"variants\"][\"binary\"][\"size_gb\"]}GB')
"

echo ""
echo "✅ Bonsai Image 安装完成"
echo "用法: python -m skills.bonsai_image.bonsai gen '提示词'"
echo "      python -m skills.bonsai_image.bonsai scene oerv_narrative '月光飞鹿'"
