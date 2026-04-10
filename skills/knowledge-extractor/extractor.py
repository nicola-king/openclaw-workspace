#!/usr/bin/env python3
"""
Knowledge Extractor (知识提取器)

功能:
1. 从 Markdown 文档提取结构化知识
2. 输出 Knowledge Abstracts
3. 支持 Console/JSON/Graph/Timeline 格式

灵感来源：HyperExtract - Smart Knowledge Extraction CLI

作者：太一 AGI
创建：2026-04-10
"""

import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional

# 添加路径
import sys
sys.path.insert(0, str(Path(__file__).parent))

from models import (
    KnowledgeAbstract, Entity, Relation, Event,
    EntityType, RelationType,
    GraphOutput, TimelineOutput,
    ExtractorConfig, create_sample_abstract
)

# 工作区路径
WORKSPACE = Path("/home/nicola/.openclaw/workspace")


# ═══════════════════════════════════════════════════════════
# 提取器核心
# ═══════════════════════════════════════════════════════════

class KnowledgeExtractor:
    """知识提取器"""
    
    def __init__(self, config: Optional[ExtractorConfig] = None):
        self.config = config or ExtractorConfig(
            input_path="",
            output_format="console"
        )
    
    def extract(self, file_path: str) -> KnowledgeAbstract:
        """
        从文件提取知识
        
        Args:
            file_path: 文件路径
        
        Returns:
            KnowledgeAbstract 知识抽象
        """
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        # 读取内容
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取各个部分
        entities = self._extract_entities(content, path)
        relationships = self._extract_relationships(content, entities)
        timeline = self._extract_timeline(content)
        tags = self._extract_tags(content)
        summary = self._generate_summary(content, entities)
        
        # 创建知识抽象
        abstract = KnowledgeAbstract(
            source=str(path),
            entities=entities,
            relationships=relationships,
            timeline=timeline,
            tags=tags,
            summary=summary,
            confidence=0.85,  # 基于规则提取，置信度中等
            model_used=self.config.model
        )
        
        return abstract
    
    def _extract_entities(self, content: str, path: Path) -> List[Entity]:
        """提取实体"""
        entities = []
        entity_id = 0
        
        # 提取标题作为实体
        title_patterns = [
            (r'^#{4,}\s+(.+)$', EntityType.SKILL),  # 4+ 级标题
            (r'^###\s+(.+)$', EntityType.FEATURE),
            (r'^##\s+(.+)$', EntityType.CONCEPT),
            (r'^#\s+(.+)$', EntityType.CONCEPT),
        ]
        
        for pattern, entity_type in title_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                name = match.strip()
                if name and len(name) < 100:  # 过滤无效标题
                    entities.append(Entity(
                        id=f"entity_{entity_id}",
                        name=name,
                        type=entity_type,
                        description=f"来自 {path.name}"
                    ))
                    entity_id += 1
        
        # 提取【决策】【任务】【洞察】等标记
        marker_patterns = {
            '【决策】': EntityType.DECISION,
            '【任务】': EntityType.TASK,
            '【洞察】': EntityType.INSIGHT,
            '【能力涌现】': EntityType.FEATURE,
        }
        
        for marker, entity_type in marker_patterns.items():
            pattern = rf'{marker}\s*\n(.*?)(?=【|$)'
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                entities.append(Entity(
                    id=f"entity_{entity_id}",
                    name=match.strip()[:50],
                    type=entity_type,
                    description=match.strip()
                ))
                entity_id += 1
        
        # 限制实体数量
        return entities[:self.config.max_entities]
    
    def _extract_relationships(self, content: str, entities: List[Entity]) -> List[Relation]:
        """提取关系"""
        relationships = []
        
        # 简单规则：如果两个实体在同一段落，建立关系
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            para_entities = []
            for entity in entities:
                if entity.name in para:
                    para_entities.append(entity.id)
            
            # 建立关系
            for i, e1 in enumerate(para_entities):
                for e2 in para_entities[i+1:]:
                    relationships.append(Relation(
                        from_entity=e1,
                        to_entity=e2,
                        type=RelationType.CONTAINS,
                        description="同段落共现"
                    ))
        
        return relationships[:self.config.max_relationships]
    
    def _extract_timeline(self, content: str) -> List[Event]:
        """提取时间线"""
        events = []
        
        # 提取时间标记 - 更精确的模式
        # 只提取 HH:MM 格式，后面跟有效中文/英文描述
        time_pattern = r'(\d{2}:\d{2})\s*[:：]?\s*([\u4e00-\u9fa5A-Za-z][^\n]{0,100})'
        matches = re.findall(time_pattern, content)
        
        for timestamp, event_text in matches:
            # 清理事件文本
            event_clean = event_text.strip()
            # 过滤无效事件
            if event_clean and len(event_clean) >= 2 and len(event_clean) <= 100:
                # 排除包含括号不匹配的
                if event_clean.count(')') == event_clean.count('('):
                    events.append(Event(
                        timestamp=timestamp,
                        event=event_clean,
                        type='time'
                    ))
        
        return events
    
    def _extract_tags(self, content: str) -> Set[str]:
        """提取标签"""
        tags = set()
        
        # 提取 #标签 (必须是有效标签 - 中文或字母开头，排除颜色代码)
        hashtag_pattern = r'#([\u4e00-\u9fa5][\u4e00-\u9fa5a-zA-Z0-9_-]{0,20}|[a-zA-Z][a-zA-Z0-9_-]{0,20})'
        matches = re.findall(hashtag_pattern, content)
        for match in matches:
            # 排除颜色代码 (如 #8E8E93, #FFFFFF 等 6 位十六进制)
            if not re.match(r'^[0-9A-Fa-f]{6}$', match):
                tags.add(match)
        
        # 提取常见关键词作为标签
        keywords = {
            'OpenClaw': 'OpenClaw',
            '记忆': '记忆系统',
            '能力': '能力涌现',
            '美学': '美学宪法',
            '设计': '设计系统',
            '模型': '模型路由',
            '知识': '知识提取',
        }
        
        for keyword, tag in keywords.items():
            if keyword in content:
                tags.add(tag)
        
        return tags
    
    def _generate_summary(self, content: str, entities: List[Entity]) -> str:
        """生成摘要"""
        # 提取第一个段落作为预览
        paragraphs = content.split('\n\n')
        preview = ""
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('#') and not para.startswith('['):
                preview = para[:300]
                break
        
        if not preview:
            preview = content[:300].strip()
        
        if len(preview) >= 300:
            preview += "..."
        
        summary = f"文档包含 {len(entities)} 个实体。内容预览：{preview}"
        return summary


# ═══════════════════════════════════════════════════════════
# 输出格式化
# ═══════════════════════════════════════════════════════════

class OutputFormatter:
    """输出格式化器"""
    
    @staticmethod
    def format_console(abstract: KnowledgeAbstract) -> str:
        """控制台格式"""
        output = []
        
        # 头部
        output.append("╔═══════════════════════════════════════════════════════════╗")
        output.append("║  🧠 知识抽象 · Knowledge Abstract                         ║")
        output.append(f"║  来源：{abstract.source:<54}║")
        output.append("╚═══════════════════════════════════════════════════════════╝")
        output.append("")
        
        # 实体
        output.append(f"【实体】{abstract.entity_count} 个")
        for entity in abstract.entities[:10]:
            output.append(f"  ├─ {entity.name} ({entity.type})")
        if abstract.entity_count > 10:
            output.append(f"  └─ ... 还有 {abstract.entity_count - 10} 个")
        output.append("")
        
        # 关系
        output.append(f"【关系】{abstract.relationship_count} 条")
        for rel in abstract.relationships[:10]:
            output.append(f"  ├─ {rel.from_entity} → {rel.type} → {rel.to_entity}")
        if abstract.relationship_count > 10:
            output.append(f"  └─ ... 还有 {abstract.relationship_count - 10} 条")
        output.append("")
        
        # 时间线
        output.append(f"【时间线】{abstract.event_count} 事件")
        for event in abstract.timeline[:10]:
            output.append(f"  ├─ {event.timestamp}: {event.event}")
        output.append("")
        
        # 标签
        output.append("【标签】")
        tag_str = " ".join([f"#{tag}" for tag in list(abstract.tags)[:20]])
        output.append(f"  {tag_str}")
        output.append("")
        
        # 摘要
        output.append("【摘要】")
        output.append(f"  {abstract.summary[:200]}")
        output.append("")
        
        # 统计
        output.append("📊 统计:")
        output.append(f"   置信度：{abstract.confidence:.0%}")
        output.append(f"   模型：{abstract.model_used}")
        output.append(f"   提取时间：{abstract.extracted_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_json(abstract: KnowledgeAbstract, indent: int = 2) -> str:
        """JSON 格式"""
        return abstract.to_json(indent)
    
    @staticmethod
    def format_graph(abstract: KnowledgeAbstract) -> str:
        """图谱格式"""
        graph = GraphOutput.from_abstract(abstract)
        return json.dumps(graph.model_dump(mode='json'), indent=2, ensure_ascii=False)
    
    @staticmethod
    def format_timeline(abstract: KnowledgeAbstract) -> str:
        """时间线格式"""
        timeline = TimelineOutput.from_abstract(abstract)
        output = []
        
        output.append("📅 时间线")
        output.append("="*60)
        for event in timeline.events:
            output.append(f"  {event.timestamp} | {event.event}")
        output.append("")
        output.append(f"摘要：{timeline.summary}")
        
        return "\n".join(output)


# ═══════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="🧠 太一知识提取器 - 从文档提取结构化知识",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 extractor.py memory/2026-04-10.md
  python3 extractor.py input.md --output json --output-file result.json
  python3 extractor.py memory/ --recursive --output graph
        """
    )
    
    parser.add_argument("input", help="输入文件/目录路径")
    parser.add_argument("--output", "-o", default="console",
                       choices=["console", "json", "graph", "timeline"],
                       help="输出格式 (默认：console)")
    parser.add_argument("--output-file", "-f", help="输出文件路径")
    parser.add_argument("--recursive", "-r", action="store_true",
                       help="递归处理目录")
    parser.add_argument("--model", "-m", default="qwen3.5-plus",
                       help="使用的模型 (默认：qwen3.5-plus)")
    parser.add_argument("--sample", action="store_true",
                       help="显示示例输出")
    
    args = parser.parse_args()
    
    # 示例模式
    if args.sample:
        print("🧠 Knowledge Extractor - 示例输出")
        print("="*60)
        print()
        abstract = create_sample_abstract()
        print(OutputFormatter.format_console(abstract))
        return 0
    
    # 创建提取器
    config = ExtractorConfig(
        input_path=args.input,
        output_format=args.output,
        output_path=args.output_file,
        recursive=args.recursive,
        model=args.model
    )
    
    extractor = KnowledgeExtractor(config)
    
    # 处理文件/目录
    input_path = Path(args.input)
    
    if input_path.is_file():
        # 单个文件
        abstract = extractor.extract(str(input_path))
        output = format_output(abstract, args.output)
        
        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ 输出已保存到：{args.output_file}")
        else:
            print(output)
    
    elif input_path.is_dir():
        # 目录
        if args.recursive:
            files = list(input_path.glob("**/*.md"))
        else:
            files = list(input_path.glob("*.md"))
        
        print(f"📁 发现 {len(files)} 个 Markdown 文件")
        
        for file in files[:10]:  # 限制处理 10 个文件
            print(f"\n处理：{file}")
            abstract = extractor.extract(str(file))
            print(OutputFormatter.format_console(abstract))
        
        if len(files) > 10:
            print(f"\n... 还有 {len(files) - 10} 个文件未显示")
    
    else:
        print(f"❌ 路径不存在：{args.input}")
        return 1
    
    return 0


def format_output(abstract: KnowledgeAbstract, format_type: str) -> str:
    """格式化输出"""
    formatters = {
        "console": OutputFormatter.format_console,
        "json": OutputFormatter.format_json,
        "graph": OutputFormatter.format_graph,
        "timeline": OutputFormatter.format_timeline,
    }
    
    formatter = formatters.get(format_type, OutputFormatter.format_console)
    return formatter(abstract)


if __name__ == "__main__":
    import sys
    sys.exit(main())
