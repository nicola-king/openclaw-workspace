#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 图片下载问题 - 自主检查自愈脚本
功能：检测代理配置、Clash 状态、Telegram CDN 连接，自动修复
"""

import subprocess
import sys
import os
import time
from datetime import datetime

# 颜色定义
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
CHAT_ID = "7073481596"
CLASH_DIR = "/home/nicola/clash"
CLASH_PORT = 7890

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime('%H:%M:%S')
    color = {"OK": GREEN, "FAIL": RED, "WARN": YELLOW, "INFO": BLUE, "FIX": GREEN}.get(level, "")
    print(f"{color}[{timestamp}] [{level}] {msg}{NC}")

def run_cmd(cmd, shell=True, timeout=10):
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def check_clash():
    """检查 Clash 状态"""
    log("检查 Clash 进程...", "INFO")
    success, output = run_cmd("pgrep -x clash")
    if success and output.strip():
        log(f"Clash 运行中 (PID: {output.strip()})", "OK")
        return True
    log("Clash 未运行", "FAIL")
    return False

def check_port():
    """检查 7890 端口监听"""
    log(f"检查端口 {CLASH_PORT}...", "INFO")
    success, output = run_cmd(f"ss -tuln | grep ':{CLASH_PORT}' || netstat -tuln | grep ':{CLASH_PORT}'")
    if success and output.strip():
        log(f"端口 {CLASH_PORT} 监听中", "OK")
        return True
    log(f"端口 {CLASH_PORT} 未监听", "FAIL")
    return False

def check_no_proxy():
    """检查 NO_PROXY 配置"""
    log("检查 NO_PROXY 配置...", "INFO")
    no_proxy = os.environ.get('NO_PROXY', '') + ',' + os.environ.get('no_proxy', '')
    if 'telegram-cdn' in no_proxy.lower():
        log("NO_PROXY 错误包含 telegram-cdn", "FAIL")
        return False
    log("NO_PROXY 配置正确", "OK")
    return True

def check_telegram_api():
    """检查 Telegram Bot API"""
    log("检查 Telegram Bot API...", "INFO")
    start = time.time()
    success, output = run_cmd(f'curl -s "https://api.telegram.org/bot{BOT_TOKEN}/getMe" --connect-timeout 10')
    latency = int((time.time() - start) * 1000)
    if success and '"ok":true' in output:
        log(f"Bot API 正常 ({latency}ms)", "OK")
        return True
    log("Bot API 失败", "FAIL")
    return False

def check_cdn(domain):
    """检查 Telegram CDN 连接"""
    log(f"检查 {domain}...", "INFO")
    start = time.time()
    success, output = run_cmd(f'curl -sI "{domain}" --connect-timeout 5 -x "http://127.0.0.1:{CLASH_PORT}" 2>/dev/null | head -1')
    latency = int((time.time() - start) * 1000)
    if success and ('200' in output or '302' in output):
        log(f"{domain} 正常 ({latency}ms)", "OK")
        return True
    log(f"{domain} 失败", "FAIL")
    return False

def fix_no_proxy():
    """修复 NO_PROXY"""
    log("修复 NO_PROXY...", "FIX")
    new_no_proxy = "localhost,127.0.0.0/8,::1"
    
    # 当前会话
    os.environ['NO_PROXY'] = new_no_proxy
    os.environ['no_proxy'] = new_no_proxy
    
    # 永久修复
    run_cmd(f'grep -q "export NO_PROXY" ~/.bashrc && sed -i "/export NO_PROXY/d" ~/.bashrc; echo "export NO_PROXY=\\"{new_no_proxy}\\"" >> ~/.bashrc')
    run_cmd(f'grep -q "export no_proxy" ~/.bashrc && sed -i "/export no_proxy/d" ~/.bashrc; echo "export no_proxy=\\"$NO_PROXY\\"" >> ~/.bashrc')
    
    log("NO_PROXY 已修复 (当前会话 + ~/.bashrc)", "OK")
    return True

def fix_clash_config():
    """修复 Clash 配置中的错误代理组引用"""
    log("修复 Clash 配置...", "FIX")
    
    config_path = f"{CLASH_DIR}/config.yaml"
    if not os.path.exists(config_path):
        log("配置文件不存在", "FAIL")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 错误代理组映射
        fallback_map = {
            '☁️ OneDrive': '🎯 全球直连',
            '🪟 Windows 更新': '🎯 全球直连',
            '🍎 Apple 服务': '🎯 全球直连',
            '🎵 TikTok': '🌍 国外网站',
            '🐦 Twitter': '🌍 国外网站',
            '📸 Instagram': '🌍 国外网站',
            '📹 YouTube': '🌍 国外网站',
            '🎮 游戏平台': '🎯 全球直连',
            '📲 Telegram': '🌍 国外网站',
            '💬 Discord': '🌍 国外网站',
            '🔰 选择节点': '🔰 手动选择',
            '📺 动画疯': '📺 哔哩哔哩',
            '🎮 Steam 登录/下载': '🎯 全球直连',
            '🎮 Steam 商店/社区': '🎯 全球直连',
        }
        
        count = 0
        for old, new in fallback_map.items():
            if old in content:
                content = content.replace(old, new)
                count += 1
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        log(f"修复 {count} 个错误引用", "OK")
        return True
    except Exception as e:
        log(f"修复失败：{e}", "FAIL")
        return False

def start_clash():
    """启动 Clash"""
    log("启动 Clash...", "FIX")
    
    # 停止现有进程
    run_cmd("pkill -x clash 2>/dev/null")
    time.sleep(2)
    
    # 启动
    os.chdir(CLASH_DIR)
    success, output = run_cmd(f"nohup {CLASH_DIR}/clash -d {CLASH_DIR} > /tmp/clash-start.log 2>&1 &")
    time.sleep(5)
    
    if check_clash() and check_port():
        log("Clash 启动成功", "OK")
        return True
    
    log("Clash 启动失败", "FAIL")
    return False

def send_notification(msg):
    """发送 Telegram 通知"""
    log("发送通知...", "INFO")
    run_cmd(f'curl -s "https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" -d "chat_id={CHAT_ID}&text={msg}"')

def main():
    print(f"{BLUE}╔══════════════════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║  Telegram 图片下载 - 自主检查自愈                          ║{NC}")
    print(f"{BLUE}╚══════════════════════════════════════════════════════════╝{NC}")
    print()
    
    issues = []
    fixes = []
    
    # 检查
    log("═══ 开始检查 ═══", "INFO")
    print()
    
    if not check_clash():
        issues.append("Clash 未运行")
    
    if not check_port():
        issues.append("7890 端口未监听")
    
    if not check_no_proxy():
        issues.append("NO_PROXY 配置错误")
    
    if not check_telegram_api():
        issues.append("Telegram Bot API 失败")
    
    # CDN 检查 (仅在 Clash 运行时)
    if check_clash():
        if not check_cdn("https://cdn1.telegram-cdn.org"):
            issues.append("CDN 节点 1 连接失败")
        if not check_cdn("https://cdn2.telegram-cdn.org"):
            issues.append("CDN 节点 2 连接失败")
    
    print()
    
    # 自愈
    if issues:
        log(f"发现 {len(issues)} 个问题: {', '.join(issues)}", "WARN")
        print()
        log("═══ 开始自愈 ═══", "INFO")
        print()
        
        # 修复 NO_PROXY
        if "NO_PROXY 配置错误" in issues:
            if fix_no_proxy():
                fixes.append("NO_PROXY 已修复")
        
        # 修复 Clash 配置并启动
        if "Clash 未运行" in issues or "7890 端口未监听" in issues:
            if fix_clash_config():
                if start_clash():
                    fixes.append("Clash 已启动")
        
        # 验证
        print()
        log("═══ 验证修复 ═══", "INFO")
        print()
        
        if check_clash() and check_port() and check_no_proxy() and check_telegram_api():
            log("✅ 所有问题已修复", "OK")
            send_notification("✅ Telegram 图片下载问题已自动修复")
        else:
            log("⚠️ 部分问题未解决，请手动检查", "WARN")
            send_notification("⚠️ Telegram 图片下载问题自愈失败，需手动干预")
    else:
        log("✅ 所有检查通过", "OK")
    
    print()
    log("═══ 自检完成 ═══", "INFO")

if __name__ == "__main__":
    main()
