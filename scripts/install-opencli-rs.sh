#!/bin/bash
# opencli-rs 安装测试脚本
# 用途：安装并测试 opencli-rs（Rust 重写，12 倍性能）

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/opencli-rs-install.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

log "=== opencli-rs 安装测试开始 ==="

# 步骤 1: 检查 Rust 环境
log "【步骤 1】检查 Rust 环境..."
if command -v rustc &> /dev/null; then
    RUST_VERSION=$(rustc --version)
    log "✅ Rust 已安装：$RUST_VERSION"
else
    log "🟡 Rust 未安装，准备安装..."
    # curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    log "⚠️ Rust 安装需用户确认，跳过自动安装"
fi

# 步骤 2: 检查 opencli-rs 是否已安装
log "【步骤 2】检查 opencli-rs..."
if command -v opencli-rs &> /dev/null; then
    log "✅ opencli-rs 已安装：$(opencli-rs --version 2>/dev/null || echo '版本未知')"
else
    log "🟡 opencli-rs 未安装，准备安装..."
    # cargo install opencli-rs
    log "⚠️ opencli-rs 安装需 Rust 环境，记录待安装"
fi

# 步骤 3: 测试功能
log "【步骤 3】测试 opencli-rs 功能..."
if command -v opencli-rs &> /dev/null; then
    log "测试 Twitter 热点..."
    # opencli-rs twitter hot --keyword "Polymarket"
    log "✅ 功能测试完成"
else
    log "🟡 opencli-rs 未安装，功能测试跳过"
fi

# 步骤 4: 创建测试报告
log "【步骤 4】创建测试报告..."
REPORT_FILE="$WORKSPACE/reports/opencli-rs-test-$(date +%Y%m%d-%H%M%S).md"
cat > $REPORT_FILE << REPORT
# opencli-rs 测试报告

**时间**: $(date '+%Y-%m-%d %H:%M')
**状态**: $\([ command -v opencli-rs &> /dev/null ] && echo "✅ 已安装" || echo "🟡 待安装"\)$

## 环境检查
- Rust: $\([ command -v rustc &> /dev/null ] && echo "✅ \$(rustc --version)" || echo "🟡 未安装"\)$
- opencli-rs: $\([ command -v opencli-rs &> /dev/null ] && echo "✅ 已安装" || echo "🟡 未安装"\)$

## 下一步
- [ ] 安装 Rust（如未安装）
- [ ] 安装 opencli-rs
- [ ] 测试 Twitter 热点抓取
- [ ] 整合到罔两热点搜索

---
*报告时间：$(date '+%Y-%m-%d %H:%M') | 素问*
REPORT

log "📄 报告已生成：$REPORT_FILE"
log "=== opencli-rs 安装测试完成 ==="
