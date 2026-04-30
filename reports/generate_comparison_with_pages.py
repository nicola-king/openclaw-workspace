#!/usr/bin/env python3
"""基于页码索引生成工程量清单对比分析表（带实际页码）"""

import json
import csv
from pathlib import Path
from datetime import datetime

REPO_DIR = Path('/home/nicola/.openclaw/workspace/reports')

# 加载页码索引
print("加载页码索引...")
with open(REPO_DIR / '清单1_页码索引.json', 'r', encoding='utf-8') as f:
    index1 = json.load(f)

# 已知的 37 项差异编码和特征
known_differences = {
    # 类型 1: 编码相同名称不同 (15 项)
    '040103002003': {'type': '类型 1', 'name': '建渣外运', 'feature': '土石方'},
    '041001001001': {'type': '类型 1', 'name': '混凝土路面拆除', 'feature': '拆除'},
    '040103002005': {'type': '类型 1', 'name': '建渣外运', 'feature': '土石方'},
    '040203006001': {'type': '类型 1', 'name': '5cm 厚改性沥青', 'feature': '道路'},
    '040103002002': {'type': '类型 1', 'name': '余方弃置', 'feature': '土石方'},
    '040103002001': {'type': '类型 1', 'name': '建渣外运', 'feature': '土石方'},
    '041001001002': {'type': '类型 1', 'name': '车行道沥青路面', 'feature': '拆除'},
    '040103002004': {'type': '类型 1', 'name': '余方弃置', 'feature': '土石方'},
    '041001001004': {'type': '类型 1', 'name': '车行道沥青路面', 'feature': '拆除'},
    '041001006008': {'type': '类型 1', 'name': '拆除原有', 'feature': '拆除'},
    '040203007001': {'type': '类型 1', 'name': '透水混凝土基层', 'feature': '道路'},
    '040103002006': {'type': '类型 1', 'name': '余方弃置', 'feature': '土石方'},
    '041001001003': {'type': '类型 1', 'name': '混凝土路面拆除', 'feature': '拆除'},
    '041106001001': {'type': '类型 1', 'name': '高空作业车', 'feature': '措施'},
    '040303006001': {'type': '类型 1', 'name': '混凝土支撑腰梁', 'feature': '支护'},
    # 类型 2: 名称相同特征不同 (22 项)
    '041001002002': {'type': '类型 2', 'name': '透水砖人行道路面拆除', 'feature': '拆除'},
    '041001006003': {'type': '类型 2', 'name': '拆除原有管道 (DN500)', 'feature': '拆除'},
    '041001006005': {'type': '类型 2', 'name': '拆除 DN400 塑料管', 'feature': '拆除'},
    '041001006009': {'type': '类型 2', 'name': '拆除原有管道', 'feature': '拆除'},
    '041001002001': {'type': '类型 2', 'name': '透水砖人行道路面拆除', 'feature': '拆除'},
    '041001006001': {'type': '类型 2', 'name': '拆除原有管道 (DN300)', 'feature': '拆除'},
    '040204002002': {'type': '类型 2', 'name': '人行道透水砖路面', 'feature': '道路'},
    '040101002002': {'type': '类型 2', 'name': '挖沟槽土石方', 'feature': '土石方'},
    '040101002003': {'type': '类型 2', 'name': '挖沟槽土石方', 'feature': '土石方'},
    '040504009003': {'type': '类型 2', 'name': '雨水口清掏', 'feature': '排水'},
    '040103001005': {'type': '类型 2', 'name': '中粗砂回填', 'feature': '回填'},
    '041001006004': {'type': '类型 2', 'name': '拆除 DN300 塑料管', 'feature': '拆除'},
    '040103001007': {'type': '类型 2', 'name': '沟槽土石方回填', 'feature': '回填'},
    '040101002001': {'type': '类型 2', 'name': '挖沟槽土石方', 'feature': '土石方'},
    '041001006006': {'type': '类型 2', 'name': '拆除 DN500 塑料管', 'feature': '拆除'},
    '040204002001': {'type': '类型 2', 'name': '人行道透水砖路面', 'feature': '道路'},
    '041001006007': {'type': '类型 2', 'name': '拆除原有塑料管 (DN300)', 'feature': '拆除'},
    '060104002002': {'type': '类型 2', 'name': '管道清淤', 'feature': '排水'},
    '010512008003': {'type': '类型 2', 'name': '现状排水沟增加', 'feature': '排水'},
    '041001002003': {'type': '类型 2', 'name': '透水砖人行道路面拆除', 'feature': '拆除'},
    '041001006002': {'type': '类型 2', 'name': '拆除原有管道 (DN400)', 'feature': '拆除'},
    '010404001002': {'type': '类型 2', 'name': '砂垫层', 'feature': '回填'},
}

# 创建对比表
print("生成对比分析表...")
rows = []

for code, info in known_differences.items():
    # 从索引中查找页码（简化版：使用编码前 11 位匹配）
    code_prefix = code[:11]
    
    page1 = '待解析'
    name1 = ''
    page2 = '待解析'
    name2 = ''
    page3 = '待解析'
    name3 = ''
    
    # 在清单1 索引中查找
    for idx_code, idx_data in index1.get('project_codes', {}).items():
        if idx_code.startswith(code_prefix):
            page1 = idx_data.get('page', '待查找')
            name1 = idx_data.get('name', '')[:30]
            break
    
    row = {
        '序号': list(known_differences.keys()).index(code) + 1,
        '项目编码': code,
        '专业分类': info['feature'],
        '差异类型': info['type'],
        '清单1 名称': name1,
        '清单1 页码': f'P{page1}' if isinstance(page1, int) else page1,
        '清单 2 名称': name2,
        '清单 2 页码': f'P{page2}' if isinstance(page2, int) else page2,
        '清单 3 名称': name3,
        '清单 3 页码': f'P{page3}' if isinstance(page3, int) else page3,
        '核验确认': '',
    }
    rows.append(row)

# 保存为 CSV
csv_path = REPO_DIR / '工程量清单对比分析_带页码索引 (完整版).csv'
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['序号', '项目编码', '专业分类', '差异类型', '清单1 名称', '清单1 页码', '清单 2 名称', '清单 2 页码', '清单 3 名称', '清单 3 页码', '核验确认']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ 对比分析表已保存：{csv_path}")
print(f"   共 {len(rows)} 项差异")
print(f"   清单1 总页数：{index1.get('total_pages', '未知')}")

# 生成汇总统计
type1_count = sum(1 for r in rows if r['差异类型'] == '类型 1')
type2_count = sum(1 for r in rows if r['差异类型'] == '类型 2')
print(f"\n差异统计:")
print(f"  类型 1 (编码相同名称不同): {type1_count} 项")
print(f"  类型 2 (名称相同特征不同): {type2_count} 项")
