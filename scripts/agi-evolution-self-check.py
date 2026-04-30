#!/usr/bin/env python3
"""
AGI 进化保障·自检脚本
执行频率：每小时
职责：验证所有 Cron/Skill/输出是否正常
"""

import subprocess
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/home/nicola/.openclaw/workspace/logs/self-check.log")
STATE_FILE = Path("/home/nicola/.openclaw/workspace/memory/agi-evolution-state.md")

# 检查清单
CHECKS = [
    {
        "name": "Cron 配置",
        "type": "cron",
        "expected": 10,
        "command": "crontab -l | grep -E 'skills/|scripts/.*evolution|scripts/.*degradation|scripts/.*verify' | wc -l"
    },
    {
        "name": "罔两高价值发现 Skill",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/skills/wangliang/high-value-discovery/run.py"
    },
    {
        "name": "庖丁变现追踪 Skill",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/skills/paoding/monetization-tracker/run.py"
    },
    {
        "name": "太一凌晨学习 Skill",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/skills/taiyi/night-learning/run.py"
    },
    {
        "name": "守藏吏干预监控 Skill",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/skills/steward/intervention-monitor/run.py"
    },
    {
        "name": "守藏吏事前确认 Skill",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/skills/steward/confirmation-monitor/run.py"
    },
    {
        "name": "守藏吏退化检测 Skill",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/skills/steward/degradation-detection/run.py"
    },
    {
        "name": "高价值机会输出",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/memory/high-value-opportunities.md"
    },
    {
        "name": "变现追踪输出",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/memory/monetization-tracker.md"
    },
    {
        "name": "状态面板",
        "type": "file",
        "path": "/home/nicola/.openclaw/workspace/memory/agi-evolution-state.md"
    },
]

def run_check(check):
    """执行单项检查"""
    if check["type"] == "file":
        path = Path(check["path"])
        exists = path.exists()
        return {
            "name": check["name"],
            "status": "✅" if exists else "❌",
            "detail": f"文件{'存在' if exists else '缺失'}"
        }
    elif check["type"] == "cron":
        try:
            result = subprocess.run(check["command"], shell=True, capture_output=True, text=True, timeout=10)
            count = int(result.stdout.strip())
            passed = count >= check["expected"]
            return {
                "name": check["name"],
                "status": "✅" if passed else "❌",
                "detail": f"{count}项（目标≥{check['expected']}）"
            }
        except Exception as e:
            return {
                "name": check["name"],
                "status": "❌",
                "detail": f"执行失败：{e}"
            }
    return {
        "name": check["name"],
        "status": "❌",
        "detail": "未知检查类型"
    }

def main():
    """主函数"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"🔍 AGI 进化保障自检启动 ({timestamp})")
    print("=" * 60)
    
    results = []
    passed = 0
    failed = 0
    
    for check in CHECKS:
        result = run_check(check)
        results.append(result)
        if result["status"] == "✅":
            passed += 1
        else:
            failed += 1
        print(f"{result['status']} {result['name']}: {result['detail']}")
    
    print("=" * 60)
    print(f"📊 总计：{passed + failed}项，✅ 通过{passed}项，❌ 失败{failed}项")
    
    # 生成报告
    report = f"""# AGI 进化保障自检报告

> 检查时间：{timestamp} | 频率：每小时

---

## 📊 检查结果

| 检查项 | 状态 | 详情 |
|--------|------|------|
"""
    for r in results:
        report += f"| {r['name']} | {r['status']} | {r['detail']} |\n"
    
    report += f"""
---

## 📈 统计

- **总计**: {passed + failed}项
- **通过**: {passed}项 ({passed * 100 // (passed + failed)}%)
- **失败**: {failed}项

---

## 🚨 告警

"""
    if failed > 0:
        report += "⚠️ 发现失败项，需立即修复：\n\n"
        for r in results:
            if r["status"] == "❌":
                report += f"- {r['name']}: {r['detail']}\n"
    else:
        report += "✅ 全部通过，无告警\n"
    
    report += f"\n---\n\n*检查时间：{timestamp} | 太一 AGI*\n"
    
    # 写入日志
    with open(LOG_FILE, 'a') as f:
        f.write(f"\n## {timestamp}\n\n")
        f.write(report)
    
    print(f"✅ 自检报告已写入：{LOG_FILE}")
    
    # 如有失败，告警太一
    if failed > 0:
        alert = f"⚠️ 自检发现{failed}项失败，需立即修复"
        notify_taiyi(alert)
    
    return failed == 0

def notify_taiyi(message):
    """上报太一"""
    cmd = [
        "openclaw", "message", "send",
        "--channel", "openclaw-weixin",
        "--target", "o9cq80yz80T13iCV5N_djDCSVo88@im.wechat",
        "--account", "387504e97169-im-bot",
        "--message", f"🚨 自检告警：{message}"
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
    except:
        pass

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
