# 📚 太一技能分类整理方案

> **版本**: v1.0  
> **创建**: 2026-04-12 19:20  
> **技能总数**: 451 个  
> **目标**: 分类整理，易于查找

---

## 🎯 分类架构

### 一级分类 (8 大类)

```
skills/
├── 01-trading/          # 交易类
├── 02-business/         # 业务类
├── 03-automation/       # 自动化类
├── 04-integration/      # 集成类
├── 05-content/          # 内容类
├── 06-analysis/         # 分析类
├── 07-system/           # 系统类
└── 08-emerged/          # 涌现技能 (待整理)
```

---

## 📋 详细分类

### 01-trading/ 交易类 (~15 个)

**核心技能**:
- binance-trading-agent (币安交易)
- gmgn-trading-agent (GMGN 交易)
- polymarket-trading-agent (Polymarket 交易)
- cross-border-trade-agent (跨境贸易)
- zhiji-e (知几 -E 策略)
- zhiji-sentiment (情绪分析)
- turboquant (量化交易)
- trading (统一交易引擎)
- alpha-vantage (金融数据)
- coingecko-price (加密货币价格)
- portfolio-tracker (组合追踪)
- cost-tracker (成本追踪)

---

### 02-business/ 业务类 (~20 个)

**核心技能**:
- cost-agent (市政工程造价)
- civil-engineering-cost (工程造价)
- 市政工程造价 (定额库)
- airtable-sync (Airtable 同步)
- gumroad (Gumroad 销售)
- ecommerce-workflow (电商流程)
- lead-scoring (线索评分)
- buyer-scraper (买家爬虫)

---

### 03-automation/ 自动化类 (~50 个)

**核心技能**:
- auto-exec (自动执行)
- auto-retry-executor (自动重试)
- auto-skill-generator (自动生成技能)
- auto-evolution-system (自进化系统)
- self-heal (自愈)
- task-orchestrator (任务编排)
- smart-skills-manager (智能技能管理)
- crontab-manager (定时任务)
- daily-report-generator (日报生成)
- heartbeat-cli (心跳检查)
- emergency-stop (紧急停止)

---

### 04-integration/ 集成类 (~30 个)

**核心技能**:
- browser-automation (浏览器自动化)
- feishu (飞书集成)
- discord-integration (Discord)
- whatsapp-integration (WhatsApp)
- wechat (微信)
- slack-notify (Slack 通知)
- telegram (Telegram)
- baidu-netdisk-integration (百度网盘)
- github-integration (GitHub)
- git-integration (Git)
- ssh (SSH 远程)
- vector-db (向量数据库)

---

### 05-content/ 内容类 (~40 个)

**核心技能**:
- content-creator (内容创作)
- shanmu (山木 - 文案生成)
- visual-designer (视觉设计)
- artistic-code (艺术代码)
- aesthetic-scorer (美学评分)
- chinese-traditional-aesthetics (传统美学)
- classic-chinese-poetry (古诗词)
- china-textbook-search (教材搜索)
- epub-book-generator (电子书)
- tts (语音合成)
- tts-alternatives (TTS 替代)
- video-factory (视频工厂)
- video-processor (视频处理)
- jimeng-cli (即梦 CLI)

---

### 06-analysis/ 分析类 (~35 个)

**核心技能**:
- wangliang (王良 - 知识库)
- semantic-search (语义搜索)
- news-fetcher (新闻获取)
- unsplash-image (图片搜索)
- public-apis-index (API 索引)
- market-research (市场调研)
- competitor-analysis (竞争分析)
- swot-analysis (SWOT 分析)
- data-visualization (数据可视化)
- chart-generator (图表生成)

---

### 07-system/ 系统类 (~40 个)

**核心技能**:
- taiyi (太一 -AGI 总管)
- taiyi-memory-palace (记忆宫殿)
- taiyi-memory-v3 (记忆系统 v3.0)
- taiyi-voice-agent (语音 Agent)
- taiyi-education-agent (教育 Agent)
- taiyi-office-agent (办公 Agent)
- taiyi-diagram-agent (图表 Agent)
- smart-model-router (模型路由)
- smart-router (智能路由)
- model-swap (模型切换)
- qa-supervisor (QA 监督)
- healthcheck (健康检查)
- security-hardening (安全加固)
- npm-audit (NPM 审计)
- cli-toolkit (CLI 工具集)

---

### 08-emerged/ 涌现技能 (~220 个)

**待整理技能**:
- emerged-skill-20260410-* (100+ 个)
- emerged-skill-20260411-* (80+ 个)
- emerged-skill-20260412-* (40+ 个)

**处理策略**:
1. 逐个分析功能
2. 归类到上述 7 大类
3. 重命名规范
4. 删除重复/无用

---

## 🗺️ 实施路线

### Phase 1: 创建分类目录 (10 分钟)
```bash
mkdir -p skills/{01-trading,02-business,03-automation,04-integration,05-content,06-analysis,07-system,08-emerged}
```

### Phase 2: 迁移核心技能 (30 分钟)
```bash
# 交易类
mv skills/binance-trading-agent skills/01-trading/
mv skills/gmgn-trading-agent skills/01-trading/
# ...
```

### Phase 3: 整理涌现技能 (2 小时)
```bash
# 分析每个 emerged-skill-*
# 归类到对应分类
# 重命名规范
```

### Phase 4: 更新引用 (30 分钟)
```bash
# 更新 SKILL.md 中的路径
# 更新配置文件
# 测试功能
```

---

## 📊 预期效果

**整理前**:
```
skills/ (451 个技能混在一起)
├── binance-trading-agent/
├── gmgn-trading-agent/
├── emerged-skill-20260410-005931/
├── emerged-skill-20260410-010001/
├── ... (450+ 个)
```

**整理后**:
```
skills/
├── 01-trading/ (15 个)
│   ├── binance-trading-agent/
│   ├── gmgn-trading-agent/
│   └── ...
├── 02-business/ (20 个)
├── 03-automation/ (50 个)
├── 04-integration/ (30 个)
├── 05-content/ (40 个)
├── 06-analysis/ (35 个)
├── 07-system/ (40 个)
└── 08-emerged/ (220 个，待整理)
```

---

## 🔧 自动化整理脚本

```bash
#!/bin/bash
# 技能分类整理脚本

# 创建分类目录
mkdir -p skills/{01-trading,02-business,03-automation,04-integration,05-content,06-analysis,07-system,08-emerged}

# 迁移交易类
mv skills/binance-trading-agent skills/01-trading/ 2>/dev/null
mv skills/gmgn-trading-agent skills/01-trading/ 2>/dev/null
mv skills/polymarket-trading-agent skills/01-trading/ 2>/dev/null
mv skills/cross-border-trade-agent skills/01-trading/ 2>/dev/null
mv skills/zhiji-e skills/01-trading/ 2>/dev/null
mv skills/zhiji-sentiment skills/01-trading/ 2>/dev/null
mv skills/turboquant skills/01-trading/ 2>/dev/null
mv skills/trading skills/01-trading/ 2>/dev/null

# 迁移集成类
mv skills/browser-automation skills/04-integration/ 2>/dev/null
mv skills/feishu skills/04-integration/ 2>/dev/null
mv skills/discord-integration skills/04-integration/ 2>/dev/null
mv skills/wechat skills/04-integration/ 2>/dev/null
mv skills/ssh skills/04-integration/ 2>/dev/null

# 迁移系统类
mv skills/taiyi skills/07-system/ 2>/dev/null
mv skills/taiyi-memory-palace skills/07-system/ 2>/dev/null
mv skills/taiyi-memory-v3 skills/07-system/ 2>/dev/null
mv skills/taiyi-voice-agent skills/07-system/ 2>/dev/null
mv skills/taiyi-education-agent skills/07-system/ 2>/dev/null
mv skills/taiyi-office-agent skills/07-system/ 2>/dev/null
mv skills/taiyi-diagram-agent skills/07-system/ 2>/dev/null

# 保留涌现技能
mv skills/emerged-skill-* skills/08-emerged/ 2>/dev/null

echo "✅ 技能分类整理完成！"
```

---

## ✅ 验证清单

整理完成后检查:
- [ ] 所有技能已归类
- [ ] 路径引用已更新
- [ ] 功能测试通过
- [ ] 文档已更新
- [ ] Git 已提交

---

**📚 太一技能分类整理方案 v1.0**

**太一 AGI · 2026-04-12**
