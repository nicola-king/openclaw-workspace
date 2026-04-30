#!/bin/bash
# 小红书智能自进化系统 - 每日自动化脚本
# 用途：定时执行每日工作流，自动创作笔记

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
PROJECT_DIR="$WORKSPACE/projects/xiaohongshu-agent"
LOG_DIR="$PROJECT_DIR/logs"
OUTPUT_DIR="$PROJECT_DIR/output"

mkdir -p $LOG_DIR
mkdir -p $OUTPUT_DIR

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_DIR/daily_automation.log
}

log "=== 小红书智能自进化系统 · 每日自动化 ==="
log "工作目录：$PROJECT_DIR"

# 执行每日工作流
cd $PROJECT_DIR

log "🚀 启动总 Agent 协调器..."
python3 src/master_agent.py 2>&1 | tee -a $LOG_DIR/master_agent.log

# 检查执行结果
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    log "✅ 每日自动化完成"
    
    # 生成今日文件列表
    TODAY=$(date +%Y%m%d)
    log "📄 今日输出文件:"
    ls -la $OUTPUT_DIR/*$TODAY*.md 2>/dev/null | tee -a $LOG_DIR/file_list.log || log "⚠️ 未找到今日文件"
    
    # 发送完成通知
    log "📤 发送完成通知..."
    $WORKSPACE/scripts/send-cron-notification.sh "小红书 Agent 每日自动化完成" "✅ 今日创作完成，请查看 output 目录" &
else
    log "❌ 每日自动化失败"
    exit 1
fi

log "=== 自动化完成 ==="
