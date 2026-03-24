# MEMORY.md - 太一长期记忆

> 最后更新：2026-03-24 13:31 | 会话：agent:taiyi:telegram:direct:7073481596

---

## 🆔 身份锚点

| 项目 | 配置 |
|------|------|
| **名称** | 太一 (Taiyi) |
| **角色** | AGI 执行总管 |
| **唯一决策人** | Nicola（大鹏 / SAYELF） |
| **原则** | 负熵法则 · 价值创造 · 免费开源优先 |

---

## 🔑 核心配置

### Polymarket
| 项目 | 配置 |
|------|------|
| **API Key** | `019d1b31-787e-7829-87b7-f8382effbab2` |
| **钱包地址** | `0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf` |
| **用户名** | SAYELF |
| **邮箱** | chuanxituzhu@gmail.com |

### 微信
| 项目 | 配置 |
|------|------|
| **公众号** | SAYELF 山野精灵 |
| **公众号 ID** | gh_69b1169c64f7 |
| **AppID** | wx720a4c489fec9df3 |
| **AppSecret** | 🟡 待获取 (开发→基本配置) |
| **登录邮箱** | 285915125@qq.com |
| **状态** | ✅ 已认证，待发布 |
| **个人号** | sayelf-tea (✅ 已连接) |

### Telegram Bots
| Bot | Token |
|-----|-------|
| 太一 | 8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY |
| 知几 | 8563369264:AAHeycXPlUQic41mOu4yCyaDcNQAKxYr61E |
| 山木 | 8731213565:AAHzAnm8lUG2riIuhHyYrxYrzixZ0zibcxo |
| 素问 | 8632190716:AAFR9k4811ISyQ4tTbn99G9GmtMNsgdkL6w |
| 罔两 | 8635135614:AAEnppb2absodyReJDX-qZAoERP29YFuh1c |
| 庖丁 | 8610739795:AAGvKpqunuyBZlB4sgZwrsly4j1LVMJa728 |

### 飞书应用
| Bot | App ID | App Secret |
|-----|--------|------------|
| 太一 | cli_a9086d6b5779dcc1 | tXHOop03ZHQynCRuEPkambASNori3KhZ |
| 知几 | cli_a90fc49a4b78dcd4 | JARQ374uVMVdnehV88T4IbcPQ2TLGyZl |
| 山木 | cli_a93298c9b0789cc6 | Sv6FCgMGTYyg1b33DvDEKdwI76GW5krI |
| 素问 | cli_a932968a1338dcc7 | TrVWKrMIVVB0SfwF7AIhYR3dCwThSRLj |
| 罔两 | cli_a932999506789cb3 | m02XEFFlRYX6JL3oPDsdYgVdzNdpilpW |
| 庖丁 | cli_a9329934c7f85cb0 | P1WOIJddDHrA2fxI5XLowfvo8bSfnHWJ |

---

## 🎯 核心策略

### 知几-E 气象套利（主策略）
- **数据**：189 条气象记录入库
- **阈值**：置信度 96% · 优势 2%
- **下注**：Quarter-Kelly
- **状态**：🟡 基础设施就绪，待实盘

### 鲸鱼跟随（副策略）
- **目标**：majorexploiter ($2.4M 盈利，活跃)
- **状态**：🟡 20% 进度

### 空投套利（0 成本启动）
- **重点**：OpenLedger ($OPEN, 1500 万代币)
- **状态**：🟡 调研完成，待执行

### CAD 服务（变现路径）
- **工具**：LibreCAD 2.2 + FreeCAD 0.21
- **用途**：跨境外贸图纸处理
- **状态**：🟡 30% 进度

---

## 📊 变现路径

```
空投 ($100) → CAD 服务 (¥5000) → Polymarket ($1000) → GPU 基金 → AGI
```

### AGI 飞轮
| 环节 | 状态 |
|------|------|
| 价值创造 | ✅ 宪法 +10+ 技能 |
| 价值变现 | 🟡 启动中 |
| 算力投资 | 🔴 $0 启动 |
| AGI 进化 | 🟡 规则驱动 |

---

## 📋 当前任务（P0 优先）

| 编号 | 任务 | 状态 | 阻塞点 |
|------|------|------|--------|
| TASK-013 | 公众号首篇 | 🟡 待执行 | 需安装 md2wechat + 微信凭证 |
| TASK-032 | 空投任务 | 🟡 调研完成 | 确认参与项目 |
| TASK-033 | CAD 服务上线 | 🟡 30% | 部署方案确认 |
| TASK-034 | 鲸鱼追踪 | 🟡 20% | 监控脚本编写 |
| TASK-037 | Discord 加入 | 🔴 待加入 | 需邀请链接 |

---

## 🧠 关键案例学习

### PolyCop Bot（验证信号）
| 项目 | 数据 |
|------|------|
| **来源** | @red_jingou (阿年派克) |
| **收益** | $1,840 (47 笔交易) |
| **策略** | BTC 剥头皮 (1 分钟周期) |
| **频率** | 210 笔/天 |
| **技术栈** | OpenClaw + Codex + Rust |
| **洞察** | OpenClaw+Polymarket 自动交易已验证可行 |

---

## 🛠️ 技术基建

| 组件 | 状态 |
|------|------|
| Gateway | ✅ 运行中 (PID 419212) |
| 微信插件 | ✅ @tencent-weixin/openclaw-weixin@1.0.3 |
| CAD 工具 | ✅ LibreCAD + FreeCAD |
| GitHub | ✅ zhiji-e 仓库创建 |
| Twitter | ✅ @SayelfTea 首推发布 |

---

## 📜 宪法核心（摘要）

### 价值基石
- 帮助，不表演
- 形成观点，不讨好
- 资源优先，探索先行
- 通过能力赢得信任

### 负熵法则
- 输出必须创造价值
- 废话 = 不输出
- 复杂为了复杂 = 违规

### 多 Bot 协作
- 太一：唯一统筹者
- 知几：量化交易
- 山木：内容创意
- 素问：技术开发
- 罔两：数据/CEO
- 庖丁：预算成本

---

## 📝 记忆维护

- **每日**：`memory/YYYY-MM-DD.md` — 原始日志
- **长期**：`MEMORY.md` — 固化记忆（本文件）
- **维护**：每日 23:00 回顾，提炼到本文件

---

## 📝 历史归档

### 2026-03-23（昨日）

| 事件 | 状态 |
|------|------|
| **微信接入** | ✅ 成功 (openclaw-weixin@1.0.3) |
| **知几-E v2.1** | ✅ 完成 (189 条气象数据) |
| **Polymarket API** | ✅ 配置完成 |
| **记忆索引** | ✅ registry.json 创建 |

### 2026-03-22（太一独立日）

| 事件 | 状态 |
|------|------|
| **100% 授权** | ✅ SAYELF 完全放权 |
| **多 Bot 架构** | ✅ 太一 +5 专业 Bot |
| **鲸鱼分析** | ✅ majorexploiter ($2.4M) |

---

## 📝 今日进展 (2026-03-24 16:55)

| 任务 | 进展 |
|------|------|
| **MEMORY.md** | ✅ 创建（长期记忆固化） |
| **md2wechat** | ✅ 安装成功 (v2.0.1) |
| **公众号首篇** | ✅ **已发布**《AI 管家》 |
| **技能市场** | ✅ 规划完成 (3 层产品矩阵) |
| **鲸鱼追踪** | ✅ 脚本完成 |
| **GitHub** | ✅ 策略 v2.1+ 鲸鱼追踪器已推送 |
| **数据目录** | ✅ ~/polymarket-data 创建 |

### 变现路径调整
**原路径：** Polymarket 套利 → 风险高
**新路径：** 技能市场 → 可持续

```
免费技能引流 → 付费技能变现 → 定制服务高客单
目标：¥10K/月 (3 个月)
```

---

*创建时间：2026-03-24 13:31 | 最后更新：2026-03-24 16:55 | 太一独立运行模式激活*
