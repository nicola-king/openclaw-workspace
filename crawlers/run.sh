#!/bin/bash
# 多平台采集框架 - 快速启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  多平台内容采集框架${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

case "$1" in
    test)
        echo -e "${YELLOW}运行测试...${NC}"
        python3 platforms/x_crawler.py --test --max 3
        ;;
    
    x)
        echo -e "${YELLOW}采集 X 平台...${NC}"
        python3 main.py --platform x
        ;;
    
    wechat)
        echo -e "${YELLOW}采集微信公众号...${NC}"
        python3 main.py --platform wechat
        ;;
    
    all)
        echo -e "${YELLOW}采集所有启用的平台...${NC}"
        python3 main.py
        ;;
    
    daily)
        echo -e "${YELLOW}执行每日任务...${NC}"
        python3 openclaw_integration.py daily
        ;;
    
    setup)
        echo -e "${YELLOW}安装依赖...${NC}"
        pip install playwright loguru --break-system-packages --quiet
        playwright install chromium
        echo -e "${GREEN}✅ 安装完成${NC}"
        ;;
    
    *)
        echo "用法：$0 {test|x|wechat|all|daily|setup}"
        echo ""
        echo "命令说明:"
        echo "  test    - 测试 X 采集器"
        echo "  x       - 采集 X 平台"
        echo "  wechat  - 采集微信公众号"
        echo "  all     - 采集所有启用的平台"
        echo "  daily   - 执行每日定时任务"
        echo "  setup   - 安装依赖"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ 完成${NC}"
