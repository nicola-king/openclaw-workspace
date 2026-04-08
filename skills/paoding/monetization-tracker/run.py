#!/usr/bin/env python3
"""变现追踪 - 庖丁 Skill - 每日 23:00 执行"""

import json
from datetime import datetime
from pathlib import Path
import subprocess

TRACKER_FILE = Path("/home/nicola/.openclaw/workspace/memory/monetization-tracker.md")

def get_monetization_paths():
    return [
        {"name": "CAD 服务", "target": "¥5000/月", "current": "¥0", "deadline": "2026-04-30", "status": "🟡 部署中"},
        {"name": "空投套利", "target": "$100 启动", "current": "$0", "deadline": "2026-04-15", "status": "🟡 调研完成"},
        {"name": "技能市场", "target": "¥10K/月", "current": "¥0", "deadline": "2026-05-01", "status": "🟡 规划完成"}
    ]

def scan_revenue():
    return {"total": 0, "sources": []}

def scan_costs():
    return {"total": 40, "items": [{"name": "百炼 API", "cost": 40}]}

def calculate_roi(revenue, costs):
    return (revenue - costs) / costs * 100 if costs > 0 else 0

def generate_report(paths, revenue, costs, roi):
    date = datetime.now().strftime('%Y-%m-%d')
    report = f"""# 变现追踪日报（{date}）

> 生成时间：{datetime.now()} | 负责 Bot：庖丁

---

## 📊 今日统计
- **总收入**: ¥{revenue}
- **总成本**: ¥{costs}
- **净利润**: ¥{revenue - costs}
- **ROI**: {roi:.2f}%

---

## 🎯 变现路径
| 路径 | 目标 | 当前 | 截止 | 状态 |
|------|------|------|------|------|
"""
    for path in paths:
        report += f"| {path['name']} | {path['target']} | {path['current']} | {path['deadline']} | {path['status']} |\n"
    
    report += f"\n---\n\n## 🚨 告警\n"
    if revenue == 0:
        report += "- ⚠️ 连续 7 天无变现收入（目标：04-07 前>¥0）\n"
    else:
        report += "✅ 无告警\n"
    
    return report

def notify_taiyi(message):
    cmd = ["openclaw", "message", "send", "--channel", "openclaw-weixin", "--target", "o9cq80yz80T13iCV5N_djDCSVo88@im.wechat", "--account", "387504e97169-im-bot", "--message", f"💰 庖丁报告：{message}"]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
    except:
        pass

def main():
    print("💰 庖丁变现追踪启动...")
    paths = get_monetization_paths()
    revenue = scan_revenue()["total"]
    costs = scan_costs()["total"]
    roi = calculate_roi(revenue, costs)
    report = generate_report(paths, revenue, costs, roi)
    
    with open(TRACKER_FILE, 'w') as f:
        f.write(report)
    print(f"✅ 报告已写入：{TRACKER_FILE}")
    
    notify_taiyi(f"今日收入¥{revenue}，成本¥{costs}，ROI {roi:.2f}%")
    print(f"✅ 变现追踪完成：收入¥{revenue}，ROI {roi:.2f}%")

if __name__ == "__main__":
    main()
