# 🧩 太一技能库 - 共享模块

> **创建时间**: 2026-04-07 00:05  
> **状态**: ✅ 激活  
> **用途**: 所有技能共享的底层模块

---

## 📁 模块结构

```
shared/
├── __init__.py
├── database.py      # 共享数据库连接
├── cache.py         # 共享缓存层
├── config.py        # 统一配置中心
└── event_bus.py     # 事件总线
```

---

## 🔌 使用方式

```python
from skills.shared import SharedDatabase, SharedCache, SharedConfig, EventBus

# 数据库
db = SharedDatabase.get_instance()
data = db.query("SELECT * FROM tasks WHERE status='pending'")

# 缓存
cache = SharedCache.get_instance()
cache.set('key', 'value', ttl=3600)
value = cache.get('key')

# 配置
config = SharedConfig.get_instance()
api_key = config.get('gemini.api_key')

# 事件总线
event_bus = EventBus.get_instance()
event_bus.publish('task.completed', {'task_id': 123})
```

---

*维护：太一 AGI | 共享层 v1.0*
