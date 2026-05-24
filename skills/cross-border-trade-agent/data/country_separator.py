#!/usr/bin/env python3
"""
太一·国内外公司分离验证层 v1.0
确保 manufacturers/prospects/competitors 数据不混入错误类别

规则：
  国内公司（.cn / 中国手机 / 中文名）→ 只出现在 manufacturers
  国外公司（.com.au / .au / 英文名）→ 只出现在 prospects
  竞品（competitors）— 通过 country 字段区分
"""

import json, re
from pathlib import Path

CN_INDICATORS = [
    r'\.cn$',                    # .cn 域名
    r'\+86-',                     # 中国电话区号
    r'中国',                       # 名称含"中国"
    r'有限公司?$',                  # 有限公司/有限责任公司
    r'浙江|广东|上海|北京|深圳|广州',  # 中国城市
]

AU_INDICATORS = [
    r'\.com\.au$',               # .com.au 域名
    r'\.net\.au$',               # .net.au 域名
    r'\.au/',                     # .au 路径
    r'pty\s*ltd',                 # Pty Ltd (澳洲特有)
    r'Pty\s*Ltd',
    r'NSW|VIC|QLD|WA|SA|TAS',    # 澳洲州名
    r'Sydney|Melbourne|Brisbane|Perth|Adelaide',
]


def classify_company(item: dict) -> str:
    """判断公司类别：'cn' / 'au' / 'other'"""
    website = item.get('website', '')
    phone = item.get('phone', '')
    name = item.get('name', '')
    address = item.get('address', '')

    text = f"{website} {phone} {name} {address}"

    # 中国特征优先匹配
    for p in CN_INDICATORS:
        if re.search(p, text, re.I):
            return 'cn'

    # 澳洲特征
    for p in AU_INDICATORS:
        if re.search(p, text, re.I):
            return 'au'

    # 后缀判断
    if website.endswith('.cn'):
        return 'cn'
    if website.endswith('.com.au') or website.endswith('.au'):
        return 'au'

    return 'other'


def check_integrity(filepath: str) -> dict:
    """验证数据隔离完整性"""
    text = open(filepath).read()
    depth, end = 0, -1
    for i, c in enumerate(text):
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = i
                break
    data = json.loads(text[:end+1]) if end > 0 else {}

    errors = []

    for m in data.get('manufacturers', []):
        cls = classify_company(m)
        if cls == 'au':
            errors.append(f"manufacturers 混入澳洲公司: {m['name']}")
        elif cls == 'other':
            errors.append(f"manufacturers 无法分类: {m['name']}")

    for p in data.get('prospects', []):
        cls = classify_company(p)
        if cls == 'cn':
            errors.append(f"prospects 混入中国公司: {p['name']}")
        elif cls == 'other':
            errors.append(f"prospects 无法分类: {p['name']}")

    for c in data.get('competitors', []):
        cls = classify_company(c)
        country = c.get('country', '')
        if cls == 'cn' and country != 'China':
            errors.append(f"competitors 标记为 {country} 但特征是中国: {c['name']}")
        elif cls == 'au' and country != 'Australia':
            errors.append(f"competitors 标记为 {country} 但特征是澳洲: {c['name']}")

    return {
        "integrity": len(errors) == 0,
        "total_companies": len(data.get('manufacturers',[])) + len(data.get('prospects',[])) + len(data.get('competitors',[])),
        "manufacturers": len(data.get('manufacturers',[])),
        "prospects": len(data.get('prospects',[])),
        "competitors": len(data.get('competitors',[])),
        "errors": errors,
    }


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    # real_companies.md 在 data/ 下
    result = check_integrity(str(script_dir / "real_companies.md"))
    status = "✅ 数据隔离完好" if result["integrity"] else "❌ 发现问题"
    print(f"{'='*50}")
    print(f"  数据完整性验证")
    print(f"{'='*50}")
    print(f"  状态: {status}")
    print(f"  总计: {result['total_companies']} 家公司")
    print(f"    manufacturers: {result['manufacturers']} (应全为中国)")
    print(f"    prospects:     {result['prospects']} (应为澳洲)")
    print(f"    competitors:   {result['competitors']} (通过 country 区分)")
    if result['errors']:
        print(f"\n  ❌ 错误 ({len(result['errors'])} 条):")
        for e in result['errors']:
            print(f"    - {e}")
    else:
        print(f"\n  ✅ 无分类错误")
