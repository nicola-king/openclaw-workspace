#!/usr/bin/env python3
"""
批量更新技能元数据
添加 category 和 tags 到所有 SKILL.md 文件
"""

import os
from pathlib import Path
import yaml

SKILLS_DIR = Path('/home/nicola/.openclaw/workspace/skills')

# 技能分类映射
SKILL_CATEGORIES = {
    # trading
    'polymarket': 'trading',
    'binance-trader': 'trading',
    'gmgn': 'trading',
    'gmgn-cooking': 'trading',
    'gmgn-market': 'trading',
    'gmgn-portfolio': 'trading',
    'gmgn-swap': 'trading',
    'gmgn-token': 'trading',
    'gmgn-track': 'trading',
    'zhiji': 'trading',
    'zhiji-sentiment': 'trading',
    'torchtrade-integration': 'trading',
    'portfolio-tracker': 'trading',
    'coingecko-price': 'trading',
    'alpha-vantage': 'trading',
    
    # content
    'shanmu': 'content',
    'shanmu-reporter': 'content',
    'content-scheduler': 'content',
    'social-publisher': 'content',
    'social-media-scheduler': 'content',
    'geo-seo-optimizer': 'content',
    'hot-topic-generator': 'content',
    'epub-book-generator': 'content',
    
    # visual
    'qiaomu-info-card-designer': 'visual',
    'ascii-art': 'visual',
    'image-generator': 'visual',
    'unsplash-image': 'visual',
    'ppt-chart-generator': 'visual',
    
    # browser
    'browser-automation': 'browser',
    'browser-adapter': 'browser',
    'geo-automation': 'browser',
    
    # cli
    'aws-cli': 'cli',
    'azure-cli': 'cli',
    'gcp-cli': 'cli',
    'docker-ctl': 'cli',
    'k8s-deploy': 'cli',
    'git-integration': 'cli',
    'gemini-cli': 'cli',
    'jimeng-cli': 'cli',
    'notebooklm-cli': 'cli',
    'taiyi-notebooklm': 'cli',
    
    # monitoring
    'api-monitor': 'monitoring',
    'self-check': 'monitoring',
    'bot-dashboard': 'monitoring',
    'polyalert': 'monitoring',
    'upgrade-guard': 'monitoring',
    
    # data
    'feishu': 'data',
    'news-fetcher': 'data',
    'weather': 'data',
    'wangliang': 'data',
    'the-well-processor': 'data',
    'china-textbook-search': 'data',
    
    # infrastructure
    'smart_router': 'infrastructure',
    'shared': 'infrastructure',
    'task-orchestrator': 'infrastructure',
    'smart-model-router': 'infrastructure',
    'smart-skills-manager': 'infrastructure',
    
    # tools
    'ssh': 'tools',
    'tts': 'tools',
    'webhook-relay': 'tools',
    'wechat': 'tools',
    'web': 'tools',
    
    # other
    'aesthetic-scorer': 'other',
    'artistic-code': 'other',
    'auto-exec': 'other',
    'cost-tracker': 'other',
    'roi-tracker': 'other',
    'growth-experiment': 'other',
    'gumroad': 'other',
    'heal-state': 'other',
    'marketplace': 'other',
    'model-empathy-router': 'other',
    'music-player': 'other',
    'play-music': 'other',
    'paoding': 'other',
    'pet-companion': 'other',
    'public-apis-index': 'other',
    'qa-supervisor': 'other',
    'rag-pipeline': 'other',
    'rust-bridge': 'other',
    'scenarios': 'other',
    'steward': 'other',
    'suwen': 'other',
    'taiyi': 'other',
    'tianji': 'other',
    'today-stage': 'other',
    'turboquant': 'other',
    'tv-control': 'other',
    'undercover-mode': 'other',
    'vector-db': 'other',
    'video-factory': 'other',
    'video-processor': 'other',
    'xishuangbanna-travel': 'other',
    'yi': 'other',
    'yijing': 'other',
    'zapier-trigger': 'other',
    'zhiji-sentiment': 'other',
}

# 技能标签映射
SKILL_TAGS = {
    'polymarket': ['prediction', 'betting', 'crypto', 'polygon', 'polymarket', '气象', '预测'],
    'binance-trader': ['crypto', 'exchange', 'trading', 'binance', '买入', '卖出', '比特币'],
    'gmgn': ['solana', 'base', 'trading', 'defi'],
    'zhiji': ['quant', 'strategy', 'meteor', 'arbitrage', '分析', '量化'],
    'coingecko-price': ['crypto', 'price', 'market', '币价', '查询'],
    'browser-automation': ['playwright', 'screenshot', 'crawl', 'automation', '浏览器', '截图'],
    'qiaomu-info-card-designer': ['card', 'design', 'pdf', 'magazine', '卡片', '信息'],
    'shanmu-reporter': ['report', 'finance', 'analysis', 'pipeline', '研报', '生成'],
    'social-publisher': ['wechat', 'xiaohongshu', 'zhihu', 'douyin', 'publish', '发布', '小红书'],
    'content-scheduler': ['calendar', 'schedule', 'rotation', 'content', '排期'],
    'ascii-art': ['ascii', 'art', 'visualization', '艺术'],
    'news-fetcher': ['news', 'media', 'api', '新闻', '获取'],
    'api-monitor': ['monitor', 'alert', 'health', 'api', '监控'],
    'self-check': ['self', 'check', 'health', 'system', '自检'],
    'docker-ctl': ['docker', 'container', 'deploy', '部署'],
    'weather': ['weather', 'forecast', 'wttr', '天气'],
    'feishu': ['feishu', 'lark', 'doc', 'wiki', '飞书'],
    'ssh': ['ssh', 'remote', 'shell', '连接'],
}


def update_skill_metadata(skill_dir: Path):
    """更新单个技能的元数据"""
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return False
    
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析现有 Frontmatter
    if not content.startswith('---'):
        return False
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        print(f'  ⚠️  YAML 解析失败：{skill_dir.name}')
        return False
    
    skill_name = skill_dir.name
    category = SKILL_CATEGORIES.get(skill_name, 'general')
    tags = SKILL_TAGS.get(skill_name, [])
    
    # 更新元数据
    meta['category'] = category
    if tags and 'tags' not in meta:
        meta['tags'] = tags
    
    # 生成新的 Frontmatter
    new_frontmatter = '---\n'
    for key, value in meta.items():
        if isinstance(value, list):
            new_frontmatter += f'{key}: {value}\n'
        elif isinstance(value, str) and (':' in value or value.startswith('[')):
            new_frontmatter += f'{key}: \"{value}\"\n'
        else:
            new_frontmatter += f'{key}: {value}\n'
    new_frontmatter += '---\n'
    
    # 写回文件
    new_content = new_frontmatter + parts[2]
    with open(skill_md, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'  ✅ {skill_name}: category={category}, tags={tags}')
    return True


def main():
    print('🔧 批量更新技能元数据...')
    print()
    
    updated = 0
    failed = 0
    skipped = 0
    
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('_') or skill_dir.name == 'shared':
            continue
        
        try:
            if update_skill_metadata(skill_dir):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f'  ❌ {skill_dir.name}: {e}')
            failed += 1
    
    print()
    print(f'📊 统计:')
    print(f'  ✅ 更新：{updated}')
    print(f'  ⚠️  跳过：{skipped}')
    print(f'  ❌ 失败：{failed}')


if __name__ == '__main__':
    main()
