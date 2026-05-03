#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MD 报告生成器 -  Telegram 友好格式
太一 AGI · 2026-04-19

功能:
- 生成 Telegram 友好的 MD 报告
- 简洁格式，易于预览
- 支持转发分享
- 可定制模板
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def generate_telegram_friendly_md(
    title: str,
    subtitle: str,
    company: str,
    products: List[Dict],
    markets: List[Dict],
    predictions: Dict,
    actions: List[str],
    contact: Dict,
    output_path: str = None
) -> str:
    """生成 Telegram 友好的 MD 报告"""
    
    content = f"""# {title}

> **生成**: {datetime.now().strftime('%Y-%m-%d')} | {subtitle}

---

## 📊 核心结论

"""
    
    # 产品列表
    for product in products:
        icon = "✅" if product.get("score", 0) >= 75 else "⚠️"
        content += f"| {product['name']} | {product['score']}/100 | {icon} {product['action']} |\n"
    
    content += f"""
---

## 🌍 目标市场

"""
    
    # 市场列表
    for market in markets:
        stars = "⭐" * market.get("rating", 3)
        content += f"""### {stars} {market['name']}
- **国家**: {market['countries']}
- **增长**: {market['growth']}
- **订单**: {market['orders']}

"""
    
    # 销售预测
    content += f"""## 💰 销售预测

| 年份 | 订单 | 毛利率 |
|------|------|--------|
| 第 1 年 | {predictions['year1']} | {predictions['margin1']} |
| 第 2 年 | {predictions['year2']} | {predictions['margin2']} |

---

## 🎯 行动清单

"""
    
    # 行动清单
    for action in actions:
        content += f"- [ ] {action}\n"
    
    # 联系信息
    content += f"""
---

## 📞 {contact.get('label', '公司信息')}

**{company}**
"""
    
    for key, value in contact.items():
        if key != 'label':
            content += f"- {key}: {value}\n"
    
    content += f"""
---

*太一 AGI 生成 | {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    # 保存文件
    if output_path is None:
        output_path = f"/home/nicola/.openclaw/workspace/reports/{datetime.now().strftime('%Y%m%d')}_report.md"
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(output_file)


# 示例：重庆兴旺工具报告
if __name__ == "__main__":
    output = generate_telegram_friendly_md(
        title="🔧 重庆兴旺工具 - 海外市场分析报告",
        subtitle="CCMT 2026 上海展 (E1-B183)",
        company="重庆兴旺工具制造有限公司",
        products=[
            {"name": "数控铣刀", "score": 78.69, "action": "重点推荐"},
            {"name": "数控刀具", "score": 77.69, "action": "重点推荐"},
            {"name": "机床附件", "score": 74.64, "action": "测试"},
            {"name": "工业钻头", "score": 74.02, "action": "测试"}
        ],
        markets=[
            {"name": "东南亚 (首选)", "countries": "越南/泰国/印尼", "growth": "+35%/年", "orders": "$500K-1M", "rating": 5},
            {"name": "中东 (蓝海)", "countries": "阿联酋/沙特", "growth": "+40%/年", "orders": "$300K-600K", "rating": 5},
            {"name": "南美 (潜力)", "countries": "巴西/智利", "growth": "+30%/年", "orders": "$200K-400K", "rating": 4}
        ],
        predictions={
            "year1": "$1.7M-3.4M",
            "margin1": "36%",
            "year2": "$3.4M-6.5M",
            "margin2": "38%"
        },
        actions=[
            "阿里巴巴国际站开店",
            "CCMT 展会客户跟进",
            "东南亚代理商招募",
            "CE 认证准备"
        ],
        contact={
            "label": "公司信息",
            "展位": "E1-B183",
            "日期": "4.21-25",
            "地点": "上海新国际博览中心"
        },
        output_path="/home/nicola/.openclaw/workspace/reports/重庆兴旺工具_Telegram 简报.md"
    )
    
    print(f"✅ MD 报告已生成：{output}")
