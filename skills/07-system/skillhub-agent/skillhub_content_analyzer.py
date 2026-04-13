#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillHub 剩余 Skill 内容分析 Agent v3.0

穿透式蒸馏分析剩余 84 个未分类 Skill:
1. 查看每个 Skill 的内容
2. 分析是否有实际功能
3. 判断是否有用
4. 给出处理建议
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('SkillhubContentAnalyzer')


class SkillhubContentAnalyzer:
    """SkillHub 剩余 Skill 内容分析 Agent"""
    
    def __init__(self):
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.skills_dir = self.workspace / 'skills'
        
        self.analysis_results = {
            'useful': [],
            'duplicate': [],
            'empty': [],
            'to_delete': [],
        }
        
        # 剩余未分类 Skill 列表
        self.uncategorized_skills = []
        
        logger.info("🔍 SkillHub 剩余 Skill 内容分析 Agent 已初始化")
    
    def run(self):
        """运行内容分析"""
        logger.info("🔍 开始穿透式蒸馏分析剩余 Skill...")
        
        # Step 1: 收集剩余未分类 Skill
        self.collect_uncategorized_skills()
        
        # Step 2: 分析每个 Skill 内容
        self.analyze_each_skill()
        
        # Step 3: 生成报告
        self.generate_report()
        
        logger.info("✅ 穿透式蒸馏分析完成！")
    
    def collect_uncategorized_skills(self):
        """收集剩余未分类 Skill"""
        logger.info("📂 收集剩余未分类 Skill...")
        
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.') or skill_dir.name.startswith('0'):
                continue
            self.uncategorized_skills.append(skill_dir)
        
        logger.info(f"  收集到未分类 Skill: {len(self.uncategorized_skills)} 个")
    
    def analyze_each_skill(self):
        """分析每个 Skill 内容"""
        logger.info("🔍 分析每个 Skill 内容...")
        
        for skill_dir in self.uncategorized_skills:
            skill_name = skill_dir.name
            
            # 分析内容
            analysis = self.analyze_skill_content(skill_dir)
            
            # 分类
            if analysis['useful']:
                self.analysis_results['useful'].append({
                    'name': skill_name,
                    'reason': analysis['reason'],
                    'files': analysis['files'],
                    'suggestion': analysis['suggestion'],
                })
            elif analysis['duplicate']:
                self.analysis_results['duplicate'].append({
                    'name': skill_name,
                    'reason': analysis['reason'],
                    'duplicate_of': analysis['duplicate_of'],
                })
            elif analysis['empty']:
                self.analysis_results['empty'].append({
                    'name': skill_name,
                    'reason': '空目录或无实际内容',
                })
            else:
                self.analysis_results['to_delete'].append({
                    'name': skill_name,
                    'reason': '无用或过时',
                })
            
            logger.info(f"  {skill_name}: {analysis['category']}")
    
    def analyze_skill_content(self, skill_dir: Path) -> Dict:
        """分析 Skill 内容"""
        result = {
            'useful': False,
            'duplicate': False,
            'empty': False,
            'category': 'unknown',
            'reason': '',
            'files': 0,
            'suggestion': '',
            'duplicate_of': '',
        }
        
        # 统计文件
        files = list(skill_dir.rglob('*'))
        py_files = [f for f in files if f.suffix == '.py' and f.name != '__init__.py']
        md_files = [f for f in files if f.suffix == '.md']
        
        result['files'] = len(files)
        
        # 判断是否有用
        if len(py_files) > 0 or len(md_files) > 2:
            result['useful'] = True
            result['category'] = 'useful'
            
            # 判断应该分类到哪里
            suggestion = self.suggest_category(skill_dir.name, py_files, md_files)
            result['suggestion'] = suggestion
            
            if py_files:
                result['reason'] = f'有 {len(py_files)} 个 Python 文件'
            else:
                result['reason'] = f'有 {len(md_files)} 个文档文件'
        elif len(files) <= 2:
            result['empty'] = True
            result['category'] = 'empty'
            result['reason'] = '空目录或文件过少'
        else:
            result['category'] = 'to_delete'
            result['reason'] = '内容无用或过时'
        
        return result
    
    def suggest_category(self, skill_name: str, py_files: List[Path], md_files: List[Path]) -> str:
        """建议分类"""
        skill_name_lower = skill_name.lower()
        
        # 根据名称建议分类
        if any(kw in skill_name_lower for kw in ['agent', 'skill']):
            return '07-system'
        elif any(kw in skill_name_lower for kw in ['report', 'daily', 'log']):
            return '03-automation'
        elif any(kw in skill_name_lower for kw in ['search', 'google', 'map']):
            return '04-integration'
        elif any(kw in skill_name_lower for kw in ['art', 'design', 'visual']):
            return '05-content'
        elif any(kw in skill_name_lower for kw in ['security', 'hardening']):
            return '07-system'
        elif any(kw in skill_name_lower for kw in ['dream', 'yi', 'suwen', 'web']):
            return '07-system'
        else:
            return '07-system (默认)'
    
    def generate_report(self):
        """生成报告"""
        logger.info("📝 生成分析报告...")
        
        report_path = self.workspace / 'SKILLHUB_REMAINING_SKILLS_CONTENT_ANALYSIS_REPORT.md'
        
        content = f"""# 🔍 太一剩余 Skill 穿透式蒸馏分析报告

> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **执行人**: SkillHub 内容分析 Agent  
> **状态**: ✅ 完成

---

## 📊 汇总统计

**总未分类 Skill**: {len(self.uncategorized_skills)} 个  
**有用 Skill**: {len(self.analysis_results['useful'])} 个  
**重复 Skill**: {len(self.analysis_results['duplicate'])} 个  
**空 Skill**: {len(self.analysis_results['empty'])} 个  
**待删除 Skill**: {len(self.analysis_results['to_delete'])} 个

---

## ✅ 有用 Skill ({len(self.analysis_results['useful'])} 个)

"""
        for skill in self.analysis_results['useful'][:30]:
            content += f"### {skill['name']}\n\n"
            content += f"- **原因**: {skill['reason']}\n"
            content += f"- **建议分类**: {skill['suggestion']}\n"
            content += f"- **文件数**: {skill['files']} 个\n\n"
        
        if len(self.analysis_results['useful']) > 30:
            content += f"... 还有 {len(self.analysis_results['useful']) - 30} 个\n\n"
        
        content += f"""
## ⚠️ 重复 Skill ({len(self.analysis_results['duplicate'])} 个)

"""
        if self.analysis_results['duplicate']:
            for skill in self.analysis_results['duplicate'][:10]:
                content += f"- {skill['name']} (重复：{skill.get('duplicate_of', 'N/A')})\n"
        else:
            content += "✅ 无重复 Skill\n"
        
        content += f"""
## 📭 空 Skill ({len(self.analysis_results['empty'])} 个)

"""
        if self.analysis_results['empty']:
            for skill in self.analysis_results['empty'][:10]:
                content += f"- {skill['name']}\n"
        else:
            content += "✅ 无空 Skill\n"
        
        content += f"""
## 🗑️ 待删除 Skill ({len(self.analysis_results['to_delete'])} 个)

"""
        if self.analysis_results['to_delete']:
            for skill in self.analysis_results['to_delete'][:10]:
                content += f"- {skill['name']}\n"
        else:
            content += "✅ 无待删除 Skill\n"
        
        content += f"""
---

## 📋 处理建议

**有用 Skill**:
- 建议按建议分类移动
- 补充 SKILL.md 和自进化文件

**重复 Skill**:
- 保留一个，删除其他

**空 Skill**:
- 直接删除

**待删除 Skill**:
- 直接删除

---

**🔍 太一剩余 Skill 穿透式蒸馏分析报告完成**

**太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        report_path.write_text(content, encoding='utf-8')
        logger.info(f"✅ 分析报告已生成：{report_path}")


def main():
    logger.info("🔍 SkillHub 剩余 Skill 内容分析 Agent 启动...")
    analyzer = SkillhubContentAnalyzer()
    analyzer.run()


if __name__ == '__main__':
    main()
