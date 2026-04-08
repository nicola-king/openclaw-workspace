---
name: vector-db
version: 1.0.0
description: vector-db skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Vector Database Skill

> **版本**: 1.0.0 | **创建时间**: 2026-04-03 | **负责 Bot**: 罔两
> **状态**: ✅ 已激活 | **优先级**: P4-02

---

## 📋 功能概述

提供向量数据库操作能力，支持 Chroma/Weaviate/Pinecone 等主流向量库。

---

## 🛠️ 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `vectordb connect` | 连接数据库 | `vectordb connect --type chroma --path ./db` |
| `vectordb create` | 创建集合 | `vectordb create --name documents` |
| `vectordb insert` | 插入向量 | `vectordb insert --collection docs --vectors [...] --metadata {...}` |
| `vectordb search` | 相似搜索 | `vectordb search --collection docs --query "text" --top-k 5` |
| `vectordb delete` | 删除文档 | `vectordb delete --collection docs --ids [...]` |
| `vectordb list` | 列出集合 | `vectordb list` |

---

## 📝 使用示例

### 示例 1: 创建向量集合

```bash
# 太一，创建文档向量集合
vectordb create --name documents --dimension 1536 --metric cosine
```

### 示例 2: 插入向量

```bash
# 太一，插入文档向量
vectordb insert --collection documents --vectors [[0.1, 0.2, ...]] --metadata '[{"text": "Hello", "source": "doc1"}]'
```

### 示例 3: 相似搜索

```bash
# 太一，搜索最相似的文档
vectordb search --collection documents --query "什么是 AGI" --top-k 5
```

---

## 🔌 支持数据库

| 数据库 | 类型 | 适用场景 |
|--------|------|---------|
| Chroma | 本地 | 开发/测试 |
| Weaviate | 本地/云 | 生产 |
| Pinecone | 云 | 大规模 |
| Qdrant | 本地/云 | 高性能 |
| Milvus | 本地/云 | 企业级 |

---

*创建时间：2026-04-03 09:33 | 罔两 | 太一 AGI v5.0*
