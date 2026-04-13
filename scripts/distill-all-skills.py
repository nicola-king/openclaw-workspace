#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
穿透式蒸馏所有 Skill
分析内容，识别重复冗余，优化重组融合
"""

import os
import json
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('DistillAllSkills')


class SkillDistiller:
    """Skill 蒸馏器"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.skills_dir = self.workspace / 'skills'
        
        self.skills_data = []
        self.duplicates = []
        self.to_merge = []
        self.to_delete = []
        
    def run(self):
        """运行蒸馏"""
        logger.info("🔍 开始穿透式蒸馏所有 Skill...")
        
        # Step 1: 收集所有 Skill
        self.collect_all_skills()
        
        # Step 2: 分析内容
        self.analyze_content()
        
        # Step 3: 识别重复
        self.identify_duplicates()
        
        # Step 4: 识别冗余
        self.identify_redundancy()
        
        # Step 5: 生成报告
        self.generate_report()
        
        logger.info("✅ 穿透式蒸馏完成！")
    
    def collect_all_skills(self):
        """收集所有 Skill"""
        logger.info("📂 收集所有 Skill...")
        
        for skill_md in self.skills_dir.rglob('SKILL.md'):
            try:
                with open(skill_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 解析基本信息
                    skill_info = {
                        'path': skill_md.parent,
                        'name': skill_md.parent.name,
                        'content': content,
                        'has_py': len(list(skill_md.parent.glob('*.py'))) > 0,
                        'py_count': len(list(skill_md.parent.glob('*.py'))),
                        'file_count': len(list(skill_md.parent.rglob('*'))),
                    }
                    
                    self.skills_data.append(skill_info)
            except Exception as e:
                logger.warning(f"  ⚠️ 读取失败：{skill_md} - {e}")
        
        logger.info(f"  收集到 Skill: {len(self.skills_data)} 个")
    
    def analyze_content(self):
        """分析内容"""
        logger.info("🔍 分析 Skill 内容...")
        
        for skill in self.skills_data:
            # 分析文件大小
            skill['size'] = len(skill['content'])
            
            # 分析是否有实际功能
            skill['has_function'] = skill['has_py'] and skill['py_count'] > 0
            
            # 分析是否空壳
            skill['is_empty'] = skill['file_count'] <= 2 and not skill['has_function']
        
        logger.info(f"  分析完成")
    
    def identify_duplicates(self):
        """识别重复 Skill"""
        logger.info("🔄 识别重复 Skill...")
        
        # 按名称分组
        name_groups = {}
        for skill in self.skills_data:
            name = skill['name']
            if name not in name_groups:
                name_groups[name] = []
            name_groups[name].append(skill)
        
        # 找出重复
        for name, skills in name_groups.items():
            if len(skills) > 1:
                self.duplicates.append({
                    'name': name,
                    'count': len(skills),
                    'paths': [s['path'] for s in skills],
                })
                logger.warning(f"  ⚠️ 重复：{name} ({len(skills)} 个)")
        
        logger.info(f"  发现重复：{len(self.duplicates)} 组")
    
    def identify_redundancy(self):
        """识别冗余 Skill"""
        logger.info("🗑️ 识别冗余 Skill...")
        
        # 识别空壳 Skill
        empty_skills = [s for s in self.skills_data if s.get('is_empty', False)]
        
        for skill in empty_skills:
            self.to_delete.append({
                'name': skill['name'],
                'path': skill['path'],
                'reason': '空壳 Skill (无实际内容)',
            })
        
        # 识别 emerged-skill (可以合并)
        emerged_skills = [s for s in self.skills_data if s['name'].startswith('emerged-skill-')]
        
        if len(emerged_skills) > 50:
            logger.info(f"  ℹ️  emerged-skill: {len(emerged_skills)} 个 (建议定期清理)")
        
        logger.info(f"  待删除：{len(self.to_delete)} 个")
    
    def generate_report(self):
        """生成报告"""
        logger.info("📝 生成蒸馏报告...")
        
        report_path = self.workspace / 'SKILL_DISTILLATION_REPORT.md'
        
        content = f"""# 🔍 Skill 穿透式蒸馏报告

> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **执行人**: 太一 AGI  
> **状态**: ✅ 完成

---

## 📊 总体统计

**总 Skill 数**: {len(self.skills_data)} 个  
**重复 Skill**: {len(self.duplicates)} 组  
**待删除**: {len(self.to_delete)} 个

---

## 🔄 重复 Skill ({len(self.duplicates)} 组)

"""
        for dup in self.duplicates[:20]:
            content += f"### {dup['name']} ({dup['count']} 个)\n\n"
            for path in dup['paths'][:5]:
                content += f"- {path}\n"
            content += "\n"
        
        content += f"""
## 🗑️ 待删除 Skill ({len(self.to_delete)} 个)

"""
        for skill in self.to_delete[:20]:
            content += f"- {skill['name']} - {skill['reason']}\n"
        
        content += f"""
---

**🔍 Skill 穿透式蒸馏报告完成**

**太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ 报告已生成：{report_path}")


def main():
    logger.info("🔍 Skill 蒸馏器启动...")
    distiller = SkillDistiller()
    distiller.run()


if __name__ == '__main__':
    main()
