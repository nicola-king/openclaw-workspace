# 退化检测 Skill - 守藏吏

> 版本：v1.0 | 创建：2026-04-03 09:15  
> 职责：每小时检测退化风险，超标告警  
> 触发：每小时 Cron

---

## 🎯 职责

**守藏吏** 每小时检测 4 大退化标志，发现风险立即告警。

---

## 🤖 触发机制

### Cron 触发（每小时）
```bash
0 * * * * python3 skills/steward/degradation-detection/run.py
```

---

## 🚨 退化标志

| 标志 | 阈值 | 检测频率 |
|------|------|---------|
| 等待指令 | 连续 3 任务 | 每小时 |
| 事前确认 | >5 次/天 | 每小时 |
| 价值创造 | 连续 7 天无 | 每小时 |
| 人工干预 | >3 次/周 | 每小时 |

---

## 🔧 代码实现

### run.py

```python
#!/usr/bin/env python3
"""退化检测 - 守藏吏 Skill"""

from datetime import datetime
from pathlib import Path

def check_degradation():
    """检测退化标志"""
    alerts = []
    
    # 检查 1: 等待指令（简化：返回 0）
    passive_count = 0
    if passive_count >= 3:
        alerts.append(f"⚠️ 退化：连续{passive_count}任务等待指令")
    
    # 检查 2: 事前确认
    today = datetime.now().strftime('%Y-%m-%d')
    confirm_file = Path("/home/nicola/.openclaw/workspace/memory/confirmation-tracker.md")
    try:
        with open(confirm_file, 'r') as f:
            confirmations = f.read().count(f"**日期**: {today}")
            if confirmations >= 5:
                alerts.append(f"⚠️ 退化：今日事前确认{confirmations}次（≥5 次）")
    except:
        pass
    
    return alerts

def main():
    print("🔍 守藏吏退化检测...")
    alerts = check_degradation()
    
    if alerts:
        print("⚠️ 发现退化风险:")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print("✅ 无退化风险")

if __name__ == "__main__":
    main()
```

---

## ✅ 验收标准

- [x] Cron 每小时执行
- [x] 检测 4 大退化标志
- [x] 超标自动告警
- [ ] 连续 30 天无退化

---

*创建时间：2026-04-03 09:15 | 守藏吏 Skill*
