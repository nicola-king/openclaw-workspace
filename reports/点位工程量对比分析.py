#!/usr/bin/env python3
"""对比相同点位在不同清单中的工程量差异"""

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

locs1 = set(index1.get('location_names', []))
locs2 = set(index2.get('location_names', []))
locs3 = set(index3.get('location_names', []))

# 找出共同点位
common_all = locs1 & locs2 & locs3
print(f"\n三份清单共有 {len(common_all)} 个共同点位")

# 生成对比报告
print("\n生成点位工程量对比报告...")

report_lines = [
    "# 渝中区污水溢流整治项目 - 点位工程量对比分析报告",
    "## （相同点位在不同清单中的差异对比）",
    "",
    "**编制时间：** 2026 年 4 月 21 日 16:50",
    "**分析范围：** 工程量清单（1）、（2）、（3）共同点位",
    "",
    "## 📊 点位分布统计",
    "",
    f"- **清单 1:** {len(locs1)} 个点位",
    f"- **清单 2:** {len(locs2)} 个点位",
    f"- **清单3:** {len(locs3)} 个点位",
    f"- **三份清单共同点位:** {len(common_all)} 个",
    "",
    "## 📍 三份清单共同点位列表 (53 个)",
    "",
]

for i, loc in enumerate(sorted(common_all), 1):
    report_lines.append(f"{i:3d}. {loc}")

report_lines.extend([
    "",
    "## 🔍 差异分析说明",
    "",
    "由于三份清单包含相同的 53 个点位，需要对比：",
    "",
    "1. **相同点位的工程量是否一致**",
    "2. **相同点位的综合单价是否一致**",
    "3. **相同点位的合价是否一致**",
    "",
    "## ⚠️ 注意事项",
    "",
    "- 如果相同点位的工程量不一致，可能存在：",
    "  - 设计变更",
    "  - 计算错误",
    "  - 统计口径不同",
    "",
    "- 如果相同点位的单价不一致，可能存在：",
    "  - 价格调整",
    "  - 定额版本不同",
    "  - 计价标准不同",
    "",
    "## 📋 下一步工作",
    "",
    "需要详细对比每个点位的：",
    "",
    "1. 分部分项工程量清单",
    "2. 措施项目清单",
    "3. 综合单价分析表",
    "",
    "---",
    "",
    "**报告编制：** 太一 AGI 系统 (造价工程师)",
    "**时间：** 2026 年 4 月 21 日 16:50",
])

# 保存报告
report_path = REPO_DIR / '点位工程量对比分析报告 (共同点位).md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"✅ 报告已保存：{report_path}")

# 生成 CSV 对比表
csv_path = REPO_DIR / '共同点位工程量对比表.csv'
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write('序号，点位名称，清单1 页码，清单 2 页码，清单 3 页码，工程量差异，单价差异，合价差异，核验确认\n')
    for i, loc in enumerate(sorted(common_all), 1):
        # 查找每个点位在各清单中的页码
        page1 = page2 = page3 = '待查找'
        for code, data in index1.get('project_codes', {}).items():
            if loc in data.get('location', ''):
                page1 = str(data.get('page', ''))
                break
        for code, data in index2.get('project_codes', {}).items():
            if loc in data.get('location', ''):
                page2 = str(data.get('page', ''))
                break
        for code, data in index3.get('project_codes', {}).items():
            if loc in data.get('location', ''):
                page3 = str(data.get('page', ''))
                break
        f.write(f'{i},{loc},{page1},{page2},{page3},待对比，待对比，待对比，\n')

print(f"✅ 对比表已保存：{csv_path}")
print(f"\n共 {len(common_all)} 个共同点位需要对比")
