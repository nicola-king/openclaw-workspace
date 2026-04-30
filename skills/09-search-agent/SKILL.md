# 🔍 智能搜索 Agent v1.0

> **版本**: 1.0.0  
> **创建时间**: 2026-04-26  
> **作者**: 太一 AGI  
> **定位**: 模块化、自进化的智能搜索系统  

---

## 🎯 核心使命

**智能搜索 Agent** 是太一系统的统一搜索入口，具备：
- 多层反反爬策略
- 智能路由选择
- 自进化学习能力
- 模块化架构设计

---

## 🏗️ 架构设计

```
用户查询
    ↓
智能路由层 (Search Router)
    ↓
├── 反爬对抗层 (Anti-Scraping)
│   ├── Playwright 浏览器自动化
│   ├── 代理轮换 (海外/国内)
│   ├── 指纹伪装
│   └── 速率控制
├── 搜索引擎层 (Search Engines)
│   ├── 海外优先：Bing > Google > DuckDuckGo
│   ├── 国内备用：百度 > 搜狗 > 360
│   └── 专业平台：LinkedIn/GitHub/行业站
├── 数据提取层 (Data Extractor)
│   ├── 结构化数据解析
│   ├── 信息验证
│   └── 置信度评分
└── 自进化层 (Self-Evolution)
    ├── 成功率统计
    ├── 策略优化
    └── 知识库更新
```

---

## 📦 模块清单

### 核心模块

| 模块 | 版本 | 依赖 | 功能 |
|------|------|------|------|
| **search-router** | v1.0 | 无 | 智能路由选择 |
| **anti-scraping** | v1.0 | Playwright | 反反爬策略 |
| **data-extractor** | v1.0 | BeautifulSoup | 数据提取 |
| **self-evolution** | v1.0 | 无 | 自进化学习 |

### 搜索引擎模块

| 模块 | 版本 | 依赖 | 功能 |
|------|------|------|------|
| **bing-search** | v1.0 | httpx | Bing 搜索 |
| **google-search** | v1.0 | Playwright | Google 搜索 |
| **duckduckgo** | v1.0 | httpx | DuckDuckGo |
| **baidu-search** | v1.0 | requests | 百度搜索 |

### 代理管理模块

| 模块 | 版本 | 依赖 | 功能 |
|------|------|------|------|
| **proxy-manager** | v1.0 | 无 | 代理池管理 |
| **geo-router** | v1.0 | 无 | 地理路由 |

---

## 🚀 使用方法

### 1. 独立运行

```bash
# 搜索
python core/search_agent.py --query "foldable container house buyer" --region "Southeast Asia"

# 测试
python tests/test_search_agent.py

# 自进化
python core/self_evolution.py --update
```

### 2. 太一系统集成

```python
from search_agent import SearchAgent

agent = SearchAgent()

# 智能搜索
results = agent.search(
    query="steel foldable container house",
    regions=["Southeast Asia", "Middle East"],
    priority="high"
)

# 自进化
agent.evolve()
```

---

## 📊 搜索策略

### 优先级排序

1. **Playwright 浏览器** (最高优先级)
   - 绕过 JS 渲染
   - 模拟真实用户
   - 支持验证码

2. **HTTP 客户端** (中等优先级)
   - 快速轻量
   - 适合简单页面
   - 需要反爬策略

3. **API 接口** (最低优先级)
   - 稳定可靠
   - 需要密钥
   - 有限制

### 地理路由

| 区域 | 代理 | 搜索引擎 |
|------|------|----------|
| 海外 | 海外代理 | Bing/Google/DuckDuckGo |
| 国内 | 国内代理 | 百度/搜狗/360 |
| 混合 | 智能切换 | 自动选择 |

---

## 🧬 自进化机制

### 学习循环

```
搜索请求 → 执行搜索 → 结果评估 → 策略更新 → 知识库保存
    ↓
成功率统计 → 策略优化 → 配置更新 → 下次搜索
```

### 进化指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **成功率** | 搜索成功比例 | >80% |
| **响应时间** | 平均响应时间 | <5s |
| **数据质量** | 信息准确度 | >90% |
| **反爬率** | 被反爬比例 | <20% |

---

## 📁 文件结构

```
09-search-agent/
├── SKILL.md                          # 本文件
├── core/
│   ├── search_agent.py               # 主搜索引擎
│   ├── search_router.py              # 智能路由
│   ├── anti_scraping.py              # 反反爬策略
│   ├── data_extractor.py             # 数据提取
│   └── self_evolution.py             # 自进化
├── modules/
│   ├── bing_search.py                # Bing 搜索
│   ├── google_search.py              # Google 搜索
│   ├── duckduckgo_search.py          # DuckDuckGo
│   └── baidu_search.py               # 百度搜索
├── strategies/
│   ├── proxy_strategy.py             # 代理策略
│   ├── fingerprint_strategy.py       # 指纹策略
│   └── rate_limit_strategy.py        # 速率策略
├── config/
│   ├── search_config.json            # 搜索配置
│   ├── proxy_config.json             # 代理配置
│   └── evolution_config.json         # 进化配置
├── data/
│   ├── search_history.json           # 搜索历史
│   ├── success_metrics.json          # 成功指标
│   └── knowledge_base.json           # 知识库
└── tests/
    ├── test_search_agent.py          # 测试文件
    └── test_anti_scraping.py         # 反爬测试
```

---

## 🔗 相关链接

| 资源 | 链接 |
|------|------|
| **Playwright** | https://playwright.dev |
| **BeautifulSoup** | https://www.crummy.com/software/BeautifulSoup |
| **HTTPx** | https://www.python-httpx.org |

---

*太一智能搜索 Agent v1.0 · 2026-04-26*  
*模块化、自进化、智能路由*