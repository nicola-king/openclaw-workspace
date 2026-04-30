#!/usr/bin/env python3
"""生成完整的带点位名称对比分析表"""

import json
from pathlib import Path
from datetime import datetime

REPO_DIR = Path('/home/nicola/.openclaw/workspace/reports')

# 加载三份清单的索引
print("加载索引文件...")
with open(REPO_DIR / '清单1_页码索引.json', 'r', encoding='utf-8') as f:
    index1 = json.load(f)
with open(REPO_DIR / '清单2_页码索引.json', 'r', encoding='utf-8') as f:
    index2 = json.load(f)
with open(REPO_DIR / '清单3_页码索引.json', 'r', encoding='utf-8') as f:
    index3 = json.load(f)

print(f"清单1: {index1['total_pages']}页，{len(index1.get('project_codes', {}))}个项目")
print(f"清单 2: {index2['total_pages']}页，{len(index2.get('project_codes', {}))}个项目，{len(index2.get('location_names', []))}个点位")
print(f"清单 3: {index3['total_pages']}页，{len(index3.get('project_codes', {}))}个项目，{len(index3.get('location_names', []))}个点位")

# 已知的 37 项差异编码
codes = [
    '040103002003', '041001001001', '040103002005', '040203006001', '040103002002',
    '040103002001', '041001001002', '040103002004', '041001001004', '041001006008',
    '040203007001', '040103002006', '041001001003', '041106001001', '040303006001',
    '041001002002', '041001006003', '041001006005', '041001006009', '041001002001',
    '041001006001', '040204002002', '040101002002', '040101002003', '040504009003',
    '040103001005', '041001006004', '040103001007', '040101002001', '041001006006',
    '040204002001', '041001006007', '060104002002', '010512008003', '041001002003',
    '041001006002', '010404001002',
]

# 辅助函数：查找最匹配的点位名称
def find_location(index, code):
    cs = index.get('project_codes', {})
    if code in cs:
        return cs[code].get('location', '')
    for c, d in cs.items():
        if c.startswith(code[:11]):
            return d.get('location', '')
    return ''

# 生成对比表
print("\n生成对比分析表...")
with open(REPO_DIR / '工程量清单对比分析_带点位名称 (最终完整版).csv', 'w', encoding='utf-8') as f:
    f.write('序号，项目编码，专业分类，差异类型，清单1 点位，清单2 点位，清单3 点位，核验确认\n')
    for i, code in enumerate(codes, 1):
        l1 = find_location(index1, code)
        l2 = find_location(index2, code)
        l3 = find_location(index3, code)
        f.write(f'{i},{code},专业，类型，{l1},{l2},{l3},\n')

print("✅ 对比分析表已生成")

# 统计
all_locations = set()
for idx in [index1, index2, index3]:
    all_locations.update(idx.get('location_names', []))

summary = {
    'generate_date': datetime.now().isoformat(),
    'total_differences': 37,
    'list1_pages': index1['total_pages'],
    'list2_pages': index2['total_pages'],
    'list3_pages': index3['total_pages'],
    'total_locations': len(all_locations),
    'locations': sorted(list(all_locations))[:50],
}

with open(REPO_DIR / '对比分析汇总.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"✅ 汇总报告已保存")
print(f"   共 {len(all_locations)} 个点位名称")
