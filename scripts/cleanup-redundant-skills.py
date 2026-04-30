#!/usr/bin/env python3
"""
太一系统 Skill 清理脚本
清理冗余 auto-skill-* 和 emerged-skill-*
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class SkillCleaner:
    """Skill 清理器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace/skills")
        self.backup_dir = self.workspace / ".cleanup-backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'auto_skills': 0,
            'emerged_skills': 0,
            'backup_count': 0,
            'deleted_count': 0,
            'kept_count': 0
        }
    
    def scan_auto_skills(self):
        """扫描 auto-skill-* 目录"""
        auto_skills = []
        for pattern in ['03-automation', 'emerged-skill-*', 'auto-skill-*']:
            matches = list(self.workspace.glob(f"**/{pattern}"))
            for match in matches:
                if match.is_dir() and match.name.startswith('auto-skill-'):
                    auto_skills.append(match)
        
        self.stats['auto_skills'] = len(auto_skills)
        return auto_skills
    
    def scan_emerged_skills(self):
        """扫描 emerged-skill-* 目录"""
        emerged_skills = []
        for match in self.workspace.glob("**/emerged-skill-*"):
            if match.is_dir():
                emerged_skills.append(match)
        
        self.stats['emerged_skills'] = len(emerged_skills)
        return emerged_skills
    
    def analyze_skill(self, skill_path):
        """分析技能内容"""
        result = {
            'path': skill_path,
            'name': skill_path.name,
            'has_skill_md': (skill_path / "SKILL.md").exists(),
            'has_config': (skill_path / "config").exists(),
            'has_src': (skill_path / "src").exists(),
            'has_tests': (skill_path / "tests").exists(),
            'file_count': len(list(skill_path.glob("**/*"))),
            'size_bytes': sum(f.stat().st_size for f in skill_path.glob("**/*") if f.is_file())
        }
        
        # 读取 SKILL.md 分析功能
        skill_md = skill_path / "SKILL.md"
        if skill_md.exists():
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()[:1000]
                result['description'] = content[:200]
        
        return result
    
    def identify_duplicates(self, skills):
        """识别重复技能"""
        # 按功能分组
        function_groups = {}
        
        for skill in skills:
            analysis = self.analyze_skill(skill)
            
            # 提取功能关键词
            keywords = self._extract_keywords(analysis)
            key = tuple(sorted(keywords))
            
            if key not in function_groups:
                function_groups[key] = []
            function_groups[key].append({
                'skill': skill,
                'analysis': analysis
            })
        
        # 找出重复组
        duplicates = {k: v for k, v in function_groups.items() if len(v) > 1}
        
        return duplicates
    
    def _extract_keywords(self, analysis):
        """提取功能关键词"""
        keywords = []
        
        if analysis['has_skill_md']:
            desc = analysis.get('description', '').lower()
            if 'web' in desc or 'search' in desc:
                keywords.append('web_search')
            if 'pdf' in desc:
                keywords.append('pdf')
            if 'image' in desc:
                keywords.append('image')
            if 'video' in desc:
                keywords.append('video')
            if 'audio' in desc or 'tts' in desc:
                keywords.append('audio')
            if 'file' in desc:
                keywords.append('file_operation')
        
        return keywords if keywords else ['unknown']
    
    def cleanup_auto_skills(self, auto_skills):
        """清理 auto-skill-*"""
        print(f"\n 开始清理 auto-skill-* ({len(auto_skills)} 个)")
        
        # 识别重复
        duplicates = self.identify_duplicates(auto_skills)
        
        print(f"📊 发现 {len(duplicates)} 组重复功能")
        
        # 处理重复组
        for keywords, group in duplicates.items():
            print(f"\n  功能组：{keywords}")
            
            # 保留最完整的一个
            best = max(group, key=lambda x: x['analysis']['file_count'])
            
            for item in group:
                skill = item['skill']
                if skill == best['skill']:
                    print(f"    ✅ 保留：{skill.name}")
                    self.stats['kept_count'] += 1
                else:
                    # 备份后删除
                    backup_path = self.backup_dir / skill.name
                    shutil.copytree(skill, backup_path)
                    self.stats['backup_count'] += 1
                    
                    # 删除原目录
                    shutil.rmtree(skill)
                    self.stats['deleted_count'] += 1
                    print(f"    🗑️ 删除 (已备份): {skill.name}")
        
        # 处理独立技能 (无重复)
        processed = set()
        for group in duplicates.values():
            for item in group:
                processed.add(item['skill'])
        
        for skill in auto_skills:
            if skill not in processed:
                analysis = self.analyze_skill(skill)
                if analysis['file_count'] < 5 and not analysis['has_skill_md']:
                    # 空技能或微型技能，删除
                    backup_path = self.backup_dir / skill.name
                    shutil.copytree(skill, backup_path)
                    self.stats['backup_count'] += 1
                    shutil.rmtree(skill)
                    self.stats['deleted_count'] += 1
                    print(f"    🗑️ 删除 (空技能): {skill.name}")
                else:
                    print(f"    ✅ 保留：{skill.name}")
                    self.stats['kept_count'] += 1
    
    def cleanup_emerged_skills(self, emerged_skills):
        """清理 emerged-skill-*"""
        print(f"\n🔍 开始清理 emerged-skill-* ({len(emerged_skills)} 个)")
        
        # 检查是否有 SKILL.md 和实际内容
        for skill in emerged_skills:
            analysis = self.analyze_skill(skill)
            
            if analysis['has_skill_md'] and analysis['file_count'] > 5:
                print(f"    ✅ 保留：{skill.name}")
                self.stats['kept_count'] += 1
            else:
                # 备份后删除
                backup_path = self.backup_dir / skill.name
                shutil.copytree(skill, backup_path)
                self.stats['backup_count'] += 1
                shutil.rmtree(skill)
                self.stats['deleted_count'] += 1
                print(f"    🗑️ 删除 (已备份): {skill.name}")
    
    def generate_report(self):
        """生成清理报告"""
        report = f"""# Skill 清理报告

> **清理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **备份目录**: {self.backup_dir}

## 📊 统计

| 类别 | 数量 |
|------|------|
| auto-skill-* 初始数量 | {self.stats['auto_skills']} |
| emerged-skill-* 初始数量 | {self.stats['emerged_skills']} |
| 备份数量 | {self.stats['backup_count']} |
| 删除数量 | {self.stats['deleted_count']} |
| 保留数量 | {self.stats['kept_count']} |

## 📁 备份位置

```
{self.backup_dir}
```

## ✅ 下一步

1. 检查备份目录确认无误
2. 手动删除备份 (确认清理成功后)
3. 更新技能索引
4. 测试核心功能
"""
        
        report_path = self.backup_dir / "cleanup_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report


def main():
    """主函数"""
    print("=" * 60)
    print("太一系统 Skill 清理脚本")
    print("=" * 60)
    
    cleaner = SkillCleaner()
    
    # 扫描
    auto_skills = cleaner.scan_auto_skills()
    emerged_skills = cleaner.scan_emerged_skills()
    
    print(f"\n📊 扫描结果:")
    print(f"  auto-skill-*: {len(auto_skills)} 个")
    print(f"  emerged-skill-*: {len(emerged_skills)} 个")
    
    # 清理
    if auto_skills:
        cleaner.cleanup_auto_skills(auto_skills)
    
    if emerged_skills:
        cleaner.cleanup_emerged_skills(emerged_skills)
    
    # 生成报告
    report = cleaner.generate_report()
    
    print("\n" + "=" * 60)
    print("清理完成！")
    print("=" * 60)
    print(f"\n📊 最终统计:")
    print(f"  备份：{cleaner.stats['backup_count']} 个")
    print(f"  删除：{cleaner.stats['deleted_count']} 个")
    print(f"  保留：{cleaner.stats['kept_count']} 个")
    print(f"\n📁 备份目录：{cleaner.backup_dir}")
    print(f"\n📄 报告：{cleaner.backup_dir}/cleanup_report.md")


if __name__ == "__main__":
    main()
