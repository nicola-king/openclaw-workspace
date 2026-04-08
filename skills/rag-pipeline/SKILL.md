---
name: rag-pipeline
version: 1.0.0
description: rag-pipeline skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# RAG Pipeline Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 罔两
> **状态**: ✅ 已激活 | **优先级**: P4-03

---

## 📋 功能概述

提供 RAG（检索增强生成）pipeline 能力，支持文档检索+LLM 生成。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `rag ingest` | 文档入库 | `rag ingest --files *.pdf --collection docs` |
| `rag query` | RAG 查询 | `rag query --question "什么是 AGI" --top-k 3` |
| `rag chunk` | 文档分块 | `rag chunk --file doc.pdf --chunk-size 500` |
| `rag embed` | 向量化 | `rag embed --text "Hello" --model text-embedding-3` |
| `rag retrieve` | 检索 | `rag retrieve --query "AGI" --collection docs --top-k 5` |
| `rag generate` | 生成回答 | `rag generate --query "..." --context "..."` |

---

## 📝 使用示例

### 示例 1: 文档入库

```bash
# 太一，把这些 PDF 文档加入 RAG 系统
rag ingest --files ./docs/*.pdf --collection knowledge --chunk-size 500
```

### 示例 2: RAG 查询

```bash
# 太一，查询知识库：太一的架构是什么？
rag query --question "太一的架构是什么" --collection knowledge --top-k 5
```

**输出**:
```
🔍 检索到 5 个相关片段:
1. [constitution/CONST-ROUTER.md] 太一采用三层架构...
2. [SOUL.md] 我是太一，AGI 执行总管...
3. [MEMORY.md] 多 Bot 协作：太一 +7 专业 Bot...

🤖 回答:
太一采用三层架构设计：
1. 核心层：SOUL.md 身份锚点
2. 宪法层：8 大宪法文件
3. 技能层：43+ 工具 Skills
...
```

---

## 🔄 Pipeline 流程

```
文档 → 分块 → 向量化 → 存储 → 检索 → 生成
       ↓        ↓        ↓      ↓      ↓
     Chunk   Embed   Vector  Search  LLM
```

---

*创建时间：2026-04-03 09:34 | 罔两 | 太一 AGI v5.0*
