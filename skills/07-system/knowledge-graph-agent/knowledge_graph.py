#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一知识图谱智能体 v1.0
基于 LLM Wiki + Graphify + Claude-Obsidian 蒸馏融合

太一 AGI · 2026-04-22 00:15
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class KnowledgeGraphAgent:
    """知识图谱智能体 - 10 个项目融合"""
    
    def __init__(self):
        """初始化知识图谱智能体"""
        self.name = "太一知识图谱智能体"
        self.version = "1.0"
        self.created_at = datetime.now()
        
        # 三层架构
        self.layers = {
            'raw': './documents',        # 原始来源
            'wiki': './knowledge-base/wiki',  # Wiki 层
            'schema': './knowledge-base/schema'  # Schema 层
        }
        
        # 实体类型
        self.entity_types = [
            '概念', '人物', '组织', '产品',
            '技术', '事件', '地点', '文档'
        ]
        
        # 关系类型
        self.relation_types = [
            '属于', '使用', '创建', '影响',
            '相关', '依赖', '增强', '替代'
        ]
    
    def build_graph(self, source_dir: str, output_dir: str = None) -> Dict:
        """
        构建知识图谱
        
        Args:
            source_dir: 源文档目录
            output_dir: 输出目录
        
        Returns:
            Dict: 图谱构建结果
        """
        print(f"\n🔍 构建知识图谱：{source_dir}")
        print("=" * 60)
        
        if output_dir is None:
            output_dir = './knowledge-base'
        
        # 创建输出目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        Path(f"{output_dir}/wiki").mkdir(parents=True, exist_ok=True)
        Path(f"{output_dir}/graph").mkdir(parents=True, exist_ok=True)
        
        # 扫描文档
        documents = self._scan_documents(source_dir)
        print(f"📄 扫描到 {len(documents)} 个文档")
        
        # 提取实体
        entities = self._extract_entities(documents)
        print(f"🏷️  提取到 {len(entities)} 个实体")
        
        # 建立关系
        relations = self._build_relations(entities)
        print(f"🔗 建立 {len(relations)} 个关系")
        
        # 生成图谱
        graph = {
            'build_time': datetime.now().isoformat(),
            'agent': f"{self.name} v{self.version}",
            'source_dir': source_dir,
            'document_count': len(documents),
            'entity_count': len(entities),
            'relation_count': len(relations),
            'entities': entities,
            'relations': relations
        }
        
        # 保存图谱
        graph_file = Path(output_dir) / 'graph' / 'knowledge_graph.json'
        with open(graph_file, 'w', encoding='utf-8') as f:
            json.dump(graph, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 图谱已保存：{graph_file}")
        
        # 生成索引
        index = self._generate_index(entities)
        index_file = Path(output_dir) / 'wiki' / 'index.md'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index)
        
        print(f"✅ 索引已保存：{index_file}")
        
        return graph
    
    def _scan_documents(self, source_dir: str) -> List[Dict]:
        """扫描文档"""
        documents = []
        source_path = Path(source_dir)
        
        if not source_path.exists():
            print(f"⚠️  目录不存在，使用示例文档")
            # 创建示例文档
            return self._create_sample_documents()
        
        for file_path in source_path.glob('**/*.md'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            documents.append({
                'path': str(file_path),
                'name': file_path.stem,
                'content': content,
                'size': len(content),
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
        
        return documents
    
    def _create_sample_documents(self) -> List[Dict]:
        """创建示例文档"""
        return [
            {
                'path': 'sample/rag-intro.md',
                'name': 'rag-intro',
                'content': '''# RAG 检索增强生成

RAG (Retrieval-Augmented Generation) 是一种结合检索和生成的 AI 架构。

## 核心组件
- LLM (大语言模型)
- 向量数据库
- Embedding 模型

## 工作流程
1. 用户提问
2. 检索相关知识
3. LLM 生成答案

## 优势
- 减少幻觉
- 提供引用
- 知识可更新
''',
                'size': 300,
                'modified': datetime.now().isoformat()
            },
            {
                'path': 'sample/llm-architecture.md',
                'name': 'llm-architecture',
                'content': '''# LLM 架构

LLM (Large Language Model) 大语言模型架构。

## 核心组件
- Transformer
- Attention 机制
- Positional Encoding

## 代表模型
- GPT 系列
- Claude 系列
- Qwen 系列

## 应用
- RAG
- Agent
- Fine-tuning
''',
                'size': 280,
                'modified': datetime.now().isoformat()
            },
            {
                'path': 'sample/agent-patterns.md',
                'name': 'agent-patterns',
                'content': '''# Agent 设计模式

AI Agent 是自主执行任务的智能体。

## 核心能力
- 规划 (Planning)
- 工具使用 (Tool Use)
- 记忆 (Memory)

## 架构
- ReAct
- Reflexion
- Tree of Thoughts

## 应用
- 代码生成
- 数据分析
- 知识管理
''',
                'size': 290,
                'modified': datetime.now().isoformat()
            }
        ]
    
    def _extract_entities(self, documents: List[Dict]) -> List[Dict]:
        """提取实体"""
        entities = []
        entity_id = 0
        
        for doc in documents:
            content = doc['content']
            
            # 简单关键词提取 (实际应使用 LLM)
            keywords = self._extract_keywords(content)
            
            for keyword in keywords:
                entity_id += 1
                entities.append({
                    'id': f'E{entity_id:04d}',
                    'name': keyword,
                    'type': self._classify_entity(keyword),
                    'source': doc['name'],
                    'mentions': 1,
                    'description': f'{keyword} - 从文档 {doc["name"]} 中提取'
                })
        
        # 去重
        unique_entities = {}
        for entity in entities:
            key = entity['name'].lower()
            if key not in unique_entities:
                unique_entities[key] = entity
            else:
                unique_entities[key]['mentions'] += 1
        
        return list(unique_entities.values())
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        # 简单实现：提取标题和粗体内容
        keywords = []
        
        # 提取标题
        titles = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        keywords.extend(titles)
        
        # 提取粗体
        bolds = re.findall(r'\*\*(.+?)\*\*', content)
        keywords.extend(bolds)
        
        # 提取英文缩写
        abbrevs = re.findall(r'\b[A-Z]{2,5}\b', content)
        keywords.extend(abbrevs)
        
        return list(set(keywords))[:20]  # 限制数量
    
    def _classify_entity(self, name: str) -> str:
        """分类实体"""
        # 简单规则分类
        if name.upper() in ['RAG', 'LLM', 'API', 'AI', 'GPU', 'TPU']:
            return '技术'
        elif name.endswith('模型'):
            return '技术'
        elif name.endswith('架构'):
            return '技术'
        elif name.endswith('模式'):
            return '概念'
        else:
            return '概念'
    
    def _build_relations(self, entities: List[Dict]) -> List[Dict]:
        """建立关系"""
        relations = []
        relation_id = 0
        
        # 简单共现关系
        entity_names = [e['name'].lower() for e in entities]
        
        for i, entity1 in enumerate(entities):
            for j, entity2 in enumerate(entities):
                if i >= j:
                    continue
                
                # 检查是否在同一文档
                if entity1['source'] == entity2['source']:
                    relation_id += 1
                    relations.append({
                        'id': f'R{relation_id:04d}',
                        'from': entity1['id'],
                        'to': entity2['id'],
                        'type': '相关',
                        'confidence': 0.8,
                        'source': entity1['source']
                    })
        
        return relations
    
    def _generate_index(self, entities: List[Dict]) -> str:
        """生成索引"""
        index = []
        index.append("# 知识图谱索引\n")
        index.append(f"> 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        index.append(f"> 实体总数：{len(entities)}\n")
        index.append("")
        
        # 按类型分组
        by_type = {}
        for entity in entities:
            entity_type = entity['type']
            if entity_type not in by_type:
                by_type[entity_type] = []
            by_type[entity_type].append(entity)
        
        # 生成目录
        for entity_type, type_entities in sorted(by_type.items()):
            index.append(f"## {entity_type}\n")
            for entity in sorted(type_entities, key=lambda x: x['name']):
                index.append(f"- **{entity['name']}** ({entity['mentions']} 次提及)")
            index.append("")
        
        return "\n".join(index)
    
    def query(self, question: str, graph_file: str = None) -> Dict:
        """
        查询知识
        
        Args:
            question: 查询问题
            graph_file: 图谱文件路径
        
        Returns:
            Dict: 查询结果
        """
        print(f"\n🔍 查询：{question}")
        print("=" * 60)
        
        # 加载图谱
        if graph_file is None:
            graph_file = './knowledge-base/graph/knowledge_graph.json'
        
        try:
            with open(graph_file, 'r', encoding='utf-8') as f:
                graph = json.load(f)
        except FileNotFoundError:
            return {
                'error': '图谱不存在，请先构建',
                'suggestion': '运行 build_graph()'
            }
        
        # 简单关键词匹配 (实际应使用向量检索)
        keywords = question.lower().split()
        matched_entities = []
        
        for entity in graph['entities']:
            for keyword in keywords:
                if keyword in entity['name'].lower():
                    matched_entities.append(entity)
                    break
        
        # 生成答案
        answer = self._generate_answer(question, matched_entities, graph)
        
        return {
            'question': question,
            'query_time': datetime.now().isoformat(),
            'matched_entities': matched_entities,
            'answer': answer,
            'sources': list(set([e['source'] for e in matched_entities]))
        }
    
    def _generate_answer(self, question: str, entities: List[Dict], graph: Dict) -> str:
        """生成答案"""
        if not entities:
            return "未找到相关知识，请尝试其他关键词。"
        
        answer = []
        answer.append(f"根据知识库，找到 {len(entities)} 个相关实体：\n")
        
        for entity in entities[:5]:  # 限制显示数量
            answer.append(f"- **{entity['name']}** ({entity['type']})")
            answer.append(f"  {entity['description']}")
        
        answer.append("\n相关文档:")
        sources = list(set([e['source'] for e in entities]))
        for source in sources[:3]:
            answer.append(f"- {source}")
        
        return "\n".join(answer)
    
    def organize(self, source_dir: str, output_dir: str = None) -> Dict:
        """
        整理文档
        
        Args:
            source_dir: 源目录
            output_dir: 输出目录
        
        Returns:
            Dict: 整理结果
        """
        print(f"\n📁 整理文档：{source_dir}")
        print("=" * 60)
        
        if output_dir is None:
            output_dir = './knowledge-base/organized'
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 扫描文档
        documents = self._scan_documents(source_dir)
        
        # 分类
        categories = {
            '技术': [],
            '概念': [],
            '教程': [],
            '其他': []
        }
        
        for doc in documents:
            category = self._categorize_document(doc['content'])
            categories[category].append(doc['name'])
        
        # 生成目录
        toc = self._generate_toc(categories)
        toc_file = Path(output_dir) / 'README.md'
        with open(toc_file, 'w', encoding='utf-8') as f:
            f.write(toc)
        
        print(f"✅ 目录已保存：{toc_file}")
        
        return {
            'organize_time': datetime.now().isoformat(),
            'document_count': len(documents),
            'categories': {k: len(v) for k, v in categories.items()}
        }
    
    def _categorize_document(self, content: str) -> str:
        """分类文档"""
        content_lower = content.lower()
        
        if '教程' in content_lower or 'guide' in content_lower:
            return '教程'
        elif '架构' in content_lower or 'architecture' in content_lower:
            return '技术'
        elif '概念' in content_lower or 'concept' in content_lower:
            return '概念'
        else:
            return '其他'
    
    def _generate_toc(self, categories: Dict) -> str:
        """生成目录"""
        toc = []
        toc.append("# 知识库目录\n")
        toc.append(f"> 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        toc.append("")
        
        for category, docs in sorted(categories.items()):
            if docs:
                toc.append(f"## {category}\n")
                for doc in sorted(docs):
                    toc.append(f"- [{doc}]({doc}.md)")
                toc.append("")
        
        return "\n".join(toc)


def main():
    """主函数 - 测试"""
    print("=" * 60)
    print("🎯 太一知识图谱智能体 v1.0")
    print("基于 LLM Wiki + Graphify + Claude-Obsidian 蒸馏融合")
    print("=" * 60)
    
    agent = KnowledgeGraphAgent()
    
    # 测试 1: 构建知识图谱
    print("\n" + "=" * 60)
    print("测试 1: 构建知识图谱")
    print("=" * 60)
    
    graph = agent.build_graph('./documents')
    
    print(f"\n📊 图谱统计:")
    print(f"  文档数：{graph['document_count']}")
    print(f"  实体数：{graph['entity_count']}")
    print(f"  关系数：{graph['relation_count']}")
    
    # 测试 2: 查询知识
    print("\n" + "=" * 60)
    print("测试 2: 查询知识")
    print("=" * 60)
    
    result = agent.query("什么是 RAG?")
    print(f"\n问题：{result['question']}")
    print(f"\n答案:\n{result['answer']}")
    
    # 测试 3: 整理文档
    print("\n" + "=" * 60)
    print("测试 3: 整理文档")
    print("=" * 60)
    
    organize_result = agent.organize('./documents')
    print(f"\n📁 整理结果:")
    print(f"  文档总数：{organize_result['document_count']}")
    print(f"  分类统计：{organize_result['categories']}")
    
    print("\n" + "=" * 60)
    print("✅ 知识图谱智能体测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
