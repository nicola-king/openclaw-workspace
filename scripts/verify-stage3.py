#!/usr/bin/env python3
"""
阶段 3 验收脚本
执行时间：2026-04-07 23:00
"""

import json
import os
from datetime import datetime

def count_high_value_tasks():
    """统计高价值任务发现数量"""
    filepath = "/home/nicola/.openclaw/workspace/memory/high-value-opportunities.md"
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            return content.count("- [")
    except:
        return 0

def count_a_level_notes():
    """统计 A 级学习笔记数量"""
    filepath = "/home/nicola/.openclaw/workspace/memory/night-learning-output.md"
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            return content.count("价值评级：A")
    except:
        return 0

def count_interventions_last_7_days():
    """统计过去 7 天人工干预次数"""
    filepath = "/home/nicola/.openclaw/workspace/memory/human-intervention-log.md"
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            # 简化：统计所有记录（实际应该按日期过滤）
            return content.count("## ")
    except:
        return 0

def get_avg_collaboration_score():
    """获取 Bot 协作平均分"""
    filepath = "/home/nicola/.openclaw/workspace/memory/bot-collaboration-scores.md"
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            # 简化：解析平均分（实际需要更复杂的解析）
            if "平均分：0" in content:
                return 0
            return 0  # 待实现
    except:
        return 0

def check_monetization_progress():
    """检查变现进展"""
    # 简化：检查是否有收入记录
    return False  # 待实现

def verify_stage3():
    """阶段 3 验收"""
    print("=" * 60)
    print("🎯 阶段 3 验收（价值驱动）")
    print("=" * 60)
    print()
    
    checks = [
        ("M1: 高价值任务发现", count_high_value_tasks() >= 3, f"当前：{count_high_value_tasks()}个"),
        ("M2: 变现路径验证", check_monetization_progress(), "当前：¥0"),
        ("M3: A 级学习笔记", count_a_level_notes() >= 3, f"当前：{count_a_level_notes()}篇"),
        ("M4: 人工干预频率", count_interventions_last_7_days() <= 1, f"当前：{count_interventions_last_7_days()}次/周"),
        ("M5: Bot 协作评分", get_avg_collaboration_score() >= 9, f"当前：{get_avg_collaboration_score()}/10"),
    ]
    
    passed = sum(1 for _, result, _ in checks if result)
    total = len(checks)
    
    print("验收结果:")
    print()
    for name, result, detail in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {name}: {detail}")
    
    print()
    print("-" * 60)
    print(f"通过率：{passed}/{total} ({passed * 20}%)")
    print("-" * 60)
    print()
    
    if passed == total:
        print("✅ 阶段 3 验收通过！")
        print()
        print("下一步：正式进入阶段 3（价值驱动）")
        update_constitution(True)
    else:
        print("❌ 阶段 3 验收失败")
        print()
        print("未通过项目:")
        for name, result, detail in checks:
            if not result:
                print(f"  - {name}: {detail}")
        print()
        print("建议:")
        print("  1. 分析未通过原因")
        print("  2. 制定补救计划")
        print("  3. 申请延期或调整目标")
        update_constitution(False)
    
    return passed == total

def update_constitution(passed):
    """更新宪法状态"""
    state_file = "/home/nicola/.openclaw/workspace/memory/agi-evolution-state.md"
    try:
        with open(state_file, 'r') as f:
            content = f.read()
        
        if passed:
            content = content.replace("🟡 验收中", "✅ 已完成")
            content = content.replace("2→3 过渡期", "阶段 3：价值驱动")
        else:
            content = content.replace("🟡 验收中", "❌ 验收失败")
        
        with open(state_file, 'w') as f:
            f.write(content)
        
        print(f"✅ 状态文件已更新：{state_file}")
    except Exception as e:
        print(f"⚠️ 更新状态文件失败：{e}")

if __name__ == "__main__":
    verify_stage3()
