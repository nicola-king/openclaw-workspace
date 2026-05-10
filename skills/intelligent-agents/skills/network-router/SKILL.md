# Network Router - 智能网络路由模块 v1.0

> **版本**: 1.0.0  
> **创建时间**: 2026-05-04  
> **职责**: 四层智能路由，国内外流量自动分流  
> **状态**: ✅ 已部署

---

## 🎯 职责域

**核心功能**: 智能网络路由 + 域名分类 + AI节点绕过

**路由规则**:
| 流量类型 | 路由 | 说明 |
|----------|------|------|
| 国内互联网 | 直连 | 百度/腾讯/阿里/字节跳动等 |
| 国内软件 | 直连 | 微信/钉钉/飞书/支付宝等 |
| 国内AI大模型 | 直连 | DeepSeek/月之暗面/百度/阿里/智谱等 |
| 国际互联网 | 代理 | Google/GitHub/Telegram/Docker等 |
| 国际AI大模型 | 代理 | OpenAI/Anthropic/Google/Meta等 |
| 香港AI节点 | 绕过 | 自动跳转美/日/新/韩节点 |

---

## 🧠 四层智能路由

### 第一层：流量分类

```python
domain -> classify()
  ├── 国内域名 (.cn, *.baidu.com 等)   → 直连
  ├── 国际域名 (*.openai.com 等)       → 代理
  ├── AI平台 (deepseek/openai 等)      → 按规则路由
  └── 未知                             → 代理 (安全优先)
```

### 第二层：香港节点检测

```python
domain -> detect_hk()
  ├── .hk 域名                         → 绕过
  ├── hongkong/hkg 关键词              → 绕过
  └── 已知HK端点                       → 重定向到US/JP/SG
```

### 第三层：健康检查

```python
health_check():
  ├── 代理连接测试                     → 每60秒自动检测
  ├── 失败重试 (3次)                   → 5秒间隔
  └── 全部失败                         → 回退直连
```

### 第四层：环境变量注入

```python
run_with_routing(command, target_domain):
  ├── 国内 → unset http_proxy/https_proxy
  ├── 国际 → set http_proxy/https_proxy
  └── HK   → set proxy + HK_BYPASS标记
```

---

## 🚀 使用说明

### 基础用法

```bash
# 查看路由状态
python3 src/router.py --status

# 测试域名路由
python3 src/router.py --route api.openai.com
python3 src/router.py --route www.baidu.com

# 代理健康检查
python3 src/router.py --health

# 运行完整测试
python3 src/router.py --test
```

### Python API

```python
from src.router import NetworkRouter

router = NetworkRouter()

# 分类域名
route = router.classify_domain("api.openai.com")  # "international"
route = router.classify_domain("open.feishu.cn")   # "domestic"

# 获取环境变量
env = router.get_routing_env("api.openai.com")
# -> {"http_proxy": "http://127.0.0.1:7890", ...}

# 在正确路由下执行命令
result = router.run_with_routing(
    ["curl", "-s", "https://api.openai.com/v1/models"],
    target_domain="api.openai.com"
)

# 获取AI平台最优端点
endpoint = router.get_optimal_endpoint("openai")

# 代理健康检查
healthy = router.health_check()
```

---

## 📊 路由测试示例

```
🟢 [国内  ] www.baidu.com                       -> 直连
🟢 [国内  ] open.feishu.cn                      -> 直连
🟢 [国内  ] api.deepseek.com                    -> 直连
🔵 [国际  ] api.openai.com                      -> 代理
🔵 [国际  ] github.com                          -> 代理
🔵 [国际  ] pypi.org                            -> 代理
🔴 [HK    ] api-hk.openai.com                   -> 代理 ⚠️ 香港绕过
🔴 [HK    ] hk.api.anthropic.com                -> 代理 ⚠️ 香港绕过
```

---

## 🔧 配置

配置文件: `config/routing-config.json`

**主要配置项**:
| 配置 | 说明 | 默认 |
|------|------|------|
| proxy.http | HTTP代理地址 | 127.0.0.1:7890 |
| proxy.https | HTTPS代理地址 | 127.0.0.1:7890 |
| proxy.socks | SOCKS代理地址 | 127.0.0.1:7891 |
| routing_rules.domains_domestic | 国内域名列表 | 50+ 域名 |
| routing_rules.domains_international | 国际域名列表 | 30+ 域名 |
| ai_platforms.domestic | 国内AI平台 | 11 个 |
| ai_platforms.international | 国际AI平台 | 10 个 |
| ai_platforms.hk_nodes | 香港节点屏蔽 | 已配置 |
| intelligent_switching | 智能切换参数 | 自动 |

---

## 🔄 与Scheduler集成

Network Router 自动集成到 Scheduler Agent：
- 每次执行任务前自动判断流量类型
- 根据流量类型配置正确的代理环境
- 每60秒自动检测代理健康
- 失败时自动回退直连

---

*太一 AGI · Network Router · 2026-05-04*
