#!/bin/bash
# Dashboard 自动管理器 - 仅太一 Dashboard
# 功能：
# 1. 太一 Dashboard 按需启动 + 闲置 20 分钟自动关闭
# 2. 其他 Dashboard 不自动管理，按需手动启动

set -e

LOG_DIR="/home/nicola/.openclaw/workspace/logs"
LOG_FILE="$LOG_DIR/dashboard-auto-manager.log"
STATE_FILE="/tmp/taiyi-dashboard-state.json"
IDLE_TIMEOUT=1200
CHECK_INTERVAL=120

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

check_port() {
    local port=$1
    curl -s -o /dev/null -w "%{http_code}" http://localhost:$port --connect-timeout 2 2>/dev/null | grep -q "200"
    return $?
}

start_taiyi() {
    if check_port 5001; then
        log "✅ 太一 Dashboard 已在运行 (端口 5001)"
        return 0
    fi
    
    log "🚀 启动 太一 Dashboard (端口 5001)..."
    cd /home/nicola/.openclaw/workspace/skills/taiyi-dashboard
    nohup python3 app.py > /tmp/taiyi-dashboard.log 2>&1 &
    sleep 3
    
    if check_port 5001; then
        log "✅ 太一 Dashboard 启动成功"
        record_access
        return 0
    else
        log "❌ 太一 Dashboard 启动失败"
        return 1
    fi
}

stop_taiyi() {
    if ! check_port 5001; then
        log "ℹ️  太一 Dashboard 未运行"
        return 0
    fi
    
    log "⏹️  停止 太一 Dashboard (端口 5001)..."
    
    local pid=$(lsof -t -i:5001 2>/dev/null | head -1)
    if [ -n "$pid" ]; then
        kill -15 $pid 2>/dev/null || kill -9 $pid 2>/dev/null
        sleep 2
        log "✅ 太一 Dashboard 已停止"
    else
        log "⚠️  未找到太一 Dashboard 进程"
    fi
}

get_idle_time() {
    if [ -f "$STATE_FILE" ]; then
        local last_access=$(cat "$STATE_FILE" | grep -o '"last_access":"[^"]*"' | cut -d'"' -f4)
        if [ -n "$last_access" ]; then
            local last_ts=$(date -d "$last_access" +%s 2>/dev/null || date +%s)
            local now_ts=$(date +%s)
            echo $((now_ts - last_ts))
            return
        fi
    fi
    echo 0
}

record_access() {
    echo "{\"last_access\":\"$(date -Iseconds)\",\"running\":true}" > "$STATE_FILE"
    log "📝 记录用户访问"
}

save_state() {
    local running=$1
    echo "{\"last_access\":\"$(date -Iseconds)\",\"running\":$running}" > "$STATE_FILE"
}

check_activity() {
    # 检查太一 Dashboard 是否有访问
    if check_port 5001; then
        # 检查日志是否有最近访问
        local log_file="/tmp/taiyi-dashboard.log"
        if [ -f "$log_file" ]; then
            local recent=$(tail -50 "$log_file" 2>/dev/null | grep -i "GET\|POST" | tail -3)
            if [ -n "$recent" ]; then
                return 0
            fi
        fi
        # 端口开放即认为有活动
        return 0
    fi
    return 1
}

start_all() {
    log "🚀 启动 太一 Dashboard..."
    start_taiyi
    log "✅ 启动完成"
}

stop_all() {
    log "⏹️  停止 太一 Dashboard..."
    stop_taiyi
    save_state "false"
    log "✅ 停止完成"
}

status() {
    echo "========== Dashboard 状态 =========="
    echo ""
    echo "【太一 Dashboard】(自动管理)"
    if check_port 5001; then
        echo "  状态：✅ 运行中 (端口 5001)"
        echo "  访问：http://localhost:5001"
    else
        echo "  状态：⚪ 未运行"
        echo "  提示：访问时自动启动，或手动运行 './dashboard-auto-manager.sh start'"
    fi
    
    echo ""
    echo "【其他 Dashboard】(手动管理)"
    echo "  Bot Dashboard   (3001): 按需启动"
    echo "  Skill Dashboard (5002): 按需启动"
    echo "  百度网盘 API    (5003): 按需启动"
    
    local idle_time=$(get_idle_time)
    local idle_minutes=$((idle_time / 60))
    echo ""
    echo "闲置时间：${idle_minutes}分钟"
    echo "自动关闭：${IDLE_TIMEOUT}秒 (${IDLE_TIMEOUT}分钟)"
    echo "=================================="
}

auto_run() {
    log "========== 太一 Dashboard 自动管理器启动 =========="
    log "管理对象：太一 Dashboard (端口 5001)"
    log "闲置超时：${IDLE_TIMEOUT}秒 (20 分钟)"
    log "检查间隔：${CHECK_INTERVAL}秒 (2 分钟)"
    log ""
    log "💡 提示：其他 Dashboard 需手动启动"
    log "   Bot Dashboard:   cd skills/bot-dashboard && npm run dev"
    log "   Skill Dashboard: cd skills/skill-dashboard && python3 app.py"
    log "   百度网盘 API:    cd skills/baidu-netdisk-integration && python3 app.py"
    log "=========================================="
    
    while true; do
        local idle_time=$(get_idle_time)
        local idle_minutes=$((idle_time / 60))
        
        if [ $((idle_time % 600)) -eq 0 ]; then
            log "⏱️  当前闲置时间：${idle_minutes}分钟"
        fi
        
        if check_activity; then
            record_access
            if [ $((idle_time % 600)) -eq 0 ]; then
                log "✅ 有用户活动，保持运行"
            fi
        else
            if [ $idle_time -ge $IDLE_TIMEOUT ]; then
                log "⚠️  闲置超过 20 分钟，关闭太一 Dashboard..."
                stop_taiyi
                save_state "false"
                log "💤 进入休眠模式，等待下次访问"
            else
                if [ $((idle_time % 600)) -eq 0 ]; then
                    log "ℹ️  无活动，继续监控"
                fi
            fi
        fi
        
        sleep $CHECK_INTERVAL
    done
}

case "${1:-auto}" in
    auto)
        auto_run
        ;;
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    status)
        status
        ;;
    open)
        # 立即打开太一 Dashboard
        start_taiyi
        echo "✅ 太一 Dashboard 已启动"
        echo "🌐 访问地址：http://localhost:5001"
        ;;
    close)
        stop_all
        echo "✅ 太一 Dashboard 已关闭"
        ;;
    *)
        echo "太一 Dashboard 自动管理器"
        echo ""
        echo "用法：$0 {auto|start|stop|status|open|close}"
        echo ""
        echo "命令说明:"
        echo "  auto   - 自动管理 (后台运行)"
        echo "  start  - 手动启动太一 Dashboard"
        echo "  stop   - 手动停止太一 Dashboard"
        echo "  status - 查看状态"
        echo "  open   - 立即打开太一 Dashboard"
        echo "  close  - 立即关闭太一 Dashboard"
        echo ""
        echo "自动管理:"
        echo "  - 闲置 20 分钟后自动关闭"
        echo "  - 访问时自动启动"
        echo "  - 每 2 分钟检查一次"
        echo ""
        echo "其他 Dashboard (手动管理):"
        echo "  Bot Dashboard:   cd skills/bot-dashboard && npm run dev"
        echo "  Skill Dashboard: cd skills/skill-dashboard && python3 app.py"
        echo "  百度网盘 API:    cd skills/baidu-netdisk-integration && python3 app.py"
        exit 1
        ;;
esac
