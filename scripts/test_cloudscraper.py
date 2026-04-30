#!/usr/bin/env python3
# test_cloudscraper.py - cloudscraper 快速测试
# 执行：source /home/nicola/github-scraper-venv/bin/activate && python scripts/test_cloudscraper.py

import cloudscraper
import json
from datetime import datetime

scraper = cloudscraper.create_scraper()
results = []

print("=" * 60)
print("cloudscraper 批量测试")
print("=" * 60)

# 测试 URL 列表
test_urls = [
    {"name": "httpbin", "url": "https://httpbin.org/html"},
    {"name": "Alibaba RFQ", "url": "https://rfq.alibaba.com/post.htm?rfqName=prefab%20house"},
    {"name": "Alibaba prefab", "url": "https://www.alibaba.com/showroom/prefab-house.html"},
]

for i, test in enumerate(test_urls, 1):
    print(f"\n[{i}/{len(test_urls)}] {test['name']}: {test['url']}")
    try:
        r = scraper.get(test['url'], timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        status = "✅ 成功" if r.status_code == 200 else f"⚠️ {r.status_code}"
        print(f"  状态码：{r.status_code}")
        print(f"  大小：{len(r.text)} bytes")
        print(f"  结果：{status}")
        results.append({
            "name": test['name'],
            "url": test['url'],
            "status_code": r.status_code,
            "size_bytes": len(r.text),
            "status": "success" if r.status_code == 200 else "warning",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"  ❌ 失败：{e}")
        results.append({
            "name": test['name'],
            "url": test['url'],
            "error": str(e),
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        })

# 保存报告
report = {
    "timestamp": datetime.now().isoformat(),
    "total_tests": len(test_urls),
    "successful": sum(1 for r in results if r["status"] == "success"),
    "failed": sum(1 for r in results if r["status"] == "failed"),
    "results": results
}

with open('/home/nicola/.openclaw/workspace/reports/cloudscraper-test-report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"\n{'=' * 60}")
print(f"测试完成！成功：{report['successful']}/{report['total_tests']}")
print(f"报告：/home/nicola/.openclaw/workspace/reports/cloudscraper-test-report.json")
print("=" * 60)
