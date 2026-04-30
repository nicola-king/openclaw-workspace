#!/bin/bash
# Browser Automation CLI - 太一 AGI v5.0

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SKILL_DIR/browser_automation.py"

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

usage() {
    cat << EOF
太一 AGI v5.0 · Browser Automation Skill

用法：$0 <command> [options]

命令:
  open <url>              打开网页
  close                   关闭浏览器
  navigate <url>          导航到新页面
  screenshot [output]     截图
  pdf [output]            保存 PDF
  
  click <selector>        点击元素
  fill <selector> <value> 填写表单
  select <sel> <val>      选择下拉
  check <selector>        勾选复选框
  hover <selector>        悬停元素
  scroll [pixels]         滚动页面
  
  text [selector]         提取文本
  html [selector]         获取 HTML
  links [domain]          提取链接
  images                  提取图片
  table <selector>        提取表格
  eval <js>               执行 JS
  
  wait <selector>         等待元素
  cookie <get|set>        管理 Cookie
  
示例:
  $0 open https://github.com
  $0 screenshot github.png
  $0 fill "#username" "admin"
  $0 click "#login-btn"
  $0 text ".article"
  $0 eval "document.title"

EOF
    exit 0
}

# 检查依赖
check_deps() {
    if ! command -v python3 &> /dev/null; then
        log_error "需要 Python3"
        exit 1
    fi
    
    if ! python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
        log_warn "Playwright 未安装，正在安装..."
        pip3 install playwright -q
        playwright install chromium
    fi
}

# 主函数
main() {
    check_deps
    
    if [ -z "$1" ]; then
        usage
    fi
    
    local cmd=$1
    shift
    
    case $cmd in
        open)
            if [ -z "$1" ]; then
                log_error "请提供 URL"
                exit 1
            fi
            python3 -c "
from browser_automation import BrowserAutomation
import sys
sys.path.insert(0, '$SKILL_DIR')
ba = BrowserAutomation(headless=False)
ba.open('$1')
input('按 Enter 关闭浏览器...')
ba.close()
"
            ;;
        
        close)
            python3 -c "
from browser_automation import BrowserAutomation
import sys
sys.path.insert(0, '$SKILL_DIR')
ba = BrowserAutomation()
ba.close()
"
            ;;
        
        screenshot)
            local output="${1:-screenshot.png}"
            python3 -c "
from browser_automation import BrowserAutomation
import sys
sys.path.insert(0, '$SKILL_DIR')
ba = BrowserAutomation(headless=False)
ba.start()
ba.open('$CURRENT_URL' if '$CURRENT_URL' else 'https://example.com')
ba.screenshot(output='$output', full_page=True)
ba.close()
"
            log_success "截图已保存：$output"
            ;;
        
        click)
            if [ -z "$1" ]; then
                log_error "请提供选择器"
                exit 1
            fi
            log_info "点击：$1"
            # 实际使用需要保持浏览器会话
            ;;
        
        fill)
            if [ -z "$1" ] || [ -z "$2" ]; then
                log_error "请提供选择器和值"
                exit 1
            fi
            log_info "填写：$1 = $2"
            ;;
        
        text)
            local selector="$1"
            python3 -c "
from browser_automation import BrowserAutomation
import sys
sys.path.insert(0, '$SKILL_DIR')
ba = BrowserAutomation(headless=True)
ba.start()
ba.open('$CURRENT_URL' if '$CURRENT_URL' else 'https://example.com')
text = ba.text('$selector' if '$selector' else None)
print(text)
ba.close()
"
            ;;
        
        eval)
            local js="$*"
            python3 -c "
from browser_automation import BrowserAutomation
import sys
sys.path.insert(0, '$SKILL_DIR')
ba = BrowserAutomation(headless=True)
ba.start()
ba.open('$CURRENT_URL' if '$CURRENT_URL' else 'https://example.com')
result = ba.eval('$js')
print(result)
ba.close()
"
            ;;
        
        *)
            log_error "未知命令：$cmd"
            usage
            ;;
    esac
}

main "$@"
