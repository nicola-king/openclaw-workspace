#!/bin/bash
# TimesFM 环境搭建脚本
# TASK-101: TimesFM 集成评估

set -e

echo '╔══════════════════════════════════════════════════════════╗'
echo '║  🚀 TimesFM 环境搭建                                      ║'
echo '╚══════════════════════════════════════════════════════════╝'
echo ""
echo "⏰ 时间：$(date -Iseconds)"
echo ""

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python3 --version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

# 使用 Python 比较版本
python3 -c "
import sys
version = tuple(map(int, '$PYTHON_VERSION'.split('.')))
if version < (3, 9):
    print('❌ Python 版本过低，需要 3.9+')
    sys.exit(1)
print('✅ Python 版本符合要求')
" || exit 1
echo ""

# 创建虚拟环境（可选，跳过）
echo "📦 虚拟环境（跳过，使用系统 Python）..."
echo "✅ 使用系统 Python 环境"
echo ""

# 直接使用系统 Python
echo "🔌 使用系统 Python..."
echo "✅ Python: $(which python3)"
echo ""

# 升级 pip
echo "📦 升级 pip..."
pip3 install --upgrade pip --quiet --break-system-packages
echo ""

# 安装 TimesFM
echo "📦 安装 TimesFM..."
pip3 install timesfm --quiet --break-system-packages
echo "✅ TimesFM 安装完成"
echo ""

# 安装其他依赖
echo "📦 安装其他依赖..."
pip3 install numpy pandas scikit-learn matplotlib --quiet --break-system-packages
echo "✅ 依赖安装完成"
echo ""

# 验证安装
echo "🧪 验证安装..."
python3 -c "import timesfm; print('✅ TimesFM 导入成功')"
python3 -c "import numpy; print('✅ NumPy 导入成功')"
python3 -c "import pandas; print('✅ Pandas 导入成功')"
echo ""

# 显示安装信息
echo '╔══════════════════════════════════════════════════════════╗'
echo '║  ✅ TimesFM 环境搭建完成                                  ║'
echo '╚══════════════════════════════════════════════════════════╝'
echo ""
echo "📋 下一步操作:"
echo ""
echo "1. 运行 Hello World 测试:"
echo "   python3 scripts/timesfm-hello-world.py"
echo ""
echo "2. 运行完整模型测试:"
echo "   python3 scripts/timesfm-full-test.py"
echo ""
echo "3. 查看技术验证报告:"
echo "   cat reports/timesfm-validation-report.md"
echo ""
