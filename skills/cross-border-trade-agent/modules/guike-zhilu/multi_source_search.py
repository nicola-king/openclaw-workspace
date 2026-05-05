"""
多源搜索引擎 — 国家自动适配版
2026-05-05

当搜索任何国家时，自动适配该国搜索资源：
├── 搜索引擎 (Google/Bing/DuckDuckGo)
├── 该国商业黄页/工商注册
├── 该国LinkedIn网络
├── 电商/贸易平台
├── Google Maps 该国定位
└── 该国特定验证源
"""

from urllib.parse import quote_plus
from typing import Dict, List

# ==================== 国家数据库 ====================

COUNTRY_DB = {
    "australia": {
        "domain": ".au",
        "google_cc": "Australia",
        "maps_center": "-25,134,4z",
        "directories": {
            "yellow_pages": "https://www.yellowpages.com.au/search/listings?clue={kw}",
            "abn_lookup": "https://abr.business.gov.au/SearchByKeyword?Keyword={kw}",
            "true_local": "https://www.truelocal.com.au/find/{kw}",
        },
        "trade": {
            "prefabaus": "https://www.prefabaus.org.au/search?q={kw}",
        },
        "lang": "en",
    },
    "saudi arabia": {
        "domain": ".sa",
        "google_cc": "Saudi+Arabia",
        "maps_center": "24,45,5z",
        "directories": {
            "saudi_business": "https://www.google.com/search?q={kw}+site:sa",
            "saudi_yellow": "https://www.google.com/search?q={kw}+%D8%AF%D9%84%D9%8A%D9%84+%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9",
        },
        "lang": "en,ar",
    },
    "uae": {
        "domain": ".ae",
        "google_cc": "UAE",
        "maps_center": "24,54,6z",
        "directories": {
            "uae_business": "https://www.google.com/search?q={kw}+site:ae",
            "uae_yellow": "https://www.yellowpages.ae/search/{kw}.html",
        },
        "lang": "en,ar",
    },
    "qatar": {
        "domain": ".qa",
        "google_cc": "Qatar",
        "maps_center": "25.3,51.2,9z",
        "directories": {
            "qatar_business": "https://www.google.com/search?q={kw}+site:qa",
        },
        "lang": "en,ar",
    },
    "usa": {
        "domain": ".us",
        "google_cc": "USA",
        "maps_center": "39.8,-95.5,4z",
        "directories": {
            "yellow_pages": "https://www.yellowpages.com/search?search_terms={kw}",
            "bbb": "https://www.bbb.org/search?find_country=USA&find_text={kw}",
        },
        "lang": "en",
        "alias": ["us", "united states", "america"],
    },
    "uk": {
        "domain": ".uk",
        "google_cc": "UK",
        "maps_center": "55.3,-3.4,5z",
        "directories": {
            "yell": "https://www.yell.com/ucs/UcsSearchAction.do?keywords={kw}",
            "companies_house": "https://find-and-update.company-information.service.gov.uk/search?q={kw}",
        },
        "lang": "en",
        "alias": ["united kingdom", "britain", "england"],
    },
    "canada": {
        "domain": ".ca",
        "google_cc": "Canada",
        "maps_center": "56.1,-106.3,4z",
        "directories": {
            "yellow_pages_ca": "https://www.yellowpages.ca/search/si/1/{kw}",
        },
        "lang": "en,fr",
    },
    "new zealand": {
        "domain": ".nz",
        "google_cc": "New+Zealand",
        "maps_center": "-41,174,5z",
        "directories": {
            "yellow_pages_nz": "https://www.yellowpages.co.nz/search/?q={kw}",
            "nzbn": "https://www.nzbn.govt.nz/search/?query={kw}",
        },
        "lang": "en",
        "alias": ["nz"],
    },
    "germany": {
        "domain": ".de",
        "google_cc": "Germany",
        "maps_center": "51.1,10.5,6z",
        "directories": {
            "gelbe_seiten": "https://www.gelbeseiten.de/suche/{kw}",
        },
        "lang": "de,en",
    },
    "france": {
        "domain": ".fr",
        "google_cc": "France",
        "maps_center": "46.6,2.2,5z",
        "directories": {
            "pages_jaunes": "https://www.pagesjaunes.fr/recherche/{kw}",
        },
        "lang": "fr,en",
    },
    "china": {
        "domain": ".cn",
        "google_cc": "China",
        "maps_center": "35.8,104.2,4z",
        "directories": {
            "alibaba": "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={kw}",
            "made_in_china": "https://www.made-in-china.com/manufacturers/{kw_slug}.html",
            "1688": "https://www.1688.com/chanpin/{kw_encoded}.html",
        },
        "lang": "zh,en",
    },
}


# ==================== 国家解析 ====================

def resolve_country(market: str) -> str:
    """将用户输入的市场名解析为标准国家代码"""
    if not market:
        return "australia"
    
    m = market.lower().strip()
    
    # 别名映射
    alias_map = {}
    for code, info in COUNTRY_DB.items():
        alias_map[code] = code
        for alias in info.get("alias", []):
            alias_map[alias] = code
    
    if m in alias_map:
        return alias_map[m]
    
    # 模糊匹配
    for code, info in COUNTRY_DB.items():
        domain = info.get("domain", "")
        if domain and domain[1:] in m:  # .au .sa .ae etc
            return code
        if code in m:
            return code
    
    return m  # 返回原始输入，尝试通用搜索


# ==================== 动态搜索 ====================

def build_search_queries(product: str, market: str) -> list:
    """动态构建5次查询（自动适配国家）"""
    country_code = resolve_country(market)
    info = COUNTRY_DB.get(country_code, {})
    domain = info.get("domain", f".{country_code}")
    country_name = info.get("google_cc", market)
    
    return [
        f"{product} company {country_name}",
        f"{product} manufacturer supplier {country_name}",
        f"{product} builder contractor {country_name}",
        f"prefab {product} modular {country_name}",
        f"{product} {country_name} company",
    ]


def generate_search_links(product: str, market: str) -> dict:
    """动态生成多平台搜索链接（自动适配国家）"""
    country_code = resolve_country(market)
    info = COUNTRY_DB.get(country_code, {})
    domain = info.get("domain", "")
    
    kw = quote_plus(f"{product} {market}")
    kw_slug = product.replace(" ", "-")
    
    links = {
        "google": f"https://www.google.com/search?q={quote_plus(f'{product} company {market}')}",
        "bing": f"https://www.bing.com/search?q={quote_plus(f'{product} {market}')}",
        "linkedin_companies": f"https://www.linkedin.com/search/results/companies/?keywords={kw}",
        "alibaba": f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={kw}",
        "made_in_china": f"https://www.made-in-china.com/manufacturers/{kw_slug}.html",
        "global_sources": f"https://www.globalsources.com/manufacturers/{kw_slug}.html",
    }
    
    # 国家特定目录
    directories = info.get("directories", {})
    for name, url_tpl in directories.items():
        links[name] = url_tpl.format(kw=quote_plus(f"{product} {market}"), 
                                      kw_slug=kw_slug,
                                      kw_encoded=quote_plus(f"{product} {market}"))
    
    # Google Maps
    maps_center = info.get("maps_center", "")
    if maps_center:
        links["google_maps"] = f"https://www.google.com/maps/search/{quote_plus(f'{product} {market}')}/@{maps_center}"
    
    # 根据country_code新增市场特有搜索
    if country_code == "china" or domain == ".cn":
        links["1688"] = f"https://www.1688.com/chanpin/{quote_plus(product)}.html"
    
    return links


def generate_linkedin_people_searches(company: str, count: int = 8) -> list:
    """生成LinkedIn人物搜索（8角色）"""
    roles = [
        "Business Development Manager", "Sales Director",
        "Procurement Manager", "Purchasing Manager",
        "Supply Chain Director", "CEO",
        "General Manager", "Founder",
    ][:count]
    
    kw = quote_plus(company)
    return [{"role": r, "url": f"https://www.linkedin.com/search/results/people/"
                                  f"?keywords={kw}+{quote_plus(r)}&origin=GLOBAL_SEARCH_HEADER"} 
            for r in roles]


def build_enriched_result(companies: list, product: str, market: str) -> dict:
    """构建完整富化结果"""
    total_li = len(companies) * 8
    country_code = resolve_country(market)
    country_info = COUNTRY_DB.get(country_code, {})
    
    return {
        "product": product,
        "market": market,
        "country_resolved": country_code,
        "total_companies": len(companies),
        "total_linkedin_searches": total_li,
        "verified_sources": [
            "DuckDuckGo (5 queries × 5 results)",
            "Google Search", "Bing Search",
            "LinkedIn Companies", "LinkedIn People (8 roles)",
            f"{market} Business Directories",
            "Google Maps", "Alibaba / Made-in-China / Global Sources",
        ],
        "search_links": generate_search_links(product, market),
        "companies": companies,
        "summary": f"{len(companies)}家公司 × 8角色LinkedIn = {total_li}个人物搜索 → {market}",
    }
