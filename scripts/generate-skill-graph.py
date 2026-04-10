#!/usr/bin/env python3
"""
Skill Graph Generator (技能关系图谱生成器)

功能:
1. 扫描所有 emerged-skill-* 目录
2. 提取 Skill 关系
3. 生成 skill-graph.json (知识图谱)
4. 可视化 Skill 关系网

集成：Knowledge Extractor + Memory System

作者：太一 AGI
创建：2026-04-10
"""

import json
import re
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"
REPORTS_DIR = WORKSPACE / "reports"


def scan_emerged_skills():
    """扫描所有能力涌现 Skill"""
    emerged_skills = []
    
    for skill_dir in SKILLS_DIR.glob("emerged-skill-*/"):
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            # 从目录名提取时间
            match = re.search(r'emerged-skill-(\d{4}\d{2}\d{2}-\d{6})', skill_dir.name)
            if match:
                timestamp_str = match.group(1)
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
                    
                    # 读取 SKILL.md 内容
                    with open(skill_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 提取 Skill 信息
                    skill_info = {
                        'id': skill_dir.name,
                        'timestamp': timestamp.isoformat(),
                        'date': timestamp.strftime("%Y-%m-%d %H:%M"),
                        'path': str(skill_dir),
                        'name': extract_skill_name(content),
                        'description': extract_skill_description(content),
                        'inspiration': extract_inspiration(content),
                        'tags': extract_tags(content)
                    }
                    
                    emerged_skills.append(skill_info)
                except Exception as e:
                    print(f"⚠️  解析 {skill_dir.name} 失败：{e}")
    
    # 按时间排序
    emerged_skills.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return emerged_skills


def extract_skill_name(content):
    """提取 Skill 名称"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Unknown"


def extract_skill_description(content):
    """提取 Skill 描述"""
    match = re.search(r'>\s*\*\*功能\*\*:\s*(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_inspiration(content):
    """提取灵感来源"""
    match = re.search(r'灵感 [来源：:]\s*(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_tags(content):
    """提取标签"""
    tags = set()
    hashtag_pattern = r'#([\\u4e00-\\u9fa5A-Za-z][\\u4e00-\\u9fa5A-Za-z0-9_-]{0,20})'
    matches = re.findall(hashtag_pattern, content)
    tags.update(matches)
    return list(tags)


def build_skill_graph(skills):
    """构建 Skill 关系图谱"""
    
    graph = {
        'schema': 'taiyi/skill-graph/v1',
        'generated_at': datetime.now().isoformat(),
        'total_skills': len(skills),
        'nodes': [],
        'edges': [],
        'metadata': {}
    }
    
    # 创建节点
    for skill in skills:
        node = {
            'id': skill['id'],
            'label': skill['name'][:50],
            'type': 'Skill',
            'timestamp': skill['timestamp'],
            'inspiration': skill['inspiration'],
            'tags': skill['tags']
        }
        graph['nodes'].append(node)
    
    # 创建边 (基于灵感来源和标签相似度)
    edges = []
    for i, skill1 in enumerate(skills):
        for skill2 in skills[i+1:]:
            # 检查是否有共同灵感来源
            if skill1['inspiration'] and skill2['inspiration']:
                if 'OpenClaw' in skill1['inspiration'] and 'OpenClaw' in skill2['inspiration']:
                    edges.append({
                        'source': skill1['id'],
                        'target': skill2['id'],
                        'type': '共同灵感',
                        'weight': 0.8
                    })
            
            # 检查是否有共同标签
            common_tags = set(skill1['tags']) & set(skill2['tags'])
            if len(common_tags) >= 2:
                edges.append({
                    'source': skill1['id'],
                    'target': skill2['id'],
                    'type': '共同标签',
                    'tags': list(common_tags),
                    'weight': min(0.5 + len(common_tags) * 0.1, 1.0)
                })
    
    graph['edges'] = edges
    graph['metadata'] = {
        'node_count': len(graph['nodes']),
        'edge_count': len(graph['edges']),
        'skills_per_day': len(skills) / max(1, (datetime.now() - datetime.strptime(skills[-1]['timestamp'], "%Y-%m-%dT%H:%M:%S")).days + 1) if skills else 0
    }
    
    return graph


def generate_summary(graph):
    """生成图谱摘要"""
    
    summary = {
        'schema': 'taiyi/skill-graph-summary/v1',
        'generated_at': datetime.now().isoformat(),
        'statistics': {
            'total_skills': graph['total_skills'],
            'nodes': graph['metadata']['node_count'],
            'edges': graph['metadata']['edge_count'],
            'avg_connections': graph['metadata']['edge_count'] / max(1, graph['metadata']['node_count'])
        },
        'top_tags': get_top_tags(graph['nodes']),
        'recent_skills': [n['label'] for n in graph['nodes'][:10]],
        'inspirations': get_unique_inspirations(graph['nodes'])
    }
    
    return summary


def get_top_tags(nodes, top_n=10):
    """获取热门标签"""
    tag_count = {}
    for node in nodes:
        for tag in node.get('tags', []):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    
    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)
    return [{'tag': tag, 'count': count} for tag, count in sorted_tags[:top_n]]


def get_unique_inspirations(nodes):
    """获取唯一样本来源"""
    inspirations = set()
    for node in nodes:
        if node.get('inspiration'):
            inspirations.add(node['inspiration'][:50])
    return list(inspirations)


def main():
    """主函数"""
    print("🧬 Skill Graph Generator - 技能关系图谱生成器")
    print("="*60)
    print()
    
    # 扫描 Skills
    print("📁 扫描能力涌现 Skills...")
    skills = scan_emerged_skills()
    print(f"✅ 发现 {len(skills)} 个 Skills")
    print()
    
    # 构建图谱
    print("🕸️ 构建关系图谱...")
    graph = build_skill_graph(skills)
    print(f"   节点：{graph['metadata']['node_count']} 个")
    print(f"   边：{graph['metadata']['edge_count']} 条")
    print()
    
    # 生成摘要
    print("📊 生成摘要...")
    summary = generate_summary(graph)
    print(f"   平均连接：{summary['statistics']['avg_connections']:.2f}")
    print(f"   热门标签：{len(summary['top_tags'])} 个")
    print()
    
    # 保存文件
    graph_file = REPORTS_DIR / "skill-graph.json"
    summary_file = REPORTS_DIR / "skill-graph-summary.json"
    
    with open(graph_file, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"✅ 图谱已保存：{graph_file}")
    
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"✅ 摘要已保存：{summary_file}")
    print()
    
    # 显示前 10 个 Skills
    print("📋 最近 Skills (前 10 个):")
    for i, skill in enumerate(skills[:10], 1):
        print(f"  {i}. {skill['name'][:50]} ({skill['date']})")
    
    if len(skills) > 10:
        print(f"  ... 还有 {len(skills) - 10} 个 Skills")
    
    print()
    print("✅ Skill Graph 生成完成")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
