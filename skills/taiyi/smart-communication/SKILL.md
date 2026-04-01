# 通讯智能自动化 Skill

> 版本：v1.0 | 创建：2026-03-28 22:15
> 职责：通讯渠道路由与消息分发
> 流量：飞书/微信→国内，Telegram→代理

---

## 🎯 功能概述

| 功能 | 描述 | 流量类型 | 状态 |
|------|------|---------|------|
| **飞书消息** | 开放平台 API | 🇨🇳 国内 | 🟡 待配置 |
| **微信消息** | 公众号/企业微信 | 🇨🇳 国内 | 🟡 待配置 |
| **Telegram 消息** | Bot API | 🌐 代理 | ✅ 已配置 |
| **智能路由** | 根据渠道自动选择流量 | 自动 | ✅ |
| **消息队列** | 批量发送/重试 | 自动 | 🟡 待开发 |

---

## 📊 渠道配置

### 飞书 (国内流量)

| 项目 | 配置 |
|------|------|
| **API 端点** | https://open.feishu.cn |
| **流量类型** | 🇨🇳 国内直连 |
| **App ID** | cli_a9086d6b5779dcc1 (太一) |
| **App Secret** | 已配置 |
| **用途** | 内部通知/日报/周报 |

### 微信 (国内流量)

| 项目 | 配置 |
|------|------|
| **API 端点** | https://api.weixin.qq.com |
| **流量类型** | 🇨🇳 国内直连 |
| **公众号** | SAYELF 山野精灵 |
| **AppID** | wx720a4c489fec9df3 |
| **用途** | 公众号推送/模板消息 |

### Telegram (代理流量)

| 项目 | 配置 |
|------|------|
| **API 端点** | https://api.telegram.org |
| **流量类型** | 🌐 代理 (7890 端口) |
| **Bot** | @sayelfbot (太一) |
| **用途** | 即时通知/用户交互 |

---

## 🔧 依赖关系

```
通讯智能自动化
├── 依赖：智能网关 (流量路由)
├── 依赖：大模型路由器 (AI 生成内容)
└── 被依赖：太一核心系统
```

---

## 🚀 快速启动

```bash
# 1. 安装依赖
pip3 install requests aiohttp

# 2. 配置环境变量
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export WECHAT_APP_ID="wx_xxx"
export WECHAT_APP_SECRET="xxx"
export TELEGRAM_BOT_TOKEN="xxx:xxx"

# 3. 测试通讯路由器
python3 ~/.openclaw/workspace/skills/taiyi/smart-communication/smart_communication.py
```

---

## 📋 使用示例

### 示例 1: 发送消息

```python
from smart_communication import SmartCommunication

comm = SmartCommunication()

# 发送飞书消息 (自动走国内流量)
comm.send_feishu(
    user_id="ou_xxx",
    message="百炼额度使用率已达 85%"
)

# 发送微信消息 (自动走国内流量)
comm.send_wechat(
    openid="xxx",
    message="公众号文章已发布"
)

# 发送 Telegram 消息 (自动走代理流量)
comm.send_telegram(
    chat_id="@sayelf_channel",
    message="系统告警：额度即将用完"
)
```

### 示例 2: 智能路由

```python
# 根据消息类型自动选择渠道
comm.send(
    message="日报已生成",
    priority="high",  # 高优先级→Telegram
    channels=["feishu", "telegram"]
)

comm.send(
    message="周报汇总",
    priority="normal",  # 普通→飞书
    channels=["feishu"]
)
```

---

## 📊 状态监控

```bash
# 查看通讯渠道状态
python3 smart_communication.py --status

# 测试所有渠道
python3 smart_communication.py --test
```

---

*版本：v1.0 | 创建时间：2026-03-28 22:15*
*太一 AGI · 通讯智能自动化*
