# 🌐 太一共享搜索服务架构

> **版本**: v1.0
> **创建时间**: 2026-05-04
> **作者**: 太一 AGI
> **定位**: 系统级共享搜索 Agent，供所有 Agent 智能调用

---

## 📐 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     太一系统 (Taiyi System)                       │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 跨境贸易    │  │ 旅游探路者  │  │ GEO外贸     │  ...        │
│  │ Agent       │  │ Agent       │  │ Agent       │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              太一共享搜索服务 (Shared Search Service)      │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │ 智能路由    │  │ 反爬对抗    │  │ 结果缓存    │     │   │
│  │  │ Router      │  │ Anti-Scrape │  │ Cache       │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │ 搜索执行    │  │ 统计监控    │  │ 配额管理    │     │   │
│  │  │ Executor    │  │ Stats       │  │ Quota       │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   搜索后端 (Search Backends)              │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │   │
│  │  │ requests │  │ browser  │  │ API      │  │ 本地数据 │ │   │
│  │  │ (快速)   │  │ (反爬)   │  │ (官方)   │  │ (缓存)   │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 核心设计

### 1. 单例模式

所有 Agent 共享同一个搜索服务实例：

```python
from skills.shared_search_agent import get_shared_search_service

service = get_shared_search_service()  # 全局单例
```

### 2. Agent 类型识别

自动识别调用 Agent，优化搜索策略：

| Agent 类型 | 标识 | 默认引擎 | 特殊处理 |
|-----------|------|---------|---------|
| 跨境贸易 | `cross_border_trade` | Google | 商业关键词优化 |
| 旅游探路者 | `travel_explorer` | Google | 价格敏感型 |
| GEO外贸 | `geo_outbound` | Google | B2B优化 |
| OSINT | `maigret` | 多引擎 | 高匿名要求 |
| 通用 | `general` | Google | 标准模式 |

### 3. 智能路由

自动选择最佳搜索模式：

```
用户请求
    ↓
检测目标网站保护等级
    ↓
┌─────────────────┐
│ 低保护?         │
│ → requests模式  │ (快速，90%场景)
└─────────────────┘
    ↓ 否
┌─────────────────┐
│ 高保护?         │
│ → browser模式   │ (反爬，10%场景)
└─────────────────┘
    ↓ 失败
自动重试 + 升级反爬等级
```

---

## 🔧 核心组件

### SearchRequest (搜索请求)

```python
@dataclass
class SearchRequest:
    query: str              # 搜索关键词
    agent_type: str         # 调用Agent类型
    search_mode: str        # 搜索模式 (auto/requests/browser)
    country: Optional[str]  # 目标国家
    engine: str             # 搜索引擎
    max_results: int        # 最大结果数
    use_cache: bool         # 是否使用缓存
```

### SearchResult (搜索结果)

```python
@dataclass
class SearchResult:
    success: bool           # 是否成功
    results: List[Dict]     # 结果列表
    source: str             # 来源 (requests/browser/cache)
    cache_hit: bool         # 是否缓存命中
    duration_ms: float      # 耗时(毫秒)
    anti_scraping_level: int # 反爬等级
```

### SearchCache (缓存管理)

- **内存缓存**: 热点数据，毫秒级访问
- **文件缓存**: 持久化存储，24小时TTL
- **自动清理**: 过期缓存自动清理

### SearchStats (统计监控)

- **全局统计**: 总请求数、缓存命中率
- **Agent统计**: 各Agent调用次数
- **每日统计**: 日活、趋势分析
- **引擎统计**: 各搜索引擎使用情况

---

## 🚀 使用方式

### 方式1: 便捷函数 (推荐)

```python
from skills.shared_search_agent import search

# 通用搜索
result = search("smart water bottle")

# 跨境贸易搜索
result = search("smart water bottle", agent_type="cross_border_trade", country="US")

# 旅游搜索
result = search("cheap flights to Tokyo", agent_type="travel_explorer")

# OSINT搜索 (自动使用browser模式)
result = search("username investigation", agent_type="maigret", search_mode="browser")
```

### 方式2: 服务实例

```python
from skills.shared_search_agent import get_shared_search_service

service = get_shared_search_service()

# 专用方法
result = service.search_for_cross_border("product research", country="US")
result = service.search_for_travel("hotel deals")
result = service.search_for_geo("market analysis")
result = service.search_for_osint("digital footprint")

# 查看统计
stats = service.get_stats()
print(f"总请求: {stats['total_requests']}")
print(f"缓存命中率: {stats['cache_hit_rate']}")
```

### 方式3: 自定义请求

```python
from skills.shared_search_agent import SearchRequest, get_shared_search_service

service = get_shared_search_service()

request = SearchRequest(
    query="custom search",
    agent_type="my_agent",
    search_mode="browser",      # 强制使用浏览器
    country="CN",
    engine="baidu",
    max_results=20,
    use_cache=True,
)

result = service.search(request)
```

---

## 📊 集成示例

### 跨境贸易 Agent 集成

```python
# 在 cross_border_agent.py 中
from skills.shared_search_agent import search

class CrossBorderAgent:
    def research_product(self, product_name: str):
        # 使用共享搜索
        result = search(
            product_name,
            agent_type="cross_border_trade",
            country="US"
        )
        
        if result.success:
            return self._analyze_results(result.results)
```

### 旅游探路者 Agent 集成

```python
# 在 ai_travel_explorer.py 中
from skills.shared_search_agent import get_shared_search_service

class TravelExplorer:
    def __init__(self):
        self.search_service = get_shared_search_service()
    
    def find_cheapest_flights(self, destination: str):
        # 使用共享搜索
        result = self.search_service.search_for_travel(
            f"cheapest flights to {destination}"
        )
        
        return result.results
```

### GEO 外贸 Agent 集成

```python
# 在 geo_outbound_skill.py 中
from skills.shared_search_agent import search

def geo_market_research(hs_code: str):
    # 使用共享搜索
    result = search(
        f"HS code {hs_code} import trends",
        agent_type="geo_outbound",
        search_mode="browser"  # 需要反爬
    )
    
    return result.results
```

---

## 🎛️ 配置选项

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SEARCH_CACHE_TTL` | 24 | 缓存有效期(小时) |
| `SEARCH_MAX_RESULTS` | 10 | 默认最大结果数 |
| `SEARCH_DEFAULT_MODE` | auto | 默认搜索模式 |
| `SEARCH_LOG_LEVEL` | INFO | 日志级别 |

### 反爬等级

| 等级 | 名称 | 功能 | 适用 |
|------|------|------|------|
| 0 | 无 | 纯requests | 内部API |
| 1 | 基础 | UA轮换 | 简单网站 |
| 2 | 标准 | +行为模拟 | 一般保护 |
| 3 | 高级 | +指纹伪装 | Google/Bing |
| 4 | 专业 | +CSP绕过 | LinkedIn等 |
| 5 | 极致 | +代理 | 极端保护 |

---

## 📈 性能指标

### 目标性能

| 指标 | 目标 | 说明 |
|------|------|------|
| 响应时间 | <3s | 95%请求 |
| 缓存命中率 | >60% | 热点查询 |
| 成功率 | >95% | 包括重试 |
| 并发支持 | 10+ | 同时查询 |

### 资源消耗

| 模式 | 内存 | CPU | 时间 |
|------|------|-----|------|
| requests | 10MB | 低 | 1-2s |
| browser | 100MB | 中 | 3-5s |
| cache | 1MB | 极低 | <100ms |

---

## 🔒 安全与合规

### 反爬原则

1. **遵守 robots.txt** - 尊重网站规则
2. **控制频率** - 默认延迟1-3秒
3. **不爬私有数据** - 仅限公开信息
4. **用户代理透明** - 不伪装成人类

### 配额管理

```python
# 每个Agent的默认配额
DEFAULT_QUOTAS = {
    "cross_border_trade": 1000,  # 每日1000次
    "travel_explorer": 500,
    "geo_outbound": 800,
    "maigret": 200,
    "general": 100,
}
```

---

## 🧪 测试

```bash
# 运行测试
cd /home/sayelf/.openclaw/workspace/skills/shared-search-agent
python3 shared_search_service.py

# 预期输出:
# 🌐 太一共享搜索服务测试
# 📦 测试 1: 跨境贸易 Agent 搜索
# ✈️ 测试 2: 旅游探路者搜索
# 💾 测试 3: 缓存测试
# 📊 测试 4: 服务统计
```

---

## 📁 文件结构

```
shared-search-agent/
├── __init__.py                    # 包入口
├── shared_search_service.py       # 核心服务 (17KB)
└── SHARED_SEARCH_ARCHITECTURE.md  # 架构文档
```

---

## 🔄 与现有系统集成

### 已集成
- ✅ 跨境贸易 Agent (prospect_search.py)
- ✅ 浏览器搜索引擎 (browser_search_engine.py)
- ✅ 反爬对抗机制 (anti_scraping_adapter.py)

### 待集成
- 🟡 旅游探路者 Agent (ai_travel_explorer.py)
- 🟡 GEO 外贸 Agent (geo_outbound_skill.md)
- 🟡 OSINT 工具 (maigret)
- 🟡 OpenClaw Gateway 技能注册

---

## 🎯 未来扩展

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 分布式搜索 | P1 | 多实例负载均衡 |
| 智能重试 | P1 | 指数退避+降级 |
| 结果去重 | P2 | 跨引擎去重 |
| 语义搜索 | P2 | 向量相似度 |
| 实时索引 | P3 | 本地数据索引 |

---

## ✅ 特点总结

1. **系统级共享** - 所有Agent共用，避免重复开发
2. **智能路由** - 自动选择最佳搜索模式
3. **统一反爬** - 集中管理反爬策略
4. **结果缓存** - 减少重复请求，提升性能
5. **统计监控** - 全面了解搜索使用情况
6. **配额管理** - 公平分配资源
7. **易于集成** - 一行代码即可使用

---

*太一 AGI · 共享搜索服务架构 v1.0*
*创建时间: 2026-05-04*
*核心能力: 统一搜索入口 + 智能反爬 + 结果共享*
