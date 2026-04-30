#!/usr/bin/env python3
"""
情景模式系统 - 384 个阶段内容填充脚本
从 384-skills-complete.json 填充到各状态目录
"""

import json
from pathlib import Path
from datetime import datetime

# 读取 384 Skills 数据
DATA_FILE = '/home/nicola/.openclaw/workspace/data/skills/384-skills-complete.json'
SKILLS_DIR = Path('/home/nicola/.openclaw/workspace/skills/scenarios')

print('=' * 60)
print('🧠 情景模式系统 - 384 阶段内容填充')
print('=' * 60)

# 读取数据
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    skills_data = json.load(f)

print(f'源数据：{len(skills_data)} 个 Skills')
print(f'目标目录：{SKILLS_DIR}')
print()

# 按状态 - 阶段分组
stages_by_state = {}
for skill in skills_data:
    state_id = skill['state_id']
    stage = skill['stage']
    key = f"{state_id}-stage{stage}"
    stages_by_state[key] = skill

# 为每个状态目录填充阶段内容
filled_count = 0
for state_dir in SKILLS_DIR.iterdir():
    if not state_dir.is_dir():
        continue
    
    # 提取状态 ID (如 A01)
    state_id = state_dir.name.split('-')[0]
    
    # 为 6 个阶段创建内容文件
    for stage_num in range(1, 7):
        key = f"{state_id}-stage{stage_num}"
        if key in stages_by_state:
            skill = stages_by_state[key]
            
            # 创建阶段 JSON 文件
            stage_file = state_dir / f"stage{stage_num}.json"
            content = {
                "stage": stage_num,
                "stage_name": skill['stage_name'],
                "type": skill['type'],
                "theme": skill['theme'],
                "situation": skill['situation'],
                "core_problem": skill['core_problem'],
                "decision": skill['decision'],
                "action": skill['action'],
                "avoid": skill['avoid'],
                "psychology": skill['psychology'],
                "metadata": skill['metadata']
            }
            
            with open(stage_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            
            filled_count += 1

print('=' * 60)
print(f'✅ 填充完成：{filled_count}/384 个阶段内容')
print(f'📁 位置：{SKILLS_DIR}')
print('=' * 60)

# 更新状态文件
status_file = Path('/tmp/scenario-api-status.json')
if status_file.exists():
    with open(status_file, 'r') as f:
        status = json.load(f)
    
    status['progress'] = 100
    status['status'] = '✅ 384 阶段完成'
    status['details']['filled'] = filled_count
    status['completed_at'] = datetime.now().isoformat()
    
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=2)
    
    print(f'\n✅ 状态文件已更新：100% 完成')
