#!/usr/bin/env python3
"""自检 - 守藏吏 Skill - 每小时执行"""

import subprocess
from datetime import datetime
from pathlib import Path

CHECKS = [
    {"name": "Cron 配置", "type": "cron", "expected": 9, "cmd": "crontab -l 2>/dev/null | grep -cE 'self-check|intervention-monitor|check-degradation|update-evolution|high-value|night-learning|monetization|stage-verification'"},
    {"name": "罔两 Skill", "type": "file", "path": "skills/wangliang/high-value-discovery/run.py"},
    {"name": "庖丁 Skill", "type": "file", "path": "skills/paoding/monetization-tracker/run.py"},
    {"name": "太一学习 Skill", "type": "file", "path": "skills/taiyi/night-learning/run.py"},
    {"name": "守藏吏干预 Skill", "type": "file", "path": "skills/steward/intervention-monitor/run.py"},
    {"name": "高价值输出", "type": "file", "path": "memory/high-value-opportunities.md"},
    {"name": "变现追踪输出", "type": "file", "path": "memory/monetization-tracker.md"},
    {"name": "状态面板", "type": "file", "path": "memory/agi-evolution-state.md"},
]

def run_check(check):
    if check["type"] == "file":
        exists = Path(check["path"]).exists()
        return {"name": check["name"], "status": "✅" if exists else "❌", "detail": f"{'存在' if exists else '缺失'}"}
    elif check["type"] == "cron":
        result = subprocess.run(check["cmd"], shell=True, capture_output=True, text=True, timeout=10)
        count = int(result.stdout.strip())
        passed = count >= check["expected"]
        return {"name": check["name"], "status": "✅" if passed else "❌", "detail": f"{count}项（目标≥{check['expected']}）"}
    return {"name": check["name"], "status": "❌", "detail": "未知类型"}

def notify_taiyi(message, urgent=False):
    cmd = ["openclaw", "message", "send", "--channel", "openclaw-weixin", "--target", "o9cq80yz80T13iCV5N_djDCSVo88@im.wechat", "--account", "387504e97169-im-bot", "--message", f"{'🚨 紧急：' if urgent else '📊 自检：'}{message}"]
    subprocess.run(cmd, capture_output=True, timeout=30)

def main():
    print("🔍 守藏吏自检启动...")
    results = [run_check(c) for c in CHECKS]
    passed = sum(1 for r in results if r["status"] == "✅")
    total = len(results)
    
    print("=" * 50)
    for r in results:
        print(f"{r['status']} {r['name']}: {r['detail']}")
    print("=" * 50)
    print(f"📊 通过率：{passed}/{total} ({passed * 100 // total}%)")
    
    # 写入日志
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = Path("/home/nicola/.openclaw/workspace/logs/self-check.log")
    with open(log_file, 'a') as f:
        f.write(f"\n## {timestamp}\n")
        f.write(f"**通过率**: {passed}/{total} ({passed * 100 // total}%)\n\n")
        for r in results:
            f.write(f"- {r['name']}: {r['status']} {r['detail']}\n")
    
    if passed < total:
        failed = total - passed
        notify_taiyi(f"自检失败{failed}项，需修复", urgent=(failed >= 3))
        print(f"⚠️ 已告警太一（失败{failed}项）")
    else:
        print("✅ 全部通过")
    
    return passed == total

if __name__ == "__main__":
    main()
