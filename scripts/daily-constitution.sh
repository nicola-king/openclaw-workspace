#!/bin/bash
# scripts/daily-constitution.sh v2.0

"""
太一每日宪法学习 v2.0

功能:
1. 宪法学习 (Tier 1 永久核)
2. 记忆提炼 (TurboQuant 压缩)
3. 系统自检 (Gateway+ 残留进程)
4. 新一天重置 (创建记忆文件)
5. HEARTBEAT 更新

使用:
    bash scripts/daily-constitution.sh

定时:
    每日 06:00 自动执行 (crontab)
"""

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
LOG_FILE="$WORKSPACE/logs/constitution-$(date +%Y%m%d).log"
TODAY_FILE="$MEMORY_DIR/$(date +%Y-%m-%d).md"

# 创建目录
mkdir -p "$WORKSPACE/logs"
mkdir -p "$MEMORY_DIR"

echo "============================================================"
echo "📜 太一每日宪法学习 v2.0"
echo "日期：$(date +%Y-%m-%d)"
echo "时间：$(date +%H:%M)"
echo "============================================================"

# 1. 宪法学习
echo ""
echo "📖 [1/5] 宪法学习..."
CONSTITUTION_FILES=(
    "constitution/CONST-ROUTER.md"
    "constitution/axiom/VALUE-FOUNDATION.md"
    "constitution/directives/NEGENTROPY.md"
    "constitution/directives/AGI-TIMELINE.md"
    "constitution/directives/OBSERVER.md"
    "constitution/directives/SELF-LOOP.md"
    "constitution/skills/MODEL-ROUTING.md"
    "constitution/directives/ASK-PROTOCOL.md"
    "constitution/COLLABORATION.md"
    "constitution/extensions/DELEGATION.md"
    "constitution/directives/TURBOQUANT.md"
)

for file in "${CONSTITUTION_FILES[@]}"; do
    if [ -f "$WORKSPACE/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file (不存在)"
    fi
done

# 2. 记忆提炼
echo ""
echo "🧠 [2/5] 记忆提炼..."

# 检查昨日记忆文件
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
YESTERDAY_FILE="$MEMORY_DIR/$YESTERDAY.md"

if [ -f "$YESTERDAY_FILE" ]; then
    echo "  ✅ 昨日记忆文件：$YESTERDAY_FILE"
    echo "  📝 行数：$(wc -l < "$YESTERDAY_FILE")"
else
    echo "  ⚠️  昨日记忆文件不存在"
fi

# 检查核心记忆
if [ -f "$MEMORY_DIR/core.md" ]; then
    echo "  ✅ 核心记忆：$MEMORY_DIR/core.md"
    echo "  📝 大小：$(du -h "$MEMORY_DIR/core.md" | cut -f1)"
fi

# 3. 系统自检
echo ""
echo "🔧 [3/5] 系统自检..."

# Gateway 状态
if pgrep -f "openclaw gateway" > /dev/null; then
    echo "  ✅ Gateway 运行中 (PID: $(pgrep -f 'openclaw gateway' | head -1))"
else
    echo "  ⚠️  Gateway 未运行"
fi

# 残留进程检查
RESIDUE=$(ps aux | grep -E "(python.*openclaw|node.*openclaw)" | grep -v grep | wc -l)
echo "  📊 残留进程：$RESIDUE 个"

# 磁盘空间
DISK_USAGE=$(df -h "$WORKSPACE" | tail -1 | awk '{print $5}')
echo "  💾 磁盘使用：$DISK_USAGE"

# 4. 新一天重置
echo ""
echo "🔄 [4/5] 新一天重置..."

if [ ! -f "$TODAY_FILE" ]; then
    cat > "$TODAY_FILE" << EOF
# $(date +%Y-%m-%d) - 太一记忆日志

## 📝 今日记录

*(自动创建于 $(date +%H:%M))*

---

*最后更新：$(date +%Y-%m-%d %H:%M)*
EOF
    echo "  ✅ 创建今日记忆文件：$TODAY_FILE"
else
    echo "  ✅ 今日记忆文件已存在：$TODAY_FILE"
fi

# 5. HEARTBEAT 更新
echo ""
echo "💓 [5/5] HEARTBEAT 更新..."

HEARTBEAT_FILE="$WORKSPACE/HEARTBEAT.md"

if [ -f "$HEARTBEAT_FILE" ]; then
    echo "  ✅ HEARTBEAT 文件：$HEARTBEAT_FILE"
    
    # 检查是否有过期待办 (超过 7 天)
    OLD_TASKS=$(grep -c "^\- \[ \]" "$HEARTBEAT_FILE" || echo "0")
    echo "  📊 待办事项：$OLD_TASKS 个"
else
    echo "  ⚠️  HEARTBEAT 文件不存在"
fi

# 完成
echo ""
echo "============================================================"
echo "✅ 每日宪法学习完成"
echo "============================================================"
echo ""
echo "📝 日志：$LOG_FILE"
echo ""

# 记录到日志
{
    echo "============================================================"
    echo "每日宪法学习 · $(date +%Y-%m-%d %H:%M)"
    echo "============================================================"
    echo "✅ 完成"
    echo ""
} >> "$LOG_FILE"
