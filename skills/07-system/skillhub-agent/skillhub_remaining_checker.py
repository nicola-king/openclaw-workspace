#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillHub 剩余 Skill 检查 Agent v3.0

检查是否还有剩余:
1. 剩余未分类 Skill
2. 剩余不健康 Skill
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SkillhubRemainingChecker')


class SkillhubRemainingChecker:
    """SkillHub 剩余 Skill 检查 Agent"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.skills_dir = self.workspace / 'skills'
        
        self.results = {
            'uncategorized': {
                'total': 0,
                'skills': [],
            },
            'unhealthy': {
                'total': 0,
                'skills': [],
            },
        }
        
        logger.info("🔍 SkillHub 剩余 Skill 检查 Agent 已初始化")
    
    def run(self):
        """运行检查"""
        logger.info("🔍 开始检查剩余 Skill...")
        
        # Step 1: 检查未分类 Skill
        self.check_uncategorized_skills()
        
        # Step 2: 检查不健康 Skill
        self.check_unhealthy_skills()
        
        # Step 3: 生成报告
        self.generate_report()
        
        logger.info("✅ 剩余 Skill 检查完成！")
    
    def check_uncategorized_skills(self):
        """检查未分类 Skill"""
        logger.info("📂 检查未分类 Skill...")
        
        uncategorized = []
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.') or skill_dir.name.startswith('0'):
                continue
            uncategorized.append(skill_dir.name)
        
        self.results['uncategorized']['total'] = len(uncategorized)
        self.results['uncategorized']['skills'] = uncategorized
        
        logger.info(f"  发现未分类 Skill: {len(uncategorized)} 个")
        if uncategorized:
            logger.info(f"  列表：{uncategorized[:20]}{'...' if len(uncategorized) > 20 else ''}")
    
    def check_unhealthy_skills(self):
        """检查不健康 Skill"""
        logger.info("🔧 检查不健康 Skill...")
        
        unhealthy = []
        for category_dir in self.skills_dir.iterdir():
            if not category_dir.is_dir() or not category_dir.name.startswith('0'):
                continue
            
            for skill_dir in category_dir.iterdir():
                if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                    continue
                
                # 检查健康度
                has_skill_md = (skill_dir / 'SKILL.md').exists()
                has_self_evolution = len(list(skill_dir.glob('self_evolution_*.py'))) > 0
                
                if not has_skill_md or not has_self_evolution:
                    skill_path = f"{category_dir.name}/{skill_dir.name}"
                    unhealthy.append(skill_path)
                    
                    # 记录原因
                    reasons = []
                    if not has_skill_md:
                        reasons.append('缺少 SKILL.md')
                    if not has_self_evolution:
                        reasons.append('缺少自进化文件')
                    
                    logger.info(f"  ⚠️ 不健康：{skill_path} - {', '.join(reasons)}")
        
        self.results['unhealthy']['total'] = len(unhealthy)
        self.results['unhealthy']['skills'] = unhealthy
        
        logger.info(f"  发现不健康 Skill: {len(unhealthy)} 个")
        if unhealthy:
            logger.info(f"  列表：{unhealthy[:20]}{'...' if len(unhealthy) > 20 else ''}")
    
    def generate_report(self):
        """生成报告"""
        logger.info("📝 生成检查报告...")
        
        report_path = self.workspace / 'SKILLHUB_REMAINING_SKILLS_CHECK_REPORT.md'
        
        content = f"""# 🔍 SkillHub 剩余 Skill 检查报告

> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **执行人**: SkillHub 剩余 Skill 检查 Agent  
> **状态**: ✅ 完成

---

## 📊 未分类 Skill

**总数**: {self.results['uncategorized']['total']} 个

"""
        if self.results['uncategorized']['skills']:
            content += "### 列表\n\n"
            for skill in self.results['uncategorized']['skills']:
                content += f"- {skill}\n"
        else:
            content += "✅ 无未分类 Skill\n"
        
        content += f"""
## 🔧 不健康 Skill

**总数**: {self.results['unhealthy']['total']} 个

"""
        if self.results['unhealthy']['skills']:
            content += "### 列表\n\n"
            for skill in self.results['unhealthy']['skills']:
                content += f"- {skill}\n"
        else:
            content += "✅ 无不健康 Skill\n"
        
        content += f"""
## ✅ 总结

**未分类 Skill**: {self.results['uncategorized']['total']} 个  
**不健康 Skill**: {self.results['unhealthy']['total']} 个

"""
        if self.results['uncategorized']['total'] == 0 and self.results['unhealthy']['total'] == 0:
            content += "🎉 所有 Skill 已分类且健康！\n"
        else:
            content += "⚠️ 仍有剩余 Skill 需要处理\n"
        
        content += f"""
---

**🔍 SkillHub 剩余 Skill 检查报告完成**

**太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        report_path.write_text(content, encoding='utf-8')
        logger.info(f"✅ 检查报告已生成：{report_path}")


def main():
    logger.info("🔍 SkillHub 剩余 Skill 检查 Agent 启动...")
    checker = SkillhubRemainingChecker()
    checker.run()


if __name__ == '__main__':
    main()
