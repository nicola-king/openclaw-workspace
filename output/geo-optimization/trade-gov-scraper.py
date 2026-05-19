#!/usr/bin/env python3
"""
Trade.gov 市场情报抓取器 — GEO系统数据源
免费开源，无需API，直接抓取公开页面

使用方式：
  python3 trade-gov-scraper.py                     # 抓取所有已配置页面
  python3 trade-gov-scraper.py --fetch-all         # 抓取+发现新页面
  python3 trade-gov-scraper.py --update-docs       # 更新GEO文档
"""

import os, json, re, sys
from datetime import datetime
import urllib.request
import urllib.error
from html.parser import HTMLParser

# === 配置 ===
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "geo-optimization")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cross-border", "trade-gov")

# 已知的高价值 Market Intelligence 页面
TARGET_PAGES = {
    "energy-storage-overview": {
        "url": "https://www.trade.gov/energy-storage",
        "category": "energy-storage",
        "markets": ["global"],
        "priority": "P0"
    },
    "brazil-bess-auction": {
        "url": "https://www.trade.gov/market-intelligence/brazil-energy-battery-storage-auction",
        "category": "market-intelligence",
        "markets": ["brazil"],
        "priority": "P0"
    },
    "italy-energy-storage": {
        "url": "https://www.trade.gov/market-intelligence/italy-energy-storage",
        "category": "market-intelligence",
        "markets": ["italy", "eu"],
        "priority": "P0"
    },
    "uk-energy-storage": {
        "url": "https://www.trade.gov/market-intelligence/united-kingdom-energy-storage-market",
        "category": "market-intelligence",
        "markets": ["uk", "eu"],
        "priority": "P1"
    },
    "poland-energy-storage-boom": {
        "url": "https://www.trade.gov/market-intelligence/poland-energy-transition-storage-boom",
        "category": "market-intelligence",
        "markets": ["poland", "eu"],
        "priority": "P1"
    },
    "india-ev-battery-storage": {
        "url": "https://www.trade.gov/market-intelligence/india-electric-vehicle-battery-and-storage-trends",
        "category": "market-intelligence",
        "markets": ["india", "apac"],
        "priority": "P2"
    },
    "us-energy-trade-dashboard": {
        "url": "https://www.trade.gov/data-visualization/us-energy-trade-dashboard",
        "category": "data-dashboard",
        "markets": ["us"],
        "priority": "P1"
    }
}

# 可发现的子页面模式（用于自动发现新内容）
DISCOVER_PATTERNS = [
    r'href="(/market-intelligence/[^"]+)"',
    r'href="(/energy-storage[^"]*)"',
    r'href="(/country-commercial-guides/[^"]+)"',
]


class TradeGovScraper:
    """Trade.gov 免费公开数据抓取器"""

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.results = {}

    def fetch_page(self, name, config):
        """抓取单个页面内容"""
        url = config["url"]
        print(f"  → {name}: {url}")
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; TaiyiGEO/1.0)",
                    "Accept": "text/html,application/xhtml+xml"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"    ❌ 失败: {e}")
            return None

        # 提取可读文本（简单提取，非完美）
        text = self._extract_text(html)
        result = {
            "url": url,
            "fetched_at": datetime.now().isoformat(),
            "category": config.get("category", ""),
            "markets": config.get("markets", []),
            "priority": config.get("priority", "P2"),
            "status": "ok",
            "content_length": len(text),
            "text_snippet": text[:500] + "..." if len(text) > 500 else text
        }

        self.results[name] = result
        self._save(name, result, text)
        print(f"    ✅ {len(text)} chars")
        return result

    def _extract_text(self, html):
        """简陋的HTML→文本提取"""
        # 去掉script/style
        html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL|re.IGNORECASE)
        # 去掉标签
        text = re.sub(r'<[^>]+>', ' ', html)
        # 多空格合并
        text = re.sub(r'\s+', ' ', text)
        # 去掉空行
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        return '\n'.join(lines)

    def _save(self, name, metadata, full_text):
        """保存抓取结果"""
        # 元数据JSON
        meta_path = os.path.join(DATA_DIR, f"{name}_meta.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # 全文Markdown
        md_path = os.path.join(DATA_DIR, f"{name}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\n")
            f.write(f"> 来源: {metadata['url']}\n")
            f.write(f"> 抓取时间: {metadata['fetched_at']}\n")
            f.write(f"> 分类: {metadata['category']} | 市场: {', '.join(metadata['markets'])} | 优先级: {metadata['priority']}\n\n")
            f.write("---\n\n")
            f.write(full_text)

    def fetch_all(self):
        """抓取所有已配置页面"""
        print(f"=== Trade.gov 市场情报抓取 ===")
        print(f"目标页面: {len(TARGET_PAGES)}")
        print()
        for name, config in TARGET_PAGES.items():
            self.fetch_page(name, config)
        self._save_summary()
        return self.results

    def _save_summary(self):
        """保存抓取摘要"""
        summary_path = os.path.join(DATA_DIR, "summary.json")
        summary = {
            "last_fetch": datetime.now().isoformat(),
            "pages_fetched": len([k for k, v in self.results.items() if v and v.get("status") == "ok"]),
            "pages_total": len(TARGET_PAGES),
            "by_priority": {
                "P0": len([k for k, v in self.results.items() if v and v.get("priority") == "P0"]),
                "P1": len([k for k, v in self.results.items() if v and v.get("priority") == "P1"]),
                "P2": len([k for k, v in self.results.items() if v and v.get("priority") == "P2"]),
            },
            "pages": {k: v.get("content_length", 0) for k, v in self.results.items() if v}
        }
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 摘要已保存: {summary_path}")

    def discover_new_pages(self):
        """发现新的 Market Intelligence 页面"""
        print("\n=== 发现新页面 ===")
        discovered = []
        for name, config in TARGET_PAGES.items():
            try:
                req = urllib.request.Request(
                    config["url"],
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    html = resp.read().decode("utf-8", errors="replace")
                for pattern in DISCOVER_PATTERNS:
                    matches = re.findall(pattern, html)
                    for m in matches:
                        full_url = f"https://www.trade.gov{m}" if m.startswith("/") else m
                        if full_url not in [v["url"] for v in TARGET_PAGES.values()]:
                            discovered.append(full_url)
            except:
                pass
        if discovered:
            print(f"发现 {len(discovered)} 个新页面 (手动添加):")
            for url in sorted(set(discovered))[:20]:
                print(f"  - {url}")
        else:
            print("未发现新页面")
        return list(set(discovered))


# === 入口 ===
if __name__ == "__main__":
    scraper = TradeGovScraper()
    
    if "--fetch-all" in sys.argv:
        scraper.fetch_all()
        scraper.discover_new_pages()
    elif "--discover" in sys.argv:
        scraper.discover_new_pages()
    else:
        scraper.fetch_all()
    
    print("\n✅ 完成")
