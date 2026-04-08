#!/usr/bin/env python3
# parse-buyer-leads.py - 解析买家数据 + 生成开发信
# 执行：source /home/nicola/github-scraper-venv/bin/activate && python scripts/parse-buyer-leads.py

import json
from datetime import datetime
from pathlib import Path

# 读取线索数据
with open('/home/nicola/.openclaw/workspace/leads/buyer-leads.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 分类整理
buying_requests = [l for l in data['leads'] if l['type'] == 'buying_request']
suppliers = [l for l in data['leads'] if l['type'] == 'supplier']

print("=" * 60)
print("买家线索解析报告")
print("=" * 60)
print(f"\n总线索：{data['total_leads']}")
print(f"采购需求 (RFQ): {len(buying_requests)}")
print(f"供应商页面：{len(suppliers)}")
print(f"关键词：{', '.join(data['keywords_searched'])}")

# 生成开发信模板
email_template = """Subject: Premium Prefab House Solutions from 宫阙 (Gongque) - Factory Direct Pricing

Dear [Buyer Name],

I hope this email finds you well.

My name is [Your Name] from 宫阙 (Gongque), a leading manufacturer of prefabricated housing solutions based in Chongqing, China.

I noticed your recent sourcing request for [Product Category] on Alibaba, and I believe our products could be an excellent fit for your needs.

## Why Choose 宫阙？

✅ **Factory Direct Pricing** - 30-50% below market rates
✅ **Rapid Deployment** - Foldable design, 10-minute setup
✅ **Quality Certified** - ISO 9001, CE, SGS certified
✅ **Customization** - Tailored solutions for your market
✅ **Proven Track Record** - $8M annual exports, 500+ sets/month

## Our Core Products

| Product | Price Range | MOQ | Lead Time |
|---------|-------------|-----|-----------|
| Foldable Container House | $2,500-4,500 | 1 set | 7-10 days |
| Modular Prefab Home | $8,000-25,000 | 1 set | 15-20 days |
| Steel Structure Warehouse | $50-120/m² | 100m² | 20-30 days |
| Light Steel Villa | $800-1,500/m² | 50m² | 25-35 days |

## Special Offer for [Company Name]

🎁 **Free Sample**: 3D rendering of your custom design
🎁 **Free Shipping**: For orders over $50,000
🎁 **Extended Warranty**: 5 years (vs. standard 2 years)

## Next Steps

I'd love to schedule a 15-minute call to discuss:
1. Your specific requirements
2. Customization options
3. Pricing and delivery timeline

Are you available for a quick call this week?

Best regards,

[Your Name]
Export Manager | 宫阙 (Gongque)
📱 WhatsApp/WeChat: [Your Number]
📧 Email: [Your Email]
🌐 Website: [Your Website]
📍 Location: Chongqing, China (中欧班列 direct connection)

---
P.S. We've successfully delivered projects to [Similar Market/Region] with 100% client satisfaction. Case studies available upon request.
"""

# 生成开发信文件
output_dir = Path('/home/nicola/.openclaw/workspace/leads')
output_dir.mkdir(parents=True, exist_ok=True)

# 保存开发信模板
with open(output_dir / 'email-template.md', 'w', encoding='utf-8') as f:
    f.write("# 宫阙海外开发信模板\n\n")
    f.write("**生成时间**: " + datetime.now().isoformat() + "\n")
    f.write("**适用场景**: Alibaba RFQ 买家跟进\n\n")
    f.write(email_template)

print(f"\n✅ 开发信模板已保存：{output_dir / 'email-template.md'}")

# 生成买家列表 Excel 格式
excel_content = """关键词，类型，URL，状态，时间戳
"""
for lead in data['leads']:
    excel_content += f"{lead['keyword']},{lead['type']},{lead['url']},{lead['status']},{lead['timestamp']}\n"

with open(output_dir / 'buyer-leads.csv', 'w', encoding='utf-8') as f:
    f.write(excel_content)

print(f"✅ 买家列表已保存：{output_dir / 'buyer-leads.csv'}")

# 生成解析报告
report = f"""# 买家线索解析报告

**生成时间**: {datetime.now().isoformat()}
**数据来源**: Alibaba RFQ + 供应商页面

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 总线索 | {data['total_leads']} |
| 采购需求 (RFQ) | {len(buying_requests)} |
| 供应商页面 | {len(suppliers)} |
| 关键词数量 | {len(data['keywords_searched'])} |

---

## 🎯 采购需求详情

| 关键词 | URL | 状态 |
|--------|-----|------|
"""

for req in buying_requests:
    report += f"| {req['keyword']} | [链接]({req['url']}) | {req['status']} |\n"

report += f"""
---

## 📦 供应商页面详情

| 关键词 | URL | 状态 |
|--------|-----|------|
"""

for sup in suppliers:
    report += f"| {sup['keyword']} | [链接]({sup['url']}) | {sup['status']} |\n"

report += f"""
---

## 📧 开发信模板

已生成标准开发信模板，包含：
- ✅ 公司介绍 (宫阙核心优势)
- ✅ 产品矩阵 (价格/MOQ/交期)
- ✅ 特别优惠 (免费样品/运费/质保)
- ✅ 行动号召 (15 分钟通话)
- ✅ 联系方式 (WhatsApp/WeChat/Email)

**文件**: `leads/email-template.md`

---

## 🚀 下一步行动

### 今日执行 (P0)
1. ✅ 解析买家数据
2. ✅ 生成开发信模板
3. [ ] 发送首批 5 封开发信
4. [ ] LinkedIn 决策者抓取
5. [ ] 定时任务配置

### 本周执行 (P1)
- [ ] 自动化开发信发送
- [ ] 回复追踪系统
- [ ] CRM 集成

---

*报告生成：太一 AGI | 2026-04-01*
"""

with open(output_dir / 'buyer-analysis-report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ 解析报告已保存：{output_dir / 'buyer-analysis-report.md'}")

print(f"\n{'=' * 60}")
print("解析完成！")
print(f"输出目录：{output_dir}")
print("=" * 60)
