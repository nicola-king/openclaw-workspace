# 太一 AGI v5.0 · Agents & Skills 完整目录

> **版本**: 5.0 | **更新时间**: 2026-04-03 10:24
> **总 Agents**: 8 | **总 Skills**: 67+ | **Claw-Code 融合**: ✅ 100%

---

## 🤖 Agents（8 Bot 舰队）

| 编号 | 英文名 | 中文名 | 职责 | 负责 Skills |
|------|--------|--------|------|------------|
| A01 | **Taiyi** | 太一 | AGI 执行总管/统筹决策 | 核心调度 |
| A02 | **Zhiji** | 知几 | 量化交易/预测市场 | polymarket, binance-trader, gmgn, zhiji-sentiment |
| A03 | **Shanmu** | 山木 | 内容创意/媒体生成 | shanmu-reporter, video-factory, ppt-chart-generator |
| A04 | **Suwen** | 素问 | 技术开发/代码实现 | git-integration, docker-ctl, k8s-deploy, terraform-apply |
| A05 | **Wangliang** | 罔两 | 数据采集/CEO 分析 | flowsint-integration, webhook-relay, market-research |
| A06 | **Paoding** | 庖丁 | 预算成本/财务分析 | cost-tracker, heal-state |
| A07 | **Yi** | 羿 | 监控追踪/信号猎手 | polyalert, hunter-bot |
| A08 | **Shoucangli** | 守藏吏 | 资源调度/任务管理 | crontab-manager, steward |

---

## 📦 Skills 完整目录（67+）

### 🔧 P0: 核心工具（3 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S001 | `git-integration` | Git 集成 | Git clone/commit/push/PR/branch/merge | Git 版本控制全工作流 | `clawhub install git-integration` |
| S002 | `npm-audit` | NPM 审计 | Dependency vulnerability scan & fix | 依赖漏洞扫描与修复 | `clawhub install npm-audit` |
| S003 | `docker-ctl` | Docker 管理 | Container/image/Compose lifecycle | 容器/镜像/Compose 全生命周期 | `clawhub install docker-ctl` |

---

### ☁️ P1: 云原生（5 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S004 | `k8s-deploy` | K8s 部署 | Kubernetes app deploy/scale/logs | K8s 应用部署/扩缩容/日志 | `clawhub install k8s-deploy` |
| S005 | `terraform-apply` | Terraform | Infrastructure as Code (IaC) | 基础设施即代码 | `clawhub install terraform-apply` |
| S006 | `aws-cli` | AWS 命令行 | AWS EC2/S3/Lambda/RDS operations | AWS 云服务操作 | `clawhub install aws-cli` |
| S007 | `gcp-cli` | GCP 命令行 | GCP Compute/GKE/Cloud Run operations | GCP 云服务操作 | `clawhub install gcp-cli` |
| S008 | `azure-cli` | Azure 命令行 | Azure VM/AKS/Functions operations | Azure 云服务操作 | `clawhub install azure-cli` |

---

### 🤝 P2: 协作集成（6 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S009 | `slack-notify` | Slack 通知 | Slack message/thread/file/reaction | Slack 消息/线程/文件/表情 | `clawhub install slack-notify` |
| S010 | `notion-db` | Notion 数据库 | Notion page/database CRUD | Notion 页面/数据库增删改查 | `clawhub install notion-db` |
| S011 | `airtable-sync` | Airtable 同步 | Airtable table sync & import/export | Airtable 表格同步与导入导出 | `clawhub install airtable-sync` |
| S012 | `zapier-trigger` | Zapier 触发 | Zapier automation trigger | Zapier 自动化触发 | `clawhub install zapier-trigger` |
| S013 | `crontab-manager` | 定时任务 | Cron job create/edit/delete/monitor | 定时任务创建/编辑/删除/监控 | `clawhub install crontab-manager` |
| S014 | `webhook-relay` | Webhook 中继 | Webhook receive/forward/process | Webhook 接收/转发/处理 | `clawhub install webhook-relay` |

---

### 🎮 P3: 趣味性功能（5 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S015 | `ascii-art` | ASCII 艺术 | Image/text to ASCII art conversion | 图片/文字转 ASCII 艺术 | `clawhub install ascii-art` |
| S016 | `pet-companion` | 虚拟宠物 | Virtual pet growth/interaction/status | 虚拟宠物成长/互动/状态 | `clawhub install pet-companion` |
| S017 | `undercover-mode` | 隐身模式 | Low-profile execution mode | 低 profile 隐身执行模式 | `clawhub install undercover-mode` |
| S018 | `easter-egg` | 彩蛋系统 | Hidden commands & surprise responses | 隐藏命令与惊喜响应 | `clawhub install easter-egg` |
| S019 | `rust-bridge` | Rust 桥接 | Rust code compile & execute | Rust 代码编译与执行 | `clawhub install rust-bridge` |

---

### 🧠 P4: 高级 AI（5 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S020 | `llm-finetune` | 模型微调 | LoRA/QLoRA model fine-tuning | LoRA/QLoRA 模型微调 | `clawhub install llm-finetune` |
| S021 | `vector-db` | 向量数据库 | Chroma/Weaviate/Pinecone operations | 向量数据库操作 | `clawhub install vector-db` |
| S022 | `rag-pipeline` | RAG 流程 | Retrieval-Augmented Generation pipeline | 检索增强生成流程 | `clawhub install rag-pipeline` |
| S023 | `agent-swap` | 模型切换 | Dynamic model switching at runtime | 运行时动态模型切换 | `clawhub install agent-swap` |
| S024 | `cost-tracker` | 成本追踪 | Real-time API cost tracking & alerts | 实时 API 成本追踪与告警 | `clawhub install cost-tracker` |

---

### 💰 交易与金融（6 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S025 | `polymarket` | Polymarket | Prediction market trading | 预测市场交易 | `clawhub install polymarket` |
| S026 | `binance-trader` | 币安交易 | Binance spot/futures trading | 币安现货/期货交易 | `clawhub install binance-trader` |
| S027 | `gmgn` | GMGN | Solana/Base chain token trading | Solana/Base 链代币交易 | `clawhub install gmgn` |
| S028 | `zhiji` | 知几-E | Quant trading strategy engine | 量化交易策略引擎 | `clawhub install zhiji` |
| S029 | `zhiji-sentiment` | 知几 - 情绪 | FinBERT sentiment analysis | FinBERT 情绪分析 | `clawhub install zhiji-sentiment` |
| S030 | `tianji` | 天基 | Market opportunity analysis | 市场机会分析 | `clawhub install tianji` |

---

### 📊 数据与分析（6 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S031 | `flowsint-integration` | Flowsint 集成 | OSINT data collection & analysis | 开源情报数据采集与分析 | `clawhub install flowsint-integration` |
| S032 | `polyalert` | PolyAlert | Polymarket alert & monitoring | Polymarket 监控与告警 | `clawhub install polyalert` |
| S033 | `bot-dashboard` | Bot 仪表盘 | Multi-bot status dashboard | 多 Bot 状态仪表盘 | `clawhub install bot-dashboard` |
| S034 | `marketplace` | 技能市场 | Skill marketplace management | 技能市场管理 | `clawhub install marketplace` |
| S035 | `gumroad` | Gumroad | Gumroad product management | Gumroad 产品管理 | `clawhub install gumroad` |
| S036 | `qa-supervisor` | 质量监督 | Quality assurance & validation | 质量保证与验证 | `clawhub install qa-supervisor` |

---

### 📝 内容与媒体（7 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S037 | `shanmu-reporter` | 山木研报 | Professional financial report generator | 专业金融研报生成 | `clawhub install shanmu-reporter` |
| S038 | `video-factory` | 视频工厂 | Video generation & editing | 视频生成与编辑 | `clawhub install video-factory` |
| S039 | `ppt-chart-generator` | PPT 图表 | PowerPoint chart generation | PPT 图表生成 | `clawhub install ppt-chart-generator` |
| S040 | `qiaomu-info-card-designer` | 乔木卡片 | Magazine-style info card generator | 杂志质感信息卡片生成 | `clawhub install qiaomu-info-card-designer` |
| S041 | `tts` | 语音合成 | Text-to-speech conversion | 文字转语音 | `clawhub install tts` |
| S042 | `tts-alternatives` | 语音替代 | Alternative TTS services | 替代语音服务 | `clawhub install tts-alternatives` |
| S043 | `weather` | 天气 | Weather forecast via wttr.in/Open-Meteo | 天气预报 | `clawhub install weather` |

---

### 📱 平台集成（6 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S044 | `feishu` | 飞书 | Feishu doc/chat/wiki/bitable operations | 飞书文档/聊天/知识库/多维表格 | `clawhub install feishu` |
| S045 | `wechat` | 微信 | WeChat message & official account | 微信消息与公众号 | `clawhub install wechat` |
| S046 | `ssh` | SSH | SSH remote control | SSH 远程控制 | `clawhub install ssh` |
| S047 | `web` | 网页 | Web scraping & automation | 网页抓取与自动化 | `clawhub install web` |
| S048 | `tv-control` | 电视控制 | Smart TV remote control | 智能电视远程控制 | `clawhub install tv-control` |
| S049 | `today-stage` | 今日舞台 | Daily content staging | 每日内容舞台 | `clawhub install today-stage` |

---

### 🧰 工具与效率（8 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S050 | `auto-exec` | 自动执行 | Automatic task execution | 自动任务执行 | `clawhub install auto-exec` |
| S051 | `auto-retry-executor` | 自动重试 | Auto-retry mechanism for failed tasks | 失败任务自动重试机制 | `clawhub install auto-retry-executor` |
| S052 | `browser-adapter` | 浏览器适配器 | Playwright browser automation | Playwright 浏览器自动化 | `clawhub install browser-adapter` |
| S053 | `smart_ai_router` | AI 路由器 | Multi-model intelligent routing | 多模型智能路由 | `clawhub install smart_ai_router` |
| S054 | `smart_gateway` | 智能网关 | Request routing & load balancing | 请求路由与负载均衡 | `clawhub install smart_gateway` |
| S055 | `smart_communication` | 智能通讯 | Multi-platform message routing | 多平台消息路由 | `clawhub install smart_communication` |
| S056 | `smart-model-router` | 模型路由器 | Dynamic model selection | 动态模型选择 | `clawhub install smart-model-router` |
| S057 | `heal-state` | 状态修复 | System state recovery | 系统状态修复 | `clawhub install heal-state` |

---

### 🏢 企业与专业（5 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S058 | `suwen` | 素问 | Technical research & learning | 技术研究与学习 | `clawhub install suwen` |
| S059 | `paoding` | 庖丁 | Cost analysis & budget management | 成本分析与预算管理 | `clawhub install paoding` |
| S060 | `shanmu` | 山木 | Content creation & creativity | 内容创作与创意 | `clawhub install shanmu` |
| S061 | `yi` | 羿 | Monitoring & signal hunting | 监控与信号猎取 | `clawhub install yi` |
| S062 | `yijing` | 易经 | I Ching divination & wisdom | 易经占卜与智慧 | `clawhub install yijing` |

---

### 📚 核心与系统（5 个）

| 编号 | 英文名 | 中文名 | 关键功能 (EN) | 关键功能 (CN) | 安装包 |
|------|--------|--------|--------------|--------------|--------|
| S063 | `taiyi` | 太一 | Core AGI orchestration | 核心 AGI 统筹 | `clawhub install taiyi` |
| S064 | `steward` | 管家 | Resource scheduling & task management | 资源调度与任务管理 | `clawhub install steward` |
| S065 | `wangliang` | 罔两 | Data collection & CEO analysis | 数据采集与 CEO 分析 | `clawhub install wangliang` |
| S066 | `turboquant` | TurboQuant | Memory compression & optimization | 记忆压缩与优化 | `clawhub install turboquant` |
| S067 | `templates` | 模板 | Skill templates & boilerplates | Skill 模板与框架 | `clawhub install templates` |

---

## 📦 安装方式

### 方式 1: ClawHub（推荐）
```bash
# 安装单个 Skill
clawhub install <skill-name>

# 示例
clawhub install git-integration
clawhub install docker-ctl
clawhub install polymarket
```

### 方式 2: Git Clone
```bash
# 克隆到 skills 目录
git clone https://github.com/nicola-king/openclaw-<skill-name>.git ~/.openclaw/workspace/skills/<skill-name>

# 重载 Gateway
openclaw gateway reload
```

### 方式 3: 压缩包
```bash
# 解压到 skills 目录
tar -xzf <skill-name>.tar.gz -C ~/.openclaw/workspace/skills/

# 重载 Gateway
openclaw gateway reload
```

### 方式 4: 批量安装
```bash
# 安装 P0 核心工具
clawhub install git-integration npm-audit docker-ctl

# 安装云原生工具
clawhub install k8s-deploy terraform-apply aws-cli gcp-cli azure-cli

# 安装全部（谨慎使用）
clawhub install --all
```

---

## 📊 统计汇总

### 按类别

| 类别 | 数量 | 占比 |
|------|------|------|
| 核心工具 (P0) | 3 | 4.5% |
| 云原生 (P1) | 5 | 7.5% |
| 协作集成 (P2) | 6 | 9.0% |
| 趣味性 (P3) | 5 | 7.5% |
| 高级 AI (P4) | 5 | 7.5% |
| 交易与金融 | 6 | 9.0% |
| 数据与分析 | 6 | 9.0% |
| 内容与媒体 | 7 | 10.4% |
| 平台集成 | 6 | 9.0% |
| 工具与效率 | 8 | 11.9% |
| 企业与专业 | 5 | 7.5% |
| 核心与系统 | 5 | 7.5% |
| **总计** | **67+** | **100%** |

### 按发布状态

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 已发布 | 3 | git-integration, docker-ctl, k8s-deploy |
| 🟡 待发布 | 64 | 已创建文档，待配置 clawhub.yaml |
| 🔴 开发中 | - | 持续新增 |

### 按负责 Bot

| Bot | 负责 Skills | 占比 |
|-----|------------|------|
| 素问 (Suwen) | 15 | 22% |
| 罔两 (Wangliang) | 12 | 18% |
| 山木 (Shanmu) | 10 | 15% |
| 知几 (Zhiji) | 8 | 12% |
| 太一 (Taiyi) | 8 | 12% |
| 庖丁 (Paoding) | 5 | 7% |
| 守藏吏 (Shoucangli) | 5 | 7% |
| 羿 (Yi) | 4 | 6% |

---

## 🔗 相关文档

- **发布指南**: `docs/SKILL-PUBLISHING-GUIDE.md`
- **配置指南**: `docs/CLOUD-CLI-SETUP.md`
- **Claw-Code 融合**: `constitution/directives/CLAW-CODE-FUSION.md`
- **执行报告**: `reports/claw-fusion-final-report.md`

---

## 📚 相关链接

- **ClawHub**: https://clawhub.ai - OpenClaw 技能市场
- **OpenClaw 文档**: https://docs.openclaw.ai
- **太一 GitHub**: https://github.com/nicola-king
- **Discord 社区**: https://discord.gg/clawd

---

*更新时间：2026-04-03 10:24 | 太一 AGI v5.0 | 67+ Skills 完整目录*
