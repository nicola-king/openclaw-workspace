#!/usr/bin/env bash
#
# lint-agents.sh -- 太一 Agent 质量检查
#
# 检查内容:
# 1. 必要字段 (name/description/vibe)
# 2. 代码示例 (至少 1 个代码块)
# 3. 成功指标 (量化标准)
# 4. 可读性 (标题层级/列表格式)
#
# Usage:
#   ./scripts/lint-agents.sh [directory]
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

ok()   { printf "${C_GREEN}✓${C_RESET}  %s\n" "$*"; }
warn() { printf "${C_YELLOW}⚠${C_RESET}  %s\n" "$*"; }
err()  { printf "${C_RED}✗${C_RESET} %s\n" "$*" >&2; }

# 统计
total=0
passed=0
failed=0
warnings=0

# ---------------------------------------------------------------------------
# 检查函数
# ---------------------------------------------------------------------------

check_required_fields() {
  local file="$1"
  local content
  content=$(cat "$file")
  
  # 检查 name
  if ! grep -q "^name:" "$file" && ! grep -q "^#.*Agent" "$file"; then
    err "缺少 name 字段：$file"
    return 1
  fi
  
  # 检查 description
  if ! grep -q "description:" "$file" && ! grep -q "职责" "$file"; then
    warn "缺少 description: $file"
    ((warnings++))
  fi
  
  # 检查 vibe/风格
  if ! grep -q "vibe:" "$file" && ! grep -q "风格" "$file"; then
    warn "缺少 vibe 描述：$file"
    ((warnings++))
  fi
  
  return 0
}

check_code_examples() {
  local file="$1"
  
  # 检查代码块
  if ! grep -q '```' "$file"; then
    warn "缺少代码示例：$file"
    ((warnings++))
    return 0
  fi
  
  # 检查代码块数量
  local count
  count=$(grep -c '```' "$file" || true)
  if (( count < 2 )); then
    warn "代码示例较少 (<1 个完整代码块): $file"
    ((warnings++))
  fi
  
  return 0
}

check_success_metrics() {
  local file="$1"
  
  # 检查成功指标
  if ! grep -q "成功指标\|Success Metrics\|✅" "$file"; then
    warn "缺少成功指标：$file"
    ((warnings++))
    return 0
  fi
  
  return 0
}

check_readability() {
  local file="$1"
  
  # 检查标题层级
  if ! grep -q '^##' "$file"; then
    warn "缺少二级标题：$file"
    ((warnings++))
  fi
  
  # 检查列表
  if ! grep -q '^[-*]' "$file" && ! grep -q '^[0-9]\.' "$file"; then
    warn "缺少列表：$file"
    ((warnings++))
  fi
  
  return 0
}

# ---------------------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------------------

main() {
  local dir="${1:-/home/nicola/.openclaw/workspace/skills}"
  
  echo "🔍 开始检查 Agent 质量..."
  echo "目录：$dir"
  echo ""
  
  # 查找所有 Markdown 文件
  while IFS= read -r -d '' file; do
    ((total++))
    
    local filename
    filename=$(basename "$file")
    
    # 跳过不相关的文件
    if [[ "$filename" == "README.md" ]] || \
       [[ "$filename" == "CHANGELOG.md" ]] || \
       [[ "$filename" == "CONTRIBUTING.md" ]]; then
      continue
    fi
    
    # 执行检查
    local errors=0
    
    check_required_fields "$file" || ((errors++))
    check_code_examples "$file" || ((errors++))
    check_success_metrics "$file" || ((errors++))
    check_readability "$file" || ((errors++))
    
    if (( errors == 0 )); then
      ok "通过：$filename"
      ((passed++))
    else
      err "未通过：$filename"
      ((failed++))
    fi
    
  done < <(find "$dir" -name "*.md" -type f -print0)
  
  # 汇总
  echo ""
  echo "═══════════════════════════════════════"
  echo "检查结果汇总"
  echo "═══════════════════════════════════════"
  echo "总计：$total 个文件"
  echo "通过：$passed 个 ${C_GREEN}✓${C_RESET}"
  echo "未通过：$failed 个 ${C_RED}✗${C_RESET}"
  echo "警告：$warnings 个 ${C_YELLOW}⚠${C_RESET}"
  echo ""
  
  if (( failed > 0 )); then
    exit 1
  else
    ok "所有 Agent 质量检查通过！"
    exit 0
  fi
}

main "$@"
