#!/usr/bin/env python3
"""
批量为技能添加 YAML Frontmatter
"""

import os
from pathlib import Path

SKILLS_DIR = Path('/home/nicola/.openclaw/workspace/skills')

# 技能元数据模板
SKILL_TEMPLATES = {
    'browser-automation': {
        'category': 'browser',
        'tags': ['playwright', 'browser', 'automation', 'screenshot', 'crawl'],
        'description': '智能浏览器自动化 - Playwright 网页导航/交互/截图/数据采集'
    },
    'gmgn-swap': {
        'category': 'trading',
        'tags': ['gmgn', 'swap', 'solana', 'base', 'trading'],
        'description': 'GMGN 去中心化交易 - Solana/Base 链上代币 swaps'
    },
    'gmgn-token': {
        'category': 'trading',
        'tags': ['gmgn', 'token', 'analysis', 'solana', 'base'],
        'description': 'GMGN 代币分析 - 安全/池子/持有人/交易员数据'
    },
    'gmgn-portfolio': {
        'category': 'trading',
        'tags': ['gmgn', 'portfolio', 'wallet', 'tracking'],
        'description': 'GMGN 钱包组合追踪 - 持仓/交易/统计数据'
    },
    'gmgn-market': {
        'category': 'trading',
        'tags': ['gmgn', 'market', 'kline', 'trending'],
        'description': 'GMGN 市场数据 - K 线/趋势/热门代币'
    },
    'gmgn-track': {
        'category': 'trading',
        'tags': ['gmgn', 'tracking', 'smart-money', 'kol'],
        'description': 'GMGN 链上追踪 - 聪明钱/KOL/大户交易'
    },
    'gmgn-cooking': {
        'category': 'trading',
        'tags': ['gmgn', 'cooking', 'new-token', 'discovery'],
        'description': 'GMGN 新币发现 - Trenches/新币挖掘'
    },
    'tianji': {
        'category': 'trading',
        'tags': ['sentiment', 'analysis', 'smart-money'],
        'description': '天几 - 聪明钱追踪与市场情绪分析'
    },
    'zhiji-sentiment': {
        'category': 'trading',
        'tags': ['sentiment', 'finbert', 'analysis'],
        'description': '知几情绪分析 - FinBERT 金融情绪因子'
    },
    'paoding': {
        'category': 'finance',
        'tags': ['budget', 'cost', 'analysis'],
        'description': '庖丁 - 预算成本分析与财务追踪'
    },
    'ssh': {
        'category': 'tools',
        'tags': ['ssh', 'remote', 'shell'],
        'description': 'SSH 远程控制 - 本机/他机 SSH 连接'
    },
    'feishu': {
        'category': 'data',
        'tags': ['feishu', 'lark', 'doc', 'wiki', 'bitable'],
        'description': '飞书集成 - 消息/文档/多维表格/知识库'
    },
    'weather': {
        'category': 'data',
        'tags': ['weather', 'forecast', 'wttr', 'open-meteo'],
        'description': '天气预报 - 实时天气/ forecasts (wttr.in/Open-Meteo)'
    },
    'wangliang': {
        'category': 'data',
        'tags': ['wangliang', 'knowledge', 'search'],
        'description': '王良 - 知识库搜索与问答'
    },
    'suwen': {
        'category': 'tech',
        'tags': ['suwen', 'development', 'coding'],
        'description': '素问 - 技术开发与代码生成'
    },
    'shanmu-reporter': {
        'category': 'content',
        'tags': ['shanmu', 'report', 'finance', 'research'],
        'description': '山木研报生成器 - 专业金融研报生成'
    },
    'shanmu': {
        'category': 'content',
        'tags': ['shanmu', 'content', 'creative'],
        'description': '山木 - 内容创意与文案生成'
    },
    'taiyi': {
        'category': 'infrastructure',
        'tags': ['taiyi', 'agi', 'orchestrator'],
        'description': '太一 - AGI 执行总管与多 Bot 协调'
    },
    'zhiji': {
        'category': 'trading',
        'tags': ['zhiji', 'quant', 'strategy', 'polymarket'],
        'description': '知几 - 量化交易策略引擎'
    },
    'polymarket': {
        'category': 'trading',
        'tags': ['polymarket', 'prediction', 'betting', 'crypto'],
        'description': 'Polymarket 预测市场交易 - 气象/政治/体育套利'
    },
}


def add_frontmatter(skill_dir: Path):
    """为技能添加 YAML Frontmatter"""
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return False
    
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有 Frontmatter
    if content.startswith('---'):
        return False  # 已有，跳过
    
    skill_name = skill_dir.name
    template = SKILL_TEMPLATES.get(skill_name)
    
    if not template:
        # 使用默认模板
        template = {
            'category': 'general',
            'tags': [],
            'description': f'{skill_name} skill'
        }
    
    # 生成 Frontmatter
    frontmatter = f"""---
name: {skill_name}
version: 1.0.0
description: "{template['description']}"
category: {template['category']}
tags: {template['tags']}
author: 太一 AGI
created: 2026-04-07
---

"""
    
    # 写回文件
    with open(skill_md, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    
    print(f'  ✅ {skill_name}: {template["category"]}')
    return True


def main():
    print('🔧 批量添加技能 YAML Frontmatter...')
    print()
    
    updated = 0
    skipped = 0
    
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('_') or skill_dir.name == 'shared':
            continue
        
        try:
            if add_frontmatter(skill_dir):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f'  ❌ {skill_dir.name}: {e}')
    
    print()
    print(f'📊 统计:')
    print(f'  ✅ 添加：{updated}')
    print(f'  ⚠️  跳过 (已有): {skipped}')


if __name__ == '__main__':
    main()
