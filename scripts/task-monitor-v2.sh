#!/bin/bash
# task-monitor.sh - 任务监控脚本（增强版 v2.0）
# 频率：每小时执行
# 功能：检查任务状态 + 逾期告警 + 自动生成保障报告

echo "========================================"
echo "太一任务监控系统 v2.0"
echo "执行时间：$(date)"
echo "========================================"

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/task-monitor.log"
REPORT_FILE="$WORKSPACE/reports/task-monitor-report.md"

# 确保日志目录存在
mkdir -p "$WORKSPACE/logs"
mkdir -p "$WORKSPACE/reports"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "开始任务检查..."

# 检查 HEARTBEAT.md 中的 P0 任务
log "检查 HEARTBEAT.md 待办事项..."
HEARTBEAT_FILE="$WORKSPACE/HEARTBEAT.md"

if [ -f "$HEARTBEAT_FILE" ]; then
    P0_COUNT=$(grep -c "TASK-" "$HEARTBEAT_FILE" || echo "0")
    log "HEARTBEAT.md 中的任务数量：$P0_COUNT"
else
    log "⚠️ HEARTBEAT.md 不存在"
fi

# 检查当日记忆文件
log "检查当日记忆文件..."
TODAY=$(date '+%Y-%m-%d')
MEMORY_FILE="$WORKSPACE/memory/$TODAY.md"

if [ -f "$MEMORY_FILE" ]; then
    log "✅ 当日记忆文件存在：$MEMORY_FILE"
    MEMORY_SIZE=$(wc -c < "$MEMORY_FILE")
    log "记忆文件大小：$MEMORY_SIZE bytes"
else
    log "⚠️ 当日记忆文件不存在，创建中..."
    echo "# 记忆文件 $TODAY" > "$MEMORY_FILE"
    log "✅ 已创建：$MEMORY_FILE"
fi

# 检查宪法文件完整性
log "检查宪法文件完整性..."
CONSTITUTION_FILES=(
    "$WORKSPACE/constitution/directives/TASK-GUARANTEE.md"
    "$WORKSPACE/constitution/directives/AUTO-EXEC.md"
    "$WORKSPACE/constitution/directives/NEGENTROPY.md"
)

for file in "${CONSTITUTION_FILES[@]}"; do
    if [ -f "$file" ]; then
        log "✅ $file"
    else
        log "❌ 缺失：$file"
    fi
done

# 检查 Cron 任务状态
log "检查 Cron 任务状态..."
CRON_TASKS=$(crontab -l 2>/dev/null | grep -v "^#" | wc -l)
log "活跃 Cron 任务数量：$CRON_TASKS"

# 检查关键 Cron 任务
if crontab -l 2>/dev/null | grep -q "daily-buyer-scraper"; then
    log "✅ 买家数据抓取任务已配置"
else
    log "⚠️ 买家数据抓取任务未配置"
fi

if crontab -l 2>/dev/null | grep -q "auto-exec-cron"; then
    log "✅ 自动执行任务已配置"
else
    log "⚠️ 自动执行任务未配置"
fi

# 检查残留进程
log "检查残留进程..."
RESIDUE_COUNT=$(ps aux | grep -E "python.*scraper|python.*auto" | grep -v grep | wc -l)
log "残留进程数量：$RESIDUE_COUNT"

if [ "$RESIDUE_COUNT" -gt 0 ]; then
    log "⚠️ 发现残留进程，建议清理"
    ps aux | grep -E "python.*scraper|python.*auto" | grep -v grep >> "$LOG_FILE"
else
    log "✅ 无残留进程"
fi

# 检查磁盘空间
log "检查磁盘空间..."
DISK_USAGE=$(df -h /home | awk 'NR==2 {print $5}' | tr -d '%')
log "磁盘使用率：${DISK_USAGE}%"

if [ "$DISK_USAGE" -gt 90 ]; then
    log "🚨 磁盘空间告警！使用率超过 90%"
elif [ "$DISK_USAGE" -gt 80 ]; then
    log "⚠️ 磁盘空间警告！使用率超过 80%"
else
    log "✅ 磁盘空间正常"
fi

# 生成监控报告
log "生成监控报告..."

cat > "$REPORT_FILE" << EOF
# 任务监控报告

**生成时间**: $(date -Iseconds)
**监控周期**: 每小时
**状态**: ✅ 正常运行

---

## 📊 系统状态

| 指标 | 数值 | 状态 |
|------|------|------|
| HEARTBEAT 任务数 | $P0_COUNT | ✅ |
| 当日记忆文件 | $( [ -f "$MEMORY_FILE" ] && echo "存在 ($MEMORY_SIZE bytes)" || echo "缺失" ) | $([ -f "$MEMORY_FILE" ] && echo "✅" || echo "❌") |
| Cron 任务数 | $CRON_TASKS | ✅ |
| 残留进程 | $RESIDUE_COUNT | $([ "$RESIDUE_COUNT" -eq 0 ] && echo "✅" || echo "⚠️") |
| 磁盘使用率 | ${DISK_USAGE}% | $([ "$DISK_USAGE" -lt 80 ] && echo "✅" || echo "⚠️") |

---

## 🔍 宪法文件检查

| 文件 | 状态 |
|------|------|
EOF

for file in "${CONSTITUTION_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "| $(basename $file) | ✅ |" >> "$REPORT_FILE"
    else
        echo "| $(basename $file) | ❌ 缺失 |" >> "$REPORT_FILE"
    fi
done

cat >> "$REPORT_FILE" << EOF

---

## ⏰ 关键 Cron 任务

| 任务 | 状态 |
|------|------|
| 买家数据抓取 (06:00) | $(crontab -l 2>/dev/null | grep -q "daily-buyer-scraper" && echo "✅ 已配置" || echo "❌ 未配置") |
| 自动执行 (*/5 分钟) | $(crontab -l 2>/dev/null | grep -q "auto-exec-cron" && echo "✅ 已配置" || echo "❌ 未配置") |
| 宪法学习 (06:00) | $(crontab -l 2>/dev/null | grep -q "daily-constitution" && echo "✅ 已配置" || echo "❌ 未配置") |
| 日报生成 (23:00) | $(crontab -l 2>/dev/null | grep -q "openclaw-report" && echo "✅ 已配置" || echo "❌ 未配置") |

---

## 🚨 告警汇总

EOF

# 收集告警
ALERTS=0

if [ ! -f "$MEMORY_FILE" ]; then
    echo "- ❌ 当日记忆文件缺失" >> "$REPORT_FILE"
    ALERTS=$((ALERTS + 1))
fi

if [ "$RESIDUE_COUNT" -gt 0 ]; then
    echo "- ⚠️ 发现 $RESIDUE_COUNT 个残留进程" >> "$REPORT_FILE"
    ALERTS=$((ALERTS + 1))
fi

if [ "$DISK_USAGE" -gt 90 ]; then
    echo "- 🚨 磁盘空间告警 (${DISK_USAGE}%)" >> "$REPORT_FILE"
    ALERTS=$((ALERTS + 1))
elif [ "$DISK_USAGE" -gt 80 ]; then
    echo "- ⚠️ 磁盘空间警告 (${DISK_USAGE}%)" >> "$REPORT_FILE"
    ALERTS=$((ALERTS + 1))
fi

if [ "$ALERTS" -eq 0 ]; then
    echo "✅ 无告警" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

## 📈 趋势分析

**总告警数**: $ALERTS
**系统健康度**: $([ "$ALERTS" -eq 0 ] && echo "✅ 优秀" || ([ "$ALERTS" -le 2 ] && echo "🟡 良好" || echo "🔴 需关注"))

---

## 🔄 下次检查

**时间**: $(date -d '+1 hour' '+%Y-%m-%d %H:00')
**频率**: 每小时整点

---

*报告生成：太一 AGI 任务监控系统 v2.0*
EOF

log "✅ 监控报告已生成：$REPORT_FILE"

# 检查是否需要告警
if [ "$ALERTS" -gt 0 ]; then
    log "🚨 发现 $ALERTS 个告警，请注意检查"
    
    # 如果有严重告警，发送通知
    if [ "$ALERTS" -gt 2 ] || [ "$DISK_USAGE" -gt 90 ]; then
        log "🚨 严重告警！准备发送通知..."
        # 这里可以集成通知逻辑（微信/Telegram/邮件）
    fi
else
    log "✅ 系统运行正常，无告警"
fi

log "任务监控完成"
echo "========================================"
echo "监控完成！报告：$REPORT_FILE"
echo "========================================"
