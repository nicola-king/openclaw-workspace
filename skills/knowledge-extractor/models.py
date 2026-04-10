#!/usr/bin/env python3
"""
Knowledge Abstracts Models (知识抽象模型)

灵感来源：HyperExtract
功能：定义结构化知识输出的 Pydantic 模型

作者：太一 AGI
创建：2026-04-10
"""

from pydantic import BaseModel, Field
from typing import List, Set, Dict, Optional
from datetime import datetime
from enum import Enum


# ═══════════════════════════════════════════════════════════
# 枚举类型
# ═══════════════════════════════════════════════════════════

class EntityType(str, Enum):
    """实体类型"""
    AGENT = "Agent"           # Agent (太一/知几/山木等)
    SKILL = "Skill"           # Skill
    SYSTEM = "System"         # 系统 (OpenClaw/Gateway 等)
    FEATURE = "Feature"       # 功能特性
    FILE = "File"             # 文件
    CONCEPT = "Concept"       # 概念
    PERSON = "Person"         # 人物 (SAYELF)
    EVENT = "Event"           # 事件
    DECISION = "Decision"     # 决策
    TASK = "Task"             # 任务
    INSIGHT = "Insight"       # 洞察


class RelationType(str, Enum):
    """关系类型"""
    IMPLEMENTS = "实现"         # Agent 实现 Feature
    CREATES = "创建"           # Agent 创建 Skill
    USES = "使用"              # Skill 使用 System
    INTEGRATES = "集成"        # System 集成 Feature
    INSPIRES = "灵感"          # X 灵感来源 Y
    DEPENDS_ON = "依赖"        # X 依赖 Y
    ENHANCES = "增强"          # X 增强 Y
    REPLACES = "替代"          # X 替代 Y
    CONTAINS = "包含"          # X 包含 Y
    TRIGGERS = "触发"          # X 触发 Y


class TagCategory(str, Enum):
    """标签分类"""
    SYSTEM = "system"         # 系统相关
    FEATURE = "feature"       # 功能相关
    SKILL = "skill"           # Skill 相关
    MEMORY = "memory"         # 记忆相关
    AESTHETIC = "aesthetic"   # 美学相关
    TASK = "task"             # 任务相关


# ═══════════════════════════════════════════════════════════
# 核心模型
# ═══════════════════════════════════════════════════════════

class Entity(BaseModel):
    """实体"""
    
    id: str = Field(..., description="实体唯一标识")
    name: str = Field(..., description="实体名称")
    type: EntityType = Field(..., description="实体类型")
    description: Optional[str] = Field(None, description="实体描述")
    metadata: Dict[str, str] = Field(default_factory=dict, description="元数据")
    
    class Config:
        use_enum_values = True


class Relation(BaseModel):
    """关系"""
    
    from_entity: str = Field(..., description="源实体 ID")
    to_entity: str = Field(..., description="目标实体 ID")
    type: RelationType = Field(..., description="关系类型")
    description: Optional[str] = Field(None, description="关系描述")
    weight: float = Field(1.0, ge=0, le=1, description="关系权重")
    
    class Config:
        use_enum_values = True


class Event(BaseModel):
    """事件 (时间线)"""
    
    timestamp: str = Field(..., description="时间戳")
    event: str = Field(..., description="事件描述")
    type: str = Field("general", description="事件类型")
    entities: List[str] = Field(default_factory=list, description="相关实体")
    
    class Config:
        use_enum_values = True


class KnowledgeAbstract(BaseModel):
    """
    知识抽象 - 结构化知识表示
    
    灵感来源：HyperExtract Knowledge Abstract
    """
    
    # 基本信息
    source: str = Field(..., description="来源文件路径")
    extracted_at: datetime = Field(default_factory=datetime.now, description="提取时间")
    extractor: str = Field("taiyi-knowledge-extractor", description="提取器")
    
    # 核心内容
    entities: List[Entity] = Field(default_factory=list, description="实体列表")
    relationships: List[Relation] = Field(default_factory=list, description="关系图谱")
    timeline: List[Event] = Field(default_factory=list, description="时间线")
    tags: Set[str] = Field(default_factory=set, description="标签集合")
    summary: str = Field(..., description="摘要")
    
    # 质量指标
    confidence: float = Field(0.0, ge=0, le=1, description="置信度")
    model_used: str = Field("qwen3.5-plus", description="使用的模型")
    
    # 统计信息
    entity_count: int = Field(0, description="实体数量")
    relationship_count: int = Field(0, description="关系数量")
    event_count: int = Field(0, description="事件数量")
    tag_count: int = Field(0, description="标签数量")
    
    def model_post_init(self, __context):
        """后处理：更新统计信息"""
        self.entity_count = len(self.entities)
        self.relationship_count = len(self.relationships)
        self.event_count = len(self.timeline)
        self.tag_count = len(self.tags)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return self.model_dump(mode='json', exclude_none=True)
    
    def to_json(self, indent: int = 2) -> str:
        """转换为 JSON 字符串"""
        import json
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════
# 输出格式模型
# ═══════════════════════════════════════════════════════════

class GraphOutput(BaseModel):
    """图谱输出 (用于可视化)"""
    
    nodes: List[Dict] = Field(default_factory=list, description="节点")
    edges: List[Dict] = Field(default_factory=list, description="边")
    metadata: Dict = Field(default_factory=dict, description="元数据")
    
    @classmethod
    def from_abstract(cls, abstract: KnowledgeAbstract) -> 'GraphOutput':
        """从 KnowledgeAbstract 创建"""
        nodes = [
            {
                "id": e.id,
                "label": e.name,
                "type": e.type,
                "description": e.description
            }
            for e in abstract.entities
        ]
        
        edges = [
            {
                "source": r.from_entity,
                "target": r.to_entity,
                "type": r.type,
                "weight": r.weight
            }
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
    
    events: List[Event] = Field(default_factory=list, description="事件列表")
    summary: str = Field("", description="时间线摘要")
    
    @classmethod
    def from_abstract(cls, abstract: KnowledgeAbstract) -> 'TimelineOutput':
        """从 KnowledgeAbstract 创建"""
        return cls(
            events=abstract.timeline,
            summary=abstract.summary
        )


# ═══════════════════════════════════════════════════════════
# 配置模型
# ═══════════════════════════════════════════════════════════

class ExtractorConfig(BaseModel):
    """提取器配置"""
    
    # 输入配置
    input_path: str = Field(..., description="输入文件/目录路径")
    recursive: bool = Field(False, description="是否递归处理目录")
    
    # 输出配置
    output_format: str = Field("console", description="输出格式 (console/json/graph/timeline)")
    output_path: Optional[str] = Field(None, description="输出文件路径")
    
    # 提取配置
    model: str = Field("qwen3.5-plus", description="使用的模型")
    confidence_threshold: float = Field(0.7, ge=0, le=1, description="置信度阈值")
    max_entities: int = Field(100, description="最大实体数")
    max_relationships: int = Field(200, description="最大关系数")
    
    # 美学配置
    aesthetic_mode: bool = Field(True, description="启用美学输出")
    apple_design_weight: float = Field(0.80, description="苹果设计权重")
    eastern_weight: float = Field(0.15, description="东方元素权重")
    chinese_weight: float = Field(0.05, description="中国元素权重")
    
    class Config:
        use_enum_values = True


# ═══════════════════════════════════════════════════════════
# 测试数据
# ═══════════════════════════════════════════════════════════

def create_sample_abstract() -> KnowledgeAbstract:
    """创建示例知识抽象 (用于测试)"""
    
    return KnowledgeAbstract(
        source="memory/2026-04-10.md",
        extracted_at=datetime.now(),
        entities=[
            Entity(id="taiyi", name="太一 AGI", type="Agent", description="AGI 执行总管"),
            Entity(id="openclaw", name="OpenClaw 4.9", type="System", description="个人 AI 助手框架"),
            Entity(id="memory_backfill", name="Memory Backfill", type="Feature", description="记忆回填系统"),
            Entity(id="provider_aliases", name="Provider Aliases", type="Feature", description="提供商认证别名"),
            Entity(id="plugin_sdk", name="Plugin SDK", type="Feature", description="Skill 开发 SDK"),
        ],
        relationships=[
            Relation(from_entity="taiyi", to_entity="openclaw", type="INTEGRATES", description="太一融合 OpenClaw 4.9"),
            Relation(from_entity="taiyi", to_entity="memory_backfill", type="IMPLEMENTS", description="太一实现记忆回填"),
            Relation(from_entity="taiyi", to_entity="provider_aliases", type="CREATES", description="太一创建 Provider Aliases"),
            Relation(from_entity="taiyi", to_entity="plugin_sdk", type="CREATES", description="太一创建 Plugin SDK"),
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
    
    # 创建示例
    abstract = create_sample_abstract()
    
    # 显示统计
    print("📊 知识抽象统计:")
    print(f"   来源：{abstract.source}")
    print(f"   实体：{abstract.entity_count} 个")
    print(f"   关系：{abstract.relationship_count} 条")
    print(f"   事件：{abstract.event_count} 个")
    print(f"   标签：{abstract.tag_count} 个")
    print(f"   置信度：{abstract.confidence:.0%}")
    print()
    
    # 显示实体
    print("【实体】")
    for entity in abstract.entities:
        print(f"  ├─ {entity.name} ({entity.type})")
    print()
    
    # 显示关系
    print("【关系】")
    for rel in abstract.relationships:
        print(f"  ├─ {rel.from_entity} → {rel.type} → {rel.to_entity}")
    print()
    
    # 显示时间线
    print("【时间线】")
    for event in abstract.timeline:
        print(f"  ├─ {event.timestamp}: {event.event}")
    print()
    
    # 显示标签
    print("【标签】")
    print(f"  {' '.join([f'#{tag}' for tag in abstract.tags])}")
    print()
    
    # 显示摘要
    print("【摘要】")
    print(f"  {abstract.summary}")
    print()
    
    # 测试 JSON 输出
    print("📄 JSON 输出 (前 500 字符):")
    print("-"*60)
    json_output = abstract.to_json()
    print(json_output[:500] + "..." if len(json_output) > 500 else json_output)
    print()
    
    # 测试图谱输出
    print("🕸️ 图谱输出:")
    graph = GraphOutput.from_abstract(abstract)
    print(f"   节点：{len(graph.nodes)} 个")
    print(f"   边：{len(graph.edges)} 条")
    print()
    
    print("✅ 模型测试完成")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
