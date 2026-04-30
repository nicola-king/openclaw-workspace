#!/bin/bash
# install-github-scraper.sh - GitHub 开源爬虫安装脚本
# 等级：Tier 1 · 永久核心
# 创建：2026-04-01 20:58

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"
}

log_info "=========================================="
log_info "GitHub 开源爬虫安装脚本"
log_info "=========================================="

# 检查 Python 版本
log_info "检查 Python 版本..."
python3 --version || {
    log_error "Python3 未安装，请先安装 Python 3.8+"
    exit 1
}

# 检查 pip
log_info "检查 pip..."
pip3 --version || {
    log_error "pip3 未安装，请先安装 pip"
    exit 1
}

# 创建虚拟环境 (用户目录)
VENV_DIR="$HOME/github-scraper-venv"
if [ ! -d "$VENV_DIR" ]; then
    log_info "创建虚拟环境：$VENV_DIR"
    python3 -m venv "$VENV_DIR" || {
        log_warning "虚拟环境创建失败，尝试使用 --break-system-packages"
        VENV_DIR=""
    }
else
    log_info "虚拟环境已存在：$VENV_DIR"
fi

# 激活虚拟环境
if [ -n "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    log_success "虚拟环境已激活"
fi

# 升级 pip
log_info "升级 pip..."
python -m pip install --upgrade pip --quiet

# 安装 Scrapling
log_info "安装 Scrapling (Cloudflare bypass)..."
if [ -n "$VENV_DIR" ]; then
    pip install scrapling --upgrade || {
        log_error "Scrapling 安装失败"
        exit 1
    }
else
    pip install scrapling --upgrade --break-system-packages || {
        log_error "Scrapling 安装失败"
        exit 1
    }
fi
log_success "Scrapling 安装完成"

# 安装 cloudscraper
log_info "安装 cloudscraper (Cloudflare 专用)..."
if [ -n "$VENV_DIR" ]; then
    pip install cloudscraper --upgrade || {
        log_error "cloudscraper 安装失败"
        exit 1
    }
else
    pip install cloudscraper --upgrade --break-system-packages || {
        log_error "cloudscraper 安装失败"
        exit 1
    }
fi
log_success "cloudscraper 安装完成"

# 安装 undetected-chromedriver (可选)
log_info "安装 undetected-chromedriver (Selenium 增强)..."
if [ -n "$VENV_DIR" ]; then
    pip install undetected-chromedriver --upgrade || {
        log_warning "undetected-chromedriver 安装失败 (可选)"
    }
else
    pip install undetected-chromedriver --upgrade --break-system-packages || {
        log_warning "undetected-chromedriver 安装失败 (可选)"
    }
fi
log_success "undetected-chromedriver 安装完成"

# 安装 SeleniumBase (可选)
log_info "安装 SeleniumBase (一体化方案)..."
if [ -n "$VENV_DIR" ]; then
    pip install seleniumbase --upgrade || {
        log_warning "SeleniumBase 安装失败 (可选)"
    }
else
    pip install seleniumbase --upgrade --break-system-packages || {
        log_warning "SeleniumBase 安装失败 (可选)"
    }
fi
log_success "SeleniumBase 安装完成"

# 安装 camoufox (可选)
log_info "安装 camoufox (Firefox 方案)..."
if [ -n "$VENV_DIR" ]; then
    pip install camoufox --upgrade || {
        log_warning "camoufox 安装失败 (可选)"
    }
else
    pip install camoufox --upgrade --break-system-packages || {
        log_warning "camoufox 安装失败 (可选)"
    }
fi
log_success "camoufox 安装完成"

# 安装 patchright (可选)
log_info "安装 patchright (Playwright 增强)..."
if [ -n "$VENV_DIR" ]; then
    pip install patchright --upgrade || {
        log_warning "patchright 安装失败 (可选)"
    }
else
    pip install patchright --upgrade --break-system-packages || {
        log_warning "patchright 安装失败 (可选)"
    }
fi
log_success "patchright 安装完成"

# 安装依赖
log_info "安装通用依赖..."
if [ -n "$VENV_DIR" ]; then
    pip install requests beautifulsoup4 lxml --upgrade || {
        log_warning "通用依赖安装失败"
    }
else
    pip install requests beautifulsoup4 lxml --upgrade --break-system-packages || {
        log_warning "通用依赖安装失败"
    }
fi
log_success "通用依赖安装完成"

# 验证安装
log_info "验证安装..."

python3 -c "from scrapling import StealthyFetcher; print('Scrapling: ✅')" || log_error "Scrapling 验证失败"
python3 -c "import cloudscraper; print('cloudscraper: ✅')" || log_error "cloudscraper 验证失败"
python3 -c "import undetected_chromedriver; print('undetected-chromedriver: ✅')" 2>/dev/null || log_warning "undetected-chromedriver 验证失败"
python3 -c "from seleniumbase import Driver; print('SeleniumBase: ✅')" 2>/dev/null || log_warning "SeleniumBase 验证失败"

log_success "=========================================="
log_success "GitHub 开源爬虫安装完成！"
log_success "=========================================="

# 显示使用说明
echo ""
echo "使用示例:"
echo "  python3 scripts/multi-channel-scraper.py"
echo ""
echo "快速测试:"
echo "  python3 -c \"from scrapling import StealthyFetcher; print(StealthyFetcher().fetch('https://httpbin.org/html').status)\""
echo ""
echo "配置文件:"
echo "  constitution/directives/GITHUB-OPEN-SCRAPER.md"
echo ""

# 退出虚拟环境
if [ -n "$VENV_DIR" ]; then
    deactivate
fi

exit 0
