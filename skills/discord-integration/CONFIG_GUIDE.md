# 🎮 Discord 集成配置指南

> **创建时间**: 2026-04-11  
> **状态**: 待配置  
> **预计时间**: 10 分钟

---

## 🔐 获取 Discord Bot 凭证

### 步骤 1: 访问 Discord 开发者门户

访问：https://discord.com/developers/applications

### 步骤 2: 登录 Discord 账号

使用你的 Discord 账号登录

### 步骤 3: 创建新应用

1. 点击右上角"New Application"
2. 填写应用名称：`太一 AGI`
3. 点击"Create"

### 步骤 4: 创建 Bot

1. 点击左侧"Bot"
2. 点击"Add Bot"
3. 点击"Yes, do it!"

### 步骤 5: 获取 Bot Token

1. 在 Bot 页面，找到"Token"部分
2. 点击"Reset Token" (首次创建)
3. 点击"Copy"复制 Token
4. **重要**: Token 只显示一次，请妥善保存！

### 步骤 6: 获取 Application ID

1. 点击左侧"General Information"
2. 找到"Application ID"
3. 点击复制

### 步骤 7: 配置 Intents

1. 返回"Bot"页面
2. 向下滚动到"Privileged Gateway Intents"
3. 启用以下 Intents:
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ PRESENCE INTENT
4. 点击"Save Changes"

### 步骤 8: 配置 Bot 权限

1. 点击左侧"OAuth2" → "URL Generator"
2. 选择 scopes:
   - ✅ bot
3. 选择 Bot Permissions:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Manage Roles (可选)
   - ✅ Manage Channels (可选)
4. 复制生成的 URL

### 步骤 9: 邀请 Bot 到服务器

1. 在浏览器打开生成的 URL
2. 选择要添加的服务器
3. 点击"Authorize"
4. 完成人机验证

---

## ⚙️ 配置本地文件

### 获取服务器 ID

1. 在 Discord 中，右键点击服务器图标
2. 点击"Copy Server ID"
3. 如果没有此选项，需要在设置中启用"开发者模式"

### 编辑配置文件

```bash
nano /home/nicola/.openclaw/workspace/config/discord/config.json
```

### 填写内容

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "application_id": "YOUR_APPLICATION_ID_HERE",
  "guild_id": "YOUR_SERVER_ID_HERE"
}
```

### 保存退出

按 `Ctrl+O` 保存，按 `Ctrl+X` 退出

---

## ✅ 测试连接

### 运行测试

```bash
python3 /home/nicola/.openclaw/workspace/skills/discord-integration/discord_client.py
```

### 启动 Bot

```bash
python3 /home/nicola/.openclaw/workspace/skills/discord-integration/discord_bot.py
```

### 成功输出

```
============================================================
🎮 Discord 客户端测试
============================================================
🎮 Discord 客户端已初始化
   Application ID: 1234567890123456789

============================================================
✅ Discord 已连接
   用户名：太一 AGI
   用户 ID: 1234567890123456789
   服务器数：1
============================================================
```

### 测试命令

在 Discord 服务器中发送:
```
!hello
!info
!help
```

---

## 🚀 使用示例

### 发送消息

```python
from discord_client import DiscordClient

client = DiscordClient()

# 需要运行 bot 后才能发送
# await client.send_text_message(123456789, "Hello!")
```

### 发送卡片消息

```python
# await client.send_embed_message(
#     channel_id=123456789,
#     title="标题",
#     description="描述",
#     fields=[
#         {"name": "字段 1", "value": "值 1"},
#         {"name": "字段 2", "value": "值 2"}
#     ]
# )
```

### 获取服务器信息

```python
# guild = client.get_guild(server_id)
# print(f"服务器：{guild.name}")
# print(f"成员数：{guild.member_count}")
```

---

## 🔧 故障排除

### 问题 1: Token 无效

**错误**: `discord.errors.LoginFailure`

**原因**: Token 错误或已过期

**解决**:
1. 检查 Token 是否正确复制
2. 确认 Token 没有多余空格
3. 在 Discord 开发者门户重新生成 Token

### 问题 2: Intents 未启用

**错误**: `discord.errors.PrivilegedIntentsRequired`

**原因**: 未启用 Privileged Intents

**解决**:
1. 访问 Discord 开发者门户
2. 进入 Bot 页面
3. 启用 MESSAGE CONTENT INTENT
4. 保存更改

### 问题 3: Bot 不在服务器

**错误**: 无法找到服务器

**原因**: Bot 未邀请到服务器

**解决**:
1. 使用 OAuth2 URL Generator 生成邀请链接
2. 打开链接邀请 Bot 到服务器
3. 确认 Bot 出现在服务器成员列表中

### 问题 4: 权限不足

**错误**: `discord.errors.Forbidden`

**原因**: Bot 权限不足

**解决**:
1. 检查 Bot 角色权限
2. 确保 Bot 角色在成员列表顶部
3. 重新生成邀请链接并授予足够权限

---

## 📚 相关文档

- [Discord 开发者门户](https://discord.com/developers/applications)
- [discord.py 文档](https://discordpy.readthedocs.io/)
- [Discord API 文档](https://discord.com/developers/docs/intro)
- [Bot 权限配置](https://discord.com/developers/docs/topics/permissions)

---

**🎮 配置完成后，运行测试验证连接！**

**太一 AGI · 2026-04-11** ✨
