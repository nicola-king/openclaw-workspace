# Semantic Search · 语义搜索

> 版本：v1.0 | 创建：2026-04-08 | 优先级：P0-02  
> 灵感：Hermes Agent FTS5+LLM Search | 状态：🟡 开发中

---

## 🎯 核心目标

**实现跨文件、跨会话的语义搜索，让记忆可检索**

```
自然语言查询 → FTS5 索引 → LLM 摘要 → 相关性排序 → 返回结果
```

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    语义搜索系统                          │
├─────────────────────────────────────────────────────────┤
│  查询层 (Query)                                          │
│  - 自然语言解析                                          │
│  - 关键词提取                                            │
│  - 意图识别                                              │
├─────────────────────────────────────────────────────────┤
│  索引层 (Index)                                          │
│  - FTS5 全文索引 (SQLite)                                │
│  - 元数据索引 (标签/日期/类型)                            │
│  - 向量索引 (可选，语义嵌入)                              │
├─────────────────────────────────────────────────────────┤
│  搜索层 (Search)                                         │
│  - 关键词匹配                                            │
│  - 语义相似度                                            │
│  - 混合搜索                                              │
├─────────────────────────────────────────────────────────┤
│  结果层 (Results)                                        │
│  - 相关性排序                                            │
│  - LLM 摘要生成                                          │
│  - 关联推荐                                              │
│  - 时间线展示                                            │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 索引策略

### FTS5 索引表设计

```sql
-- 记忆内容索引
CREATE VIRTUAL TABLE memory_index USING fts5(
    content,
    title,
    tags,
    type,
    date,
    file_path,
    tokenize='unicode61'
);

-- 技能索引
CREATE VIRTUAL TABLE skill_index USING fts5(
    name,
    description,
    responsibilities,
    commands,
    tags,
    file_path
);

-- 对话索引
CREATE VIRTUAL TABLE conversation_index USING fts5(
    content,
    participants,
    date,
    session_id,
    channel
);

-- 宪法索引
CREATE VIRTUAL TABLE constitution_index USING fts5(
    name,
    content,
    directives,
    priority,
    file_path
);
```

### 元数据表

```sql
-- 文件元数据
CREATE TABLE file_metadata (
    file_path TEXT PRIMARY KEY,
    file_type TEXT,  -- memory/skill/constitution/report
    created_at TEXT,
    updated_at TEXT,
    word_count INTEGER,
    tags TEXT  -- JSON array
);

-- 搜索历史
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY,
    query TEXT,
    timestamp TEXT,
    results_count INTEGER,
    clicked_file TEXT
);
```

---

## 🔍 搜索功能

### 搜索类型

| 类型 | 描述 | 示例 |
|------|------|------|
| **关键词搜索** | FTS5 全文匹配 | `hermes 技能` |
| **语义搜索** | 向量相似度 | 「自学习」→ 搜索 emergence/auto-skill |
| **混合搜索** | 关键词 + 语义 | `hermes + 自学习` |
| **时间范围** | 日期过滤 | `2026-04-01..2026-04-08` |
| **类型过滤** | 文件类型过滤 | `type:memory 太一` |
| **标签搜索** | 标签匹配 | `tag:P0 任务` |

### 搜索语法

```
# 基础搜索
hermes 技能              # 关键词匹配

# 字段过滤
type:memory 太一          # 仅搜索记忆
type:skill 交易           # 仅搜索技能
tag:P0 任务              # 按标签搜索

# 时间范围
2026-04-01..2026-04-08  # 日期范围
last:7d                 # 最近 7 天
last:30d                # 最近 30 天

# 布尔逻辑
hermes AND 技能          # 与
hermes OR 自动           # 或
hermes NOT 迁移          # 非

# 短语搜索
"自学习回路"             # 精确短语

# 通配符
自动*                   # 自动/自动化/自动生成
```

---

## 🧠 语义增强

### LLM 摘要生成

```python
def generate_summary(search_results, query):
    """为搜索结果生成 LLM 摘要"""
    prompt = f"""
    用户查询：{query}
    
    找到 {len(search_results)} 个相关文件：
    {format_results_for_llm(search_results)}
    
    请生成一个简洁的摘要（200 字以内），包括：
    1. 核心发现
    2. 关键文件推荐（前 3 个）
    3. 相关内容关联
    
    格式：Markdown
    """
    return llm.generate(prompt)
```

### 语义相似度

```python
def semantic_similarity(query, documents):
    """计算查询与文档的语义相似度"""
    # 方案 1: 使用嵌入模型
    query_embedding = embed(query)
    doc_embeddings = [embed(doc) for doc in documents]
    similarities = cosine_similarity(query_embedding, doc_embeddings)
    return similarities
    
    # 方案 2: 使用 LLM 零样本
    # 让 LLM 直接评分相关性 (0-1)
```

### 关联推荐

```python
def recommend_related(results, query):
    """推荐相关内容"""
    # 基于共现关系
    co_occurring_files = find_co_occurrence(results)
    
    # 基于时间邻近
    time_nearby = find_time_nearby(results, days=7)
    
    # 基于标签相似
    tag_similar = find_tag_similar(results)
    
    return {
        'co_occurring': co_occurring_files,
        'time_nearby': time_nearby,
        'tag_similar': tag_similar
    }
```

---

## 📊 搜索结果排序

### 相关性评分算法

```python
def relevance_score(doc, query):
    """计算文档相关性评分 (0-1)"""
    score = 0.0
    
    # FTS5 排名 (+0.4)
    score += 0.4 * normalize_fts5_rank(doc['fts5_rank'])
    
    # 关键词匹配度 (+0.2)
    score += 0.2 * keyword_match_ratio(doc, query)
    
    # 语义相似度 (+0.2)
    score += 0.2 * semantic_similarity(query, doc['content'])
    
    # 时间新鲜度 (+0.1)
    score += 0.1 * recency_score(doc['date'])
    
    # 文件类型权重 (+0.1)
    score += 0.1 * type_weight(doc['type'], query)
    
    return score

def rank_results(results, query):
    """对搜索结果排序"""
    for doc in results:
        doc['relevance'] = relevance_score(doc, query)
    return sorted(results, key=lambda x: x['relevance'], reverse=True)
```

### 类型权重

| 查询类型 | memory | skill | constitution | report |
|----------|--------|-------|--------------|--------|
| **任务/待办** | 1.0 | 0.5 | 0.3 | 0.8 |
| **技能/工具** | 0.5 | 1.0 | 0.3 | 0.5 |
| **规则/协议** | 0.3 | 0.5 | 1.0 | 0.3 |
| **报告/总结** | 0.8 | 0.5 | 0.3 | 1.0 |
| **通用查询** | 0.8 | 0.8 | 0.8 | 0.8 |

---

## 🎯 使用示例

### 示例 1: 关键词搜索

```
# 用户：搜索「hermes 技能」

太一执行：
1. FTS5 索引查询：hermes AND 技能
2. 找到 5 个文件
3. 生成摘要
4. 返回结果

结果：
📁 reports/2026-04-08-hermes-agent-analysis.md (相关性：0.92)
   Hermes Agent 功能分析，包含 10 个特殊功能...

📁 skills/auto-skill-generator/SKILL.md (相关性：0.85)
   灵感来自 Hermes 的自学习回路...

📁 reports/2026-04-08-taiyi-vs-hermes-comparison.md (相关性：0.83)
   太一与 Hermes 功能对比报告...
```

### 示例 2: 语义搜索

```
# 用户：「太一的自学习能力怎么实现的？」

太一执行：
1. 语义解析：自学习 = 自动技能生成/能力涌现/自进化
2. 搜索相关概念
3. 返回结果 + 摘要

结果：
📁 constitution/directives/EMERGENCE.md (相关性：0.89)
   涌现法则：Agent/Skills/太一自发秩序，非设计而是演化...

📁 skills/auto-skill-generator/SKILL.md (相关性：0.87)
   技能自动生成机制，从任务经验提取可复用模式...

📁 constitution/directives/SELF-EVOLUTION.md (相关性：0.82)
   自进化协议：太一自主进化框架...

💡 摘要：
太一的自学习通过「能力涌现机制」实现：
1. 检测重复任务 (≥3 次) → 自动提议新技能
2. 从复杂任务提取模式 → 生成技能草稿
3. SAYELF 确认 → 激活技能

当前状态：🟡 开发中 (P0-01)
```

### 示例 3: 时间范围搜索

```
# 用户：「上周关于交易的讨论」

太一执行：
1. 解析时间：last:7d
2. 解析主题：交易
3. 过滤搜索结果

结果：
📁 memory/2026-04-01.md (相关性：0.88)
   知几-E 策略讨论，GMGN 集成...

📁 skills/gmgn/SKILL.md (相关性：0.85)
   GMGN.AI 统一链上交易技能...
```

### 示例 4: 类型过滤

```
# 用户：type:skill 交易

结果：
📁 skills/gmgn/SKILL.md
   GMGN.AI 统一链上交易技能

📁 skills/trading/SKILL.md
   交易引擎 - 币安/Polymarket/TorchTrade

📁 skills/zhiji/SKILL.md
   知几 - 量化交易策略引擎
```

---

## 🔧 实现路线图

### Phase 1: 基础索引 (1-2 天)

| 任务 | 状态 | 说明 |
|------|------|------|
| **SQLite FTS5 索引** | 🟡 待开发 | 创建 4 个索引表 |
| **索引构建器** | 🟡 待开发 | 遍历 memory/skills/constitution |
| **增量更新** | 🟡 待开发 | 文件变更时更新索引 |

### Phase 2: 搜索功能 (1 天)

| 任务 | 状态 | 说明 |
|------|------|------|
| **关键词搜索** | 🟡 待开发 | FTS5 查询 |
| **语法解析** | 🟡 待开发 | type:/tag:/时间范围 |
| **结果排序** | 🟡 待开发 | 相关性评分 |

### Phase 3: 语义增强 (1 天)

| 任务 | 状态 | 说明 |
|------|------|------|
| **LLM 摘要** | 🟡 待开发 | 为结果生成摘要 |
| **语义相似度** | 🟡 待开发 | 嵌入模型或 LLM |
| **关联推荐** | 🟡 待开发 | 相关内容推荐 |

---

## 📋 文件结构

```
skills/semantic-search/
├── SKILL.md              # 技能定义
├── indexer.py            # 索引构建器
├── searcher.py           # 搜索执行器
├── ranker.py             # 结果排序器
├── summarizer.py         # LLM 摘要生成
├── db/
│   └── semantic_index.db # SQLite 数据库
└── tests/
    ├── test_indexer.py
    └── test_searcher.py
```

---

## 🎯 成功标准

| 指标 | 目标值 | 时间 |
|------|--------|------|
| **索引覆盖率** | 100% | 1 周 |
| **搜索响应时间** | <1 秒 | 1 周 |
| **相关性准确率** | ≥80% | 2 周 |
| **SAYELF 满意度** | ≥4/5 | 2 周 |

---

## 🔗 与现有系统集成

### 记忆系统

```
memory/ 目录 → 索引构建器 → FTS5 索引
```

### HEARTBEAT.md

```
心跳检查 → 索引更新 → 确保最新
```

### 技能系统

```
skills/ 目录 → 索引构建器 → 技能搜索
```

---

*记忆的价值在于可检索性。让太一记住一切，并随时可回忆。*
