#!/bin/bash
# 云 CLI 快速配置脚本 - 太一 AGI v5.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "========================================"
echo "  太一 AGI v5.0 · 云 CLI 配置向导"
echo "========================================"
echo ""

# 检查是否已安装
check_install() {
    if command -v $1 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# ==================== AWS ====================
configure_aws() {
    echo ""
    echo "【1/3】配置 AWS CLI"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if ! check_install aws; then
        log_warn "AWS CLI 未安装"
        echo "安装命令：curl 'https://awscli.amazonaws.com/awscli-2.2.0.zip' -o 'awscli.zip'"
        return 1
    fi
    
    read -p "是否配置 AWS? (y/n): " choice
    if [ "$choice" != "y" ]; then
        log_warn "跳过 AWS 配置"
        return 0
    fi
    
    echo ""
    echo "请登录 AWS 控制台获取凭证:"
    echo "https://console.aws.amazon.com/iam/home?#/security_credentials"
    echo ""
    
    aws configure
    
    # 验证
    if aws sts get-caller-identity &>/dev/null; then
        log_success "AWS 配置成功!"
        aws sts get-caller-identity --query 'Arn' --output text
    else
        log_error "AWS 验证失败"
        return 1
    fi
}

# ==================== GCP ====================
configure_gcp() {
    echo ""
    echo "【2/3】配置 GCP CLI"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if ! check_install gcloud; then
        log_warn "gcloud 未安装"
        echo "安装命令：curl https://sdk.cloud.google.com | bash"
        read -p "是否现在安装？(y/n): " choice
        if [ "$choice" = "y" ]; then
            curl https://sdk.cloud.google.com | bash
            exec -l $SHELL
        else
            return 1
        fi
    fi
    
    read -p "是否配置 GCP? (y/n): " choice
    if [ "$choice" != "y" ]; then
        log_warn "跳过 GCP 配置"
        return 0
    fi
    
    echo ""
    echo "即将打开浏览器进行认证..."
    gcloud auth login
    
    # 设置项目
    echo ""
    echo "可用项目:"
    gcloud projects list --format="table(projectId,name)"
    
    read -p "输入默认项目 ID: " project_id
    if [ -n "$project_id" ]; then
        gcloud config set project "$project_id"
    fi
    
    # 验证
    if gcloud config get-value project &>/dev/null; then
        log_success "GCP 配置成功!"
        echo "项目：$(gcloud config get-value project)"
    else
        log_error "GCP 验证失败"
        return 1
    fi
}

# ==================== Azure ====================
configure_azure() {
    echo ""
    echo "【3/3】配置 Azure CLI"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if ! check_install az; then
        log_warn "Azure CLI 未安装"
        echo "安装命令：curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
        return 1
    fi
    
    read -p "是否配置 Azure? (y/n): " choice
    if [ "$choice" != "y" ]; then
        log_warn "跳过 Azure 配置"
        return 0
    fi
    
    echo ""
    echo "即将打开浏览器进行认证..."
    echo "如无浏览器，使用：az login --use-device-code"
    echo ""
    
    az login
    
    # 显示订阅
    echo ""
    echo "可用订阅:"
    az account list --output table
    
    read -p "输入默认订阅 ID 或名称: " subscription
    if [ -n "$subscription" ]; then
        az account set --subscription "$subscription"
    fi
    
    # 验证
    if az account show &>/dev/null; then
        log_success "Azure 配置成功!"
        echo "订阅：$(az account show --query 'name' --output text)"
    else
        log_error "Azure 验证失败"
        return 1
    fi
}

# ==================== 主流程 ====================
main() {
    configure_aws || true
    configure_gcp || true
    configure_azure || true
    
    echo ""
    echo "========================================"
    echo "  配置完成!"
    echo "========================================"
    echo ""
    echo "验证命令:"
    echo "  ./scripts/verify-skills.sh"
    echo ""
    echo "使用示例:"
    echo "  ./scripts/cli-wrapper.sh aws ec2 describe-instances"
    echo "  ./scripts/cli-wrapper.sh gcloud compute instances list"
    echo "  ./scripts/cli-wrapper.sh az vm list"
    echo ""
}

main
