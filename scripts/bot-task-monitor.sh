#!/bin/bash
# Bot 任务监控脚本 - 太一 AGI v5.0
# 监控各 Bot 任务执行进度，自动汇总汇报

set -e

AGENTS_DIR="$HOME/.openclaw/agents"
WORKSPACE="/home/nicola/.openclaw/workspace"
REPORTS_DIR="$WORKSPACE/reports"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[监控]${NC} $1"; }
log_success() { echo -e "${GREEN}[完成]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[警告]${NC} $1"; }
log_error() { echo -e "${RED}[错误]${NC} $1"; }

# 检查 Bot inbox/outbox
check_bot_status() {
    local bot=$1
    local inbox="$AGENTS_DIR/$bot/inbox"
    local outbox="$AGENTS_DIR/$bot/outbox"
    
    echo "========================================"
    echo "🤖 $bot 状态检查"
    echo "========================================"
    
    # 检查 inbox 任务
    if [ -d "$inbox" ] && [ "$(ls -A $inbox 2>/dev/null)" ]; then
        echo "📬 待处理任务:"
        ls -1 "$inbox" | while read f; do
            echo "  - $f"
        done
    else
        echo "✅ 无待处理任务"
    fi
    
    # 检查 outbox 汇报
    if [ -d "$outbox" ] && [ "$(ls -A $outbox 2>/dev/null)" ]; then
        echo "📤 最新汇报:"
        ls -lt "$outbox" | head -5 | while read line; do
            echo "  $line"
        done
    else
        echo "⏳ 暂无汇报"
    fi
    
    echo ""
}

# 生成汇总报告
generate_summary() {
    local report="$REPORTS_DIR/bot-task-summary-$(date +%Y%m%d-%H%M).md"
    
    cat > "$report" << EOF
# Bot 任务执行汇总报告

> 生成时间：$(date '+%Y-%m-%d %H:%M') | 太一 AGI v5.0

---

## 📊 任务分发状态

| Bot | 任务数 | 状态 | 最新汇报 |
|-----|--------|------|---------|
EOF

    for bot in suwen yi zhiji shoucangli; do
        local inbox_count=$(ls -1 "$AGENTS_DIR/$bot/inbox" 2>/dev/null | wc -l)
        local outbox_count=$(ls -1 "$AGENTS_DIR/$bot/outbox" 2>/dev/null | wc -l)
        local status="🟡 执行中"
        
        if [ "$outbox_count" -gt 0 ]; then
            local latest=$(ls -t "$AGENTS_DIR/$bot/outbox" 2>/dev/null | head -1)
            if [[ "$latest" == *"完成"* ]] || [[ "$latest" == *"DONE"* ]]; then
                status="✅ 已完成"
            fi
        fi
        
        echo "| $bot | $inbox_count | $status | $outbox_count 份 |" >> "$report"
    done

    cat >> "$report" << EOF

---

## 📋 详细状态

EOF

    for bot in suwen yi zhiji shoucangli; do
        echo "### $bot" >> "$report"
        echo "" >> "$report"
        
        # 读取最新汇报
        local latest_report=$(ls -t "$AGENTS_DIR/$bot/outbox" 2>/dev/null | head -1)
        if [ -n "$latest_report" ]; then
            echo "\`\`\`" >> "$report"
            head -20 "$AGENTS_DIR/$bot/outbox/$latest_report" >> "$report"
            echo "\`\`\`" >> "$report"
        else
            echo "*暂无汇报*" >> "$report"
        fi
        echo "" >> "$report"
    done

    echo "✅ 汇总报告已生成：$report"
    echo "$report"
}

# 主函数
main() {
    log_info "开始 Bot 任务监控..."
    echo ""
    
    # 检查各 Bot 状态
    for bot in suwen yi zhiji shoucangli; do
        check_bot_status "$bot"
    done
    
    # 生成汇总报告
    echo ""
    log_info "生成汇总报告..."
    local report=$(generate_summary)
    
    echo ""
    log_success "监控完成！"
    echo "汇总报告：$report"
}

# 如果是直接执行
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi
