#!/bin/bash
# 核心系统监控脚本
# 监控 Ubuntu 系统和 Gateway 核心运行状态

LOG_FILE="/home/nicola/.openclaw/workspace/logs/core-monitor.log"
ALERT_THRESHOLD_CPU=80
ALERT_THRESHOLD_MEMORY=80
ALERT_THRESHOLD_DISK=90

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查 Ubuntu 系统资源
check_system_resources() {
    log "📊 检查系统资源..."
    
    # CPU 使用率
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if (( $(echo "$CPU_USAGE > $ALERT_THRESHOLD_CPU" | bc -l) )); then
        log "❌ CPU 使用率过高：${CPU_USAGE}%"
        send_alert "CPU 使用率过高：${CPU_USAGE}%"
    else
        log "✅ CPU 使用率：${CPU_USAGE}%"
    fi
    
    # 内存使用率
    MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
    if (( $(echo "$MEMORY_USAGE > $ALERT_THRESHOLD_MEMORY" | bc -l) )); then
        log "❌ 内存使用率过高：${MEMORY_USAGE}%"
        send_alert "内存使用率过高：${MEMORY_USAGE}%"
    else
        log "✅ 内存使用率：${MEMORY_USAGE}%"
    fi
    
    # 磁盘使用率
    DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    if [ "$DISK_USAGE" -gt "$ALERT_THRESHOLD_DISK" ]; then
        log "❌ 磁盘使用率过高：${DISK_USAGE}%"
        send_alert "磁盘使用率过高：${DISK_USAGE}%"
    else
        log "✅ 磁盘使用率：${DISK_USAGE}%"
    fi
}

# 检查 Gateway 状态
check_gateway() {
    log "🤖 检查 Gateway 状态..."
    
    # 检查进程
    if pgrep -f "openclaw-gateway" > /dev/null; then
        PID=$(pgrep -f "openclaw-gateway")
        log "✅ Gateway 进程运行中 (PID: $PID)"
    else
        log "❌ Gateway 进程未运行，尝试重启..."
        systemctl restart openclaw-gateway
        send_alert "Gateway 进程已重启"
    fi
    
    # 检查端口
    if netstat -tln 2>/dev/null | grep -q ":18789"; then
        log "✅ Gateway 端口 18789 正常监听"
    else
        log "❌ Gateway 端口未监听，尝试重启..."
        systemctl restart openclaw-gateway
        send_alert "Gateway 端口已恢复"
    fi
}

# 发送告警
send_alert() {
    local message="$1"
    log "🚨 发送告警：$message"
    # TODO: 实现 Telegram/邮件告警
}

# 主循环
main() {
    log "🛡️ 核心监控系统启动..."
    
    while true; do
        check_system_resources
        check_gateway
        
        # 每 5 分钟检查一次
        sleep 300
    done
}

main
