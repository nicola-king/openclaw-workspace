#!/bin/bash
# 软件安全安装脚本
# 用法：./install-safe.sh <package> [port]

set -e

PACKAGE=${1:-$2}
PORT=${2:-}
BACKUP_DIR="/opt/backup/$(date +%Y%m%d-%H%M%S)"

if [ -z "$PACKAGE" ]; then
    echo "用法：$0 <package> [port]"
    exit 1
fi

echo "=========================================="
echo "软件安全安装流程"
echo "=========================================="
echo ""
echo "【安装目标】$PACKAGE"
if [ ! -z "$PORT" ]; then
    echo "【预期端口】$PORT"
fi
echo ""

# 步骤 1: 检测
echo "【步骤 1/6】检测系统状态"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/install-check.sh" ]; then
    bash "$SCRIPT_DIR/install-check.sh" $PACKAGE $PORT
else
    echo "⚠️  检测脚本不存在，继续执行..."
fi
echo ""

# 步骤 2: 备份
echo "【步骤 2/6】备份现有配置"
mkdir -p "$BACKUP_DIR"
echo "备份目录：$BACKUP_DIR"

# 备份配置
cp -r ~/.config/$PACKAGE "$BACKUP_DIR/" 2>/dev/null && echo "  ✅ 已备份 ~/.config/$PACKAGE" || echo "  ℹ️  无用户配置"
cp -r /etc/$PACKAGE "$BACKUP_DIR/" 2>/dev/null && echo "  ✅ 已备份 /etc/$PACKAGE" || echo "  ℹ️  无系统配置"
cp -r /var/lib/$PACKAGE "$BACKUP_DIR/" 2>/dev/null && echo "  ✅ 已备份 /var/lib/$PACKAGE" || echo "  ℹ️  无数据目录"

# 备份服务
cp /etc/systemd/system/$PACKAGE.service "$BACKUP_DIR/" 2>/dev/null && echo "  ✅ 已备份系统服务" || echo "  ℹ️  无系统服务"
cp ~/.config/systemd/user/$PACKAGE.service "$BACKUP_DIR/" 2>/dev/null && echo "  ✅ 已备份用户服务" || echo "  ℹ️  无用户服务"

echo ""

# 步骤 3: 修复或清理
echo "【步骤 3/6】尝试修复现有安装"

# 检查是否已安装
if dpkg -l | grep -q "^ii  $PACKAGE"; then
    echo "检测到已安装，尝试修复..."
    
    # 尝试修复依赖
    sudo apt --fix-broken install -y && echo "  ✅ 依赖修复成功" || echo "  ⚠️  依赖修复失败"
    
    # 尝试重启服务
    systemctl restart $PACKAGE 2>/dev/null && echo "  ✅ 系统服务重启成功" || echo "  ℹ️  无系统服务"
    systemctl --user restart $PACKAGE 2>/dev/null && echo "  ✅ 用户服务重启成功" || echo "  ℹ️  无用户服务"
    
    # 验证
    sleep 3
    if systemctl --user is-active $PACKAGE &> /dev/null || systemctl is-active $PACKAGE &> /dev/null; then
        echo "✅ 修复成功，无需重装"
        echo ""
        echo "=========================================="
        echo "✅ 安装流程完成 (修复模式)"
        echo "=========================================="
        exit 0
    else
        echo "❌ 修复失败，执行清理..."
        
        # 停止服务
        systemctl stop $PACKAGE 2>/dev/null || true
        systemctl --user stop $PACKAGE 2>/dev/null || true
        pkill -9 $PACKAGE 2>/dev/null || true
        
        # 删除包
        sudo apt remove --purge -y $PACKAGE && echo "  ✅ 已删除包" || echo "  ⚠️  删除失败"
        
        # 清理残留
        rm -rf ~/.config/$PACKAGE 2>/dev/null || true
        rm -rf ~/.local/state/$PACKAGE 2>/dev/null || true
        rm -rf /var/lib/$PACKAGE 2>/dev/null || true
        
        # 清理 systemd
        rm /etc/systemd/system/$PACKAGE.service 2>/dev/null || true
        rm ~/.config/systemd/user/$PACKAGE.service 2>/dev/null || true
        systemctl daemon-reload
        systemctl --user daemon-reload
        
        echo "✅ 清理完成"
    fi
else
    echo "ℹ️  未安装，执行新安装"
fi

echo ""

# 步骤 4: 安装
echo "【步骤 4/6】执行安装"
sudo apt update
sudo apt install -y $PACKAGE
echo "✅ 安装完成"

echo ""

# 步骤 5: 配置
echo "【步骤 5/6】配置服务"

# 启用服务
systemctl enable $PACKAGE 2>/dev/null && echo "  ✅ 系统服务已启用" || echo "  ℹ️  无系统服务"
systemctl --user enable $PACKAGE 2>/dev/null && echo "  ✅ 用户服务已启用" || echo "  ℹ️  无用户服务"

# 启动服务
systemctl start $PACKAGE 2>/dev/null && echo "  ✅ 系统服务已启动" || echo "  ℹ️  无系统服务"
systemctl --user start $PACKAGE 2>/dev/null && echo "  ✅ 用户服务已启动" || echo "  ℹ️  无用户服务"

# 配置防火墙
if [ ! -z "$PORT" ]; then
    echo "配置防火墙 (端口：$PORT)..."
    sudo ufw allow $PORT/tcp comment "$PACKAGE TCP" 2>/dev/null && echo "  ✅ TCP 端口已开放" || echo "  ⚠️  防火墙配置失败"
    sudo ufw allow $PORT/udp comment "$PACKAGE UDP" 2>/dev/null && echo "  ✅ UDP 端口已开放" || echo "  ⚠️  防火墙配置失败"
fi

echo ""

# 步骤 6: 测试
echo "【步骤 6/6】运行测试"
sleep 5

# 测试 1: 服务状态
echo "测试 1: 服务状态..."
if systemctl --user is-active $PACKAGE &> /dev/null || systemctl is-active $PACKAGE &> /dev/null; then
    echo "  ✅ 服务运行正常"
else
    echo "  ❌ 服务未运行"
fi

# 测试 2: 端口监听
if [ ! -z "$PORT" ]; then
    echo "测试 2: 端口监听 ($PORT)..."
    if ss -tlnp 2>/dev/null | grep -q ":$PORT "; then
        echo "  ✅ 端口监听正常"
    else
        echo "  ❌ 端口未监听"
    fi
fi

# 测试 3: Web 访问 (如果有端口)
if [ ! -z "$PORT" ]; then
    echo "测试 3: Web 访问..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$PORT 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
        echo "  ✅ Web 访问正常 (HTTP $HTTP_CODE)"
    else
        echo "  ❌ Web 访问失败 (HTTP $HTTP_CODE)"
    fi
fi

# 测试 4: 资源占用
echo "测试 4: 资源占用..."
MEM=$(ps aux | grep $PACKAGE | grep -v grep | awk '{sum+=$4} END {print sum}' 2>/dev/null || echo "0")
if [ ! -z "$MEM" ] && [ $(echo "$MEM < 20" | bc -l 2>/dev/null || echo 0) -eq 1 ]; then
    echo "  ✅ 内存占用正常 (${MEM}%)"
else
    echo "  ℹ️  内存占用：${MEM}%"
fi

echo ""
echo "=========================================="
echo "✅ 安装流程完成"
echo "=========================================="
echo ""
echo "备份位置：$BACKUP_DIR"
echo ""
echo "【回滚命令】"
echo "  cp -r $BACKUP_DIR/$PACKAGE ~/.config/ 2>/dev/null"
echo "  cp $BACKUP_DIR/$PACKAGE.service /etc/systemd/system/ 2>/dev/null"
echo "  systemctl daemon-reload && systemctl restart $PACKAGE"
echo ""
