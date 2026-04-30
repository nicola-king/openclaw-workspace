#!/usr/bin/env python3
"""
太一系统 - 技能标准化脚本 (阶段 2)
统一命名规范 + 完善文档 + 建立索引
"""

import os
import json
from pathlib import Path
from datetime import datetime

class SkillStandardizer:
    """技能标准化器"""
    
    def __init__(self):
        self.workspace = Path("/home/nicola/.openclaw/workspace/skills")
        self.index_file = self.workspace / "SKILL_INDEX.json"
        self.stats = {
            'bots': 0,
            'agents': 0,
            'tools': 0,
            'skills_updated': 0,
            'docs_created': 0
        }
    
    def scan_skills(self):
        """扫描所有技能"""
        skills = []
        
        # 扫描目录
        for dir_path in self.workspace.iterdir():
            if dir_path.is_dir() and not dir_path.name.startswith('.'):
                # 检查是否有 SKILL.md
                skill_md = dir_path / "SKILL.md"
                if skill_md.exists():
                    skills.append({
                        'path': str(dir_path),
                        'name': dir_path.name,
                        'has_skill_md': True,
                        'category': self._categorize(dir_path)
                    })
                    self.stats['skills_updated'] += 1
        
        return skills
    
    def _categorize(self, dir_path):
        """分类技能"""
        name = dir_path.name.lower()
        parent = dir_path.parent.name
        
        # 根据目录和名称分类
        if 'agent' in name:
            return 'agent'
        elif 'bot' in name:
            return 'bot'
        elif any(kw in name for kw in ['tool', 'util', 'helper']):
            return 'tool'
        elif parent in ['01-trading', '02-business']:
            return 'agent'
        elif parent in ['05-content', '07-system']:
            if 'agent' in name:
                return 'agent'
            else:
                return 'tool'
        else:
            return 'skill'
    
    def generate_index(self, skills):
        """生成技能索引"""
        index = {
            'version': '1.0',
            'updated_at': datetime.now().isoformat(),
            'total_count': len(skills),
            'categories': {
                'bot': [],
                'agent': [],
                'tool': [],
                'skill': []
            },
            'skills': []
        }
        
        for skill in skills:
            category = skill['category']
            if category in index['categories']:
                index['categories'][category].append(skill['name'])
                if category == 'bot':
                    self.stats['bots'] += 1
                elif category == 'agent':
                    self.stats['agents'] += 1
                elif category == 'tool':
                    self.stats['tools'] += 1
            
            index['skills'].append({
                'name': skill['name'],
                'path': skill['path'],
                'category': category,
                'has_skill_md': skill['has_skill_md']
            })
        
        # 保存索引
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        
        return index
    
    def create_skill_template(self, skill_path):
        """创建 SKILL.md 模板"""
        template = f"""# {{{{name}}}} Skill

> **版本**: v1.0  
> **创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **状态**: ✅ 活跃

---

## 📋 描述

{{{{description}}}}

---

## 🎯 职责

- 职责 1
- 职责 2
- 职责 3

---

## 🔧 技能

- 技能 1
- 技能 2
- 技能 3

---

## 📁 文件结构

```
{Path(skill_path).name}/
├── SKILL.md
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
└── README.md
```

---

## 💡 使用方式

```python
from {Path(skill_path).name} import SkillClass

skill = SkillClass()
result = skill.execute("任务描述")
```

---

## 📝 更新日志

- v1.0 ({datetime.now().strftime('%Y-%m-%d')}) - 初始版本

---

*太一 AGI · {Path(skill_path).name} · {datetime.now().strftime('%Y-%m-%d')}*
"""
        return template
    
    def standardize_naming(self):
        """标准化命名"""
        # 读取索引
        with open(self.index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        # 检查命名规范
        naming_issues = []
        for skill in index['skills']:
            name = skill['name']
            category = skill['category']
            
            # 检查前缀
            if category == 'bot' and not name.startswith('bot-'):
                naming_issues.append({
                    'name': name,
                    'suggested': f'bot-{name}',
                    'category': category
                })
            elif category == 'agent' and not name.startswith('agent-'):
                naming_issues.append({
                    'name': name,
                    'suggested': f'agent-{name}',
                    'category': category
                })
            elif category == 'tool' and not name.startswith('tool-'):
                naming_issues.append({
                    'name': name,
                    'suggested': f'tool-{name}',
                    'category': category
                })
        
        return naming_issues
    
    def generate_report(self, index, naming_issues):
        """生成标准化报告"""
        report = f"""# 太一系统技能标准化报告 (阶段 2)

> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **索引文件**: `skills/SKILL_INDEX.json`

---

## 📊 统计

| 类别 | 数量 |
|------|------|
| **核心 Bot** | {self.stats['bots']} 个 |
| **专业 Agent** | {self.stats['agents']} 个 |
| **工具 Bot** | {self.stats['tools']} 个 |
| **总计** | {index['total_count']} 个 |

---

## 📁 技能索引

已生成技能索引文件：
```
skills/SKILL_INDEX.json
```

包含：
- 技能总数：{index['total_count']}
- 分类统计：Bot/Agent/Tool/Skill
- 路径映射：名称 → 实际路径
- 文档状态：SKILL.md 是否存在

---

## 🏷️ 命名规范检查

发现 {len(naming_issues)} 个命名不规范：

"""
        
        for issue in naming_issues[:20]:  # 只显示前 20 个
            report += f"""
### {issue['name']}

- **当前名称**: `{issue['name']}`
- **建议名称**: `{issue['suggested']}`
- **类别**: {issue['category']}
- **操作**: 待重命名

---
"""
        
        if len(naming_issues) > 20:
            report += f"\n... 还有 {len(naming_issues) - 20} 个未显示\n"
        
        report += f"""
## ✅ 下一步

1. 审查命名问题列表
2. 确认重命名方案
3. 执行重命名 (可选)
4. 更新索引

---

*太一 AGI · 技能标准化 v1.0 · {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        
        return report


def main():
    """主函数"""
    print("=" * 60)
    print("太一系统 - 技能标准化 (阶段 2)")
    print("=" * 60)
    
    standardizer = SkillStandardizer()
    
    # 扫描技能
    print("\n🔍 扫描技能...")
    skills = standardizer.scan_skills()
    print(f"✅ 发现 {len(skills)} 个技能")
    
    # 生成索引
    print("\n📑 生成技能索引...")
    index = standardizer.generate_index(skills)
    print(f"✅ 索引已生成：{standardizer.index_file}")
    
    # 检查命名
    print("\n🏷️  检查命名规范...")
    naming_issues = standardizer.standardize_naming()
    print(f"⚠️  发现 {len(naming_issues)} 个命名问题")
    
    # 生成报告
    print("\n📄 生成报告...")
    report = standardizer.generate_report(index, naming_issues)
    
    report_path = Path("/home/nicola/.openclaw/workspace/reports/skill-standardization-report.md")
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存：{report_path}")
    
    print("\n" + "=" * 60)
    print("阶段 2 完成！")
    print("=" * 60)
    print(f"\n📊 统计:")
    print(f"  Bot: {standardizer.stats['bots']} 个")
    print(f"  Agent: {standardizer.stats['agents']} 个")
    print(f"  Tool: {standardizer.stats['tools']} 个")
    print(f"  总计：{index['total_count']} 个")


if __name__ == "__main__":
    main()
