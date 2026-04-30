#!/bin/bash
# Clash 自检自愈脚本 v2.0 - 智能抑制版
# 功能：智能检查 Clash 状态，避免频繁告警和重启
# 作者：太一 AGI
# 创建：2026-04-22 01:15
# 优化：告警抑制 + 自愈冷却 + 智能检查

set -e

# ============================================
# 配置
# ============================================
CLASH_PORT=7890
CLASH_CONTROLLER=9090
CLASH_PATH="/home/nicola/clash/clash"
CLASH_CONFIG="/home/nicola/clash"
LOG_FILE="/tmp/clash-watchdog.log"
STATE_FILE="/tmp/clash-watchdog-state.json"
TELEGRAM_BOT_TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID="7073481596"

# 智能抑制配置
MAX_FAILURES_BEFORE_ALERT=3      # 连续失败 3 次才告警
SELF_HEAL_COOLDOWN=3600          # 自愈冷却时间 (秒) = 1 小时
CHECK_INTERVAL=900               # 检查间隔 (秒) = 15 分钟

# ============================================
# 工具函数
# ============================================

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Telegram 通知 (使用系统代理)
send_telegram() {
    local message="$1"
    local use_proxy="${2:-true}"
    
    if [ "$use_proxy" = true ]; then
        curl -s -x http://127.0.0.1:$CLASH_PORT \
            "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -H "Content-Type: application/json" \
            -d "{\"chat_id\":\"${TELEGRAM_CHAT_ID}\",\"text\":\"${message}\",\"parse_mode\":\"HTML\"}" > /dev/null 2>&1
    else
        # 直连 (Clash 故障时使用)
        curl -s \
            "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -H "Content-Type: application/json" \
            -d "{\"chat_id\":\"${TELEGRAM_CHAT_ID}\",\"text\":\"${message}\",\"parse_mode\":\"HTML\"}" > /dev/null 2>&1
    fi
}

# 读取状态
get_state() {
    local key="$1"
    if [ -f "$STATE_FILE" ]; then
        jq -r ".$key // 0" "$STATE_FILE" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# 保存状态
set_state() {
    local key="$1"
    local value="$2"
    
    # 创建或更新状态文件
    if [ -f "$STATE_FILE" ]; then
        jq --arg key "$key" --argjson val "$value" '.[$key] = $val' "$STATE_FILE" > /tmp/state.json && mv /tmp/state.json "$STATE_FILE"
    else
        echo "{\"$key\":$value}" > "$STATE_FILE"
    fi
}

# 重置失败计数
reset_failure_count() {
    set_state "consecutive_failures" 0
    set_state "last_success_time" $(date +%s)
}

# 增加失败计数
increment_failure_count() {
    local current=$(get_state "consecutive_failures")
    set_state "consecutive_failures" $((current + 1))
}

# ============================================
# 检查函数 (只检查核心项)
# ============================================

# 检查 Clash 进程 (核心检查)
check_process() {
    if pgrep -f "clash -d $CLASH_CONFIG" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# 检查端口监听 (核心检查)
check_port() {
    if ss -tlnp 2>/dev/null | grep -q ":$CLASH_PORT "; then
        return 0
    else
        return 1
    fi
}

# 检查 API 可访问性 (可选检查)
check_api() {
    local response=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$CLASH_CONTROLLER/proxies" 2>/dev/null || echo "000")
    if [ "$response" = "200" ] || [ "$response" = "401" ]; then
        return 0
    else
        return 1
    fi
}

# 不再检查代理连通性 (避免误报)
# check_proxy() 已移除

# ============================================
# 自愈函数
# ============================================

# 检查是否在冷却期
check_cooldown() {
    local last_heal=$(get_state "last_self_heal_time")
    local now=$(date +%s)
    local elapsed=$((now - last_heal))
    
    if [ $elapsed -lt $SELF_HEAL_COOLDOWN ]; then
        local remaining=$((SELF_HEAL_COOLDOWN - elapsed))
        log "ℹ️  自愈冷却中 (剩余 ${remaining}秒)"
        return 0  # 在冷却期
    else
        return 1  # 不在冷却期
    fi
}

# 重启 Clash
restart_clash() {
    log "🔄 重启 Clash..."
    
    # 尝试 systemd 重启
    if systemctl --user restart clash.service 2>/dev/null; then
        log "✅ systemd 重启成功"
        sleep 5
        set_state "last_self_heal_time" $(date +%s)
        return 0
    fi
    
    # 备用方案：直接启动
    log "⚠️  systemd 失败，尝试直接启动..."
    pkill -f "clash -d $CLASH_CONFIG" 2>/dev/null || true
    sleep 2
    nohup $CLASH_PATH -d $CLASH_CONFIG > /tmp/clash.log 2>&1 &
    sleep 5
    
    if check_process; then
        log "✅ 直接启动成功"
        set_state "last_self_heal_time" $(date +%s)
        return 0
    else
        log "❌ 启动失败"
        return 1
    fi
}

# ============================================
# 主检查流程
# ============================================

main() {
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "🔍 Clash 智能自检开始 (v2.0)"
    
    # 只检查核心项 (进程 + 端口)
    local core_issues=0
    
    # 检查 1: 进程 (核心)
    if check_process; then
        log "✅ 进程正常"
    else
        log "❌ 进程异常"
        core_issues=$((core_issues + 1))
    fi
    
    # 检查 2: 端口 (核心)
    if check_port; then
        log "✅ 端口 $CLASH_PORT 监听正常"
    else
        log "❌ 端口 $CLASH_PORT 未监听"
        core_issues=$((core_issues + 1))
    fi
    
    # 检查 3: API (可选，仅记录)
    if check_api; then
        log "✅ Controller API 正常"
    else
        log "ℹ️  Controller API 异常 (不触发告警)"
    fi
    
    # 判断是否需要处理
    if [ $core_issues -gt 0 ]; then
        log "⚠️  核心问题数：$core_issues"
        
        # 增加失败计数
        increment_failure_count
        local failures=$(get_state "consecutive_failures")
        log "📊 连续失败次数：$failures / $MAX_FAILURES_BEFORE_ALERT"
        
        # 判断是否达到告警阈值
        if [ $failures -ge $MAX_FAILURES_BEFORE_ALERT ]; then
            log "🚨 达到告警阈值，开始自愈..."
            
            # 检查冷却期
            if check_cooldown; then
                log "ℹ️  在冷却期内，仅发送告警，不自愈"
                send_telegram false "⚠️ <b>Clash 异常告警</b>%0A%0A📋 问题：核心检查失败 (连续$failures 次)%0A⏰ 时间：$(date '+%Y-%m-%d %H:%M:%S')%0Aℹ️  状态：冷却期内，1 小时后自动自愈"
            else
                # 发送告警
                send_telegram false "⚠️ <b>Clash 异常告警</b>%0A%0A📋 问题：核心检查失败 (连续$failures 次)%0A🔧 状态：正在自愈...%0A⏰ 时间：$(date '+%Y-%m-%d %H:%M:%S')"
                
                # 执行自愈
                if restart_clash; then
                    log "✅ 自愈成功"
                    reset_failure_count
                    send_telegram false "✅ <b>Clash 自愈成功</b>%0A%0A📋 问题：核心检查失败%0A⏰ 时间：$(date '+%Y-%m-%d %H:%M:%S')%0A🟢 状态：已恢复%0Aℹ️  下次自愈冷却：1 小时"
                else
                    log "❌ 自愈失败"
                    send_telegram false "❌ <b>Clash 自愈失败</b>%0A%0A📋 问题：核心检查失败%0A⚠️ 状态：需要人工干预%0A⏰ 时间：$(date '+%Y-%m-%d %H:%M:%S')"
                fi
            fi
        else
            log "ℹ️  未达到告警阈值，继续观察..."
        fi
    else
        log "✅ 所有核心检查通过"
        reset_failure_count
    fi
    
    log "🔍 自检完成"
    log ""
}

# 执行
main
