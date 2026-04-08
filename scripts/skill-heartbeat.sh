#!/bin/bash
# Skills 心跳自检脚本
# 功能：每个 Skills 定期报告存活状态

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
HEARTBEAT_DIR="/tmp/skill-heartbeats"
LOG_FILE="$WORKSPACE/logs/skill-heartbeat.log"

mkdir -p "$HEARTBEAT_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Skills 心跳报告
send_heartbeat() {
    local skill_name=$1
    local skill_path=$2
    local frequency=$3  # 5m, 15m, 30m
    
    local heartbeat_file="$HEARTBEAT_DIR/${skill_name}.json"
    local timestamp=$(date -Iseconds)
    
    # 检查 Skills 状态
    local status="alive"
    local scripts_count=0
    local cron_status="unknown"
    
    if [ -d "$skill_path" ]; then
        scripts_count=$(find "$skill_path" -name "*.sh" -o -name "*.py" 2>/dev/null | wc -l)
        
        # 检查 Cron 状态
        if crontab -l 2>/dev/null | grep -q "$skill_name"; then
            cron_status="active"
        else
            cron_status="inactive"
        fi
    else
        status="missing"
    fi
    
    # 生成心跳报告
    cat > "$heartbeat_file" << EOF
{
  "skill": "$skill_name",
  "path": "$skill_path",
  "status": "$status",
  "timestamp": "$timestamp",
  "frequency": "$frequency",
  "scripts_count": $scripts_count,
  "cron_status": "$cron_status"
}
EOF
    
    log "💓 $skill_name: $status (scripts: $scripts_count, cron: $cron_status)"
}

# 主流程
log "=== Skills 心跳自检开始 ==="

# P0 核心 Skills (每 5 分钟)
send_heartbeat "polymarket" "$WORKSPACE/skills/polymarket" "5m"
send_heartbeat "gmgn-swap" "$WORKSPACE/skills/gmgn-swap" "5m"
send_heartbeat "gmgn-market" "$WORKSPACE/skills/gmgn-market" "5m"
send_heartbeat "weather-forecast" "$WORKSPACE/skills/suwen" "5m"

# P1 重要 Skills (每 15 分钟)
send_heartbeat "wangliang" "$WORKSPACE/skills/wangliang" "15m"
send_heartbeat "shanmu" "$WORKSPACE/skills/shanmu" "15m"
send_heartbeat "suwen" "$WORKSPACE/skills/suwen" "15m"

# P2 常规 Skills (每 30 分钟)
send_heartbeat "task-orchestrator" "$WORKSPACE/skills/task-orchestrator" "30m"
send_heartbeat "taiyi" "$WORKSPACE/skills/taiyi" "30m"

log "=== 心跳自检完成 ==="
log ""
