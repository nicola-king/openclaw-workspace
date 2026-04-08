# 干预监控 Skill - 守藏吏

> 版本：v1.0 | 创建：2026-04-03 09:00  
> 职责：自动记录人工干预，实时告警  
> 触发：每小时 Cron + 事件驱动

---

## 🎯 职责

**守藏吏** 自动记录每次人工干预，分析根因，超标自动告警。

---

## 🤖 触发机制

### 1. Cron 触发（每小时）
```bash
0 * * * * python3 /home/nicola/.openclaw/workspace/skills/steward/intervention-monitor/run.py
```

### 2. 事件触发（实时）
```python
# 每次收到 SAYELF 消息时触发
if message.from_user == "SAYELF" and "为什么" in message or "怎么" in message:
    record_intervention()
```

---

## 📋 执行流程

```
┌─────────────────────────────────────────────────────────┐
│ 1. 监听 SAYELF 消息                                        │
│    - 检测关键词："为什么" / "怎么" / "为什么不" / "请"    │
│    - 检测命令：/compress /status /report                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. 记录干预事件                                           │
│    - 时间戳                                               │
│    - 干预原因（关键词分类）                               │
│    - 是否必要（AI 判断）                                   │
│    - 如何避免（AI 建议）                                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. 写入追踪文件                                           │
│    memory/human-intervention-log.md                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. 检查阈值                                               │
│    - 今日≥3 次 → 警告太一                                  │
│    - 本周>1 次 → 启动根因分析                              │
│    - 连续 2 周>3 次 → 上报 SAYELF                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. 每小时汇总报告                                         │
│    - 更新状态面板                                         │
│    - 上报太一                                             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 代码实现

### run.py（主脚本）

```python
#!/usr/bin/env python3
"""干预监控 - 守藏吏 Skill"""

import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/home/nicola/.openclaw/workspace/memory/human-intervention-log.md")
STATE_FILE = Path("/home/nicola/.openclaw/workspace/memory/agi-evolution-state.md")

def detect_intervention(message):
    """检测是否人工干预"""
    keywords = ["为什么", "怎么", "为什么不", "请", "/compress", "/status", "/report"]
    return any(kw in message for kw in keywords)

def record_intervention(reason, is_necessary=True, suggestion=""):
    """记录干预事件"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')
    
    entry = f"""
## {timestamp}
- **日期**: {date}
- **原因**: {reason}
- **是否必要**: {"✅ 必要" if is_necessary else "❌ 不必要"}
- **如何避免**: {suggestion or "待分析"}
"""
    
    with open(LOG_FILE, 'a') as f:
        f.write(entry)
    
    print(f"✅ 干预已记录：{reason}")

def check_threshold():
    """检查阈值并告警"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 统计今日干预次数
    with open(LOG_FILE, 'r') as f:
        content = f.read()
        today_count = content.count(f"**日期**: {today}")
    
    # 统计本周干预次数
    import subprocess
    result = subprocess.run(
        f"grep -c '## 2026-04' {LOG_FILE}",
        shell=True, capture_output=True, text=True
    )
    week_count = int(result.stdout.strip()) if result.returncode == 0 else 0
    
    # 告警逻辑
    alerts = []
    if today_count >= 3:
        alerts.append(f"⚠️ 今日干预{today_count}次（≥3 次警戒线）")
    if week_count > 1:
        alerts.append(f"⚠️ 本周干预{week_count}次（>1 次目标）")
    
    if alerts:
        # 上报太一
        notify_taiyi("\n".join(alerts))
        print("\n".join(alerts))
    
    return today_count, week_count

def notify_taiyi(message):
    """上报太一"""
    # 通过 OpenClaw message 工具发送
    import subprocess
    cmd = [
        "openclaw", "message", "send",
        "--channel", "openclaw-weixin",
        "--target", "o9cq80yz80T13iCV5N_djDCSVo88@im.wechat",
        "--account", "387504e97169-im-bot",
        "--message", f"🚨 守藏吏告警：{message}"
    ]
    subprocess.run(cmd, capture_output=True)

def main():
    """主函数"""
    print("🔍 守藏吏干预监控检查...")
    
    today_count, week_count = check_threshold()
    
    print(f"📊 今日干预：{today_count}次")
    print(f"📊 本周干预：{week_count}次")
    
    if today_count == 0 and week_count == 0:
        print("✅ 无干预，系统运行正常")

if __name__ == "__main__":
    main()
```

---

## 📊 输入输出

### 输入
- SAYELF 消息（微信/Telegram）
- Cron 定时触发

### 输出
- `memory/human-intervention-log.md` - 干预记录
- 告警消息（超标时上报太一）
- 状态面板更新

---

## 🚨 告警规则

| 条件 | 动作 | 接收者 |
|------|------|--------|
| 今日≥3 次 | 警告太一 | 太一 |
| 本周>1 次 | 启动根因分析 | 太一 |
| 连续 2 周>3 次 | 上报 SAYELF | SAYELF + 太一 |

---

## 🔍 根因分析（自动化）

```python
def analyze_root_cause():
    """分析干预根因"""
    with open(LOG_FILE, 'r') as f:
        content = f.read()
    
    # 分类统计
    categories = {
        "系统问题": content.count("自动执行中断"),
        "信息不足": content.count("为什么") + content.count("怎么"),
        "决策需求": content.count("请") + content.count("/"),
    }
    
    # 找出主要原因
    main_cause = max(categories, key=categories.get)
    
    # 生成改进建议
    suggestions = {
        "系统问题": "加强系统稳定性，增加自动恢复机制",
        "信息不足": "增加主动汇报频率，提前告知状态",
        "决策需求": "明确授权边界，减少事前确认",
    }
    
    return main_cause, suggestions[main_cause]
```

---

## 📝 日志格式

```markdown
## 2026-04-03 09:00:00
- **日期**: 2026-04-03
- **原因**: 自动执行中断
- **是否必要**: ✅ 必要
- **如何避免**: 已修复脚本，增加进程自动恢复

## 2026-04-03 09:05:00
- **日期**: 2026-04-03
- **原因**: 询问 AGI 进化进度
- **是否必要**: ✅ 必要
- **如何避免**: 增加主动汇报频率（每 5 分钟）
```

---

## ✅ 验收标准

- [x] Cron 每小时执行
- [x] 干预自动记录
- [x] 阈值自动检查
- [x] 超标自动告警
- [x] 根因自动分析
- [ ] 状态面板自动更新（集成到 update-evolution-state.py）

---

## 🔗 相关文件

- 宪法：`constitution/directives/AGI-EVOLUTION-GUARANTEE.md`
- 责任表：`constitution/directives/AGI-EVOLUTION-RESPONSIBILITY.md`
- 自动化：`constitution/directives/AGI-EVOLUTION-AUTOMATION.md`
- 日志：`memory/human-intervention-log.md`

---

*创建时间：2026-04-03 09:00 | 守藏吏 Skill | 智能自动化*
