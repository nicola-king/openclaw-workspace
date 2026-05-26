# Scrapling 自适应爬取层 v1.0

> **引擎**: Scrapling v0.4.8 (54K ⭐) + requests fallback
> **原理**: 根据目标网站 URL 自动检测防护等级，选择最优爬取引擎

---

## 三层策略

| 等级 | 防护 | 引擎 | 速度 | 适用 |
|------|------|------|------|------|
| Level 0 | 无/低 | requests | ⚡ 最快 | 政府网站/开源站点/API |
| Level 1 | 中等 | Scrapling Fetcher | 🚀 快 | 一般商业网站 |
| Level 2 | 强(Cloudflare等) | Scrapling + 自适应 | 🐌 较慢 | LinkedIn/Amazon/社交媒体 |

---

## 使用

```python
from skills.scrapling_adaptor.core import smart_fetch, extract_items

# 自动选择引擎
result = smart_fetch("https://abr.business.gov.au/Search/ResultsActive?SearchText=test")
# → Level 0: 用 requests 直连，最快

result = smart_fetch("https://example.com/products", adaptive=True)
# → Level 1: Scrapling + 自适应解析

# 提取结构化数据（未来改版自动重定位）
items = extract_items(result["response"], ".product-item", auto_save=True)
for item in items:
    print(item.css("h2::text").get())
```

## CLI

```bash
python3 core.py https://example.com
python3 core.py https://example.com --adaptive
python3 core.py https://example.com --extract 'h1.title'
```
