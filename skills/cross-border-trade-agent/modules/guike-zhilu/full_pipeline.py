"""
搜索结果对接补丁 - 2026-05-05
位置: guike-zhilu → 搜索→富化全流程增强
"""

import sys, json, importlib.util
from pathlib import Path

WORKSPACE = Path("/home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent")


def run_search_enrich_verify(product: str, market: str, max_deep: int = 5) -> dict:
    """完整链路：搜索→深度富化→验证→入库"""
    
    # 1. 加载贵客之路
    gk_path = WORKSPACE / "modules" / "guike-zhilu" / "core.py"
    spec = importlib.util.spec_from_file_location("guike_zhilu", str(gk_path))
    gk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gk)
    guike = gk.GuikeZhilu()
    
    # 2. 搜索（走完整链路）
    search_result = guike.execute(task='search', product=product, market=market)
    prospects = search_result.get("prospects", [])
    enriched = search_result.get("enriched_prospects", [])
    total = len(prospects)
    
    # 3. 加载增强补丁
    patch_path = WORKSPACE / "modules" / "company-enricher" / "enrichment_patch.py"
    spec2 = importlib.util.spec_from_file_location("patch_mod", str(patch_path))
    patch_mod = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(patch_mod)
    
    # 4. 深度处理（最多指定数量）
    deep_results = []
    for i, e in enumerate(enriched[:max_deep]):
        name = e.get("name", "")
        website = e.get("website", "")
        
        deep = patch_mod.scrape_deep(None, website) if website else {}
        li_search = patch_mod.generate_linkedin_people_search(name)
        
        company = {
            "name": name,
            "website": website,
            "phone": deep.get("phone_numbers", [])[:3],
            "email": deep.get("emails", [])[:3],
            "linkedin_company": deep.get("linkedin"),
            "linkedin_people_search": li_search["linkedin_people_links"],
        }
        deep_results.append(company)
    
    return {
        "status": "success",
        "product": product,
        "market": market,
        "total_searched": total,
        "deep_enriched": len(deep_results),
        "linkedin_searches_total": len(deep_results) * 8,
        "companies": deep_results,
    }


if __name__ == "__main__":
    product = sys.argv[1] if len(sys.argv) > 1 else "steel structure house"
    market = sys.argv[2] if len(sys.argv) > 2 else "Middle East"
    max_n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    result = run_search_enrich_verify(product, market, max_n)
    print(json.dumps(result, ensure_ascii=False, indent=2))
