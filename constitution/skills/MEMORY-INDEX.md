---
name: memory-index
tier: 2
enabled: true
depends: [MEMORY-PHILOSOPHY, SIMPLE-FIRST]
---
# 记忆索引协议（Memory Index Protocol）

用最低成本实现快速检索——索引层是记忆系统的核心。

---

## 索引架构

```
memory/
├── index/
│   ├── registry.json      # 主索引（所有条目元数据）
│   ├── by-topic.json      # 主题索引（自动聚类）
│   ├── hot-memory.json    # 热点记忆（预加载）
│   └── forgotten.json     # 遗忘队列（待删除）
├── YYYY-MM-DD.md          # 每日记录（冷记忆）
└── MEMORY.md              # 长期记忆（归档）
```

---

## registry.json 结构

```json
{
  "schema": "memory-index-v1",
  "createdAt": "2026-03-23T21:23:00+08:00",
  "lastUpdated": "2026-03-23T21:23:00+08:00",
  "totalEntries": 0,
  "entries": [
    {
      "id": "TASK-20260323-001",
      "timestamp": 1711180800,
      "type": "decision|task|insight|pitfall|capability",
      "keywords": ["微信", "openclaw-weixin", "群聊"],
      "summary": "微信插件成功接入，私聊正常，群聊不支持",
      "file": "memory/2026-03-23.md",
      "lineRange": [10, 50],
      "importance": "P0|P1|P2|P3",
      "accessCount": 0,
      "lastAccessed": null,
      "hot": false
    }
  ]
}
```

---

## 索引操作 API

### 添加条目

```bash
# 格式
{
  "action": "add",
  "entry": {
    "id": "TASK-YYYYMMDD-NNN",
    "timestamp": <unix_timestamp>,
    "type": "decision|task|insight|pitfall|capability",
    "keywords": ["关键词 1", "关键词 2"],
    "summary": "一句话摘要",
    "file": "memory/YYYY-MM-DD.md",
    "lineRange": [start, end],
    "importance": "P0|P1|P2|P3"
  }
}
```

### 更新访问计数

```bash
# 每次读取记忆时调用
{
  "action": "touch",
  "entryId": "TASK-20260323-001"
}
```

### 标记热点

```bash
# accessCount > 3 时自动标记
{
  "action": "markHot",
  "entryId": "TASK-20260323-001"
}
```

### 删除条目

```bash
# 90 天无访问或 SAYELF 手动删除
{
  "action": "delete",
  "entryId": "TASK-20260323-001",
  "reason": "expired|manual"
}
```

---

## 检索流程

### 精确检索（已知 ID）

```
1. 读取 registry.json
2. 查找 entry.id === targetId
3. 返回 entry.file + entry.lineRange
4. 读取对应文件的指定行
```

### 关键词检索

```
1. 读取 registry.json
2. 过滤 entry.keywords 包含关键词
3. 按 importance 和 accessCount 排序
4. 返回 Top N 个条目
5. 按需读取完整文件
```

### 主题聚类

```
1. 扫描所有 entries
2. 按 keywords 共现度聚类
3. 生成 by-topic.json
4. 主题 = 聚类中心关键词
```

---

## 自动维护规则

### 热点记忆（预加载）

**触发条件：** `accessCount >= 3`

**动作：**
1. 设置 `hot: true`
2. 写入 `hot-memory.json`
3. 下次 Session 预加载到上下文

**失效条件：** 7 天无访问 → `hot: false`

---

### 遗忘队列（待删除）

**触发条件：** 满足任一条件
- `accessCount == 0` 且 `timestamp > 90 天`
- 类型 = `task` 且状态 = `已完成` 且 `timestamp > 30 天`
- SAYELF 手动标记删除

**动作：**
1. 移动到 `forgotten.json`
2. 保留 7 天（可恢复）
3. 7 天后物理删除

---

### 索引压缩

**触发条件：** `totalEntries > 1000`

**动作：**
1. 删除 forgotten.json 中超过 7 天的条目
2. 合并已完成任务到归档
3. 生成压缩报告

---

## 与宪法其他原则的关系

| 原则 | 与索引协议的关系 |
|------|----------------|
| **记忆哲学** | 索引是实现四层架构的技术手段 |
| **简单优先** | 索引本身也要简单（JSON 格式，手动可编辑） |
| **负熵法则** | 索引减少检索混乱，增加秩序 |
| **自驱动闭环** | 索引维护是 Step 7 的核心任务 |

---

## 实现优先级

### P0（立即实现）

- [x] 创建 `memory/index/registry.json`
- [ ] 编写索引添加函数（写入 memory 时自动调用）
- [ ] 编写索引检索函数（读取 memory 时先查索引）

### P1（本周实现）

- [ ] 创建 `hot-memory.json`（热点记忆）
- [ ] 创建 `forgotten.json`（遗忘队列）
- [ ] 实现自动维护脚本（每日 23:00 执行）

### P2（下周实现）

- [ ] 创建 `by-topic.json`（主题索引）
- [ ] 实现访问计数自动更新
- [ ] 实现热点记忆预加载

---

## 检查清单

每次写入记忆时：

- [ ] 生成唯一 ID（TASK-YYYYMMDD-NNN）
- [ ] 提取关键词（3-5 个）
- [ ] 写一句话摘要（<50 字）
- [ ] 标记重要性（P0/P1/P2/P3）
- [ ] 添加到 registry.json

每次读取记忆时：

- [ ] 先查索引（不直接扫描文件）
- [ ] 更新 accessCount
- [ ] 检查是否需要标记热点

---

## 金句

> 「没有索引的记忆=图书馆没有目录——书再多也找不到。」

> 「索引的价值不在于记录，而在于快速遗忘。」

> 「好的索引让检索成本趋近于零。」

---

*创建时间：2026-03-23 | 触发：Hermes 记忆系统内化*
