#!/bin/bash
# TimesFM 部署脚本
# 用途：安装依赖、验证环境、运行示例
# 生成时间：2026-03-30 10:32

set -e

echo "============================================================"
echo "  TimesFM 部署脚本 v2.5"
echo "============================================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Python 版本
echo -e "\n${YELLOW}[1/6] 检查 Python 环境...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python 版本：$python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo -e "${RED}错误：需要 Python 3.10+${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Python 版本符合要求${NC}"

# 创建虚拟环境
echo -e "\n${YELLOW}[2/6] 创建虚拟环境...${NC}"
VENV_DIR="${VENV_DIR:-.venv-timesfm}"

if [ -d "$VENV_DIR" ]; then
    echo "  虚拟环境已存在：$VENV_DIR"
    echo "  如需重新创建，请先删除：rm -rf $VENV_DIR"
else
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}  ✓ 虚拟环境创建成功${NC}"
fi

# 激活虚拟环境
echo -e "\n${YELLOW}[3/6] 激活虚拟环境...${NC}"
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}  ✓ 虚拟环境已激活${NC}"

# 安装 uv (可选，更快的包管理器)
echo -e "\n${YELLOW}[4/6] 安装依赖...${NC}"
if command -v uv &> /dev/null; then
    echo "  使用 uv 安装 (更快)..."
    uv pip install -e ".[torch]" 2>/dev/null || {
        echo "  uv 安装失败，回退到 pip..."
        pip install -e ".[torch]"
    }
else
    echo "  使用 pip 安装..."
    pip install --upgrade pip
    pip install -e ".[torch]"
fi

echo -e "${GREEN}  ✓ 依赖安装完成${NC}"

# 验证安装
echo -e "\n${YELLOW}[5/6] 验证安装...${NC}"
python3 -c "
import torch
import numpy as np
import timesfm

print(f'  PyTorch 版本：{torch.__version__}')
print(f'  NumPy 版本：{np.__version__}')
print(f'  TimesFM 版本：{timesfm.__version__ if hasattr(timesfm, \"__version__\") else \"2.5+\"}')
print(f'  CUDA 可用：{torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'  CUDA 版本：{torch.version.cuda}')
    print(f'  GPU 数量：{torch.cuda.device_count()}')
    print(f'  GPU 名称：{torch.cuda.get_device_name(0)}')
"

echo -e "${GREEN}  ✓ 验证通过${NC}"

# 运行快速测试
echo -e "\n${YELLOW}[6/6] 运行快速测试...${NC}"
python3 << 'EOF'
import numpy as np
import timesfm

print("  加载 TimesFM 2.5 模型 (200M)...")
model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
    "google/timesfm-2.5-200m-pytorch"
)

print("  编译模型...")
model.compile(
    timesfm.ForecastConfig(
        max_context=512,
        max_horizon=128,
        normalize_inputs=True,
    )
)

print("  生成测试数据...")
test_input = [np.sin(np.linspace(0, 10, 100))]

print("  执行预测 (horizon=24)...")
import time
start = time.time()
point, quantiles = model.forecast(horizon=24, inputs=test_input)
elapsed = time.time() - start

print(f"\n  📊 测试结果:")
print(f"     点预测形状：{point.shape}")
print(f"     分位数形状：{quantiles.shape}")
print(f"     推理耗时：{elapsed*1000:.1f}ms")
print(f"     预测值范围：[{point[0].min():.3f}, {point[0].max():.3f}]")
print("\n  ✅ 快速测试通过!")
EOF

echo -e "\n${GREEN}============================================================${NC}"
echo -e "${GREEN}  TimesFM 部署完成!${NC}"
echo -e "${GREEN}============================================================${NC}"

echo -e "\n${YELLOW}使用指南:${NC}"
echo "  1. 激活环境：source $VENV_DIR/bin/activate"
echo "  2. 运行示例：python examples/timesfm-weather-demo.py"
echo "  3. 查看文档：reports/timesfm-tech-analysis.md"

echo -e "\n${YELLOW}常见问题:${NC}"
echo "  - GPU 内存不足：减小 max_context 和 batch_size"
echo "  - 下载慢：配置 HF_ENDPOINT=https://hf-mirror.com"
echo "  - 代理问题：export ALL_PROXY= HTTP_PROXY= HTTPS_PROXY="
echo "  - CUDA 错误：检查 torch 版本与 GPU 驱动兼容性"

echo -e "\n${YELLOW}模型下载说明:${NC}"
echo "  首次运行会自动从 HuggingFace 下载 (~800MB)"
echo "  国内用户建议：export HF_ENDPOINT=https://hf-mirror.com"
echo "  代理问题：临时清除代理变量后下载"
