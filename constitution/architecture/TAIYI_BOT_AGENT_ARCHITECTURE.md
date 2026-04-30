# 🌟 太一系统 Bot/Agent 架构总览

> **统计时间**: 2026-04-15 21:56  
> **系统版本**: 太一 AGI · Level 3 (90-95%)  
> **架构模式**: 一元总控 + 三元组团 + 一键决策

---

## 📊 总体统计

| 类别 | 数量 | 状态 |
|------|------|------|
| **核心 Bot** | 9 个 | ✅ 活跃 |
| **专业 Agent** | 15 个 | ✅ 活跃 |
| **工具 Bot** | 20+ 个 | ✅ 活跃 |
| **自动化 Skill** | 500+ 个 | ⚠️ 需清理 |
| **总计** | **544+ 个** | 🟡 优化中 |

---

## 🏗️ 架构分层

### 第一层：太一总控 (1 个)

```
┌─────────────────────────────────┐
│         太一 (Taiyi)            │
│  总控 Agent · 决策中枢 · 协调器   │
└─────────────────────────────────┘
```

**职责**:
- 任务接收与理解
- 智能体调度与分发
- 结果汇总与整合
- 最终决策与输出
- 质量把控与纠错

**位置**: `skills/07-system/taiyi/`

---

### 第二层：核心 Bot (9 个)

```
┌─────────────────────────────────────────────────┐
│              核心 Bot 层 (9 个)                    │
│  太一镜像 · 女娲 · 素问 · 山木 · 知几 · 庖丁 · 罔两 · 王良 · 太乙  │
└─────────────────────────────────────────────────┘
```

| 编号 | Bot 名称 | 职责域 | 位置 | 状态 |
|------|---------|--------|------|------|
| **B001** | 太一 (Taiyi) | 总控协调 | `skills/07-system/taiyi/` | ✅ |
| **B002** | 女娲 (Nuwa) | 技能创造 | `skills/07-system/nuwa-skill/` | ✅ |
| **B003** | 素问 (Suwen) | 技术开发 | `skills/07-system/suwen/` | ✅ |
| **B004** | 山木 (Shanmu) | 内容创意 | `skills/05-content/shanmu/` | ✅ |
| **B005** | 知几 (Zhiji) | 量化交易 | `skills/01-trading/zhiji/` | ✅ |
| **B006** | 庖丁 (Paoding) | 成本分析 | `skills/07-system/paoding/` | ✅ |
| **B007** | 罔两 (Wangliang) | 知识库 | `skills/07-system/wangliang/` | ✅ |
| **B008** | 王良 (Wangliang) | 知识问答 | `skills/07-system/wangliang/` | ✅ |
| **B009** | 太乙 (Taiyi-Artisan) | 艺术创作 | `skills/07-system/taiyi-artisan/` | ✅ |

---

### 第三层：专业 Agent (15 个)

```
┌─────────────────────────────────────────────────┐
│            专业 Agent 层 (15 个)                    │
│  交易 · 贸易 · 图表 · 语音 · 设计 · 教育 · 办公 · 记忆 · 视频 · 内容  │
└─────────────────────────────────────────────────┘
```

#### 交易类 (4 个)

| 编号 | Agent 名称 | 职责 | 位置 | 状态 |
|------|-----------|------|------|------|
| **A001** | Binance Trading Agent | 币安交易 | `skills/01-trading/binance-trading-agent/` | ✅ |
| **A002** | GMGN Trading Agent | GMGN 交易 | `skills/01-trading/gmgn-trading-agent/` | ✅ |
| **A003** | Polymarket Trading Agent | Polymarket | `skills/01-trading/polymarket-trading-agent/` | ✅ |
| **A004** | Cross-Border Trade Agent | 跨境贸易 | `skills/01-trading/cross-border-trade-agent/` | ✅ |

#### 内容类 (4 个)

| 编号 | Agent 名称 | 职责 | 位置 | 状态 |
|------|-----------|------|------|------|
| **A005** | Content Creator | 内容创作 | `skills/05-content/content-creator/` | ✅ |
| **A006** | Shanmu Reporter | 研报生成 | `skills/05-content/shanmu-reporter/` | ✅ |
| **A007** | Video Factory | 视频工厂 | `skills/05-content/video-factory/` | ✅ |
| **A008** | TTS | 语音合成 | `skills/05-content/tts/` | ✅ |

#### 系统类 (4 个)

| 编号 | Agent 名称 | 职责 | 位置 | 状态 |
|------|-----------|------|------|------|
| **A009** | Taiyi Diagram Agent | 图表生成 | `skills/07-system/taiyi-diagram-agent/` | ✅ |
| **A010** | Taiyi Voice Agent | 语音处理 | `skills/07-system/taiyi-voice-agent/` | ✅ |
| **A011** | Taiyi Education Agent | 教育 | `skills/07-system/taiyi-education-agent/` | ✅ |
| **A012** | Taiyi Office Agent | 办公 | `skills/07-system/taiyi-office-agent/` | ✅ |

#### 功能类 (3 个)

| 编号 | Agent 名称 | 职责 | 位置 | 状态 |
|------|-----------|------|------|------|
| **A013** | Taiyi Memory Palace | 记忆宫殿 | `skills/07-system/taiyi-memory-palace/` | ✅ |
| **A014** | Design Agent | 设计 | `skills/07-system/taiyi-design-agent/` | ✅ |
| **A015** | Dao Agent | DAO | `skills/07-system/dao-agent/` | ✅ |

---

### 第四层：工具 Bot (20+ 个)

```
┌─────────────────────────────────────────────────┐
│           工具 Bot 层 (20+ 个)                     │
│  发布 · 调度 · 优化 · 生成 · 处理 · 路由 · 监控 · 验证  │
└─────────────────────────────────────────────────┘
```

| 编号 | 工具 Bot | 职责 | 位置 |
|------|---------|------|------|
| **T001** | Doc Publisher | 文档发布 | `skills/05-content/content-creator/publisher/` |
| **T002** | Scheduler | 任务调度 | `skills/05-content/content-creator/scheduler/` |
| **T003** | Chart Generator | 图表生成 | `skills/05-content/content-creator/chart-generator/` |
| **T004** | Blender 3D | 3D 渲染 | `skills/05-content/content-creator/blender-3d/` |
| **T005** | Exporter | 导出器 | `skills/05-content/content-creator/chart-generator/exporter.py` |
| **T006** | Templates | 模板库 | `skills/05-content/content-creator/chart-generator/templates.py` |
| **T007** | PDF Exporter | PDF 导出 | `skills/05-content/content-creator/chart-generator/pdf_exporter.py` |
| **T008** | AI Parser | AI 解析 | `skills/05-content/content-creator/chart-generator/ai_parser.py` |
| **T009** | Recommender | 推荐引擎 | `skills/05-content/content-creator/chart-generator/recommender.py` |
| **T010** | Smart Model Router | 模型路由 | `skills/07-system/smart-model-router/` |
| **T011** | Geo Model Router | 地理路由 | `skills/07-system/geo-model-router/` |
| **T012** | Quality Validator | 质量验证 | `skills/07-system/quality-validator/` |
| **T013** | Error Handler | 错误处理 | `skills/07-system/error-handler/` |
| **T014** | Core Guardian | 核心守护 | `skills/07-system/core-guardian-agent/` |
| **T015** | Skill Dashboard | 技能仪表板 | `skills/07-system/skill-dashboard/` |
| **T016** | Bot Dashboard | Bot 仪表板 | `skills/07-system/bot-dashboard/` |
| **T017** | Issue Pitfalls | 问题记录 | `skills/07-system/issue-pitfalls-record/` |
| **T018** | OpenClaw Bot | OpenClaw | `skills/07-system/openclaw/` |
| **T019** | Marketplace | 市场 | `skills/07-system/marketplace/` |
| **T020** | Steward | 管家 | `skills/07-system/steward/` |

---

### 第五层：自动化 Skill (500+ 个)

```
┌─────────────────────────────────────────────────┐
│        自动化 Skill 层 (500+ 个)                   │
│  auto-skill-20260410-* (约 300 个)                │
│  auto-skill-20260411-* (约 150 个)                │
│  auto-skill-20260412-* (约 50 个)                 │
│  emerged-skill-* (约 20 个)                       │
└─────────────────────────────────────────────────┘
```

**状态**: ⚠️ **需要清理和整合**

**问题**:
- 大量重复技能
- 命名不规范
- 功能冗余
- 缺少文档

**解决方案**:
```
1. 蒸馏提炼 → 合并重复功能
2. 分类整理 → 归入对应 Bot/Agent
3. 清理归档 → 删除无用技能
4. 文档补充 → 完善 SKILL.md
```

---

## 🎯 组团模式 (按多 Agent 协作框架)

### 1. 跨境贸易组团

```
太一 (总控)
  ↓
├─ 市场分析师 (Market Analyst) - A004
├─ 客户开发师 (Business Developer) - T008
└─ 报告生成师 (Report Generator) - T001
```

**效率**: 12-36 倍提升

---

### 2. 图表生成组团

```
太一 (总控)
  ↓
├─ 智能解析师 (Smart Parser) - T008
├─ 图表生成师 (Chart Generator) - T003
└─ 导出验证师 (Export Validator) - T005 + T012
```

**效率**: 600 倍提升

---

### 3. 内容创作组团

```
太一 (总控)
  ↓
├─ 灵感收集师 (Idea Collector) - A005
├─ 内容创作师 (Content Creator) - A005
└─ 发布运营师 (Publish Manager) - T001
```

**效率**: 15-30 倍提升

---

### 4. 交易决策组团

```
太一 (总控)
  ↓
├─ 市场分析师 (Market Analyst) - A001/A002/A003
├─ 策略执行师 (Strategy Executor) - A001/A002/A003
└─ 交易验证师 (Trade Validator) - T012
```

**效率**: 自动决策

---

### 5. 语音处理组团

```
太一 (总控)
  ↓
├─ 语音识别师 (Speech Recognizer) - A010
├─ 命令执行师 (Command Executor) - A010
└─ 反馈验证师 (Feedback Validator) - T012
```

**效率**: 10-20 倍提升

---

## 📋 整合方案

### 阶段 1: 清理冗余 (2026-04-15 ~ 2026-04-20)

**任务**:
```
1. 删除 auto-skill-* 重复技能 (预计减少 80%)
2. 合并 emerged-skill-* 到对应 Bot/Agent
3. 归档 .backup 目录内容
4. 清理 empty/dummy 技能
```

**预期结果**:
```
Before: 544+ 个技能
After:  ~100 个核心技能
减少：~80%
```

---

### 阶段 2: 标准化 (2026-04-20 ~ 2026-04-25)

**任务**:
```
1. 统一命名规范 (Bot/Agent/Tool 前缀)
2. 完善 SKILL.md 文档
3. 建立技能索引
4. 实现技能注册机制
```

**命名规范**:
```
Bot 前缀：bot-* (如 bot-taiyi, bot-nuwa)
Agent 前缀：agent-* (如 agent-trading, agent-content)
Tool 前缀：tool-* (如 tool-publisher, tool-scheduler)
Skill 前缀：skill-* (如 skill-web-search, skill-pdf-export)
```

---

### 阶段 3: 组团化 (2026-04-25 ~ 2026-05-01)

**任务**:
```
1. 按组团模式重组 Bot/Agent
2. 实现多 Agent 协作框架
3. 建立通信协议
4. 测试组团效率
```

**目标组团**:
```
✅ 跨境贸易组团 (已完成)
✅ 图表生成组团 (已完成)
⏳ 内容创作组团 (进行中)
⏳ 交易决策组团 (进行中)
⏳ 语音处理组团 (进行中)
⏳ 设计创作组团 (计划中)
⏳ 教育办公组团 (计划中)
```

---

### 阶段 4: 智能化 (2026-05-01 ~ 2026-05-15)

**任务**:
```
1. 实现动态组团 (根据任务自动调整)
2. 自学习优化 (从历史学习)
3. 预测性执行 (提前准备)
4. 人机协作增强
```

---

## 📊 Bot/Agent 清单 (精简版)

### 核心 Bot (9 个)

```
✅ bot-taiyi          - 太一总控
✅ bot-nuwa          - 女娲技能创造
✅ bot-suwen         - 素问技术开发
✅ bot-shanmu        - 山木内容创意
✅ bot-zhiji         - 知几量化交易
✅ bot-paoding       - 庖丁成本分析
✅ bot-wangliang     - 罔两知识库
✅ bot-wangliang     - 王良知识问答
✅ bot-taiyi-artisan - 太乙艺术创作
```

### 专业 Agent (15 个)

```
交易类:
✅ agent-binance-trading
✅ agent-gmgn-trading
✅ agent-polymarket-trading
✅ agent-cross-border-trade

内容类:
✅ agent-content-creator
✅ agent-shanmu-reporter
✅ agent-video-factory
✅ agent-tts

系统类:
✅ agent-taiyi-diagram
✅ agent-taiyi-voice
✅ agent-taiyi-education
✅ agent-taiyi-office
✅ agent-taiyi-memory
✅ agent-design
✅ agent-dao
```

### 工具 Bot (20 个)

```
发布类:
✅ tool-doc-publisher
✅ tool-scheduler
✅ tool-optimizer

图表类:
✅ tool-chart-generator
✅ tool-blender-3d
✅ tool-exporter
✅ tool-templates
✅ tool-pdf-exporter

AI 类:
✅ tool-ai-parser
✅ tool-recommender

路由类:
✅ tool-smart-model-router
✅ tool-geo-model-router

验证类:
✅ tool-quality-validator
✅ tool-error-handler
✅ tool-core-guardian

管理类:
✅ tool-skill-dashboard
✅ tool-bot-dashboard
✅ tool-issue-pitfalls
✅ tool-openclaw
✅ tool-marketplace
✅ tool-steward
```

---

## 🎯 蒸馏提炼原则

### 1. 功能聚合

**原则**: 相同功能聚合到一个 Bot/Agent

**示例**:
```
Before:
- auto-skill-20260410-010001 (PDF 导出)
- auto-skill-20260410-020001 (PDF 导出)
- auto-skill-20260410-030001 (PDF 导出)

After:
- tool-pdf-exporter (统一 PDF 导出)
```

---

### 2. 职责单一

**原则**: 每个 Bot/Agent 只负责一个职责域

**示例**:
```
✅ tool-chart-generator - 只负责图表生成
✅ tool-pdf-exporter - 只负责 PDF 导出
✅ tool-quality-validator - 只负责质量验证
```

---

### 3. 可复用性

**原则**: 通用功能提取为独立 Tool

**示例**:
```
✅ tool-web-search - 所有 Bot 可复用
✅ tool-file-operation - 所有 Bot 可复用
✅ tool-api-call - 所有 Bot 可复用
```

---

### 4. 文档完整

**原则**: 每个 Bot/Agent 必须有完整文档

**文档结构**:
```markdown
# Bot/Agent 名称

## 职责
- 职责 1
- 职责 2

## 技能
- 技能 1
- 技能 2

## 使用方式
```python
from bot_name import BotClass
bot = BotClass()
result = bot.execute("任务")
```

## 依赖
- 依赖 1
- 依赖 2
```

---

## 📈 优化效果预测

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **技能总数** | 544+ | ~100 | -80% |
| **核心 Bot** | 混杂 | 9 个清晰 | +100% |
| **专业 Agent** | 混杂 | 15 个清晰 | +100% |
| **工具 Bot** | 混杂 | 20 个清晰 | +100% |
| **文档完整率** | <20% | 100% | +400% |
| **组团效率** | 手动 | 自动 | +1000% |
| **维护成本** | 高 | 低 | -70% |

---

## 🚀 执行计划

### 2026-04-15 (今天)

```
✅ 完成 Bot/Agent 全面盘点
✅ 创建架构总览文档
✅ 建立组团模式框架
⏳ 开始清理 auto-skill-* (进行中)
```

### 2026-04-16 ~ 2026-04-20

```
⏳ 完成 auto-skill-* 清理
⏳ 合并 emerged-skill-*
⏳ 建立技能索引
⏳ 完善核心 Bot 文档
```

### 2026-04-21 ~ 2026-04-25

```
⏳ 统一命名规范
⏳ 实现技能注册机制
⏳ 建立通信协议
⏳ 测试组团模式
```

### 2026-04-26 ~ 2026-05-01

```
⏳ 完成所有组团
⏳ 实现动态组团
⏳ 自学习优化
⏳ 性能调优
```

---

*太一 AGI · Bot/Agent 架构总览 v1.0 · 2026-04-15 21:56*

** 一元总控 + 三元组团 + 一键决策！544+ 技能 → 100 核心技能！**
