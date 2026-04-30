#!/bin/bash
# OpenClaw Dashboard 优化启动脚本

DASHBOARD_URL="http://localhost:3000"

# 检查 Dashboard 是否运行
if ! curl -s "$DASHBOARD_URL" > /dev/null; then
    echo "Dashboard 未运行，正在启动..."
    cd /tmp/OpenClaw-bot-review
    nohup npm run dev > /tmp/bot-dashboard.log 2>&1 &
    sleep 3
fi

# 使用优化参数打开浏览器
echo "打开 Dashboard: $DASHBOARD_URL"

# 尝试多种方式打开浏览器
if command -v chromium-browser &> /dev/null; then
    chromium-browser \
        --disable-features=Vulkan \
        --ozone-platform=x11 \
        --disable-gpu \
        --no-sandbox \
        --disable-dev-shm-usage \
        "$DASHBOARD_URL" &
elif command -v google-chrome &> /dev/null; then
    google-chrome \
        --disable-features=Vulkan \
        --ozone-platform=x11 \
        --disable-gpu \
        --no-sandbox \
        --disable-dev-shm-usage \
        "$DASHBOARD_URL" &
elif command -v xdg-open &> /dev/null; then
    xdg-open "$DASHBOARD_URL" &
else
    echo "❌ 未找到浏览器，请手动访问：$DASHBOARD_URL"
fi

echo "✅ Dashboard 已启动"
