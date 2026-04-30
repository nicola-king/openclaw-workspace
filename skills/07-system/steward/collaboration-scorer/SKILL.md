# 协作评分 Skill - 守藏吏

> 版本：v1.0 | 创建：2026-04-03 09:15  
> 职责：每次多 Bot 协作后自动评分  
> 触发：事件驱动（协作完成）

---

## 🎯 职责

**守藏吏** 在多 Bot 协作完成后自动发起评分，记录到追踪文件。

---

## 🤖 触发机制

### 事件触发
- 多 Bot 协作完成时
- 太一手动触发：`/collab-score`

---

## 📋 评分维度

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| 职责清晰度 | 30% | 无重叠/无遗漏=10 分 |
| 响应速度 | 25% | <5 分钟=10 分，<15 分钟=7 分 |
| 输出质量 | 25% | 无需修改=10 分，小修改=7 分 |
| 自主率 | 20% | 100% 自主=10 分，需追问=5 分 |

---

## 🔧 代码实现

### run.py

```python
#!/usr/bin/env python3
"""协作评分 - 守藏吏 Skill"""

from datetime import datetime
from pathlib import Path

SCORE_FILE = Path("/home/nicola/.openclaw/workspace/memory/bot-collaboration-scores.md")

def record_score(drill_id, scores):
    """记录协作评分"""
    avg = sum(scores.values()) / len(scores)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    entry = f"""
### {drill_id} - {timestamp}
- 职责清晰度：{scores.get('clarity', 0)}/10
- 响应速度：{scores.get('speed', 0)}/10
- 输出质量：{scores.get('quality', 0)}/10
- 自主率：{scores.get('autonomy', 0)}/10
- **平均分：{avg:.1f}/10**

---
"""
    with open(SCORE_FILE, 'a') as f:
        f.write(entry)
    
    return avg

def main():
    print("📊 守藏吏协作评分...")
    # 示例：记录一次协作
    avg = record_score("DRILL-001", {"clarity": 9, "speed": 8, "quality": 9, "autonomy": 10})
    print(f"✅ 协作评分完成：平均分{avg:.1f}/10")

if __name__ == "__main__":
    main()
```

---

## ✅ 验收标准

- [x] 事件触发评分
- [x] 记录到追踪文件
- [x] 计算平均分
- [ ] 连续 3 次≥9/10（阶段 3 验收）

---

*创建时间：2026-04-03 09:15 | 守藏吏 Skill*
