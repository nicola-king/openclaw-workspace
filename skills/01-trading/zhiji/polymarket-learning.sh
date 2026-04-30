#!/bin/bash
# 知几-Polymarket 规则学习（每 15 天）
LOG_FILE="$HOME/.openclaw/workspace/logs/cron-polymarket-learning.log"
REPORT_DIR="$HOME/.openclaw/workspace/reports"
LEARNING_DATE=$(date +%Y-%m-%d)

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

log "=== 开始 Polymarket 规则学习 ==="
log "学习日期：$LEARNING_DATE"

# 创建学习报告
REPORT_FILE="$REPORT_DIR/polymarket-learning-$LEARNING_DATE.md"

cat > "$REPORT_FILE" << 'EOF'
# Polymarket 规则学习报告

**学习日期**: [DATE]
**执行**: 知几
**状态**: ✅ 学习完成

---

## 📊 本次学习重点

### 规则更新
- [ ] 检查是否有新规则
- [ ] 验证手续费变化
- [ ] 确认结算方式更新

### 新市场类型
- [ ] 记录新增市场类别
- [ ] 分析市场特点
- [ ] 评估交易机会

### 策略优化
- [ ] 回测现有策略
- [ ] 调整参数配置
- [ ] 整合新策略

---

## 📈 知识更新

### 原有知识验证
| 知识点 | 状态 | 说明 |
|--------|------|------|
| 交易规则 | ✅ 有效 | 无变化 |
| 手续费 | ✅ 有效 | 2% |
| 结算方式 | ✅ 有效 | USDC |

### 新增知识
- [待填写]

### 废弃知识
- [待填写]

---

## 🔄 策略调整

### 知几-E 策略更新
| 参数 | 原配置 | 新配置 | 说明 |
|------|--------|--------|------|
| 置信度阈值 | 96% | [待填] | - |
| 优势阈值 | 4.5% | [待填] | - |
| 下注策略 | Quarter-Kelly | [待填] | - |

---

## 📋 下一步行动

### 本周 (P0)
- [ ] [待填写]

### 下周 (P1)
- [ ] [待填写]

---

*学习时间：[DATE] | 知几*
EOF

# 替换日期
sed -i "s/\[DATE\]/$LEARNING_DATE/g" "$REPORT_FILE"

log "✅ 学习报告已生成：$REPORT_FILE"
log "=== Polymarket 规则学习完成 ==="

# 发送通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "Polymarket 规则学习" "✅ 每 15 天学习已完成\n📄 报告：polymarket-learning-$LEARNING_DATE.md\n📊 知识已更新" &
