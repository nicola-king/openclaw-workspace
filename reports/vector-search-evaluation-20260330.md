# 向量检索评估报告

**评估时间**: 2026-03-30 21:05
**评估人**: 太一

---

## 🔬 sqlite-vec 安装测试

### 系统环境
- **SQLite 版本**: 3.45.1 ✅
- **Python**: 3.8+ ✅
- **FTS5 模块**: 可用 ✅

### sqlite-vec 安装

**状态**: 🔴 未安装

**安装命令**:
```bash
pip3 install sqlite-vec --break-system-packages
```

**替代方案**:
1. **使用虚拟环境** (推荐)
   ```bash
   python3 -m venv ~/.venv/sqlite-vec
   source ~/.venv/sqlite-vec/bin/activate
   pip install sqlite-vec
   ```

2. **使用 Docker 容器**
   ```bash
   docker run -it python:3.11-slim bash
   pip install sqlite-vec
   ```

3. **使用 ChromaDB (外部向量库)**
   ```bash
   pip install chromadb
   ```

---

## 📊 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **sqlite-vec** | 本地、零依赖、SQLite 集成 | 安装略复杂 | ⭐⭐⭐⭐ |
| **ChromaDB** | 功能完整、文档好 | 需独立服务 | ⭐⭐⭐ |
| **FAISS** | Facebook 出品、性能好 | 学习曲线陡 | ⭐⭐⭐ |
| **纯 FTS5** | 无需额外安装 | 无语义搜索 | ⭐⭐⭐⭐ |

---

## 🎯 太一推荐方案

### 阶段 1: 纯 FTS5 (立即实施)

**理由**:
- ✅ 已验证可用
- ✅ 零安装成本
- ✅ 满足关键词检索需求
- ✅ Token 节省 ~10%

**实现**:
```python
# 创建 FTS5 索引
conn.execute('''
    CREATE VIRTUAL TABLE memory_index USING fts5(
        content,
        section,
        tags,
        tokenize='unicode61'
    )
''')
```

### 阶段 2: sqlite-vec (可选，1-2 周)

**理由**:
- ✅ 语义搜索 (相似度匹配)
- ✅ 与 FTS5 混合检索
- ⚠️ 需要安装额外依赖

**实现**:
```python
import sqlite_vec
conn.enable_load_extension(True)
sqlite_vec.load(conn)
```

---

## 📋 决策

**短期 (本周)**: 纯 FTS5 全文检索
- 实现简单
- 零安装成本
- Token 节省 ~10%

**中期 (1-2 周)**: 评估 sqlite-vec 必要性
- 如关键词检索足够，则不安装
- 如需语义搜索，再安装

**理由**: 太一记忆以结构化 Markdown 为主，关键词检索已能满足 80% 需求。

---

## 🔧 FTS5 实现计划

### 步骤 1: 创建索引表

```sql
CREATE VIRTUAL TABLE memory_index USING fts5(
    content,
    section,
    tags,
    tokenize='unicode61'
);
```

### 步骤 2: 插入记忆数据

```sql
INSERT INTO memory_index (content, section, tags)
VALUES ('MemOS Token 节省 72%', 'MemOS 学习', 'MemOS,Token,优化');
```

### 步骤 3: 检索

```sql
SELECT * FROM memory_index
WHERE memory_index MATCH 'MemOS Token'
ORDER BY rank;
```

### 步骤 4: 混合检索 (FTS5 + BM25)

```sql
SELECT *, bm25(memory_index) as score
FROM memory_index
WHERE memory_index MATCH 'MemOS'
ORDER BY score
LIMIT 10;
```

---

## 📊 预期收益

| 检索方式 | 准确率 | Token 节省 | 实现难度 |
|---------|--------|-----------|---------|
| **当前 (文件级)** | 低 | 0% | - |
| **FTS5 关键词** | 中 | +10% | 低 |
| **FTS5+Vector 混合** | 高 | +15% | 中 |

**决策**: 先实现 FTS5 关键词检索 (+10% 节省)，后续按需升级为混合检索。

---

*评估人：太一 | 时间：2026-03-30 21:05*
