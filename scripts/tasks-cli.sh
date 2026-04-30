#!/usr/bin/env bash
# OpenClaw /tasks CLI 工具
# 版本：1.0 | 创建时间：2026-04-02 12:12
# 功能：任务可视化管理（待办/执行中/完成）

set -e

# 配置
TASKS_FILE="${OPENCLAW_HOME:-$HOME/.openclaw}/workspace/HEARTBEAT.md"
TASK_LOG="${OPENCLAW_HOME:-$HOME/.openclaw}/workspace/memory/task-log.json"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    cat << EOF
${BLUE}OpenClaw /tasks CLI 工具${NC}

用法：
  $0 <command> [options]

命令:
  list              查看所有任务
  add <title>       添加新任务
  start <id>        开始任务（标记为执行中）
  complete <id>     完成任务
  remove <id>       删除任务
  search <query>    搜索任务
  stats             显示统计信息

示例:
  $0 list
  $0 add "知几下注"
  $0 start TASK-050
  $0 complete TASK-050

环境变量:
  OPENCLAW_HOME     OpenClaw 主目录（默认：~/.openclaw）
EOF
}

# 初始化任务日志
init_task_log() {
    if [ ! -f "$TASK_LOG" ]; then
        echo '{"tasks":[]}' > "$TASK_LOG"
    fi
}

# 生成任务 ID
generate_id() {
    local prefix=$1
    local timestamp=$(date +%s)
    local random=$(shuf -i 1000-9999 -n 1)
    echo "${prefix}-${random}"
}

# 列出所有任务
list_tasks() {
    init_task_log
    
    echo -e "${BLUE}=== 任务列表 ===${NC}\n"
    
    # 待办任务
    echo -e "${YELLOW}📋 待办 (TODO):${NC}"
    jq -r '.tasks[] | select(.status=="todo") | "  [\(.id)] \(.title) (创建：\(.created_at))"' "$TASK_LOG" 2>/dev/null || echo "  (无)"
    
    echo ""
    
    # 执行中任务
    echo -e "${BLUE}🔄 执行中 (IN_PROGRESS):${NC}"
    jq -r '.tasks[] | select(.status=="in_progress") | "  [\(.id)] \(.title) (开始：\(.started_at))"' "$TASK_LOG" 2>/dev/null || echo "  (无)"
    
    echo ""
    
    # 已完成任务（最近 5 个）
    echo -e "${GREEN}✅ 已完成 (DONE):${NC}"
    jq -r '.tasks[] | select(.status=="done") | "  [\(.id)] \(.title) (完成：\(.completed_at))"' "$TASK_LOG" 2>/dev/null | tail -5 || echo "  (无)"
    
    echo ""
    stats
}

# 添加任务
add_task() {
    local title="$1"
    
    if [ -z "$title" ]; then
        echo -e "${RED}错误：请提供任务标题${NC}"
        exit 1
    fi
    
    init_task_log
    local id=$(generate_id "TASK")
    local timestamp=$(date -Iseconds)
    
    # 添加任务到日志
    local tmp_file=$(mktemp)
    jq --arg id "$id" \
       --arg title "$title" \
       --arg ts "$timestamp" \
       '.tasks += [{"id":$id,"title":$title,"status":"todo","created_at":$ts}]' \
       "$TASK_LOG" > "$tmp_file" && mv "$tmp_file" "$TASK_LOG"
    
    echo -e "${GREEN}✅ 任务已添加${NC}"
    echo "  ID: $id"
    echo "  标题：$title"
    echo "  创建时间：$timestamp"
    
    # 同步到 HEARTBEAT.md
    sync_to_heartbeat "$id" "$title"
}

# 开始任务
start_task() {
    local id="$1"
    
    if [ -z "$id" ]; then
        echo -e "${RED}错误：请提供任务 ID${NC}"
        exit 1
    fi
    
    init_task_log
    local timestamp=$(date -Iseconds)
    local tmp_file=$(mktemp)
    
    # 更新任务状态
    jq --arg id "$id" \
       --arg ts "$timestamp" \
       '.tasks = [.tasks[] | if .id == $id then .status = "in_progress" | .started_at = $ts else . end]' \
       "$TASK_LOG" > "$tmp_file" && mv "$tmp_file" "$TASK_LOG"
    
    echo -e "${GREEN}✅ 任务已开始${NC}"
    echo "  ID: $id"
    echo "  开始时间：$timestamp"
}

# 完成任务
complete_task() {
    local id="$1"
    
    if [ -z "$id" ]; then
        echo -e "${RED}错误：请提供任务 ID${NC}"
        exit 1
    fi
    
    init_task_log
    local timestamp=$(date -Iseconds)
    local tmp_file=$(mktemp)
    
    # 更新任务状态
    jq --arg id "$id" \
       --arg ts "$timestamp" \
       '.tasks = [.tasks[] | if .id == $id then .status = "done" | .completed_at = $ts else . end]' \
       "$TASK_LOG" > "$tmp_file" && mv "$tmp_file" "$TASK_LOG"
    
    echo -e "${GREEN}✅ 任务已完成${NC}"
    echo "  ID: $id"
    echo "  完成时间：$timestamp"
    
    # 从 HEARTBEAT.md 移除
    remove_from_heartbeat "$id"
}

# 删除任务
remove_task() {
    local id="$1"
    
    if [ -z "$id" ]; then
        echo -e "${RED}错误：请提供任务 ID${NC}"
        exit 1
    fi
    
    init_task_log
    local tmp_file=$(mktemp)
    
    jq --arg id "$id" '.tasks = [.tasks[] | select(.id != $id)]' "$TASK_LOG" > "$tmp_file" && mv "$tmp_file" "$TASK_LOG"
    
    echo -e "${GREEN}✅ 任务已删除${NC}"
    echo "  ID: $id"
}

# 搜索任务
search_tasks() {
    local query="$1"
    
    if [ -z "$query" ]; then
        echo -e "${RED}错误：请提供搜索关键词${NC}"
        exit 1
    fi
    
    init_task_log
    
    echo -e "${BLUE}=== 搜索结果：'$query' ===${NC}\n"
    
    jq -r --arg q "$query" '.tasks[] | select(.title | contains($q)) | "[\(.status)] [\(.id)] \(.title)"' "$TASK_LOG" 2>/dev/null || echo "(无匹配)"
}

# 显示统计
stats() {
    init_task_log
    
    local total=$(jq '.tasks | length' "$TASK_LOG" 2>/dev/null || echo 0)
    local todo=$(jq '[.tasks[] | select(.status=="todo")] | length' "$TASK_LOG" 2>/dev/null || echo 0)
    local in_progress=$(jq '[.tasks[] | select(.status=="in_progress")] | length' "$TASK_LOG" 2>/dev/null || echo 0)
    local done=$(jq '[.tasks[] | select(.status=="done")] | length' "$TASK_LOG" 2>/dev/null || echo 0)
    
    echo -e "${BLUE}=== 任务统计 ===${NC}"
    echo "  总计：$total"
    echo -e "  ${YELLOW}待办${NC}: $todo"
    echo -e "  ${BLUE}执行中${NC}: $in_progress"
    echo -e "  ${GREEN}已完成${NC}: $done"
}

# 同步到 HEARTBEAT.md
sync_to_heartbeat() {
    local id="$1"
    local title="$2"
    
    local heartbeat_file="${OPENCLAW_HOME:-$HOME/.openclaw}/workspace/HEARTBEAT.md"
    
    if [ -f "$heartbeat_file" ]; then
        # 检查是否已存在
        if ! grep -q "$id" "$heartbeat_file"; then
            # 添加到待办表格
            local timestamp=$(date +%Y-%m-%d)
            sed -i "/^| 编号 | 任务 | 状态 | 下一步 | 截止 |$/a | **$id** | **$title** | 🟡 待执行 | - | $timestamp |" "$heartbeat_file" 2>/dev/null || true
        fi
    fi
}

# 从 HEARTBEAT.md 移除
remove_from_heartbeat() {
    local id="$1"
    
    local heartbeat_file="${OPENCLAW_HOME:-$HOME/.openclaw}/workspace/HEARTBEAT.md"
    
    if [ -f "$heartbeat_file" ]; then
        sed -i "/$id/d" "$heartbeat_file" 2>/dev/null || true
    fi
}

# 主程序
main() {
    local command="${1:-help}"
    
    case "$command" in
        list|ls|l)
            list_tasks
            ;;
        add|a)
            add_task "$2"
            ;;
        start|s)
            start_task "$2"
            ;;
        complete|done|c)
            complete_task "$2"
            ;;
        remove|rm|del)
            remove_task "$2"
            ;;
        search|find)
            search_tasks "$2"
            ;;
        stats)
            stats
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}未知命令：$command${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
