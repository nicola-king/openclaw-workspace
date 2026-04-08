#!/bin/bash
# PolyAlert 监控保障脚本
# 功能：进程监控 + 自动重启 + 状态报告

set -e

POLYALERT_DIR="/home/nicola/.openclaw/workspace/skills/polyalert"
LOG_FILE="/home/nicola/.openclaw/logs/polyalert-monitor.log"
PID_FILE="/tmp/polyalert.pid"
STATE_FILE="/tmp/polyalert-state.json"
RESTART_COUNT_FILE="/tmp/polyalert-restart-count"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查 PolyAlert 进程
check_polyalert() {
    PID=$(pgrep -f "python3 monitor.py" | head -1 || echo "")
    
    if [ -n "$PID" ]; then
        echo "$PID"
        return 0
    else
        echo ""
        return 1
    fi
}

# 启动 PolyAlert
start_polyalert() {
    log "${YELLOW}[启动]${NC} 启动 PolyAlert 监控服务..."
    
    cd "$POLYALERT_DIR"
    nohup python3 monitor.py > /tmp/polyalert-stdout.log 2>&1 &
    PID=$!
    
    echo "$PID" > "$PID_FILE"
    
    sleep 3
    
    if ps -p "$PID" > /dev/null 2>&1; then
        log "${GREEN}[启动成功]${NC} PID: $PID"
        return 0
    else
        log "${RED}[启动失败]${NC} PID: $PID"
        return 1
    fi
}

# 停止 PolyAlert
stop_polyalert() {
    PID=$(check_polyalert)
    
    if [ -n "$PID" ]; then
        log "${YELLOW}[停止]${NC} 停止 PolyAlert (PID: $PID)..."
        kill "$PID" 2>/dev/null || true
        sleep 2
        
        # 如果还在运行，强制停止
        if ps -p "$PID" > /dev/null 2>&1; then
            kill -9 "$PID" 2>/dev/null || true
            log "${YELLOW}[强制停止]${NC} PID: $PID"
        fi
        
        rm -f "$PID_FILE"
        log "${GREEN}[停止成功]${NC}"
    fi
}

# 重启 PolyAlert
restart_polyalert() {
    log "${YELLOW}[重启]${NC} 重启 PolyAlert..."
    stop_polyalert
    sleep 2
    start_polyalert
}

# 获取重启次数
get_restart_count() {
    if [ -f "$RESTART_COUNT_FILE" ]; then
        cat "$RESTART_COUNT_FILE"
    else
        echo "0"
    fi
}

# 增加重启次数
increment_restart_count() {
    COUNT=$(get_restart_count)
    COUNT=$((COUNT + 1))
    echo "$COUNT" > "$RESTART_COUNT_FILE"
    echo "$COUNT"
}

# 重置重启次数
reset_restart_count() {
    echo "0" > "$RESTART_COUNT_FILE"
}

# 更新状态文件
update_state() {
    local status="$1"
    local pid="$2"
    local restart_count="$3"
    local last_check="$(date +%s)"
    
    cat > "$STATE_FILE" << EOF
{
    "status": "$status",
    "pid": $pid,
    "restart_count": $restart_count,
    "last_check": $last_check,
    "last_check_time": "$(date '+%Y-%m-%d %H:%M:%S')"
}
EOF
}

# 主监控循环
monitor_loop() {
    log "${GREEN}[监控启动]${NC} PolyAlert 监控保障系统启动"
    
    while true; do
        PID=$(check_polyalert)
        
        if [ -n "$PID" ]; then
            # 运行正常
            RESTART_COUNT=$(get_restart_count)
            
            # 如果之前有重启记录，且现在正常运行，重置计数器
            if [ "$RESTART_COUNT" -gt 0 ]; then
                log "${GREEN}[恢复]${NC} PolyAlert 正常运行 (PID: $PID)，重置重启计数"
                reset_restart_count
            fi
            
            update_state "running" "$PID" "0"
            
            # 每 5 分钟检查一次日志
            if [ $(( $(date +%M) % 5 )) -eq 0 ]; then
                log "${GREEN}[心跳]${NC} PolyAlert 运行中 (PID: $PID)"
            fi
        else
            # 进程消失，自动重启
            RESTART_COUNT=$(increment_restart_count)
            
            log "${RED}[异常]${NC} PolyAlert 进程消失！重启次数：$RESTART_COUNT"
            
            # 重启次数过多告警
            if [ "$RESTART_COUNT" -ge 5 ]; then
                log "${RED}[告警]${NC} PolyAlert 重启次数过多 ($RESTART_COUNT)，需要人工干预！"
                # 可以添加 Telegram 通知
            fi
            
            # 尝试重启
            if start_polyalert; then
                NEW_PID=$(check_polyalert)
                update_state "restarted" "$NEW_PID" "$RESTART_COUNT"
                log "${GREEN}[重启成功]${NC} 新 PID: $NEW_PID"
            else
                update_state "failed" "0" "$RESTART_COUNT"
                log "${RED}[重启失败]${NC} 需要人工干预"
            fi
        fi
        
        # 每 60 秒检查一次
        sleep 60
    done
}

# 显示状态
show_status() {
    echo "=== PolyAlert 监控状态 ==="
    echo ""
    
    PID=$(check_polyalert)
    
    if [ -n "$PID" ]; then
        echo -e "进程状态：${GREEN}运行中${NC} (PID: $PID)"
    else
        echo -e "进程状态：${RED}已停止${NC}"
    fi
    
    if [ -f "$STATE_FILE" ]; then
        echo ""
        echo "状态文件:"
        cat "$STATE_FILE"
    fi
    
    RESTART_COUNT=$(get_restart_count)
    echo ""
    echo "重启次数：$RESTART_COUNT"
    
    echo ""
    echo "最近日志:"
    tail -10 "$LOG_FILE"
}

# 主函数
main() {
    local action="${1:-monitor}"
    
    case "$action" in
        monitor)
            monitor_loop
            ;;
        start)
            start_polyalert
            ;;
        stop)
            stop_polyalert
            ;;
        restart)
            restart_polyalert
            ;;
        status)
            show_status
            ;;
        *)
            echo "用法：$0 {monitor|start|stop|restart|status}"
            exit 1
            ;;
    esac
}

main "$@"
