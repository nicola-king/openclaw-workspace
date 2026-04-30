#!/usr/bin/env python3
"""
多项目自动汇报生成器 v1
读取各自动执行项目的状态，生成统一进度报告
"""

import json
from datetime import datetime

# 项目状态文件映射
PROJECTS = {
    "知几-E 气象套利": {
        "status_file": "/tmp/zhiji-weather-status.json",
        "type": "quant",
        "priority": "P0"
    },
    "山木研报生成": {
        "status_file": "/tmp/shanmu-report-status.json",
        "type": "content",
        "priority": "P0"
    },
    "鲸鱼追踪器": {
        "status_file": "/tmp/whale-tracker-status.json",
        "type": "data",
        "priority": "P1"
    },
    "CLI-Anything 集成": {
        "status_file": "/tmp/cli-progress.json",
        "type": "dev",
        "priority": "P0"
    },
    "TimesFM 集成": {
        "status_file": "/tmp/timesfm-status.json",
        "type": "dev",
        "priority": "P0"
    },
    "情景模式系统": {
        "status_file": "/tmp/scenario-api-status.json",
        "type": "dev",
        "priority": "P0"
    }
}

def get_project_status(name, config):
    """读取项目状态文件"""
    try:
        with open(config["status_file"], "r") as f:
            data = json.load(f)
        return {
            "name": name,
            "priority": config["priority"],
            "type": config["type"],
            "status": data.get("status", "未知"),
            "progress": data.get("progress", data.get("percent", 0)),
            "details": data.get("details", data.get("step", "未知")),
            "last_update": data.get("last_update", "未知")
        }
    except FileNotFoundError:
        return {
            "name": name,
            "priority": config["priority"],
            "type": config["type"],
            "status": "⏳ 未启动",
            "progress": 0,
            "details": "状态文件不存在",
            "last_update": "-"
        }
    except Exception as e:
        return {
            "name": name,
            "priority": config["priority"],
            "type": config["type"],
            "status": f"❌ 错误",
            "progress": 0,
            "details": str(e),
            "last_update": "-"
        }

def generate_report():
    """生成多项目进度报告"""
    report = []
    
    # 头部
    report.append("╔═══════════════════════════════════════════════════════════╗")
    report.append("║  多项目自动进度汇报                      太一 AGI         ║")
    report.append(f"║  更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}                          ║")
    report.append("╠═══════════════════════════════════════════════════════════╣")
    
    # 按优先级排序
    projects = []
    for name, config in PROJECTS.items():
        projects.append(get_project_status(name, config))
    
    projects.sort(key=lambda x: (0 if x["priority"]=="P0" else 1, x["name"]))
    
    # 项目列表
    for proj in projects:
        # 进度条
        progress = min(100, int(proj["progress"]))
        filled = progress // 5
        empty = 20 - filled
        bar = "█" * filled + "░" * empty
        
        # 状态图标
        if "✅" in proj["status"] or "完成" in proj["status"]:
            icon = "✅"
        elif "❌" in proj["status"] or "错误" in proj["status"]:
            icon = "❌"
        elif "🔄" in proj["status"] or "执行中" in proj["status"]:
            icon = "🔄"
        elif "⏳" in proj["status"] or "未启动" in proj["status"]:
            icon = "⏳"
        else:
            icon = "🟡"
        
        report.append(f"║  {icon} [{proj['priority']}] {proj['name'][:15]:<15} [{bar}] {progress:3d}%  ║")
        report.append(f"║     状态：{proj['status'][:40]:<40}  ║")
    
    report.append("╠═══════════════════════════════════════════════════════════╣")
    report.append("║  🤖 自动汇报 · 每 5 分钟更新 · 多项目监控                    ║")
    report.append("╚═══════════════════════════════════════════════════════════╝")
    
    return "\n".join(report)

if __name__ == "__main__":
    print(generate_report())
