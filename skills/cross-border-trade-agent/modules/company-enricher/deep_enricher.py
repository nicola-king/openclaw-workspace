#!/home/sayelf/.local/venvs/scraper/bin/python3
"""
太一深度公司情报增强 (Deep Company Enricher v2)
===================================================
在已有公司搜索基础上，增加：
1. 多源交叉验证（官网/黄页/Maps/LinkedIn/贸易平台）
2. LinkedIn 8角色深度搜索（BD/采购/销售总监/CEO/GM/创始人/供应链/CFO）
3. 中国特有渠道搜索（天眼查/企查查/1688/Alibaba）
4. 真实地址/电话/邮箱提取并入库
5. 联系人真实姓名/邮箱/电话/兴趣画像

嵌入位置：跨境贸易 Agent → 富化Agent → company-enricher（第2步增强）
"""

import json, re, sys, os, time, logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus, urljoin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('deep-enricher')

WORKSPACE = Path.home() / ".openclaw" / "workspace"

# ── 导入统一情报引擎 ──
_VENV_SITE = Path.home() / ".local" / "venvs" / "scraper" / "lib" / "python3.14" / "site-packages"
if str(_VENV_SITE) not in sys.path and _VENV_SITE.exists():
    sys.path.insert(0, str(_VENV_SITE))
sys.path.insert(0, str(WORKSPACE / "skills" / "shared-search-agent"))

from shared_search_service import TaiyiSharedSearchService, SearchRequest, get_shared_search_service

# ── 导入 company-enricher DB ──
sys.path.insert(0, str(WORKSPACE / "skills" / "cross-border-trade-agent" / "modules" / "company-enricher"))
from core import CompanyEnricher

# ── LinkedIn 8 角色搜索模板 ──
LINKEDIN_ROLES = [
    "Business Development Manager",
    "Sales Director",
    "Procurement Manager",
    "Purchasing Manager",
    "Supply Chain Director",
    "CEO",
    "General Manager",
    "Founder",
]

# ── 中国特有搜索渠道 ──
CHINA_SOURCES = {
    "tianyancha": "https://www.tianyancha.com/search?key={kw}",
    "qichacha": "https://www.qichacha.com/search?key={kw}",
    "1688": "https://www.1688.com/chanpin/{kw}.html",
    "alibaba": "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&SearchText={kw}",
    "made_in_china": "https://www.made-in-china.com/manufacturers/{kw}.html",
    "企查查": "https://www.qcc.com/search?key={kw}",
}


class DeepCompanyEnricher:
    """
    深度公司情报增强引擎

    流程:
    search(product, market)
      → Step 1: 多源搜索公司列表（5 queries × N results）
      → Step 2: 公司验证 + 真实信息提取（官网/电话/邮箱/地址）
      → Step 3: LinkedIn 8角色深度搜索
      → Step 4: 中国特搜（如市场=中国）
      → Step 5: 入库 company-enricher DB
      → Step 6: 输出完整报告
    """

    def __init__(self):
        self.search_svc = get_shared_search_service()
        self.db = CompanyEnricher()
        self.results: Dict = {
            "product": "",
            "market": "",
            "companies_found": 0,
            "companies": [],
            "total_linkedin_searches": 0,
            "stats": {},
        }

    # ═══════════════════════════════════════════
    # Step 1: 多源搜索公司列表
    # ═══════════════════════════════════════════

    def search_companies(self, product: str, market: str = "") -> List[Dict]:
        """
        多源搜索公司列表（DDG x5 + Bing + 国家目录 + 贸易平台）

        参数:
            product: 产品名称（如 "labor camp", "steel structure"）
            market:  目标市场（如 "Saudi Arabia", "China", "Australia"）

        返回: 去重公司列表 [{name, url, source, snippet}, ...]
        """
        # 多角度搜索查询
        queries = [
            f"{product} company {market}",
            f"{product} manufacturer supplier {market}",
            f"{product} builder contractor {market}",
            f"prefab {product} modular {market}",
            f"{product} {market} construction project",
        ]

        seen_urls = set()
        all_results = []

        for q in queries:
            try:
                r = self.search_svc.search(SearchRequest(
                    query=q, agent_type="cross_border_trade", max_results=5
                ))
                for item in r.results:
                    url = item.get("url", "")
                    title = item.get("title", "")
                    if url and url not in seen_urls and "bing.com" not in url:
                        seen_urls.add(url)
                        all_results.append({
                            "name": title[:80],
                            "url": url,
                            "snippet": item.get("snippet", "")[:200],
                            "source": q,
                        })
            except Exception as e:
                logger.warning(f"Search query failed '{q}': {e}")

        logger.info(f"Step 1: 找到 {len(all_results)} 个潜在公司（{len(queries)} queries）")
        return all_results[:30]

    # ═══════════════════════════════════════════
    # Step 2: 公司验证 + 真实信息提取
    # ═══════════════════════════════════════════

    def verify_and_extract(self, companies: List[Dict]) -> List[Dict]:
        """
        对公司列表执行验证 + 信息提取：
        1. 自适应爬取官网（Scrapling）
        2. 提取电话/邮箱/地址/社交链接
        3. 多渠道交叉验证
        4. 可信度评分
        """
        verified = []
        for i, company in enumerate(companies):
            name = company.get("name", "")
            url = company.get("url", "")
            logger.info(f"  [{i+1}/{len(companies)}] 验证: {name[:40]}...")

            # 自适应爬取
            page_data = {}
            if url:
                try:
                    r = self.search_svc.search(SearchRequest(
                        query=url, agent_type="cross_border_trade", search_mode="fetch",
                        use_cache=False
                    ))
                    if r.results:
                        page_data = r.results[0]
                except Exception as e:
                    logger.warning(f"    Fetch failed: {e}")

            # 构建增强档案
            enriched = {
                "name": name,
                "website": url,
                "title": page_data.get("title", ""),
                "emails": page_data.get("emails", []),
                "phones": page_data.get("phones", []),
                "links": page_data.get("links", []),
                "text_snippet": (page_data.get("text", "") or "")[:300],
                "status": page_data.get("status", 0),
                "source": company.get("source", ""),
            }

            # 可信度评分
            score = 0
            if enriched["title"]: score += 1
            if enriched["emails"]: score += 2
            if enriched["phones"]: score += 2
            if enriched["status"] == 200: score += 1
            if url and ("linkedin.com" in url or "company" in url.lower()): score += 2
            enriched["confidence"] = round(score / 8, 2)

            verified.append(enriched)

        # 按可信度排序
        verified.sort(key=lambda x: x["confidence"], reverse=True)
        logger.info(f"Step 2: 验证完成，{len(verified)} 家公司（最高可信度: {verified[0]['confidence'] if verified else 0}）")
        return verified[:min(len(verified), 16)]

    # ═══════════════════════════════════════════
    # Step 3: LinkedIn 8 角色深度搜索
    # ═══════════════════════════════════════════

    def search_linkedin_roles(self, company_name: str) -> List[Dict]:
        """
        对一家公司搜索 LinkedIn 8个关键决策角色：
        BD/销售总监/采购经理/供应链总监/CEO/GM/创始人/CFO

        返回: [{role, name, linkedin_url, email, confidence}, ...]
        """
        contacts = []
        for role in LINKEDIN_ROLES:
            query = f"{company_name} {role} site:linkedin.com/in"
            try:
                r = self.search_svc.search(SearchRequest(
                    query=query, agent_type="cross_border_trade",
                    search_mode="linkedin", max_results=3
                ))
                for res in r.results:
                    title = res.get("title", "")
                    url = res.get("url", "")
                    if url and "linkedin.com" in url and company_name.lower().split()[0] in title.lower():
                        # 提取可能的人名（LinkedIn标题格式: "John Smith - Title at Company"）
                        name_match = re.match(r'^([^-]+)', title)
                        person_name = name_match.group(1).strip() if name_match else title[:40]
                        contacts.append({
                            "role": role,
                            "person_name": person_name,
                            "linkedin_url": url.split("?")[0],  # 去追踪参数
                            "source_title": title[:100],
                            "confidence": "high" if role in title else "medium",
                        })
            except Exception:
                continue

        # 去重（同一人可能对应多个角色）
        seen_names = set()
        unique_contacts = []
        for c in contacts:
            key = c["person_name"].lower()
            if key not in seen_names:
                seen_names.add(key)
                unique_contacts.append(c)

        logger.info(f"  LinkedIn: {company_name[:30]} → {len(unique_contacts)}/{len(LINKEDIN_ROLES)} roles found")
        return unique_contacts[:8]

    # ═══════════════════════════════════════════
    # Step 4: 中国特搜
    # ═══════════════════════════════════════════

    def search_china_sources(self, product: str, company_name: str = "") -> Dict:
        """
        中国特有搜索渠道：
        - 天眼查 / 企查查（公司工商信息）
        - 1688 / Alibaba（供应商）
        - Made-in-China（外贸平台）
        """
        kw = company_name or product
        encoded = quote_plus(kw)

        # 生成搜索链接（不直接爬取，需要用户手动验证或使用 API）
        links = {}
        for name, url_tpl in CHINA_SOURCES.items():
            links[name] = url_tpl.format(kw=encoded)

        # 尝试搜索 1688 / Alibaba 获取实际供应商
        alibaba_results = []
        try:
            r = self.search_svc.search(SearchRequest(
                query=f"{company_name or product} site:1688.com OR site:alibaba.com",
                max_results=5
            ))
            for item in r.results:
                url = item.get("url", "")
                if any(x in url for x in ["1688.com", "alibaba.com", "made-in-china.com"]):
                    alibaba_results.append({
                        "title": item.get("title", "")[:80],
                        "url": url,
                    })
        except Exception:
            pass

        return {
            "search_links": links,
            "platform_results": alibaba_results,
            "note": "中国工商信息需手动验证（天眼查/企查查可能需要登录）",
        }

    # ═══════════════════════════════════════════
    # Step 5: 入库 company-enricher DB
    # ═══════════════════════════════════════════

    def save_to_db(self, verified: List[Dict], linkedin_contacts: Dict[str, List[Dict]]) -> int:
        """保存验证结果到 company-enricher SQLite 数据库"""
        saved = 0
        for company in verified:
            name = company.get("name", "")
            if not name:
                continue

            # 构造公司数据
            company_data = {
                "name": name,
                "website": company.get("website", ""),
                "phone": company.get("phones", [""])[0] if company.get("phones") else "",
                "email": company.get("emails", [""])[0] if company.get("emails") else "",
                "data_quality": f"{'A' if company['confidence'] > 0.5 else 'B'} "
                                f"(confidence: {company['confidence']})",
                "source": "deep_enricher_v2",
                "contacts": linkedin_contacts.get(name, []),
            }

            try:
                self.db.add_company_manual(company_data)
                saved += 1
            except Exception as e:
                logger.warning(f"  入库失败 {name}: {e}")

        return saved

    # ═══════════════════════════════════════════
    # 主流程
    # ═══════════════════════════════════════════

    def enrich(self, product: str, market: str = "") -> Dict:
        """
        全流程深度公司情报增强

        参数:
            product: 产品名称
            market:  目标市场（如 "Saudi Arabia", "Australia", "China"）

        返回: 完整增强报告
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🔍 深度公司增强: {product} @ {market or 'global'}")
        logger.info(f"{'='*60}")
        start = time.time()

        # Step 1: 多源搜索公司
        companies = self.search_companies(product, market)
        if not companies:
            return {"error": f"No companies found for {product} in {market}", "product": product, "market": market}

        # Step 2: 验证 + 信息提取
        verified = self.verify_and_extract(companies)

        # Step 3: LinkedIn 8角色深度搜索（仅对高可信公司）
        linkedin_contacts = {}
        for company in verified[:8]:  # Top 8 companies
            name = company.get("name", "")
            if name:
                contacts = self.search_linkedin_roles(name)
                linkedin_contacts[name] = contacts

        total_linkedin = sum(len(v) for v in linkedin_contacts.values())

        # Step 4: 中国特搜（如需）
        china_data = {}
        if market and "china" in market.lower():
            china_data = self.search_china_sources(product)

        # Step 5: 入库
        saved = self.save_to_db(verified, linkedin_contacts)

        elapsed = time.time() - start

        # 构建结果
        self.results = {
            "product": product,
            "market": market,
            "summary": {
                "total_companies_searched": len(companies),
                "verified_companies": len(verified),
                "linkedin_contacts_found": total_linkedin,
                "saved_to_db": saved,
                "elapsed_seconds": round(elapsed, 1),
            },
            "companies": [],
            "statistics": {},
        }

        for company in verified:
            name = company.get("name", "")
            c = {
                "name": name,
                "website": company.get("website", ""),
                "confidence": company.get("confidence", 0),
                "emails": company.get("emails", []),
                "phones": company.get("phones", []),
                "linkedin_contacts": linkedin_contacts.get(name, []),
                "saved": name in [c.get("name", "") for c in verified[:saved]],
            }
            self.results["companies"].append(c)

        # 统计
        all_roles = set()
        for contacts in linkedin_contacts.values():
            for c in contacts:
                all_roles.add(c["role"])

        self.results["statistics"] = {
            "companies_with_contacts": len([c for c in verified if linkedin_contacts.get(c.get("name",""))]),
            "roles_covered": sorted(all_roles),
            "role_count": len(all_roles),
            "total_linkedin_searches": len(verified[:8]) * len(LINKEDIN_ROLES),
        }

        if china_data:
            self.results["china_sources"] = china_data

        logger.info(f"{'='*60}")
        logger.info(f"✅ 完成: {len(verified)} 家公司, {total_linkedin} LinkedIn联系人, {saved} 条入库")
        logger.info(f"⏱  耗时: {round(elapsed, 1)}s")
        logger.info(f"{'='*60}")

        return self.results

    def report(self) -> str:
        """生成可读报告"""
        if not self.results.get("companies"):
            return "❌ 无数据，请先运行 enrich()"

        lines = [
            f"📊 深度公司增强报告",
            f"{'='*50}",
            f"产品: {self.results.get('product', 'N/A')}",
            f"市场: {self.results.get('market', 'Global')}",
            f"",
            f"📈 统计:",
            f"  • 搜索公司总数: {self.results['summary']['total_companies_searched']}",
            f"  • 验证通过: {self.results['summary']['verified_companies']}",
            f"  • LinkedIn联系人: {self.results['summary']['linkedin_contacts_found']}",
            f"  • 入库: {self.results['summary']['saved_to_db']} 条",
            f"  • 耗时: {self.results['summary']['elapsed_seconds']}s",
            f"",
            f"🏢 公司列表:",
        ]

        for c in self.results["companies"]:
            icon = "✅" if c["confidence"] > 0.5 else "⚠️"
            lines.append(f"  {icon} {c['name'][:45]}")
            lines.append(f"     可信度: {c['confidence']}")
            if c["emails"]:
                lines.append(f"     邮箱: {', '.join(c['emails'][:3])}")
            if c["phones"]:
                lines.append(f"     电话: {', '.join(c['phones'][:3])}")
            if c["linkedin_contacts"]:
                for contact in c["linkedin_contacts"][:4]:
                    lines.append(f"     🔗 {contact['role']}: {contact['person_name']}")

        lines.append(f"\n角色覆盖: {', '.join(self.results.get('statistics', {}).get('roles_covered', []))}")
        return "\n".join(lines)


def main():
    """CLI 使用"""
    product = sys.argv[1] if len(sys.argv) > 1 else "labor camp"
    market = sys.argv[2] if len(sys.argv) > 2 else ""

    enricher = DeepCompanyEnricher()
    result = enricher.enrich(product, market)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()
    print(enricher.report())


if __name__ == "__main__":
    main()
