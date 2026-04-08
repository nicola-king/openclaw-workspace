# 微信通道使用指南

> 版本：v2.0 | 更新：2026-04-08 | 负责 Bot：太一 AGI

---

## 📋 目录

1. [快速开始](#快速开始)
2. [账号管理](#账号管理)
3. [日常使用](#日常使用)
4. [故障排查](#故障排查)
5. [高级配置](#高级配置)

---

## 🚀 快速开始

### 1. 检查状态

```bash
# 运行健康检查
python3 ~/.openclaw/workspace/skills/wechat/health-check.py
```

### 2. 查看账号

```bash
# 列出所有账号
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py list
```

### 3. 测试消息

在微信中发送一条消息到你绑定的账号，太一 AGI 会自动回复。

---

## 📱 账号管理

### 添加新账号

**方式 1：自动扫码（推荐）**

1. 在微信中搜索并关注「OpenClaw」公众号
2. 扫描登录二维码
3. 系统自动完成配置

**方式 2：手动配置**

```bash
# 编辑账号配置文件
nano ~/.openclaw/openclaw-weixin/accounts/<account-id>.json
```

### 查看账号详情

```bash
# 查看指定账号
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py show <account-id>

# 示例
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py show 1947559cd522-im-bot
```

### 删除账号

```bash
# 删除账号（需要确认）
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py remove <account-id>

# 示例
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py remove 3df0dca14cc5-im-bot
```

---

## 📊 日常使用

### 健康检查

```bash
# 快速检查
python3 ~/.openclaw/workspace/skills/wechat/health-check.py

# 详细输出
python3 ~/.openclaw/workspace/skills/wechat/health-check.py --verbose
```

### 监控状态

```bash
# 单次检查
python3 ~/.openclaw/workspace/skills/wechat/monitor.py

# 持续监控（每 60 秒）
python3 ~/.openclaw/workspace/skills/wechat/monitor.py --interval 60

# 输出到文件
python3 ~/.openclaw/workspace/skills/wechat/monitor.py --output /tmp/wechat-status.json
```

### 测试消息

```bash
# 发送测试消息
python3 ~/.openclaw/workspace/skills/wechat/test-message.py "你好，测试"
```

---

## 🔍 故障排查

### 问题 1：账号未认证

**症状**: 健康检查显示「未认证」

**解决**:
```bash
# 1. 检查账号文件
cat ~/.openclaw/openclaw-weixin/accounts/*.json

# 2. 重新扫码登录
# 在微信中扫描登录二维码

# 3. 重启 Gateway
openclaw gateway restart
```

### 问题 2：消息不回复

**症状**: 发送消息后无回复

**解决**:
```bash
# 1. 检查 Gateway 状态
openclaw gateway status

# 2. 查看日志
tail -f /tmp/openclaw/openclaw-*.log | grep weixin

# 3. 检查会话
openclaw sessions list

# 4. 重启 Gateway
openclaw gateway restart
```

### 问题 3：同步延迟

**症状**: 消息延迟收到或丢失

**解决**:
```bash
# 1. 清除同步缓存
rm ~/.openclaw/openclaw-weixin/accounts/*.sync.json

# 2. 重启 Gateway
openclaw gateway restart

# 3. 等待自动重新同步（约 30 秒）
```

### 问题 4：Gateway 启动失败

**症状**: `openclaw gateway start` 失败

**解决**:
```bash
# 1. 检查配置
openclaw doctor

# 2. 查看错误日志
tail -100 /tmp/openclaw/openclaw-*.log

# 3. 修复配置后重启
openclaw gateway restart
```

---

## ⚙️ 高级配置

### 多账号管理

微信通道支持多账号同时运行：

```bash
# 查看所有账号
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py list

# 查看每个账号状态
python3 ~/.openclaw/workspace/skills/wechat/monitor.py
```

### 自定义配置

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "channels": {
    // 其他通道配置...
  }
}
```

**注意**: 微信通道使用官方插件，自动注册，无需手动配置。

### 日志位置

| 日志类型 | 路径 |
|---------|------|
| Gateway 日志 | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| 账号配置 | `~/.openclaw/openclaw-weixin/accounts/` |
| 同步状态 | `~/.openclaw/openclaw-weixin/accounts/*.sync.json` |

---

## 📚 相关资源

- [SKILL.md](SKILL.md) - 技能文档
- [health-check.py](health-check.py) - 健康检查脚本
- [account-manager.py](account-manager.py) - 账号管理工具
- [monitor.py](monitor.py) - 监控脚本
- [test-message.py](test-message.py) - 消息测试工具

---

## 🆘 获取帮助

```bash
# 查看账号管理帮助
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py help

# 查看健康检查帮助
python3 ~/.openclaw/workspace/skills/wechat/health-check.py --help

# 联系太一 AGI
# 在飞书/Telegram/微信中直接询问
```

---

*文档版本：v2.0 | 最后更新：2026-04-08 | 太一 AGI*
