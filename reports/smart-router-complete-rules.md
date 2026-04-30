# 🔄 太一智能路由系统 - 完整规则配置

> **更新时间**: 2026-04-16 14:07  
> **版本**: v2.0  
> **路由数量**: 4 个协同工作

---

## 📋 路由系统架构

### 4 大路由器协同

| 路由器 | 职责 | 位置 | 状态 |
|--------|------|------|------|
| **smart-model-router** | 语义分析/模型选择 | skills/07-system/smart-model-router/ | ✅ |
| **geo-model-router** | 地理感知/流量分流 | skills/07-system/geo-model-router/ | ✅ |
| **smart-search-router** | 搜索路由/引擎选择 | skills/07-system/smart_router/ | ✅ |
| **quota-router** | 配额控制/成本管理 | skills/07-system/quota-aware-model-router/ | ✅ |

---

## 🔌 路由协同工作流

```
用户请求
    ↓
1. smart-model-router
   → 任务分类 (语义分析)
   → 模型选择 (成本优化)
    ↓
2. geo-model-router
   → 地理感知 (目标位置)
   → 流量分流 (国内/国外)
    ↓
3. smart-search-router
   → 搜索类型识别 (国内/国外)
   → 搜索引擎选择 (bing_cn/chromium)
    ↓
4. quota-router
   → 配额检查
   → 成本控制
    ↓
执行请求
```

---

## 📊 smart-search-router 规则

### 规则 1: 国内内容搜索

**触发关键词**:
```
中国，国内，中文，大陆，内地，CN, china domestic
```

**路由配置**:
```json
{
  "name": "国内内容搜索",
  "search_engine": "bing_cn",
  "endpoint": "https://cn.bing.com",
  "proxy": false,
  "traffic": "domestic",
  "priority": 1
}
```

**流量配置**:
```json
{
  "name": "国内流量",
  "proxy_enabled": false,
  "proxy_url": null,
  "dns": "114.114.114.114",
  "timeout": 10
}
```

**使用示例**:
```
查询："中国最新科技新闻"
结果:
  - search_type: domestic_search
  - search_engine: bing_cn
  - proxy_enabled: false
  - traffic_type: domestic
```

---

### 规则 2: 国外内容搜索

**触发关键词**:
```
国外，国际，海外，US, global, international
```

**路由配置**:
```json
{
  "name": "国外内容搜索",
  "search_engine": "chromium",
  "endpoint": "https://www.google.com",
  "proxy": true,
  "traffic": "proxy",
  "priority": 2
}
```

**流量配置**:
```json
{
  "name": "代理流量",
  "proxy_enabled": true,
  "proxy_url": "http://127.0.0.1:7890",
  "dns": "8.8.8.8",
  "timeout": 30
}
```

**使用示例**:
```
查询："US latest technology news"
结果:
  - search_type: international_search
  - search_engine: chromium
  - proxy_enabled: true
  - traffic_type: proxy
```

---

### 规则 3: 默认搜索

**触发条件**: 未匹配到国内/国外关键词

**路由配置**:
```json
{
  "name": "默认搜索",
  "search_engine": "bing_cn",
  "endpoint": "https://cn.bing.com",
  "proxy": false,
  "traffic": "domestic",
  "priority": 3
}
```

**流量配置**:
```json
{
  "name": "国内流量",
  "proxy_enabled": false,
  "proxy_url": null,
  "dns": "114.114.114.114",
  "timeout": 10
}
```

**使用示例**:
```
查询："默认搜索测试"
结果:
  - search_type: default
  - search_engine: bing_cn
  - proxy_enabled: false
  - traffic_type: domestic
```

---

## 🌐 geo-model-router 规则

### 国内服务白名单

```json
{
  "domestic_services": [
    "cn.bing.com",
    "baidu.com",
    "zhihu.com",
    "weibo.com",
    "taobao.com",
    "jd.com",
    "163.com",
    "qq.com",
    "aliyun.com",
    "tencent.com"
  ]
}
```

### 国外服务白名单

```json
{
  "international_services": [
    "google.com",
    "github.com",
    "stackoverflow.com",
    "twitter.com",
    "youtube.com",
    "reddit.com",
    "medium.com",
    "openai.com",
    "anthropic.com"
  ]
}
```

### 路由规则

```json
{
  "domestic": {
    "route_type": "domestic",
    "proxy": null,
    "dns": "114.114.114.114",
    "timeout": 10
  },
  "international": {
    "route_type": "international",
    "proxy": "socks5://127.0.0.1:7890",
    "dns": "8.8.8.8",
    "timeout": 30
  }
}
```

---

## 🧠 smart-model-router 规则

### 国内模型

```json
{
  "DOMESTIC_MODELS": {
    "qwen": "bailian",
    "qwen-turbo": "bailian",
    "qwen-plus": "bailian",
    "qwen-max": "bailian",
    "qwen-coder": "bailian",
    "qwen3.5-plus": "bailian",
    "qwen3-coder-plus": "bailian",
    "deepseek": "deepseek",
    "deepseek-chat": "deepseek",
    "deepseek-coder": "deepseek",
    "kimi": "moonshot",
    "kimi-chat": "moonshot"
  }
}
```

### 国外模型

```json
{
  "OVERSEAS_MODELS": {
    "gemini": "google",
    "gemini-pro": "google",
    "gemini-2.5-pro": "google",
    "gpt": "openai",
    "gpt-4": "openai",
    "gpt-4o": "openai",
    "gpt-3.5-turbo": "openai",
    "claude": "anthropic",
    "claude-3": "anthropic",
    "claude-sonnet": "anthropic"
  }
}
```

### 本地模型

```json
{
  "LOCAL_MODELS": [
    "qwen2.5:7b",
    "qwen2.5-coder:7b",
    "llama3:8b"
  ]
}
```

---

## 💰 quota-router 规则

### 配额配置

```json
{
  "quota_config": {
    "daily_limit": 100.0,
    "monthly_limit": 3000.0,
    "per_request_limit": 10.0,
    "currency": "CNY"
  }
}
```

### 成本层级

```json
{
  "cost_tiers": {
    "low": {
      "max_cost_per_1k": 0.01,
      "models": ["qwen-turbo", "deepseek-chat"]
    },
    "medium": {
      "max_cost_per_1k": 0.1,
      "models": ["qwen-plus", "gpt-4o"]
    },
    "high": {
      "max_cost_per_1k": 1.0,
      "models": ["qwen-max", "gpt-4", "claude-3"]
    }
  }
}
```

---

## 📈 完整路由示例

### 示例 1: 国内搜索任务

```
用户请求："中国最新 AI 新闻"

路由流程:
1. smart-model-router
   → 任务类型：research
   → 模型选择：qwen3.5-plus (国内模型)

2. geo-model-router
   → 目标位置：国内
   → 流量类型：domestic

3. smart-search-router
   → 搜索类型：domestic_search (检测到"中国")
   → 搜索引擎：bing_cn
   → 代理：false

4. quota-router
   → 配额检查：通过
   → 成本估算：0.05 CNY

执行:
→ 使用 bing_cn 搜索
→ 走国内流量 (不走代理)
→ 使用 qwen3.5-plus 分析结果
```

---

### 示例 2: 国外搜索任务

```
用户请求："US AI regulation news"

路由流程:
1. smart-model-router
   → 任务类型：research
   → 模型选择：gpt-4o (国外模型)

2. geo-model-router
   → 目标位置：国外 (US)
   → 流量类型：proxy

3. smart-search-router
   → 搜索类型：international_search (检测到"US")
   → 搜索引擎：chromium
   → 代理：true

4. quota-router
   → 配额检查：通过
   → 成本估算：0.2 CNY

执行:
→ 使用 chromium 搜索
→ 走代理流量
→ 使用 gpt-4o 分析结果
```

---

## 🚀 路由规则总结

### 搜索路由 (smart-search-router)

| 规则 | 关键词 | 引擎 | 代理 | 流量 |
|------|--------|------|------|------|
| 国内搜索 | 中国/国内/中文/CN | bing_cn | ❌ | domestic |
| 国外搜索 | 国外/国际/海外/US | chromium | ✅ | proxy |
| 默认搜索 | 未匹配 | bing_cn | ❌ | domestic |

### 地理路由 (geo-model-router)

| 规则 | 服务类型 | 代理 | DNS | 超时 |
|------|----------|------|-----|------|
| 国内服务 | cn.bing.com/baidu.com | ❌ | 114.114.114.114 | 10s |
| 国外服务 | google.com/github.com | ✅ | 8.8.8.8 | 30s |

### 模型路由 (smart-model-router)

| 规则 | 模型类型 | 提供商 | 位置 |
|------|----------|--------|------|
| 国内模型 | qwen/deepseek/kimi | bailian/deepseek/moonshot | 国内 |
| 国外模型 | gpt/gemini/claude | openai/google/anthropic | 国外 |
| 本地模型 | qwen2.5/llama3 | local | 本地 |

### 配额路由 (quota-router)

| 规则 | 限制类型 | 金额 | 货币 |
|------|----------|------|------|
| 每日限制 | daily_limit | 100.0 | CNY |
| 每月限制 | monthly_limit | 3000.0 | CNY |
| 单次限制 | per_request_limit | 10.0 | CNY |

---

## 📁 配置文件位置

```
太一智能路由系统/
├── smart-model-router/
│   ├── router.py
│   ├── config/
│   └── providers/
│
├── geo-model-router/
│   ├── geo_router.py
│   ├── config/geo_config.json
│   └── cache/
│
├── smart_router/
│   ├── smart_search_router.py
│   ├── smart_search_router_v2.py
│   └── routers/
│
├── quota-aware-model-router/
│   ├── quota_router.py
│   └── config/
│
└── smart-search-router/
    ├── router_config.json
    ├── integration_config.json
    └── search_log.json
```

---

## 🎯 核心优势

### 智能切换
```
✅ 自动识别搜索类型
✅ 自动选择搜索引擎
✅ 自动切换流量类型
✅ 自动选择最优模型
```

### 多路由协同
```
✅ smart-model-router: 任务分类
✅ geo-model-router: 地理感知
✅ smart-search-router: 搜索路由
✅ quota-router: 配额控制
```

### 性能优化
```
✅ 国内搜索走国内流量 (快速)
✅ 国外搜索走代理流量 (可访问)
✅ 本地模型优先 (低成本)
✅ 配额控制 (防超支)
```

---

*太一 AGI · 智能路由系统 v2.0 · 2026-04-16 14:07*

**🔄 太一智能路由系统 - 4 个路由器协同工作！**
