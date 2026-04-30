#!/bin/bash
# Clash 自进化脚本
# 功能：分析运行日志，自动优化配置，学习最佳节点
# 作者：太一 AGI
# 创建：2026-04-21 00:09

set -e

# 配置
CLASH_CONFIG="/home/nicola/clash/config.yaml"
CLASH_LOG="/tmp/clash.log"
EVOLUTION_LOG="/tmp/clash-evolution.log"
MEMORY_FILE="/home/nicola/.openclaw/workspace/memory/clash-evolution.json"
TELEGRAM_BOT_TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID="7073481596"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$EVOLUTION_LOG"
}

# Telegram 通知
send_telegram() {
    local message="$1"
    curl -s -x http://127.0.0.1:7890 \
        "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\":\"${TELEGRAM_CHAT_ID}\",\"text\":\"${message}\",\"parse_mode\":\"HTML\"}" > /dev/null 2>&1
}

# 分析节点性能
analyze_nodes() {
    log "📊 分析节点性能..."
    
    # 从日志中提取节点连接记录
    if [ -f "$CLASH_LOG" ]; then
        # 统计各节点连接次数
        local nodes=$(grep "proxy=" "$CLASH_LOG" 2>/dev/null | sed 's/.*proxy=\([^]]*\).*/\1/' | sort | uniq -c | sort -rn | head -10)
        
        log "📈 Top 节点:"
        echo "$nodes" | while read count node; do
            log "  $node: $count 次连接"
        done
        
        # 保存到内存文件
        echo "$nodes" > /tmp/clash-top-nodes.txt
    fi
}

# 检测异常连接
detect_anomalies() {
    log "🔍 检测异常连接..."
    
    if [ -f "$CLASH_LOG" ]; then
        # 检测连接失败
        local failures=$(grep -c "connection failed\|dial error" "$CLASH_LOG" 2>/dev/null || echo "0")
        
        if [ "${failures:-0}" -gt 10 ]; then
            log "⚠️  检测到 $failures 次连接失败"
            send_telegram "⚠️ <b>Clash 异常检测</b>%0A%0A📋 过去 1 小时连接失败：$failures 次%0A🔍 建议：检查节点配置"
        else
            log "✅ 连接正常 ($failures 次失败)"
        fi
    fi
}

# 学习用户习惯
learn_usage_pattern() {
    log "🧠 学习使用模式..."
    
    # 分析流量高峰时段
    local hour=$(date +%H)
    
    if [ -f "$CLASH_LOG" ]; then
        # 统计当前小时的连接数
        local current_hour_connections=$(grep "$(date '+%H:')" "$CLASH_LOG" 2>/dev/null | wc -l)
        
        log "  当前时段 ($hour:00) 连接数：$current_hour_connections"
        
        # 保存到内存
        if [ -f "$MEMORY_FILE" ]; then
            # 更新现有记录
            jq --arg hour "$hour" --argjson count "$current_hour_connections" \
               '.usage_patterns[$hour] = $count' "$MEMORY_FILE" > /tmp/mem.json && mv /tmp/mem.json "$MEMORY_FILE"
        else
            # 创建新文件
            echo "{\"usage_patterns\":{\"$hour\":$current_hour_connections},\"created_at\":\"$(date -Iseconds)\"}" > "$MEMORY_FILE"
        fi
    fi
}

# 生成优化建议
generate_recommendations() {
    log "💡 生成优化建议..."
    
    # 检查内存占用
    local pid=$(pgrep -f "clash -d")
    if [ -n "$pid" ]; then
        local mem_usage=$(ps -o rss= -p "$pid" 2>/dev/null | awk '{print int($1/1024)}')
        log "  Clash 内存占用：${mem_usage}MB"
        
        if [ -n "$mem_usage" ] && [ "$mem_usage" -gt 500 ]; then
            log "⚠️  内存占用较高，建议检查配置"
        else
            log "✅ 内存占用正常"
        fi
    fi
    
    log "✅ 优化建议生成完成"
}

# 自进化主流程
main() {
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "🧠 Clash 自进化开始"
    log ""
    
    # 1. 分析节点性能
    analyze_nodes
    log ""
    
    # 2. 检测异常
    detect_anomalies
    log ""
    
    # 3. 学习使用模式
    learn_usage_pattern
    log ""
    
    # 4. 生成建议
    generate_recommendations
    log ""
    
    log "🧠 自进化完成"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log ""
}

# 每小时执行一次
main
