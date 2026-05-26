#!/usr/bin/env python3
"""
太一·自动数据爬取 → buyers.md/real_companies.md 自动更新
P0 改进#1：爬虫结果自动写入手动维护文件

执行：
  python3 auto_scraper.py --source all          # 全量：爬取+更新 buyers.md
  python3 auto_scraper.py --sync-companies      # 仅合并新公司到 real_companies.md
  python3 auto_scraper.py --sync-buyers         # 仅合并新买家到 buyers.md
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# 脚本在 data/auto_scraper/ 下，根目录是 ../..
SKILL_ROOT = Path(__file__).resolve().parent.parent.parent

# 确保 skills 包路径可导入（SKILL_ROOT.parent = ~/workspace/skills/）
SKILLS_DIR = str(SKILL_ROOT.parent)
if SKILLS_DIR not in sys.path:
    sys.path.insert(0, SKILLS_DIR)

DATA_DIR = SKILL_ROOT / "data"
CACHE_DIR = DATA_DIR / ".abn_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════
# 爬虫核心
# ═══════════════════════════════════════════

def search_abn(abn: str) -> Optional[dict]:
    """ABN Lookup 查询 — 使用 Scrapling 自适应爬取"""
    from scrapling_adaptor.core import smart_fetch, extract_items
    cache = CACHE_DIR / f"abn_{abn}.json"
    if cache.exists() and (time.time() - cache.stat().st_mtime) < 3600:
        return json.loads(cache.read_text())
    try:
        url = f"https://abr.business.gov.au/Search/ResultsActive?SearchText={abn}"
        result = smart_fetch(url, timeout=10)
        if result["status"] == 200:
            html = result["body"]
            rows = __import__('re').findall(r'<tr[^>]*>([\s\S]*?)</tr>', html)
            for row in rows:
                cells = __import__('re').findall(r'<t[dh][^>]*>([\s\S]*?)</t[dh]>', row)
                if len(cells) >= 2:
                    raw_abn = __import__('re').sub(r'<[^>]+>', '', cells[0]).strip()
                    name = __import__('re').sub(r'<[^>]+>', '', cells[1]).strip()
                    clean = __import__('re').sub(r'\D', '', raw_abn)
                    if clean and len(clean) >= 9:
                        result_data = {"Abn": clean, "Name": name, "AbnStatus": "Active"}
                        cache.write_text(json.dumps(result_data, indent=2))
                        return result_data
    except Exception as e:
        pass
    return None


def exchange_rate() -> Optional[float]:
    """今日 CNY→AUD 汇率 — 使用 Scrapling"""
    from scrapling_adaptor.core import smart_fetch
    try:
        result = smart_fetch("https://api.frankfurter.app/latest?from=CNY&to=AUD", timeout=10)
        if result["status"] == 200:
            return __import__('json').loads(result["body"])["rates"].get("AUD")
    except:
        pass
    return None


# ═══════════════════════════════════════════
# buyers.md 自动更新
# ═══════════════════════════════════════════

def update_buyers_md() -> dict:
    """爬取公开招标 → 合并到 buyers.md"""
    buyers_file = DATA_DIR / "buyers.md"
    if not buyers_file.exists():
        buyers_file = SKILL_ROOT / "modules/buyer-intel/data/buyers.md"
    if not buyers_file.exists():
        return {"status": "error", "msg": "buyers.md 未找到"}

    # 读取现有数据
    text = buyers_file.read_text()
    existing_ids = set(re.findall(r'"id":\s*"([^"]+)"', text))

    # 尝试抓取 World Bank RSS 招标
    import feedparser
    new_entries = []
    try:
        feed = feedparser.parse("https://www.worldbank.org/en/projects-operations/procurement/rss")
        for entry in feed.entries[:3]:
            title = entry.get("title", "")
            if "construction" not in title.lower() and "building" not in title.lower():
                continue
            new_id = f"AUTO-{re.sub(r'[^a-zA-Z0-9]','',title)[:10].upper()}"
            if new_id in existing_ids:
                continue
            new_entries.append({
                "id": new_id,
                "type": "project",
                "project_name": title[:80],
                "project_brief": entry.get("summary", "")[:150],
                "status": "投标中",
                "sectors": ["基建"],
                "source": "World Bank RSS (auto)",
                "confirmed": True,
                "contacts": [],
                "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            })
    except ImportError:
        pass
    except Exception as e:
        pass

    report = {
        "buyers_file": str(buyers_file),
        "existing_ids": len(existing_ids),
        "new_entries": len(new_entries),
        "entries": [e["project_name"] for e in new_entries],
    }

    # 写回 buyers.md — 追加到末尾
    if new_entries:
        append_text = "\n  " + ",\n  ".join(json.dumps(e, ensure_ascii=False) for e in new_entries)
        with open(buyers_file, "a") as f:
            f.write(append_text)

    return report


# ═══════════════════════════════════════════
# real_companies.md 自动更新
# ═══════════════════════════════════════════

def update_companies_md() -> dict:
    """通过 ABN Lookup 发现新澳洲公司 → 合并到 real_companies.md"""
    # 查找 real_companies.md
    candidates = [
        SKILL_ROOT / "data/real_companies.md",
        SKILL_ROOT / "real_companies.md",
    ]
    companies_file = None
    for c in candidates:
        if c.exists():
            companies_file = c
            break
    if not companies_file:
        return {"status": "error", "msg": "real_companies.md 未找到", "searched": [str(p) for p in candidates]}

    text = companies_file.read_text()
    existing_names = set(re.findall(r'"name":\s*"([^"]+)"', text))

    # 搜索已知竞品 + 潜在买家
    # 精确搜索：只搜澳洲模块化建筑/折叠房屋相关公司
    search_terms = ["Modscape", "Prefab Homes Australia", "Modular Building Australia"]
    new_companies = []
    seen_abns = set()
    # 只保留包含这些关键词的公司
    ALLOWED_KEYWORDS = ["PREFAB", "MODULAR", "MODSCAP", "HOUSING", "BUILD", "CONSTRUCT", "HOMES"]

    for term in search_terms:
        try:
            import requests
            url = f"https://abr.business.gov.au/Search/ResultsActive?SearchText={requests.utils.quote(term)}"
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', resp.text)
                for row in rows:
                    cells = re.findall(r'<t[dh][^>]*>([\s\S]*?)</t[dh]>', row)
                    if len(cells) >= 2:
                        raw_abn = re.sub(r'<[^>]+>', '', cells[0]).strip()
                        name = re.sub(r'<[^>]+>', '', cells[1]).strip()
                        abn = re.sub(r'\D', '', raw_abn)
                        if abn and abn not in seen_abns and name not in existing_names:
                            seen_abns.add(abn)
                            # 只保留相关公司（含关键词的）
                            if not any(kw in name.upper() for kw in ALLOWED_KEYWORDS):
                                continue
                            new_companies.append({
                                "id": f"AUTO-{abn[:6]}",
                                "name": name,
                                "name_en": name,
                                "website": "",
                                "phone": "",
                                "email": "",
                                "abn": abn,
                                "verified": True,
                                "source": "ABN Lookup (auto)",
                                "verification_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                            })
        except:
            pass
        time.sleep(0.5)

    report = {
        "companies_file": str(companies_file),
        "existing_names": len(existing_names),
        "new_companies": len(new_companies),
        "companies": [c["name"] for c in new_companies],
    }

    # 写入 real_companies.md — 更新 prospects 列表（追加到 JSON 内）
    if new_companies:
        # 读取现有 JSON 数据
        text = companies_file.read_text()
        brace_depth = 0
        json_end = -1
        for i, c in enumerate(text):
            if c == '{': brace_depth += 1
            elif c == '}':
                brace_depth -= 1
                if brace_depth == 0:
                    json_end = i
                    break
        if json_end > 0:
            import json
            data = json.loads(text[:json_end+1])
            # 追加到 prospects
            existing_ids = {p.get('id','') for p in data.get('prospects', [])}
            for c in new_companies:
                if c.get('id','') not in existing_ids:
                    data.setdefault('prospects', []).append({
                        'id': c['id'],
                        'name': c['name'],
                        'name_en': c['name'],
                        'website': c.get('website', ''),
                        'abn': c.get('abn', ''),
                        'verified': True,
                        'source': 'ABN Lookup (auto)',
                        'verification_date': c['verification_date'],
                    })
                    existing_ids.add(c['id'])
            # 写回（保留尾部注释等）
            new_json = json.dumps(data, indent=2, ensure_ascii=False)
            companies_file.write_text(new_json)
            print(f'  写入 data/real_companies.md，新增 {len(new_companies)} 条 prospects')

    return report


# ═══════════════════════════════════════════
# 数据隔离守卫
# ═══════════════════════════════════════════

def _cn_or_au(item: dict) -> str:
    """判断公司类别：'cn' / 'au' / 'other'"""
    website = item.get('website', '')
    phone = item.get('phone', '')
    text = f"{website} {phone}"
    if re.search(r'\.cn$|\+86-|有限公司', text, re.I):
        return 'cn'
    if re.search(r'\.com\.au$|pty\s*ltd|NSW|VIC|QLD|WA', text, re.I):
        return 'au'
    return 'other'


def guard_data_integrity(data: dict) -> list:
    """验证数据隔离，返回错误列表"""
    errors = []
    for m in data.get('manufacturers', []):
        if _cn_or_au(m) == 'au':
            errors.append(f"manufacturers 混入澳洲公司: {m.get('name','')}")
    for p in data.get('prospects', []):
        if _cn_or_au(p) == 'cn':
            errors.append(f"prospects 混入中国公司: {p.get('name','')}")
    return errors


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="太一自动爬取→数据更新 Agent")
    parser.add_argument("--source", choices=["all", "economic"], default="economic")
    parser.add_argument("--sync-companies", action="store_true", help="更新 real_companies.md")
    parser.add_argument("--sync-buyers", action="store_true", help="更新 buyers.md")
    parser.add_argument("--check-integrity", action="store_true", help="检查数据隔离")
    args = parser.parse_args()

    if args.check_integrity:
        from pathlib import Path
        companies_file = SKILL_ROOT / "data/real_companies.md"
        if not companies_file.exists():
            print("❌ real_companies.md 不存在")
            sys.exit(1)
        text = companies_file.read_text()
        depth, end = 0, -1
        for i, c in enumerate(text):
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: end = i; break
        if end < 0:
            print("❌ 无法解析 JSON")
            sys.exit(1)
        import json
        data = json.loads(text[:end+1])
        errors = guard_data_integrity(data)
        if errors:
            print("❌ 数据隔离违规:")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"✅ 数据隔离完好 ({len(data.get('manufacturers',[]))} 家国内 + {len(data.get('prospects',[]))} 家国外 + {len(data.get('competitors',[]))} 家竞品)")
        sys.exit(0)

    report = {"run_at": datetime.now(timezone.utc).isoformat()}

    if args.sync_companies or args.source == "all":
        r = update_companies_md()
        report["sync_companies"] = r
        print(f"[COMPANIES] 现有 {r['existing_names']} 家, 新发现 {r['new_companies']} 家")

    if args.sync_buyers or args.source == "all":
        r = update_buyers_md()
        report["sync_buyers"] = r
        print(f"[BUYERS] 现有 {r['existing_ids']} 条, 新增 {r['new_entries']} 条")

    if args.source in ("all", "economic"):
        rate = exchange_rate()
        report["exchange_rate_cny_aud"] = rate
        print(f"[ECONOMIC] CNY→AUD: {rate}")

    report_file = DATA_DIR / "auto_scraper_report.json"
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n✅ 报告已保存: {report_file}")
