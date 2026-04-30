#!/bin/bash
# 即梦 CLI 安装脚本
set -euo pipefail

PROGRAM_NAME="dreamina"
DOWNLOAD_BASE="https://lf3-static.bytednsdoc.com/obj/eden-cn/psj_hupthlyk/ljhwZthlaukjlkulzlp/dreamina_cli_beta"

say() { printf '%s\n' "$*"; }
fail() { printf 'install.sh: %s\n' "$*" >&2; exit 1; }

has_command() { command -v "$1" >/dev/null 2>&1; }

download_file() {
  url="$1"; output="$2"
  if has_command curl; then curl -fsSL "$url" -o "$output"; return; fi
  if has_command wget; then wget -qO "$output" "$url"; return; fi
  fail "需要 curl 或 wget"
}

detect_os_arch() {
  os=$(uname -s | tr '[:upper:]' '[:lower:]')
  arch=$(uname -m)
  case "$arch" in x86_64) arch="amd64" ;; aarch64|arm64) arch="arm64" ;; esac
  case "$os" in linux) ;; darwin) os="darwin" ;; esac
  echo "${os}-${arch}"
}

main() {
  say "正在安装即梦 CLI..."
  mkdir -p "${HOME}/.dreamina_cli/bin"
  platform=$(detect_os_arch)
  say "平台：$platform"
  
  binary_url="${DOWNLOAD_BASE}/dreamina-${platform}"
  say "下载：$binary_url"
  download_file "$binary_url" "${HOME}/.dreamina_cli/bin/dreamina"
  chmod +x "${HOME}/.dreamina_cli/bin/dreamina"
  
  if ! grep -q "dreamina_cli/bin" "${HOME}/.bashrc" 2>/dev/null; then
    echo 'export PATH="${HOME}/.dreamina_cli/bin:$PATH"' >> "${HOME}/.bashrc"
  fi
  
  if "${HOME}/.dreamina_cli/bin/dreamina" --version >/dev/null 2>&1; then
    say "✅ 即梦 CLI 安装成功"
    say "使用：dreamina --help"
  else
    say "⚠️  安装完成但版本测试失败（可能需要登录）"
  fi
}

main "$@"
