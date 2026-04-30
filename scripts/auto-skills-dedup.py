#!/usr/bin/env python3
"""
Auto-Skills 去重清理工具 v1.0
太一 AGI · 2026-04-14
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class AutoSkillDeduplicator:
    """自动化技能去重工具"""
    
    def __init__(self, automation_dir: str):
        self.automation_dir = Path(automation_dir)
        self.auto_skills_dir = self.automation_dir
        self.analyzed_count = 0
        self.duplicate_groups = []
        self.to_remove = []
        self.to_keep = []
        
    def analyze_skills(self):
        """分析所有 auto-skills"""
        print("🔍 分析 auto-skills...")
        
        skills_by_pattern = defaultdict(list)
        
        for skill_dir in self.auto_skills_dir.iterdir():
            if skill_dir.is_dir() and skill_dir.name.startswith("auto-skill-"):
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text(encoding="utf-8")
                    # 提取技能类型/功能
                    skill_type = self._extract_skill_type(content)
                    skills_by_pattern[skill_type].append(skill_dir)
                    self.analyzed_count += 1
        
        print(f"   分析完成：{self.analyzed_count} 个技能")
        
        # 识别重复组
        for skill_type, skills in skills_by_pattern.items():
            if len(skills) > 3:  # 超过 3 个相似技能视为可能重复
                self.duplicate_groups.append({
                    "type": skill_type,
                    "skills": skills,
                    "count": len(skills)
                })
        
        print(f"   发现重复组：{len(self.duplicate_groups)} 个")
        
        return skills_by_pattern
    
    def _extract_skill_type(self, content: str) -> str:
        """从 SKILL.md 提取技能类型"""
        # 尝试提取 name
        name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
        if name_match:
            return name_match.group(1).strip()
        
        # 尝试提取 description
        desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
        if desc_match:
            return desc_match.group(1).strip()[:50]
        
        # 尝试提取标题
        title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        return "unknown"
    
    def deduplicate(self, dry_run=True):
        """执行去重"""
        print("\n🧹 执行去重...")
        
        for group in self.duplicate_groups:
            skills = group["skills"]
            
            # 保留最早的 1 个和最新的 1 个
            sorted_skills = sorted(skills, key=lambda x: x.name)
            
            # 保留第一个（最早）
            self.to_keep.append(sorted_skills[0])
            
            # 如果有很多重复，保留最后一个（最新）
            if len(sorted_skills) > 5:
                self.to_keep.append(sorted_skills[-1])
            
            # 其余标记为删除
            for skill in sorted_skills[1:-1 if len(sorted_skills) > 5 else len(sorted_skills)]:
                self.to_remove.append(skill)
        
        print(f"   保留：{len(self.to_keep)} 个")
        print(f"   待删除：{len(self.to_remove)} 个")
        
        if dry_run:
            print("\n⚠️  干运行模式，未实际删除")
        
        return self.to_keep, self.to_remove
    
    def generate_report(self, output_path: str):
        """生成去重报告"""
        report_path = Path(output_path)
        
        content = f"""# 🧹 Auto-Skills 去重清理报告

> **执行时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
> **执行工具**: AutoSkillDeduplicator v1.0  
> **模式**: 分析完成

---

## 📊 分析结果

**分析技能数**: {self.analyzed_count} 个  
**发现重复组**: {len(self.duplicate_groups)} 个  
**建议保留**: {len(self.to_keep)} 个  
**建议删除**: {len(self.to_remove)} 个  

---

## 🎯 重复组详情

"""
        
        for i, group in enumerate(self.duplicate_groups[:10], 1):  # 只显示前 10 组
            content += f"""### 组 {i}: {group['type'][:50]}

- **技能数量**: {group['count']} 个
- **技能列表**:
"""
            for skill in group['skills'][:5]:  # 只显示前 5 个
                content += f"  - `{skill.name}`\n"
            
            if len(group['skills']) > 5:
                content += f"  - ... 还有 {len(group['skills']) - 5} 个\n"
            
            content += "\n"
        
        content += f"""---

## 📋 建议操作

### 保留技能 ({len(self.to_keep)} 个)

"""
        for skill in self.to_keep[:20]:
            content += f"- `{skill.name}`\n"
        
        content += f"""
### 待删除技能 ({len(self.to_remove)} 个)

"""
        for skill in self.to_remove[:20]:
            content += f"- `{skill.name}`\n"
        
        if len(self.to_remove) > 20:
            content += f"- ... 还有 {len(self.to_remove) - 20} 个\n"
        
        content += f"""
---

## ⚠️ 注意事项

1. **备份优先**: 删除前请确保已备份
2. **逐步执行**: 建议分批删除，每次删除后测试
3. **验证功能**: 删除后验证系统功能正常
4. **Git 提交**: 删除后提交 Git 便于回滚

---

*太一 AGI · Auto-Skills 去重清理 · {datetime.now().strftime("%Y-%m-%d")}*
"""
        
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(content, encoding="utf-8")
        print(f"\n📄 报告已保存：{report_path}")
        
        return str(report_path)


if __name__ == "__main__":
    automation_dir = "/home/nicola/.openclaw/workspace/skills/03-automation"
    deduplicator = AutoSkillDeduplicator(automation_dir)
    
    # 分析
    skills_by_pattern = deduplicator.analyze_skills()
    
    # 去重（干运行）
    deduplicator.deduplicate(dry_run=True)
    
    # 生成报告
    report_path = deduplicator.generate_report(
        "/home/nicola/.openclaw/workspace/reports/auto-skills-dedup-analysis.md"
    )
    
    print(f"\n✅ 分析完成！报告：{report_path}")
