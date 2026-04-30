#!/bin/bash
# ============================================================
# 突发新闻触发脚本
# 功能：手动或自动触发突发新闻搜索和推送
# 作者：太一 AGI
# 创建：2026-04-19
# ============================================================

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="${WORKSPACE}/logs/breaking-news"
LOG_FILE="${LOG_DIR}/突发新闻 -$(date +%Y-%m-%d).log"

# 创建日志目录
mkdir -p "${LOG_DIR}"

# 记录开始
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 突发新闻触发..." >> "${LOG_FILE}"

# 参数：新闻标题（可选）
NEWS_TITLE="$1"

if [ -n "$NEWS_TITLE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 手动触发：$NEWS_TITLE" >> "${LOG_FILE}"
    
    # 启动子代理执行搜索
    openclaw sessions_spawn \
        --task "执行突发新闻搜索：$NEWS_TITLE，搜索 AI/时事/热点/经济/中国政经，生成 MD 报告并推送到 Telegram" \
        --label "breaking-news-$(date +%Y%m%d-%H%M)" \
        --mode "run" \
        --runtime "subagent" \
        >> "${LOG_FILE}" 2>&1
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 自动监测模式" >> "${LOG_FILE}"
    
    # 启动监测脚本（后台运行）
    nohup python3 "${WORKSPACE}/scripts/breaking-news-monitor.py" >> "${LOG_FILE}" 2>&1 &
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 监测脚本已启动 (PID: $!)" >> "${LOG_FILE}"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 突发新闻触发完成" >> "${LOG_FILE}"

exit 0
