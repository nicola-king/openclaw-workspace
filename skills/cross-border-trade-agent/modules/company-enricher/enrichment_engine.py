"""
富化 Agent 定制度增强 — 深度公司信息采集引擎
2026-05-05
集成位置：guike-zhilu → enrich() Step 1.5

执行链路：
搜索 → 深度爬取(多页) → 国际电话/邮箱 → LinkedIn公司页 → 8角色人物搜索 → 入库
"""

import re, json
from urllib.request import Request, urlopen
from urllib.parse import urljoin, quote_plus
from typing import Dict, List, Optional

# ==================== 1. 深度爬取（多页+多格式） ====================

CONTACT_PATHS = ["/contact", "/contact-us", "/contactus", "/contact_us", 
                 "/about", "/about-us", "/aboutus", "/team", "/company"]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# 全球电话格式
PHONE_PATTERNS = [
    r'\+61[\s\-]?\d[\s\-]?\d{4}[\s\-]?\d{4}',   # 澳洲
    r'\+966[\s\-]?\d[\s\-]?\d{3}[\s\-]?\d{4}',   # 沙特
    r'\+971[\s\-]?\d[\s\-]?\d{3}[\s\-]?\d{4}',   # 阿联酋
    r'\+974[\s\-]?\d[\s\-]?\d{3}[\s\-]?\d{4}',   # 卡塔尔
    r'\+86[\s\-]?\d{3}[\s\-]?\d{4}[\s\-]?\d{4}', # 中国
    r'\+1[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{4}',  # 美国/加拿大
    r'\+44[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{4}', # 英国
    r'\+49[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{4}', # 德国
    r'\+\d{2,3}[\s\-]?\d{2,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # 通用
    r'\(\d{2,4}\)[\s\-]?\d{3,4}[\s\-]?\d{3,4}',  # (区号)号码
    r'1300[\s\-]?\d{3}[\s\-]?\d{3}',
    r'1800[\s\-]?\d{3}[\s\-]?\d{3}',
    r'1[38]00\s?\d{3}\s?\d{3}',
]

SKIP_EMAILS = ['example.com', 'domain.com', 'noreply@', 'no-reply@', 
               'donotreply@', 'test@', 'wordpress@', 'demo@']


def scrape_deep(ce_instance, base_url: str) -> dict:
    """深度爬取：主页+Contact+About多页，提取电话/邮箱/LinkedIn"""
    
    if not base_url or not base_url.startswith('http'):
        return {"phone_numbers": [], "emails": [], "addresses": [], "linkedin": None}
    
    if '/search' in base_url or 'google.com' in base_url:
        return {"phone_numbers": [], "emails": [], "addresses": [], "linkedin": None}
    
    all_html = ""
    pages = [base_url] + [urljoin(base_url, p) for p in CONTACT_PATHS]
    
    for page_url in set(pages):
        try:
            req = Request(page_url, headers={'User-Agent': USER_AGENT}, method='GET')
            with urlopen(req, timeout=8) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                all_html += html
        except Exception:
            continue
    
    if not all_html:
        return {"phone_numbers": [], "emails": [], "addresses": [], "linkedin": None}
    
    # === 提取邮箱 ===
    emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', all_html))
    valid_emails = [e for e in emails 
                    if len(e) < 60 
                    and not any(s in e.lower() for s in SKIP_EMAILS)
                    and '.' in e.split('@')[1]]
    
    # === 提取电话 ===
    all_phones = set()
    for pat in PHONE_PATTERNS:
        phones = re.findall(pat, all_html)
        for p in phones:
            p_clean = p.strip().rstrip(')').rstrip('-').rstrip('.')
            if len(p_clean) > 6:
                all_phones.add(p_clean)
    
    # === 提取LinkedIn ===
    linkedin = re.findall(r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[^\s"\'<>]+', all_html)
    
    return {
        "phone_numbers": sorted(all_phones)[:5],
        "emails": valid_emails[:5],
        "addresses": [],
        "linkedin": linkedin[0] if linkedin else None,
    }


# ==================== 2. LinkedIn 8角色人物搜索 ====================

def generate_linkedin_people_search(company_name: str, category: str = None) -> dict:
    """生成LinkedIn人物搜索链接（按品类定制角色）"""
    
    # 品类定制角色映射
    CATEGORY_ROLES = {
        "steel_structure": [
            "Project Manager", "Procurement Manager", "Developer",
            "Construction Manager", "CEO", "General Manager",
            "Business Development Manager", "Operations Director"
        ],
        "transformer_energy": [
            "Electrical Engineer", "Asset Manager", "CEO",
            "Energy Manager", "CTO", "Investment Director",
            "Procurement Manager", "Technical Director"
        ],
        "auto_parts": [
            "Parts Manager", "Fleet Manager", "Buyer",
            "Sales Director", "Supply Chain Manager",
            "CEO", "Operations Manager", "Procurement Director"
        ],
        "default": [
            "Business Development Manager", "Sales Director",
            "Procurement Manager", "Purchasing Manager",
            "Supply Chain Director", "CEO",
            "General Manager", "Founder"
        ]
    }
    
    roles = CATEGORY_ROLES.get(category, CATEGORY_ROLES["default"])
    kw_company = quote_plus(company_name)
    
    searches = {}
    for role in roles:
        kw_role = quote_plus(role)
        searches[role] = (f"https://www.linkedin.com/search/results/people/"
                          f"?keywords={kw_company}+{kw_role}&origin=GLOBAL_SEARCH_HEADER")
    
    return {
        "company": company_name,
        "category": category or "default",
        "total_roles": len(roles),
        "searches": searches,
    }


# ==================== 3. 公司信息验证链接生成 ====================

def generate_verification_links(company_name: str, website: str = None, 
                                 source_url: str = None, source_query: str = None) -> dict:
    """生成公司验证链路"""
    kw = quote_plus(company_name)
    links = {
        "google": f"https://www.google.com/search?q={kw}",
        "linkedin_company": f"https://www.linkedin.com/search/results/companies/?keywords={kw}",
        "google_maps": f"https://www.google.com/maps/search/{kw}",
    }
    if website and website.startswith('http'):
        links["website"] = website
    if source_url:
        links["source"] = source_url
    return links


# ==================== 4. 数据质量评级 ====================

def assess_data_quality(company: dict) -> str:
    """评估数据质量等级"""
    score = 0
    if company.get('phone'): score += 25
    if company.get('email'): score += 25
    if company.get('address'): score += 15
    if company.get('website'): score += 15
    if company.get('linkedin_url'): score += 10
    if company.get('abn'): score += 10
    
    if score >= 80: return "A+"
    if score >= 60: return "A"
    if score >= 40: return "B"
    if score >= 20: return "C"
    return "D"
