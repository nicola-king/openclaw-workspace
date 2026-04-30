#!/usr/bin/env python3
"""生成三份清单差异位置对照表（带页码）"""

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
print(f"清单2: {index2['total_pages']}页，{len(index2.get('project_codes', {}))}个项目")
print(f"清单3: {index3['total_pages']}页，{len(index3.get('project_codes', {}))}个项目")

# 找出共同点位
locs1 = set(index1.get('location_names', []))
locs2 = set(index2.get('location_names', []))
locs3 = set(index3.get('location_names', []))
common_all = locs1 & locs2 & locs3

print(f"\n三份清单共有 {len(common_all)} 个共同点位")

# 生成页码对照表
print("\n生成差异位置对照表...")

# CSV 文件
csv_path = REPO_DIR / '三份清单差异位置对照表 (带页码).csv'
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write('序号，点位名称，清单 1 页码，清单 2 页码，清单3 页码，差异说明，核验确认\n')
    
    for i, loc in enumerate(sorted(common_all), 1):
        # 查找每个点位在各清单中的页码
        pages1 = []
        pages2 = []
        pages3 = []
        
        for code, data in index1.get('project_codes', {}).items():
            if loc in data.get('location', '') or loc in data.get('text_snippet', ''):
                pages1.append(str(data.get('page', '')))
        
        for code, data in index2.get('project_codes', {}).items():
            if loc in data.get('location', '') or loc in data.get('text_snippet', ''):
                pages2.append(str(data.get('page', '')))
        
        for code, data in index3.get('project_codes', {}).items():
            if loc in data.get('location', '') or loc in data.get('text_snippet', ''):
                pages3.append(str(data.get('page', '')))
        
        page1_str = ';'.join(sorted(set(pages1), key=int)) if pages1 else '待查找'
        page2_str = ';'.join(sorted(set(pages2), key=int)) if pages2 else '待查找'
        page3_str = ';'.join(sorted(set(pages3), key=int)) if pages3 else '待查找'
        
        # 判断是否有差异
        diff_note = ''
        if pages1 and pages2 and pages3:
            if len(set(pages1)) != len(set(pages2)) or len(set(pages2)) != len(set(pages3)):
                diff_note = '页数不一致'
            elif set(pages1) != set(pages2) or set(pages2) != set(pages3):
                diff_note = '页码位置不同'
        elif not pages1:
            diff_note = '清单 1 未找到'
        elif not pages2:
            diff_note = '清单 2 未找到'
        elif not pages3:
            diff_note = '清单 3 未找到'
        
        f.write(f'{i},{loc},{page1_str},{page2_str},{page3_str},{diff_note},\n')

print(f"✅ 对照表已保存：{csv_path}")

# Markdown 报告
report_path = REPO_DIR / '三份清单差异位置对照报告 (带页码).md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# 渝中区污水溢流整治项目 - 三份清单差异位置对照表\n\n")
    f.write("## （带页码·方便人工核对）\n\n")
    f.write(f"**编制时间：** 2026 年 4 月 21 日 {datetime.now().strftime('%H:%M')}\n\n")
    f.write(f"**分析范围：** 工程量清单（1）、（2）、（3）共同点位\n\n")
    
    f.write("## 📊 清单基本信息\n\n")
    f.write(f"| 清单 | 总页数 | 项目数量 | 点位数量 |\n")
    f.write(f"|------|--------|---------|---------|\n")
    f.write(f"| 工程量清单 (1) | {index1['total_pages']}页 | {len(index1.get('project_codes', {}))}个 | {len(locs1)}个 |\n")
    f.write(f"| 工程量清单 (2) | {index2['total_pages']}页 | {len(index2.get('project_codes', {}))}个 | {len(locs2)}个 |\n")
    f.write(f"| 工程量清单 (3) | {index3['total_pages']}页 | {len(index3.get('project_codes', {}))}个 | {len(locs3)}个 |\n\n")
    
    f.write(f"## 📍 共同点位数量：{len(common_all)} 个\n\n")
    
    f.write("## 📋 差异位置对照表\n\n")
    f.write("| 序号 | 点位名称 | 清单1 页码 | 清单2 页码 | 清单3 页码 | 差异说明 |\n")
    f.write("|:----:|---------|:---------:|:---------:|:---------:|---------|\n")
    
    for i, loc in enumerate(sorted(common_all), 1):
        pages1 = []
        pages2 = []
        pages3 = []
        
        for code, data in index1.get('project_codes', {}).items():
            if loc in data.get('location', '') or loc in data.get('text_snippet', ''):
                pages1.append(str(data.get('page', '')))
        
        for code, data in index2.get('project_codes', {}).items():
            if loc in data.get('location', '') or loc in data.get('text_snippet', ''):
                pages2.append(str(data.get('page', '')))
        
        for code, data in index3.get('project_codes', {}).items():
            if loc in data.get('location', '') or loc in data.get('text_snippet', ''):
                pages3.append(str(data.get('page', '')))
        
        page1_str = ';'.join(sorted(set(pages1), key=int)) if pages1 else '待查找'
        page2_str = ';'.join(sorted(set(pages2), key=int)) if pages2 else '待查找'
        page3_str = ';'.join(sorted(set(pages3), key=int)) if pages3 else '待查找'
        
        diff_note = ''
        if pages1 and pages2 and pages3:
            if set(pages1) != set(pages2) or set(pages2) != set(pages3):
                diff_note = '⚠️ 页码位置不同'
        elif not pages1:
            diff_note = '❌ 清单 1 未找到'
        elif not pages2:
            diff_note = '❌ 清单2 未找到'
        elif not pages3:
            diff_note = '❌ 清单3 未找到'
        
        f.write(f"| {i} | {loc[:50]} | {page1_str} | {page2_str} | {page3_str} | {diff_note} |\n")
    
    f.write("\n## 🔍 使用说明\n\n")
    f.write("1. **核对页码**：打开三份清单 PDF，跳转到对应页码\n")
    f.write("2. **对比工程量**：对比相同点位的工程量是否一致\n")
    f.write("3. **对比单价**：对比综合单价是否一致\n")
    f.write("4. **标注差异**：在'核验确认'栏标注差异情况并签字\n\n")
    
    f.write("---\n\n")
    f.write("**报告编制：** 太一 AGI 系统 (造价工程师)\n")
    f.write(f"**时间：** 2026 年 4 月 21 日 {datetime.now().strftime('%H:%M')}\n")

print(f"✅ 报告已保存：{report_path}")
print(f"\n共 {len(common_all)} 个共同点位的页码对照表已生成")
