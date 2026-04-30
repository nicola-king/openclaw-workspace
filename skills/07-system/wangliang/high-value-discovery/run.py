#!/usr/bin/env python3
"""高价值发现 - 罔两 Skill - 每日 01:00 执行"""

import subprocess
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path("/home/nicola/.openclaw/workspace/memory/high-value-opportunities.md")
MEMORY_FILE = Path("/home/nicola/.openclaw/workspace/MEMORY.md")

def analyze_competitors():
    """分析竞品动态"""
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
    opportunities = []
    
    try:
        with open(MEMORY_FILE, 'r') as f:
            content = f.read()
            
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

def notify_taiyi(opportunities):
    """上报太一"""
    a_level = [o for o in opportunities if o.get('value') == 'A']
    
    if not a_level:
        return
    
    message = f"""🚀 罔两发现{len(opportunities)}个高价值机会

**A 级机会** ({len(a_level)}个):
"""
    for opp in a_level[:3]:
        message += f"\n- {opp['opportunity'][:40]}...（{opp.get('revenue', '待评估')}）"
    
    message += f"\n\n建议立即执行：{a_level[0]['opportunity']}"
    
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
    
    # 1. 分析竞品
    competitor_opps = analyze_competitors()
    
    # 2. 提取用户兴趣
    user_opps = extract_user_interests()
    
    # 3. 合并机会
    all_opportunities = competitor_opps + user_opps
    
    # 4. 生成报告
    report = generate_report(all_opportunities)
    
    # 5. 写入文件
    with open(OUTPUT_FILE, 'w') as f:
        f.write(report)
    print(f"✅ 报告已写入：{OUTPUT_FILE}")
    
    # 6. 上报太一
    notify_taiyi(all_opportunities)
    
    print(f"✅ 发现{len(all_opportunities)}个机会，其中{sum(1 for o in all_opportunities if o.get('value') == 'A')}个 A 级")

if __name__ == "__main__":
    main()
