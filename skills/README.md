# 📚 太一技能库索引

> **版本**: v2.0 (分类整理版)  
> **更新**: 2026-04-12 19:20  
> **技能总数**: 451 个  
> **分类数**: 8 大类

---

## 🗂️ 分类导航

| 分类 | 目录 | 数量 | 说明 |
|------|------|------|------|
| **01** | [01-trading/](#01-trading-交易类) | ~15 | 交易类技能 |
| **02** | [02-business/](#02-business-业务类) | ~20 | 业务类技能 |
| **03** | [03-automation/](#03-automation-自动化类) | ~50 | 自动化类技能 |
| **04** | [04-integration/](#04-integration-集成类) | ~30 | 集成类技能 |
| **05** | [05-content/](#05-content-内容类) | ~40 | 内容类技能 |
| **06** | [06-analysis/](#06-analysis-分析类) | ~35 | 分析类技能 |
| **07** | [07-system/](#07-system-系统类) | ~40 | 系统类技能 |
| **08** | [08-emerged/](#08-emerged-涌现技能) | ~220 | 涌现技能 (待整理) |

---

## 📋 详细分类

### 01-trading/ 交易类

**核心技能**:
- `binance-trading-agent` - 币安交易 Agent
- `gmgn-trading-agent` - GMGN 链上交易 Agent
- `polymarket-trading-agent` - Polymarket 预测市场交易 Agent
- `cross-border-trade-agent` - 跨境贸易 Agent
- `zhiji-sentiment` - 知几情绪分析
- `turboquant` - TurboQuant 量化交易
- `trading` - 统一交易引擎
- `alpha-vantage` - Alpha Vantage 金融数据
- `coingecko-price` - CoinGecko 加密货币价格
- `portfolio-tracker` - 投资组合追踪
- `cost-tracker` - 成本追踪

**用途**: 交易执行、量化策略、金融数据分析

---

### 02-business/ 业务类

**核心技能**:
- `cost-agent` - 市政工程造价 Agent
- `civil-engineering-cost` - 土木工程造价
- `市政工程造价` - 定额知识库
- `airtable-sync` - Airtable 数据同步
- `gumroad` - Gumroad 销售管理
- `ecommerce-workflow` - 电商工作流程

**用途**: 工程造价、业务管理、销售流程

---

### 03-automation/ 自动化类

**核心技能**:
- `auto-exec` - 自动执行
- `auto-retry-executor` - 自动重试执行
- `auto-skill-generator` - 自动生成技能
- `auto-evolution-system` - 自进化系统
- `self-heal` - 自愈系统
- `task-orchestrator` - 任务编排
- `smart-skills-manager` - 智能技能管理
- `crontab-manager` - 定时任务管理
- `daily-report-generator` - 日报生成
- `heartbeat-cli` - 心跳检查
- `emergency-stop` - 紧急停止

**用途**: 自动化任务、系统维护、定时执行

---

### 04-integration/ 集成类

**核心技能**:
- `browser-automation` - 浏览器自动化
- `feishu` - 飞书集成
- `discord-integration` - Discord 集成
- `wechat` - 微信集成
- `ssh` - SSH 远程控制
- `baidu-netdisk-integration` - 百度网盘集成
- `git-integration` - Git 集成

**用途**: 第三方平台集成、外部服务连接

---

### 05-content/ 内容类

**核心技能**:
- `content-creator` - 内容创作引擎
- `shanmu` - 山木文案生成
- `visual-designer` - 视觉设计引擎
- `artistic-code` - 艺术代码生成
- `aesthetic-scorer` - 美学评分
- `chinese-traditional-aesthetics` - 中国传统美学
- `classic-chinese-poetry` - 中国古典诗词
- `china-textbook-search` - 教材搜索
- `epub-book-generator` - EPUB 电子书生成
- `tts` - 语音合成
- `video-factory` - 视频工厂
- `video-processor` - 视频处理

**用途**: 内容创作、视觉设计、媒体处理

---

### 06-analysis/ 分析类

**核心技能**:
- `wangliang` - 王良知识库搜索
- `semantic-search` - 语义搜索
- `news-fetcher` - 新闻获取
- `unsplash-image` - Unsplash 图片搜索
- `public-apis-index` - 公共 API 索引
- `data-visualization` - 数据可视化
- `chart-generator` - 图表生成

**用途**: 数据分析、信息检索、可视化

---

### 07-system/ 系统类

**核心技能**:
- `taiyi` - 太一 AGI 总管 ⭐
- `taiyi-memory-palace` - 太一记忆宫殿
- `taiyi-memory-v3` - 太一记忆系统 v3.0
- `taiyi-voice-agent` - 太一语音 Agent
- `taiyi-education-agent` - 太一教育 Agent
- `taiyi-office-agent` - 太一办公 Agent
- `taiyi-diagram-agent` - 太一图表 Agent
- `smart-model-router` - 智能模型路由
- `smart-router` - 智能路由
- `healthcheck` - 健康检查
- `security-hardening` - 安全加固
- `npm-audit` - NPM 安全审计
- `cli-toolkit` - CLI 工具集

**用途**: 系统核心、模型调度、安全管理

---

### 08-emerged/ 涌现技能

**说明**: 自进化系统自动生成的技能，共 220+ 个

**命名规则**:
```
emerged-skill-YYYYMMDD-HHMMSS/
```

**处理策略**:
1. 定期分析功能
2. 归类到上述 7 大类
3. 重命名规范
4. 删除重复/无用

**待整理数量**: ~220 个

---

## 🔍 快速查找

**按名称搜索**:
```bash
cd /home/nicola/.openclaw/workspace/skills
find . -name "*trading*" -type d
```

**按分类查找**:
```bash
ls -la 01-trading/
ls -la 07-system/
```

**查看技能详情**:
```bash
cat 01-trading/binance-trading-agent/SKILL.md
```

---

## 📊 统计信息

| 指标 | 数值 |
|------|------|
| 技能总数 | 451 个 |
| 已分类 | 230 个 (51%) |
| 待整理 | 220 个 (49%) |
| 分类数 | 8 大类 |
| GitHub 发布 | 9 个 |

---

## 🔗 相关链接

- **GitHub**: https://github.com/nicola-king
- **文档**: `/home/nicola/.openclaw/workspace/docs/`
- **分类方案**: `SKILLS_CATEGORY_PLAN.md`

---

**📚 太一技能库 - 分类整理 v2.0**

**太一 AGI · 2026-04-12**
