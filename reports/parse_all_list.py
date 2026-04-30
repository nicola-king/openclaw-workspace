#!/usr/bin/env python3
"""解析三份工程量清单 PDF 并生成页码索引"""

import pdfplumber
import json
import re
from pathlib import Path
from datetime import datetime

# PDF 文件路径
PDF_DIR = Path('/home/nicola/.openclaw/media/inbound')
OUTPUT_DIR = Path('/home/nicola/.openclaw/workspace/reports')

# 查找工程量清单 PDF 文件
pdf_files = []
for f in PDF_DIR.glob('*.pdf'):
    if '工程量清单' in f.name or 'å_ç_é_æ_å' in f.name:
        pdf_files.append(f)

print(f"找到 {len(pdf_files)} 个 PDF 文件:")
for f in pdf_files:
    print(f"  - {f.name}")

# 解析每个 PDF
all_indices = {}

for pdf_path in pdf_files:
    print(f"\n{'='*60}")
    print(f"解析：{pdf_path.name}")
    print('='*60)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page_count = len(pdf.pages)
            print(f"总页数：{page_count}")
            
            # 提取每页的项目编码和名称
            project_codes = {}
            
            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                text = page.extract_text()
                
                if not text:
                    continue
                
                # 查找项目编码（12 位数字格式：04XXXXXXXX 或 01XXXXXXXX）
                lines = text.split('\n')
                for line_idx, line in enumerate(lines):
                    # 匹配项目编码
                    code_match = re.search(r'(0[146]\d{9})', line)
                    if code_match:
                        code = code_match.group(1)
                        # 获取项目名称（通常在编码同一行或下一行）
                        name_start = line.find(code) + len(code)
                        name_line = line[name_start:name_start+100].strip()
                        
                        if code not in project_codes:
                            project_codes[code] = {
                                'page': page_num,
                                'name': name_line[:50],
                                'full_text': line[:200]
                            }
            
            print(f"找到项目编码：{len(project_codes)} 个")
            
            # 保存索引
            index_data = {
                'file_name': pdf_path.name,
                'total_pages': page_count,
                'extract_date': datetime.now().isoformat(),
                'project_codes': project_codes
            }
            
            # 确定是清单几
            if '1' in pdf_path.name or '(1)' in pdf_path.name:
                list_num = '1'
            elif '2' in pdf_path.name or '(2)' in pdf_path.name:
                list_num = '2'
            elif '3' in pdf_path.name or '(3)' in pdf_path.name:
                list_num = '3'
            else:
                list_num = 'unknown'
            
            index_path = OUTPUT_DIR / f'清单{list_num}_页码索引.json'
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            
            print(f"索引已保存：{index_path}")
            all_indices[f'清单{list_num}'] = index_data
            
    except Exception as e:
        print(f"解析失败：{e}")
        import traceback
        traceback.print_exc()

# 生成对比分析表
print(f"\n{'='*60}")
print("生成对比分析表...")
print('='*60)

# 已知的 37 项差异编码
known_differences = [
    '040103002003', '041001001001', '040103002005', '040203006001',
    '040103002002', '040103002001', '041001001002', '040103002004',
    '041001001004', '041001006008', '040203007001', '040103002006',
    '041001001003', '041106001001', '040303006001',
    '041001002002', '041001006003', '041001006005', '041001006009',
    '041001002001', '041001006001', '040204002002', '040101002002',
    '040101002003', '040504009003', '040103001005', '041001006004',
    '040103001007', '040101002001', '041001006006', '040204002001',
    '041001006007', '060104002002', '010512008003', '041001002003',
    '041001006002', '010404001002'
]

# 创建对比表
comparison_rows = []

for code in known_differences:
    row = {
        '项目编码': code,
        '清单 1_页码': all_indices.get('清单 1', {}).get('project_codes', {}).get(code, {}).get('page', '待查找'),
        '清单 1_名称': all_indices.get('清单 1', {}).get('project_codes', {}).get(code, {}).get('name', ''),
        '清单 2_页码': all_indices.get('清单 2', {}).get('project_codes', {}).get(code, {}).get('page', '待查找'),
        '清单 2_名称': all_indices.get('清单 2', {}).get('project_codes', {}).get(code, {}).get('name', ''),
        '清单 3_页码': all_indices.get('清单 3', {}).get('project_codes', {}).get(code, {}).get('page', '待查找'),
        '清单 3_名称': all_indices.get('清单 3', {}).get('project_codes', {}).get(code, {}).get('name', ''),
    }
    comparison_rows.append(row)

# 保存对比表
comparison_path = OUTPUT_DIR / '工程量清单对比分析_带页码索引.json'
with open(comparison_path, 'w', encoding='utf-8') as f:
    json.dump({
        'extract_date': datetime.now().isoformat(),
        'total_differences': len(known_differences),
        'indices': all_indices,
        'comparison': comparison_rows
    }, f, ensure_ascii=False, indent=2)

print(f"对比分析表已保存：{comparison_path}")
print(f"\n✅ 解析完成！共处理 {len(known_differences)} 项差异")
