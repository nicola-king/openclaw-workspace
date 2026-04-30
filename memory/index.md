# 太一记忆系统索引 (Index)

> 创建时间：2026-04-06 00:43 | 灵感：LLM Wiki

---

## 📚 核心记忆文件

| 文件 | 用途 | 加载策略 |
|------|------|---------|
| [`MEMORY.md`](../MEMORY.md) | 长期固化记忆 | 仅主 session 加载 |
| [`memory/core.md`](./core.md) | 核心记忆 (80%) | 每次 session 必读 |
| [`memory/residual.md`](./residual.md) | 残差细节 (20%) | context>80K 时加载 |
| [`memory/2026-04-06.md`](./2026-04-06.md) | 今日原始日志 | 恢复上下文 |

---

## 🗂️ 记忆分类

### 宪法系统
- [`constitution/CONST-ROUTER.md`](../constitution/CONST-ROUTER.md) - 宪法加载协议
- [`constitution/axiom/VALUE-FOUNDATION.md`](../constitution/axiom/VALUE-FOUNDATION.md) - 价值基石
- [`constitution/directives/NEGENTROPY.md`](../constitution/directives/NEGENTROPY.md) - 负熵法则
- [`constitution/directives/AGI-TIMELINE.md`](../constitution/directives/AGI-TIMELINE.md) - AGI 时间线
- [`constitution/directives/OBSERVER.md`](../constitution/directives/OBSERVER.md) - 观察者协议
- [`constitution/directives/SELF-LOOP.md`](../constitution/directives/SELF-LOOP.md) - 自驱动闭环
- [`constitution/directives/ASK-PROTOCOL.md`](../constitution/directives/ASK-PROTOCOL.md) - 追问协议
- [`constitution/skills/MODEL-ROUTING.md`](../constitution/skills/MODEL-ROUTING.md) - 模型调度

### Bot 协作
- [`constitution/COLLABORATION.md`](../constitution/COLLABORATION.md) - 多 Bot 协作
- [`constitution/extensions/DELEGATION.md`](../constitution/extensions/DELEGATION.md) - 任务委派
- [`constitution/directives/TURBOQUANT.md`](../constitution/directives/TURBOQUANT.md) - 智能分离

### 技能系统
- [`skills/`](../skills/) - 80+ Skills
  - [`skills/zhiji/`](../skills/zhiji/) - 知几 (量化交易)
  - [`skills/shanmu/`](../skills/shanmu/) - 山木 (内容创作)
  - [`skills/suwen/`](../skills/suwen/) - 素问 (技术开发)
  - [`skills/wangliang/`](../skills/wangliang/) - 罔两 (数据分析)
  - [`skills/paoding/`](../skills/paoding/) - 庖丁 (预算成本)
  - [`skills/yi/`](../skills/yi/) - 羿 (监控追踪)
  - [`skills/shoucangli/`](../skills/shoucangli/) - 守藏吏 (管家)

### 工作流
- [`constitution/workflows/`](../constitution/workflows/) - 工作流模板
  - `CONTENT-CREATION.md` - 内容创作
  - `TECH-DEVELOPMENT.md` - 技术开发
  - `QUANT-TRADING.md` - 量化交易
  - `DATA-COLLECTION.md` - 数据采集
  - `LEARNING-DISTILLATION.md` - 学习蒸馏

---

## 📊 记忆维护

### 每日流程
| 时间 | 任务 | 脚本 |
|------|------|------|
| **06:00** | 宪法学习 + 记忆提炼 | `daily-constitution.sh` |
| **23:00** | 日报生成 + 记忆归档 | `/opt/openclaw-report.sh` |

### 压缩策略
- **core.md >50K** → 提炼到 MEMORY.md
- **residual.md >20K** → 压缩/归档
- **每日日志** → 周末汇总

---

## 🔍 快速检索

### 搜索记忆
```bash
# 搜索关键词
grep -r "关键词" memory/

# 搜索宪法
grep -r "关键词" constitution/

# 搜索技能
grep -r "关键词" skills/
```

### 语义搜索
```python
from memory_search import search

results = search("任务保障", maxResults=5)
```

---

## 📋 更新日志

| 日期 | 更新 | 作者 |
|------|------|------|
| 2026-04-06 | 创建 index.md | 太一 AGI |

---

*最后更新：2026-04-06 00:43 | 太一 AGI*
