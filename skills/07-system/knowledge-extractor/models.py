#!/usr/bin/env python3
"""
Knowledge Abstracts Models (知识抽象模型)

灵感来源：HyperExtract
功能：定义结构化知识输出的 Pydantic 模型

作者：太一 AGI
创建：2026-04-10
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Set, Dict, Optional
from datetime import datetime
from enum import Enum


# ═══════════════════════════════════════════════════════════
# 枚举类型
# ═══════════════════════════════════════════════════════════

class EntityType(str, Enum):
    """实体类型"""
    AGENT = "Agent"
    SKILL = "Skill"
    SYSTEM = "System"
    FEATURE = "Feature"
    FILE = "File"
    CONCEPT = "Concept"
    PERSON = "Person"
    EVENT = "Event"
    DECISION = "Decision"
    TASK = "Task"
    INSIGHT = "Insight"


class RelationType(str, Enum):
    """关系类型"""
    IMPLEMENTS = "实现"
    CREATES = "创建"
    USES = "使用"
    INTEGRATES = "集成"
    INSPIRES = "灵感"
    DEPENDS_ON = "依赖"
    ENHANCES = "增强"
    REPLACES = "替代"
    CONTAINS = "包含"
    TRIGGERS = "触发"


# ═══════════════════════════════════════════════════════════
# 核心模型
# ═══════════════════════════════════════════════════════════

class Entity(BaseModel):
    """实体"""
    
    model_config = ConfigDict(use_enum_values=True)
    
    id: str = Field(..., description="实体唯一标识")
    name: str = Field(..., description="实体名称")
    type: EntityType = Field(..., description="实体类型")
    description: Optional[str] = Field(None, description="实体描述")
    metadata: Dict[str, str] = Field(default_factory=dict, description="元数据")


class Relation(BaseModel):
    """关系"""
    
    model_config = ConfigDict(use_enum_values=True)
    
    from_entity: str = Field(..., description="源实体 ID")
    to_entity: str = Field(..., description="目标实体 ID")
    type: RelationType = Field(..., description="关系类型")
    description: Optional[str] = Field(None, description="关系描述")
    weight: float = Field(1.0, ge=0, le=1, description="关系权重")


class Event(BaseModel):
    """事件 (时间线)"""
    
    model_config = ConfigDict(use_enum_values=True)
    
    timestamp: str = Field(..., description="时间戳")
    event: str = Field(..., description="事件描述")
    type: str = Field("general", description="事件类型")
    entities: List[str] = Field(default_factory=list, description="相关实体")


class KnowledgeAbstract(BaseModel):
    """知识抽象 - 结构化知识表示"""
    
    model_config = ConfigDict(use_enum_values=True)
    
    source: str = Field(..., description="来源文件路径")
    extracted_at: datetime = Field(default_factory=datetime.now, description="提取时间")
    extractor: str = Field("taiyi-knowledge-extractor", description="提取器")
    
    entities: List[Entity] = Field(default_factory=list, description="实体列表")
    relationships: List[Relation] = Field(default_factory=list, description="关系图谱")
    timeline: List[Event] = Field(default_factory=list, description="时间线")
    tags: Set[str] = Field(default_factory=set, description="标签集合")
    summary: str = Field(..., description="摘要")
    
    confidence: float = Field(0.0, ge=0, le=1, description="置信度")
    model_used: str = Field("qwen3.5-plus", description="使用的模型")
    
    entity_count: int = Field(0, description="实体数量")
    relationship_count: int = Field(0, description="关系数量")
    event_count: int = Field(0, description="事件数量")
    tag_count: int = Field(0, description="标签数量")
    
    def model_post_init(self, __context):
        self.entity_count = len(self.entities)
        self.relationship_count = len(self.relationships)
        self.event_count = len(self.timeline)
        self.tag_count = len(self.tags)
    
    def to_dict(self) -> dict:
        return self.model_dump(mode='json', exclude_none=True)
    
    def to_json(self, indent: int = 2) -> str:
        import json
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════
# 输出格式模型
# ═══════════════════════════════════════════════════════════

class GraphOutput(BaseModel):
    """图谱输出"""
    
    nodes: List[Dict] = Field(default_factory=list)
    edges: List[Dict] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)
    
    @classmethod
    def from_abstract(cls, abstract: KnowledgeAbstract) -> 'GraphOutput':
        nodes = [
            {"id": e.id, "label": e.name, "type": e.type, "description": e.description}
            for e in abstract.entities
        ]
        edges = [
            {"source": r.from_entity, "target": r.to_entity, "type": r.type, "weight": r.weight}
            for r in abstract.relationships
        ]
        return cls(
            nodes=nodes,
            edges=edges,
            metadata={
                "source": abstract.source,
                "extracted_at": abstract.extracted_at.isoformat(),
                "entity_count": abstract.entity_count,
                "relationship_count": abstract.relationship_count
            }
        )


class TimelineOutput(BaseModel):
    """时间线输出"""
    
    events: List[Event] = Field(default_factory=list)
    summary: str = Field("")
    
    @classmethod
    def from_abstract(cls, abstract: KnowledgeAbstract) -> 'TimelineOutput':
        return cls(events=abstract.timeline, summary=abstract.summary)


# ═══════════════════════════════════════════════════════════
# 配置模型
# ═══════════════════════════════════════════════════════════

class ExtractorConfig(BaseModel):
    """提取器配置"""
    
    model_config = ConfigDict(use_enum_values=True)
    
    input_path: str = Field(..., description="输入文件/目录路径")
    recursive: bool = Field(False, description="是否递归处理目录")
    output_format: str = Field("console", description="输出格式")
    output_path: Optional[str] = Field(None, description="输出文件路径")
    model: str = Field("qwen3.5-plus", description="使用的模型")
    confidence_threshold: float = Field(0.7, ge=0, le=1, description="置信度阈值")
    max_entities: int = Field(100, description="最大实体数")
    max_relationships: int = Field(200, description="最大关系数")
    aesthetic_mode: bool = Field(True, description="启用美学输出")


# ═══════════════════════════════════════════════════════════
# 测试数据
# ═══════════════════════════════════════════════════════════

def create_sample_abstract() -> KnowledgeAbstract:
    """创建示例知识抽象"""
    
    return KnowledgeAbstract(
        source="memory/2026-04-10.md",
        extracted_at=datetime.now(),
        entities=[
            Entity(id="taiyi", name="太一 AGI", type=EntityType.AGENT, description="AGI 执行总管"),
            Entity(id="openclaw", name="OpenClaw 4.9", type=EntityType.SYSTEM, description="个人 AI 助手框架"),
            Entity(id="memory_backfill", name="Memory Backfill", type=EntityType.FEATURE, description="记忆回填系统"),
            Entity(id="provider_aliases", name="Provider Aliases", type=EntityType.FEATURE, description="提供商认证别名"),
            Entity(id="plugin_sdk", name="Plugin SDK", type=EntityType.FEATURE, description="Skill 开发 SDK"),
        ],
        relationships=[
            Relation(from_entity="taiyi", to_entity="openclaw", type=RelationType.INTEGRATES, description="太一融合 OpenClaw 4.9"),
            Relation(from_entity="taiyi", to_entity="memory_backfill", type=RelationType.IMPLEMENTS, description="太一实现记忆回填"),
            Relation(from_entity="taiyi", to_entity="provider_aliases", type=RelationType.CREATES, description="太一创建 Provider Aliases"),
            Relation(from_entity="taiyi", to_entity="plugin_sdk", type=RelationType.CREATES, description="太一创建 Plugin SDK"),
        ],
        timeline=[
            Event(timestamp="13:00", event="开始 P0 实施", type="start"),
            Event(timestamp="13:35", event="P1 功能完成", type="milestone"),
            Event(timestamp="13:50", event="P2 功能完成", type="complete"),
        ],
        tags={"OpenClaw", "记忆系统", "能力涌现", "P0/P1/P2", "知识提取"},
        summary="2026-04-10 完成 OpenClaw 4.9 全面融合，实施 11 项 P0/P1/P2 功能。",
        confidence=0.95,
        model_used="qwen3.5-plus"
    )


# ═══════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════

def main():
    """主函数 - 测试模型"""
    print("🧠 Knowledge Abstracts Models - 知识抽象模型")
    print("="*60)
    print()
    
    abstract = create_sample_abstract()
    
    print("📊 知识抽象统计:")
    print(f"   来源：{abstract.source}")
    print(f"   实体：{abstract.entity_count} 个")
    print(f"   关系：{abstract.relationship_count} 条")
    print(f"   事件：{abstract.event_count} 个")
    print(f"   标签：{abstract.tag_count} 个")
    print(f"   置信度：{abstract.confidence:.0%}")
    print()
    
    print("【实体】")
    for entity in abstract.entities:
        print(f"  ├─ {entity.name} ({entity.type})")
    print()
    
    print("【关系】")
    for rel in abstract.relationships:
        print(f"  ├─ {rel.from_entity} → {rel.type} → {rel.to_entity}")
    print()
    
    print("【时间线】")
    for event in abstract.timeline:
        print(f"  ├─ {event.timestamp}: {event.event}")
    print()
    
    print("【标签】")
    print(f"  {' '.join([f'#{tag}' for tag in abstract.tags])}")
    print()
    
    print("【摘要】")
    print(f"  {abstract.summary}")
    print()
    
    print("✅ 模型测试完成")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
