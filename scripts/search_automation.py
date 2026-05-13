#!/home/sayelf/.local/venvs/scraper/bin/python3
"""
太一智能搜索自动化 v1.0
═══════════════════════════════════
动态国家识别 · 智能策略配置 · 自动化监控

自动检测目标国家/地区 → 配置最优搜索资源
→ 穿透式监控 → 新买家入库 → 报告推送
"""

import sys, json, os, re, time, hashlib
# 将 venv site-packages 加入路径（兼容 cron 不使用 shebang 的情况）
_venv_site = os.path.expanduser("~/.local/venvs/scraper/lib/python3.14/site-packages")
if os.path.isdir(_venv_site) and _venv_site not in sys.path:
    sys.path.insert(0, _venv_site)
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

sys.path.insert(0, str(Path.home() / ".openclaw" / "workspace" / "scripts"))
from penetrating_search import PenetratingSearch

# ═══════════════════════════════════════════════════════════════
# 国家数据库 — 自动识别 + 动态配置
# ═══════════════════════════════════════════════════════════════

COUNTRY_PROFILES = {
    "saudi_arabia": {
        "aliases": ["沙特", "沙特阿拉伯", "KSA", "Saudi", "Saudi Arabia", "sa"],
        "domain": ".sa", "lang": "en,ar",
        "google_cc": "Saudi+Arabia",
        "search_queries": [
            "{product} Saudi Arabia buyer",
            "{product} Saudi Arabia procurement",
            "{product} company Saudi",
            "{product} supplier Saudi Vision 2030",
            "{product} distributor Riyadh Jeddah",
        ],
        "yellow_pages": [
            "https://www.yellowpages.com.sa/search?q={kw}",
            "https://www.google.com/search?q={kw}+site:sa",
        ],
        "tender_platforms": ["etimad.sa"],
        "language_hint": ["الرياض", "السعودية", "الدمام", "جدة"],
        "default_proxy": "clash",
        "certification_needed": ["SASO"],
        "risk_level": "medium",
    },
    "uae": {
        "aliases": ["阿联酋", "UAE", "Dubai", "Abu Dhabi", "迪拜", "阿布扎比", "ae"],
        "domain": ".ae", "lang": "en,ar",
        "google_cc": "UAE",
        "search_queries": [
            "{product} UAE buyer", "{product} Dubai procurement",
            "{product} company Abu Dhabi", "{product} supplier Emirates",
            "{product} distributor Dubai",
        ],
        "yellow_pages": [
            "https://www.yellowpages.ae/search/{kw}.html",
            "https://www.google.com/search?q={kw}+site:ae",
        ],
        "tender_platforms": ["etenders.ae", "abudhabitenders.ae"],
        "language_hint": ["دبي", "أبوظبي", "الشارقة"],
        "default_proxy": "clash",
        "certification_needed": ["ESMA", "SASO"],
        "risk_level": "low",
    },
    "iraq": {
        "aliases": ["伊拉克", "Iraq", "Baghdad", "iq"],
        "domain": ".iq", "lang": "en,ar",
        "google_cc": "Iraq",
        "search_queries": [
            "{product} Iraq buyer", "{product} Iraq reconstruction",
            "{product} Baghdad procurement", "{product} Iraq government tender",
            "{product} UNDP Iraq housing",
        ],
        "yellow_pages": [],
        "tender_platforms": [],
        "language_hint": ["بغداد", "العراق", "البصرة"],
        "default_proxy": "clash",
        "certification_needed": [],
        "risk_level": "high",
        "payment_risk": "信用证+出口保险",
    },
    "qatar": {
        "aliases": ["卡塔尔", "Qatar", "Doha", "qa"],
        "domain": ".qa", "lang": "en,ar",
        "google_cc": "Qatar",
        "search_queries": [
            "{product} Qatar buyer", "{product} Doha procurement",
            "{product} Qatar World Cup legacy", "{product} supplier Qatar",
        ],
        "yellow_pages": ["https://www.google.com/search?q={kw}+site:qa"],
        "tender_platforms": [],
        "language_hint": ["قطر", "الدوحة"],
        "default_proxy": "clash",
        "certification_needed": ["QSAS"],
        "risk_level": "low",
    },
    "australia": {
        "aliases": ["澳洲", "澳大利亚", "Australia", "Sydeny", "Melbourne", "au"],
        "domain": ".au", "lang": "en",
        "google_cc": "Australia",
        "search_queries": [
            "{product} Australia buyer", "{product} Australian importer",
            "{product} supplier Sydney Melbourne",
            "{product} distributor Brisbane Perth",
            "{product} prefab builder Australia",
        ],
        "yellow_pages": [
            "https://www.yellowpages.com.au/search/listings?clue={kw}",
            "https://www.google.com/search?q={kw}+site:au",
        ],
        "tender_platforms": ["tenders.nsw.gov.au", "tenders.vic.gov.au"],
        "default_proxy": "clash",
        "certification_needed": ["NCC", "CodeMark"],
        "risk_level": "low",
    },
    "usa": {
        "aliases": ["美国", "USA", "US", "America", "us"],
        "domain": ".us", "lang": "en",
        "google_cc": "USA",
        "search_queries": [
            "{product} USA buyer", "{product} US importer distributor",
            "{product} supplier America", "{product} US procurement",
        ],
        "yellow_pages": [
            "https://www.yellowpages.com/search?search_terms={kw}",
            "https://www.bbb.org/search?find_country=USA&find_text={kw}",
        ],
        "tender_platforms": ["sam.gov", "govtribe.com"],
        "default_proxy": "clash",
        "certification_needed": ["ASTM", "IBC"],
        "risk_level": "low",
    },
    "china": {
        "aliases": ["中国", "China", "cn"],
        "domain": ".cn", "lang": "zh",
        "google_cc": "China",
        "search_queries": [
            "{product} 中国出口商", "{product} 厂家供应商",
            "{product} 外贸公司", "{product} manufacturer China",
            "{product} supplier export",
        ],
        "yellow_pages": [
            "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={kw}",
            "https://www.made-in-china.com/manufacturers/{kw_slug}.html",
        ],
        "default_proxy": "direct",
        "certification_needed": ["ISO", "CE"],
        "risk_level": "low",
    },
}

# ═══════════════════════════════════════════════════════════════
# 智能自动化引擎
# ═══════════════════════════════════════════════════════════════

class SearchAutomation:
    """
    智能搜索自动化引擎
    
    动态识别 → 智能配置 → 自动执行 → 监控循环
    """
    
    def __init__(self):
        self.pen = PenetratingSearch()
        self.workspace = Path.home() / ".openclaw" / "workspace"
        self.data_dir = self.workspace / "data" / "search-automation"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def detect_country(self, query: str) -> tuple:
        """从查询/上下文中自动识别目标国家"""
        query_lower = query.lower()
        
        # 精确匹配别名
        for code, profile in COUNTRY_PROFILES.items():
            for alias in profile["aliases"]:
                if alias.lower() in query_lower:
                    return code, profile
        
        # 域名匹配
        domain_match = re.search(r'\.([a-z]{2})\b', query_lower)
        if domain_match:
            tld = domain_match.group(1)
            for code, profile in COUNTRY_PROFILES.items():
                if profile.get("domain", "").lstrip(".") == tld:
                    return code, profile
        
        # 城市匹配
        city_map = {"riyadh": "saudi_arabia", "jeddah": "saudi_arabia", "dammam": "saudi_arabia",
                    "dubai": "uae", "abu dhabi": "uae", "sharjah": "uae",
                    "baghdad": "iraq", "basra": "iraq",
                    "doha": "qatar", "sydney": "australia", "melbourne": "australia"}
        for city, code in city_map.items():
            if city in query_lower:
                return code, COUNTRY_PROFILES[code]
        
        # 默认: 未识别则返回 None
        return None, None
    
    def build_search_plan(self, product: str, country_code: str) -> dict:
        """根据国家和产品动态生成搜索计划"""
        profile = COUNTRY_PROFILES.get(country_code, {})
        
        # 生成搜索词
        queries = [q.format(product=product) for q in profile.get("search_queries", [])]
        
        # 添加黄页搜索
        from urllib.parse import quote
        kw = quote(f"{product}")
        for yp_url in profile.get("yellow_pages", []):
            queries.append(yp_url.format(kw=kw))
        
        plan = {
            "product": product,
            "country": country_code,
            "country_name": profile.get("aliases", [country_code])[0],
            "search_queries": queries,
            "tender_platforms": profile.get("tender_platforms", []),
            "proxy_mode": profile.get("default_proxy", "clash"),
            "certification_needed": profile.get("certification_needed", []),
            "risk_level": profile.get("risk_level", "medium"),
            "language_hint": profile.get("language_hint", []),
            "estimated_buyers": 0,
        }
        return plan
    
    def run_sweep(self, product: str, country: str = "") -> dict:
        """
        智能扫描一个产品+国家的买家
        
        自动识别国家 → 生成搜索计划 → 穿透式执行 → 入库
        """
        # 1. 自动识别国家
        country_code, profile = self.detect_country(country or product)
        if not country_code:
            return {"status": "error", "message": f"无法识别国家: {country or product}"}
        
        print(f"\n🌍 识别到国家: {profile['aliases'][0]} ({country_code})")
        
        # 2. 生成搜索计划
        plan = self.build_search_plan(product, country_code)
        print(f"📋 搜索计划: {len(plan['search_queries'])} 个查询")
        
        # 3. 开始穿透式搜索
        from scraper_v4 import search_buyers as crawl_buyers
        all_results = []
        seen_companies = set()
        
        for i, query in enumerate(plan["search_queries"]):
            print(f"  🔍 [{i+1}/{len(plan['search_queries'])}] {query[:40]}...")
            try:
                # Step 1: 爬虫搜买家名单
                raw = crawl_buyers(query, region=country_code, count=15)
                for item in raw:
                    name = item.get("company", item.get("title", ""))
                    if name and len(name) > 3 and name not in seen_companies:
                        seen_companies.add(name)
                        
                        # Step 2: 穿透式提取联系方式
                        info = self.pen.find_company(name, 
                            country=profile.get("aliases", [""])[0])
                        all_results.append(info)
                        status = "✅" if info["verified"] else "⚠️"
                        print(f"    {status} {name[:35]} | {info['confidence']*100:.0f}%")
            except Exception as e:
                print(f"    ❌ {e}")
        
        # 4. 排序 + 统计
        all_results.sort(key=lambda x: x["confidence"], reverse=True)
        verified = [r for r in all_results if r["verified"]]
        
        report = {
            "status": "success",
            "product": product,
            "country": country_code,
            "country_name": plan["country_name"],
            "total_buyers_found": len(seen_companies),
            "verified_buyers": len(verified),
            "verified_rate": f"{len(verified)/max(len(all_results),1)*100:.0f}%",
            "search_plan": plan,
            "buyers": all_results[:20],
            "recommendations": [],
        }
        
        # 5. 自动推荐
        if verified:
            report["recommendations"].append(f"发现 {len(verified)} 个已验证买家，建议优先跟进")
        if all_results and not verified:
            report["recommendations"].append("找到潜在买家名单但联系方式不足，建议补充 LinkedIn 搜索")
        if plan["certification_needed"]:
            report["recommendations"].append(
                f"进入 {plan['country_name']} 需认证: {', '.join(plan['certification_needed'])}")
        
        # 6. 缓存结果
        cache_key = hashlib.md5(f"{product}:{country_code}".encode()).hexdigest()[:12]
        cache_file = self.data_dir / f"sweep-{cache_key}.json"
        cache_file.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(f"\n💾 已缓存: {cache_file.name}")
        
        return report
    
    def monitor_all(self, products: list = None) -> List[dict]:
        """监控多个产品+国家组合"""
        if not products:
            products = [
                "steel structure foldable house",
                "prefab house",
                "modular building",
            ]
        
        reports = []
        for product in products:
            # 自动识别国家对所有支持的都扫一遍
            for country_code in ["saudi_arabia", "uae", "iraq", "qatar", "australia"]:
                print(f"\n{'='*50}")
                print(f"扫描: {product} @ {country_code}")
                print(f"{'='*50}")
                try:
                    r = self.run_sweep(product, country_code)
                    r["target"] = f"{product} @ {country_code}"
                    reports.append(r)
                except Exception as e:
                    print(f"❌ 失败: {e}")
        
        return reports


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    auto = SearchAutomation()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "sweep":
            product = " ".join(sys.argv[2:4]) if len(sys.argv) > 3 else " ".join(sys.argv[2:])
            country = sys.argv[4] if len(sys.argv) > 4 else ""
            result = auto.run_sweep(product, country)
            print(f"\n📊 扫描完成")
            print(f"   买家总数: {result['total_buyers_found']}")
            print(f"   已验证: {result['verified_buyers']}")
            for r in result.get("recommendations", []):
                print(f"   💡 {r}")
        
        elif cmd == "monitor":
            products = sys.argv[2:] if len(sys.argv) > 2 else None
            reports = auto.monitor_all(products)
            total = sum(r["total_buyers_found"] for r in reports)
            verified = sum(r["verified_buyers"] for r in reports)
            print(f"\n{'='*50}")
            print(f"📊 全量监控完成")
            print(f"   扫描组合: {len(reports)} 个")
            print(f"   买家总数: {total}")
            print(f"   已验证: {verified}")
            for r in reports[:5]:
                print(f"   {r['country']:15s} | {r['product'][:20]:20s} | {r['verified_buyers']}个已验证")
        
        elif cmd == "countries":
            print("\n支持的国家/地区:")
            for code, profile in sorted(COUNTRY_PROFILES.items()):
                names = " / ".join(profile["aliases"][:3])
                risk = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(profile["risk_level"], "⚪")
                certs = ",".join(profile.get("certification_needed", ["无"]))
                print(f"  {risk} {names:25s} | 域名{profile['domain']:5s} | 认证: {certs}")
        
        else:
            print("用法: python3 search_automation.py <sweep|monitor|countries> [参数]")
    else:
        # demo
        print("=" * 50)
        print("  太一智能搜索自动化 v1.0")
        print("  动态识别 · 智能配置 · 自动执行")
        print("=" * 50)
        print("\n命令:")
        print("  sweep <产品> [国家]    — 智能扫描买家")
        print("  monitor [产品列表]     — 全量监控多个市场")
        print("  countries             — 查看支持的国家列表")
        print("\n示例:")
        print("  python3 search_automation.py sweep \"foldable house\" \"Saudi\"")
        print("  → 自动识别沙特 → 配置阿拉伯语搜索 → 穿透式提取联系方式")