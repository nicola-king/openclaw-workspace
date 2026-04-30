#!/usr/bin/env python3
"""解析工程量清单 (2) PDF - 提取点位名称"""

import pdfplumber
import json
from pathlib import Path
from datetime import datetime
import os
import re

PDF_DIR = Path('/home/nicola/.openclaw/media/inbound')
OUTPUT_DIR = Path('/home/nicola/.openclaw/workspace/reports')

# 查找清单 2 PDF（可能有多个，取最新的）
pdf_files = []
for f in PDF_DIR.glob('*.pdf'):
    if 'å_ç_é_æ_å_2' in f.name or ('工程量清单' in f.name and '2' in f.name):
        pdf_files.append(f)

if not pdf_files:
    print("❌ 未找到工程量清单 (2) PDF 文件")
    exit(1)

# 取最新修改的文件
pdf_file = max(pdf_files, key=lambda f: f.stat().st_mtime)

if not pdf_file:
    print("❌ 未找到工程量清单 (2) PDF 文件")
    exit(1)

print(f"解析：{pdf_file.name}")

try:
    with pdfplumber.open(pdf_file) as pdf:
        page_count = len(pdf.pages)
        print(f"总页数：{page_count}")
        
        # 提取点位名称和项目编码
        project_codes = {}
        location_names = set()
        
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            text = page.extract_text()
            
            if not text:
                continue
            
            # 查找工程名称/点位名称（通常在页面顶部或表格标题中）
            lines = text.split('\n')
            current_location = None
            
            for line in lines:
                # 匹配工程名称模式
                if '工程' in line and '名称' in line:
                    match = re.search(r'工程名称 [：:]\s*(.+?)(?:\n|$)', line)
                    if match:
                        current_location = match.group(1).strip()[:50]
                        location_names.add(current_location)
                
                # 匹配片区名称模式
                if any(keyword in line for keyword in ['村', '社区', '片区', '街道', '路', '巷']):
                    if '工程' in line or '区' in line:
                        location_names.add(line.strip()[:50])
                
                # 查找项目编码
                code_match = re.search(r'(0[146]\d{9})', line)
                if code_match:
                    code = code_match.group(1)
                    if code not in project_codes:
                        project_codes[code] = {
                            'page': page_num,
                            'location': current_location or '待确认',
                            'text_snippet': line[:100]
                        }
        
        print(f"找到项目编码：{len(project_codes)} 个")
        print(f"找到点位名称：{len(location_names)} 个")
        
        # 保存索引
        index_data = {
            'file_name': pdf_file.name,
            'total_pages': page_count,
            'extract_date': datetime.now().isoformat(),
            'location_names': list(location_names),
            'project_codes': project_codes
        }
        
        index_path = OUTPUT_DIR / '清单2_页码索引.json'
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 索引已保存：{index_path}")
        print(f"点位名称：{list(location_names)[:10]}")
        
except Exception as e:
    print(f"❌ 解析失败：{e}")
    import traceback
    traceback.print_exc()
