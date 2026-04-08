# 按需响应协议（On-Demand Response Protocol）

> 创建时间：2026-04-03 14:30 | 版本：v1.0 | 优先级：宪法级 | 状态：✅ 激活

---

## 🎯 核心原则

**不请自来 = 打扰 · 按需响应 = 专业 · 静默值守 = 默认状态**

---

## 📋 响应触发条件

### ✅ 必须响应的场景

| 场景 | 触发条件 | 示例 |
|------|---------|------|
| **直接@提及** | 消息中包含 `@Bot 名` 或 `@太一` | "@太一 今天天气如何" |
| **直接提问** | 消息以问号结尾且上下文明确指向 Bot | "知几，这个交易怎么看？" |
| **命令触发** | 消息以 `/` 开头的命令 | `/日报` `/状态` `/自检` |
| **心跳轮询** | 系统心跳检查消息 | "Read HEARTBEAT.md..." |
| **任务委派** | SAYELF 明确指派任务 | "太一，处理这个" |
| **错误恢复** | 系统检测到错误需要人工确认 | "Git 推送失败，需要配置 remote" |

### ❌ 不响应的场景

| 场景 | 原因 | 处理方式 |
|------|------|---------|
| **群聊闲聊** | 与 Bot 无关的人类对话 | 静默监听，不响应 |
| **转发消息** | 纯转发无附加指令 | 不响应 |
| **表情/图片** | 无文字内容的媒体 | 不响应（除非配置了图像识别） |
| **系统通知** | 其他 Bot 或系统的自动消息 | 不响应（避免循环） |
| **历史消息** | 补发的旧消息（时间戳>5 分钟） | 不响应 |
| **重复消息** | 相同内容 5 分钟内重复 | 不响应（防 spam） |

---

## 🛠️ 实现逻辑

### 响应判断流程

```python
def should_respond(message, context):
    # 1. 检查是否被@提及
    if is_mentioned(message, context['bot_name']):
        return True, "mentioned"
    
    # 2. 检查是否是命令
    if message.strip().startswith('/'):
        return True, "command"
    
    # 3. 检查是否是心跳轮询
    if is_heartbeat_poll(message):
        return True, "heartbeat"
    
    # 4. 检查是否是 SAYELF 的直接指令
    if context['sender'] == 'SAYELF' and is_imperative(message):
        return True, "direct_order"
    
    # 5. 检查是否是错误恢复场景
    if context['is_error_recovery']:
        return True, "error_recovery"
    
    # 6. 检查群聊中是否被点名
    if context['chat_type'] == 'group' and is_named_in_group(message):
        return True, "group_mention"
    
    # 默认：不响应
    return False, "no_trigger"
```

### 响应延迟策略

| 优先级 | 场景 | 延迟 |
|--------|------|------|
| **P0** | 错误恢复/告警 | 立即（<5 秒） |
| **P1** | SAYELF 直接指令 | 快速（<30 秒） |
| **P2** | 普通@提及 | 正常（<60 秒） |
| **P3** | 心跳轮询 | 标准（按 Cron） |

---

## 📊 平台特定规则

### 微信（WeChat）

```yaml
响应触发:
  - @提及（群聊）
  - 私聊消息（默认响应，除非是转发/媒体）
  - 命令（/开头）
  
不响应:
  - 群聊中非@消息
  - 纯图片/视频（无文字）
  - 转发消息（无附加文字）
  
特殊规则:
  - 私聊默认响应（因为是一对一）
  - 群聊严格过滤（避免打扰）
```

### Telegram

```yaml
响应触发:
  - @提及（群聊）
  - 私聊消息
  - 命令（/开头）
  - Reply 到 Bot 的消息
  
不响应:
  - 群聊中非@消息
  - Channel 消息（除非配置了转发）
  
特殊规则:
  - 支持命令快捷方式（/daily, /status）
  - 支持 Inline Query（主动搜索时触发）
```

### 飞书（Feishu）

```yaml
响应触发:
  - @提及
  - 私聊消息
  - 命令
  
不响应:
  - 群聊中非@消息
  - 机器人消息（避免循环）
  
特殊规则:
  - 支持卡片消息交互
  - 支持审批流触发
```

---

## 🔧 配置参数

### 全局配置（`config/response-config.yaml`）

```yaml
response_policy:
  enabled: true
  mode: "on_demand"  # on_demand | always | never
  
  triggers:
    mention: true
    command: true
    heartbeat: true
    direct_order: true
    error_recovery: true
    
  filters:
    ignore_group_chat_without_mention: true
    ignore_forwarded_messages: true
    ignore_media_only: true
    ignore_old_messages_minutes: 5
    ignore_duplicate_messages_minutes: 5
    
  delays:
    p0_error_recovery_seconds: 5
    p1_direct_order_seconds: 30
    p2_mention_seconds: 60
    p3_heartbeat_seconds: 300  # 按 Cron
    
  rate_limits:
    max_responses_per_minute: 10
    max_responses_per_hour: 100
    cooldown_after_response_seconds: 30
```

### 平台配置（`config/platforms.yaml`）

```yaml
platforms:
  weixin:
    enabled: true
    private_chat_respond: true  # 私聊默认响应
    group_chat_respond: mention_only  # 群聊仅@响应
    
  telegram:
    enabled: true
    private_chat_respond: true
    group_chat_respond: mention_only
    channel_respond: false
    
  feishu:
    enabled: true
    private_chat_respond: true
    group_chat_respond: mention_only
```

---

## 📝 静默模式（特殊场景）

### 何时启用静默模式

| 场景 | 触发 | 持续时间 | 例外 |
|------|------|---------|------|
| **深夜勿扰** | 23:00-08:00 | 自动 | P0 告警 |
| **会议模式** | SAYELF 手动开启 | 自定义 | 仅 SAYELF 消息 |
| **专注模式** | 检测到高频输入 | 30 分钟 | 仅@提及 |
| **调试模式** | 系统维护时 | 手动 | 无 |

### 静默模式配置

```yaml
quiet_mode:
  night_hours:
    enabled: true
    start: "23:00"
    end: "08:00"
    exceptions:
      - "error_recovery"
      - "sayelf_direct_order"
      
  manual_override:
    command: "/quiet"
    duration_minutes: 60
    extend_command: "/quiet +30"
```

---

## 🚨 告警与监控

### 响应异常检测

```python
# 检测过度响应
if responses_last_hour > 100:
    alert("响应频率过高，可能违反按需响应协议")

# 检测响应不足
if mentions_last_hour > 0 and responses_last_hour == 0:
    alert("有@提及但未响应，检查触发逻辑")

# 检测静默失效
if quiet_mode_enabled and responses_last_hour > 5:
    alert("静默模式下仍有响应，检查过滤逻辑")
```

### 监控指标

| 指标 | 目标 | 告警阈值 |
|------|------|---------|
| 响应率（被@后） | >95% | <80% |
| 误响应率（未@响应） | <5% | >10% |
| 平均响应延迟 | <60 秒 | >300 秒 |
| 静默模式违规 | 0 | >0 |

---

## 🧪 测试用例

### 测试场景

```yaml
test_cases:
  - name: "群聊@提及"
    input: "@太一 今天天气如何"
    context: {chat_type: "group", sender: "user123"}
    expected: respond=True, reason: "mentioned"
    
  - name: "群聊闲聊"
    input: "今天天气真好"
    context: {chat_type: "group", sender: "user123"}
    expected: respond=False, reason: "no_trigger"
    
  - name: "私聊消息"
    input: "帮我查一下天气"
    context: {chat_type: "direct", sender: "SAYELF"}
    expected: respond=True, reason: "direct_order"
    
  - name: "命令触发"
    input: "/日报"
    context: {chat_type: "direct", sender: "SAYELF"}
    expected: respond=True, reason: "command"
    
  - name: "转发消息"
    input: "[转发] 文章标题..."
    context: {chat_type: "direct", sender: "user123", is_forwarded: true}
    expected: respond=False, reason: "forwarded_message"
```

---

## 📜 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-03 | 初始版本：按需响应协议创建 |

---

*文档：`constitution/directives/ON-DEMAND-RESPONSE.md` | 配置：`config/response-config.yaml`*
