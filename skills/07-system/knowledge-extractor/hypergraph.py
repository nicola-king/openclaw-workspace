#!/usr/bin/env python3
"""
Hypergraph Output (超图输出)

功能:
1. 将 KnowledgeAbstract 转换为 Hypergraph
2. 支持超边 (Hyperedge) - 连接多个节点
3. 导出为 JSON/GraphML 格式

灵感来源：HyperExtract Hypergraph

作者：太一 AGI
创建：2026-04-10
"""

import json
from typing import List, Dict, Set, Any
from datetime import datetime

# 添加路径
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from models import KnowledgeAbstract, Entity, Relation


class HypergraphNode:
    """超图节点"""
    
    def __init__(self, id: str, label: str, type: str, **kwargs):
        self.id = id
        self.label = label
        self.type = type
        self.attributes = kwargs
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'label': self.label,
            'type': self.type,
            **self.attributes
        }


class HypergraphEdge:
    """超图边 (超边 - 可连接多个节点)"""
    
    def __init__(self, id: str, nodes: List[str], type: str, **kwargs):
        self.id = id
        self.nodes = nodes  # 连接的节点 ID 列表
        self.type = type
        self.attributes = kwargs
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nodes': self.nodes,
            'type': self.type,
            **self.attributes
        }


class Hypergraph:
    """超图"""
    
    def __init__(self, name: str = "Knowledge Hypergraph"):
        self.name = name
        self.nodes: Dict[str, HypergraphNode] = {}
        self.edges: Dict[str, HypergraphEdge] = {}
        self.metadata: Dict[str, Any] = {}
    
    def add_node(self, id: str, label: str, type: str, **kwargs):
        """添加节点"""
        self.nodes[id] = HypergraphNode(id, label, type, **kwargs)
    
    def add_edge(self, id: str, nodes: List[str], type: str, **kwargs):
        """添加超边"""
        self.edges[id] = HypergraphEdge(id, nodes, type, **kwargs)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'name': self.name,
            'generated_at': datetime.now().isoformat(),
            'metadata': self.metadata,
            'nodes': [node.to_dict() for node in self.nodes.values()],
            'edges': [edge.to_dict() for edge in self.edges.values()]
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为 JSON"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def to_graphml(self) -> str:
        """转换为 GraphML 格式 (用于 Gephi/Cytoscape 可视化)"""
        graphml = ['<?xml version="1.0" encoding="UTF-8"?>']
        graphml.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
        graphml.append('  <graph edgedefault="undirected">')
        
        # 节点
        for node in self.nodes.values():
            graphml.append(f'    <node id="{node.id}">')
            graphml.append(f'      <data key="label">{node.label}</data>')
            graphml.append(f'      <data key="type">{node.type}</data>')
            graphml.append('    </node>')
        
        # 边 (超图需要特殊处理)
        for edge in self.edges.values():
            if len(edge.nodes) == 2:
                # 普通边
                graphml.append(f'    <edge source="{edge.nodes[0]}" target="{edge.nodes[1]}">')
                graphml.append(f'      <data key="type">{edge.type}</data>')
                graphml.append('    </edge>')
            else:
                # 超边 - 使用超节点表示
                hypernode_id = f"hyper_{edge.id}"
                graphml.append(f'    <node id="{hypernode_id}">')
                graphml.append(f'      <data key="label">Hyperedge: {edge.type}</data>')
                graphml.append(f'      <data key="type">hyperedge</data>')
                graphml.append('    </node>')
                
                for node_id in edge.nodes:
                    graphml.append(f'    <edge source="{hypernode_id}" target="{node_id}"/>')
        
        graphml.append('  </graph>')
        graphml.append('</graphml>')
        
        return '\n'.join(graphml)
    
    @classmethod
    def from_abstract(cls, abstract: KnowledgeAbstract) -> 'Hypergraph':
        """从 KnowledgeAbstract 创建超图"""
        
        hypergraph = cls(name=f"Knowledge Hypergraph - {abstract.source}")
        hypergraph.metadata = {
            'source': abstract.source,
            'extracted_at': abstract.extracted_at.isoformat(),
            'entity_count': abstract.entity_count,
            'relationship_count': abstract.relationship_count,
            'tag_count': abstract.tag_count
        }
        
        # 添加实体节点
        for entity in abstract.entities:
            hypergraph.add_node(
                id=entity.id,
                label=entity.name,
                type=entity.type,
                description=entity.description
            )
        
        # 添加关系边 (普通边)
        for i, rel in enumerate(abstract.relationships):
            hypergraph.add_edge(
                id=f"rel_{i}",
                nodes=[rel.from_entity, rel.to_entity],
                type=rel.type,
                description=rel.description,
                weight=rel.weight
            )
        
        # 添加标签超边 (连接所有具有相同标签的实体)
        tags = list(abstract.tags)
        if tags:
            hypergraph.add_edge(
                id="tag_hyperedge",
                nodes=[e.id for e in abstract.entities],
                type="shared_tags",
                tags=tags
            )
        
        return hypergraph


def main():
    """主函数 - 测试超图"""
    print("🕸️ Hypergraph Output - 超图输出")
    print("="*60)
    print()
    
    # 创建示例 KnowledgeAbstract
    from models import create_sample_abstract
    abstract = create_sample_abstract()
    
    # 转换为超图
    hypergraph = Hypergraph.from_abstract(abstract)
    
    print(f"📊 超图统计:")
    print(f"   名称：{hypergraph.name}")
    print(f"   节点：{len(hypergraph.nodes)} 个")
    print(f"   边：{len(hypergraph.edges)} 条")
    print(f"   超边：{len([e for e in hypergraph.edges.values() if len(e.nodes) > 2])} 条")
    print()
    
    # JSON 输出
    print("📄 JSON 输出 (前 1000 字符):")
    json_output = hypergraph.to_json()
    print(json_output[:1000] + "..." if len(json_output) > 1000 else json_output)
    print()
    
    # GraphML 输出
    print("📄 GraphML 输出 (前 1000 字符):")
    graphml_output = hypergraph.to_graphml()
    print(graphml_output[:1000] + "..." if len(graphml_output) > 1000 else graphml_output)
    print()
    
    print("✅ 超图测试完成")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
