#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工程量清单对比分析工具
对比三个工程量清单文件的差异：
1. 项目编码相同，项目名称不同
2. 项目名称相同，项目特征不同
3. 项目名称相同，综合单价不同
"""

import fitz
import json
import re
from collections import defaultdict
from pathlib import Path

def extract_text_from_pdf(pdf_path, max_pages=100):
    """从 PDF 提取文本内容"""
    doc = fitz.open(pdf_path)
    texts = []
    
    for i in range(min(max_pages, len(doc))):
        page = doc[i]
        text = page.get_text()
        if text.strip():
            texts.append({
                'page': i + 1,
                'text': text
            })
    
    return texts

def parse_item_table(text):
    """解析分部分项工程项目清单计价表"""
    items = []
    lines = text.split('\n')
    
    current_item = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 匹配项目编码 (如 041001006001)
        code_match = re.match(r'^(\d{12})$', line)
        if code_match:
            if current_item:
                items.append(current_item)
            current_item = {
                '项目编码': code_match.group(1),
                '项目名称': '',
                '项目特征': '',
                '计量单位': '',
                '工程量': '',
                '综合单价': '',
                '合价': ''
            }
            continue
        
        if current_item:
            # 收集项目名称、特征等信息
            if '项目特征' in line or '[项目特征]' in line:
                current_item['项目名称'] = current_item.get('项目名称', '').strip()
                current_item['项目特征开始'] = True
            elif '工程内容' in line or '[工程内容]' in line:
                current_item['项目特征'] = current_item.get('项目特征', '').strip()
                current_item['项目特征开始'] = False
            elif current_item.get('项目特征开始'):
                current_item['项目特征'] = current_item.get('项目特征', '') + line + ' '
            elif not current_item['项目名称']:
                current_item['项目名称'] = line
            elif 'm3' in line or 'm2' in line or 'm' in line or '个' in line or '套' in line:
                # 匹配单位和工程量
                unit_qty_match = re.search(r'(\d+\.?\d*)\s*(m3|m2|m|个|套|km|项)', line)
                if unit_qty_match:
                    current_item['工程量'] = unit_qty_match.group(1)
                    current_item['计量单位'] = unit_qty_match.group(2)
    
    if current_item:
        items.append(current_item)
    
    return items

def compare_items(items1, items2, items3, name1="清单 1", name2="清单 2", name3="清单 3"):
    """对比三个清单的项目差异"""
    
    # 按项目编码索引
    def index_by_code(items):
        indexed = {}
        for item in items:
            code = item.get('项目编码', '')
            if code:
                indexed[code] = item
        return indexed
    
    idx1 = index_by_code(items1)
    idx2 = index_by_code(items2)
    idx3 = index_by_code(items3)
    
    all_codes = set(idx1.keys()) | set(idx2.keys()) | set(idx3.keys())
    
    # 差异分类
    diff_same_code_diff_name = []  # 项目编码相同，项目名称不同
    diff_same_name_diff_feature = []  # 项目名称相同，项目特征不同
    diff_same_name_diff_price = []  # 项目名称相同，综合单价不同
    
    for code in all_codes:
        item1 = idx1.get(code, {})
        item2 = idx2.get(code, {})
        item3 = idx3.get(code, {})
        
        names = [
            item1.get('项目名称', ''),
            item2.get('项目名称', ''),
            item3.get('项目名称', '')
        ]
        names = [n for n in names if n]
        
        features = [
            item1.get('项目特征', ''),
            item2.get('项目特征', ''),
            item3.get('项目特征', '')
        ]
        features = [f for f in features if f]
        
        prices = [
            item1.get('综合单价', ''),
            item2.get('综合单价', ''),
            item3.get('综合单价', '')
        ]
        prices = [p for p in prices if p]
        
        # 检查：项目编码相同，项目名称不同
        if len(set(names)) > 1 and len(names) > 1:
            diff_same_code_diff_name.append({
                '项目编码': code,
                '清单 1': item1.get('项目名称', ''),
                '清单 2': item2.get('项目名称', ''),
                '清单 3': item3.get('项目名称', '')
            })
        
        # 检查：项目名称相同，项目特征不同
        if len(set(names)) == 1 and len(names) > 1:
            if len(set(features)) > 1:
                diff_same_name_diff_feature.append({
                    '项目编码': code,
                    '项目名称': names[0],
                    '清单 1 特征': item1.get('项目特征', '')[:100],
                    '清单 2 特征': item2.get('项目特征', '')[:100],
                    '清单 3 特征': item3.get('项目特征', '')[:100]
                })
        
        # 检查：项目名称相同，综合单价不同
        if len(set(names)) == 1 and len(names) > 1:
            if len(set(prices)) > 1:
                diff_same_name_diff_price.append({
                    '项目编码': code,
                    '项目名称': names[0],
                    '清单 1 单价': item1.get('综合单价', ''),
                    '清单 2 单价': item2.get('综合单价', ''),
                    '清单 3 单价': item3.get('综合单价', '')
                })
    
    return {
        '编码相同名称不同': diff_same_code_diff_name,
        '名称相同特征不同': diff_same_name_diff_feature,
        '名称相同单价不同': diff_same_name_diff_price
    }

def main():
    print("=" * 80)
    print("工程量清单对比分析工具")
    print("=" * 80)
    
    # 提取三个清单的内容
    print("\n正在提取清单内容...")
    
    texts1 = extract_text_from_pdf('/tmp/bill.pdf', max_pages=50)
    texts2 = extract_text_from_pdf('/tmp/bill2.pdf', max_pages=50)
    texts3 = extract_text_from_pdf('/tmp/bill3.pdf', max_pages=50)
    
    print(f"清单 1 提取：{len(texts1)} 页")
    print(f"清单 2 提取：{len(texts2)} 页")
    print(f"清单 3 提取：{len(texts3)} 页")
    
    # 解析项目
    print("\n正在解析项目数据...")
    items1 = []
    items2 = []
    items3 = []
    
    for t in texts1:
        items = parse_item_table(t['text'])
        items1.extend(items)
    
    for t in texts2:
        items = parse_item_table(t['text'])
        items2.extend(items)
    
    for t in texts3:
        items = parse_item_table(t['text'])
        items3.extend(items)
    
    print(f"清单 1 解析：{len(items1)} 个项目")
    print(f"清单 2 解析：{len(items2)} 个项目")
    print(f"清单 3 解析：{len(items3)} 个项目")
    
    # 对比分析
    print("\n正在对比分析...")
    diffs = compare_items(items1, items2, items3)
    
    print("\n" + "=" * 80)
    print("对比分析结果")
    print("=" * 80)
    
    print(f"\n1. 项目编码相同，项目名称不同：{len(diffs['编码相同名称不同'])} 项")
    for item in diffs['编码相同名称不同'][:10]:  # 显示前 10 项
        print(f"   编码：{item['项目编码']}")
        print(f"     清单 1: {item['清单 1']}")
        print(f"     清单 2: {item['清单 2']}")
        print(f"     清单 3: {item['清单 3']}")
        print()
    
    print(f"\n2. 项目名称相同，项目特征不同：{len(diffs['名称相同特征不同'])} 项")
    for item in diffs['名称相同特征不同'][:10]:
        print(f"   编码：{item['项目编码']}")
        print(f"     名称：{item['项目名称']}")
        print(f"     清单 1 特征：{item['清单 1 特征']}...")
        print(f"     清单 2 特征：{item['清单 2 特征']}...")
        print(f"     清单 3 特征：{item['清单 3 特征']}...")
        print()
    
    print(f"\n3. 项目名称相同，综合单价不同：{len(diffs['名称相同单价不同'])} 项")
    for item in diffs['名称相同单价不同'][:10]:
        print(f"   编码：{item['项目编码']}")
        print(f"     名称：{item['项目名称']}")
        print(f"     清单 1 单价：{item['清单 1 单价']}")
        print(f"     清单 2 单价：{item['清单 2 单价']}")
        print(f"     清单 3 单价：{item['清单 3 单价']}")
        print()
    
    print("\n" + "=" * 80)
    print("分析完成")
    print("=" * 80)

if __name__ == "__main__":
    main()
