#!/bin/bash
# CLI Wrapper for Taiyi AGI v5.0
# 统一封装 Git/Docker/NPM/K8s/Terraform/Cloud CLI

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查命令是否存在
check_cmd() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装"
        return 1
    fi
    return 0
}

# ==================== Git ====================
git_wrapper() {
    local cmd=$1
    shift
    case $cmd in
        clone)
            log_info "克隆仓库：$1"
            git clone "$@"
            log_success "克隆完成"
            ;;
        status)
            git status --short
            ;;
        add)
            git add "$@"
            log_success "文件已添加"
            ;;
        commit)
            git commit -m "$*"
            log_success "提交完成"
            ;;
        push)
            git push "$@"
            log_success "推送完成"
            ;;
        pull)
            git pull "$@"
            log_success "拉取完成"
            ;;
        branch)
            git branch -a "$@"
            ;;
        checkout)
            git checkout "$@"
            log_success "切换分支完成"
            ;;
        log)
            git log --oneline -${1:-10}
            ;;
        *)
            git "$cmd" "$@"
            ;;
    esac
}

# ==================== Docker ====================
docker_wrapper() {
    local cmd=$1
    shift
    case $cmd in
        run)
            log_info "运行容器：$*"
            docker run "$@"
            ;;
        ps)
            docker ps -a "$@"
            ;;
        images)
            docker images "$@"
            ;;
        build)
            log_info "构建镜像：$*"
            docker build "$@"
            ;;
        logs)
            docker logs "$@"
            ;;
        exec)
            docker exec "$@"
            ;;
        stop)
            docker stop "$@"
            log_success "容器已停止"
            ;;
        start)
            docker start "$@"
            log_success "容器已启动"
            ;;
        rm)
            docker rm "$@"
            log_success "容器已删除"
            ;;
        compose)
            docker compose "$@"
            ;;
        *)
            docker "$cmd" "$@"
            ;;
    esac
}

# ==================== NPM ====================
npm_wrapper() {
    local cmd=$1
    shift
    case $cmd in
        install)
            log_info "安装依赖：$*"
            npm install "$@"
            ;;
        audit)
            log_info "安全审计..."
            npm audit "$@"
            ;;
        outdated)
            npm outdated "$@"
            ;;
        run)
            npm run "$@"
            ;;
        test)
            npm test "$@"
            ;;
        build)
            npm run build "$@"
            ;;
        *)
            npm "$cmd" "$@"
            ;;
    esac
}

# ==================== Kubectl ====================
kubectl_wrapper() {
    if ! check_cmd kubectl; then
        log_warn "kubectl 未安装，跳过"
        return 1
    fi
    local cmd=$1
    shift
    case $cmd in
        get)
            kubectl get "$@"
            ;;
        apply)
            log_info "应用配置：$*"
            kubectl apply "$@"
            ;;
        delete)
            kubectl delete "$@"
            log_success "资源已删除"
            ;;
        logs)
            kubectl logs "$@"
            ;;
        exec)
            kubectl exec "$@"
            ;;
        describe)
            kubectl describe "$@"
            ;;
        scale)
            log_info "扩缩容：$*"
            kubectl scale "$@"
            ;;
        *)
            kubectl "$cmd" "$@"
            ;;
    esac
}

# ==================== Terraform ====================
terraform_wrapper() {
    if ! check_cmd terraform; then
        log_warn "terraform 未安装，跳过"
        return 1
    fi
    local cmd=$1
    shift
    case $cmd in
        init)
            log_info "初始化 Terraform..."
            terraform init "$@"
            ;;
        plan)
            log_info "生成执行计划..."
            terraform plan "$@"
            ;;
        apply)
            log_warn "应用变更：$* (需确认)"
            terraform apply "$@"
            ;;
        destroy)
            log_error "销毁资源：$* (危险操作)"
            terraform destroy "$@"
            ;;
        state)
            terraform state "$@"
            ;;
        output)
            terraform output "$@"
            ;;
        *)
            terraform "$cmd" "$@"
            ;;
    esac
}

# ==================== AWS CLI ====================
aws_wrapper() {
    if ! check_cmd aws; then
        log_warn "aws CLI 未安装，跳过"
        return 1
    fi
    local service=$1
    shift
    aws "$service" "$@"
}

# ==================== GCP CLI ====================
gcloud_wrapper() {
    if ! check_cmd gcloud; then
        log_warn "gcloud 未安装，跳过"
        return 1
    fi
    local cmd=$1
    shift
    gcloud "$cmd" "$@"
}

# ==================== Azure CLI ====================
az_wrapper() {
    if ! check_cmd az; then
        log_warn "az CLI 未安装，跳过"
        return 1
    fi
    local cmd=$1
    shift
    az "$cmd" "$@"
}

# ==================== 主入口 ====================
main() {
    local tool=$1
    shift
    
    if [ -z "$tool" ]; then
        echo "用法：$0 <tool> <command> [args...]"
        echo ""
        echo "支持的工具:"
        echo "  git       - Git 版本控制"
        echo "  docker    - Docker 容器管理"
        echo "  npm       - NPM 包管理"
        echo "  kubectl   - Kubernetes (需安装)"
        echo "  terraform - Terraform IaC (需安装)"
        echo "  aws       - AWS CLI (需安装)"
        echo "  gcloud    - GCP CLI (需安装)"
        echo "  az        - Azure CLI (需安装)"
        echo ""
        echo "示例:"
        echo "  $0 git clone https://github.com/user/repo.git"
        echo "  $0 docker run -d -p 80:80 nginx"
        echo "  $0 npm install"
        exit 0
    fi
    
    case $tool in
        git)
            git_wrapper "$@"
            ;;
        docker)
            docker_wrapper "$@"
            ;;
        npm)
            npm_wrapper "$@"
            ;;
        kubectl)
            kubectl_wrapper "$@"
            ;;
        terraform)
            terraform_wrapper "$@"
            ;;
        aws)
            aws_wrapper "$@"
            ;;
        gcloud)
            gcloud_wrapper "$@"
            ;;
        az)
            az_wrapper "$@"
            ;;
        *)
            log_error "未知工具：$tool"
            exit 1
            ;;
    esac
}

main "$@"
