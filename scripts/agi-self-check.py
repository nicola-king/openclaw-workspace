#!/usr/bin/env python3
"""AGI 进化保障·自检脚本 - 每小时执行"""
import subprocess
from datetime import datetime
from pathlib import Path

CHECKS = [
    {"name": "Cron 配置", "type": "cron", "expected": 10, "command": "crontab -l | grep -E 'skills/|scripts/.*evolution|scripts/.*degradation|scripts/.*verify' | wc -l"},
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
        try:
            result = subprocess.run(check["command"], shell=True, capture_output=True, text=True, timeout=10)
            count = int(result.stdout.strip())
            passed = count >= check["expected"]
            return {"name": check["name"], "status": "✅" if passed else "❌", "detail": f"{count}项（目标≥{check['expected']}）"}
        except:
            return {"name": check["name"], "status": "❌", "detail": "执行失败"}
    return {"name": check["name"], "status": "❌", "detail": "未知类型"}

def main():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"🔍 AGI 自检启动 ({timestamp})")
    results = [run_check(c) for c in CHECKS]
    passed = sum(1 for r in results if r["status"] == "✅")
    failed = len(results) - passed
    print("=" * 50)
    for r in results:
        print(f"{r['status']} {r['name']}: {r['detail']}")
    print("=" * 50)
    print(f"📊 总计：{passed}/{len(results)} 通过 ({passed * 100 // len(results)}%)")
    if failed > 0:
        print(f"⚠️ {failed}项失败，需修复")
    else:
        print("✅ 全部通过")
    return failed == 0

if __name__ == "__main__":
    main()
