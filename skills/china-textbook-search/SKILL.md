---
skill: china-textbook-search
version: 1.0.0
author: 太一 AGI
created: 2026-04-06
status: active
tags: ['教材，检索，知识图谱，学习路径，人教版']
category: data
---



# ChinaTextbook 教材检索 Skill

> 人教版教材 (小学→大学) 智能检索系统

---

## 📊 功能概述

处理 42GB 人教版教材 PDF:
- 文件系统检索
- PDF 内容检索
- 知识图谱构建
- 学习路径生成
- 权威引用生成

---

## 🛠️ 技术栈

| 组件 | 用途 | 状态 |
|------|------|------|
| PyPDF2 | PDF 解析 | ✅ 可用 |
| ChromaDB | 向量检索 | ✅ 已安装 |
| jieba | 中文分词 | ✅ 可用 |
| networkx | 知识图谱 | ✅ 可用 |

---

## 🔧 核心功能

### 1. 文件系统检索
```python
from textbook_search import TextbookFinder

finder = TextbookFinder(base_path="/tmp/ChinaTextbook")

# 按关键词搜索
results = finder.search(
    keyword="人工智能",
    subject="信息技术",
    grade="高中"
)

# 输出：[pdf_path1, pdf_path2, ...]
```

### 2. PDF 内容检索
```python
from textbook_search import PDFSearcher

searcher = PDFSearcher()

# 搜索 PDF 内容
matches = searcher.search_content(
    pdf_path="高中/信息技术/人工智能基础.pdf",
    keyword="机器学习",
    context_window=200  # 字符
)

# 输出：[{"page": 10, "text": "...", "position": 1234}, ...]
```

### 3. 向量检索 (语义搜索)
```python
from textbook_search import VectorSearcher

searcher = VectorSearcher()

# 构建向量索引
await searcher.build_index(
    textbook_dir="/tmp/ChinaTextbook",
    embedding_model="bge-large-zh"
)

# 语义搜索
results = await searcher.semantic_search(
    query="如何学习编程",
    top_k=10
)

# 输出：[{"text": "...", "score": 0.92, "source": "高中/信息技术/..."}, ...]
```

### 4. 知识图谱构建
```python
from textbook_search import KnowledgeGraphBuilder

builder = KnowledgeGraphBuilder()

# 构建知识图谱
graph = await builder.build(
    textbook_dir="/tmp/ChinaTextbook",
    extract_relations=True
)

# 查询知识点关联
related = graph.query_related("函数", depth=2)
# 输出：["变量", "映射", "导数", "积分", ...]
```

### 5. 学习路径生成
```python
from textbook_search import LearningPathGenerator

generator = LearningPathGenerator()

# 生成学习路径
path = await generator.generate(
    goal="学习 Python 编程",
    start_grade="初中",
    end_grade="大学",
    include_exercises=True
)

# 输出：
# {
#   "stages": [
#     {"grade": "初中", "topics": ["基础语法", "循环"], "textbooks": [...]},
#     {"grade": "高中", "topics": ["函数", "面向对象"], "textbooks": [...]},
#     {"grade": "大学", "topics": ["数据结构", "算法"], "textbooks": [...]}
#   ]
# }
```

### 6. 权威引用生成
```python
from textbook_search import CitationGenerator

generator = CitationGenerator()

# 生成引用
citation = generator.generate_citation(
    textbook="高中/语文/必修三.pdf",
    page=45,
    quote="人工智能是未来科技的重要方向"
)

# 输出：
# "人教版高中语文必修三，第 45 页：'人工智能是未来科技的重要方向'"
```

---

## 📋 使用示例

### 场景 1: 山木 Bot 内容创作引用
```python
from textbook_search import search_by_topic, get_citation

# 搜索相关教材
results = search_by_topic("量子力学", grade="高中")

# 生成引用
citations = [get_citation(pdf) for pdf in results[:5]]

# 创作带引用的内容
content = f"""
# 量子力学简介

## 权威来源
{format_citations(citations)}

## 核心概念
...
"""
```

### 场景 2: 素问 Bot 学习路径
```python
from textbook_search import generate_learning_path

# 生成系统化学习路径
path = generate_learning_path(
    goal="成为数据科学家",
    start_grade="高中",
    end_grade="大学"
)

# 输出完整学习路线
print(path["stages"])
```

### 场景 3: 罔两 Bot 知识图谱
```python
from textbook_search import build_knowledge_graph

# 构建全学科知识图谱
graph = build_knowledge_graph()

# 分析知识点覆盖率
coverage = graph.analyze_coverage("机器学习")
print(f"覆盖教材：{coverage['textbook_count']}")
print(f"相关知识点：{coverage['concept_count']}")
```

---

## 🎯 Bot 集成

### 山木 Bot - 内容创作
```python
async def shanmu_create_content(topic):
    results = search_by_topic(topic)
    citations = [get_citation(pdf) for pdf in results]
    
    content = generate_article(topic, citations)
    return content
```

### 素问 Bot - 学习路径
```python
async def suwen_generate_path(goal):
    path = generate_learning_path(goal)
    return path
```

### 罔两 Bot - 知识图谱
```python
async def wangliang_build_graph():
    graph = build_knowledge_graph()
    return graph
```

---

## 🔗 集成文档

- 检索脚本：`integrations/china-textbook/textbook_search.py`
- 分析报告：`integrations/china-textbook/analysis-report.md`
- 仓库地址：https://github.com/TapXWorld/ChinaTextbook

---

## 📝 待办事项

- [ ] 仓库克隆完成 (42GB)
- [ ] 构建 PDF 索引
- [ ] 向量检索测试
- [ ] 知识图谱 Demo

---

*创建时间：2026-04-06 01:00 | 太一 AGI*
