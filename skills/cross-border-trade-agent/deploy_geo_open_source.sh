#!/bin/bash
# GEO 开源方案快速部署脚本
# 版本：v1.0
# 创建：2026-04-20 21:22
# 功能：一键部署免费开源 GEO 审计系统

set -e

echo "=========================================="
echo "🚀 GEO 开源方案快速部署"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查系统
echo "📋 检查系统..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✅ Linux 系统检测到"
    SYSTEM="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ macOS 系统检测到"
    SYSTEM="macos"
else
    echo -e "${RED}❌ 不支持的系统：$OSTYPE${NC}"
    exit 1
fi

echo ""

# 步骤 1: 安装 Ollama
echo "📦 步骤 1/4: 安装 Ollama (本地 LLM 运行器)..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama 已安装${NC}"
    ollama --version
else
    echo "⬇️  下载并安装 Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}✅ Ollama 安装成功${NC}"
    else
        echo -e "${RED}❌ Ollama 安装失败${NC}"
        exit 1
    fi
fi

echo ""

# 步骤 2: 拉取模型
echo "📦 步骤 2/4: 拉取 Llama 3.1 模型 (8B)..."
if ollama list | grep -q "llama3.1"; then
    echo -e "${GREEN}✅ Llama 3.1 已存在${NC}"
else
    echo "⬇️  拉取模型 (约需 5-10 分钟，取决于网速)..."
    ollama pull llama3.1:8b
    
    if ollama list | grep -q "llama3.1"; then
        echo -e "${GREEN}✅ 模型拉取成功${NC}"
    else
        echo -e "${YELLOW}⚠️  模型拉取失败，可稍后手动执行：ollama pull llama3.1:8b${NC}"
    fi
fi

echo ""

# 步骤 3: 安装 Python 依赖
echo "📦 步骤 3/4: 安装 Python 依赖..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ -f "requirements_geo.txt" ]; then
    pip install -r requirements_geo.txt
else
    echo "⬇️  安装基础依赖..."
    pip install requests chromadb
fi

echo -e "${GREEN}✅ Python 依赖安装完成${NC}"

echo ""

# 步骤 4: 配置 Google Custom Search
echo "📦 步骤 4/4: 配置 Google Custom Search (可选)"
echo ""
echo "💡 Google Custom Search 提供每天 100 次免费搜索"
echo "   配置步骤:"
echo "   1. 访问：https://cse.google.com/cse/all"
echo "   2. 创建新搜索引擎"
echo "   3. 获取 Search Engine ID (cx)"
echo "   4. 访问：https://console.cloud.google.com/apis/credentials"
echo "   5. 创建 API Key"
echo "   6. 启用 Custom Search API"
echo ""
read -p "是否现在配置？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "输入 Google API Key: " GOOGLE_API_KEY
    read -p "输入 Google CSE ID: " GOOGLE_CSE_ID
    
    # 更新配置文件
    if [ -f "geo_config.json" ]; then
        # 使用 sed 更新配置 (需要安装 jq 或手动编辑)
        echo "✅ 请在 geo_config.json 中手动添加以下配置:"
        echo ""
        echo "  \"google_api_key\": \"$GOOGLE_API_KEY\","
        echo "  \"google_cse_id\": \"$GOOGLE_CSE_ID\""
        echo ""
    fi
else
    echo "⏭️  跳过配置，可稍后手动编辑 geo_config.json"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ 部署完成！${NC}"
echo "=========================================="
echo ""
echo "📚 下一步:"
echo "   1. 启动 Ollama 服务：ollama serve"
echo "   2. 运行 GEO 审计：python3 geo_auditor_open_source.py"
echo "   3. 查看指南：cat GEO_OPEN_SOURCE_GUIDE.md"
echo ""
echo "💰 成本：$0/月 (完全免费开源)"
echo "=========================================="
echo ""

# 测试 Ollama
echo "🧪 测试 Ollama 连接..."
if ollama list &> /dev/null; then
    echo -e "${GREEN}✅ Ollama 运行正常${NC}"
    echo ""
    echo "可用模型:"
    ollama list
else
    echo -e "${YELLOW}⚠️  Ollama 未运行，请先执行：ollama serve${NC}"
fi

echo ""
echo "🎉 开始使用 GEO 开源方案！"
