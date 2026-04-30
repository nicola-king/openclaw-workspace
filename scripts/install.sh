#!/usr/bin/env bash
#
# install.sh -- 安装太一 Agent 到本地工具
#
# 支持工具：OpenClaw / Claude Code / Cursor / Copilot
#
# Usage:
#   ./scripts/install.sh [--tool <name>] [--interactive] [--help]
#
# Tools:
#   openclaw     -- 安装到 ~/.openclaw/workspace/skills/
#   claude-code  -- 安装到 ~/.claude/agents/
#   cursor       -- 安装到 .cursor/rules/
#   copilot      -- 安装到 ~/.github/copilot/
#   all          -- 安装到所有检测到的工具 (默认)
#

set -euo pipefail

# 颜色
if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
  C_GREEN='\033[0;32m'
  C_YELLOW='\033[1;33m'
  C_RED='\033[0;31m'
  C_CYAN='\033[0;36m'
  C_RESET='\033[0m'
else
  C_GREEN=''; C_YELLOW=''; C_RED=''; C_CYAN=''; C_RESET=''
fi

ok()   { printf "${C_GREEN}[OK]${C_RESET}  %s\n" "$*"; }
warn() { printf "${C_YELLOW}[!!]${C_RESET}  %s\n" "$*"; }
err()  { printf "${C_RED}[ERR]${C_RESET} %s\n" "$*" >&2; }
header() { printf "\n${C_BOLD}%s${C_RESET}\n" "$*"; }

# 路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/home/nicola/.openclaw/workspace"

# ---------------------------------------------------------------------------
# 安装函数
# ---------------------------------------------------------------------------

install_openclaw() {
  header "🤖 安装到 OpenClaw"
  
  # 创建目标目录
  mkdir -p ~/.openclaw/agency-agents
  
  # 复制 Agent 文件
  cp -r "$WORKSPACE_DIR/skills" ~/.openclaw/agency-agents/
  cp -r "$WORKSPACE_DIR/agents" ~/.openclaw/agency-agents/
  
  ok "已安装到 ~/.openclaw/agency-agents/"
  ok "重启 Gateway: openclaw gateway restart"
}

install_claude_code() {
  header "🎭 安装到 Claude Code"
  
  mkdir -p ~/.claude/agents
  
  # 复制 Engineering Agent
  if [[ -d "/tmp/agency-agents/engineering" ]]; then
    cp /tmp/agency-agents/engineering/*.md ~/.claude/agents/
    ok "已安装 Engineering Agents"
  fi
  
  # 复制 Design Agent
  if [[ -d "/tmp/agency-agents/design" ]]; then
    cp /tmp/agency-agents/design/*.md ~/.claude/agents/
    ok "已安装 Design Agents"
  fi
  
  ok "已安装到 ~/.claude/agents/"
}

install_cursor() {
  header "🔍 安装到 Cursor"
  
  mkdir -p .cursor/rules
  
  # 生成 Cursor rules
  cat > .cursor/rules/taiyi-agents.mdc << 'EOF'
# 太一 Agent 规则

## 可用 Agent
- 知几 (数据分析)
- 山木 (业务执行)
- 素问 (技术研究)
- 罔两 (市场情报)
- 庖丁 (财务管控)

## 使用方式
激活特定 Agent: "使用 [Agent 名] 模式处理这个任务"
EOF
  
  ok "已安装到 .cursor/rules/"
}

install_copilot() {
  header "🤖 安装到 GitHub Copilot"
  
  mkdir -p ~/.github/copilot
  
  # 复制 Agent 配置
  if [[ -d "$WORKSPACE_DIR/constitution/agents" ]]; then
    cp -r "$WORKSPACE_DIR/constitution/agents" ~/.github/copilot/
    ok "已安装 Agent 配置"
  fi
  
  ok "已安装到 ~/.github/copilot/"
}

# ---------------------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------------------

main() {
  local tool="${1:-all}"
  
  case "$tool" in
    openclaw)
      install_openclaw
      ;;
    claude-code)
      install_claude_code
      ;;
    cursor)
      install_cursor
      ;;
    copilot)
      install_copilot
      ;;
    all)
      install_openclaw
      install_claude_code
      install_cursor
      install_copilot
      ;;
    *)
      echo "用法：$0 [--tool <name>]"
      echo "工具：openclaw, claude-code, cursor, copilot, all"
      exit 1
      ;;
  esac
  
  echo ""
  ok "✅ 安装完成！"
}

main "$@"
