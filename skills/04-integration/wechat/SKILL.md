---
name: wechat
version: 2.0.0
description: 微信通道集成 - 官方插件 + 本地技能
category: channel
tags: [wechat, 微信，消息，通道]
author: 太一 AGI
created: 2026-04-03
updated: 2026-04-08
status: stable
---

# WeChat 微信通道技能

> 版本：v2.0 | 更新：2026-04-08 | 负责 Bot：太一  
> 官方插件：`@tencent-weixin/openclaw-weixin@2.1.7`

---

## 🎯 职责

**微信消息收发通道**，使用腾讯官方 iLink AI 协议

- ✅ 个人微信消息自动接收
- ✅ 消息自动回复（通过 OpenClaw Gateway）
- ✅ 多账号支持
- ✅ 会话状态管理

---

## 📦 架构

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                      │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │  微信官方插件   │    │       其他通道 (飞书/Telegram) │ │
│  │ @tencent-weixin │    │                             │ │
│  │   openclaw      │    │                             │ │
│  └────────┬────────┘    └─────────────────────────────┘ │
│           │                                              │
│           ▼                                              │
│  ┌─────────────────┐                                     │
│  │   OpenClaw AI   │ ← 太一 AGI (qwen3.5-plus)           │
│  │    (taiyi)      │                                     │
│  └─────────────────┘                                     │
└─────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────┐
│   腾讯 iLink AI     │
│  (微信官方协议)      │
└─────────────────────┘
```

---

## 🔧 配置管理

### 配置位置

| 类型 | 路径 | 说明 |
|------|------|------|
| **账号配置** | `~/.openclaw/openclaw-weixin/accounts.json` | 账号列表 |
| **账号详情** | `~/.openclaw/openclaw-weixin/accounts/*.json` | 各账号 Token |
| **会话状态** | `~/.openclaw/openclaw-weixin/accounts/*.sync.json` | 同步状态 |
| **技能文件** | `~/.openclaw/workspace/skills/wechat/` | 本地技能 |

### 查看配置

```bash
# 查看已配置账号
cat ~/.openclaw/openclaw-weixin/accounts.json

# 查看账号详情
cat ~/.openclaw/openclaw-weixin/accounts/*.json

# 查看同步状态
cat ~/.openclaw/openclaw-weixin/accounts/*.sync.json
```

### 添加新账号

**方式 1：扫描二维码（推荐）**
```bash
# 官方插件会自动处理二维码
# 在微信中扫描登录即可
```

**方式 2：手动配置 Token**
```bash
# 编辑账号配置文件
nano ~/.openclaw/openclaw-weixin/accounts/<account-id>.json
```

---

## 🛠️ 工具脚本

### 健康检查

```bash
# 检查微信通道状态
python3 ~/.openclaw/workspace/skills/wechat/health-check.py
```

### 账号管理

```bash
# 列出所有账号
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py list

# 查看账号详情
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py show <account-id>

# 删除账号
python3 ~/.openclaw/workspace/skills/wechat/account-manager.py remove <account-id>
```

### 消息测试

```bash
# 发送测试消息
python3 ~/.openclaw/workspace/skills/wechat/test-message.py "你好，测试消息"
```

---

## 📊 监控指标

| 指标 | 说明 | 正常值 |
|------|------|--------|
| **账号状态** | 是否已认证 | ✅ 已认证 |
| **同步状态** | 消息同步是否正常 | ✅ 正常 |
| **最后活动** | 最后消息时间 | <24h |
| **Gateway 连接** | 与 OpenClaw Gateway 连接 | ✅ 正常 |

---

## 🔍 故障排查

### 问题 1：账号未认证

**症状**: 消息无法接收

**解决**:
```bash
# 1. 检查账号配置
cat ~/.openclaw/openclaw-weixin/accounts/*.json

# 2. 重新扫码登录
# 在微信中扫描登录二维码

# 3. 重启 Gateway
openclaw gateway restart
```

### 问题 2：消息不回复

**症状**: 收到消息但无回复

**解决**:
```bash
# 1. 检查 Gateway 状态
openclaw gateway status

# 2. 检查日志
tail -f /tmp/openclaw/openclaw-*.log | grep weixin

# 3. 验证会话配置
openclaw sessions list
```

### 问题 3：同步延迟

**症状**: 消息延迟收到

**解决**:
```bash
# 1. 清除同步缓存
rm ~/.openclaw/openclaw-weixin/accounts/*.sync.json

# 2. 重启 Gateway
openclaw gateway restart

# 3. 等待自动重新同步
```

---

## 🔗 相关文档

- `constitution/channels/WECHAT-CHANNEL.md` - 微信通道协议
- `docs/weixin-config.md` - 详细配置指南
- `memory/learning-notes/wechat-rpa-skill.md` - RPA 技能学习

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0.0 | 2026-04-08 | 深度修复：重构 + 优化 |
| v1.0.0 | 2026-04-03 | 初始版本 |

---

*创建：2026-04-03 | 更新：2026-04-08 | 太一 AGI*
