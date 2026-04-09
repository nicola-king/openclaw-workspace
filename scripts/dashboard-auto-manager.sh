#!/bin/bash
# Dashboard 自动管理器 - 按需启动 + 10 分钟自动关闭
# 功能：检测访问需求，自动启动/停止 Dashboard
# 运行：每 2 分钟自动检查 (crontab)

set -e

LOG_DIR="/home/nicola/.openclaw/workspace/logs"
LOG_FILE="$LOG_DIR/dashboard-auto-manager.log"
STATE_FILE="$LOG_DIR/dashboard-state.json"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
IDLE_TIMEOUT=600  # 10 分钟空闲自动关闭

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# 初始化状态文件
init_state() {
    if [ ! -f "$STATE_FILE" ]; then
        cat > "$STATE_FILE" << EOF
{
    "bot_dashboard": {"running": false, "last_access": 0},
    "roi_dashboard": {"running": false, "last_access": 0},
    "skill_dashboard": {"running": false, "last_access": 0}
}
EOF
    fi
}

# 检查端口是否有访问
check_port_access() {
    local port=$1
    # 检查最近 10 分钟是否有 HTTP 请求
    local recent_requests=$(netstat -an 2>/dev/null | grep ":$port" | grep ESTABLISHED | wc -l)
    echo $recent_requests
}

# 启动 Dashboard
start_dashboard() {
    local name=$1
    local port=$2
    local cmd=$3
    
    if ! curl -s -o /dev/null -w "%{http_code}" http://localhost:$port | grep -q "200"; then
        log "🚀 启动 $name (端口$port)..."
        eval "$cmd" &
        sleep 5
        
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:$port | grep -q "200"; then
            log "✅ $name 启动成功"
            update_state "$name" "running" "true"
        else
            log "❌ $name 启动失败"
        fi
    fi
}

# 停止 Dashboard
stop_dashboard() {
    local name=$1
    local port=$2
    local pattern=$3
    
    log "🛑 停止 $name (端口$port) - 空闲超时..."
    pkill -f "$pattern" 2>/dev/null || true
    sleep 2
    update_state "$name" "running" "false"
    log "✅ $name 已停止"
}

# 更新状态
update_state() {
    local name=$1
    local key=$2
    local value=$3
    
    # 简化实现：直接更新状态文件
    python3 << PYTHON
import json
from pathlib import Path

state_file = Path("$STATE_FILE")
if state_file.exists():
    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)
    
    name_key = "$name".lower().replace(" ", "_").replace("_dashboard", "")
    if name_key in state:
        state[name_key][key] = value
        if key == "last_access":
            state[name_key][key] = $value
        elif key == "running":
            state[name_key][key] = $value
    
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
PYTHON
}

# 主逻辑
main() {
    log "========== Dashboard 自动管理检查 =========="
    
    init_state
    
    # 检查 Bot Dashboard (3000)
    bot_access=$(check_port_access 3000)
    if [ "$bot_access" -gt 0 ]; then
        start_dashboard "Bot Dashboard" "3000" "cd /home/nicola/.openclaw/workspace/skills/bot-dashboard && npm run dev"
        update_state "bot_dashboard" "last_access" "$(date +%s)"
    fi
    
    # 检查 ROI Dashboard (8080)
    roi_access=$(check_port_access 8080)
    if [ "$roi_access" -gt 0 ]; then
        start_dashboard "ROI Dashboard" "8080" "cd /home/nicola/.openclaw/workspace/skills/roi-tracker && /usr/bin/python3 roi_dashboard.py"
        update_state "roi_dashboard" "last_access" "$(date +%s)"
    fi
    
    # 检查 Skill Dashboard (5002)
    skill_access=$(check_port_access 5002)
    if [ "$skill_access" -gt 0 ]; then
        start_dashboard "Skill Dashboard" "5002" "cd /home/nicola/.openclaw/workspace/skills/skill-dashboard && /usr/bin/python3 app.py"
        update_state "skill_dashboard" "last_access" "$(date +%s)"
    fi
    
    # 检查空闲超时 (10 分钟)
    current_time=$(date +%s)
    
    # 检查 Bot Dashboard 空闲
    bot_last=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['bot_dashboard']['last_access'])" 2>/dev/null || echo "0")
    if [ "$bot_last" -gt 0 ]; then
        idle_time=$((current_time - bot_last))
        if [ "$idle_time" -gt "$IDLE_TIMEOUT" ]; then
            stop_dashboard "Bot Dashboard" "3000" "vite.*3000"
        fi
    fi
    
    # 检查 ROI Dashboard 空闲
    roi_last=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['roi_dashboard']['last_access'])" 2>/dev/null || echo "0")
    if [ "$roi_last" -gt 0 ]; then
        idle_time=$((current_time - roi_last))
        if [ "$idle_time" -gt "$IDLE_TIMEOUT" ]; then
            stop_dashboard "ROI Dashboard" "8080" "roi_dashboard.*8080"
        fi
    fi
    
    # 检查 Skill Dashboard 空闲
    skill_last=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['skill_dashboard']['last_access'])" 2>/dev/null || echo "0")
    if [ "$skill_last" -gt 0 ]; then
        idle_time=$((current_time - skill_last))
        if [ "$idle_time" -gt "$IDLE_TIMEOUT" ]; then
            stop_dashboard "Skill Dashboard" "5002" "app.py.*5002"
        fi
    fi
    
    log "========== 检查完成 =========="
    log ""
}

# 执行
main
