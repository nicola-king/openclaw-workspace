#!/bin/bash
# ============================================================
# 每日新闻搜索 - Cron 触发脚本
# 功能：北京时间 08:00 触发新闻搜索任务
# 作者：太一 AGI
# 创建：2026-04-19
# ============================================================

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="${WORKSPACE}/logs/news"
LOG_FILE="${LOG_DIR}/晨间新闻 -$(date +%Y-%m-%d).log"  # 中文日志名

# 创建日志目录
mkdir -p "${LOG_DIR}"

# 记录开始
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始执行每日新闻搜索..." >> "${LOG_FILE}"

# 方法 1: 通过 OpenClaw sessions_spawn 触发（推荐）
# 这会启动一个子代理来执行搜索任务
openclaw sessions_spawn \
    --task "执行每日新闻搜索任务，搜索 7 类新闻（AI/前沿科技/国际时事/国际热点/国际经济/产品趋势/中国政经），每类 5 条，输出到 news/daily/晨间新闻简报-YYYY-MM-DD.md，然后执行冰山理论分析选择 5 条重要新闻深度分析" \
    --label "daily-news-$(date +%Y%m%d)" \
    --mode "run" \
    --runtime "subagent" \
    >> "${LOG_FILE}" 2>&1

# 方法 2: 直接执行 Python 脚本（备用）
# python3 "${WORKSPACE}/scripts/daily-news-search.py"
# python3 "${WORKSPACE}/scripts/iceberg-news-analyzer.py"

# 记录完成
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 新闻搜索任务已提交" >> "${LOG_FILE}"

# 可选：发送通知
# openclaw send-message --channel telegram --text "🌅 晨间新闻搜索已启动，预计 5-10 分钟完成"

exit 0
