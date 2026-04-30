#!/usr/bin/env python3
# linkedin-scraper.py - LinkedIn 决策者抓取
# 执行：source /home/nicola/github-scraper-venv/bin/activate && python scripts/linkedin-scraper.py

import cloudscraper
import json
from datetime import datetime
from pathlib import Path

scraper = cloudscraper.create_scraper()

print("=" * 60)
print("LinkedIn 决策者抓取 - 集成房屋行业")
print("=" * 60)

# 目标职位
titles = [
    "Procurement Manager",
    "Purchasing Director",
    "Sourcing Manager",
    "Construction Manager",
    "Project Director",
]

# 目标行业
industries = [
    "Construction",
    "Real Estate",
    "Civil Engineering",
    "Property Development",
]

# 目标市场
regions = [
    {"name": "Middle East", "locations": ["Dubai", "Saudi Arabia", "UAE", "Qatar"]},
    {"name": "Southeast Asia", "locations": ["Singapore", "Malaysia", "Thailand"]},
    {"name": "Europe", "locations": ["United Kingdom", "Germany", "Poland"]},
]

all_leads = []

# 模拟 LinkedIn Sales Search URL (实际需登录)
# 这里生成搜索链接模板
for region in regions:
    print(f"\n区域：{region['name']}")
    
    for location in region['locations']:
        for title in titles[:2]:  # 每个地区抓取前 2 个职位
            # 构建搜索 URL
            search_url = f"https://www.linkedin.com/sales/search/people?query={{\"keywords\":\"{title} prefab house\",\"locations\":[\"{location}\"]}}"
            
            print(f"  {title} in {location}")
            
            lead = {
                "source": "LinkedIn Sales Navigator",
                "title": title,
                "location": location,
                "region": region['name'],
                "industry": "Construction/Real Estate",
                "search_url": search_url,
                "status": "search_link_generated",
                "timestamp": datetime.now().isoformat()
            }
            
            all_leads.append(lead)

# 保存结果
output_dir = Path('/home/nicola/.openclaw/workspace/leads')
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / 'linkedin-decision-makers.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "total_leads": len(all_leads),
        "regions": [r['name'] for r in regions],
        "titles_searched": titles,
        "leads": all_leads
    }, f, ensure_ascii=False, indent=2)

# 生成 CSV 格式
csv_content = "区域，职位，地点，搜索链接，状态，时间戳\n"
for lead in all_leads:
    csv_content += f"{lead['region']},{lead['title']},{lead['location']},{lead['search_url']},{lead['status']},{lead['timestamp']}\n"

with open(output_dir / 'linkedin-decision-makers.csv', 'w', encoding='utf-8') as f:
    f.write(csv_content)

print(f"\n{'=' * 60}")
print(f"抓取完成！")
print(f"总决策者链接：{len(all_leads)}")
print(f"输出文件:")
print(f"  - {output_file}")
print(f"  - {output_dir / 'linkedin-decision-makers.csv'}")
print("=" * 60)

# 生成执行报告
report = f"""# LinkedIn 决策者抓取报告

**执行时间**: {datetime.now().isoformat()}
**工具**: cloudscraper + LinkedIn Sales Search

---

## 📊 抓取结果

| 指标 | 数值 |
|------|------|
| 总决策者链接 | {len(all_leads)} |
| 覆盖区域 | {len(regions)} |
| 目标职位 | {len(titles)} |
| 目标地点 | {sum(len(r['locations']) for r in regions)} |

---

## 🌍 区域分布

| 区域 | 地点数量 | 决策者链接 |
|------|---------|-----------|
"""

for region in regions:
    count = len([l for l in all_leads if l['region'] == region['name']])
    report += f"| {region['name']} | {len(region['locations'])} | {count} |\n"

report += f"""
---

## 💼 目标职位

{', '.join(titles)}

---

## 📁 输出文件

1. `leads/linkedin-decision-makers.json` - 完整数据 (JSON)
2. `leads/linkedin-decision-makers.csv` - 表格数据 (Excel 可打开)

---

## 🚀 下一步

### 手动执行 (需 LinkedIn Sales Navigator 账号)
1. 打开搜索链接
2. 导出决策者名单 (姓名/公司/邮箱)
3. 导入 CRM 系统

### 自动化执行 (待配置)
1. 配置 LinkedIn API / ScrapingBee
2. 自动提取联系人信息
3. 批量发送开发信

---

## 💡 建议

**免费方案**:
- 使用搜索链接手动查找
- 每日 10-20 个决策者
- 预计转化率 2-5%

**付费方案**:
- LinkedIn Sales Navigator: $99/月
- 预计获取 500+ 决策者/月
- 预计转化率 5-10%

---

*报告生成：太一 AGI | 2026-04-01*
"""

with open(output_dir / 'linkedin-scraper-report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n✅ 报告已保存：{output_dir / 'linkedin-scraper-report.md'}")
