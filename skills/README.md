# 太一技能库 v2.0 - 整合版

> **版本**: 2.1.0 | **更新时间**: 2026-04-07 08:45  
> **技能数量**: 88 (原 127，减少 30.7%)  
> **状态**: ✅ 文档完善完成

---

## 📊 技能架构

### 三层架构

```
┌─────────────────────────────────────────┐
│  Layer 1: Bot 专属技能 (8 个)              │
│  太一/知几/山木/素问/罔两/庖丁/羿/守藏吏    │
└─────────────────────────────────────────┘
              ↓ 调用
┌─────────────────────────────────────────┐
│  Layer 2: 通用技能 (~40 个)               │
│  整合后：browser/gmgn/content/visual/... │
└─────────────────────────────────────────┘
              ↓ 依赖
┌─────────────────────────────────────────┐
│  Layer 3: 工具技能 (~40 个)               │
│  独立工具：feishu/ssh/tts/weather/...    │
└─────────────────────────────────────────┘
```

---

## 🏆 核心技能

### 基础设施

| 技能 | 说明 | 优先级 |
|------|------|--------|
| **smart-model-router** | 智能模型路由 | P0 |
| **smart-router** | 智能技能路由 | P0 |
| **shared** | 共享数据层 | P0 |

### 业务技能

| 技能 | 说明 | 优先级 |
|------|------|--------|
| **browser-automation** | 浏览器自动化 | P0 |
| **gmgn** | GMGN 链上交易 | P0 |
| **content-creator** | 内容创作引擎 | P0 |
| **visual-designer** | 视觉设计引擎 | P0 |
| **cli-toolkit** | CLI 工具集 | P1 |
| **monitoring** | 监控告警 | P1 |
| **trading** | 交易引擎 | P1 |

---

## 📈 整合成果

### P0 整合 (2026-04-07 08:19-08:50)

- ✅ browser-automation (3→1)
- ✅ smart-model-router (4→1)
- ✅ gmgn (6→2)
- ✅ content-creator (5→1)
- ✅ visual-designer (4→1)
- ✅ shared 共享层 (已存在)
- ✅ smart-router 路由引擎 (已存在)

**减少**: 14 技能 (11%)

### P1 整合 (2026-04-07 09:00-09:15)

- ✅ cli-toolkit (5→1)
- ✅ monitoring (4→1)
- ✅ trading (3→1)
- ✅ 技能注册表更新

**减少**: 9 技能 (8%)

### 累计

- **初始**: 127 技能
- **当前**: 88 技能
- **减少**: 39 技能 (30.7%)

---

## 🚀 快速开始

### 使用技能

```python
# 导入共享层
from skills.shared import SharedDatabase, EventBus

# 使用浏览器自动化
from skills.browser_automation import BrowserAutomation

# 使用 GMGN
from skills.gmgn import GMGN

# 使用内容创作
from skills.content_creator import ContentCreator
```

### 智能路由

```python
from skills.smart_router import SmartRouter

router = SmartRouter()
skill = router.route("帮我分析一下 Polymarket 市场")
# 自动选择最优技能
```

---

## 📚 文档

### 整合报告
- [P0 整合报告](../reports/skill-integration-p0.md)
- [P1 整合报告](../reports/skill-integration-p1.md)
- [P2 文档完善报告](../reports/p2-docs-completion.md)

### 使用文档
- [技能使用手册](USAGE.md)
- [技能注册表](registry.yaml)

### 技能文档
- [GMGN](gmgn/README.md) - 链上交易
- [Content Creator](content-creator/README.md) - 内容创作
- [Visual Designer](visual-designer/README.md) - 视觉设计
- [CLI Toolkit](cli-toolkit/README.md) - CLI 工具集
- [Monitoring](monitoring/README.md) - 监控告警
- [Trading](trading/README.md) - 交易引擎
- [Smart Router](smart-router/README.md) - 智能技能路由
- [Smart Model Router](smart-model-router/README.md) - 智能模型路由
- [Browser Automation](browser-automation/README.md) - 浏览器自动化
- [Shared](shared/README.md) - 共享数据层

---

## 📋 完整技能列表

### Bot 专属 (8)

| 技能 | 负责 Bot | 说明 |
|------|---------|------|
| taiyi | 太一 | AGI 执行总管 |
| zhiji | 知几 | 量化交易策略 |
| zhiji-sentiment | 知几 | 金融情绪分析 |
| shanmu | 山木 | 内容创意生成 |
| shanmu-reporter | 山木 | 金融研报生成 |
| suwen | 素问 | 技术开发 |
| wangliang | 罔两 | 知识库搜索 |
| paoding | 庖丁 | 预算成本分析 |

### 基础设施 (5)

| 技能 | 说明 |
|------|------|
| smart-model-router | 智能模型路由引擎 |
| smart-router | 智能技能路由引擎 |
| shared | 共享数据层 (数据库/事件总线/缓存) |
| task-orchestrator | 任务编排引擎 |
| smart-skills-manager | 智能技能管理器 |

### 浏览器自动化 (2)

| 技能 | 说明 |
|------|------|
| browser-automation | Playwright 网页导航/交互/截图 |
| geo-automation | 地理位置自动化 |

### 交易金融 (10)

| 技能 | 说明 |
|------|------|
| gmgn | GMGN 链上交易统一 API |
| gmgn-cooking | 代币发射平台 |
| trading | 交易引擎 (币安/Polymarket) |
| portfolio-tracker | 投资组合追踪 |
| alpha-vantage | 股票/外汇数据 |
| coingecko-price | 加密货币价格 |
| news-fetcher | 新闻数据采集 |
| public-apis-index | 公共 API 索引 |
| turboquant | 量化交易框架 |
| tianji | 聪明钱追踪 |

### 内容创作 (4)

| 技能 | 说明 |
|------|------|
| content-creator | 内容创作引擎 (排期/优化/发布) |
| shanmu-reporter | 专业金融研报 |
| epub-book-generator | EPUB 电子书生成 |
| video-factory | 视频工厂 |

### 视觉设计 (4)

| 技能 | 说明 |
|------|------|
| visual-designer | 图表/卡片/艺术生成 |
| unsplash-image | 高质量图片搜索 |
| paddleocr | OCR 文字识别 |
| video-processor | 视频处理 |

### CLI 工具 (8)

| 技能 | 说明 |
|------|------|
| cli-toolkit | 云厂商/DevOps 工具集 |
| git-integration | Git 操作集成 |
| gemini-cli | Gemini CLI 封装 |
| jimeng-cli | 即梦 CLI 封装 |
| notebooklm-cli | NotebookLM CLI |
| ssh | SSH 远程控制 |
| terraform-apply | Terraform 部署 |
| npm-audit | NPM 安全审计 |

### 监控告警 (4)

| 技能 | 说明 |
|------|------|
| monitoring | 监控告警系统 |
| self-check | 系统自检 |
| api-monitor | API 监控 |
| upgrade-guard | 升级守卫 |

### 数据通信 (8)

| 技能 | 说明 |
|------|------|
| feishu | 飞书消息/文档/多维表格 |
| wechat | 微信集成 |
| slack-notify | Slack 通知 |
| tts | 文字转语音 |
| tts-alternatives | TTS 替代方案 |
| webhook-relay | Webhook 中继 |
| email-sender | 邮件发送 |
| notion-db | Notion 数据库 |

### 开发工具 (6)

| 技能 | 说明 |
|------|------|
| github | GitHub 操作 |
| gh-issues | GitHub Issues 处理 |
| rust-bridge | Rust 桥接 |
| vector-db | 向量数据库 |
| rag-pipeline | RAG 流水线 |
| llm-finetune | LLM 微调 |

### 工作流 (8)

| 技能 | 说明 |
|------|------|
| arc-reel-workflow | 视频工作流 |
| ecommerce-workflow | 电商工作流 |
| the-well-processor | 内容处理器 |
| task-orchestrator | 任务编排 |
| flowsint-integration | Flowsint 集成 |
| zapier-trigger | Zapier 触发器 |
| airtable-sync | Airtable 同步 |
| crontab-manager | 定时任务管理 |

### 工具技能 (21)

| 技能 | 说明 |
|------|------|
| weather | 天气预报 |
| pet-companion | 宠物伴侣 |
| play-music | 音乐播放 |
| tv-control | 电视控制 |
| heal-state | 状态恢复 |
| steward | 管家服务 |
| yi | 易学咨询 |
| yijing | 易经占卜 |
| easter-egg | 彩蛋功能 |
| undercover-mode | 潜伏模式 |
| artistic-code | 艺术代码 |
| aesthetic-scorer | 美学评分 |
| agent-swap | Agent 交换 |
| cost-tracker | 成本追踪 |
| roi-tracker | ROI 追踪 |
| growth-experiment | 增长实验 |
| gumroad | Gumroad 集成 |
| marketplace | 市场集成 |
| meta-skill-creator | 元技能创建 |
| qa-supervisor | QA 监督 |
| today-stage | 今日阶段 |

---

*维护：太一 AGI | 技能库 v2.0*
