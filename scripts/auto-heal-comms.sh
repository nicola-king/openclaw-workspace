#!/bin/bash
# OpenClaw 通讯自动自愈脚本
# 功能：检测并自动修复 Telegram/微信/飞书通讯问题

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/auto-heal-comms.log"
STATE_FILE="$WORKSPACE/memory/heal-state.json"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ==================== 状态检查 ====================

check_gateway() {
    log "🔍 检查 Gateway 状态..."
    if curl -s http://127.0.0.1:18789/health | grep -q '"ok":true'; then
        log "✅ Gateway 正常"
        return 0
    else
        log "❌ Gateway 异常，尝试重启..."
        openclaw gateway restart
        sleep 5
        if curl -s http://127.0.0.1:18789/health | grep -q '"ok":true'; then
            log "✅ Gateway 重启成功"
            return 0
        else
            log "❌ Gateway 重启失败"
            return 1
        fi
    fi
}

check_telegram() {
    log "🔍 检查 Telegram Bot 状态..."
    local bots=(
        "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY:太一"
        "8563369264:AAHeycXPlUQic41mOu4yCyaDcNQAKxYr61E:知几"
        "8731213565:AAHzAnm8lUG2riIuhHyYrxYrzixZ0zibcxo:山木"
        "8632190716:AAFR9k4811ISyQ4tTbn99G9GmtMNsgdkL6w:素问"
        "8635135614:AAEnppb2absodyReJDX-qZAoERP29YFuh1c:罔两"
        "8610739795:AAGvKpqunuyBZlB4sgZwrsly4j1LVMJa728:庖丁"
    )
    
    local failed=0
    for bot_info in "${bots[@]}"; do
        IFS=':' read -r bot_id token name <<< "$bot_info"
        # 重新组合 token（因为名字中可能有冒号）
        token="${token}:${name}"
        token="${token%:*}"  # 移除名字部分
        
        response=$(curl -s "https://api.telegram.org/bot${bot_id}:${token}/getMe")
        if echo "$response" | grep -q '"ok":true'; then
            log "✅ Telegram Bot $name 正常"
        else
            log "❌ Telegram Bot $name 异常"
            ((failed++))
        fi
    done
    
    return $failed
}

check_weixin() {
    log "🔍 检查微信账号状态..."
    
    # 检查 accounts.json
    if [ ! -f "/home/nicola/.openclaw/openclaw-weixin/accounts.json" ]; then
        log "❌ 微信 accounts.json 不存在"
        return 1
    fi
    
    # 检查 token 文件
    local token_count=$(ls /home/nicola/.openclaw/openclaw-weixin/accounts/*.json 2>/dev/null | grep -v ".sync.json" | wc -l)
    if [ "$token_count" -gt 0 ]; then
        log "✅ 微信账号正常 ($token_count 个)"
        
        # 检查 session 是否过期
        if tail -100 /tmp/openclaw/openclaw-*.log 2>/dev/null | grep -q "session expired.*errcode -14"; then
            log "⚠️ 检测到微信 session 过期，尝试清理..."
            bash /home/nicola/.openclaw/workspace/scripts/weixin-cleanup.sh
            return 0
        fi
        return 0
    else
        log "❌ 微信账号未登录"
        return 1
    fi
}

check_feishu() {
    log "🔍 检查飞书状态..."
    
    # 检查 openclaw status 输出
    if openclaw status 2>&1 | grep -q "Feishu.*OK"; then
        log "✅ 飞书正常"
        return 0
    else
        log "⚠️ 飞书状态异常"
        return 1
    fi
}

# ==================== 自愈操作 ====================

heal_telegram() {
    log "🔧 尝试修复 Telegram..."
    # Telegram 通常不需要特殊修复，重启 gateway 即可
    openclaw gateway restart
    sleep 3
    check_telegram
}

heal_weixin() {
    log "🔧 尝试修复微信..."
    # 1. 清理过期 token
    bash /home/nicola/.openclaw/workspace/scripts/weixin-cleanup.sh
    
    # 2. 重启 gateway
    openclaw gateway restart
    sleep 3
    
    # 3. 重新检查
    check_weixin
}

heal_gateway() {
    log "🔧 尝试修复 Gateway..."
    
    # 尝试重启
    openclaw gateway restart
    sleep 5
    
    # 检查是否成功
    if curl -s http://127.0.0.1:18789/health | grep -q '"ok":true'; then
        log "✅ Gateway 修复成功"
        return 0
    else
        log "❌ Gateway 修复失败，尝试 systemd 重启..."
        systemctl --user restart openclaw-gateway.service
        sleep 5
        return 0
    fi
}

# ==================== 主流程 ====================

main() {
    log "=========================================="
    log "🚑 OpenClaw 通讯自动自愈开始"
    log "=========================================="
    
    local issues=0
    local healed=0
    
    # 检查 Gateway
    if ! check_gateway; then
        ((issues++))
        if heal_gateway; then
            ((healed++))
        fi
    fi
    
    # 检查 Telegram
    if ! check_telegram; then
        ((issues++))
        if heal_telegram; then
            ((healed++))
        fi
    fi
    
    # 检查微信
    if ! check_weixin; then
        ((issues++))
        if heal_weixin; then
            ((healed++))
        fi
    fi
    
    # 检查飞书
    if ! check_feishu; then
        ((issues++))
        log "⚠️ 飞书问题需手动检查"
    fi
    
    # 总结
    log "=========================================="
    log "📊 自愈结果汇总"
    log "=========================================="
    log "发现问题：$issues 个"
    log "成功修复：$healed 个"
    
    if [ $issues -eq 0 ]; then
        log "✅ 所有通讯正常"
    elif [ $issues -eq $healed ]; then
        log "✅ 所有问题已修复"
    else
        log "⚠️ 仍有 $(($issues - $healed)) 个问题需手动处理"
    fi
    
    # 更新状态文件
    cat > "$STATE_FILE" << EOF
{
  "lastCheck": "$(date -Iseconds)",
  "issuesFound": $issues,
  "issuesHealed": $healed,
  "status": "$([ $issues -eq 0 ] && echo 'ok' || echo 'partial')"
}
EOF
    
    log "状态已写入：$STATE_FILE"
    log "=========================================="
}

main "$@"
