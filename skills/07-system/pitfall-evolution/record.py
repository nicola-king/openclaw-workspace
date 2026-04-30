#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
踩坑记录工具

用法:
    python3 record.py --type "配置坑" --desc "问题描述" --solution "解决方案"
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
PITFALLS_FILE = WORKSPACE / "memory" / "PITFALLS.md"
TODAY_FILE = WORKSPACE / "memory" / f"{datetime.now().strftime('%Y-%m-%d')}.md"

def get_seq():
    """获取今日序号"""
    today = datetime.now().strftime('%Y%m%d')
    seq = 1
    # 简单实现，实际应该查询已有记录
    return seq

def create_pitfall_record(pitfall_type, description, solution):
    """创建踩坑记录"""
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    lesson_id = f"LESSON-{datetime.now().strftime('%Y%m%d')}-{get_seq()}"
    
    # 写入 PITFALLS.md
    pitfalls_entry = f"""
### {date_str}: {pitfall_type}

**编号**: `{lesson_id}`

**问题**: {description}

**根因**: [待分析]

**解决方案**: {solution}

**教训**: > [待提炼]

**相关文件**:
- [待补充]

**状态**: 🟡 处理中 | ⏳ 待记录
"""
    
    with open(PITFALLS_FILE, 'a', encoding='utf-8') as f:
        f.write(pitfalls_entry)
    
    # 写入当日记忆
    today_entry = f"""
## {lesson_id}: {pitfall_type}

**问题**: {description}

**解决方案**: {solution}

**状态**: 🟡 处理中
"""
    
    if TODAY_FILE.exists():
        with open(TODAY_FILE, 'a', encoding='utf-8') as f:
            f.write(today_entry)
    else:
        with open(TODAY_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# {date_str} 记忆\n\n{today_entry}")
    
    print(f"✅ 踩坑记录已创建")
    print(f"   编号：{lesson_id}")
    print(f"   类型：{pitfall_type}")
    print(f"   文件：{PITFALLS_FILE}")
    print(f"   记忆：{TODAY_FILE}")
    
    return lesson_id

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='踩坑记录工具')
    parser.add_argument('--type', required=True, help='踩坑类型')
    parser.add_argument('--desc', required=True, help='问题描述')
    parser.add_argument('--solution', required=True, help='解决方案')
    
    args = parser.parse_args()
    
    lesson_id = create_pitfall_record(args.type, args.desc, args.solution)
    print(f"\n📝 请继续完成:")
    print(f"   1. 分析根因")
    print(f"   2. 提炼教训")
    print(f"   3. 更新状态为 ✅ 已解决 | 📝 已记录")
