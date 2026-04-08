#!/usr/bin/env python3
"""
Update Skill Registry - 技能注册表更新工具

自动扫描 skills/ 目录，更新 smart-router/registry.yaml

用法:
    python scripts/update-skill-registry.py [--dry-run] [--force]
"""

import os
import sys
import yaml
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


# 技能分类映射（根据目录名或 SKILL.md 内容推断）
CATEGORY_KEYWORDS = {
    'core': ['router', 'orchestrator', 'scheduler'],
    'automation': ['auto', 'cron', 'retry', 'exec'],
    'content': ['content', 'shanmu', 'reporter', 'creator', 'writer'],
    'development': ['code', 'dev', 'artistic', 'suwen'],
    'finance': ['finance', 'trading', 'zhiji', 'tianji', 'gmgn', 'binance', 'quant'],
    'knowledge': ['knowledge', 'wiki', 'search', 'wangliang', 'yi'],
    'system': ['system', 'health', 'docker', 'k8s', 'taiyi'],
    'data': ['data', 'ocr', 'video', 'processor', 'paddle'],
    'communication': ['feishu', 'slack', 'wechat', 'message', 'notify'],
    'design': ['design', 'visual', 'card', 'qiaomu'],
    'utility': ['weather', 'price', 'news', 'image', 'tts', 'tool']
}

# 成本等级推断规则
COST_TIER_RULES = {
    'high': ['finance', 'trading', 'quant', 'gmgn', 'zhiji', 'tianji', 'video', 'data'],
    'medium': ['content', 'development', 'design', 'automation', 'data'],
    'low': ['core', 'knowledge', 'system', 'communication', 'utility']
}

# 延迟等级推断规则
LATENCY_TIER_RULES = {
    'fast': ['core', 'knowledge', 'communication', 'utility', 'automation'],
    'normal': ['content', 'development', 'design', 'system'],
    'slow': ['data', 'video', 'finance']
}


def parse_args():
    parser = argparse.ArgumentParser(description='更新技能注册表')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不写入文件')
    parser.add_argument('--force', action='store_true', help='强制更新所有技能')
    parser.add_argument('--workspace', default='/home/nicola/.openclaw/workspace', 
                       help='工作区根目录')
    return parser.parse_args()


def load_existing_registry(registry_path: Path) -> Dict[str, Any]:
    """加载现有注册表"""
    if not registry_path.exists():
        return {
            'version': '1.0.0',
            'updated': datetime.now().isoformat(),
            'skills': {}
        }
    
    with open(registry_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def scan_skills(skills_dir: Path) -> List[Path]:
    """扫描技能目录"""
    skill_dirs = []
    
    for item in skills_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            skill_md = item / 'SKILL.md'
            if skill_md.exists():
                skill_dirs.append(item)
    
    return sorted(skill_dirs)


def infer_category(skill_name: str, skill_md_path: Path) -> str:
    """推断技能分类"""
    # 读取 SKILL.md 获取元数据
    category = None
    
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # 只读前 2000 字符
            
            # 尝试从 YAML frontmatter 获取 category
            if content.startswith('---'):
                lines = content.split('\n')
                in_frontmatter = False
                for line in lines:
                    if line.strip() == '---':
                        in_frontmatter = not in_frontmatter
                        continue
                    if in_frontmatter and line.startswith('category:'):
                        category = line.split(':', 1)[1].strip()
                        break
            
            # 尝试从内容推断
            if not category:
                content_lower = content.lower()
                for cat, keywords in CATEGORY_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword in content_lower or keyword in skill_name.lower():
                            category = cat
                            break
                    if category:
                        break
    except Exception as e:
        print(f"  ⚠️  读取 {skill_name} 失败：{e}")
    
    return category or 'other'


def infer_cost_tier(category: str, skill_name: str) -> str:
    """推断成本等级"""
    name_lower = skill_name.lower()
    
    # 高成本
    for keyword in COST_TIER_RULES['high']:
        if keyword in name_lower or keyword in category:
            return 'high'
    
    # 中等成本
    for keyword in COST_TIER_RULES['medium']:
        if keyword in name_lower or keyword in category:
            return 'medium'
    
    # 低成本
    return 'low'


def infer_latency_tier(category: str, skill_name: str) -> str:
    """推断延迟等级"""
    name_lower = skill_name.lower()
    
    # 快速
    for keyword in LATENCY_TIER_RULES['fast']:
        if keyword in name_lower or keyword in category:
            return 'fast'
    
    # 慢速
    for keyword in LATENCY_TIER_RULES['slow']:
        if keyword in name_lower or keyword in category:
            return 'slow'
    
    # 正常
    return 'normal'


def extract_capabilities(skill_md_path: Path) -> List[str]:
    """从 SKILL.md 提取能力列表"""
    capabilities = []
    
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 尝试从 API 部分提取
            if '### `' in content:
                lines = content.split('\n')
                for line in lines:
                    if '### `' in line:
                        # 提取 API 名称
                        api_name = line.split('`')[1] if '`' in line else None
                        if api_name:
                            # 转换为能力描述
                            capability = api_name.replace('_', ' ').strip()
                            if capability:
                                capabilities.append(capability)
    except Exception as e:
        pass
    
    return capabilities if capabilities else ['general']


def update_skill_registry(workspace_root: str, dry_run: bool = False, force: bool = False):
    """更新技能注册表"""
    workspace = Path(workspace_root)
    skills_dir = workspace / 'skills'
    registry_path = skills_dir / 'smart-router' / 'registry.yaml'
    
    print(f"📂 工作区：{workspace}")
    print(f"📁 技能目录：{skills_dir}")
    print(f"📄 注册表：{registry_path}")
    print()
    
    # 加载现有注册表
    registry = load_existing_registry(registry_path)
    existing_skills = set(registry.get('skills', {}).keys())
    print(f"📊 现有技能：{len(existing_skills)}")
    
    # 扫描技能
    skill_dirs = scan_skills(skills_dir)
    print(f"🔍 发现技能目录：{len(skill_dirs)}")
    print()
    
    # 更新技能
    updated_count = 0
    new_count = 0
    removed_skills = set(existing_skills)
    
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        skill_md = skill_dir / 'SKILL.md'
        
        # 跳过 smart-router 自身
        if skill_name == 'smart-router':
            continue
        
        print(f"📝 处理：{skill_name}")
        
        # 推断元数据
        category = infer_category(skill_name, skill_md)
        cost_tier = infer_cost_tier(category, skill_name)
        latency_tier = infer_latency_tier(category, skill_name)
        capabilities = extract_capabilities(skill_md)
        
        # 构建技能元数据
        skill_metadata = {
            'category': category,
            'cost_tier': cost_tier,
            'latency_tier': latency_tier,
            'capabilities': capabilities,
            'enabled': True
        }
        
        # 检查是否需要更新
        if skill_name in registry['skills']:
            existing = registry['skills'][skill_name]
            if force or existing != skill_metadata:
                print(f"  ✏️  更新技能")
                registry['skills'][skill_name] = skill_metadata
                updated_count += 1
            else:
                print(f"  ✓ 无需更新")
        else:
            print(f"  ➕ 新增技能")
            registry['skills'][skill_name] = skill_metadata
            new_count += 1
        
        # 从待删除列表中移除
        removed_skills.discard(skill_name)
        print()
    
    # 标记已删除的技能
    for skill_name in removed_skills:
        print(f"  ⚠️  技能已删除：{skill_name}")
        registry['skills'][skill_name]['enabled'] = False
    
    # 更新元数据
    registry['version'] = '1.0.0'
    registry['updated'] = datetime.now().isoformat()
    
    # 输出结果
    print("=" * 60)
    print(f"📊 更新摘要:")
    print(f"  - 新增技能：{new_count}")
    print(f"  - 更新技能：{updated_count}")
    print(f"  - 禁用技能：{len(removed_skills)}")
    print(f"  - 总技能数：{len(registry['skills'])}")
    print()
    
    # 写入文件
    if dry_run:
        print("🔍 预览模式：未写入文件")
        print()
        print("📄 将写入的内容:")
        print(yaml.dump(registry, allow_unicode=True, default_flow_style=False))
    else:
        # 确保目录存在
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(registry_path, 'w', encoding='utf-8') as f:
            f.write("# Smart Router - 技能注册表\n")
            f.write(f"# 版本：{registry['version']}\n")
            f.write(f"# 更新：{registry['updated']}\n\n")
            yaml.dump(registry, f, allow_unicode=True, default_flow_style=False)
        
        print(f"✅ 注册表已更新：{registry_path}")
    
    return registry


def main():
    args = parse_args()
    
    try:
        update_skill_registry(
            workspace_root=args.workspace,
            dry_run=args.dry_run,
            force=args.force
        )
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
