#!/usr/bin/env python3
"""
买家情报引擎 v3 — 联系人富化模块
提取公司官网的真实联系方式（邮箱/电话/负责人）
自动注入 buyer-intel 数据库
"""

import json, os, re, sys
from datetime import datetime
from pathlib import Path
import urllib.request
from html.parser import HTMLParser

BASE = Path.home() / ".openclaw" / "workspace"
BUYER_DB = BASE / "skills" / "cross-border-trade-agent" / "modules" / "buyer-intel" / "data" / "buyers.json"
CONTACT_CACHE = BASE / "data" / "cross-border" / "contact-cache"
CONTACT_CACHE.mkdir(parents=True, exist_ok=True)


class ContactExtractor:
    """从公司官网提取联系方式"""

    @staticmethod
    def fetch_html(url, timeout=10):
        """获取网页内容"""
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except:
            return None

    @staticmethod
    def extract_emails(html):
        """提取邮箱"""
        return list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)))

    @staticmethod
    def extract_phones(html, country="au"):
        """提取电话"""
        patterns = {
            "au": [r'1300[\s-]?[0-9]{3}[\s-]?[0-9]{3}',
                   r'0?4[0-9]{2}[\s-]?[0-9]{3}[\s-]?[0-9]{3}',
                   r'\+61[\s-]?[0-9][\s-]?[0-9]{4}[\s-]?[0-9]{4}'],
            "nz": [r'0?2[0-9][\s-]?[0-9]{3}[\s-]?[0-9]{4}',
                   r'0?[3-9][\s-]?[0-9]{3}[\s-]?[0-9]{4}',
                   r'\+64[\s-]?[0-9][\s-]?[0-9]{3}[\s-]?[0-9]{4}'],
            "global": [r'\+[\d][\d\s\-\(\)]{7,15}']
        }
        phones = []
        for pat in patterns.get(country, []) + patterns["global"]:
            phones.extend(re.findall(pat, html))
        return list(set(phones))

    @staticmethod
    def extract_contact_pages(html, base_url):
        """找联系页面URL"""
        urls = re.findall(r'href=["\']([^"\']*(?:contact|about|team)[^"\']*)["\']', html, re.I)
        from urllib.parse import urljoin
        return [urljoin(base_url, u) for u in urls if not u.startswith('#')]

    @staticmethod
    def extract_names(html):
        """提取负责人名称（在contact/team页面中的名字）"""
        # 找常见的头衔模式
        patterns = [
            r'(?:Director|CEO|Manager|Founder|Owner|Sales|Managing|Head)\s*(?:of)?\s*[:\-–\s]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*(?:–|-|—)\s*(?:Director|CEO|Manager|Founder|Owner|Sales)',
        ]
        names = []
        for pat in patterns:
            names.extend(re.findall(pat, html))
        return list(set(names))

    def enrich_company(self, name, url, country="au"):
        """对公司官网进行完整联系方式提取"""
        cache_key = re.sub(r'https?://', '', url).replace('/', '_').replace('.', '_')[:50]
        cache_path = CONTACT_CACHE / f"{cache_key}.json"

        # Check cache (7天有效)
        if cache_path.exists():
            age = datetime.now().timestamp() - os.path.getmtime(cache_path)
            if age < 604800:  # 7 days
                return json.load(open(cache_path))

        result = {
            "company": name,
            "url": url,
            "fetched_at": datetime.now().isoformat(),
            "emails": [],
            "phones": [],
            "contacts": [],
            "contact_page_found": False
        }

        print(f"  🔍 爬取: {name} ({url})")
        html = self.fetch_html(url)
        if not html:
            result["status"] = "unreachable"
            self._save_cache(cache_path, result)
            return result

        # 首页提取
        result["emails"] = self.extract_emails(html)
        result["phones"] = self.extract_phones(html, country)
        names = self.extract_names(html)

        # 找联系页面
        contact_urls = self.extract_contact_pages(html, url)
        if contact_urls:
            result["contact_page_found"] = True
            for cu in contact_urls[:3]:  # 最多爬3个联系页
                contact_html = self.fetch_html(cu)
                if contact_html:
                    result["emails"].extend(self.extract_emails(contact_html))
                    result["phones"].extend(self.extract_phones(contact_html, country))
                    names.extend(self.extract_names(contact_html))

        # 去重
        result["emails"] = list(set(result["emails"]))
        result["phones"] = list(set(result["phones"]))
        result["contacts"] = list(set(names))

        # 构建联系人列表
        result["people"] = []
        for name in result["contacts"][:10]:
            person = {"name": name}
            # 尝试匹配邮箱
            email_prefix = name.lower().split()[0] if name.split() else ""
            for e in result["emails"]:
                if email_prefix and email_prefix in e.lower():
                    person["email"] = e
                    break
            result["people"].append(person)

        result["status"] = "ok"
        self._save_cache(cache_path, result)
        return result

    def _save_cache(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def batch_enrich(self, companies):
        """批量富化"""
        results = []
        for c in companies:
            r = self.enrich_company(c["name"], c["url"], c.get("country", "au"))
            results.append(r)
        return results

    def inject_into_buyer_db(self, companies_data, product="钢结构折叠集成房屋"):
        """将富化后的联系人数据注入买家情报数据库"""
        buyers = []
        if BUYER_DB.exists():
            buyers = json.load(open(BUYER_DB))

        for cd in companies_data:
            if cd.get("status") != "ok":
                continue
            buyer = {
                "id": f"BUY-WEB-{datetime.now().strftime('%y%m%d')}-{len(buyers)+1:03d}",
                "type": "company",
                "project_name": cd["company"],
                "project_brief": f"通过官网爬取获取的{product}潜在买家",
                "source": "官网公开信息",
                "confirmed": True,
                "contacts": [],
                "url": cd["url"],
                "location": "",
                "sectors": [product],
                "buyer_type": "进口商/分销商/建筑商",
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }

            # 联系人
            for person in cd.get("people", []):
                contact = {"name": person["name"]}
                if person.get("email"):
                    contact["email"] = person["email"]
                buyer["contacts"].append(contact)

            # 邮箱（如果没有匹配到具体联系人的）
            for e in cd.get("emails", []):
                if not any(e == c.get("email") for c in buyer["contacts"]):
                    buyer["contacts"].append({"name": "通用", "email": e})

            # 电话
            if cd.get("phones"):
                buyer["phones"] = cd["phones"]

            buyers.append(buyer)

        with open(BUYER_DB, "w", encoding="utf-8") as f:
            json.dump(buyers, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 已注入 {len([c for c in companies_data if c.get('status')=='ok'])} 条联系人到 buyer-intel 数据库")
        print(f"   数据库总记录: {len(buyers)}")


# === 入口 ===
if __name__ == "__main__":
    extractor = ContactExtractor()

    # 澳大利亚+新西兰钢结构房屋潜在买家列表
    companies = [
        {"name": "Kiwi Modular Structures", "url": "https://kiwimodularstructures.com/", "country": "nz"},
        {"name": "Expanders NZ", "url": "https://www.expanders.co.nz/", "country": "nz"},
        {"name": "LGS Solutions", "url": "https://www.lgssolutions.com.au/", "country": "au"},
        {"name": "Cargo Connect", "url": "https://www.cargoconnect.com.au/", "country": "au"},
        {"name": "ACS Steel Construction", "url": "https://acsteelconstruction.com.au/", "country": "au"},
        {"name": "Modern Modular NZ", "url": "https://www.modernmodular.co.nz/", "country": "nz"},
        {"name": "ANZ Modular", "url": "https://www.anzmodular.com/", "country": "nz"},
        {"name": "Steeltec NZ", "url": "https://www.steeltec.co.nz/", "country": "nz"},
        {"name": "Gear Steel Buildings", "url": "https://www.gearsteelbuildings.co.nz/", "country": "nz"},
        {"name": "Flexi House NZ", "url": "https://www.flexihouse.co.nz/", "country": "nz"},
    ]

    if "--enrich" in sys.argv:
        results = extractor.batch_enrich(companies)
        for r in results:
            status = "✅" if r.get("status") == "ok" else "❌"
            print(f"  {status} {r['company']}: {len(r.get('emails',[]))} emails, {len(r.get('phones',[]))} phones, {len(r.get('contacts',[]))} contacts")

    elif "--inject" in sys.argv:
        # 直接从已有缓存注入
        for c in companies:
            cache_key = re.sub(r'https?://', '', c['url']).replace('/', '_').replace('.', '_')[:50]
            cp = CONTACT_CACHE / f"{cache_key}.json"
            if cp.exists():
                data = json.load(open(cp))
                print(f"  📦 {c['name']}: {len(data.get('emails',[]))} emails")
        extractor.inject_into_buyer_db(
            [json.load(open(CONTACT_CACHE / re.sub(r'https?://', '', c['url']).replace('/', '_').replace('.', '_')[:50] + ".json"))
             for c in companies if (CONTACT_CACHE / re.sub(r'https?://', '', c['url']).replace('/', '_').replace('.', '_')[:50] + ".json").exists()]
        )

    elif "--import-known" in sys.argv:
        # 注入已知数据（之前已经人工验证的）
        known = [
            {
                "company": "Kiwi Modular Structures",
                "url": "https://kiwimodularstructures.com/", "country": "nz",
                "status": "ok", "emails": ["gareth@kiwimodularstructures.com", "samantha@kiwimodularstructures.com"],
                "phones": ["027 205 7243", "09 886 7205"],
                "people": [
                    {"name": "Gareth O'Keeffe", "email": "gareth@kiwimodularstructures.com"},
                    {"name": "Samantha Zeta", "email": "samantha@kiwimodularstructures.com"}
                ],
                "contacts": ["Gareth O'Keeffe", "Samantha Zeta"]
            },
            {
                "company": "Expanders NZ",
                "url": "https://www.expanders.co.nz/", "country": "nz",
                "status": "ok", "emails": ["info@expanders.co.nz"],
                "phones": ["027 210 6839"],
                "people": [{"name": "Taylor", "email": "info@expanders.co.nz"}],
                "contacts": ["Taylor"]
            },
            {
                "company": "LGS Solutions",
                "url": "https://www.lgssolutions.com.au/", "country": "au",
                "status": "ok", "emails": ["info@lgssolutions.com.au"],
                "phones": ["1300 941 481"],
                "people": [{"name": "LGS Team", "email": "info@lgssolutions.com.au"}],
                "contacts": []
            },
            {
                "company": "Cargo Connect",
                "url": "https://www.cargoconnect.com.au/", "country": "au",
                "status": "ok",
                "emails": ["bne@cargoconnect.com.au", "syd@cargoconnect.com.au", "mel@cargoconnect.com.au", "per@cargoconnect.com.au"],
                "phones": ["1300 580 838"],
                "people": [
                    {"name": "Brisbane Office", "email": "bne@cargoconnect.com.au"},
                    {"name": "Sydney Office", "email": "syd@cargoconnect.com.au"},
                    {"name": "Melbourne Office", "email": "mel@cargoconnect.com.au"},
                    {"name": "Perth Office", "email": "per@cargoconnect.com.au"}
                ],
                "contacts": []
            }
        ]
        extractor.inject_into_buyer_db(known, product="钢结构折叠集成房屋")

    else:
        print("用法:")
        print("  --enrich        爬取官网提取联系方式")
        print("  --inject        将爬取的数据注入buyer-intel数据库")
        print("  --import-known  导入已知已验证的买家数据（含真实联系方式）")
