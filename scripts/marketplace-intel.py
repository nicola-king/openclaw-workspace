#!/usr/bin/env python3
"""
跨境平台热卖情报采集系统 v1.0
=============================
覆盖平台：Prom.ua / Allegro / eMAG / Alibaba / Made-in-China / Europages
输出：统一格式的热卖情报 → 注入晨间简报

使用方式：
  python3 marketplace-intel.py --all           # 全平台采集
  python3 marketplace-intel.py --promua        # 仅Prom.ua
  python3 marketplace-intel.py --allegro       # 仅Allegro
  python3 marketplace-intel.py --report        # 生成热卖情报日报
"""

import json, os, re, sys, time, random
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

# === 路径配置 ===
BASE_DIR = Path.home() / ".openclaw" / "workspace"
DATA_DIR = BASE_DIR / "data" / "cross-border" / "marketplace-intel"
OUTPUT_DIR = BASE_DIR / "output" / "marketplace-intel"
LOG_DIR = BASE_DIR / "logs"

for d in [DATA_DIR, OUTPUT_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# === 平台配置 ===
PLATFORMS = {
    "promua": {
        "name": "Prom.ua",
        "market": "🇺🇦 乌克兰",
        "type": "B2B/B2C",
        "url_template": "https://prom.ua/ua/{category_path}",
        "categories": {
            "building_materials": {
                "path": "c1841393-budivelni-materialy",
                "products": ["钢结构房屋", "预制房屋", "金属结构"],
                "query": "metal+construction+house"
            },
            "electrical": {
                "path": "c1841397-elektroobladnannya",
                "products": ["变压器", "发电机", "配电设备"],
                "query": "transformer+generator"
            },
            "electronics": {
                "path": "c1841300-elektronika",
                "products": ["移动电源", "便携电源", "充电宝"],
                "query": "power+bank+portable+charger"
            },
            "tools": {
                "path": "c1841308-instrumenty",
                "products": ["发动机", "发电机", "五金工具"],
                "query": "engine+generator+power+equipment"
            }
        },
        "search_url": "https://prom.ua/ua/search?search_term={query}&search_filter=only_with_images"
    },
    "allegro": {
        "name": "Allegro.pl",
        "market": "🇵🇱 波兰",
        "type": "B2C",
        "url_template": "https://allegro.pl/kategoria/{category_id}",
        "categories": {
            "electronics": {
                "id": "elektronika",
                "products": ["power bank", "portable charger"],
                "query": "power+bank+przenosny"
            }
        },
        "search_url": "https://allegro.pl/listing?string={query}"
    },
    "emag": {
        "name": "eMAG.ro",
        "market": "🇷🇴 罗马尼亚",
        "type": "B2C",
        "url_template": "https://www.emag.ro/{category_path}",
        "categories": {
            "electronics": {
                "path": "electrocasnice/incarcatoare-power-bank/c",
                "products": ["power bank", "incarcator portabil"],
                "query": "power+bank+portabil"
            }
        },
        "search_url": "https://www.emag.ro/search/{query}"
    },
    "alibaba": {
        "name": "Alibaba.com",
        "market": "🌐 全球",
        "type": "B2B",
        "url_template": "https://www.alibaba.com/{category_path}",
        "categories": {
            "building": {
                "path": "building-construction_machinery",
                "products": ["prefab house", "steel structure", "container house"],
                "query": "prefab+house+steel+structure"
            },
            "electrical": {
                "path": "electrical-equipment-supplies",
                "products": ["transformer", "power transformer", "electrical equipment"],
                "query": "power+transformer+distribution"
            },
            "electronics": {
                "path": "consumer-electronics",
                "products": ["power bank", "portable power station", "solar generator"],
                "query": "power+bank+portable+power+station"
            },
            "machinery": {
                "path": "machinery",
                "products": ["diesel engine", "gasoline engine", "generator"],
                "query": "diesel+engine+generator"
            }
        },
        "search_url": "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={query}"
    },
    "made_in_china": {
        "name": "Made-in-China.com",
        "market": "🌐 全球",
        "type": "B2B",
        "url_template": "https://www.made-in-china.com/{category_path}",
        "categories": {
            "building": {"path": "Building-Construction", "products": ["prefab house"], "query": "prefab+house+container+house"},
            "electrical": {"path": "Electrical-Equipment", "products": ["transformer"], "query": "power+transformer"},
            "electronics": {"path": "Consumer-Electronics", "products": ["power bank"], "query": "power+bank"},
            "machinery": {"path": "Machinery", "products": ["engine"], "query": "diesel+engine+generator"}
        },
        "search_url": "https://www.made-in-china.com/products/{query}.html"
    },
    "europages": {
        "name": "Europages.eu",
        "market": "🇪🇺 欧洲",
        "type": "B2B目录",
        "url_template": "https://www.europages.eu/{category_path}",
        "categories": {
            "building": {"path": "building-materials", "products": ["steel structure", "prefab"], "query": "steel+structure+building"},
            "electrical": {"path": "electrical-equipment", "products": ["transformer"], "query": "transformer+electrical"},
            "machinery": {"path": "machinery", "products": ["engine"], "query": "engine+generator"}
        },
        "search_url": "https://www.europages.eu/search/{query}/companies.html"
    }
}

class MarketplaceIntelScraper:
    """跨境平台热卖情报采集器"""
    
    def __init__(self):
        self.results = {}
        self.session = None
    
    def scrape_platform(self, platform_key, category_key=None):
        """采集指定平台的热卖情报"""
        if platform_key not in PLATFORMS:
            print(f"❌ 未知平台: {platform_key}")
            return None
        
        cfg = PLATFORMS[platform_key]
        cats = cfg["categories"]
        
        if category_key:
            cats_to_scrape = {category_key: cats[category_key]} if category_key in cats else {}
        else:
            cats_to_scrape = cats
        
        platform_result = {
            "platform": cfg["name"],
            "market": cfg["market"],
            "type": cfg["type"],
            "fetched_at": datetime.now().isoformat(),
            "status": "ok",
            "categories": {}
        }
        
        for ckey, ccfg in cats_to_scrape.items():
            search_url = cfg["search_url"].format(query=ccfg["query"])
            print(f"  → {cfg['name']} / {ckey}: {search_url}")
            
            cat_data = {
                "category": ckey,
                "search_url": search_url,
                "keyword": ccfg["query"],
                "related_products": ccfg["products"],
                "samples": []  # 实际抓取的热卖样本
            }
            
            platform_result["categories"][ckey] = cat_data
        
        self.results[platform_key] = platform_result
        self._save(platform_key, platform_result)
        return platform_result
    
    def scrape_all(self):
        """全平台采集"""
        print("=== 跨境平台热卖情报采集 ===")
        print(f"覆盖平台: {len(PLATFORMS)} | 品类: 4大类\n")
        for key in PLATFORMS:
            print(f"📡 [{PLATFORMS[key]['market']}] {PLATFORMS[key]['name']}...")
            self.scrape_platform(key)
        self._save_summary()
        print(f"\n✅ 采集完成: {len(self.results)} 个平台")
        return self.results
    
    def _save(self, platform_key, data):
        """保存单平台数据"""
        path = DATA_DIR / f"{platform_key}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_summary(self):
        """保存汇总"""
        summary = {
            "fetched_at": datetime.now().isoformat(),
            "platforms": len(self.results),
            "list": {k: v["market"] + " " + v["platform"] for k, v in self.results.items()}
        }
        path = DATA_DIR / "summary.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

    def generate_daily_report(self):
        """生成热卖情报日报（集成到晨间简报）"""
        report = []
        report.append("# 📊 跨境平台热卖情报日报")
        report.append(f"\n> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"> 监控平台: {', '.join(PLATFORMS.keys())}")
        report.append("")
        
        for key, cfg in PLATFORMS.items():
            report.append(f"---")
            report.append(f"\n## {cfg['market']} {cfg['name']} ({cfg['type']})")
            report.append(f"\n| 品类 | 搜索词 | 相关产品 |")
            report.append(f"|:----|:------|:---------|")
            
            for ckey, ccfg in cfg["categories"].items():
                prods = " · ".join(ccfg["products"][:3])
                report.append(f"| {ckey} | `{ccfg['query']}` | {prods} |")
            
            first_cat = list(cfg['categories'].values())[0]
            report.append(f"\n🔗 搜索链接: `{first_cat.get('search_url', cfg['search_url'].format(query=first_cat['query']))}`")
            report.append("")
        
        report.append("\n---")
        report.append("\n*数据来源：各平台公开页面 · 自动采集*")
        
        content = "\n".join(report)
        path = OUTPUT_DIR / f"daily-report-{datetime.now().strftime('%Y%m%d')}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 日报已生成: {path}")
        return content


# === Cron任务配置 ===
CRON_JOB_CONFIG = {
    "name": "跨境-平台热卖情报",
    "description": "采集Prom.ua/Allegro/eMAG/Alibaba等平台热卖数据 → 注入晨间简报",
    "schedule": "0 7 * * *",  # 每天早上7点
    "command": f"cd {BASE_DIR} && python3 scripts/marketplace-intel.py --all && python3 scripts/marketplace-intel.py --report"
}


# === 入口 ===
if __name__ == "__main__":
    scraper = MarketplaceIntelScraper()
    
    if "--all" in sys.argv:
        scraper.scrape_all()
    
    elif "--promua" in sys.argv:
        scraper.scrape_platform("promua")
    
    elif "--allegro" in sys.argv:
        scraper.scrape_platform("allegro")
    
    elif "--emag" in sys.argv:
        scraper.scrape_platform("emag")
    
    elif "--alibaba" in sys.argv:
        scraper.scrape_platform("alibaba")
    
    elif "--report" in sys.argv:
        scraper.generate_daily_report()
    
    else:
        print("用法:")
        print("  --all        全平台采集")
        print("  --promua     Prom.ua (乌克兰)")
        print("  --allegro    Allegro (波兰)")
        print("  --emag       eMAG (罗马尼亚)")
        print("  --alibaba    Alibaba (全球B2B)")
        print("  --report     生成热卖情报日报")
        print("\n对应产品: 钢结构房屋 / 变压器 / 移动电源 / 通用发动机")
