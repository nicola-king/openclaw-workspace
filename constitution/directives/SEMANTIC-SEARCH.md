# 语义搜索协议 (Semantic Search Protocol)

> 版本：v1.0 | 创建：2026-04-08  
> 灵感：Hermes Agent FTS5+LLM Search  
> 状态：✅ 激活 | 优先级：P1

---

## 🎯 核心原则

**记忆的价值在于可检索性**

传统文件存储的问题是：
- 关键词匹配不准确
- 跨文件检索困难
- 语义理解缺失
- 时间线追溯繁琐

语义搜索通过以下方式增强:
1. **FTS5 全文索引** - 快速关键词匹配
2. **LLM 语义理解** - 理解用户意图
3. **跨文件关联** - 自动链接相关内容
4. **时间线索引** - 按时间追溯演化

---

## 🏗️ 搜索架构

```
语义搜索系统
├── 索引层 (Indexing)
│   ├── FTS5 索引 (SQLite)
│   ├── 元数据索引 (标签/类型/日期)
│   └── 向量索引 (可选，语义嵌入)
│
├── 查询层 (Query)
│   ├── 关键词查询
│   ├── 语义查询
│   ├── 混合查询
│   └── 时间范围查询
│
└── 结果层 (Results)
    ├── 相关性排序
    ├── 摘要生成
    ├── 关联推荐
    └── 时间线展示
```

---

## 📋 索引策略

### FTS5 索引表

```sql
-- 记忆内容索引
CREATE VIRTUAL TABLE memory_index USING fts5(
    content,
    title,
    tags,
    type,
    date,
    file_path
);

-- 技能索引
CREATE VIRTUAL TABLE skill_index USING fts5(
    name,
    description,
    responsibilities,
    commands,
    tags
);

-- 对话索引
CREATE VIRTUAL TABLE conversation_index USING fts5(
    content,
    participants,
    date,
    session_id
);
```

### 元数据提取

```python
def extract_metadata(file_path: str) -> Dict:
    """从文件提取元数据"""
    content = read_file(file_path)
    
    # 提取标签
    tags = extract_tags(content)  # [决策] [任务] [洞察] 等
    
    # 提取类型
    doc_type = extract_type(content)  # memory/skill/constitution
    
    # 提取日期
    date = extract_date(content)
    
    # 提取标题
    title = extract_title(content)
    
    return {
        "content": content,
        "title": title,
        "tags": tags,
        "type": doc_type,
        "date": date,
        "file_path": file_path
    }
```

---

## 🔍 查询接口

### Python API

```python
from skills.hermes_learning_loop.search.memory_search import MemorySearch

searcher = MemorySearch()

# 1. 关键词搜索
results = searcher.search("知几-E 策略", limit=10)

# 2. 语义搜索
results = searcher.semantic_search("上次提到的套利方法")

# 3. 混合搜索 (关键词 + 语义)
results = searcher.hybrid_search(
    query="预算追踪",
    semantic_weight=0.3,  # 30% 语义 + 70% 关键词
    limit=10
)

# 4. 时间范围搜索
results = searcher.search_by_date(
    query="预算支出",
    start="2026-04-01",
    end="2026-04-08"
)

# 5. 标签过滤搜索
results = searcher.search_by_tag(
    query="技能",
    tags=["[能力涌现]", "[决策]"],
    limit=5
)

# 6. 跨文件关联搜索
results = searcher.search_with_relations(
    query="Hermes Agent",
    include_relations=True,  # 包含相关内容
    relation_depth=2  # 2 层关联
)
```

### CLI 命令

```bash
# 关键词搜索
hermes-search "知几-E 策略" --limit 10

# 语义搜索
hermes-search "上次提到的套利方法" --semantic

# 时间范围搜索
hermes-search "预算" --from 2026-04-01 --to 2026-04-08

# 标签过滤
hermes-search "技能" --tag "[能力涌现]" --tag "[决策]"

# 导出结果
hermes-search "Hermes" --export results.json
```

---

## 📊 搜索结果格式

### 标准格式

```markdown
📚 搜索结果："知几-E 策略" (找到 5 条)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [2026-04-06] 知几-E v40 部署
   标签：[决策] [能力涌现]
   文件：memory/2026-04-06.md:45
   相关性：95%
   
   摘要：部署知几-E v40 版本，新增风险控制模块...
   
   关键内容:
   - 部署时间：2026-04-06 14:00
   - 版本：v40
   - 新增功能：风险控制、回测优化
   
   [查看原文] [查看关联] [复制内容]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. [2026-04-05] 知几-E 策略回测
   标签：[任务]
   文件：memory/2026-04-05.md:23
   相关性：88%
   
   摘要：完成 v39 策略回测，夏普比率 2.3...
   
   [查看原文] [查看关联] [复制内容]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 相关搜索建议:
- "知几-E 回测"
- "知几-E 风险控制"
- "知几-E v40"
```

### 时间线视图

```bash
hermes-search "知几-E" --timeline

📅 知几-E 演化时间线

2026-04-01  知几-E v38 上线
            └─ 新增：链上数据监控

2026-04-03  知几-E v39 回测
            └─ 夏普比率：2.3

2026-04-06  知几-E v40 部署 ✅
            └─ 新增：风险控制模块

2026-04-08  知几-E 策略优化 (当前)
            └─ 进行中
```

---

## 🧠 LLM 增强

### 查询理解

```python
def understand_query(query: str) -> Dict:
    """
    使用 LLM 理解查询意图
    
    返回:
    {
        "intent": "search|compare|summarize|trace",
        "topics": ["知几-E", "策略"],
        "time_range": {"start": "2026-04-01", "end": "2026-04-08"},
        "expected_type": ["[决策]", "[任务]"],
        "semantic_query": "知几-E 交易策略的演化和回测结果"
    }
    """
    pass
```

### 摘要生成

```python
def generate_summary(results: List[Dict]) -> str:
    """
    使用 LLM 生成搜索结果摘要
    
    输入: 搜索结果列表
    输出: 综合摘要
    
    示例输出:
    "找到 5 条关于'知几-E 策略'的记录:
     - 4 月 1 日：v38 上线，新增链上监控
     - 4 月 3 日：v39 回测完成，夏普比率 2.3
     - 4 月 6 日：v40 部署，新增风险控制
     - 4 月 8 日：策略优化进行中
     
     演化趋势：从基础监控→回测优化→风险控制→持续优化"
    """
    pass
```

### 关联推荐

```python
def recommend_relations(query: str, results: List[Dict]) -> List[Dict]:
    """
    推荐相关内容
    
    基于:
    - 共同标签
    - 时间接近
    - 语义相似
    - 引用关系
    
    返回: 相关内容列表
    """
    pass
```

---

## 🔧 与太一体系集成

### 记忆架构增强

```yaml
原架构:
  - core.md (核心记忆)
  - residual.md (残差细节)
  - MEMORY.md (长期固化)
  - YYYY-MM-DD.md (原始日志)

增强:
  + memory_index.db (FTS5 索引)
  + skill_index.db (技能索引)
  + search_cache.json (搜索缓存)
```

### HEARTBEAT.md 增强

```markdown
## 🔍 搜索系统状态

| 索引 | 条目数 | 最后更新 |
|------|--------|---------|
| 记忆索引 | 1,234 | 2026-04-08 23:00 |
| 技能索引 | 94 | 2026-04-08 22:00 |
| 对话索引 | 5,678 | 实时 |

### 热门搜索 (本周)
1. "知几-E 策略" - 23 次
2. "Hermes Agent" - 15 次
3. "预算追踪" - 12 次
```

### 技能集成

```python
# 太一内置搜索能力
async def search_memory(query: str, **kwargs):
    """太一，搜索 XXX"""
    searcher = MemorySearch()
    results = searcher.search(query, **kwargs)
    return format_results(results)
```

---

## 📈 性能指标

| 指标 | 基线 | 目标 | 当前 |
|------|------|------|------|
| **搜索延迟** | N/A | <500ms | 🟡 待测试 |
| **召回率** | N/A | >85% | 🟡 待测试 |
| **准确率** | N/A | >80% | 🟡 待测试 |
| **索引更新** | N/A | <1s | 🟡 待测试 |

---

## ⚠️ 注意事项

### 隐私保护

- ✅ 仅索引用户授权的内容
- ❌ 不索引敏感信息 (密码/API 密钥等)
- ✅ 支持删除特定内容的索引

### 性能优化

- 使用缓存减少重复搜索
- 增量索引更新 (非全量重建)
- 异步索引构建

---

## 📚 参考资料

- [SQLite FTS5](https://www.sqlite.org/fts5.html)
- [Hermes Agent Search](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- [语义搜索最佳实践](https://www.semrush.com/blog/semantic-search/)

---

*创建：2026-04-08 23:30 | 太一 AGI | 灵感：Hermes Agent FTS5+LLM Search*
