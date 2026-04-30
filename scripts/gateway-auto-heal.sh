#!/bin/bash
# Gateway 自动修复脚本
# 自动检测并修复 Gateway 故障

LOG_FILE="/home/nicola/.openclaw/workspace/logs/gateway-auto-heal.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查并修复 Gateway
check_and_heal() {
    log "🔧 检查 Gateway 状态..."
    
    # 检查进程
    if ! pgrep -f "openclaw-gateway" > /dev/null; then
        log "❌ Gateway 进程未运行"
        
        # 尝试重启
        log "🔄 尝试重启 Gateway..."
        systemctl restart openclaw-gateway
        
        # 等待 10 秒
        sleep 10
        
        # 验证重启成功
        if pgrep -f "openclaw-gateway" > /dev/null; then
            log "✅ Gateway 重启成功"
            send_alert "Gateway 已自动重启"
        else
            log "❌ Gateway 重启失败，需要人工干预"
            send_alert "❌ Gateway 重启失败，需要人工干预"
        fi
    else
        log "✅ Gateway 运行正常"
    fi
    
    # 检查端口
    if ! netstat -tln 2>/dev/null | grep -q ":18789"; then
        log "❌ Gateway 端口未监听"
        
        # 尝试重启
        log "🔄 尝试重启 Gateway..."
        systemctl restart openclaw-gateway
        
        # 等待 10 秒
        sleep 10
        
        # 验证重启成功
        if netstat -tln 2>/dev/null | grep -q ":18789"; then
            log "✅ Gateway 端口已恢复"
            send_alert "Gateway 端口已自动恢复"
        else
            log "❌ Gateway 端口恢复失败，需要人工干预"
            send_alert "❌ Gateway 端口恢复失败，需要人工干预"
        fi
    else
        log "✅ Gateway 端口正常监听"
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
    log "🛡️ Gateway 自动修复脚本启动..."
    
    while true; do
        check_and_heal
        sleep 60  # 每分钟检查一次
    done
}

main
