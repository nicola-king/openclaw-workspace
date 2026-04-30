# Hermes Learning Loop - 使用指南

> 快速开始：3 分钟上手自进化学习循环

---

## 🚀 快速开始

### 1. 重建索引 (首次使用)

```bash
cd /home/nicola/.openclaw/workspace/skills/hermes-learning-loop/search
python3 fts5_index.py rebuild
```

### 2. 测试搜索

```bash
# 关键词搜索
python3 memory_search.py

# 搜索特定内容
python3 -c "from memory_search import MemorySearch; s = MemorySearch(); print(s.search('Hermes'))"
```

### 3. 运行自动触发器

```bash
cd /home/nicola/.openclaw/workspace/skills/hermes-learning-loop/loop
python3 auto_trigger.py
```

---

## 📋 API 使用

### 搜索 API

```python
from skills.hermes_learning_loop.search.memory_search import MemorySearch

searcher = MemorySearch()

# 关键词搜索
results = searcher.search("知几-E 策略", limit=10)

# 技能搜索
skills = searcher.search_skills("交易", limit=5)

# 宪法搜索
constitution = searcher.search_constitution("负熵", limit=5)

# 时间范围搜索
results = searcher.search_by_date(
    query="预算",
    start="2026-04-01",
    end="2026-04-08"
)

# 标签过滤
results = searcher.search_by_tag(
    query="技能",
    tags=["[能力涌现]", "[决策]"]
)
```

### 技能创建 API

```python
from skills.hermes_learning_loop.loop.skill_creator import SkillCreator

creator = SkillCreator()

# 检查重复任务
proposal = creator.check_task_repetition(task_history)

# 创建技能
result = creator.create_skill_from_proposal(proposal, approved=True)
```

### Nudge 管理 API

```python
from skills.hermes_learning_loop.loop.nudge_manager import NudgeManager

manager = NudgeManager()

# 创建 Nudge
nudge = manager.create_nudge(
    content="重要洞察内容",
    nudge_type="[洞察]",
    target="core",
    priority="P1"
)

# 处理 Nudge
result = manager.process_nudge(nudge)

# 快捷持久化
result = manager.persist(
    content="内容",
    type="[洞察]",
    target="memory/core.md"
)
```

### 自动触发器 API

```python
from skills.hermes_learning_loop.loop.auto_trigger import AutoTrigger

trigger = AutoTrigger()

# 运行自动触发器
results = trigger.run()

# 检查结果
print(f"技能创建：{len(results['skill_creations'])}")
print(f"Nudge 执行：{len(results['nudges'])}")
```

---

## ⚙️ 配置

### 索引配置

```python
# 自定义数据库路径
from fts5_index import FTS5Index
indexer = FTS5Index(db_path="/path/to/custom.db")
```

### 触发器配置

```python
# 自定义触发条件
TRIGGER_CONFIG = {
    "repetition_threshold": 3,  # 重复次数阈值
    "session_timeout_minutes": 30,  # 会话超时
    "daily_nudge_time": "23:30"  # 每日 Nudge 时间
}
```

---

## 📊 监控

### 查看索引统计

```bash
python3 -c "from fts5_index import FTS5Index; i = FTS5Index(); print(i.get_stats())"
```

### 查看触发日志

```bash
cat /home/nicola/.openclaw/workspace/skills/hermes-learning-loop/trigger_log.json
```

### 查看 Nudge 历史

```bash
python3 -c "from nudge_manager import NudgeManager; m = NudgeManager(); print(m.get_stats())"
```

---

## 🔧 故障排查

### 问题 1: 索引为空

**解决**:
```bash
# 重建索引
python3 fts5_index.py rebuild
```

### 问题 2: 搜索无结果

**检查**:
1. 索引是否已重建
2. 搜索词是否正确
3. 内容是否已索引

### 问题 3: 触发器未触发

**检查**:
1. 任务历史是否满足条件
2. 触发日志是否有记录
3. 权限是否正确

---

## 📚 相关文档

- [SKILL.md](SKILL.md) - 完整技能文档
- [DIALECTIC-USER-MODEL.md](../../../constitution/directives/DIALECTIC-USER-MODEL.md) - 辩证用户模型
- [SEMANTIC-SEARCH.md](../../../constitution/directives/SEMANTIC-SEARCH.md) - 语义搜索协议

---

*创建：2026-04-08 23:30 | 太一 AGI*
