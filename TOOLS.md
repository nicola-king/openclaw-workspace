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

*更新时间：2026-05-16 12:00*
*登录方式：Telegram 账号*

---

## 🎨 html-anything 自动渲染引擎

> 已融入太一系统，自动根据内容类型智能调用

### 服务
| 项目 | 配置 |
|------|------|
| **服务名** | `html-anything.service` |
| **端口** | 3777 |
| **状态** | ✅ systemd 自启 |
| **位置** | `skills/html-anything/` |

### 自动路由策略（太一自动判断）

| 渲染方式 | 成本 | 适用场景 |
|---------|------|---------|
| `html-render.py`（静态） | 零 token | 日常日报/报告/系统状态 |
| `html-agent.py`（Agent） | 消耗 token | 公众号文章/月报/高价值内容 |
| `art-agent`（品牌/视觉） | 消耗 token | 品牌设计/视觉叙事/美学审校 |

### 脚本位置
- 静态渲染: `scripts/html-render.py`
- Agent渲染: `scripts/html-agent.py`
- Shell包装: `scripts/html-anything-render.sh`、`scripts/html-agent.sh`

### 模板速查
- `doc-kami-parchment` — 羊皮纸报告（默认）
- `article-magazine` — 杂志文章
- `data-report` — 暗色数据报告
- `card-xiaohongshu` — 小红书卡片
- `deck-swiss-international` — 瑞士国际 Deck

## 🔧 OpenClaw 唤醒别名

| 别名 | 命令 | 用途 |
|------|------|------|
| `oc-status` | `openclaw channels status --deep` | 深度状态查看，避免跨用户调用报错 |

> 已写入 ~/.bashrc，2026-05-21

## 🧠 知识沉淀原则

> 参见 constitution/rules/KNOWLEDGE-SEDIMENTATION.md

**四层沉淀路径**：
- 代码层 → CLAUDE.md / 项目 docs/
- 工具层 → 本文件 (TOOLS.md)
- 会话层 → memory/core.md + memory/YYYY-MM-DD.md
- 全局层 → wiki/ 或 constitution/


## 🖼️ VLM 视觉预处理 (2026-05-21 部署)

> 状态：✅ 已集成到 OpenClaw tools.media

### 架构
```
消息入站（任意渠道）
  → OpenClaw Gateway 自动检测图片附件
  → tools.media 调用 VLM CLI wrapper
  → ollama VLM (minicpm-v) 处理图片
  → 描述文本注入为 [Image] 上下文块
  → DeepSeek 接收完整上下文
```

### 服务
| 组件 | 状态 | 端口/位置 |
|------|------|-----------|
| ollama serve | systemd 自启 | 127.0.0.1:11434 |
| VLM CLI wrapper | scripts/vlm-understand.sh | ~/.openclaw/workspace/ |
| Python venv | ~/.venvs/vlm/ | ollama 0.6.2 |

### 模型
| 模型 | 大小 | 角色 |
|------|------|------|
| minicpm-v | 5.5GB | 主用 VLM（中文优先） |
| llava:7b | 4.7GB | 备用 VLM |
| qwen2.5:7b | 4.7GB | 纯文本备用 |

### 测试
```bash
# 直接测试 VLM
bash ~/.openclaw/workspace/scripts/vlm-understand.sh /path/to/image.jpg

# Python API 测试
source ~/.venvs/vlm/bin/activate
python3 -c "import ollama; r=ollama.chat(model='minicpm-v', messages=[{'role':'user','content':'描述这张图','images':['/path/img.jpg']}]); print(r['message']['content'])"
```

---

## 🌐 FreeDomain Skill — 免费域名管理 (2026-05-31)

> 集成自 DigitalPlatDev/FreeDomain ⭐172K
> AGPL-3.0 | https://github.com/DigitalPlatDev/FreeDomain

| 项目 | 配置 |
|------|------|
| **后缀** | .DPDNS.ORG / .UL.KG / .QZZ.IO / .XX.KG / .QD.JE |
| **仪表盘** | https://dash.domain.digitalplat.org/ |
| **社区** | Discord: https://discord.gg/ma4RZzMmVW |
| **注册数** | 500,000+ |
| **用途** | OERV分发 / 邮件域名 / GEO矩阵 |
| **安全提示** | ⚠️ 该项目 Telegram 群已被入侵，勿信 |

---

## 🐟 MiroFish — 群体智能预测引擎 (2026-05-31)

> 集成自 666ghj/MiroFish ⭐63K
> AGPL-3.0 | https://github.com/666ghj/MiroFish

| 项目 | 配置 |
|------|------|
| **类型** | 多 Agent 社会模拟预测引擎 |
| **技术栈** | Python + Node.js (React + Flask) |
| **状态** | 🔴 未部署（需 LLM API + Zep Cloud API） |
| **用途** | 跨境贸易舆情预测 / 竞品推演 / 内容沙盒 |
| **官网** | https://mirofish.ai |

---

## 🧠 Understand-Anything — 太一智能自动化集成 (2026-05-23)

> 状态: ✅ 已安装 | 18.4K ⭐ | 8个子技能

### 安装路径
| 组件 | 路径 |
|------|------|
| 技能链接 | `~/.openclaw/skills/understand-anything/` |
| 插件根目录 | `~/.understand-anything-plugin/` |
| 仓库位置 | `~/.understand-anything/repo/` |

### 子技能速查
| 子技能 | 位置 |
|--------|------|
| `understand` | `~/.openclaw/skills/understand-anything/understand/` |
| `understand-chat` | `~/.openclaw/skills/understand-anything/understand-chat/` |
| `understand-dashboard` | `~/.openclaw/skills/understand-anything/understand-dashboard/` |
| `understand-diff` | `~/.openclaw/skills/understand-anything/understand-diff/` |
| `understand-explain` | `~/.openclaw/skills/understand-anything/understand-explain/` |
| `understand-onboard` | `~/.openclaw/skills/understand-anything/understand-onboard/` |
| `understand-domain` | `~/.openclaw/skills/understand-anything/understand-domain/` |
| `understand-knowledge` | `~/.openclaw/skills/understand-anything/understand-knowledge/` |

### 首次使用构建
```bash
cd ~/.understand-anything-plugin && pnpm install --frozen-lockfile 2>/dev/null || pnpm install
cd ~/.understand-anything-plugin && pnpm --filter @understand-anything/core build
```

### 太一自动调度规则
参见 `skills/understand-anything/SKILL.md` — 太一根据用户意图自动匹配最优子技能。

**匹配矩阵摘要**:
- 理解代码 → `/understand`
- 看可视化 → `/understand-dashboard`
- 提问代码 → `/understand-chat`
- 差异分析 → `/understand-diff`
- 解释文件 → `/understand-explain`
- 上手指南 → `/understand-onboard`
- 业务领域 → `/understand-domain`
- 知识库分析 → `/understand-knowledge`

---

## 🤖 NotebookLM 集成 (2026-05-24)

| 项目 | 配置 |
|------|------|
| **上游** | teng-lin/notebooklm-py ⭐14.8K |
| **安装路径** | skills/notebooklm-py/ |
| **虚拟环境** | skills/notebooklm-py/.venv/ |
| **版本** | 0.5.0 |
| **CLI** | `source .venv/bin/activate && notebooklm ...` |
| **状态** | ✅ 已安装 |

### 使用
```bash
cd ~/.openclaw/workspace/skills/notebooklm-py && source .venv/bin/activate
notebooklm --version
```
