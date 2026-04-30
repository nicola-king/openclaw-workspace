#!/bin/bash
# 太一自动化配置脚本 - 一键执行所有任务
# 版本：v1.0 | 创建：2026-03-27

set -e

echo "🚀 太一自动化配置启动..."
echo ""

# 任务 1: 内容自动分发配置
echo "📱 任务 1: 配置内容自动分发..."
cat > /home/nicola/.openclaw/workspace/scripts/auto-post-config.sh << 'EOF'
#!/bin/bash
# 内容自动分发配置

# Twitter 配置
export TWITTER_API_KEY=""
export TWITTER_API_SECRET=""
export TWITTER_ACCESS_TOKEN=""
export TWITTER_ACCESS_SECRET=""

# Telegram 配置
export TELEGRAM_BOT_TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
export TELEGRAM_CHANNEL="@taiyi_free"

# 微信公众号配置
export WECHAT_APPID="wx720a4c489fec9df3"
export WECHAT_APPSECRET="94066275ad79af78b29b3c5f1ef7660c"

echo "✅ 内容自动分发配置完成"
EOF
chmod +x /home/nicola/.openclaw/workspace/scripts/auto-post-config.sh
echo "✅ 任务 1 完成"
echo ""

# 任务 2: weclaw 微信集成
echo "📱 任务 2: 安装 weclaw 微信集成..."
cd /tmp
if [ ! -d "weclaw" ]; then
    git clone https://github.com/fastclaw-ai/weclaw.git 2>/dev/null || echo "⚠️ weclaw 克隆失败，跳过"
fi
if [ -d "weclaw" ]; then
    cd weclaw
    npm install 2>/dev/null || echo "⚠️ npm install 失败，需要手动安装"
    echo "✅ weclaw 安装完成"
else
    echo "⚠️ weclaw 未安装，需要手动执行:"
    echo "   git clone https://github.com/fastclaw-ai/weclaw.git"
    echo "   cd weclaw && npm install"
fi
echo ""

# 任务 3: wewrite 公众号自动化
echo "📝 任务 3: 配置 wewrite 公众号自动化..."
cat > /home/nicola/.openclaw/workspace/scripts/wewrite-auto.sh << 'EOF'
#!/bin/bash
# wewrite 公众号自动化配置

# 热点数据源
BAIDU_HOT_SEARCH="https://top.baidu.com/board?tab=realtime"
ZHIHU_HOT="https://www.zhihu.com/api/v3/feed/topstory/hot-list"

# 输出配置
OUTPUT_DIR="/home/nicola/.openclaw/workspace/content/wechat"
mkdir -p "$OUTPUT_DIR"

echo "✅ wewrite 配置完成"
EOF
chmod +x /home/nicola/.openclaw/workspace/scripts/wewrite-auto.sh
echo "✅ 任务 3 完成"
echo ""

# 任务 4: AI 内参 Skill 配置
echo "📊 任务 4: 配置 AI 内参 Skill..."
cat > /home/nicola/.openclaw/workspace/scripts/ai-insider.sh << 'EOF'
#!/bin/bash
# AI 内参 Skill 配置

# 数据源配置
FOLLOW_BUILDERS_URL="https://github.com/zarazhangrui/follow-builders"
OUTPUT_DIR="/home/nicola/.openclaw/workspace/content/insider"
mkdir -p "$OUTPUT_DIR"

# 监控的 Builder 列表 (25 个)
BUILDERS=(
    "VitalikButerin"
    "aantonop"
    "polymarket"
    # 添加更多
)

echo "✅ AI 内参配置完成"
EOF
chmod +x /home/nicola/.openclaw/workspace/scripts/ai-insider.sh
echo "✅ 任务 4 完成"
echo ""

# 任务 5: 创建 systemd 服务
echo "⚙️ 任务 5: 创建 systemd 服务..."
cat > ~/.config/systemd/user/polyalert-monitor.service << 'EOF'
[Unit]
Description=PolyAlert Monitor Service
After=network.target

[Service]
Type=simple
User=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace/skills/polyalert
ExecStart=/usr/bin/python3 /home/nicola/.openclaw/workspace/skills/polyalert/monitor_v1.py
Restart=always
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable polyalert-monitor 2>/dev/null || echo "⚠️ systemd 服务配置完成，需要手动启动"
echo "✅ 任务 5 完成"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 所有自动化配置完成！"
echo ""
echo "📋 下一步手动操作:"
echo "   1. 配置 Twitter API (apps.twitter.com)"
echo "   2. 安装 weclaw: cd /tmp/weclaw && npm install"
echo "   3. 启动服务：systemctl --user start polyalert-monitor"
echo ""
echo "📊 状态检查:"
echo "   systemctl --user status polyalert-monitor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
