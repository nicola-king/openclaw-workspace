#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理重复报告文件

保留策略:
1. emerged-skill: 保留最近 20 个
2. hourly-summary: 保留最近 24 个 (1 天)
3. self-evolution: 保留最近 50 个
4. enhanced-bug-fix: 保留最近 10 个

作者：太一 AGI
创建：2026-04-14
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
REPORTS_DIR = WORKSPACE / "reports"
SKILLS_DIR = WORKSPACE / "skills"


def cleanup_files(pattern, keep_count, description):
    """清理文件，保留最新的 keep_count 个"""
    print(f"\n🗑️ 清理 {description}...")
    
    files = list(REPORTS_DIR.glob(pattern))
    
    if len(files) <= keep_count:
        print(f"  ✅ 无需清理 (当前 {len(files)} 个，保留 {keep_count} 个)")
        return 0
    
    # 按修改时间排序
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    
    # 删除旧文件
    deleted = 0
    for file in files[keep_count:]:
        try:
            file.unlink()
            deleted += 1
        except Exception as e:
            print(f"  ⚠️ 删除失败：{file.name} - {e}")
    
    print(f"  ✅ 删除 {deleted} 个文件 (保留 {keep_count} 个)")
    return deleted


def cleanup_emerged_skills(keep_count=20):
    """清理 emerged-skill 目录"""
    print(f"\n🗑️ 清理 emerged-skill (保留最近 {keep_count} 个)...")
    
    skills = list(SKILLS_DIR.glob("emerged-skill-*"))
    
    if len(skills) <= keep_count:
        print(f"  ✅ 无需清理 (当前 {len(skills)} 个)")
        return 0
    
    # 按目录名排序 (时间戳)
    skills.sort(key=lambda s: s.name, reverse=True)
    
    # 删除旧目录
    deleted = 0
    for skill_dir in skills[keep_count:]:
        try:
            import shutil
            shutil.rmtree(skill_dir)
            deleted += 1
        except Exception as e:
            print(f"  ⚠️ 删除失败：{skill_dir.name} - {e}")
    
    print(f"  ✅ 删除 {deleted} 个目录 (保留 {keep_count} 个)")
    return deleted


def main():
    """主函数"""
    print("=" * 60)
    print("🗑️ 清理重复报告文件")
    print("=" * 60)
    print(f"\n清理时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_deleted = 0
    
    # 清理各类报告
    total_deleted += cleanup_files("hourly-summary-*.json", 24, "小时汇总报告")
    total_deleted += cleanup_files("self-evolution-*.json", 50, "自进化报告")
    total_deleted += cleanup_files("self-evolution-*.md", 50, "自进化 MD 报告")
    total_deleted += cleanup_files("enhanced-bug-fix-*.md", 10, "Bug 修复报告")
    total_deleted += cleanup_emerged_skills(20)
    
    print("\n" + "=" * 60)
    print(f"📊 清理完成")
    print("=" * 60)
    print(f"总计删除：{total_deleted} 个文件/目录")
    
    return total_deleted


if __name__ == '__main__':
    total = main()
    sys.exit(0 if total < 100 else 1)
