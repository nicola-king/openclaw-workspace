#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillHub 清理和智能分类 Agent v3.0

执行:
1. 删除所有空 Skill
2. 删除所有待删除 Skill
3. 智能分类有用 Skill
"""

import shutil
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SkillhubCleanupAndClassify')


class SkillhubCleanupAndClassify:
    """SkillHub 清理和智能分类 Agent"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.skills_dir = self.workspace / 'skills'
        
        self.stats = {
            'deleted_empty': 0,
            'deleted_useless': 0,
            'classified': 0,
        }
        
        # 空 Skill 列表 (从分析报告)
        self.empty_skills = [
            'agent-swap', 'web', 'daily-report-generator', 'dreaming',
            'artistic-code', 'batch-safe-processing', 'jimeng-cli',
            'terraform-apply', 'qa-supervisor', 'undercover-mode',
            'growth-experiment', 'agent-reach', 'china-textbook-search',
            'classic-chinese-poetry', 'unsplash-image', 'multi-agent-scoring',
            'llm-finetune', 'advisor-strategy', 'rust-bridge', 'sdk',
            'chinese-traditional-aesthetics', 'aesthetic-research',
            'easter-egg', 'weather', 'daily-wisdom', 'vector-db',
            'arc-reel-workflow', 'classic-chinese-art', 'project-deployer',
            'weixin-file-sender', 'webhook-relay', 'npm-audit',
            'gemini-cli', 'airtable-sync', 'rag-pipeline', 'news-fetcher',
            'pet-companion', 'reverse-synthid', 'wechat-article-publish',
            'chinese-art-research', 'the-well-processor', '市政工程造价',
            'notebooklm-cli',
        ]
        
        # 待删除 Skill 列表
        self.to_delete_skills = []
        for i in range(1, 24):
            for hour in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.to_delete_skills.append(f'emerged-skill-20260413-{hour:02d}{i:02d}01')
        
        # 有用 Skill 及其建议分类
        self.useful_skills = {
            'suwen': '07-system',
            'yi': '07-system',
            'google-search-cn': '04-integration',
            'security-hardening': '07-system',
            'quota-aware-model-router': '07-system',
            'marketplace': '07-system',
            'semantic-search': '04-integration',
            'session-enhancement': '07-system',
            'geo-model-router': '07-system',
            'smart_router': '07-system',
            'tv-control': '07-system',
            'today-stage': '07-system',
            'bot-dashboard': '07-system',
            'agora-deliberation': '07-system',
            '10d-scoring': '07-system',
            'commands-list': '07-system',
            'paoding': '07-system',
            'shoucangli': '07-system',
            'quality-validator': '07-system',
            'agent-spawning': '07-system',
            'shared': '07-system',
            'yijing': '07-system',
            'knowledge-extractor': '07-system',
            'cost-agent': '07-system',
            'hermes-learning-loop': '07-system',
            'cli-toolkit': '07-system',
            'reverse-SynthID': '07-system',
            'yuanshu-teahouse': '07-system',
            'epub-book-generator': '07-system',
            'mind-model-extractor': '07-system',
            'paddleocr': '07-system',
            'play-music': '07-system',
            'heal-state': '07-system',
            'wecom': '07-system',
            'honest-boundary': '07-system',
            'wangliang': '07-system',
            'steward': '07-system',
            'brain-hands-separator': '07-system',
            'civil-engineering-cost': '07-system',
            'error-handler': '07-system',
        }
        
        logger.info("🗑️ SkillHub 清理和智能分类 Agent 已初始化")
    
    def run(self):
        """运行清理和分类"""
        logger.info("🗑️ 开始清理和智能分类...")
        
        # Step 1: 删除空 Skill
        self.delete_empty_skills()
        
        # Step 2: 删除待删除 Skill
        self.delete_useless_skills()
        
        # Step 3: 智能分类有用 Skill
        self.classify_useful_skills()
        
        # Step 4: 生成报告
        self.generate_report()
        
        logger.info("✅ 清理和智能分类完成！")
    
    def delete_empty_skills(self):
        """删除空 Skill"""
        logger.info("🗑️ 删除空 Skill...")
        
        for skill_name in self.empty_skills:
            skill_dir = self.skills_dir / skill_name
            if skill_dir.exists():
                try:
                    shutil.rmtree(skill_dir)
                    self.stats['deleted_empty'] += 1
                    logger.info(f"  ✅ 删除：{skill_name}")
                except Exception as e:
                    logger.warning(f"  ⚠️ 删除失败：{skill_name} - {e}")
        
        logger.info(f"  删除空 Skill: {self.stats['deleted_empty']} 个")
    
    def delete_useless_skills(self):
        """删除待删除 Skill"""
        logger.info("🗑️ 删除待删除 Skill...")
        
        for skill_name in self.to_delete_skills:
            skill_dir = self.skills_dir / skill_name
            if skill_dir.exists():
                try:
                    shutil.rmtree(skill_dir)
                    self.stats['deleted_useless'] += 1
                    logger.info(f"  ✅ 删除：{skill_name}")
                except Exception as e:
                    logger.warning(f"  ⚠️ 删除失败：{skill_name} - {e}")
        
        logger.info(f"  删除待删除 Skill: {self.stats['deleted_useless']} 个")
    
    def classify_useful_skills(self):
        """智能分类有用 Skill"""
        logger.info("📂 智能分类有用 Skill...")
        
        for skill_name, target_category in self.useful_skills.items():
            skill_dir = self.skills_dir / skill_name
            target_dir = self.skills_dir / target_category
            
            if skill_dir.exists() and target_dir.exists():
                try:
                    # 移动到目标分类
                    shutil.move(str(skill_dir), str(target_dir / skill_name))
                    self.stats['classified'] += 1
                    logger.info(f"  ✅ 分类：{skill_name} → {target_category}")
                except Exception as e:
                    logger.warning(f"  ⚠️ 分类失败：{skill_name} - {e}")
        
        logger.info(f"  分类有用 Skill: {self.stats['classified']} 个")
    
    def generate_report(self):
        """生成报告"""
        logger.info("📝 生成清理报告...")
        
        report_path = self.workspace / 'SKILLHUB_CLEANUP_AND_CLASSIFY_REPORT.md'
        
        content = f"""# 🗑️ 太一 Skill 清理和智能分类报告

> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **执行人**: SkillHub 清理和分类 Agent  
> **状态**: ✅ 完成

---

## 📊 执行统计

**删除空 Skill**: {self.stats['deleted_empty']} 个  
**删除待删除 Skill**: {self.stats['deleted_useless']} 个  
**分类有用 Skill**: {self.stats['classified']} 个  
**总计处理**: {self.stats['deleted_empty'] + self.stats['deleted_useless'] + self.stats['classified']} 个

---

## ✅ 删除空 Skill ({self.stats['deleted_empty']} 个)

"""
        for skill_name in self.empty_skills:
            content += f"- {skill_name}\n"
        
        content += f"""
## ✅ 删除待删除 Skill ({self.stats['deleted_useless']} 个)

- emerged-skill-20260413-* (无用的自动生成 Skill)

---

## ✅ 分类有用 Skill ({self.stats['classified']} 个)

"""
        for skill_name, target_category in self.useful_skills.items():
            content += f"- {skill_name} → {target_category}\n"
        
        content += f"""
---

**🗑️ 太一 Skill 清理和智能分类报告完成**

**太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        report_path.write_text(content, encoding='utf-8')
        logger.info(f"✅ 清理报告已生成：{report_path}")


def main():
    logger.info("🗑️ SkillHub 清理和智能分类 Agent 启动...")
    agent = SkillhubCleanupAndClassify()
    agent.run()


if __name__ == '__main__':
    main()
