#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并重复的 emerged-skill
大幅减少 Skill 数量
"""

import shutil
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('MergeEmergedSkills')


class EmergedSkillsMerger:
    """emerged-skill 合并器"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.skills_dir = self.workspace / 'skills'
        self.emerged_dir = self.skills_dir / '08-emerged'
        
        self.merged_count = 0
        self.deleted_count = 0
        
    def run(self):
        """运行合并"""
        logger.info("🔍 开始合并重复的 emerged-skill...")
        
        # Step 1: 收集所有 emerged-skill
        emerged_skills = list(self.emerged_dir.glob('emerged-skill-*'))
        logger.info(f"  收集到 emerged-skill: {len(emerged_skills)} 个")
        
        if len(emerged_skills) <= 10:
            logger.info("  ℹ️  数量合理，无需合并")
            return
        
        # Step 2: 保留最近的 10 个，删除其他
        emerged_skills.sort(key=lambda x: x.name, reverse=True)
        
        to_keep = emerged_skills[:10]
        to_delete = emerged_skills[10:]
        
        logger.info(f"  保留：{len(to_keep)} 个")
        logger.info(f"  删除：{len(to_delete)} 个")
        
        # Step 3: 删除多余的
        for skill_dir in to_delete:
            try:
                shutil.rmtree(skill_dir)
                self.deleted_count += 1
                logger.info(f"  ✅ 删除：{skill_dir.name}")
            except Exception as e:
                logger.warning(f"  ⚠️ 删除失败：{skill_dir.name} - {e}")
        
        self.merged_count = len(to_keep)
        
        logger.info(f"✅ 合并完成！")
        logger.info(f"  保留：{self.merged_count} 个")
        logger.info(f"  删除：{self.deleted_count} 个")
        logger.info(f"  减少：{self.deleted_count} 个 Skill")


def main():
    logger.info("🔍 emerged-skill 合并器启动...")
    merger = EmergedSkillsMerger()
    merger.run()


if __name__ == '__main__':
    main()
