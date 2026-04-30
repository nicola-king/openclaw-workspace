# 🔍 搜索 Bot 统一归属方案

> **分析时间**: 2026-04-19 10:20  
> **目标**: 整合所有搜索相关 Bot/Skill 到太一 AI 搜索 Skill  
> **原则**: 智能自动化调用 + 自进化

---

## 📊 现有搜索相关 Bot/Skill 清单

### 1️⃣ Hunter Bot (猎手) - 情报狙击手

| 项目 | 信息 |
|------|------|
| **位置** | `skills/07-system/yi/hunter_bot.py` |
| **职责** | 聪明钱监控 + 高置信度信号发现 |
| **功能** | Telegram Bot + 实时推送 |
| **状态** | ⚠️ 需整合 |

**整合方案**:
- 保留 Telegram Bot 接口
- 搜索功能调用 `ai_search_skill_evolution`
- 信号发现使用 `agent_query` 方法

---

### 2️⃣ Smart Search Router (智能搜索路由)

| 项目 | 信息 |
|------|------|
| **位置** | `skills/07-system/smart_router/smart_search_router_v2.py` |
| **职责** | 国内/国外搜索智能路由 |
| **功能** | 必应国内/Google 代理 |
| **状态** | ✅ 可集成 |

**整合方案**:
- 作为 `ai_search_skill_evolution` 的路由模块
- 提供 `search` 方法的底层实现
- 保留国内/国外智能路由逻辑

---

### 3️⃣ Product Trend Researcher (产品趋势研究员)

| 项目 | 信息 |
|------|------|
| **位置** | `skills/02-business/product-trend-researcher/` |
| **职责** | 产品趋势研究 |
| **功能** | SKILL.md 配置 |
| **状态** | ⚠️ 需整合 |

**整合方案**:
- 研究方法调用 `ai_search_skill_evolution.agent_query`
- 数据收集使用 `search_and_crawl`
- 保留产品分析逻辑

---

### 4️⃣ Product UX Researcher (产品 UX 研究员)

| 项目 | 信息 |
|------|------|
| **位置** | `skills/02-business/product-ux-researcher/` |
| **职责** | 产品 UX 研究 |
| **功能** | SKILL.md 配置 |
| **状态** | ⚠️ 需整合 |

**整合方案**:
- UX 数据收集调用 `ai_search_skill_evolution.crawl`
- 用户反馈分析使用 `agent_query`
- 保留 UX 分析框架

---

### 5️⃣ Google Search CN (国内 Google 搜索)

| 项目 | 信息 |
|------|------|
| **位置** | `skills/07-system/google-search-cn/` |
| **职责** | 国内 Google 搜索 |
| **功能** | 代理搜索 |
| **状态** | ✅ 可集成 |

**整合方案**:
- 作为 `search` 方法的备选引擎
- 与 Smart Search Router 协同
- 保留代理配置

---

### 6️⃣ Semantic Search (语义搜索)

| 项目 | 信息 |
|------|------|
| **位置** | `skills/07-system/semantic-search/` |
| **职责** | 语义搜索 |
| **功能** | 向量搜索 |
| **状态** | ✅ 可集成 |

**整合方案**:
- 作为 `search` 方法的增强功能
- 提供语义相似度排序
- 与关键词搜索互补

---

## 🏗️ 统一归属架构

```
太一 AI 搜索 Skill (ai_search_skill_evolution) v2.0
│
├── 智能调用层 (Smart Call Layer)
│   ├── 自动方法选择
│   ├── 结晶模式匹配
│   └── 关键词策略
│
├── 路由层 (Routing Layer) ← Smart Search Router
│   ├── 国内搜索 (必应)
│   ├── 国外搜索 (Google)
│   └── 语义搜索 (Semantic)
│
├── 执行层 (Execution Layer)
│   ├── search (搜索)
│   ├── crawl (爬取)
│   ├── search_and_crawl (搜索 + 爬取)
│   ├── agent_query (Agent 查询)
│   └── interact (交互)
│
├── 自进化层 (Evolution Layer)
│   ├── 使用统计
│   ├── 技能记忆
│   ├── 结晶模式
│   └── 策略优化
│
└── Bot 接口层 (Bot Interface Layer)
    ├── Hunter Bot (情报狙击)
    ├── Product Researcher (产品研究)
    └── UX Researcher (UX 研究)
```

---

## 🔄 整合流程

### P0: 核心整合 (立即执行)

1. **Smart Search Router 集成**
   ```python
   # 在 ai_search_skill_evolution.py 中
   from smart_search_router import SmartSearchRouter
   
   class AISearchSkillEvolution:
       def __init__(self):
           self.router = SmartSearchRouter()
       
       async def search(self, query: str, limit: int = 10):
           # 智能路由
           route = self.router.route_query(query)
           # 执行搜索
           results = await self._execute_search(route, query, limit)
           return results
   ```

2. **Hunter Bot 调用集成**
   ```python
   # 在 hunter_bot.py 中
   from ai_search_skill_evolution import AISearchSkillEvolution
   
   class HunterBot:
       def __init__(self):
           self.ai_search = AISearchSkillEvolution()
       
       async def scan_smart_money(self):
           # 使用 AI 搜索
           result = await self.ai_search.smart_call("聪明钱交易信号")
           return result
   ```

### P1: 功能增强 (本周执行)

3. **Product Researcher 集成**
4. **UX Researcher 集成**
5. **Semantic Search 集成**

### P2: 优化完善 (下周执行)

6. **统一日志系统**
7. **统一配置管理**
8. **性能优化**

---

## 📋 调用关系图

```
用户请求
    ↓
太一系统
    ↓
AI 搜索 Skill (ai_search_skill_evolution)
    ↓
┌───────────────────────────────────────┐
│  智能调用 (smart_call)                │
│  → 自动选择方法                        │
│  → 结晶模式匹配                        │
│  → 关键词策略                          │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│  路由层 (Smart Search Router)         │
│  → 国内搜索 (必应)                     │
│  → 国外搜索 (Google)                   │
│  → 语义搜索 (Semantic)                 │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│  执行层                                │
│  → search / crawl / agent_query        │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│  Bot 接口层                            │
│  → Hunter Bot / Product Researcher     │
│  → UX Researcher                       │
└───────────────────────────────────────┘
    ↓
返回结果 → 自进化记录
```

---

## ✅ 整合状态

| Bot/Skill | 整合状态 | 优先级 | 预计完成 |
|-----------|---------|--------|---------|
| **Smart Search Router** | 🟡 进行中 | P0 | 立即 |
| **Hunter Bot** | 🟡 进行中 | P0 | 立即 |
| **Product Trend Researcher** | ⚪ 待整合 | P1 | 本周 |
| **Product UX Researcher** | ⚪ 待整合 | P1 | 本周 |
| **Google Search CN** | ⚪ 待整合 | P2 | 下周 |
| **Semantic Search** | ⚪ 待整合 | P2 | 下周 |

---

## 🎯 太一智能自动化调用

### 统一调用接口

```python
# 所有搜索相关请求统一调用
from ai_search_skill_evolution import AISearchSkillEvolution

skill = AISearchSkillEvolution()

# Hunter Bot 调用
result = await skill.smart_call("聪明钱交易信号")

# Product Researcher 调用
result = await skill.smart_call("分析 2026 年产品趋势")

# UX Researcher 调用
result = await skill.smart_call("爬取用户反馈并分析")

# 通用搜索
result = await skill.smart_call("搜索 AI 爬虫相关信息")
```

### 自进化共享

- 所有 Bot 调用共享使用统计
- 结晶模式全局共享
- 技能记忆统一管理
- 策略优化全局生效

---

## 📊 整合后优势

| 维度 | 整合前 | 整合后 |
|------|--------|--------|
| **调用方式** | 分散调用 | ✅ 统一智能调用 |
| **自进化** | 各自为政 | ✅ 全局共享 |
| **结晶模式** | 无法共享 | ✅ 全局结晶 |
| **使用统计** | 分散统计 | ✅ 统一统计 |
| **策略优化** | 独立优化 | ✅ 全局优化 |
| **维护成本** | 高 | ✅ 低 |
| **性能** | 重复调用 | ✅ 缓存共享 |

---

## 📁 文件结构调整

```
skills/07-system/ai-search/
├── ai_search_skill.py              # v1.0 基础版
├── ai_search_skill_evolution.py    # v2.0 自进化版 ✅ (核心)
├── unified_search_bot_manager.py   # 统一 Bot 管理器 🆕
├── README.md                       # 使用文档
├── skill_config.json               # 配置文件
├── evolution/                      # 进化数据
│   ├── usage_stats.json
│   ├── crystallized_patterns.json
│   └── evolution_state.json
├── memory/                         # 技能记忆
│   └── skill_memories.json
└── integration/                    # 集成模块 🆕
    ├── smart_search_router_integration.py
    ├── hunter_bot_integration.py
    ├── product_researcher_integration.py
    └── ux_researcher_integration.py
```

---

## 🚀 执行计划

### P0 立即执行

- [ ] 创建 `unified_search_bot_manager.py`
- [ ] 集成 Smart Search Router
- [ ] 集成 Hunter Bot
- [ ] 更新调用文档

### P1 本周执行

- [ ] 集成 Product Researcher
- [ ] 集成 UX Researcher
- [ ] 统一日志系统
- [ ] 性能测试

### P2 下周执行

- [ ] 集成 Google Search CN
- [ ] 集成 Semantic Search
- [ ] 统一配置管理
- [ ] 优化文档

---

**🔍 搜索 Bot 统一归属方案完成！**

**✅ 6 个搜索 Bot/Skill 清单！统一架构设计！太一智能自动化调用！自进化共享！P0 立即执行整合！**
