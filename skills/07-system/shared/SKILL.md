# shared - 太一共享层

> 太一系统的核心共享模块，提供数据库、缓存、事件总线、配置管理能力。

---

## 📦 模块组成

| 模块 | 文件 | 职责 |
|------|------|------|
| **配置管理** | `config.py` | 统一配置中心，支持环境变量/JSON 文件/动态重载 |
| **数据库** | `database.py` | SQLite 连接池，事务支持，CRUD 封装 |
| **缓存** | `cache.py` | 内存缓存（LRU），TTL 过期，缓存装饰器 |
| **事件总线** | `event_bus.py` | 发布/订阅模式，异步事件处理，优先级队列 |

---

## 🚀 快速开始

### 导入模块

```python
from skills.shared import config, db, cache, bus
```

### 初始化

```python
import asyncio
from skills.shared import db, cache, bus

async def init():
    # 初始化数据库
    await db.connect()
    
    # 初始化缓存
    await cache.initialize()
    
    # 启动事件总线
    await bus.start(workers=4)
```

---

## 📖 使用示例

### 1. 配置管理 (config.py)

```python
from skills.shared import config

# 获取配置
db_host = config.get("database.host")
cache_ttl = config.get("cache.ttl_default")
debug = config.get("system.debug")

# 动态设置
config.set("custom.key", "custom_value")

# 重新加载
config.reload()

# 保存配置
config.save_to_file()
```

**环境变量覆盖：**
```bash
export TAIYI_DB_HOST=192.168.1.100
export TAIYI_CACHE_TTL=7200
export TAIYI_DEBUG=true
```

---

### 2. 数据库操作 (database.py)

```python
from skills.shared import db

# 连接数据库
await db.connect()

# 插入
row_id = await db.insert("users", {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
})

# 查询
result = await db.fetch("SELECT * FROM users WHERE age > ?", (18,))
for row in result.to_dicts():
    print(row["name"])

# 单条查询
user = await db.fetch_one("SELECT * FROM users WHERE id = ?", (1,))

# 单个值
count = await db.fetch_scalar("SELECT COUNT(*) FROM users")

# 更新
affected = await db.update(
    "users",
    {"age": 26},
    "id = ?",
    (1,)
)

# 删除
deleted = await db.delete("users", "id = ?", (1,))

# 事务
async with db.transaction() as tx:
    tx.execute("INSERT INTO logs (msg) VALUES (?)", ("start",))
    tx.execute("INSERT INTO logs (msg) VALUES (?)", ("end",))
# 自动 commit，异常时自动 rollback

# 批量插入
rows = [
    {"name": f"user{i}", "email": f"user{i}@example.com"}
    for i in range(100)
]
await db.batch_insert("users", rows)

# 关闭连接
await db.close()
```

---

### 3. 缓存系统 (cache.py)

```python
from skills.shared import cache

# 初始化
await cache.initialize()

# 设置缓存
await cache.set("user:123", {"name": "Alice", "age": 25})
await cache.set("temp:key", "value", ttl=60)  # 60 秒过期

# 获取缓存
user = await cache.get("user:123")

# 检查存在
exists = await cache.exists("user:123")

# 删除
await cache.delete("user:123")

# 清空
await cache.clear()

# 缓存装饰器
@cache.cached(ttl=300, key_prefix="api")
async def fetch_user_data(user_id):
    # 这个函数的结果会被缓存 5 分钟
    return await expensive_api_call(user_id)

# get_or_set 模式
data = await cache.get_or_set(
    "expensive:computation",
    lambda: compute_expensive_value(),
    ttl=3600
)

# 批量操作
await cache.mset({"key1": "val1", "key2": "val2"})
result = await cache.mget(["key1", "key2"])

# 统计信息
stats = await cache.stats()
print(f"命中率：{stats['hit_rate']}")
```

---

### 4. 事件总线 (event_bus.py)

```python
from skills.shared import bus
from skills.shared.event_bus import EventPriority

# 启动事件总线
await bus.start(workers=4)

# 订阅事件（装饰器方式）
@bus.on("user.created")
async def on_user_created(event):
    print(f"新用户：{event.payload['name']}")

# 订阅事件（编程方式）
async def on_user_deleted(event):
    print(f"用户删除：{event.payload['id']}")

sub_id = await bus.subscribe("user.deleted", on_user_deleted)

# 通配符订阅
@bus.on("user.*", pattern=True)
async def on_any_user_event(event):
    print(f"用户事件：{event.event_type}")

# 带过滤器的订阅
@bus.on(
    "system.alert",
    filter_fn=lambda e: e.payload.get("level") == "critical"
)
async def on_critical_alert(event):
    print(f"严重告警：{event.payload['message']}")

# 发布事件
await bus.publish(
    "user.created",
    {"name": "Alice", "id": 123},
    priority=EventPriority.NORMAL,
    source="user_service"
)

# 高优先级事件
await bus.publish(
    "system.alert",
    {"level": "critical", "message": "CPU 过载"},
    priority=EventPriority.CRITICAL
)

# 取消订阅
await bus.unsubscribe(sub_id)

# 获取统计
stats = bus.stats()
print(f"已发布：{stats['published']}, 已处理：{stats['processed']}")

# 获取历史
history = await bus.get_history("user.created", limit=10)

# 停止事件总线
await bus.stop()
```

---

## 🔧 配置选项

### config.json 示例

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "database": "taiyi",
    "user": "taiyi",
    "password": "",
    "pool_size": 10
  },
  "cache": {
    "backend": "memory",
    "host": "localhost",
    "port": 6379,
    "ttl_default": 3600,
    "max_size": 10000
  },
  "event_bus": {
    "backend": "memory",
    "channel_prefix": "taiyi",
    "max_queue_size": 10000
  },
  "system": {
    "workspace": "/home/nicola/.openclaw/workspace",
    "log_level": "INFO",
    "debug": false
  }
}
```

---

## 📊 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    太一系统                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   config    │  │    cache    │  │  event_bus  │     │
│  │   配置中心   │  │   缓存层    │  │   事件总线   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│                 ┌────────▼────────┐                     │
│                 │    database     │                     │
│                 │    数据库层      │                     │
│                 └────────┬────────┘                     │
│                          │                              │
│                 ┌────────▼────────┐                     │
│                 │   SQLite/Redis  │                     │
│                 └─────────────────┘                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 设计原则

1. **单例模式** - 所有模块使用单例，确保全局状态一致
2. **异步优先** - 所有 I/O 操作使用 async/await
3. **零外部依赖** - 仅使用 Python 标准库
4. **类型提示** - 完整的类型注解，便于 IDE 支持
5. **文档完善** - 每个函数都有 docstring 和使用示例

---

## 🧪 测试

每个模块都包含自测试代码：

```bash
cd /home/nicola/.openclaw/workspace/skills/shared
python3 config.py
python3 database.py
python3 cache.py
python3 event_bus.py
```

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-07 | 初始版本，包含 config/database/cache/event_bus |

---

**维护者**: 太一  
**状态**: ✅ 生产就绪
