# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Related

- [Agent workspace](/concepts/agent-workspace)

---

## GMGN.AI 配置

> 更新时间：2026-03-27 21:03 | 状态：✅ 已登录

### 🔐 登录信息

| 项目 | 配置 |
|------|------|
| **登录方式** | Telegram 账号登录 ✅ |
| **Telegram 账号** | @nicola king (7073481596) |
| **状态** | ✅ 已登录 |

### 💳 钱包地址

#### Solana
| 项目 | 地址/状态 |
|------|----------|
| **地址** | `5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq` |
| **余额** | 0 SOL (余额不足，需充值) |
| **用途** | Solana 链上交易 |

#### Base
| 项目 | 地址/状态 |
|------|----------|
| **地址** | `0x73d6a5835ddf6f54480e28c8fdf399f8ec1b1c79` |
| **余额** | 0 ETH (余额不足，需充值) |
| **用途** | Base 链上交易 |

### 🌐 受信任 IP

| 项目 | IP 地址 | 状态 |
|------|--------|------|
| **直连出口** | `106.92.155.193` | ✅ 当前公网出站IP |
| **代理出口** | `103.151.173.197` | ✅ Clash 代理出口 |
| **内网 IP** | `192.168.31.99` | ✅ 本地 |
| **币安白名单** | `103.172.182.26` | 🔴 待配置 |

### 🔑 Ed25519 密钥对 (2026-03-30 生成)

| 编号 | 公钥 | 添加时间 | 可用时间 | 状态 |
|------|------|---------|---------|------|
| **#1** | `MCowBQYDK2VwAyEA6mgm2uPp5dApdRTt35fIHHEu932kkpw+O7QKXopEqN0=` | 2026-03-30 | 2026-04-06 | 🟡 冷却中 |
| **#2** | `MCowBQYDK2VwAyEAiRb0DJJxPPYUeRGYgFilNZR7sr9HIBGe/zPqcY9pN4A=` | 2026-03-30 | 2026-04-06 | 🟡 冷却中 |

**算法**: Ed25519 | **私钥**: 已安全存储 (不显示) | **冷却期**: 7 天

### 🤖 GMGN Bot

| 项目 | 配置 |
|------|------|
| **Bot 名称** | GMGN.AI |
| **Bot ID** | 6887194564 |
| **功能** | 秒级交易 Bot |
| **状态** | ✅ 已连接 |

### 📋 使用说明

#### 充值
1. **Solana**: 转账 SOL 到 `5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq`
2. **Base**: 转账 ETH 到 `0x73d6a5835ddf6f54480e28c8fdf399f8ec1b1c79`

#### 交易
- 在 GMGN Bot 中发送交易指令
- 支持秒级快速交易
- 支持限价单/市价单

### 🔗 相关链接

- GMGN 官网：https://gmgn.ai
- Telegram Bot: @GMGN_bot

---

---

## 🌐 本地代理配置

> 状态：✅ 白名单（有意配置，非遗留污染）

| 项目 | 配置 |
|------|------|
| **类型** | Clash（本地代理） |
| **地址** | `127.0.0.1:7890` |
| **用途** | Gateway 对外请求（Telegram API / 飞书 API / 外网访问）|
| **配置位置** | `~/.config/systemd/user/openclaw-gateway.service` 中的 `Environment=` 字段 |
| **白名单理由** | SAYELF 确认：此为有意配置，不清理 |

**doctor 检查处理**：该配置被 OpenClaw doctor 标记为非标准，已确认忽略。

---

*更新时间：2026-05-05 20:40*
*登录方式：Telegram 账号*
