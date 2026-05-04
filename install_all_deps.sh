#!/bin/bash
# =============================================================================
# 太一系统统一安装脚本
# 一键安装所有项目依赖
# =============================================================================

set -e  # 遇到错误立即退出

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           太一 AGI 系统统一安装脚本                          ║"
echo "║           时间: $(date '+%Y-%m-%d %H:%M:%S')                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 sudo 权限
check_sudo() {
    echo -e "${BLUE}[1/5] 检查 sudo 权限...${NC}"
    if ! sudo -n true 2>/dev/null; then
        echo -e "${RED}✗ 需要 sudo 权限${NC}"
        echo "请运行: sudo bash install_all_deps.sh"
        exit 1
    fi
    echo -e "${GREEN}✓ sudo 权限已确认${NC}"
}

# 安装系统依赖
install_system_deps() {
    echo -e "\n${BLUE}[2/5] 安装系统依赖...${NC}"
    
    sudo apt update
    
    # Python 基础
    sudo apt install -y python3-pip python3-venv python3-dev
    
    # 编译工具
    sudo apt install -y build-essential gcc g++ make
    
    # 开发库
    sudo apt install -y libffi-dev libssl-dev
    sudo apt install -y libxml2-dev libxslt1-dev
    sudo apt install -y zlib1g-dev libjpeg-dev libpng-dev
    
    # 音频处理 (TTS)
    sudo apt install -y libsndfile1-dev portaudio19-dev
    
    # 浏览器自动化
    sudo apt install -y chromium-browser chromium-chromedriver
    
    echo -e "${GREEN}✓ 系统依赖安装完成${NC}"
}

# 安装 MOSS-TTS-Nano
install_moss_tts() {
    echo -e "\n${BLUE}[3/5] 安装 MOSS-TTS-Nano...${NC}"
    
    cd /home/sayelf/.openclaw/workspace/skills/moss-tts-nano
    
    # 创建虚拟环境
    python3 -m venv venv-moss-tts
    source venv-moss-tts/bin/activate
    
    # 安装依赖
    pip install --upgrade pip
    pip install numpy scipy librosa soundfile
    pip install onnxruntime  # CPU版本
    
    # 安装 Playwright (用于网页抓取)
    pip install playwright
    playwright install chromium
    
    deactivate
    
    echo -e "${GREEN}✓ MOSS-TTS-Nano 安装完成${NC}"
}

# 安装 Maigret
install_maigret() {
    echo -e "\n${BLUE}[4/5] 安装 Maigret...${NC}"
    
    cd /home/sayelf/.openclaw/workspace/skills/maigret
    
    # 创建虚拟环境
    python3 -m venv venv-maigret
    source venv-maigret/bin/activate
    
    # 安装依赖
    pip install --upgrade pip
    pip install -e .
    
    deactivate
    
    echo -e "${GREEN}✓ Maigret 安装完成${NC}"
}

# 安装跨境贸易 Agent 依赖
install_trading_agent() {
    echo -e "\n${BLUE}[5/5] 安装跨境贸易 Agent 依赖...${NC}"
    
    cd /home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent
    
    # 创建虚拟环境
    python3 -m venv venv-trading
    source venv-trading/bin/activate
    
    # 安装基础依赖
    pip install --upgrade pip
    pip install requests beautifulsoup4 lxml
    pip install pandas numpy matplotlib
    pip install python-telegram-bot
    
    # 安装反爬工具
    pip install fake-useragent requests-cache
    pip install crawl4ai
    
    deactivate
    
    echo -e "${GREEN}✓ 跨境贸易 Agent 依赖安装完成${NC}"
}

# 验证安装
verify_installation() {
    echo -e "\n${BLUE}[验证] 检查安装结果...${NC}"
    
    # 检查 Python
    python3 --version
    pip3 --version
    
    # 检查虚拟环境
    echo -e "\n${YELLOW}虚拟环境列表:${NC}"
    ls -la /home/sayelf/.openclaw/workspace/skills/*/venv-* 2>/dev/null || echo "无虚拟环境"
    
    echo -e "\n${GREEN}✓ 验证完成${NC}"
}

# 主函数
main() {
    echo -e "${YELLOW}开始安装太一系统所有依赖...${NC}\n"
    
    check_sudo
    install_system_deps
    install_moss_tts
    install_maigret
    install_trading_agent
    verify_installation
    
    echo -e "\n╔══════════════════════════════════════════════════════════════╗"
    echo -e "║           ${GREEN}✓ 所有依赖安装完成！${NC}                             ║"
    echo -e "╚══════════════════════════════════════════════════════════════╝"
    echo -e "\n${YELLOW}后续步骤:${NC}"
    echo "1. 配置外部 API Keys (参考各项目文档)"
    echo "2. 测试各模块功能"
    echo "3. 配置 OpenClaw Gateway Skill 注册"
    echo -e "\n${YELLOW}使用方式:${NC}"
    echo "- MOSS-TTS: cd skills/moss-tts-nano && source venv-moss-tts/bin/activate"
    echo "- Maigret: cd skills/maigret && source venv-maigret/bin/activate"
    echo "- 跨境贸易: cd skills/cross-border-trade-agent && source venv-trading/bin/activate"
}

# 执行
main
