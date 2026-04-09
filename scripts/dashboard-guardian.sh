#!/bin/bash
# Dashboard Guardian - Dashboard 守护进程
# 功能：自动监控和重启 Dashboard 服务
# 运行：每 5 分钟自动执行 (crontab)

set -e

LOG_DIR="/home/nicola/.openclaw/workspace/logs"
LOG_FILE="$LOG_DIR/dashboard-guardian.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

check_and_restart() {
    local name=$1
    local port=$2
    local start_cmd=$3
    
    if ! curl -s -o /dev/null -w "%{http_code}" http://localhost:$port | grep -q "200"; then
        log "❌ $name (端口$port) 无响应，尝试重启..."
        
        # 清理旧进程
        pkill -f "$name" 2>/dev/null || true
        sleep 2
        
        # 启动新进程
        eval "$start_cmd" &
        sleep 5
        
        # 验证重启
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:$port | grep -q "200"; then
            log "✅ $name 重启成功"
        else
            log "❌ $name 重启失败，需要人工干预"
        fi
    else
        log "✅ $name (端口$port) 运行正常"
    fi
}

# 确保日志目录存在
mkdir -p "$LOG_DIR"

log "========== Dashboard 守护进程检查 =========="

# 检查 Bot Dashboard
check_and_restart "vite" "3000" "cd /home/nicola/.openclaw/workspace/skills/bot-dashboard && npm run dev"

# 检查 ROI Dashboard
check_and_restart "roi_dashboard" "8080" "cd /home/nicola/.openclaw/workspace/skills/roi-tracker && /usr/bin/python3 roi_dashboard.py"

# 检查 Skill Dashboard
check_and_restart "skill-dashboard" "5002" "cd /home/nicola/.openclaw/workspace/skills/skill-dashboard && /usr/bin/python3 app.py"

log "========== 检查完成 =========="
log ""
