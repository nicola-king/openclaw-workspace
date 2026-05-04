# 太一飞书集成 (Taiyi Feishu Integration)

> **版本**: v1.0
> **创建时间**: 2026-05-04
> **作者**: 太一 AGI
> **类别**: 集成/消息推送/协作
> **状态**: ✅ 已部署

---

## 🎯 职责域

**核心功能**: 太一系统与飞书生态的无缝集成

**适用场景**:
- 系统状态推送至飞书群/用户
- 接收飞书指令并路由到对应Agent
- 任务完成通知
- 告警信息实时推送
- 日报/周报自动发送
- 多Bot协作消息中转

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    太一系统 (Taiyi System)                │
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ 跨境贸易 │  │ 旅游探路 │  │ OSINT   │  │ TTS     │   │
│  │ Agent   │  │ Agent   │  │ Agent   │  │ Agent   │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
│       │            │            │            │         │
│       └────────────┴────────────┴────────────┘         │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              飞书集成层 (Feishu Integration)       │   │
│  │                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │ 消息推送  │  │ 指令接收  │  │ 事件处理  │      │   │
│  │  │ Push     │  │ Command  │  │ Event    │      │   │
│  │  └──────────┘  └──────────┘  └──────────┘      │   │
│  │                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │ 群管理   │  │ 用户管理  │  │ 模板消息  │      │   │
│  │  │ Group    │  │ User     │  │ Template │      │   │
│  │  └──────────┘  └──────────┘  └──────────┘      │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              飞书开放平台 (Feishu Open Platform)   │   │
│  │                                                  │   │
│  │  Webhook │ Bot API │ Event Callback │ Auth      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 核心组件

### 1. 消息推送 (Push)

**功能**: 将太一系统内部信息推送至飞书

**支持消息类型**:
| 类型 | 说明 | 使用场景 |
|------|------|---------|
| 文本 | 纯文本消息 | 简单通知 |
| Markdown | 富文本消息 | 格式化报告 |
| 卡片 | 交互式卡片 | 任务状态 |
| 图片 | 图片消息 | 图表/截图 |
| 文件 | 文件消息 | 文档传输 |

**推送目标**:
- 个人用户 (Open ID)
- 群组 (Chat ID)
- 部门 (Department ID)

### 2. 指令接收 (Command)

**功能**: 接收飞书用户指令，路由到对应Agent

**指令格式**:
```
@太一 /命令 参数
```

**支持命令**:
| 命令 | 功能 | 路由目标 |
|------|------|---------|
| `/汇率` | 查询汇率 | 跨境贸易Agent |
| `/选品` | 智能选品 | 跨境贸易Agent |
| `/旅游` | 旅游规划 | 旅游探路者 |
| `/搜索` | 全网搜索 | 共享搜索服务 |
| `/tts` | 语音合成 | MOSS-TTS |
| `/osint` | 数字足迹 | Maigret |
| `/状态` | 系统状态 | 太一 |
| `/日报` | 生成日报 | 太一 |
| `/周报` | 生成周报 | 太一 |

### 3. 事件处理 (Event)

**功能**: 处理飞书平台事件

**支持事件**:
| 事件 | 说明 | 处理 |
|------|------|------|
| 消息接收 | 用户@Bot | 解析指令并执行 |
| 群加入 | Bot被拉入群 | 发送欢迎消息 |
| 卡片点击 | 用户点击卡片按钮 | 执行对应操作 |
| 审批通过 | 审批流程完成 | 触发后续动作 |

---

## 📡 系统内部信息集成

### 信息来源

太一飞书集成采用系统内部信息，不依赖外部API:

```
系统内部信息
├── Agent状态
│   ├── 跨境贸易Agent运行状态
│   ├── 旅游探路者任务队列
│   ├── OSINT扫描进度
│   └── TTS合成任务
├── 任务执行结果
│   ├── 搜索结果
│   ├── 分析报告
│   ├── 选品建议
│   └── 旅游方案
├── 系统监控
│   ├── CPU/内存使用
│   ├── 磁盘空间
│   ├── 网络状态
│   └── 服务健康度
├── 定时任务
│   ├── 日报生成状态
│   ├── 周报生成状态
│   ├── 数据备份状态
│   └── 系统自检状态
└── 告警信息
    ├── 服务异常
    ├── 任务失败
    ├── 资源不足
    └── 安全事件
```

### 信息流转

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  系统内部    │────▶│  飞书集成层  │────▶│  飞书平台   │
│  信息源     │     │  格式化     │     │  推送       │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  消息模板   │
                   │  Markdown │
                   │  卡片模板  │
                   └─────────────┘
```

---

## 🚀 使用方式

### 1. 配置飞书应用

```yaml
# config/feishu.yaml
app_id: "cli_xxxxxxxxxxxx"
app_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
encrypt_key: "xxxxxxxxxxxxxxxx"
verification_token: "xxxxxxxxxxxxxxxx"

# 推送配置
webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# 目标配置
default_chat_id: "oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
admin_open_id: "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 2. 发送消息

```python
from skills.feishu_integration import FeishuIntegration

# 初始化
feishu = FeishuIntegration()

# 发送文本消息
feishu.send_text("系统启动完成", chat_id="oc_xxx")

# 发送Markdown报告
feishu.send_markdown("""
# 日报

## 今日完成
- 跨境贸易Agent: 5个任务
- 旅游探路者: 3个查询

## 系统状态
- CPU: 45%
- 内存: 60%
""")

# 发送卡片消息
feishu.send_card({
    "header": {"title": "任务完成"},
    "elements": [
        {"tag": "div", "text": "选品分析完成"},
        {"tag": "action", "actions": [
            {"tag": "button", "text": "查看详情", "url": "..."}
        ]}
    ]
})
```

### 3. 接收指令

```python
# 在飞书事件回调中
@feishu.on_message
def handle_message(message):
    text = message.get("text", "")
    
    if text.startswith("/汇率"):
        # 路由到跨境贸易Agent
        result = cross_border_agent.get_exchange_rate()
        feishu.reply(result)
    
    elif text.startswith("/旅游"):
        # 路由到旅游探路者
        result = travel_explorer.plan_trip(text)
        feishu.reply(result)
```

---

## 📊 消息模板

### 系统状态卡片

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "🤖 太一系统状态"},
    "template": "blue"
  },
  "elements": [
    {
      "tag": "div",
      "text": {
        "tag": "lark_md",
        "content": "**运行时间**: 24h\n**Agent数**: 5\n**任务队列**: 3"
      }
    },
    {
      "tag": "hr"
    },
    {
      "tag": "action",
      "actions": [
        {"tag": "button", "text": {"tag": "plain_text", "content": "查看详情"}, "type": "primary"}
      ]
    }
  ]
}
```

### 任务完成通知

```markdown
## ✅ 任务完成

**任务**: 跨境贸易选品分析
**耗时**: 2.3s
**结果**: 找到3个高潜力产品

| 产品 | 评分 | 利润 |
|------|------|------|
| 智能水杯 | 92 | 45% |
| 便携风扇 | 88 | 38% |
| 无线充电器 | 85 | 42% |

[查看详情](链接)
```

---

## 🔒 安全与权限

### 信息分级

| 级别 | 信息类型 | 推送范围 |
|------|---------|---------|
| 公开 | 系统状态、任务完成 | 所有群 |
| 内部 | 分析报告、选品建议 | 工作群 |
| 敏感 | 客户数据、交易信息 | 私聊管理员 |
| 机密 | API密钥、配置信息 | 不推送 |

### 权限控制

```python
# 权限检查
def check_permission(user_id, message_type):
    if message_type == "sensitive" and user_id not in ADMIN_LIST:
        return False
    return True
```

---

## 📈 监控与统计

### 推送统计

| 指标 | 说明 |
|------|------|
| 日推送量 | 每日消息推送次数 |
| 成功率 | 推送成功比例 |
| 响应时间 | 平均响应时间 |
| 活跃用户 | 交互用户数 |

### 指令统计

| 指标 | 说明 |
|------|------|
| 指令分布 | 各命令使用频率 |
| 响应时间 | 指令处理时间 |
| 错误率 | 指令失败比例 |
| 用户满意度 | 反馈评分 |

---

## 🧪 测试

```bash
# 测试消息推送
python3 skills/feishu-integration/test_push.py

# 测试指令接收
python3 skills/feishu-integration/test_command.py

# 测试事件处理
python3 skills/feishu-integration/test_event.py
```

---

## 📁 文件结构

```
skills/feishu-integration/
├── SKILL.md                          # 技能说明
├── feishu_integration.py             # 核心集成类
├── message_templates.py              # 消息模板
├── command_router.py                 # 指令路由
├── event_handler.py                  # 事件处理
├── config.yaml                       # 配置文件
├── test_push.py                      # 推送测试
├── test_command.py                   # 指令测试
└── test_event.py                     # 事件测试
```

---

## 🔄 与现有系统集成

### 已集成
- ✅ 跨境贸易Agent - 汇率/选品/物流查询
- ✅ 旅游探路者 - 行程规划
- ✅ 共享搜索服务 - 全网搜索
- ✅ 系统监控 - 状态推送

### 待集成
- 🟡 MOSS-TTS - 语音消息
- 🟡 Maigret - OSINT报告推送
- 🟡 定时任务 - 日报/周报自动发送

---

## 🎯 未来扩展

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 审批集成 | P1 | 任务审批流程 |
| 日历集成 | P1 | 日程管理 |
| 文档协作 | P2 | 飞书文档操作 |
| 多维表格 | P2 | 数据表格管理 |
| 视频会议 | P3 | 会议控制 |

---

*太一 AGI · 飞书集成技能 v1.0*
*创建时间: 2026-05-04*
*核心能力: 系统内部信息 → 飞书平台无缝推送*
