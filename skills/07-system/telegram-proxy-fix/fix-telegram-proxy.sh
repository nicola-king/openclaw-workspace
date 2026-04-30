#!/bin/bash
# Telegram 代理修复脚本
# 问题：OpenClaw Telegram 模块未使用代理配置
# 解决：设置环境变量并重启 Gateway

set -e

echo "=========================================="
echo "🔧 Telegram 代理修复"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. 检查代理是否可用
echo "1️⃣  检查代理状态..."
if curl -s -x http://127.0.0.1:7890 -o /dev/null -w "%{http_code}" "https://api.telegram.org/" | grep -q "200\|404"; then
    echo -e "${GREEN}✅ 代理可用 (127.0.0.1:7890)${NC}"
else
    echo -e "${RED}❌ 代理不可用${NC}"
    echo "请检查 Clash 是否运行：ps aux | grep clash"
    exit 1
fi

echo ""

# 2. 检查 .env 配置
echo "2️⃣  检查环境变量配置..."
ENV_FILE="/home/nicola/.openclaw/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  .env 文件不存在，创建中...${NC}"
    cat > "$ENV_FILE" << EOF
# Telegram 配置
TELEGRAM_BOT_TOKEN=8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY
TELEGRAM_CHAT_ID=7073481596

# 代理配置 (Telegram 专用)
HTTPS_PROXY=http://127.0.0.1:7890
HTTP_PROXY=http://127.0.0.1:7890
NO_PROXY=localhost,127.0.0.1,*.weixin.qq.com,*.feishu.cn
EOF
    echo -e "${GREEN}✅ .env 已创建${NC}"
else
    # 检查是否已有代理配置
    if grep -q "HTTPS_PROXY" "$ENV_FILE" && grep -q "127.0.0.1:7890" "$ENV_FILE"; then
        echo -e "${GREEN}✅ 代理配置已存在${NC}"
    else
        echo -e "${YELLOW}⚠️  添加代理配置...${NC}"
        cat >> "$ENV_FILE" << EOF

# Telegram 代理配置 (添加于 $(date +%Y-%m-%d_%H:%M:%S))
HTTPS_PROXY=http://127.0.0.1:7890
HTTP_PROXY=http://127.0.0.1:7890
EOF
        echo -e "${GREEN}✅ 代理配置已添加${NC}"
    fi
fi

echo ""

# 3. 导出环境变量 (当前 shell)
echo "3️⃣  导出环境变量..."
export HTTPS_PROXY="http://127.0.0.1:7890"
export HTTP_PROXY="http://127.0.0.1:7890"
export NO_PROXY="localhost,127.0.0.1,*.weixin.qq.com,*.feishu.cn"
echo -e "${GREEN}✅ 环境变量已导出${NC}"

echo ""

# 4. 重启 Gateway
echo "4️⃣  重启 OpenClaw Gateway..."
openclaw gateway restart

echo ""

# 5. 等待 Gateway 启动
echo "5️⃣  等待 Gateway 启动..."
sleep 5

# 检查 Gateway 状态
if openclaw gateway status 2>&1 | grep -q "running"; then
    echo -e "${GREEN}✅ Gateway 已启动${NC}"
else
    echo -e "${RED}❌ Gateway 启动失败${NC}"
    exit 1
fi

echo ""

# 6. 测试 Telegram 连接
echo "6️⃣  测试 Telegram 连接..."
sleep 3  # 等待 Gateway 完全初始化

# 使用 bot API 测试
TEST_RESULT=$(curl -s -x http://127.0.0.1:7890 "https://api.telegram.org/bot8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY/getMe" | jq -r '.ok')

if [ "$TEST_RESULT" = "true" ]; then
    echo -e "${GREEN}✅ Telegram API 连接成功${NC}"
else
    echo -e "${YELLOW}⚠️  Telegram API 连接失败，但 Gateway 已配置代理${NC}"
    echo "请查看日志：tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep telegram"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Telegram 代理修复完成！${NC}"
echo "=========================================="
echo ""
echo "📋 下一步:"
echo "   1. 在 Telegram 中打开 @sayelfbot"
echo "   2. 发送 /start 测试"
echo "   3. 查看日志：tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep telegram"
echo ""
echo "🔧 配置详情:"
echo "   代理：http://127.0.0.1:7890"
echo "   环境变量：HTTPS_PROXY, HTTP_PROXY"
echo "   配置文件：$ENV_FILE"
echo ""
