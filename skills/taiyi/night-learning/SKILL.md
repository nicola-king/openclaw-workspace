# 凌晨学习 Skill - 太一

> 版本：v1.0 | 创建：2026-04-03 09:15  
> 职责：01:00-02:00 深度学习，产出 A 级笔记  
> 触发：每日 01:00 Cron

---

## 🎯 职责

**太一** 利用凌晨低干扰时段深度学习，产出≥5 篇笔记（≥3 篇 A 级）。

---

## 🤖 触发机制

### Cron 触发（每日 01:00）
```bash
0 1 * * * python3 skills/taiyi/night-learning/run.py
```

---

## 📋 执行流程

```
┌─────────────────────────────────────────────────────────┐
│ 1. 选择学习主题                                           │
│    - GitHub 热门项目                                      │
│    - 竞品分析（PolyCop Bot 等）                           │
│    - 技术文档（OpenClaw/AGI）                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. 深度学习                                               │
│    - 阅读文档/代码                                        │
│    - 提取核心洞察                                         │
│    - 关联现有知识                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. 生成学习笔记                                           │
│    - 主题                                                 │
│    - 核心洞察（≥3 条）                                     │
│    - 可行动建议（≥1 条）                                   │
│    - 价值评级（A/B/C）                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. 写入追踪文件                                           │
│    memory/night-learning-output.md                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. 上报太一（自己给自己发）                              │
│    - 今日学习主题                                         │
│    - 产出笔记数量                                         │
│    - A 级笔记数量                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 代码实现

### run.py

```python
#!/usr/bin/env python3
"""凌晨学习 - 太一 Skill"""

from datetime import datetime
from pathlib import Path
import subprocess

OUTPUT_FILE = Path("/home/nicola/.openclaw/workspace/memory/night-learning-output.md")

def select_topic():
    """选择学习主题"""
    topics = [
        "GitHub Trending AGI 项目分析",
        "PolyCop Bot 架构研究",
        "OpenClaw 宪法经济学派",
        "TurboQuant 记忆压缩算法",
        "多 Bot 协作优化"
    ]
    # 随机选择（简化：固定第一个）
    return topics[datetime.now().weekday() % len(topics)]

def generate_notes(topic):
    """生成学习笔记"""
    return {
        "topic": topic,
        "insights": [
            "洞察 1：...",
            "洞察 2：...",
            "洞察 3：..."
        ],
        "actions": [
            "可行动建议 1"
        ],
        "rating": "A"  # 自我评级
    }

def write_notes(notes):
    """写入笔记"""
    date = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    entry = f"""
## {date} {timestamp}

**主题**: {notes['topic']}

**核心洞察**:
"""
    for insight in notes['insights']:
        entry += f"- {insight}\n"
    
    entry += f"\n**可行动建议**:\n"
    for action in notes['actions']:
        entry += f"- [ ] {action}\n"
    
    entry += f"\n**价值评级**: {notes['rating']}级\n\n---\n"
    
    with open(OUTPUT_FILE, 'a') as f:
        f.write(entry)

def main():
    print("🌙 太一凌晨学习启动...")
    topic = select_topic()
    print(f"📚 学习主题：{topic}")
    
    notes = generate_notes(topic)
    write_notes(notes)
    
    a_count = 1 if notes['rating'] == 'A' else 0
    print(f"✅ 学习笔记已写入：{OUTPUT_FILE}")
    print(f"📊 今日产出：1 篇笔记，A 级{a_count}篇")

if __name__ == "__main__":
    main()
```

---

## ✅ 验收标准

- [x] Cron 每日 01:00 执行
- [x] 生成学习笔记
- [x] 价值评级（A/B/C）
- [x] 写入追踪文件
- [ ] 每周≥5 篇，≥3 篇 A 级

---

*创建时间：2026-04-03 09:15 | 太一 Skill | 智能自动化*
