#!/bin/bash
#
# 环境安全验证脚本 (.env Security Validator)
#
# 功能:
# 1. 验证 .env 文件安全性
# 2. 阻止敏感变量被覆盖
# 3. 检测 unsafe URL-style 控制
# 4. 运行时报错而非静默失败
#
# 灵感来源：OpenClaw v2026.4.9 Security/dotenv
#
# 作者：太一 AGI
# 创建：2026-04-10
#

set -e

# 配置
WORKSPACE="/home/nicola/.openclaw/workspace"
ENV_FILE="${WORKSPACE}/.env"
ENV_SECURITY_FILE="${WORKSPACE}/.env.security"
LOG_FILE="${WORKSPACE}/logs/env-security-$(date +%Y%m%d-%H%M%S).log"

# 敏感变量白名单 (不应被工作区 .env 覆盖)
SENSITIVE_VARS=(
    "GATEWAY_BIND"
    "GATEWAY_REMOTE_URL"
    "OPENCLAW_ADMIN_PASSWORD"
    "NODE_EXEC_ALLOWED"
    "BROWSER_CONTROL_OVERRIDE"
    "SKIP_SERVER"
    "RUNTIME_CONTROL"
    "AGENT_DEFAULTS_TIMEOUT"
    "AGENT_DEFAULTS_IDLE_TIMEOUT"
)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1" | tee -a "$LOG_FILE"
}

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

log "═══════════════════════════════════════════════════════════"
log "环境安全验证 - .env Security Validator"
log "═══════════════════════════════════════════════════════════"
log ""

# 检查 .env 文件是否存在
if [ ! -f "$ENV_FILE" ]; then
    warn ".env 文件不存在，跳过验证"
    exit 0
fi

log "检查文件：$ENV_FILE"
log ""

# 计数器
ISSUES_FOUND=0
VARS_CHECKED=0

# 检查敏感变量
log "【1】检查敏感变量覆盖..."
for var in "${SENSITIVE_VARS[@]}"; do
    if grep -q "^${var}=" "$ENV_FILE"; then
        value=$(grep "^${var}=" "$ENV_FILE" | cut -d'=' -f2-)
        
        # 检查是否是危险值
        if [[ "$value" == *"http://"* ]] || [[ "$value" == *"0.0.0.0"* ]] || [[ "$value" == *"localhost"* ]]; then
            error "敏感变量 $var 被设置为危险值：$value"
            ((ISSUES_FOUND++))
        else
            warn "敏感变量 $var 在工作区 .env 中定义：$value"
            ((VARS_CHECKED++))
        fi
    fi
done
log ""

# 检查 URL-style 浏览器控制覆盖
log "【2】检查 URL-style 浏览器控制覆盖..."
URL_PATTERNS=(
    "BROWSER_CONTROL_OVERRIDE=.*http://"
    "BROWSER_CONTROL_OVERRIDE=.*ws://"
    "SKIP_SERVER=.*http://"
    "RUNTIME_CONTROL=.*http://"
)

for pattern in "${URL_PATTERNS[@]}"; do
    if grep -qE "$pattern" "$ENV_FILE"; then
        match=$(grep -E "$pattern" "$ENV_FILE")
        error "检测到 unsafe URL-style 覆盖：$match"
        ((ISSUES_FOUND++))
    fi
done
log ""

# 检查基本安全配置
log "【3】检查基本安全配置..."

# 检查是否有明文密码
if grep -qiE "(PASSWORD|SECRET|KEY|TOKEN)=.+" "$ENV_FILE" | grep -v "^#"; then
    # 提取变量名 (不显示值)
    insecure_vars=$(grep -iE "(PASSWORD|SECRET|KEY|TOKEN)=.+" "$ENV_FILE" | grep -v "^#" | cut -d'=' -f1)
    if [ -n "$insecure_vars" ]; then
        warn "检测到敏感变量定义 (请确保值已加密或使用环境变量):"
        echo "$insecure_vars" | while read var; do
            warn "  - $var"
        done
    fi
fi
log ""

# 检查是否有硬编码 IP/端口
log "【4】检查硬编码网络配置..."
if grep -qE "=[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" "$ENV_FILE" | grep -v "^#"; then
    warn "检测到硬编码 IP 地址 (建议 DNS 或配置文件管理)"
fi

if grep -qE "PORT=[0-9]+" "$ENV_FILE" | grep -v "^#"; then
    warn "检测到硬编码端口 (确保防火墙规则正确)"
fi
log ""

# 检查 .env.security 文件 (如果存在)
log "【5】检查 .env.security 配置文件..."
if [ -f "$ENV_SECURITY_FILE" ]; then
    success "找到 .env.security 配置文件"
    # 可以在此添加额外的安全检查逻辑
else
    log ".env.security 不存在 (可选配置文件)"
fi
log ""

# 总结
log "═══════════════════════════════════════════════════════════"
log "验证总结"
log "═══════════════════════════════════════════════════════════"
log "检查变量数：$VARS_CHECKED"
log "发现问题：$ISSUES_FOUND"
log "日志文件：$LOG_FILE"
log ""

if [ $ISSUES_FOUND -gt 0 ]; then
    error "发现 $ISSUES_FOUND 个安全问题，请审查后修复!"
    exit 1
else
    success "环境安全检查通过 ✅"
    exit 0
fi
