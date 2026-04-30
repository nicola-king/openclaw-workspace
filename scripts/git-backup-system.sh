#!/bin/bash
# Git 版本管理 + 自动备份系统
# 功能：自动提交、每日备份、丢失恢复、远程同步
# 🆕 v1.1 (2026-04-03 14:45): 备份频率调整为 12 小时一次

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
BACKUP_DIR="/home/nicola/.openclaw/backup"
LOG_FILE="/home/nicola/.openclaw/logs/git-backup.log"
STATE_FILE="/tmp/git-backup-state.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

ensure_dirs() {
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$(dirname "$LOG_FILE")"
}

# Git 自动提交（每 30 分钟）
auto_commit() {
    log "${YELLOW}[Git 提交]${NC} 检查变更..."
    
    cd "$WORKSPACE"
    
    # 忽略 __pycache__ 和临时文件
    git add -A
    git diff --cached --quiet && {
        log "${GREEN}[Git 提交]${NC} 无变更，跳过"
        return 0
    }
    
    # 生成提交信息
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
    CHANGED_FILES=$(git diff --cached --name-only | wc -l)
    COMMIT_MSG="🤖 自动提交 [$TIMESTAMP] - $CHANGED_FILES 个文件变更"
    
    git commit -m "$COMMIT_MSG"
    log "${GREEN}[Git 提交]${NC} 完成：$COMMIT_MSG"
    
    # 尝试 push（如果有 remote）
    if git remote -v | grep -q origin; then
        log "${YELLOW}[Git 推送]${NC} 推送到远程..."
        git push origin master 2>&1 | tee -a "$LOG_FILE" || {
            log "${RED}[Git 推送]${NC} 失败（可能无网络或无权限）"
        }
    fi
    
    # 更新状态
    update_state "last_commit" "$(date +%s)"
}

# 每日备份（压缩归档）
daily_backup() {
    log "${YELLOW}[每日备份]${NC} 开始备份..."
    
    ensure_dirs
    
    BACKUP_DATE=$(date '+%Y%m%d')
    BACKUP_FILE="$BACKUP_DIR/workspace-$BACKUP_DATE.tar.gz"
    
    # 创建压缩备份
    tar -czf "$BACKUP_FILE" \
        --exclude='.git' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='node_modules' \
        -C "$(dirname "$WORKSPACE")" \
        "$(basename "$WORKSPACE")"
    
    # 保留最近 30 天备份
    find "$BACKUP_DIR" -name "workspace-*.tar.gz" -mtime +30 -delete
    
    log "${GREEN}[每日备份]${NC} 完成：$BACKUP_FILE"
    log "${GREEN}[每日备份]${NC} 大小：$(du -h "$BACKUP_FILE" | cut -f1)"
    
    update_state "last_backup" "$(date +%s)"
    update_state "backup_file" "$BACKUP_FILE"
}

# 文件丢失检测与恢复
check_and_restore() {
    log "${YELLOW}[丢失检测]${NC} 扫描关键文件..."
    
    cd "$WORKSPACE"
    
    # 关键文件列表（宪法 + 核心配置）
    CRITICAL_FILES=(
        "SOUL.md"
        "AGENTS.md"
        "USER.md"
        "HEARTBEAT.md"
        "MEMORY.md"
        "constitution/directives/NEGENTROPY.md"
        "constitution/directives/AUTO-EXEC.md"
        "constitution/CONST-ROUTER.md"
    )
    
    RESTORED=0
    
    for file in "${CRITICAL_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            log "${RED}[丢失检测]${NC} 发现丢失：$file"
            
            # 尝试从 Git 恢复
            if git show HEAD:"$file" > "$file" 2>/dev/null; then
                log "${GREEN}[恢复完成]${NC} 已恢复：$file"
                RESTORED=$((RESTORED + 1))
            else
                log "${RED}[恢复失败]${NC} 无法恢复：$file"
            fi
        fi
    done
    
    if [ $RESTORED -gt 0 ]; then
        log "${GREEN}[恢复统计]${NC} 本次恢复 $RESTORED 个文件"
        update_state "last_restore" "$(date +%s)"
        update_state "restored_count" "$RESTORED"
    else
        log "${GREEN}[丢失检测]${NC} 所有关键文件完整"
    fi
}

# 状态更新
update_state() {
    local key="$1"
    local value="$2"
    
    # 创建或更新状态文件
    if [ -f "$STATE_FILE" ]; then
        # 使用 jq 更新（如果可用）
        if command -v jq &> /dev/null; then
            jq ".$key = \"$value\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
        else
            # 简单 JSON 更新（无 jq）
            echo "{\"last_commit\": \"$(date -d @$(grep -o '"last_commit": "[0-9]*' "$STATE_FILE" | grep -o '[0-9]*') '+%Y-%m-%d %H:%M')\", \"$key\": \"$value\"}" > "$STATE_FILE"
        fi
    else
        echo "{\"$key\": \"$value\"}" > "$STATE_FILE"
    fi
}

# 显示状态
show_status() {
    echo "=== Git 备份系统状态 ==="
    echo ""
    
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo "状态文件不存在"
    fi
    
    echo ""
    echo "=== 最近备份 ==="
    ls -lht "$BACKUP_DIR"/*.tar.gz 2>/dev/null | head -5 || echo "无备份文件"
    
    echo ""
    echo "=== Git 状态 ==="
    cd "$WORKSPACE"
    git status --short | head -10
}

# 主函数
main() {
    local action="${1:-status}"
    
    case "$action" in
        commit)
            auto_commit
            ;;
        backup)
            daily_backup
            ;;
        restore)
            check_and_restore
            ;;
        status)
            show_status
            ;;
        all)
            check_and_restore
            auto_commit
            daily_backup
            ;;
        *)
            echo "用法：$0 {commit|backup|restore|status|all}"
            exit 1
            ;;
    esac
}

main "$@"
