#!/usr/bin/env python3
"""
自动进度汇报脚本 v4 - Python 版本
每 5 分钟自动发送进度更新到微信
"""

import json
import time
import subprocess
from datetime import datetime

PROGRESS_FILE = "/tmp/cli-progress.json"
LOG_FILE = "/tmp/progress-report.log"
TARGET = "o9cq80-xCy8pt54Dz3jqOJHAgVZ8@im.wechat"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def send_progress():
    try:
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
        
        percent = data.get("percent", 0)
        step = data.get("step", "未知")
        status = data.get("status", "未知")
        elapsed = data.get("elapsed_minutes", 0)
        
        # 生成进度条
        filled = percent // 5
        empty = 20 - filled
        bar = "█" * filled + "░" * empty
        
        # 生成消息
        msg = f"""╔═══════════════════════════════════════════════════════════╗
║  CLI-Anything 集成进度                      14:30 开始    ║
╠═══════════════════════════════════════════════════════════╣
║  [{bar}] {percent}%  Step {percent//20}/5                    ║
╠═══════════════════════════════════════════════════════════╣
║  当前任务：{step}
║  状态：{status}
║  耗时：{elapsed} 分钟 / 预计 120 分钟
╠═══════════════════════════════════════════════════════════╣
║  🤖 自动汇报 · 每 5 分钟更新 · 后台进程运行中
╚═══════════════════════════════════════════════════════════╝"""
        
        # 发送消息
        result = subprocess.run(
            ["openclaw", "message", "send", "--channel", "openclaw-weixin", "--target", TARGET, "--message", msg],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            log(f"✅ 进度汇报发送成功：{percent}%")
            return True
        else:
            log(f"❌ 进度汇报发送失败：{result.stderr}")
            return False
            
    except Exception as e:
        log(f"❌ 错误：{e}")
        return False

def main():
    log("🚀 自动进度汇报 v4 (Python) 启动")
    
    # 立即发送一次
    log("发送首次汇报...")
    send_progress()
    
    # 然后每 5 分钟发送
    while True:
        time.sleep(300)  # 5 分钟
        log("定时汇报时间到...")
        send_progress()

if __name__ == "__main__":
    main()
