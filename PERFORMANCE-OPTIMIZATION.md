# 太一性能优化清单

> 创建：2026-03-28 22:24
> 目标：响应时间 <1 秒

---

## 🐌 慢的原因

1. **Session Startup 读 16 个文件** - 宪法 + 记忆 + 配置
2. **定时任务残留** - 多个 Python 进程占用资源
3. **context 过大** - >80K 时加载 residual.md

---

## 🚀 优化方案

### 1. 精简 Startup (立即执行)

**原**: 16 个文件全读
**新**: 只读核心 5 个

```
必读 (5 个):
1. SOUL.md
2. USER.md
3. memory/core.md
4. memory/2026-03-28.md
5. HEARTBEAT.md

可选 (按需):
- 宪法文件 (仅首次)
- MEMORY.md (仅主 session)
- residual.md (仅 context>80K)
```

---

### 2. 清理残留进程 (已执行)

```bash
# 清理定时任务残留
pkill -f "weather-lite.py"
pkill -f "whale_tracker.py"
pkill -f "strategy_v21.py"
```

---

### 3. 修复代码警告 (已执行)

```python
# 旧代码 (弃用)
datetime.utcnow()

# 新代码
datetime.now(datetime.timezone.utc)
```

---

### 4. context 压缩

**当前**: 待检查
**目标**: <50K

```bash
# 检查 context 大小
wc -c ~/.openclaw/workspace/memory/core.md
```

---

## 📊 性能指标

| 指标 | 当前 | 目标 | 状态 |
|------|------|------|------|
| 首次响应 | ~3 秒 | <1 秒 | 🟡 |
| Startup 文件数 | 16 个 | 5 个 | 🟡 |
| 残留进程 | 多个 | 0 | ✅ |
| context 大小 | 待检查 | <50K | 🟡 |

---

*创建时间：2026-03-28 22:24*
*太一 AGI · 性能优化*
