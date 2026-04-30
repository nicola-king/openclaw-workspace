# 网关路由与智能自动化分流配置

**更新时间**: 2026-04-08 15:17  
**状态**: ✅ 生产环境运行中

---

## 🎯 网关路由架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户请求入口                          │
│         Telegram / 飞书 / 微信 / API                     │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│              OpenClaw Gateway (端口 18789)               │
│  - 认证验证 (Token)                                      │
│  - 通道分发 (Telegram/Feishu/WeChat)                    │
│  - 会话管理 (Session)                                    │
│  - 插件加载 (plugins.allow 白名单)                       │
└────────────┬────────────────────┬────────────────────────┘
             ↓                    ↓
    ┌────────────────┐   ┌────────────────┐
    │  主会话 (main)  │   │  专项会话      │
    │  qwen3.5-plus  │   │  weixin/feishu │
    └───────┬────────┘   └────────────────┘
            ↓
┌─────────────────────────────────────────────────────────┐
│              太一 AGI (主 Agent)                         │
│  - 意图识别                                              │
│  - 任务分类                                              │
│  - Bot 调度                                              │
│  - 模型路由                                              │
└────────────┬────────────────────┬────────────────────────┘
             ↓                    ↓
    ┌────────────────┐   ┌────────────────┐
    │  Bot 能力层     │   │  模型路由层    │
    │  知几/山木/...  │   │  Smart Router  │
    └────────────────┘   └────────────────┘
```

---

## ⚙️ Gateway 核心配置

**配置文件**: `/home/nicola/.openclaw/openclaw.json`

### 基础配置

```json
{
  "gateway": {
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "89e5f8f7165421e1d1579cdcb3a335f282c432b79d4d9e21"
    },
    "port": 18789,
    "bind": "loopback",
    "trustedProxies": ["127.0.0.1", "::1"],
    "controlUi": {
      "allowInsecureAuth": false
    }
  }
}
```

### 安全配置

```json
{
  "plugins": {
    "allow": [
      "qwen",
      "openclaw-wechat"
    ],
    "entries": {
      "qwen": {"enabled": true},
      "openclaw-wechat": {"enabled": true}
    }
  },
  "gateway": {
    "nodes": {
      "denyCommands": [
        "canvas.present",
        "canvas.hide",
        "canvas.navigate",
        "camera.snap",
        "screen.record",
        "contacts.add",
        "sms.send"
      ]
    }
  }
}
```

---

## 🧠 智能模型路由 (Smart Model Router)

**配置文件**: `/home/nicola/.openclaw/openclaw.json`

### 大模型配置

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "qwen": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus",
            "contextWindow": 1000000,
            "maxTokens": 65536,
            "cost": {"input": 0, "output": 0}
          },
          {
            "id": "qwen3-coder-plus",
            "name": "qwen3-coder-plus",
            "contextWindow": 1000000,
            "maxTokens": 65536,
            "reasoning": false
          },
          {
            "id": "MiniMax-M2.5",
            "name": "MiniMax-M2.5",
            "reasoning": true,
            "contextWindow": 1000000
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "qwen/qwen3.5-plus"
      },
      "compaction": {
        "mode": "safeguard"
      }
    }
  }
}
```

### 三层模型池

```
┌─────────────────────────────────────────┐
│  Layer 1: 本地模型 (免费·零延迟)          │
│  - Qwen 2.5 7B (Ollama)                 │
│  适用：快速推理·简单任务·高频调用         │
└─────────────────────────────────────────┘
              ↓ (复杂任务上移)
┌─────────────────────────────────────────┐
│  Layer 2: 云端主力 (性价比·通用)          │
│  - qwen3.5-plus (¥40/月)                │
│  适用：日常对话·中等任务·Bot 调度          │
└─────────────────────────────────────────┘
              ↓ (长文本/代码)
┌─────────────────────────────────────────┐
│  Layer 3: 云端专项 (强大·昂贵)            │
│  - Gemini 2.5 Pro (¥145/月)             │
│  - qwen3-coder-plus (代码专项)           │
│  适用：长文本·复杂推理·代码·战略           │
└─────────────────────────────────────────┘
```

---

## 🤖 智能分流决策树

### 自动路由规则

```
用户请求
  ↓
[1] 是否需要联网搜索？
  ├─ 是 → qwen3.5-plus
  └─ 否 ↓
[2] 是否超过 10K tokens？
  ├─ 是 → qwen3.5-plus / Gemini
  └─ 否 ↓
[3] 是否是代码任务？
  ├─ 是 → qwen3-coder-plus
  └─ 否 ↓
[4] 是否是简单任务？
  ├─ 是 (问答/翻译/润色) → ✅ Qwen 2.5 7B (本地)
  └─ 否 (复杂推理) → qwen3.5-plus
[5] 是否是长文档/多来源？
  ├─ 是 → Gemini 2.5 Pro
  └─ 否 → qwen3.5-plus
```

### 任务分类路由表

| 任务类型 | 示例 | 自动路由 | 理由 |
|---------|------|---------|------|
| **简单问答** | "1+1 等于几" | Qwen 2.5 7B | 本地快速响应 |
| **快速翻译** | "翻译成英文" | Qwen 2.5 7B | 本地零成本 |
| **文本润色** | "优化这句话" | Qwen 2.5 7B | 简单任务 |
| **日常对话** | "你好/谢谢" | Qwen 2.5 7B | 高频低复杂度 |
| **事实查询** | "中国首都是？" | Qwen 2.5 7B | 知识库内 |
| **复杂推理** | "分析市场趋势" | qwen3.5-plus | 需要强推理 |
| **代码生成** | "写个 Python 脚本" | qwen3-coder-plus | 专业代码模型 |
| **长文档分析** | "总结这份 100 页报告" | Gemini 2.5 Pro | 1M 上下文窗口 |
| **多来源汇总** | "整合 5 份研报" | Gemini 2.5 Pro | 多文档处理 |
| **战略规划** | "制定 Q2 计划" | qwen3.5-plus | 高质量决策 |
| **情感支持** | "我心情不好" | qwen3.5-plus (共情模式) | 情感感知 |

---

## 📡 通道分流配置

### Telegram 通道

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY",
      "groups": {
        "*": {
          "requireMention": true
        }
      }
    }
  }
}
```

### 飞书通道

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a9086d6b5779dcc1",
      "appSecret": "tXHOop03ZHQynCRuEPkambASNori3KhZ"
    }
  }
}
```

### 会话分流

| 会话类型 | 会话 Key | 模型 | 用途 |
|---------|---------|------|------|
| **主会话** | `agent:main:telegram:direct:7073…` | qwen3.5-plus | 主要对话 (187k/1000k) |
| **飞书会话** | `agent:main:feishu:direct:ou_73a…` | qwen3.5-plus | 飞书通道 (32k/1000k) |
| **微信会话** | `agent:main:openclaw-weixin:3df0…` | qwen3.5-plus | 微信通道 (29k/1000k) |
| **默认会话** | `agent:main:main` | qwen3.5-plus | 备用会话 (36k/1000k) |

---

## 🔄 智能自动化分流

### 任务发现层

```yaml
# HEARTBEAT.md 待办事项
- 定时任务 (Cron)
  - 06:00 宪法学习
  - 23:00 日报生成
  - 每小时 任务健康检查
  - 每 30 分钟 自愈恢复
- 事件触发 (Webhook)
  - GitHub Issue
  - Polymarket 信号
  - 邮件通知
```

### 任务调度层

```
任务发现
    ↓
太一意图识别
    ↓
┌─────────────────────────────────┐
│  任务分类                        │
├─────────────────────────────────┤
│  P0: 紧急重要 (5 分钟内执行)     │
│  P1: 重要不紧急 (加入 HEARTBEAT) │
│  P2: 常规任务 (记录待办)         │
│  阻塞：跳过 + 记录原因           │
└─────────────────────────────────┘
    ↓
Bot 职责域匹配
    ↓
┌─────────────────────────────────┐
│  Bot 分配                        │
├─────────────────────────────────┤
│  知几：量化交易/数据分析         │
│  山木：内容创意/业务执行         │
│  素问：技术研究/系统开发         │
│  罔两：市场情报/竞品监控         │
│  庖丁：财务成本/预算控制         │
└─────────────────────────────────┘
```

### 执行监控层

```yaml
# 5 分钟进度汇报
reportProgress:
  enabled: true
  triggerOnTask: true
  taskInterval: 300  # 5 分钟
  idleInterval: 43200  # 12 小时

# 自愈恢复
selfHeal:
  enabled: true
  interval: 1800  # 30 分钟
  maxRetries: 3

# 健康检查
healthCheck:
  enabled: true
  interval: 3600  # 每小时
```

---

## 📊 当前分流状态

### 会话使用情况

| 会话 | Token 使用 | 状态 |
|------|-----------|------|
| 主会话 (Telegram) | 187k/1000k (19%) | ✅ 活跃 |
| 飞书会话 | 32k/1000k (3%) | ✅ 活跃 |
| 微信会话 | 29k/1000k (3%) | ✅ 活跃 |
| 默认会话 | 36k/1000k (4%) | ✅ 活跃 |

### 模型使用情况

| 模型 | 使用场景 | 成本 |
|------|---------|------|
| **qwen3.5-plus** | 主力模型 (80% 任务) | ¥40/月 |
| **qwen3-coder-plus** | 代码任务 (10%) | 包含 |
| **MiniMax-M2.5** | 复杂推理 (5%) | 包含 |
| **本地 Qwen 2.5** | 简单任务 (5%) | 免费 |

### Bot 分流统计

| Bot | 职责 | 触发关键词 |
|-----|------|-----------|
| **太一** | 统筹决策 | 所有任务 |
| **知几** | 数据分析 | 数据/分析/图表/趋势 |
| **山木** | 内容创作 | 文章/文案/发布/小红书 |
| **素问** | 技术开发 | 代码/技术/开发/研究 |
| **罔两** | 市场情报 | 市场/竞品/价格/监控 |
| **庖丁** | 财务成本 | 成本/预算/财务/利润 |

---

## 🔧 配置优化建议

### 性能优化

1. **本地模型优先**: 简单任务自动使用 Qwen 2.5 7B
2. **会话复用**: 避免频繁创建新会话
3. **context 管理**: >80K 时建议切换新对话
4. **批量处理**: 相似任务合并处理

### 成本优化

1. **用量追踪**: 记录每个模型的使用量
2. **成本分析**: 定期审查模型使用成本
3. **免费优先**: 能使用免费模型就不用付费
4. **按需升级**: 复杂任务才用高端模型

### 安全优化

1. **插件白名单**: `plugins.allow` 限制可信插件
2. **命令限制**: `denyCommands` 禁止危险命令
3. **本地绑定**: Gateway 仅监听 loopback
4. **信任代理**: 配置可信反向代理 IP

---

## 📚 相关配置文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `openclaw.json` | 主配置文件 | `~/.openclaw/` |
| `MODEL-ROUTING.md` | 模型路由协议 | `constitution/skills/` |
| `smart-model-router/` | 智能路由技能 | `skills/` |
| `COLLABORATION.md` | 多 Bot 协作 | `constitution/` |
| `HEARTBEAT.md` | 核心待办 | `workspace/` |

---

**架构版本**: v4.0  
**最后更新**: 2026-04-08 15:17  
**系统状态**: ✅ 生产环境运行中
