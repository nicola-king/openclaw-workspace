# Telegram 重复消息问题修复方案

## 🔍 问题诊断

根据日志分析，Telegram 重复发消息的原因：

### 1. Gateway 多次重启
```
16:46:54 - Telegram provider 启动
16:58:28 - 配置变更触发热重载
16:58:59 - Telegram channel 重启
16:59:00 - Telegram provider 再次启动
16:59:37 - Telegram provider 第三次启动
```

**问题**：每次重启时，grammY 的 long polling 会重新获取未确认的 updates，导致重复处理。

### 2. 网络超时重试
```
telegram sendChatAction failed: Network request for 'sendChatAction' failed!
```

**问题**：网络请求失败后，OpenClaw 可能触发重试机制。

### 3. 缺少去重机制
grammY 默认使用 `update_id` 去重，但重启后可能失效。

---

## ✅ 解决方案

### 方案 1：配置优化（已应用）

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY",
      "streaming": {
        "mode": "partial"
      },
      "groups": {
        "*": {
          "requireMention": true
        }
      }
    }
  }
}
```

### 方案 2：添加消息缓存去重

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "channels": {
    "telegram": {
      "dedup": {
        "enabled": true,
        "window": 60,
        "cacheSize": 1000
      }
    }
  }
}
```

### 方案 3：稳定 Gateway 运行

避免频繁重启：

```bash
# 检查 Gateway 稳定性
openclaw gateway status

# 查看重启原因
journalctl --user -u openclaw-gateway --since "16:00" | grep -E "restart|reload|error"
```

### 方案 4：网络优化

检查网络连接质量：

```bash
# 测试 Telegram API 连接
curl -s https://api.telegram.org/bot8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY/getMe

# 检查网络延迟
ping -c 5 api.telegram.org
```

---

## 🔧 立即执行

### 1. 清理旧的 update 偏移量

```bash
# 停止 Gateway
openclaw gateway stop

# 清理 Telegram update 缓存
rm -rf ~/.openclaw/telegram/*.json

# 重启 Gateway
openclaw gateway start
```

### 2. 添加去重配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY",
      "streaming": {
        "mode": "partial"
      },
      "groups": {
        "*": {
          "requireMention": true
        }
      },
      "polling": {
        "timeout": 30,
        "allowedUpdates": ["message", "callback_query", "edited_message"]
      }
    }
  }
}
```

### 3. 监控日志

```bash
# 实时查看 Telegram 消息
journalctl --user -u openclaw-gateway -f | grep telegram
```

---

## 📊 验证步骤

1. **发送测试消息** 到 Telegram Bot
2. **检查日志** 确认只处理一次
3. **观察响应** 确认只回复一次

---

## 🛡️ 长期优化建议

1. **使用 Webhook 模式** 替代 Long Polling（需要公网 IP）
2. **配置消息指纹** 去重机制
3. **添加速率限制** 防止频繁发送
4. **启用消息队列** 缓冲突发请求

---

*创建时间：2026-04-15 18:06*
*问题：Telegram 重复发送相同消息*
