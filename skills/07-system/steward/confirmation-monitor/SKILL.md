# 事前确认监控 Skill - 守藏吏

> 版本：v1.0 | 创建：2026-04-03 09:15  
> 职责：统计每日事前确认次数，超标告警  
> 触发：每小时 Cron

---

## 🎯 职责

**守藏吏** 自动统计事前确认次数，≥3 次/天自动告警。

---

## 🤖 触发机制

### Cron 触发（每小时）
```bash
0 * * * * python3 skills/steward/confirmation-monitor/run.py
```

---

## 🔧 代码实现

### run.py

```python
#!/usr/bin/env python3
"""事前确认监控 - 守藏吏 Skill"""

from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/home/nicola/.openclaw/workspace/memory/confirmation-tracker.md")

def count_confirmations():
    """统计今日确认次数"""
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        with open(LOG_FILE, 'r') as f:
            content = f.read()
            return content.count(f"**日期**: {today}")
    except:
        return 0

def main():
    print("🔍 守藏吏事前确认监控...")
    count = count_confirmations()
    status = "⚠️ 超标" if count >= 3 else "✅ 正常"
    print(f"📊 今日事前确认：{count}次 {status}")

if __name__ == "__main__":
    main()
```

---

## ✅ 验收标准

- [x] Cron 每小时执行
- [x] 统计确认次数
- [x] ≥3 次告警
- [ ] 连续 7 天<3 次（阶段 4 验收）

---

*创建时间：2026-04-03 09:15 | 守藏吏 Skill*
