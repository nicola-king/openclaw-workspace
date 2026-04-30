# 太一智能自动化架构

> 版本：v1.0 | 创建：2026-03-28 22:15
> 原则：各自独立，互联互通

---

## 📊 三大智能自动化模块

```
太一智能自动化系统
├── 🧠 大模型智能自动化 (smart-ai-router)
│   ├── 职责：AI 模型选择与调度
│   ├── 配置：百炼/Gemini/本地/Claude
│   └── 依赖：智能网关 (流量路由)
│
├── 🌐 网关智能自动化 (smart-gateway)
│   ├── 职责：流量路由选择
│   ├── 配置：国内/代理/本地
│   └── 依赖：无 (基础服务)
│
└── 💬 通讯智能自动化 (smart-communication)
    ├── 职责：通讯渠道路由
    ├── 配置：飞书/微信/Telegram
    └── 依赖：智能网关 (流量路由)
```

---

## 📁 Skill 目录结构

```
~/.openclaw/workspace/skills/taiyi/
├── smart-ai-router/          # 大模型智能自动化
│   ├── SKILL.md              # Skill 文档
│   ├── smart_ai_router.py    # 路由器核心
│   ├── quota_monitor.py      # 额度监控
│   └── models/               # 模型配置
│       ├── bailian.yaml      # 百炼配置
│       ├── gemini.yaml       # Gemini 配置
│       └── local.yaml        # 本地配置
│
├── smart-gateway/            # 网关智能自动化
│   ├── SKILL.md              # Skill 文档
│   ├── smart_gateway.py      # 网关核心
│   └── config/               # 路由配置
│       ├── domestic.yaml     # 国内域名白名单
│       └── international.yaml # 国外域名白名单
│
└── smart-communication/      # 通讯智能自动化 🆕
    ├── SKILL.md              # Skill 文档
    ├── smart_communication.py # 通讯路由器
    ├── channels/             # 通讯渠道
    │   ├── feishu.py         # 飞书 (国内流量)
    │   ├── wechat.py         # 微信 (国内流量)
    │   └── telegram.py       # Telegram (代理流量)
    └── config/               # 渠道配置
        ├── feishu.yaml       # 飞书配置
        ├── wechat.yaml       # 微信配置
        └── telegram.yaml     # Telegram 配置
```

---

## 🔗 互联互通协议

### 依赖关系

```
智能网关 (基础服务)
    ↓
大模型路由器 (调用网关)
    ↓
通讯路由器 (调用网关 + 大模型)
```

### 统一接口

```python
# 所有 Skill 实现统一接口
class SmartModule:
    """智能模块基类"""
    
    def __init__(self):
        self.gateway = SmartGateway()  # 依赖智能网关
    
    def route(self, request):
        """路由请求"""
        pass
    
    def get_status(self):
        """获取状态"""
        pass
```

### 配置共享

```yaml
# shared_config.yaml
# 所有 Skill 共享的配置

gateway:
  proxy_server: "127.0.0.1:7890"
  domestic_domains:
    - aliyun.com
    - wechat.com
    - feishu.cn

ai_models:
  bailian:
    api_key: "${DASHSCOPE_API_KEY}"
    endpoint: "https://dashscope.aliyun.com"
    traffic: "domestic"  # 国内流量
  
  gemini:
    api_key: "${GEMINI_API_KEY}"
    endpoint: "https://generativelanguage.googleapis.com"
    traffic: "proxy"  # 代理流量

communication:
  feishu:
    app_id: "${FEISHU_APP_ID}"
    app_secret: "${FEISHU_APP_SECRET}"
    traffic: "domestic"
  
  wechat:
    app_id: "${WECHAT_APP_ID}"
    app_secret: "${WECHAT_APP_SECRET}"
    traffic: "domestic"
  
  telegram:
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    traffic: "proxy"
```

---

## 📊 流量路由规则

### 大模型智能自动化

| 模型 | 端点 | 流量类型 | 网关路由 |
|------|------|---------|---------|
| 百炼 | dashscope.aliyun.com | 🇨🇳 国内 | 直连 |
| Gemini | googleapis.com | 🌐 国际 | 代理 |
| 本地 | localhost:11434 | 🏠 本地 | 直连 |
| Claude | anthropic.com | 🌐 国际 | 代理 |

### 通讯智能自动化

| 渠道 | 端点 | 流量类型 | 网关路由 |
|------|------|---------|---------|
| 飞书 | open.feishu.cn | 🇨🇳 国内 | 直连 |
| 微信 | api.weixin.qq.com | 🇨🇳 国内 | 直连 |
| Telegram | api.telegram.org | 🌐 国际 | 代理 |

---

## 🚀 快速启动

```bash
# 1. 启动智能网关 (基础服务)
python3 ~/.openclaw/workspace/skills/taiyi/smart-gateway/smart_gateway.py

# 2. 启动大模型路由器
python3 ~/.openclaw/workspace/skills/taiyi/smart-ai-router/smart_ai_router.py

# 3. 启动通讯路由器
python3 ~/.openclaw/workspace/skills/taiyi/smart-communication/smart_communication.py

# 4. 查看整体状态
python3 ~/.openclaw/workspace/skills/taiyi/show_status.py
```

---

## 📋 使用示例

### 示例 1: 发送消息 (自动选择渠道和流量)

```python
from smart_communication import SmartCommunication

comm = SmartCommunication()

# 发送飞书消息 (自动走国内流量)
comm.send_feishu(
    channel="太一通知",
    message="百炼额度使用率已达 85%"
)

# 发送 Telegram 消息 (自动走代理流量)
comm.send_telegram(
    chat_id="@sayelf_channel",
    message="Gemini 额度剩余 1200 次"
)
```

### 示例 2: AI 调用 (自动选择模型和流量)

```python
from smart_ai_router import SmartAIRouter

router = SmartAIRouter()

# 代码任务 (自动选择百炼，走国内流量)
result = router.call(
    task="写一个 Python 函数",
    type="code"
)

# 文档任务 (自动选择 Gemini，走代理流量)
result = router.call(
    task="写一篇技术文档",
    type="document"
)
```

### 示例 3: 完整流程

```python
from smart_ai_router import SmartAIRouter
from smart_communication import SmartCommunication
from smart_gateway import SmartGateway

# 初始化
gateway = SmartGateway()
ai_router = SmartAIRouter()
comm = SmartCommunication()

# 任务：分析数据并发送报告
task = "分析这份销售数据，找出趋势"

# 1. 智能选择 AI 模型
model = ai_router.select_model(task)  # 返回：gemini

# 2. 调用 AI (自动走代理流量)
result = ai_router.call(task)

# 3. 发送报告到飞书 (自动走国内流量)
comm.send_feishu(
    channel="数据分析报告",
    message=result
)
```

---

## 🔒 安全配置

### 环境变量

```bash
# ~/.bashrc

# AI API Keys
export DASHSCOPE_API_KEY="sk-xxx"
export GEMINI_API_KEY="xxx"
export ANTHROPIC_API_KEY="sk-ant-xxx"

# 通讯配置
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export WECHAT_APP_ID="wx_xxx"
export WECHAT_APP_SECRET="xxx"
export TELEGRAM_BOT_TOKEN="xxx:xxx"

# 代理配置
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

### 配置文件加密

```bash
# 敏感配置使用加密
gpg -c config/secrets.yaml
# 解密
gpg -d config/secrets.yaml.gpg
```

---

## 📊 监控与告警

### 健康检查

```python
# health_check.py

def check_all_modules():
    """检查所有模块状态"""
    status = {
        'gateway': gateway.get_status(),
        'ai_router': ai_router.get_status(),
        'communication': comm.get_status(),
    }
    
    # 发送健康报告
    if any(s['status'] != 'ok' for s in status.values()):
        comm.send_alert("⚠️ 模块异常", status)
    
    return status
```

### 定时任务

```bash
# crontab -e

# 每小时健康检查
0 * * * * python3 ~/.openclaw/workspace/skills/taiyi/health_check.py

# 每日额度报告
0 9 * * * python3 ~/.openclaw/workspace/skills/taiyi/daily_report.py
```

---

*版本：v1.0 | 创建时间：2026-03-28 22:15*
*原则：各自独立，互联互通*
*太一 AGI · 三大智能自动化架构*
