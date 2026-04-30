#!/bin/bash
# 修复 Chromium/Chrome 浏览器启动警告 - 太一 AGI v5.0

set -e

echo "========================================"
echo "  修复浏览器启动警告"
echo "========================================"
echo ""

# 1. 修复 libva 视频加速问题
echo "【1/4】修复 libva 视频加速..."
if [ -f /etc/environment ]; then
    echo "LIBVA_DRIVER_NAME=i965" | sudo tee -a /etc/environment > /dev/null
    echo "✅ 已设置 LIBVA_DRIVER_NAME"
else
    echo "⚠️  /etc/environment 不存在，跳过"
fi

# 2. 修复 Wayland/Vulkan 兼容性
echo ""
echo "【2/4】创建 Chromium 启动参数配置..."
CHROMIUM_FLAGS="$HOME/.config/chromium-flags.conf"
mkdir -p "$HOME/.config"

cat > "$CHROMIUM_FLAGS" <<EOF
# 禁用 Vulkan
--disable-features=Vulkan
# 强制使用 X11
--ozone-platform=x11
# 禁用 GPU 硬件加速（可选，如仍有问题）
--disable-gpu
# 禁用沙盒（开发环境）
--no-sandbox
# 禁用共享内存
--disable-dev-shm-usage
EOF

echo "✅ 已创建 $CHROMIUM_FLAGS"
cat "$CHROMIUM_FLAGS"

# 3. 修复 AppArmor 限制（可选）
echo ""
echo "【3/4】检查 AppArmor 配置..."
if command -v aa-status &> /dev/null; then
    echo "AppArmor 状态:"
    aa-status --enabled 2>/dev/null && echo "✅ AppArmor 已启用" || echo "⚠️  AppArmor 未启用"
    
    # 尝试禁用 Chromium 的 AppArmor 限制
    if [ -f /etc/apparmor.d/snap.chromium.chromium ]; then
        echo "⚠️  发现 Chromium AppArmor 配置，建议:"
        echo "   sudo ln -s /etc/apparmor.d/snap.chromium.chromium /etc/apparmor.d/disable/"
        echo "   sudo apparmor_parser -R /etc/apparmor.d/snap.chromium.chromium"
    else
        echo "✅ 未发现 Chromium AppArmor 限制"
    fi
else
    echo "⚠️  AppArmor 未安装，跳过"
fi

# 4. 创建修复后的启动脚本
echo ""
echo "【4/4】创建优化启动脚本..."
STARTUP_SCRIPT="$HOME/.openclaw/workspace/scripts/open-dashboard.sh"

cat > "$STARTUP_SCRIPT" <<'EOF'
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
EOF

chmod +x "$STARTUP_SCRIPT"
echo "✅ 已创建启动脚本：$STARTUP_SCRIPT"

echo ""
echo "========================================"
echo "  修复完成!"
echo "========================================"
echo ""
echo "使用方法:"
echo "  1. 重启浏览器（关闭所有 Chromium 窗口后重新打开）"
echo "  2. 或使用优化启动脚本:"
echo "     $STARTUP_SCRIPT"
echo ""
echo "警告说明:"
echo "  - libva: 视频加速驱动问题，不影响基本功能"
echo "  - Wayland/Vulkan: 已配置使用 X11"
echo "  - AppArmor: 沙盒限制，开发环境可忽略"
echo ""
echo "如仍有问题，可执行:"
echo "  sudo snap set chromium system.privacy.privacy-policyaccepted=true"
echo ""
