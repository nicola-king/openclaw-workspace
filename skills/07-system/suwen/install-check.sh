#!/bin/bash
# 软件安装前检测脚本
# 用法：./install-check.sh <package> [port]

set -e

PACKAGE=${1:-$2}
PORT=${2:-}

if [ -z "$PACKAGE" ]; then
    echo "用法：$0 <package> [port]"
    exit 1
fi

echo "=========================================="
echo "软件安装前检测报告"
echo "=========================================="
echo ""
echo "【检测目标】$PACKAGE"
if [ ! -z "$PORT" ]; then
    echo "【预期端口】$PORT"
fi
echo ""

# 1. 检查已安装版本
echo "【1. 安装状态】"
APT_INSTALLED=false
SNAP_INSTALLED=false
COMMAND_EXISTS=false

if dpkg -l | grep -q "^ii  $PACKAGE"; then
    VERSION=$(dpkg -l | grep "^ii  $PACKAGE" | awk '{print $3}')
    echo "  ✅ apt: 已安装 (版本：$VERSION)"
    APT_INSTALLED=true
else
    echo "  ❌ apt: 未安装"
fi

if snap list 2>/dev/null | grep -q "$PACKAGE"; then
    VERSION=$(snap list 2>/dev/null | grep "$PACKAGE" | awk '{print $3}')
    echo "  ✅ snap: 已安装 (版本：$VERSION)"
    SNAP_INSTALLED=true
else
    echo "  ❌ snap: 未安装"
fi

if command -v $PACKAGE &> /dev/null; then
    echo "  ✅ 命令：可用 ($(which $PACKAGE))"
    COMMAND_EXISTS=true
else
    echo "  ❌ 命令：不可用"
fi

echo ""

# 2. 检查服务状态
echo "【2. 服务状态】"
SYSTEM_SERVICE=false
USER_SERVICE=false

if systemctl is-active $PACKAGE &> /dev/null; then
    echo "  ✅ 系统服务：运行中"
    SYSTEM_SERVICE=true
elif systemctl is-enabled $PACKAGE &> /dev/null 2>&1; then
    echo "  ⚠️  系统服务：已启用但未运行"
    SYSTEM_SERVICE=true
else
    echo "  ❌ 系统服务：未配置"
fi

if systemctl --user is-active $PACKAGE &> /dev/null 2>&1; then
    echo "  ✅ 用户服务：运行中"
    USER_SERVICE=true
elif systemctl --user is-enabled $PACKAGE &> /dev/null 2>&1; then
    echo "  ⚠️  用户服务：已启用但未运行"
    USER_SERVICE=true
else
    echo "  ❌ 用户服务：未配置"
fi

echo ""

# 3. 检查进程
echo "【3. 进程状态】"
PROCESS_COUNT=$(ps aux | grep $PACKAGE | grep -v grep | wc -l)
if [ $PROCESS_COUNT -gt 0 ]; then
    echo "  ✅ 进程运行中 (数量：$PROCESS_COUNT)"
    ps aux | grep $PACKAGE | grep -v grep | head -3 | awk '{print "     PID: "$2", CPU: "$3"%, MEM: "$4"%"}'
else
    echo "  ❌ 无进程运行"
fi

echo ""

# 4. 检查端口占用
if [ ! -z "$PORT" ]; then
    echo "【4. 端口占用 ($PORT)】"
    if ss -tlnp 2>/dev/null | grep -q ":$PORT "; then
        echo "  ⚠️  端口已占用"
        ss -tlnp 2>/dev/null | grep ":$PORT " | head -3
    else
        echo "  ✅ 端口空闲"
    fi
    echo ""
fi

# 5. 检查依赖
echo "【5. 依赖检查】"
if apt-cache depends $PACKAGE 2>/dev/null | head -20 | grep -q Depends; then
    DEP_COUNT=$(apt-cache depends $PACKAGE 2>/dev/null | grep "^  Depends:" | wc -l)
    echo "  依赖数量：$DEP_COUNT"
    apt-cache depends $PACKAGE 2>/dev/null | grep "^  Depends:" | head -5 | sed 's/^/    /'
else
    echo "  ℹ️  无依赖或无法检查"
fi

echo ""

# 6. 检查磁盘空间
echo "【6. 磁盘空间】"
ROOT_FREE=$(df -h / | tail -1 | awk '{print $4}')
HOME_FREE=$(df -h /home | tail -1 | awk '{print $4}')
echo "  根分区可用：$ROOT_FREE"
echo "  家目录可用：$HOME_FREE"

echo ""

# 7. 风险评估
echo "【7. 风险评估】"
RISK_SCORE=0

# 多版本共存
if [ "$APT_INSTALLED" = true ] && [ "$SNAP_INSTALLED" = true ]; then
    echo "  ⚠️  多版本共存 (+3 分)"
    RISK_SCORE=$((RISK_SCORE + 3))
fi

# 服务冲突
if [ "$SYSTEM_SERVICE" = true ] && [ "$USER_SERVICE" = true ]; then
    echo "  ⚠️  服务配置冲突 (+2 分)"
    RISK_SCORE=$((RISK_SCORE + 2))
fi

# 端口占用
if [ ! -z "$PORT" ] && ss -tlnp 2>/dev/null | grep -q ":$PORT "; then
    echo "  ⚠️  端口冲突 (+2 分)"
    RISK_SCORE=$((RISK_SCORE + 2))
fi

if [ $RISK_SCORE -eq 0 ]; then
    echo "  ✅ 低风险 (0 分) - 可安全安装/升级"
elif [ $RISK_SCORE -le 3 ]; then
    echo "  🟡 中风险 ($RISK_SCORE 分) - 需要修复"
else
    echo "  🔴 高风险 ($RISK_SCORE 分) - 需要清理后重装"
fi

echo ""

# 8. 建议
echo "【8. 建议方案】"
if [ "$APT_INSTALLED" = true ] || [ "$SNAP_INSTALLED" = true ]; then
    if [ $RISK_SCORE -eq 0 ]; then
        echo "  → 优先修复现有安装"
        echo "  → 命令：systemctl restart $PACKAGE"
    elif [ $RISK_SCORE -le 3 ]; then
        echo "  → 尝试修复配置"
        echo "  → 命令：systemctl --user unmask $PACKAGE && systemctl --user daemon-reload"
    else
        echo "  → 建议彻底清理后重装"
        echo "  → 命令：apt remove --purge $PACKAGE && apt install -y $PACKAGE"
    fi
else
    echo "  → 执行新安装"
    echo "  → 命令：apt update && apt install -y $PACKAGE"
fi

echo ""
echo "=========================================="
echo "检测完成"
echo "=========================================="

# 输出 JSON 格式 (可选)
if [ "$1" = "--json" ]; then
    cat << EOF
{
  "package": "$PACKAGE",
  "installed": {
    "apt": $APT_INSTALLED,
    "snap": $SNAP_INSTALLED,
    "command": $COMMAND_EXISTS
  },
  "services": {
    "system": $SYSTEM_SERVICE,
    "user": $USER_SERVICE
  },
  "process_count": $PROCESS_COUNT,
  "risk_score": $RISK_SCORE
}
EOF
fi
