"""company-enricher 增强补丁 - 2026-05-05"""

import re
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse

# 扩展爬虫：多页面+国际电话格式
ADDITIONAL_PHONE_PATTERNS = [
    r'\+966[\s\-]?\d[\s\-]?\d{3}[\s\-]?\d{4}',   # 沙特
    r'\+971[\s\-]?\d[\s\-]?\d{3}[\s\-]?\d{4}',   # 阿联酋
    r'\+974[\s\-]?\d[\s\-]?\d{3}[\s\-]?\d{4}',   # 卡塔尔
    r'\+965[\s\-]?\d[\s\-]?\d{3}[\s\-]?\d{4}',   # 科威特
    r'\+968[\s\-]?\d[\s\-]?\d{3}[\s\-]?\d{4}',   # 阿曼
    r'\+86[\s\-]?\d{3}[\s\-]?\d{4}[\s\-]?\d{4}', # 中国
]

def scrape_deep(ce_instance, base_url: str) -> dict:
    """深度爬取：主页+Contact Us页+About Us页
    不依赖ce_instance（兼容直接调用和管道调用）
    """
    results = {"phone_numbers": [], "emails": [], "addresses": [], "linkedin": None}
    
    pages = [base_url]
    # 尝试常用联系页面路径
    for path in ["/contact", "/contact-us", "/contactus", "/about", "/about-us"]:
        pages.append(urljoin(base_url, path))
    
    seen_emails = set()
    seen_phones = set()
    
    for page_url in set(pages):
        try:
            req = Request(page_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urlopen(req, timeout=8) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            # 邮箱
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
            skip = {'example.com', 'domain.com', 'noreply@', 'no-reply@', 'donotreply@'}
            for e in emails:
                if e.lower() not in seen_emails and not any(s in e.lower() for s in skip):
                    # 跳过太长的（可能是base64编码）
                    if len(e) < 60:
                        results["emails"].append(e)
                        seen_emails.add(e.lower())
            
            # 电话（全部格式）
            all_phone_patterns = [
                r'\+[\d\s\-\(\)]{7,20}',
                r'0\d[\s\-]?\d{4}[\s\-]?\d{4}',
                r'1[38]00[\s\-]?\d{3}[\s\-]?\d{3}',
                r'\(\d{2,4}\)[\s\-]?\d{3,4}[\s\-]?\d{3,4}',
            ]
            for pat in all_phone_patterns:
                phones = re.findall(pat, html)
                for p in phones:
                    p_clean = p.strip()
                    if p_clean not in seen_phones and len(p_clean) > 6:
                        results["phone_numbers"].append(p_clean)
                        seen_phones.add(p_clean)
            
            # LinkedIn链接
            linkedin = re.findall(r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[^\s"\'<>]+', html)
            if linkedin and not results["linkedin"]:
                results["linkedin"] = linkedin[0]
                
        except Exception:
            continue  # 某个页面失败继续下一个
    
    return results


def generate_linkedin_people_search(company_name: str, roles: list = None) -> dict:
    """为一家公司生成LinkedIn人物搜索（8角色）"""
    if roles is None:
        roles = [
            "Business Development Manager",
            "Sales Director", 
            "Procurement Manager",
            "Purchasing Manager",
            "Supply Chain Director",
            "CEO",
            "General Manager",
            "Founder"
        ]
    
    from urllib.parse import quote_plus
    searches = {}
    for role in roles:
        kw = quote_plus(f"{company_name} {role}")
        searches[role] = f"https://www.linkedin.com/search/results/people/?keywords={kw}"
    
    return {
        "company": company_name,
        "total_searches": len(roles),
        "linkedin_people_links": searches,
        "note": "LinkedIn禁止自动爬取，请手动点开链接查看真实联系人"
    }
