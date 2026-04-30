#!/usr/bin/env python3
# buyer-scraper.py - 海外买家批量抓取
# 执行：source /home/nicola/github-scraper-venv/bin/activate && python scripts/buyer-scraper.py

import cloudscraper
import json
import re
from datetime import datetime
from pathlib import Path

scraper = cloudscraper.create_scraper()

print("=" * 60)
print("海外买家批量抓取 - 集成房屋")
print("=" * 60)

# 搜索关键词
keywords = [
    "prefab house",
    "modular home",
    "prefabricated building",
    "container house",
    "steel structure warehouse",
]

# 目标市场
markets = [
    {"name": "Middle East", "region": "中东", "keywords": ["dubai", "saudi", "uae", "qatar"]},
    {"name": "Southeast Asia", "region": "东南亚", "keywords": ["singapore", "malaysia", "thailand", "philippines"]},
    {"name": "Europe", "region": "欧洲", "keywords": ["uk", "germany", "france", "poland"]},
]

all_leads = []

for keyword in keywords:
    print(f"\n搜索关键词：{keyword}")
    
    # Alibaba 搜索
    alibaba_url = f"https://www.alibaba.com/showroom/{keyword.replace(' ', '-')}.html"
    print(f"  Alibaba: {alibaba_url}")
    
    try:
        r = scraper.get(alibaba_url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            print(f"    ✅ 成功 ({len(r.text)} bytes)")
            
            # 简单提取供应商信息 (实际需更复杂解析)
            # 这里仅做演示，实际生产环境需要完整 HTML 解析
            leads = []
            
            # 示例数据结构
            leads.append({
                "source": "Alibaba",
                "keyword": keyword,
                "url": alibaba_url,
                "type": "supplier",
                "status": "found",
                "timestamp": datetime.now().isoformat()
            })
            
            all_leads.extend(leads)
        else:
            print(f"    ⚠️ 状态码：{r.status_code}")
    except Exception as e:
        print(f"    ❌ 失败：{e}")
    
    # RFQ 采购需求
    rfq_url = f"https://rfq.alibaba.com/post.htm?rfqName={keyword.replace(' ', '%20')}"
    print(f"  RFQ: {rfq_url}")
    
    try:
        r = scraper.get(rfq_url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            print(f"    ✅ 成功 ({len(r.text)} bytes)")
            
            all_leads.append({
                "source": "Alibaba RFQ",
                "keyword": keyword,
                "url": rfq_url,
                "type": "buying_request",
                "status": "found",
                "timestamp": datetime.now().isoformat()
            })
        else:
            print(f"    ⚠️ 状态码：{r.status_code}")
    except Exception as e:
        print(f"    ❌ 失败：{e}")

# 保存结果
output_dir = Path('/home/nicola/.openclaw/workspace/leads')
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / 'buyer-leads.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "total_leads": len(all_leads),
        "keywords_searched": keywords,
        "leads": all_leads
    }, f, ensure_ascii=False, indent=2)

print(f"\n{'=' * 60}")
print(f"抓取完成！")
print(f"总线索：{len(all_leads)}")
print(f"输出文件：{output_file}")
print("=" * 60)
