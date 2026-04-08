#!/usr/bin/env python3
"""
全通道自动汇报系统 v1
支持微信、Telegram、飞书三个通道
每 5 分钟自动发送项目进度汇报
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
PROGRESS_FILE = Path("/tmp/cli-progress.json")
LOG_FILE = Path("/tmp/auto-report.log")

# 项目状态文件映射
PROJECTS = {
    "CLI-Anything 集成": "/tmp/cli-progress.json",
    "TimesFM 集成": "/tmp/timesfm-status.json",
    "情景模式系统": "/tmp/scenario-api-status.json",
    "知几-E 气象套利": "/tmp/zhiji-weather-status.json",
    "山木研报生成": "/tmp/shanmu-report-status.json",
    "鲸鱼追踪器": "/tmp/whale-tracker-status.json",
}

# 通道配置
CHANNELS = [
    {
        "name": "微信",
        "channel": "openclaw-weixin",
        "target": "o9cq80-xCy8pt54Dz3jqOJHAgVZ8@im.wechat",
        "enabled": True
    },
    {
        "name": "Telegram",
        "channel": "telegram",
        "target": "7073481596",  # @nicola king
        "enabled": True
    },
    {
        "name": "飞书",
        "channel": "feishu",
        "target": "cli_a9086d6b5779dcc1",  # 太一 AppID
        "enabled": False  # 暂时禁用，待配置正确的 chatId
    }
]

def log(message):
    """写日志"""
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def get_project_status(name, status_file):
    """读取项目状态"""
    try:
        path = Path(status_file)
        if not path.exists():
            return {"status": "⏳ 未启动", "progress": 0, "details": "状态文件不存在"}
        
        with open(path, "r") as f:
            data = json.load(f)
        
        return {
            "status": data.get("status", "未知"),
            "progress": data.get("progress", data.get("percent", 0)),
            "details": data.get("details", data.get("step", "未知"))
        }
    except Exception as e:
        return {"status": f"❌ 错误", "progress": 0, "details": str(e)}

def generate_report():
    """生成多项目进度报告"""
    lines = []
    lines.append("╔═══════════════════════════════════════════════════════════╗")
    lines.append("║  全通道自动进度汇报                      太一 AGI         ║")
    lines.append(f"║  更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}                          ║")
    lines.append("╠═══════════════════════════════════════════════════════════╣")
    
    for name, status_file in PROJECTS.items():
        status = get_project_status(name, status_file)
        progress = min(100, int(status["progress"]))
        filled = progress // 5
        empty = 20 - filled
        # 淡蓝色进度条 (使用 ANSI 转义码或 Unicode 浅色字符)
        # 方案：使用浅蓝色方块 ░▒▓█ 渐变
        bar = "▓" * filled + "░" * empty  # 使用浅色方块
        
        # 状态图标
        if "✅" in status["status"] or "完成" in status["status"]:
            icon = "✅"
        elif "❌" in status["status"]:
            icon = "❌"
        elif "🔄" in status["status"] or "执行中" in status["status"]:
            icon = "🔄"
        else:
            icon = "⏳"
        
        short_name = name[:12].ljust(12)
        lines.append(f"║  {icon} {short_name} [{bar}] {progress:3d}%  ║")
        detail_val = status.get("details", status.get("step", "未知"))
        if isinstance(detail_val, dict):
            detail_val = str(detail_val.get("next", detail_val.get("step", "未知")))
        detail = str(detail_val)[:35].ljust(35)
        lines.append(f"║     {detail}  ║")
    
    lines.append("╠═══════════════════════════════════════════════════════════╣")
    lines.append("║  🤖 全自动汇报 · 每 5 分钟更新 · 三通道同步                  ║")
    lines.append("╚═══════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)

def send_message(channel, target, message):
    """发送消息到指定通道"""
    try:
        cmd = [
            "openclaw", "message", "send",
            "--channel", channel,
            "--target", target,
            "--message", message
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            log(f"✅ {channel} 发送成功")
            return True
        else:
            log(f"❌ {channel} 发送失败：{result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"❌ {channel} 异常：{e}")
        return False

def main():
    log("🚀 全通道自动汇报系统启动")
    
    # 生成报告
    report = generate_report()
    log(f"生成报告：{len(report)} 字符")
    
    # 发送到所有通道
    success_count = 0
    for channel_config in CHANNELS:
        if not channel_config["enabled"]:
            log(f"⏭️  跳过 {channel_config['name']} (未启用)")
            continue
        
        success = send_message(
            channel_config["channel"],
            channel_config["target"],
            report
        )
        if success:
            success_count += 1
    
    log(f"✅ 发送完成：{success_count}/{len(CHANNELS)} 通道成功")
    return success_count > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
