"""
自动爬虫搜客引擎 — 无需人工点击，自动搜公司真实信息
2026-05-05

自动链路：
搜索产品+市场 → 找到公司 → 爬官网 → 爬黄页 → 搜LinkedIn → 搜邮箱 → 入库
"""

import re, json, sys
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, urljoin
from typing import Dict, List, Optional
from pathlib import Path

# 加载scrapling（如可用）
try:
    SCRAPLING_AVAILABLE = False
    scrapling_path = Path("/home/sayelf/.openclaw/workspace/skills/scrapling-integration/scrapling_safe.py")
    if scrapling_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("scrapling_safe", str(scrapling_path))
        scrapling_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scrapling_mod)
        SafeFetcher = scrapling_mod.SafeFetcher
        SCRAPLING_AVAILABLE = True
except Exception:
    SafeFetcher = None


# ==================== 1. 搜索引擎自动搜公司 ====================

def search_companies_auto(product: str, market: str) -> List[Dict]:
    """自动搜公司：DDG + Google + 黄页"""
    seen_urls = set()
    companies = []
    
    # 查询列表
    queries = [
        f"{product} company {market} contact",
        f"{product} manufacturer {market} email phone",
        f"{product} supplier {market}",
        f"{market} {product} company",
    ]
    
    for query in queries:
        try:
            results = search_duckduckgo(query, max_results=5)
            for r in results:
                url = r.get("url", "")
                title = r.get("title", "")
                if url and url not in seen_urls and not is_noise_url(url, title):
                    seen_urls.add(url)
                    companies.append({"name": title, "url": url, "source": query})
        except Exception:
            continue
    
    return companies


def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict]:
    """反爬搜索 — 使用太一共享搜索Agent"""
    try:
        import importlib.util as iu
        path = str(Path(__file__).resolve().parent.parent.parent.parent.parent /
                   "skills" / "shared-search-agent" / "core.py")
        spec = iu.spec_from_file_location("shared_search", path)
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        engine = mod.get_search_engine()
        
        # Search for company info
        result = engine.search_company(query) if " " in query else engine.search(query)
        
        # Convert to expected format
        results = []
        for email in result.get("emails", [])[:max_results]:
            results.append({"title": email, "url": f"mailto:{email}"})
        for link in result.get("linkedin", [])[:max_results]:
            results.append({"title": link.split("/")[-1] if "/" in link else link, "url": link})
        return results
    except Exception as e:
        print(f"[search_duckduckgo] error: {e}")
        return []


def is_noise_url(url: str, title: str) -> bool:
    """过滤噪音链接（搜索页/聚合页/视频等）"""
    noise = ['google.com/search', 'youtube.com', 'facebook.com', 'twitter.com', 
             'pinterest', 'instagram', 'wikipedia.org', 'amazon.com/s?',
             'shopping', 'news.google']
    return any(n in url.lower() for n in noise)


# ==================== 2. 自动爬官网提取联系方式 ====================

def extract_contacts_from_website(base_url: str) -> Dict:
    """自动爬官网+Contact页，提取电话/邮箱/LinkedIn"""
    result = {"phone": [], "email": [], "linkedin": None}
    
    pages_to_try = [base_url]
    for path in ["/contact", "/contact-us", "/about", "/about-us", "/contactus"]:
        pages_to_try.append(urljoin(base_url, path))
    
    phone_pattern = re.compile(r'(\+[\d\s\-\(\)]{7,20}|0\d[\s\-]?\d{3,4}[\s\-]?\d{3,4}|1[38]00[\s\-]?\d{3}[\s\-]?\d{3})')
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    linkedin_pattern = re.compile(r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[^\s"\'<>]+')
    
    seen_emails = set()
    
    for page_url in pages_to_try:
        try:
            if SCRAPLING_AVAILABLE and SafeFetcher:
                fetcher = SafeFetcher()
                resp = fetcher.get(page_url)
                html = resp.text
            else:
                req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urlopen(req, timeout=8) as resp:
                    html = resp.read().decode('utf-8', errors='ignore')
            
            # 提取电话
            phones = phone_pattern.findall(html)
            for p in phones:
                p = p.strip().rstrip(')').rstrip('-')
                if p not in result["phone"] and len(p) > 6:
                    result["phone"].append(p)
            
            # 提取邮箱
            emails = email_pattern.findall(html)
            skip = {'example.com', 'domain.com', 'noreply@', 'no-reply@', 'donotreply@'}
            for e in emails:
                e_lower = e.lower()
                if e_lower not in seen_emails and not any(s in e_lower for s in skip) and len(e) < 60:
                    result["email"].append(e)
                    seen_emails.add(e_lower)
            
            # 提取LinkedIn
            if not result["linkedin"]:
                li = linkedin_pattern.findall(html)
                if li:
                    result["linkedin"] = li[0]
                    
        except Exception:
            continue
    
    result["phone"] = result["phone"][:5]
    result["email"] = result["email"][:5]
    return result


# ==================== 3. 自动搜黄页/工商信息 ====================

def search_business_directory(company_name: str, market: str) -> Dict:
    """搜索黄页获取公司信息"""
    result = {"phone": [], "email": [], "address": []}
    
    # 尝试搜索公司名在黄页上
    for domain in [f"https://www.yellowpages.com.au/search/listings?clue={quote_plus(company_name)}",
                   f"https://www.yellowpages.com/search?search_terms={quote_plus(company_name)}",
                   f"https://www.yell.com/ucs/UcsSearchAction.do?keywords={quote_plus(company_name)}"]:
        try:
            req = Request(domain, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req, timeout=8) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            # 提取电话
            phones = re.findall(r'(?:(?:\+?61)|(?:\+?1)|(?:\+?44))[\s\-]?\d[\s\-]?\d{3,4}[\s\-]?\d{3,4}', html)
            for p in phones:
                if p not in result["phone"]:
                    result["phone"].append(p.strip())
            
            # 提取邮箱
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
            skip = {'example.com', 'noreply@'}
            for e in emails:
                if e.lower() not in [x.lower() for x in result["email"]] and not any(s in e.lower() for s in skip):
                    result["email"].append(e)
        except Exception:
            continue
    
    return result


# ==================== 4. 全自动搜客 ====================

def auto_search_company_info(product: str, market: str, max_companies: int = 8) -> Dict:
    """全自动搜客：搜公司→爬官网→搜黄页→入库"""
    
    # Step 1: 自动搜公司
    companies_found = search_companies_auto(product, market)
    print(f"自动搜索到 {len(companies_found)} 家公司")
    
    # Step 2: 过滤和去重
    seen = set()
    unique_companies = []
    for c in companies_found:
        domain = c['url'].split('/')[2] if '://' in c['url'] else c['url']
        if domain not in seen:
            seen.add(domain)
            unique_companies.append(c)
    
    print(f"去重后 {len(unique_companies)} 家")
    
    # Step 3: 逐家爬取联系信息
    enriched = []
    for i, company in enumerate(unique_companies[:max_companies]):
        name = company['name']
        url = company['url']
        print(f"  [{i+1}/{min(max_companies,len(unique_companies))}] 处理: {name}")
        
        contacts = extract_contacts_from_website(url)
        directory = search_business_directory(name, market)
        
        all_phones = list(set(contacts["phone"] + directory["phone"]))
        all_emails = list(set(contacts["email"] + directory["email"]))
        
        enriched.append({
            "name": name,
            "website": url,
            "phone": all_phones,
            "email": all_emails,
            "linkedin": contacts.get("linkedin"),
            "address": directory.get("address", []),
        })
        
        print(f"    电话: {all_phones[:3] if all_phones else '未找到'}")
        print(f"    邮箱: {all_emails[:3] if all_emails else '未找到'}")
        print(f"    LinkedIn: {contacts.get('linkedin','未找到')}")
    
    return {
        "market": market,
        "product": product,
        "total_found": len(companies_found),
        "total_enriched": len(enriched),
        "companies": enriched,
    }


if __name__ == "__main__":
    product = sys.argv[1] if len(sys.argv) > 1 else "steel structure foldable house"
    market = sys.argv[2] if len(sys.argv) > 2 else "Saudi Arabia"
    result = auto_search_company_info(product, market, 5)
    print(json.dumps(result, ensure_ascii=False, indent=2))
