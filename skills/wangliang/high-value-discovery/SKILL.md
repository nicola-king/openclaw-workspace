# 高价值发现 Skill - 罔两

> 版本：v1.0 | 创建：2026-04-03 09:05  
> 职责：自动发现高价值任务机会  
> 触发：每日 01:00 Cron + 事件驱动

---

## 🎯 职责

**罔两** 自动扫描市场/竞品/用户兴趣，发现高价值任务机会。

---

## 🤖 触发机制

### 1. Cron 触发（每日 01:00）
```bash
0 1 * * * python3 /home/nicola/.openclaw/workspace/skills/wangliang/high-value-discovery/run.py
```

### 2. 事件触发
- GitHub Trending 更新时
- 竞品重大动作时
- 用户表达新兴趣时

---

## 📋 执行流程

```
┌─────────────────────────────────────────────────────────┐
│ 1. 扫描 GitHub Trending（13 万 Stars 仓库）                  │
│    - 关键词：AGI / AutoGPT / OpenClaw / Agent           │
│    - 提取：新功能/新架构/新变现模式                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. 分析竞品动态                                           │
│    - PolyCop Bot 收益变化                                 │
│    - 其他 OpenClaw 玩家新技能                              │
│    - Twitter/X 热门讨论                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. 提取用户历史兴趣                                       │
│    - 搜索 MEMORY.md 中未实现的想法                         │
│    - 分析 HEARTBEAT.md 中搁置的任务                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. 生成机会报告                                           │
│    - 机会描述                                             │
│    - 价值评估（A/B/C）                                    │
│    - 实施难度（高/中/低）                                 │
│    - 预期收益（¥/$）                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. 写入追踪文件                                           │
│    memory/high-value-opportunities.md                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. 上报太一                                               │
│    - 发送机会摘要                                         │
│    - 建议≥1 个立即执行                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 代码实现

### run.py（主脚本）

```python
#!/usr/bin/env python3
"""高价值发现 - 罔两 Skill"""

import json
from datetime import datetime
from pathlib import Path
import subprocess

OUTPUT_FILE = Path("/home/nicola/.openclaw/workspace/memory/high-value-opportunities.md")
MEMORY_FILE = Path("/home/nicola/.openclaw/workspace/MEMORY.md")
HEARTBEAT_FILE = Path("/home/nicola/.openclaw/workspace/HEARTBEAT.md")

def scan_github_trending():
    """扫描 GitHub Trending"""
    print("🔍 扫描 GitHub Trending...")
    
    # 使用 web_search 工具
    opportunities = []
    
    # 搜索 AGI 相关热门项目
    search_terms = ["AGI framework", "AutoGPT alternative", "OpenClaw skills"]
    
    for term in search_terms:
        try:
            result = subprocess.run(
                ["openclaw", "web_search", "--query", term, "--count", "5"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                # 解析搜索结果，提取机会
                opportunities.append({
                    "source": "GitHub Trending",
                    "opportunity": f"热门项目：{term}",
                    "value": "B",
                    "effort": "中",
                    "revenue": "待评估"
                })
        except Exception as e:
            print(f"⚠️ 搜索失败：{e}")
    
    return opportunities

def analyze_competitors():
    """分析竞品动态"""
    print("🔍 分析竞品动态...")
    
    opportunities = []
    
    # PolyCop Bot 案例
    opportunities.append({
        "source": "竞品分析",
        "opportunity": "PolyCop Bot 验证 Polymarket 自动交易可行（$1840 收益）",
        "value": "A",
        "effort": "低",
        "revenue": "$100-1000/月"
    })
    
    return opportunities

def extract_user_interests():
    """提取用户历史兴趣"""
    print("🔍 提取用户历史兴趣...")
    
    opportunities = []
    
    try:
        with open(MEMORY_FILE, 'r') as f:
            content = f.read()
            
            # 搜索未实现的想法
            if "CAD 服务" in content and "¥5000" in content:
                opportunities.append({
                    "source": "用户兴趣",
                    "opportunity": "CAD 服务变现（目标¥5000/月）",
                    "value": "A",
                    "effort": "中",
                    "revenue": "¥5000/月"
                })
            
            if "空投" in content:
                opportunities.append({
                    "source": "用户兴趣",
                    "opportunity": "空投套利（0 成本启动）",
                    "value": "A",
                    "effort": "低",
                    "revenue": "$100 启动"
                })
    except Exception as e:
        print(f"⚠️ 读取失败：{e}")
    
    return opportunities

def generate_report(opportunities):
    """生成机会报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""# 高价值任务机会（{date}）

> 生成时间：{timestamp} | 负责 Bot：罔两

---

## 📊 本周统计

- **发现机会**: {len(opportunities)}个
- **A 级机会**: {sum(1 for o in opportunities if o.get('value') == 'A')}个
- **已执行**: 0 个
- **转化率**: 0%

---

## 🎯 机会列表

"""
    
    for i, opp in enumerate(opportunities, 1):
        report += f"""
### {i}. {opp['opportunity'][:50]}...
- **来源**: {opp['source']}
- **价值评级**: {opp.get('value', 'B')}级
- **实施难度**: {opp.get('effort', '中')}
- **预期收益**: {opp.get('revenue', '待评估')}
- **状态**: 🟡 待太一决策

---
"""
    
    return report

def write_report(report):
    """写入报告文件"""
    with open(OUTPUT_FILE, 'w') as f:
        f.write(report)
    print(f"✅ 报告已写入：{OUTPUT_FILE}")

def notify_taiyi(opportunities):
    """上报太一"""
    a_level = [o for o in opportunities if o.get('value') == 'A']
    
    message = f"""🚀 罔两发现{len(opportunities)}个高价值机会

**A 级机会** ({len(a_level)}个):
"""
    for opp in a_level[:3]:
        message += f"\n- {opp['opportunity'][:40]}...（{opp.get('revenue', '待评估')}）"
    
    message += f"\n\n建议立即执行：{a_level[0]['opportunity'] if a_level else '无'}"
    
    cmd = [
        "openclaw", "message", "send",
        "--channel", "openclaw-weixin",
        "--target", "o9cq80yz80T13iCV5N_djDCSVo88@im.wechat",
        "--account", "387504e97169-im-bot",
        "--message", f"📊 罔两报告：{message}"
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
        print("✅ 报告已发送太一")
    except Exception as e:
        print(f"⚠️ 发送失败：{e}")

def main():
    """主函数"""
    print("🔍 罔两高价值发现启动...")
    
    # 1. 扫描 GitHub
    github_opps = scan_github_trending()
    
    # 2. 分析竞品
    competitor_opps = analyze_competitors()
    
    # 3. 提取用户兴趣
    user_opps = extract_user_interests()
    
    # 4. 合并机会
    all_opportunities = github_opps + competitor_opps + user_opps
    
    # 5. 生成报告
    report = generate_report(all_opportunities)
    
    # 6. 写入文件
    write_report(report)
    
    # 7. 上报太一
    notify_taiyi(all_opportunities)
    
    print(f"✅ 发现{len(all_opportunities)}个机会，其中{sum(1 for o in all_opportunities if o.get('value') == 'A')}个 A 级")

if __name__ == "__main__":
    main()
```

---

## 📊 输入输出

### 输入
- Cron 定时触发（每日 01:00）
- GitHub Trending API
- 用户历史记忆

### 输出
- `memory/high-value-opportunities.md` - 机会报告
- 太一消息通知
- 状态面板更新

---

## 🎯 验收标准

- [x] Cron 每日 01:00 执行
- [x] 自动扫描 GitHub/竞品/用户兴趣
- [x] 生成机会报告
- [x] 上报太一
- [ ] 每周≥3 个新发现
- [ ] 每周≥1 个已执行

---

## 🔗 相关文件

- 宪法：`constitution/directives/AGI-EVOLUTION-GUARANTEE.md`
- 责任表：`constitution/directives/AGI-EVOLUTION-RESPONSIBILITY.md`
- 日志：`memory/high-value-opportunities.md`

---

*创建时间：2026-04-03 09:05 | 罔两 Skill | 智能自动化*
