#!/bin/bash
# 全域自进化系统定时自检脚本

LOG_FILE="/home/nicola/.openclaw/workspace/logs/self_evolving_system_check.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "🧬 开始全域自进化系统定时自检"

cd /home/nicola/.openclaw/workspace
python3 skills/07-system/self_evolving_system_check.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ 全域自进化系统自检完成"
else
    log "❌ 全域自进化系统自检失败"
fi

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
