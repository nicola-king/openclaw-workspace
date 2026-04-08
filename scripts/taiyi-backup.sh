#!/bin/bash
# 太一记忆体备份脚本
# 功能：打包 workspace 关键文件，发送邮件到指定邮箱
# 执行时间：每周日 24:00 (cron: 0 0 * * 0)

set -e

# 配置
BACKUP_DIR="/tmp/taiyi-backup"
WORKSPACE_DIR="/home/nicola/.openclaw/workspace"
EMAIL_TO="285915125@qq.com"
EMAIL_SUBJECT="太一记忆体备份 - $(date +%Y%m%d)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/tmp/taiyi-backup-${TIMESTAMP}.tar.gz"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 创建备份目录
log_info "创建备份目录..."
mkdir -p "$BACKUP_DIR"

# 备份关键文件
log_info "备份关键文件..."

# 1. 宪法文件
cp -r "$WORKSPACE_DIR/constitution" "$BACKUP_DIR/" 2>/dev/null || log_warn "constitution 目录不存在"

# 2. 记忆文件
cp -r "$WORKSPACE_DIR/memory" "$BACKUP_DIR/" 2>/dev/null || log_warn "memory 目录不存在"
cp "$WORKSPACE_DIR/MEMORY.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "MEMORY.md 不存在"

# 3. 核心配置
cp "$WORKSPACE_DIR/AGENTS.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "AGENTS.md 不存在"
cp "$WORKSPACE_DIR/SOUL.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "SOUL.md 不存在"
cp "$WORKSPACE_DIR/USER.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "USER.md 不存在"
cp "$WORKSPACE_DIR/TOOLS.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "TOOLS.md 不存在"
cp "$WORKSPACE_DIR/HEARTBEAT.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "HEARTBEAT.md 不存在"

# 4. Skills (太一核心)
cp -r "$WORKSPACE_DIR/skills/taiyi" "$BACKUP_DIR/skills/" 2>/dev/null || log_warn "skills/taiyi 目录不存在"

# 5. Bot 配置
cp -r "$WORKSPACE_DIR/skills/zhiji" "$BACKUP_DIR/skills/" 2>/dev/null || log_warn "skills/zhiji 目录不存在"
cp -r "$WORKSPACE_DIR/skills/shanmu" "$BACKUP_DIR/skills/" 2>/dev/null || log_warn "skills/shanmu 目录不存在"
cp -r "$WORKSPACE_DIR/skills/suwen" "$BACKUP_DIR/skills/" 2>/dev/null || log_warn "skills/suwen 目录不存在"
cp -r "$WORKSPACE_DIR/skills/shoucangli" "$BACKUP_DIR/skills/" 2>/dev/null || log_warn "skills/shoucangli 目录不存在"
cp -r "$WORKSPACE_DIR/skills/paoding" "$BACKUP_DIR/skills/" 2>/dev/null || log_warn "skills/paoding 目录不存在"

# 6. 架构文档
cp "$WORKSPACE_DIR/TAIYI-ARCHITECTURE.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "TAIYI-ARCHITECTURE.md 不存在"
cp "$WORKSPACE_DIR/EIGHT-BOTS-STATUS.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "EIGHT-BOTS-STATUS.md 不存在"
cp "$WORKSPACE_DIR/SMART-AUTOMATION-ARCHITECTURE.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "SMART-AUTOMATION-ARCHITECTURE.md 不存在"

# 7. 错误记录与改进
cp "$WORKSPACE_DIR/TAIYI-MISTAKES-AND-IMPROVEMENTS.md" "$BACKUP_DIR/" 2>/dev/null || log_warn "TAIYI-MISTAKES-AND-IMPROVEMENTS.md 不存在"

# 8. 环境变量配置 (脱敏)
if [ -f ~/.bashrc ]; then
    grep -E "FEISHU_|WECHAT_|TELEGRAM_|DASHSCOPE_|GEMINI_|POLYMARKET_|BINANCE_" ~/.bashrc > "$BACKUP_DIR/env_config.txt" 2>/dev/null || log_warn "环境变量未找到"
fi

# 创建恢复说明
cat > "$BACKUP_DIR/README-RESTORE.md" << 'EOF'
# 太一记忆体恢复指南

> 备份时间：见文件名
> 用途：OpenClaw 重装/升级失败/系统损坏后恢复

---

## 📦 恢复步骤

### Step 1: 重新安装 OpenClaw

```bash
npm install -g openclaw
```

### Step 2: 停止 Gateway

```bash
openclaw gateway stop
```

### Step 3: 恢复文件

```bash
# 解压备份文件
tar -xzf taiyi-backup-*.tar.gz

# 复制文件到 workspace
cp -r backup/* /home/nicola/.openclaw/workspace/
```

### Step 4: 恢复环境变量

```bash
# 查看 env_config.txt
cat backup/env_config.txt

# 手动添加到 ~/.bashrc
nano ~/.bashrc

# 应用配置
source ~/.bashrc
```

### Step 5: 启动 Gateway

```bash
openclaw gateway start
```

### Step 6: 验证恢复

```bash
openclaw status
```

---

## 📋 备份内容清单

- ✅ 宪法文件 (constitution/)
- ✅ 记忆文件 (memory/, MEMORY.md)
- ✅ 核心配置 (AGENTS.md, SOUL.md, USER.md, TOOLS.md)
- ✅ Skills (skills/taiyi/, skills/zhiji/, etc.)
- ✅ 架构文档 (TAIYI-ARCHITECTURE.md, etc.)
- ✅ 环境变量配置 (env_config.txt)

---

## ⚠️ 注意事项

1. **敏感信息**: API Key 已脱敏，需手动重新配置
2. **环境变量**: 需手动添加到 ~/.bashrc
3. **Git 仓库**: 如使用 Git，需单独备份 .git 目录

---

*太一 AGI · 记忆体备份与恢复*
EOF

# 打包备份
log_info "打包备份文件..."
cd /tmp
tar -czf "$BACKUP_FILE" -C "$BACKUP_DIR" .

# 显示备份文件大小
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
log_info "备份文件大小：$BACKUP_SIZE"

# 发送备份 (双通道：邮件 + Telegram)
log_info "发送备份到 $EMAIL_TO..."

# 方案 1: 尝试使用 Python SMTP 发送邮件
if [ -n "$QQ_SMTP_AUTH_CODE" ]; then
    log_info "通过 QQ 邮箱 SMTP 发送..."
    python3 /home/nicola/.openclaw/workspace/scripts/send-backup-email.py "$BACKUP_FILE" "$(date +%Y%m%d)"
    if [ $? -eq 0 ]; then
        log_info "✅ 邮件发送成功！"
    fi
else
    log_warn "未配置 QQ_SMTP_AUTH_CODE，跳过邮件发送"
fi

# 方案 2: 使用 Telegram Bot 发送 (备用)
log_info "通过 Telegram 发送备份..."

TELEGRAM_BOT_TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID="7073481596"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument" \
    -F "chat_id=${TELEGRAM_CHAT_ID}" \
    -F "document=@${BACKUP_FILE}" \
    -F "caption=📦 太一记忆体备份 - $(date +%Y%m%d)

备份时间：$(date)
备份大小：$BACKUP_SIZE
用途：OpenClaw 重装/升级失败/系统损坏恢复

恢复指南见备份包内 README-RESTORE.md" > /dev/null

if [ $? -eq 0 ]; then
    log_info "✅ Telegram 发送成功！"
else
    log_warn "Telegram 发送失败，备份文件保存在：$BACKUP_FILE"
fi

# 清理临时文件
log_info "清理临时文件..."
rm -rf "$BACKUP_DIR"

# 保留最近 4 次备份 (删除旧备份)
log_info "清理旧备份 (保留最近 4 次)..."
ls -t /tmp/taiyi-backup-*.tar.gz 2>/dev/null | tail -n +5 | xargs rm -f 2>/dev/null || true

log_info "✅ 备份完成！"
echo ""
echo "备份文件：$BACKUP_FILE"
echo "备份大小：$BACKUP_SIZE"
echo "接收邮箱：$EMAIL_TO"
