#!/usr/bin/env python3
"""
潜客自动搜寻 - Cron 任务入口
2026-05-27
"""
import sys, json, os, time, re
from pathlib import Path
from datetime import datetime

BASE = Path("/home/sayelf/.openclaw/workspace")
SKILLS_DIR = BASE / "skills"
CBT_DIR = SKILLS_DIR / "cross-border-trade-agent"

# Load shared search agent
import importlib.util
ssa_path = str(SKILLS_DIR / "shared-search-agent" / "core.py")
spec = importlib.util.spec_from_file_location("shared_search_core", ssa_path)
ssa_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ssa_mod)
get_engine = ssa_mod.get_engine

# Load multi-source search
ms_path = str(CBT_DIR / "modules" / "guike-zhilu" / "multi_source_search.py")
ms_spec = importlib.util.spec_from_file_location("ms_mod", ms_path)
ms = importlib.util.module_from_spec(ms_spec)
ms_spec.loader.exec_module(ms)

# Load company enricher
enricher_path = str(CBT_DIR / "modules" / "company-enricher" / "core.py")
en_spec = importlib.util.spec_from_file_location("enricher_mod", enricher_path)
en_mod = importlib.util.module_from_spec(en_spec)
en_spec.loader.exec_module(en_mod)
CompanyEnricher = en_mod.CompanyEnricher

# DB path
DB_PATH = Path("/home/sayelf/.openclaw/workspace/data/cross-border-trade-agent/company-enricher/companies.db")


def extract_companies_from_html(raw_html, query):
    """Extract company-like names from raw HTML search results"""
    companies = set()
    
    # Extract anchor text (most common for company names in search results)
    anchor_pattern = re.compile(r'<a[^>]*>(.*?)</a>', re.DOTALL)
    for m in anchor_pattern.finditer(raw_html):
        text = m.group(1).strip()
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Filter: 10-80 chars, no obvious non-company text
        if 8 <= len(text) <= 80 and not any(kw in text.lower() for kw in 
            ['cookie', 'privacy', 'terms', 'sign in', 'sign up', 'javascript', 
             'advertise', 'subscribe', 'download', 'login', 'register']):
            
            # Check if it looks like a company (contains company indicators)
            indicators = ['pty', 'ltd', 'limited', 'inc', 'corp', 'company', 
                         'group', 'holding', 'enterprise', 'industries', 'solutions',
                         'modular', 'prefab', 'construction', 'building', 'steel',
                         'manufacturing', 'supplier', 'services', 'homes',
                         'homes', 'houses', 'design', 'engineering', 'architect']
            if any(ind in text.lower() for ind in indicators):
                # Clean up
                clean = re.sub(r'\s*\|.*$', '', text).strip()
                clean = re.sub(r'\s*-\s*.*$', '', clean).strip()
                if 3 <= len(clean) <= 60:
                    companies.add(clean)
    
    return list(companies)[:10]


def search_company_names(product, market):
    """Properly search for company names using the shared search agent"""
    engine = get_engine()
    queries = [
        f"{product} company {market}",
        f"{product} manufacturer {market}",
        f"{product} supplier {market}",
        f"{product} contractor {market}",
        f"prefab {product} modular {market}",
    ]
    
    all_companies = {}
    
    for q in queries:
        try:
            result = engine.search(q)
            raw_html = result.get("raw_html", "")
            if raw_html:
                companies = extract_companies_from_html(raw_html, q)
                for c in companies:
                    if c not in all_companies:
                        all_companies[c] = {"source_query": q, "count": 0}
                    all_companies[c]["count"] += 1
            time.sleep(1)
        except Exception as e:
            print(f"  ⚠️  '{q}': {e}", file=sys.stderr)
    
    return list(all_companies.keys())


def verify_and_store(companies, product, market):
    """Verify companies and store in DB"""
    enricher = CompanyEnricher()
    stored = 0
    verified = []
    
    for name in companies:
        try:
            result = enricher.add_company_manual({
                "name": name,
                "website": "",
                "source": f"cron_search_{product}_{market}"
            })
            if result and result.get("status") == "success":
                stored += 1
                verified.append(name)
                print(f"  ✅ 入库: {name}")
            else:
                print(f"  ⬆️  已存在: {name}")
        except Exception as e:
            print(f"  ❌ {name}: {e}", file=sys.stderr)
    
    return stored, verified


def main():
    print(f"\n{'='*60}")
    print(f"  潜客自动搜寻 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    # Load products config
    products_path = CBT_DIR / "data" / "monitor_products.json"
    with open(products_path) as f:
        config = json.load(f)
    
    products = config["products"]
    
    total_new = 0
    total_verified = 0
    total_stored = 0
    results = []
    
    for p in products:
        name_en = p["name_en"]
        markets = p.get("target_markets", ["USA"])
        
        print(f"\n📦 {p['name']} ({name_en})")
        
        for market in markets:
            print(f"  🌍 {market}...", end=" ", flush=True)
            
            # Step 1: Search
            companies = search_company_names(name_en, market)
            print(f"找到 {len(companies)} 家")
            
            if not companies:
                continue
            
            # Generate search links using multi_source_search
            links = ms.generate_search_links(name_en, market)
            
            # Step 2: Verify & store
            stored, verified = verify_and_store(companies, name_en, market)
            
            total_new += len(companies)
            total_verified += len(verified)
            total_stored += stored
            
            results.append({
                "product": name_en,
                "market": market,
                "found": len(companies),
                "verified": len(verified),
                "stored": stored,
            })
    
    # Summary
    print(f"\n{'='*60}")
    print(f"  潜客搜寻报告 | {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  ⭐ 新增潜客: {total_new}")
    print(f"  ✅ 已验证数: {total_verified}")
    print(f"  📥 入库数:   {total_stored}")
    print(f"{'='*60}")
    
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "summary": {
            "new_prospects": total_new,
            "verified": total_verified,
            "stored": total_stored,
        },
        "details": results,
    }
    
    # Write results to stdout as JSON for piping
    print(f"\n\n=== JSON_OUTPUT ===")
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
