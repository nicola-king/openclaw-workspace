#!/bin/bash
# 日报生成定时任务 - 每日 23:00 自动执行
# 功能：汇总当日记忆 + 生成日报 + 归档

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
REPORT_DIR="$WORKSPACE/reports"
LOG_FILE="/home/nicola/.openclaw/logs/daily-report.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/daily-report-$TODAY.md"

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "========== 日报生成开始 =========="

# 确保目录存在
mkdir -p "$REPORT_DIR"

# 1. 汇总当日记忆
log "📝 汇总当日记忆..."
MEMORY_FILE="$WORKSPACE/memory/$TODAY.md"
if [ -f "$MEMORY_FILE" ]; then
    log "✅ 读取 $MEMORY_FILE"
else
    log "📝 创建记忆文件..."
    mkdir -p "$WORKSPACE/memory"
    cat > "$MEMORY_FILE" << EOF
# $TODAY 记忆

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
fi

# 2. 生成日报框架
log "📊 生成日报框架..."
cat > "$REPORT_FILE" << EOF
# $TODAY 日报

> 生成时间：$(date '+%Y-%m-%d %H:%M') | 太一 AGI

---

## 📋 今日核心成果

| 任务 | 状态 | 详情 |
|------|------|------|
| - | 🟡 待填写 | - |

---

## 🛠️ 技术决策

- 

---

## 📊 产出统计

| 指标 | 数值 |
|------|------|
| 文件变更 | - |
| Git 提交 | - |
| 执行时间 | - |

---

## 🎯 明日计划

### P0 任务
| 编号 | 任务 | 截止 | 状态 |
|------|------|------|------|
| - | - | - | 🔴 待填写 |

### P1 任务
- [ ] 

---

## 💓 系统状态

### 每日检查
- [ ] Gateway 状态
- [ ] Cron 任务
- [ ] Bot 配置
- [ ] 宪法文件

### 每周检查（周一）
- [ ] 聚合本周 memory
- [ ] 更新 MEMORY.md
- [ ] 生成周报

---

*日报生成完成 | 太一 AGI | $TODAY*
EOF

log "✅ 日报已生成：$REPORT_FILE"

# 3. Git 提交
log "💾 Git 提交..."
cd "$WORKSPACE"
if ! git diff --quiet 2>/dev/null; then
    git add -A
    git commit -m "📊 日报生成 [$TODAY]" >> "$LOG_FILE" 2>&1 || true
    log "✅ Git 提交完成"
else
    log "✅ 无变更，跳过提交"
fi

log "========== 日报生成完成 =========="
log ""
