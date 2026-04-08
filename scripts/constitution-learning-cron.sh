#!/bin/bash
# 宪法学习定时任务 - 每日 06:00 自动执行
# 功能：宪法学习 + 记忆提炼 + 系统自检 + 新一天重置

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="/home/nicola/.openclaw/logs/constitution-learning.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "========== 宪法学习开始 =========="

# 1. 宪法文件学习
log "📖 宪法学习..."
CORE_FILES=(
    "$WORKSPACE/constitution/CONST-ROUTER.md"
    "$WORKSPACE/constitution/axiom/VALUE-FOUNDATION.md"
    "$WORKSPACE/constitution/directives/NEGENTROPY.md"
    "$WORKSPACE/constitution/directives/TURBOQUANT.md"
    "$WORKSPACE/constitution/directives/AUTO-EXEC.md"
    "$WORKSPACE/SOUL.md"
    "$WORKSPACE/HEARTBEAT.md"
)

for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        log "✅ $file"
    else
        log "🔴 缺失：$file"
    fi
done

# 2. 记忆提炼
log "🧠 记忆提炼..."
if [ -f "$WORKSPACE/memory/$(date +%Y-%m-%d).md" ]; then
    log "✅ 今日记忆文件已存在"
else
    log "📝 创建今日记忆文件..."
    cat > "$WORKSPACE/memory/$(date +%Y-%m-%d).md" << EOF
# $(date +%Y-%m-%d) 记忆

## 核心事件
- 

## 关键决策
- 

## 能力涌现
- 

## 待办事项
- [ ] 

*归档时间：$(date '+%Y-%m-%d %H:%M')*
EOF
    log "✅ 创建完成"
fi

# 3. 系统自检
log "🔍 系统自检..."
if [ -f "$WORKSPACE/scripts/self-check.sh" ]; then
    bash "$WORKSPACE/scripts/self-check.sh" --quick >> "$LOG_FILE" 2>&1
    log "✅ 自检完成"
else
    log "⚠️ 自检脚本不存在"
fi

# 4. HEARTBEAT 更新
log "📋 更新 HEARTBEAT..."
if [ -f "$WORKSPACE/HEARTBEAT.md" ]; then
    # 添加最后更新时间
    sed -i "s/最后更新：.*/最后更新：**$(date '+%Y-%m-%d %H:%M')**/" "$WORKSPACE/HEARTBEAT.md" 2>/dev/null || true
    log "✅ HEARTBEAT 已更新"
fi

# 5.  Git 提交
log "💾 Git 提交..."
cd "$WORKSPACE"
if ! git diff --quiet 2>/dev/null; then
    git add -A
    git commit -m "🌅 宪法学习 [$(date '+%Y-%m-%d %H:%M')]" >> "$LOG_FILE" 2>&1 || true
    log "✅ Git 提交完成"
else
    log "✅ 无变更，跳过提交"
fi

log "========== 宪法学习完成 =========="
log ""
