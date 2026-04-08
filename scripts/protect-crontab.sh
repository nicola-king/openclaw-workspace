#!/bin/bash
# Crontab 保护脚本 - 禁止自动注释，强制审批

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
PROTECTION_LOG="$WORKSPACE/logs/crontab-protection.log"
BACKUP_DIR="$WORKSPACE/backups/crontab"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$PROTECTION_LOG"
}

# === 步骤 1: 备份当前 crontab ===
log "=== Crontab 保护检查开始 ==="
BACKUP_FILE="$BACKUP_DIR/crontab-$(date +%Y%m%d-%H%M%S).txt"
crontab -l > "$BACKUP_FILE" 2>/dev/null || true
log "✅ 备份完成：$BACKUP_FILE"

# === 步骤 2: 统计注释行 ===
TOTAL_LINES=$(crontab -l 2>/dev/null | wc -l)
COMMENT_LINES=$(crontab -l 2>/dev/null | grep -c "^#" || echo "0")
DISABLED_TASKS=$(crontab -l 2>/dev/null | grep -E "^#.*[0-9]+\s+[*0-9]" | wc -l || echo "0")

log "📊 统计信息:"
log "  - 总行数：$TOTAL_LINES"
log "  - 注释行：$COMMENT_LINES"
log "  - 疑似禁用任务：$DISABLED_TASKS"

# === 步骤 3: 检测新增注释 ===
if [ -f "$WORKSPACE/logs/crontab-last-check.txt" ]; then
    LAST_DISABLED=$(cat "$WORKSPACE/logs/crontab-last-check.txt")
    if [ "$DISABLED_TASKS" -gt "$LAST_DISABLED" ]; then
        log "🚨 警告：发现新增禁用任务！(上次：$LAST_DISABLED, 本次：$DISABLED_TASKS)"
        
        # 生成差异报告
        DIFF_FILE="$BACKUP_DIR/diff-$(date +%Y%m%d-%H%M%S).txt"
        crontab -l > "$BACKUP_DIR/current.txt"
        diff -u "$WORKSPACE/logs/crontab-last.txt" "$BACKUP_DIR/current.txt" > "$DIFF_FILE" || true
        
        log "📝 差异报告：$DIFF_FILE"
        log "🚨 立即上报太一..."
        
        # 生成告警文件
        ALERT_FILE="$WORKSPACE/reports/crontab-change-alert-$(date +%Y%m%d-%H%M).md"
        cat > "$ALERT_FILE" << EOF
# 🚨 Crontab 变更告警

> **检测时间**: $(date '+%Y-%m-%d %H:%M') | **负责 Bot**: 太一

## 告警内容

**发现新增禁用任务**: $DISABLED_TASKS 个 (上次：$LAST_DISABLED)

## 详细信息

- **备份文件**: $BACKUP_FILE
- **差异报告**: $DIFF_FILE
- **注释行总数**: $COMMENT_LINES / $TOTAL_LINES

## 疑似禁用任务

\`\`\`bash
$(crontab -l 2>/dev/null | grep -E "^#.*[0-9]+\s+[*0-9]")
\`\`\`

## 处理建议

1. **立即审查**: 确认为何被禁用
2. **联系责任人**: 询问禁用原因
3. **恢复任务**: 如无正当理由，立即恢复
4. **记录原因**: 如确需禁用，走审批流程

## 审批流程

根据 \`constitution/directives/CRON-PROTECTION.md\`:
- 禁用任务必须经过太一审批
- 必须标注原因和恢复时间
- 超期自动恢复

---
*自动生成 | Crontab 保护机制 v1.0*
EOF
        
        log "✅ 告警报告已生成：$ALERT_FILE"
    fi
fi

# === 步骤 4: 保存当前状态 ===
echo "$DISABLED_TASKS" > "$WORKSPACE/logs/crontab-last-check.txt"
crontab -l > "$WORKSPACE/logs/crontab-last.txt" 2>/dev/null || true

# === 步骤 5: 检查无原因注释 ===
log "🔍 检查无原因注释..."
NO_REASON=$(crontab -l 2>/dev/null | grep -E "^#\s+[0-9]+\s+[*0-9]" | grep -v "\[临时禁用\]" | grep -v "\[已审批\]" | wc -l || echo "0")

if [ "$NO_REASON" -gt 0 ]; then
    log "⚠️  发现 $NO_REASON 个无审批标记的禁用任务"
    log "📝 违规任务列表:"
    crontab -l 2>/dev/null | grep -E "^#\s+[0-9]+\s+[*0-9]" | grep -v "\[临时禁用\]" | grep -v "\[已审批\]" | while read line; do
        log "  - $line"
    done
fi

# === 步骤 6: 验证关键任务 ===
log "🔍 验证关键任务状态..."

CRITICAL_TASKS=(
    "weather-forecast.sh"
    "polymarket-hot-weather-cron.sh"
    "daily-constitution.sh"
    "auto-exec-cron.sh"
)

for task in "${CRITICAL_TASKS[@]}"; do
    if crontab -l 2>/dev/null | grep -q "^#.*$task"; then
        log "🚨 关键任务被禁用：$task"
    elif crontab -l 2>/dev/null | grep -q "$task"; then
        log "✅ 关键任务正常：$task"
    else
        log "⚠️  关键任务未找到：$task"
    fi
done

log "=== Crontab 保护检查完成 ==="
log ""
