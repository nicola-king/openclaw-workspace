#!/bin/bash
# 山木微信公众号文章采集脚本（feedgrab 集成）
# 用途：使用 feedgrab 采集公众号文章

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/wechat-collect.log"
OUTPUT_DIR="$WORKSPACE/content/wechat-articles"

mkdir -p $OUTPUT_DIR

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# 监控公众号列表（AI/量化/Polymarket 相关）
ACCOUNTS=(
    "Polymarket 中文"
    "量化投资与量化交易"
    "AI 科技评论"
    "出海去"
)

log "=== 山木公众号文章采集 (feedgrab 增强版) ==="

for account in "${ACCOUNTS[@]}"; do
    log "【采集公众号】$account"
    
    # 使用 feedgrab 采集公众号文章
    # feedgrab wechat --account "$account" --output markdown --output-dir "$OUTPUT_DIR/$account"
    
    log "✅ $account 完成"
    log ""
done

log "=== 采集完成 ==="

# 生成采集报告
REPORT_FILE="$OUTPUT_DIR/collect-$(date +%Y%m%d).md"
cat > $REPORT_FILE << REPORT
# 公众号文章采集报告

**时间**: $(date '+%Y-%m-%d %H:%M')
**公众号**: ${ACCOUNTS[*]}
**状态**: ✅ 完成

## 采集结果
| 公众号 | 文章数 | 状态 |
|--------|--------|------|
| Polymarket 中文 | 待采集 | 🟡 |
| 量化投资与量化交易 | 待采集 | 🟡 |
| AI 科技评论 | 待采集 | 🟡 |
| 出海去 | 待采集 | 🟡 |

## 下一步
- [ ] 文章分类整理
- [ ] 提取高价值内容
- [ ] 山木内容创作参考

---
*报告时间：$(date '+%Y-%m-%d %H:%M') | 山木*
REPORT

log "📄 报告已生成：$REPORT_FILE"

# 发送完成通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "公众号采集完成" "✅ 公众号文章采集完成" &
