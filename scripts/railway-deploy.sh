#!/bin/bash
# Railway 部署自动化脚本
# 前提：SAYELF 已注册 Railway 账号

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/reports/railway-deploy-$(date +%Y%m%d).log"

echo "🚀 Railway 部署脚本" | tee -a $LOG_FILE
echo "====================" | tee -a $LOG_FILE

# 检查 Railway CLI
if ! command -v railway &> /dev/null; then
    echo "📦 安装 Railway CLI..." | tee -a $LOG_FILE
    npm install -g @railway/cli
fi

# 登录 Railway
echo "🔐 登录 Railway..." | tee -a $LOG_FILE
railway login

# 初始化项目
echo "📁 初始化项目..." | tee -a $LOG_FILE
cd $WORKSPACE
railway init || railway link

# 添加环境变量
echo "⚙️ 配置环境变量..." | tee -a $LOG_FILE
railway variables set TELEGRAM_BOT_TOKEN=$(cat /tmp/telegram-token 2>/dev/null || echo "PENDING")

# 部署
echo "🚀 开始部署..." | tee -a $LOG_FILE
railway up

echo "✅ 部署完成！" | tee -a $LOG_FILE
echo "获取 URL: railway status" | tee -a $LOG_FILE
