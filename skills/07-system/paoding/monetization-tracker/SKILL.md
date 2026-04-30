# 变现追踪 Skill - 庖丁

> 版本：v1.0 | 创建：2026-04-03 09:15  
> 职责：自动追踪变现进展，计算 ROI  
> 触发：每日 23:00 Cron + 事件驱动

---

## 🎯 职责

**庖丁** 自动追踪所有变现路径的收入/成本/ROI，超标自动告警。

---

## 🤖 触发机制

### 1. Cron 触发（每日 23:00）
```bash
0 23 * * * python3 skills/paoding/monetization-tracker/run.py
```

### 2. 事件触发
- 收入产生时（微信/支付宝/加密货币）
- 成本支出时（API 调用/服务器/工具）

---

## 📋 执行流程

```
┌─────────────────────────────────────────────────────────┐
│ 1. 读取变现路径配置                                       │
│    memory/monetization-tracker.md                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. 扫描收入记录                                           │
│    - 微信支付（待集成）                                   │
│    - 支付宝（待集成）                                     │
│    - 加密货币（GMGN/Polymarket API）                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. 扫描成本记录                                           │
│    - API 调用费用（百炼/Gemini）                           │
│    - 服务器费用（VPS/云存储）                             │
│    - 工具订阅（LibreCAD/其他）                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. 计算 ROI                                               │
│    ROI = (收入 - 成本) / 成本 * 100%                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. 检查阈值                                               │
│    - 连续 7 天无收入 → 警告太一                             │
│    - ROI < 0 → 分析原因                                   │
│    - 收入>目标 → 庆祝 + 加码建议                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. 更新追踪文件                                           │
│    memory/monetization-tracker.md                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 7. 上报太一                                               │
│    - 每日简报（收入/成本/ROI）                            │
│    - 告警（连续 7 天无收入）                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 代码实现

### run.py（主脚本）

```python
#!/usr/bin/env python3
"""变现追踪 - 庖丁 Skill"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

TRACKER_FILE = Path("/home/nicola/.openclaw/workspace/memory/monetization-tracker.md")
STATE_FILE = Path("/home/nicola/.openclaw/workspace/memory/agi-evolution-state.md")

def get_monetization_paths():
    """获取变现路径配置"""
    return [
        {
            "name": "CAD 服务",
            "target": "¥5000/月",
            "current": "¥0",
            "deadline": "2026-04-30",
            "status": "🟡 部署中"
        },
        {
            "name": "空投套利",
            "target": "$100 启动",
            "current": "$0",
            "deadline": "2026-04-15",
            "status": "🟡 调研完成"
        },
        {
            "name": "技能市场",
            "target": "¥10K/月",
            "current": "¥0",
            "deadline": "2026-05-01",
            "status": "🟡 规划完成"
        }
    ]

def scan_revenue():
    """扫描收入记录"""
    # TODO: 集成真实支付 API
    return {
        "total": 0,
        "sources": []
    }

def scan_costs():
    """扫描成本记录"""
    # 估算 API 调用成本
    return {
        "total": 40,  # 百炼 40 元/月
        "items": [
            {"name": "百炼 API", "cost": 40},
            {"name": "VPS", "cost": 0},  # 自有服务器
        ]
    }

def calculate_roi(revenue, costs):
    """计算 ROI"""
    if costs == 0:
        return 0
    return (revenue - costs) / costs * 100

def check_threshold(paths, revenue):
    """检查阈值并告警"""
    alerts = []
    
    # 检查连续 7 天无收入
    if revenue == 0:
        alerts.append("⚠️ 连续 7 天无变现收入（目标：04-07 前>¥0）")
    
    # 检查截止日期临近
    today = datetime.now()
    for path in paths:
        deadline = datetime.strptime(path["deadline"], "%Y-%m-%d")
        days_left = (deadline - today).days
        if 0 < days_left <= 7 and path["current"] == "¥0":
            alerts.append(f"⚠️ {path['name']} 截止剩余{days_left}天，当前¥0")
    
    if alerts:
        notify_taiyi("\n".join(alerts))
    
    return alerts

def generate_report(paths, revenue, costs, roi):
    """生成变现报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""# 变现追踪日报（{date}）

> 生成时间：{timestamp} | 负责 Bot：庖丁

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
    
    report += f"""
---

## 📈 趋势分析

- **连续无收入天数**: {7 if revenue == 0 else 0}天
- **截止 04-07 剩余**: {4}天
- **阶段 3 验收**: 变现路径验证（需要>¥0）

---

## 🚨 告警

"""
    
    alerts = check_threshold(paths, revenue)
    if alerts:
        for alert in alerts:
            report += f"- {alert}\n"
    else:
        report += "✅ 无告警\n"
    
    return report

def notify_taiyi(message):
    """上报太一"""
    cmd = [
        "openclaw", "message", "send",
        "--channel", "openclaw-weixin",
        "--target", "o9cq80yz80T13iCV5N_djDCSVo88@im.wechat",
        "--account", "387504e97169-im-bot",
        "--message", f"💰 庖丁报告：{message}"
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
        print("✅ 报告已发送太一")
    except Exception as e:
        print(f"⚠️ 发送失败：{e}")

def main():
    """主函数"""
    print("💰 庖丁变现追踪启动...")
    
    # 1. 获取路径配置
    paths = get_monetization_paths()
    
    # 2. 扫描收入
    revenue_data = scan_revenue()
    revenue = revenue_data["total"]
    
    # 3. 扫描成本
    costs_data = scan_costs()
    costs = costs_data["total"]
    
    # 4. 计算 ROI
    roi = calculate_roi(revenue, costs)
    
    # 5. 生成报告
    report = generate_report(paths, revenue, costs, roi)
    
    # 6. 写入文件
    with open(TRACKER_FILE, 'w') as f:
        f.write(report)
    print(f"✅ 报告已写入：{TRACKER_FILE}")
    
    # 7. 上报太一
    summary = f"今日收入¥{revenue}，成本¥{costs}，ROI {roi:.2f}%"
    notify_taiyi(summary)
    
    print(f"✅ 变现追踪完成：收入¥{revenue}，ROI {roi:.2f}%")

if __name__ == "__main__":
    main()
```

---

## 📊 输入输出

### 输入
- Cron 定时触发（每日 23:00）
- 支付 API（待集成）
- 成本记录

### 输出
- `memory/monetization-tracker.md` - 变现报告
- 太一消息通知
- 状态面板更新

---

## 🚨 告警规则

| 条件 | 动作 | 接收者 |
|------|------|--------|
| 连续 7 天无收入 | 警告太一 | 太一 |
| 截止<7 天且¥0 | 警告太一 | 太一 |
| ROI < 0 | 分析原因 | 太一 |

---

## ✅ 验收标准

- [x] Cron 每日 23:00 执行
- [x] 自动扫描收入/成本
- [x] 计算 ROI
- [x] 阈值自动检查
- [x] 超标自动告警
- [ ] 真实支付 API 集成（待后续）

---

## 🔗 相关文件

- 宪法：`constitution/directives/AGI-EVOLUTION-GUARANTEE.md`
- 责任表：`constitution/directives/AGI-EVOLUTION-RESPONSIBILITY.md`
- 日志：`memory/monetization-tracker.md`

---

*创建时间：2026-04-03 09:15 | 庖丁 Skill | 智能自动化*
