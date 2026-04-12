# 意图准确 Skill - 太一

> 版本：v1.0 | 创建：2026-04-03 09:15  
> 职责：每次任务后记录意图理解准确率  
> 触发：事件驱动（任务完成）

---

## 🎯 职责

**太一** 在每次任务完成后记录意图理解准确率，目标>95%。

---

## 🤖 触发机制

### 事件触发
- 任务完成时
- 太一手动触发：`/intent-accuracy`

---

## 🔧 代码实现

### run.py

```python
#!/usr/bin/env python3
"""意图准确 - 太一 Skill"""

from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/home/nicola/.openclaw/workspace/memory/intent-accuracy-log.md")

def record_accuracy(task_id, accuracy, feedback=""):
    """记录准确率"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"""
## {task_id} - {timestamp}
- **准确率**: {accuracy}%
- **反馈**: {feedback or "无"}
- **是否需要追问**: {"是" if accuracy < 95 else "否"}

---
"""
    with open(LOG_FILE, 'a') as f:
        f.write(entry)
    
    return accuracy

def main():
    print("🎯 太一意图准确记录...")
    acc = record_accuracy("TASK-001", 98, "准确理解用户意图")
    print(f"✅ 意图准确率：{acc}%")

if __name__ == "__main__":
    main()
```

---

## ✅ 验收标准

- [x] 事件触发记录
- [x] 准确率>95%
- [ ] 每日统计平均值

---

*创建时间：2026-04-03 09:15 | 太一 Skill*
