# 🤖 Discord 接入指南

> **状态**: 🟡 待用户创建 Bot Token  
> **创建**: 2026-04-06 13:10  
> **执行**: 太一 AGI 智能自动化

---

## 📊 当前状态

| 组件 | 状态 |
|------|------|
| **Gateway** | ✅ 运行中 (PID 207154) |
| **Discord 插件** | 🟡 待配置 |
| **Bot Token** | 🔴 待创建 |
| **配置文件** | 🟡 待更新 |

---

## 🎯 立即执行步骤

### 步骤 1: 创建 Discord Bot (5 分钟)

**访问**: https://discord.com/developers/applications

1. 登录 Discord 账号
2. 点击右上角 **"New Application"**
3. 输入名称：`Taiyi AGI` 或 `太一`
4. 点击 **"Create"**
5. 左侧菜单选择 **"Bot"**
6. 点击 **"Add Bot"** → **"Yes, do it!"**
7. 点击 **"Reset Token"** 生成 Token
8. **立即复制 Token** (只显示一次！)

---

### 步骤 2: 启用必要权限

在 **Bot** 页面，滚动到 **"Privileged Gateway Intents"**:

- ✅ **Message Content Intent** (必须启用)
- 🟡 Server Members Intent (可选)
- 🟡 Presence Intent (可选)

---

### 步骤 3: 邀请 Bot 到服务器

1. 左侧菜单：**OAuth2** → **URL Generator**
2. Scopes: 勾选 `bot`
3. Bot Permissions: 勾选
   - `Send Messages`
   - `Read Message History`
   - `Embed Links`
   - `Attach Files`
4. 复制生成的 URL
5. 浏览器打开 URL，选择服务器，授权

---

### 步骤 4: 获取 Server ID

1. Discord 设置 → 高级 → 启用 **开发者模式**
2. 右键服务器图标 → **复制 ID**
3. 保存 Server ID (如：`987654321098765432`)

---

### 步骤 5: 配置到 OpenClaw

**方式 A: 使用脚本 (推荐)**

```bash
# 复制你的 Bot Token
BOT_TOKEN="你的 Bot Token"

# 运行配置脚本
python3 /home/nicola/.openclaw/workspace/scripts/add-discord-channel.py $BOT_TOKEN

# 或指定 Server ID
python3 /home/nicola/.openclaw/workspace/scripts/add-discord-channel.py $BOT_TOKEN 987654321098765432
```

**方式 B: 手动编辑配置**

编辑 `~/.openclaw/openclaw.json`，在 `channels` 添加:

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "defaultAccount": "taiyi",
      "streaming": "partial",
      "accounts": {
        "taiyi": {
          "enabled": true,
          "botToken": "YOUR_BOT_TOKEN_HERE",
          "dmPolicy": "pairing",
          "groupPolicy": "allowlist",
          "allowFrom": ["YOUR_SERVER_ID"],
          "streaming": "partial"
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "taiyi",
      "match": {
        "channel": "discord",
        "accountId": "taiyi"
      }
    }
  ]
}
```

---

### 步骤 6: 重启 Gateway

```bash
openclaw gateway restart
```

等待 10-15 秒。

---

### 步骤 7: 验证连接

**方法 1: 检查日志**

```bash
journalctl --user -u openclaw-gateway.service -f
```

成功日志:
```
[Discord] Connected as Taiyi AGI#1234
[Discord] Listening for messages...
```

**方法 2: Discord 测试**

在 Discord 服务器发送:
```
@Taiyi 你好
```

如果 Bot 回复，表示成功！✅

---

## 📋 所需信息清单

请准备以下 3 个信息：

| 信息 | 获取位置 | 示例 |
|------|---------|------|
| **Bot Token** | Discord Dev Portal → Bot → Reset Token | `MTIzNDU2Nzg5MDEy...` |
| **Client ID** | General Information | `1234567890123456789` |
| **Server ID** | 右键服务器 → 复制 ID | `987654321098765432` |

---

## 🚨 安全提示

### ⚠️ Bot Token 保护

- **不要**分享到公开场合
- **不要**提交到 GitHub
- **不要**发送给他人
- **立即**保存到安全位置
- 如泄露，立即 Reset Token

### ✅ 推荐做法

- 使用 `.env` 文件存储 Token
- 使用环境变量
- 定期轮换 Token (每 90 天)
- 限制 Bot 权限到最小必需

---

## 🔧 故障排查

### 问题 1: Bot 不回复

**检查清单**:
- [ ] Bot Token 是否正确
- [ ] Bot 是否在服务器中
- [ ] Message Content Intent 是否启用
- [ ] Gateway 是否重启
- [ ] Bot 权限是否足够

**解决方法**:
```bash
# 检查 Gateway 状态
openclaw gateway status

# 查看日志
journalctl --user -u openclaw-gateway.service -f

# 重启 Gateway
openclaw gateway restart
```

### 问题 2: Token 无效

**解决方法**:
1. Discord Dev Portal → Bot
2. 点击 **Reset Token**
3. 更新配置文件
4. 重启 Gateway

### 问题 3: Bot 无法加入服务器

**检查**:
- 服务器是否达到 Bot 上限
- 是否有邀请权限
- URL 是否正确

---

## 📚 相关文件

| 文件 | 内容 |
|------|------|
| `docs/discord-bot-setup.md` | 详细创建教程 |
| `scripts/add-discord-channel.py` | 自动配置脚本 |
| `reports/discord-integration-guide.md` | 本文件 |

---

## 🎯 下一步

**用户需执行**:
1. [ ] 访问 https://discord.com/developers/applications
2. [ ] 创建 Discord Bot
3. [ ] 复制 Bot Token
4. [ ] 邀请 Bot 到服务器
5. [ ] 获取 Server ID
6. [ ] 运行配置脚本或手动更新配置
7. [ ] 重启 Gateway
8. [ ] 测试连接

**太一待执行** (用户提供 Token 后):
- [ ] 自动更新配置文件
- [ ] 自动重启 Gateway
- [ ] 自动验证连接
- [ ] 发送测试消息

---

## 🔗 相关链接

- **Discord Developer Portal**: https://discord.com/developers/applications
- **Discord API 文档**: https://discord.com/developers/docs
- **OpenClaw 文档**: https://docs.openclaw.ai/channels/discord
- **权限计算器**: https://discordapi.com/permissions.html
- **详细教程**: `docs/discord-bot-setup.md`

---

## 📝 配置示例

### 完整配置 (openclaw.json)

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "defaultAccount": "taiyi",
      "streaming": "partial",
      "accounts": {
        "taiyi": {
          "enabled": true,
          "botToken": "MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GJKLmN.opqrstUVWXYZabcdefGHIJKL",
          "dmPolicy": "pairing",
          "groupPolicy": "allowlist",
          "allowFrom": ["987654321098765432"],
          "streaming": "partial"
        },
        "zhiji": {
          "enabled": true,
          "botToken": "ANOTHER_TOKEN",
          "dmPolicy": "pairing",
          "groupPolicy": "allowlist",
          "allowFrom": ["987654321098765432"],
          "streaming": "partial"
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "taiyi",
      "match": {
        "channel": "discord",
        "accountId": "taiyi"
      }
    },
    {
      "agentId": "zhiji",
      "match": {
        "channel": "discord",
        "accountId": "zhiji"
      }
    }
  ]
}
```

---

*报告生成：太一 AGI | 2026-04-06 13:10*  
**状态**: 🟡 待用户提供 Bot Token  
**下一步**: 用户创建 Bot Token 后，太一自动完成配置
