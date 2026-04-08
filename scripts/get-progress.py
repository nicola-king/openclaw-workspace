#!/usr/bin/env python3
"""
自动进度汇报脚本 v6 - 读取进度文件并输出消息
由 cron 任务调用，输出到 stdout，由 cron 的 --announce 发送
"""

import json
from datetime import datetime

PROGRESS_FILE = "/tmp/cli-progress.json"

def get_progress():
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
║  🤖 自动汇报 · 每 5 分钟更新 · cron 调度
╚═══════════════════════════════════════════════════════════╝"""
        
        return msg
        
    except Exception as e:
        return f"⚠️ 读取进度失败：{e}"

if __name__ == "__main__":
    print(get_progress())
