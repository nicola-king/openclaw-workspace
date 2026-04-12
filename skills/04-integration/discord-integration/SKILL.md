---
name: discord-integration
version: 1.0.0
description: Discord 集成 - 消息收发/频道管理/机器人控制
category: communication
tags: ['discord', 'messaging', 'bot', 'integration', 'communication']
author: 太一 AGI
created: 2026-04-08
updated: 2026-04-08
status: active
priority: P1
---

# 💬 Discord Integration - Discord 集成 v1.0

> **状态**: ✅ 新创建 | **版本**: 1.0.0 | **创建时间**: 2026-04-08  
> **核心功能**: 消息收发/频道管理/机器人控制/自动响应

---

## 🎯 核心功能

### 1. 消息收发 ✅

- 发送文本消息
- 发送嵌入消息 (Embeds)
- 发送文件/图片
- 接收消息事件
- 消息编辑/删除

### 2. 频道管理 ✅

- 列出频道
- 创建频道
- 删除频道
- 频道权限管理
- 频道分类

### 3. 机器人控制 ✅

- 机器人状态管理
- 机器人昵称修改
- 机器人头像修改
- 在线状态设置

### 4. 自动响应 ✅

- 关键词触发
- 命令前缀识别
- 定时任务
- 事件监听

---

## 📦 文件结构

```
discord-integration/
├── SKILL.md (本文档)
├── discord_bot.py (机器人核心)
├── config/
│   └── discord_config.json (配置文件)
├── commands/
│   ├── admin.py (管理命令)
│   ├── info.py (信息查询)
│   └── auto.py (自动响应)
├── events/
│   ├── on_message.py (消息事件)
│   ├── on_ready.py (就绪事件)
│   └── on_member.py (成员事件)
└── tests/
    └── test_discord.py (测试)
```

---

## 🔐 配置说明

### 1. 创建 Discord 应用

**步骤**:
```
1. 访问：https://discord.com/developers/applications
2. 点击 "New Application"
3. 填写应用名称：太一 AGI
4. 点击 "Create"
```

### 2. 获取 Bot Token

**步骤**:
```
1. 左侧菜单 → Bot
2. 点击 "Add Bot" → "Yes, do it!"
3. 点击 "Reset Token" (或 "Copy Token")
4. 复制 Token (只保存一次)
```

### 3. 启用 Intents

**步骤**:
```
1. Bot 页面 → Privileged Gateway Intents
2. 启用:
   - MESSAGE CONTENT INTENT ✅
   - SERVER MEMBERS INTENT ✅
   - PRESENCE INTENT ✅
3. 点击 "Save Changes"
```

### 4. 邀请机器人到服务器

**步骤**:
```
1. 左侧菜单 → OAuth2 → URL Generator
2. Scopes: 勾选 "bot"
3. Bot Permissions: 勾选:
   - Send Messages
   - Manage Messages
   - Read Message History
   - Embed Links
   - Attach Files
4. 复制生成的 URL
5. 在浏览器打开，选择服务器，授权
```

### 5. 填写配置文件

**编辑**: `config/discord_config.json`

```json
{
  "token": "你的 Bot Token",
  "client_id": "你的 Client ID",
  "guild_id": "你的服务器 ID",
  "prefix": "!",
  "channels": {
    "general": "频道 ID",
    "bot": "频道 ID"
  }
}
```

---

## 🚀 使用方式

### 基础用法

```python
from skills.discord_integration.discord_bot import DiscordBot

# 初始化
bot = DiscordBot()

# 启动机器人
bot.start()

# 发送消息
bot.send_message(
    channel_id="123456789",
    content="你好，我是太一 AGI！"
)

# 发送嵌入消息
bot.send_embed(
    channel_id="123456789",
    title="太一 AGI",
    description="你的数字幕僚",
    color=0x00ff00
)

# 获取状态
status = bot.get_status()
print(status)
```

### 命令行用法

```bash
# 启动机器人
cd /home/nicola/.openclaw/workspace/skills/discord-integration
python3 discord_bot.py

# 测试发送
python3 -c "from discord_bot import DiscordBot; b = DiscordBot(); b.send_message('频道 ID', '测试消息')"
```

---

## 📋 配置模板

### 基础配置

```json
{
  "enabled": true,
  "token": "${DISCORD_BOT_TOKEN}",
  "client_id": "1234567890",
  "guild_id": "9876543210",
  "prefix": "!",
  
  "intents": {
    "messages": true,
    "message_content": true,
    "guilds": true,
    "guild_members": true,
    "guild_presences": true
  },
  
  "channels": {
    "general": "1111111111",
    "announcements": "2222222222",
    "bot_commands": "3333333333"
  },
  
  "features": {
    "auto_response": true,
    "command_prefix": "!",
    "logging": true,
    "rate_limit": 10
  }
}
```

---

## 🤖 自动响应配置

### 关键词触发

```json
{
  "auto_response": {
    "enabled": true,
    "rules": [
      {
        "trigger": "你好",
        "response": "你好！我是太一 AGI，有什么可以帮你的？",
        "exact_match": false
      },
      {
        "trigger": "帮助",
        "response": "可用命令：!help, !status, !info",
        "exact_match": true
      }
    ]
  }
}
```

### 命令配置

```json
{
  "commands": {
    "prefix": "!",
    "available": [
      "help",
      "status",
      "info",
      "ping",
      "serverinfo"
    ],
    "admin_only": [
      "broadcast",
      "cleanup"
    ]
  }
}
```

---

## 📊 监控指标

### 实时状态

```yaml
机器人状态:
  在线：✅
  延迟：25ms
  服务器：1 个
  频道：5 个
  
消息统计:
  今日发送：120 条
  今日接收：350 条
  命令执行：45 次
  
性能指标:
  平均响应：1.2 秒
  成功率：99.5%
```

---

## 🔧 故障排查

### Q: 机器人无法连接？

**检查**:
1. Token 是否正确
2. Intents 是否启用
3. 网络是否通畅

```bash
# 测试连接
python3 -c "import discord; print('✅ discord.py 已安装')"
```

### Q: 无法读取消息内容？

**解决**:
1. Discord 开发者门户 → Bot → Privileged Gateway Intents
2. 启用 "MESSAGE CONTENT INTENT"
3. 保存并重启机器人

### Q: 无法发送消息？

**检查**:
1. 机器人权限是否足够
2. 频道 ID 是否正确
3. 速率限制是否触发

---

## ⚠️ 注意事项

### 1. 速率限制

```yaml
Discord API 限制:
  - 每频道：每 5 秒最多 5 条消息
  - 全局：每 60 秒最多 50 条消息
  
解决方案:
  - 启用消息队列
  - 批量发送合并
  - 错误重试机制
```

### 2. 权限管理

```yaml
最小权限原则:
  - Send Messages (必需)
  - Read Message History (必需)
  - Embed Links (可选)
  - Attach Files (可选)
  - Manage Messages (管理用)
```

### 3. Token 安全

```yaml
安全建议:
  - 不要硬编码 Token
  - 使用环境变量
  - 定期更换 Token
  - 不要泄露到 Git
```

---

## 📚 相关文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `SKILL.md` | 本文档 | `skills/discord-integration/` |
| `discord_bot.py` | 机器人核心 | `skills/discord-integration/` |
| `discord_config.json` | 配置文件 | `skills/discord-integration/config/` |

---

## 🎯 下一步

- [ ] 创建 `discord_bot.py` 核心实现
- [ ] 配置 Discord Bot Token
- [ ] 配置服务器/频道 ID
- [ ] 测试消息收发
- [ ] 配置自动响应
- [ ] 集成到太一 AGI 系统

---

*版本：1.0.0 | 创建时间：2026-04-08 | 状态：✅ 已创建*
