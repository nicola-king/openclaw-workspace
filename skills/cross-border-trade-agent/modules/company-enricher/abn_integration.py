#!/usr/bin/env python3
"""
太一·ABN 自动验证集成 — P2 完善
接入 abr.business.gov.au 公共 API，自动验证澳洲公司

集成位置：company-enricher 模块
用法：
  python3 abn_integration.py --company "Crystalbrook Collection"
  python3 abn_integration.py --verify-batch data/real_companies.md

返回格式：与 company-enricher 的 data_quality 字段兼容
"""

import json
import os
import sys
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# 路径
SKILL_DIR = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = SKILL_DIR / "data/.abn_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ABN Lookup 免费 API
# ABN Lookup Web Search (新URL, JSON API 已弃用)
ABN_SEARCH_URL = "https://abr.business.gov.au/Search/ResultsActive?SearchText="
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TaiyiTradeBot/1.0)"}


def _clean_html_cell(raw: str) -> str:
    """清理 HTML 单元格内容"""
    import html as html_mod
    text = re.sub(r'<[^>]+>', '', raw)
    text = html_mod.unescape(text)
    # 移除 &nbsp; / \xa0 等不可见字符
    text = text.replace(chr(160), '').replace('\xa0', '').replace('\u00a0', '').replace('&nbsp;', '')
    text = ' '.join(text.split())  # 合并多余空白
    return text.strip()


def _extract_table_rows(html: str) -> list:
    """从 HTML 提取 ABN 搜索结果（支持两种格式）
    格式1：搜索页表格（4 列：ABN/Name/Type/Location）
    格式2：详情页标签（th/td 对）
    """
    import html as html_mod
    results = []

    # 格式1：搜索页表格（多个结果）
    tables = re.findall(r'<table[^>]*>([\s\S]*?)</table>', html)
    for table in tables:
        rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', table)
        for row in rows:
            cells = re.findall(r'<t[dh][^>]*>([\s\S]*?)</t[dh]>', row)
            if len(cells) >= 3:
                abn_raw = _clean_html_cell(cells[0])
                name = _clean_html_cell(cells[1])
                entity_type = _clean_html_cell(cells[2])
                if abn_raw.upper() == 'ABN' or not abn_raw:
                    continue
                abn = re.sub(r'\D', '', abn_raw)
                if abn and len(abn) >= 9:
                    results.append({
                        "Abn": abn,
                        "Name": name,
                        "AbnStatus": "Active",
                        "EntityType": entity_type,
                    })

    # 格式2：详情页（单个结果 — th/td 对）
    if not results:
        detail = {}
        rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', html)
        for row in rows:
            th = re.findall(r'<th[^>]*>([\s\S]*?)</th>', row)
            td = re.findall(r'<td[^>]*>([\s\S]*?)</td>', row)
            if th and td:
                key = _clean_html_cell(th[0]).lower()
                val = html_mod.unescape(re.sub(r'<[^>]+>', '', td[0])).strip()
                detail[key] = val

        # 检查是否有 entity name 信息（key 可能有多种格式）
        entity_key = next((k for k in detail if 'entity name' in k.lower()), None)
        if entity_key:
            # 尝试从页面中提取 ABN
            abn_match = re.search(r'(\d{2}[\s]?\d{3}[\s]?\d{3}[\s]?\d{3})', html)
            abn = re.sub(r'\D', '', abn_match.group(1)) if abn_match else ''
            status = detail.get('abn status', 'Active')
            if 'Active' in status:
                results.append({
                    "Abn": abn,
                    "Name": detail.get(entity_key, ''),
                    "AbnStatus": "Active",
                    "EntityType": detail.get(next((k for k in detail if 'entity type' in k.lower()), ''), ''),
                    "GstStatus": detail.get("goods & services tax (gst)", ''),
                    "Location": detail.get(next((k for k in detail if 'main business location' in k.lower() or 'location' in k.lower()), ''), ''), 'GstStatus': detail.get(next((k for k in detail if 'gst' in k.lower()), ''), ''),
                })

    return results


def search_name(name: str) -> list:
    """按公司名搜索（Web 搜索，免费无需注册）"""
    import requests
    cache_file = CACHE_DIR / f"name_{re.sub(r'[^a-zA-Z0-9]', '_', name)[:30]}.json"
    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < 3600:
            return json.loads(cache_file.read_text())

    try:
        url = f"{ABN_SEARCH_URL}{requests.utils.quote(name)}"
        resp = requests.get(url, timeout=10, headers=HEADERS)
        if resp.status_code == 200:
            data = _extract_table_rows(resp.text)
            cache_file.write_text(json.dumps(data, indent=2))
            return data
    except Exception as e:
        print(f"[ABN] 名称搜索失败 {name}: {e}")
    return []


def search_abn(abn: str) -> Optional[dict]:
    """按 ABN 号查询（Web 搜索）— 使用 Scrapling 自适应爬取"""
    from skills.scrapling_adaptor.core import smart_fetch
    cache_file = CACHE_DIR / f"abn_{abn}.json"
    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < 3600:
            return json.loads(cache_file.read_text())

    try:
        url = f"{ABN_SEARCH_URL}{abn}"
        result = smart_fetch(url, timeout=10)
        if result["status"] == 200:
            data = _extract_table_rows(result["body"])
            if data:
                cache_file.write_text(json.dumps(data[0], indent=2))
                return data[0]
    except Exception as e:
        print(f"[ABN] 查询失败 {abn}: {e}")
    return None


def verify_company(name: str, expected_abn: str = "") -> dict:
    """公司验证 → 返回 company-enricher 兼容格式"""
    result = {
        "name": name,
        "verified": False,
        "abn": "",
        "acn": "",
        "status": "",
        "gst_status": "",
        "entity_type": "",
        "entity_name": "",
        "address": "",
        "data_quality": "D",
        "source": "abr.business.gov.au",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "all_matches": [],
    }

    if expected_abn:
        data = search_abn(expected_abn)
        if data:
            result.update({
                "abn": data.get("Abn", ""),
                "status": data.get("AbnStatus", ""),
                "entity_name": data.get("Name", ""),
                "entity_type": data.get("EntityType", ""),
            })
            result["verified"] = data.get("AbnStatus") == "Active"
            result["data_quality"] = "A" if result["verified"] else "C"
            return result

    # 如果是纯数字，当作 ABN 搜索
    if name.isdigit() and len(name) >= 9:
        result["abn"] = name
        data = search_abn(name)
        if data:
            result["abn"] = data.get("Abn", name)
            result["status"] = data.get("AbnStatus", "")
            result["entity_name"] = data.get("Name", "")
            result["entity_type"] = data.get("EntityType", "")
            result["verified"] = data.get("AbnStatus") == "Active"
            result["data_quality"] = "A" if result["verified"] else "C"
        return result

    # 按名称搜索 — 尝试多个搜索变体
    search_terms = [name]
    # 如果名字包含空格，只搜第一部分
    parts = name.split()
    if len(parts) >= 2:
        search_terms.append(parts[0])  # 搜第一个词
        # 搜前两个词
        if len(parts) >= 3:
            search_terms.append(' '.join(parts[:2]))

    all_matches = []
    seen_abns = set()
    for term in search_terms:
        matches = search_name(term)
        for m in matches:
            abn = m.get("Abn", "")
            if abn and abn not in seen_abns:
                seen_abns.add(abn)
                all_matches.append(m)
        if len(all_matches) >= 10:
            break

    if all_matches:
        result["all_matches"] = all_matches
        # 最佳匹配：优先精确名称匹配
        exact = [m for m in all_matches if name.lower() in m.get("Name", "").lower()]
        if exact:
            best = exact[0]
        else:
            best = all_matches[0]

        result["abn"] = best.get("Abn", "")
        result["status"] = best.get("AbnStatus", "")
        result["entity_name"] = best.get("Name", "")
        result["verified"] = best.get("AbnStatus") == "Active"
        result["data_quality"] = "A" if result["verified"] else "B"

    return result


def _find_json_boundary(text: str) -> int:
    """找到 JSON 主体的闭合位置（跳过尾部附加内容）"""
    depth = 0
    for i, c in enumerate(text):
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i
    return -1


def _classify(item: dict) -> str:
    """判断公司类别：'cn' / 'au' / 'other'（基于 website/phone/name）"""
    website = item.get('website', '').lower()
    phone = item.get('phone', '')
    name = item.get('name', '')

    # 优先检查 website 后缀（最可靠的特征）
    if website.endswith('.cn'):
        return 'cn'
    if website.endswith('.com.au') or website.endswith('.net.au'):
        return 'au'

    # 其次检查 phone
    if '+86-' in phone:
        return 'cn'
    if '61-' in phone:
        return 'au'

    # 最后检查名称中的特征词
    text_au = f"{name} {website}"
    if re.search(r'pty\s*ltd|NSW|VIC|QLD|WA|SA|TAS|sydney|melbourne|brisbane', text_au, re.I):
        return 'au'

    text_cn = f"{name}"
    if re.search(r'有限公司|浙江|广东|上海|北京|深圳|广州', text_cn):
        return 'cn'

    return 'other'


def extract_australian_companies(md_file: Path) -> list:
    """从 real_companies.md 提取澳洲公司（JSON 解析 + 特征分类）"""
    if not md_file.exists():
        return []
    import json
    text = md_file.read_text()
    
    json_end = _find_json_boundary(text)
    if json_end < 0:
        return []
    
    try:
        data = json.loads(text[:json_end+1])
    except json.JSONDecodeError:
        return []

    result = []
    # 从 prospects 提取，但加上分类验证作为保险
    for item in data.get('prospects', []):
        if _classify(item) == 'au':
            result.append({
                'name': item.get('name', ''),
                'website': item.get('website', ''),
            })
    return result


def batch_verify(md_file: Path) -> list:
    """批量验证 real_companies.md 中的澳洲公司"""
    companies = extract_australian_companies(md_file)
    print(f"[ABN] 找到 {len(companies)} 个澳洲公司，开始批量验证...\n")
    results = []
    for idx, c in enumerate(companies, 1):
        print(f"  [{idx}/{len(companies)}] {c['name']}...", end=" ", flush=True)
        res = verify_company(c["name"])
        status = "✅" if res["verified"] else "❌"
        print(f"{status} (ABN: {res['abn'] or 'N/A'}, {res['status'] or '未查询到'})")
        results.append(res)
        time.sleep(0.5)  # 礼貌间隔
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="太一·ABN 自动验证集成")
    parser.add_argument("--company", type=str, help="验证单个公司")
    parser.add_argument("--verify-batch", type=str, help="批量验证 real_companies.md")
    parser.add_argument("--cache-clear", action="store_true", help="清除缓存")
    args = parser.parse_args()

    if args.cache_clear:
        for f in CACHE_DIR.iterdir():
            f.unlink()
        print("✅ 缓存已清除")
        sys.exit(0)

    if args.company:
        result = verify_company(args.company)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.verify_batch:
        md_path = Path(args.verify_batch)
        if not md_path.exists():
            print(f"文件不存在: {md_path}")
            sys.exit(1)
        results = batch_verify(md_path)
        output_path = md_path.parent / ".abn_verify_results.json"
        output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        verified = sum(1 for r in results if r["verified"])
        print(f"\n📊 验证完成: {verified}/{len(results)} 家公司验证通过")
        print(f"   结果已保存: {output_path}")
