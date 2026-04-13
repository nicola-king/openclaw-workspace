---
name: geo-model-router
version: 1.0.0
description: 地理感知智能路由 - 国内流量走国内/国外流量走代理/智能识别分流
category: infrastructure
tags: ['geo-routing', 'traffic-split', 'proxy', 'domestic', 'international', 'intelligent-routing']
author: 太一 AGI
created: 2026-04-08
updated: 2026-04-08
status: active
priority: P0
---

# 🌍 Geo-Model Router - 地理感知智能路由 v1.0

> **状态**: ✅ 新创建 | **版本**: 1.0.0 | **创建时间**: 2026-04-08  
> **核心原则**: 国内流量走国内·国外流量走代理·智能识别分流

---

## 🎯 四大核心原则

### 原则 1: 国内流量走国内 ✅

**适用范围**:
- 🇨🇳 国内大模型 API (阿里百炼/百度/智谱等)
- 🇨🇳 国内互联网服务 (微信/飞书/微博等)
- 🇨🇳 国内通讯通道 (企业微信/钉钉等)

**路由规则**:
```yaml
目标类型：国内服务
路由策略：直连 (不经过代理)
示例:
  - 阿里百炼：https://dashscope.aliyuncs.com
  - 智谱 AI: https://open.bigmodel.cn
  - 飞书 API: https://open.feishu.cn
  - 企业微信：https://qyapi.weixin.qq.com
```

**优势**:
- ✅ 低延迟 (国内直连)
- ✅ 高稳定性 (不依赖代理)
- ✅ 合规性 (数据不出境)

---

### 原则 2: 国外流量走代理 ✅

**适用范围**:
- 🌐 国外大模型 API (OpenAI/Anthropic/Google 等)
- 🌐 国外互联网服务 (GitHub/Twitter/YouTube 等)
- 🌐 国外通讯通道 (Telegram/WhatsApp/Slack 等)

**路由规则**:
```yaml
目标类型：国外服务
路由策略：代理 (经过 SOCKS5/HTTP 代理)
代理配置:
  host: 127.0.0.1
  port: 7890  # Mihomo/Clash 端口
  protocol: socks5
示例:
  - OpenAI: https://api.openai.com → 代理
  - Anthropic: https://api.anthropic.com → 代理
  - Google: https://generativelanguage.googleapis.com → 代理
  - Telegram Bot API → 代理
```

**优势**:
- ✅ 可访问性 (突破地域限制)
- ✅ 统一出口 (便于管理)
- ✅ 安全性 (流量加密)

---

### 原则 3: 智能识别智能分流 ✅

**自动识别维度**:

| 维度 | 识别方式 | 分流策略 |
|------|---------|---------|
| **域名** | TLD/.cn → 国内 | 自动路由 |
| **IP 地址** | GeoIP 数据库 | 自动路由 |
| **API 路径** | URL 关键词匹配 | 自动路由 |
| **服务类型** | 预定义白名单 | 自动路由 |
| **响应时间** | 超时检测 | 自动切换 |

**智能决策流程**:
```
请求发起
    ↓
[1] 检查目标域名
    ├─ *.cn → 国内直连
    ├─ *.com → 检查服务列表
    └─ 其他 → IP 检测
    ↓
[2] 查询服务白名单
    ├─ 国内服务列表 → 直连
    ├─ 国外服务列表 → 代理
    └─ 未知 → 智能探测
    ↓
[3] 智能探测 (可选)
    ├─ 先尝试直连 (超时 3 秒)
    ├─ 失败 → 切换代理
    └─ 记录结果到缓存
    ↓
[4] 执行请求
    ↓
[5] 更新缓存 (TTL 300 秒)
```

---

### 原则 4: 单独的 Skill ✅

**独立模块设计**:

```
skills/geo-model-router/
├── SKILL.md (本文档)
├── geo_router.py (路由核心)
├── config/ (配置文件)
│   ├── domestic_services.yaml (国内服务列表)
│   ├── international_services.yaml (国外服务列表)
│   └── proxy_config.yaml (代理配置)
├── detectors/ (检测器)
│   ├── domain_detector.py (域名检测)
│   ├── ip_detector.py (IP 检测)
│   └── latency_detector.py (延迟检测)
├── cache/ (缓存)
│   └── route_cache.py (路由缓存)
└── tests/ (测试)
    └── test_geo_router.py
```

**独立使用**:
```python
from skills.geo_model_router.geo_router import GeoRouter

# 初始化
router = GeoRouter()

# 自动路由 (智能识别)
response = router.request(
    url="https://api.openai.com/v1/chat/completions",
    method="POST",
    json={"model": "gpt-4", "messages": [...]}
)
# 自动识别为国外服务 → 使用代理

# 手动指定
response = router.request(
    url="https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
    proxy="auto"  # auto/domestic/international
)
# 自动识别为国内服务 → 直连
```

---

## 📋 服务白名单

### 国内服务列表 (直连)

```yaml
# config/domestic_services.yaml
domestic_services:
  # 大模型 API
  - name: 阿里百炼
    domains:
      - "dashscope.aliyuncs.com"
      - "aliyuncs.com"
    route: domestic
    
  - name: 智谱 AI
    domains:
      - "open.bigmodel.cn"
      - "bigmodel.cn"
    route: domestic
    
  - name: 百度千帆
    domains:
      - "qianfan.baidubce.com"
      - "baidubce.com"
    route: domestic
    
  - name: 讯飞星火
    domains:
      - "spark-api.xf-yun.com"
      - "xf-yun.com"
    route: domestic
    
  # 通讯通道
  - name: 飞书
    domains:
      - "open.feishu.cn"
      - "feishu.cn"
    route: domestic
    
  - name: 企业微信
    domains:
      - "qyapi.weixin.qq.com"
      - "weixin.qq.com"
    route: domestic
    
  - name: 钉钉
    domains:
      - "oapi.dingtalk.com"
      - "dingtalk.com"
    route: domestic
    
  # 互联网服务
  - name: 微信公众号
    domains:
      - "mp.weixin.qq.com"
    route: domestic
    
  - name: 微博
    domains:
      - "api.weibo.com"
    route: domestic
    
  - name: 知乎
    domains:
      - "zhihu.com"
      - "zhimg.com"
    route: domestic
```

### 国外服务列表 (代理)

```yaml
# config/international_services.yaml
international_services:
  # 大模型 API
  - name: OpenAI
    domains:
      - "api.openai.com"
      - "openai.com"
    route: international
    
  - name: Anthropic
    domains:
      - "api.anthropic.com"
      - "anthropic.com"
    route: international
    
  - name: Google AI
    domains:
      - "generativelanguage.googleapis.com"
      - "googleapis.com"
    route: international
    
  - name: Cohere
    domains:
      - "api.cohere.ai"
    route: international
    
  # 通讯通道
  - name: Telegram
    domains:
      - "api.telegram.org"
      - "t.me"
    route: international
    
  - name: WhatsApp
    domains:
      - "graph.facebook.com"  # WhatsApp Business API
    route: international
    
  - name: Slack
    domains:
      - "slack.com"
      - "slack-api.com"
    route: international
    
  # 互联网服务
  - name: GitHub
    domains:
      - "api.github.com"
      - "github.com"
    route: international
    
  - name: Twitter/X
    domains:
      - "api.twitter.com"
      - "x.com"
    route: international
    
  - name: YouTube
    domains:
      - "youtube.googleapis.com"
    route: international
```

---

## ⚙️ 代理配置

### 代理配置模板

```yaml
# config/proxy_config.yaml
proxy:
  enabled: true
  default_mode: auto  # auto/domestic/international
  
  # SOCKS5 代理 (推荐)
  socks5:
    host: 127.0.0.1
    port: 7890
    username: null
    password: null
    
  # HTTP 代理 (备选)
  http:
    host: 127.0.0.1
    port: 7890
    username: null
    password: null
    
  # 超时配置
  timeout:
    domestic: 10  # 国内直连超时 (秒)
    international: 30  # 国外代理超时 (秒)
    probe: 3  # 智能探测超时 (秒)
    
  # 故障切换
  fallback:
    enabled: true
    max_retries: 2
    retry_delay: 1  # 重试间隔 (秒)
    
  # 缓存配置
  cache:
    enabled: true
    ttl: 300  # 缓存有效期 (秒)
    max_size: 1000  # 最大缓存条目
```

---

## 🚀 使用方式

### 基础用法

```python
from skills.geo_model_router.geo_router import GeoRouter

# 初始化 (自动加载配置)
router = GeoRouter()

# 方式 1: 自动路由 (推荐)
response = router.request(
    url="https://api.openai.com/v1/chat/completions",
    method="POST",
    headers={"Authorization": "Bearer xxx"},
    json={"model": "gpt-4", "messages": [...]}
)
# 自动识别：api.openai.com → 国外服务 → 使用代理

# 方式 2: 手动指定路由
response = router.request(
    url="https://dashscope.aliyuncs.com/api/v1/...",
    proxy="domestic"  # 强制国内直连
)

# 方式 3: 智能探测模式
response = router.request(
    url="https://unknown-service.com/api",
    proxy="auto",  # 先直连尝试，失败切换代理
    probe=True
)
```

### 集成到大模型调用

```python
from skills.geo_model_router.geo_router import GeoRouter
from openai import OpenAI

# 初始化路由
router = GeoRouter()

# 创建 OpenAI 客户端 (自动走代理)
client = OpenAI(
    api_key="sk-xxx",
    http_client=router.create_http_client(
        url="https://api.openai.com"
    )
)

# 创建百炼客户端 (自动直连)
bailian_client = OpenAI(
    api_key="sk-xxx",
    base_url="https://dashscope.aliyuncs.com/v1",
    http_client=router.create_http_client(
        url="https://dashscope.aliyuncs.com"
    )
)
```

### 集成到 Telegram Bot

```python
from skills.geo_model_router.geo_router import GeoRouter
import telebot

# 初始化路由
router = GeoRouter()

# Telegram Bot API 自动走代理
bot = telebot.TeleBot(
    "YOUR_BOT_TOKEN",
    requests_session=router.create_session(
        url="https://api.telegram.org"
    )
)
```

---

## 📊 路由决策日志

### 日志格式

```yaml
timestamp: 2026-04-08T15:23:00+08:00
request:
  url: https://api.openai.com/v1/chat/completions
  method: POST
routing:
  detected_type: international
  detected_by: domain_whitelist
  proxy_used: socks5://127.0.0.1:7890
  decision_time_ms: 2
response:
  status_code: 200
  latency_ms: 1250
  proxy_latency_ms: 1248
```

### 监控指标

```yaml
metrics:
  total_requests: 1000
  domestic_requests: 600  # 60%
  international_requests: 400  # 40%
  
  # 成功率
  domestic_success_rate: 99.5%
  international_success_rate: 98.2%
  
  # 延迟统计
  domestic_avg_latency_ms: 150
  international_avg_latency_ms: 1200
  
  # 代理使用统计
  proxy_usage:
    socks5: 95%
    http: 5%
    direct: 60%
```

---

## 🔧 配置检查清单

### 系统检查

```bash
# 1. 检查代理是否运行
curl -x socks5://127.0.0.1:7890 https://api.openai.com

# 2. 检查国内直连
curl https://dashscope.aliyuncs.com

# 3. 检查 Geo Router Skill
cd /home/nicola/.openclaw/workspace
python3 -c "from skills.geo_model_router.geo_router import GeoRouter; print('✅ GeoRouter OK')"
```

### 配置验证

```python
from skills.geo_model_router.geo_router import GeoRouter

router = GeoRouter()

# 测试国内服务
result = router.detect_route("https://dashscope.aliyuncs.com")
assert result.proxy == "domestic", "国内服务应直连"

# 测试国外服务
result = router.detect_route("https://api.openai.com")
assert result.proxy == "international", "国外服务应代理"

print("✅ 所有测试通过")
```

---

## ⚠️ 注意事项

### 1. 代理依赖

- 确保代理软件运行 (Mihomo/Clash/V2Ray 等)
- 默认端口：7890 (SOCKS5) / 7891 (HTTP)
- 代理故障时自动降级为直连

### 2. 缓存策略

- 路由决策缓存 300 秒
- 缓存命中可提升性能
- 清除缓存：`router.clear_cache()`

### 3. 故障切换

- 直连超时：3 秒
- 自动切换代理
- 记录故障到日志

### 4. 隐私保护

- 国内数据不出境
- 国外数据走加密代理
- 不记录敏感信息

---

## 📚 相关文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `SKILL.md` | 本文档 | `skills/geo-model-router/` |
| `geo_router.py` | 路由核心 | `skills/geo-model-router/` |
| `domestic_services.yaml` | 国内服务列表 | `skills/geo-model-router/config/` |
| `international_services.yaml` | 国外服务列表 | `skills/geo-model-router/config/` |
| `proxy_config.yaml` | 代理配置 | `skills/geo-model-router/config/` |

---

## 🎯 下一步

- [ ] 创建 `geo_router.py` 核心实现
- [ ] 配置国内/国外服务白名单
- [ ] 配置代理连接参数
- [ ] 测试自动路由功能
- [ ] 集成到现有技能系统

---

*版本：1.0.0 | 创建时间：2026-04-08 | 状态：✅ 已创建*
