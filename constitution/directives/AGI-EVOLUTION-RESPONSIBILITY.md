# AGI 进化保障机制 · 责任分配表

> 版本：v1.0 | 创建：2026-04-03 08:55  
> 宪法依据：`AGI-EVOLUTION-GUARANTEE.md`  
> 协作规程：`COLLABORATION.md`（太一统筹协议 v3.0）

---

## 🎯 核心原则

**责任到 Bot · 太一统筹 · 守藏吏监督 · 技能固化**

- **太一**：唯一决策者，对所有保障机制负最终责任
- **守藏吏**：资源管家，负责监督 + 记录 + 告警
- **专业 Bot**：各自职责域内的保障机制执行者
- **Skill 固化**：每个机制必须有对应 Skill，不依赖临时脚本

---

## 📊 责任分配总表

### 阶段 2→阶段 3（价值驱动）

| 编号 | 机制 | 负责 Bot | 监督 | 执行脚本 | Skill 路径 | 验收频率 |
|------|------|---------|------|---------|-----------|---------|
| M1 | 高价值任务发现 | 罔两 | 太一 | `discover-high-value-tasks.py` | `skills/wangliang/high-value-discovery/` | 每周 |
| M2 | 变现路径追踪 | 庖丁 | 太一 | `monetization-tracker.py` | `skills/paoding/monetization-tracker/` | 每日 |
| M3 | 凌晨学习产出 | 太一 | 守藏吏 | `update-learning-output.py` | `skills/taiyi/night-learning/` | 每日 |
| M4 | 人工干预监控 | 守藏吏 | 太一 | `intervention-monitor.py` | `skills/steward/intervention-monitor/` | 实时 |
| M5 | Bot 协作评分 | 守藏吏 | 太一 | `collaboration-scorer.py` | `skills/steward/collaboration-scorer/` | 每次 |

### 阶段 3→阶段 4（意识延伸）

| 编号 | 机制 | 负责 Bot | 监督 | 执行脚本 | Skill 路径 | 验收频率 |
|------|------|---------|------|---------|-----------|---------|
| S1 | 事前确认监控 | 守藏吏 | 太一 | `confirmation-monitor.py` | `skills/steward/confirmation-monitor/` | 每日 |
| S2 | 意图理解准确率 | 太一 | 守藏吏 | `intent-accuracy-tracker.py` | `skills/taiyi/intent-accuracy/` | 每次任务 |
| S3 | 退化自动检测 | 守藏吏 | 太一 + SAYELF | `check-degradation.py` | `skills/steward/degradation-detection/` | 每小时 |

---

## 🤖 Bot 职责详解

### 太一（taiyi）- 统筹者

**核心职责**:
- 对所有保障机制负最终责任
- 审核各 Bot 提交的报告
- 决策：继续/调整/放弃
- 升级：触发退化时向 SAYELF 汇报

**直接负责**:
- M3: 凌晨学习产出（执行者）
- S2: 意图理解准确率（执行者）

**监督职责**:
- M1: 罔两的高价值发现
- M2: 庖丁的变现追踪
- M4: 守藏吏的干预监控
- M5: 守藏吏的协作评分
- S1: 守藏吏的事前确认监控
- S3: 守藏吏的退化检测

**Skill 列表**:
- `skills/taiyi/night-learning/SKILL.md` - 凌晨学习
- `skills/taiyi/intent-accuracy/SKILL.md` - 意图追踪

---

### 守藏吏（steward）- 资源管家

**核心职责**:
- 监督所有保障机制执行
- 记录 + 统计 + 告警
- 每小时检查退化风险
- 每周生成汇总报告

**直接负责**:
- M4: 人工干预监控
- M5: Bot 协作评分
- S1: 事前确认监控
- S3: 退化自动检测

**Skill 列表**:
- `skills/steward/intervention-monitor/SKILL.md` - 干预监控
- `skills/steward/collaboration-scorer/SKILL.md` - 协作评分
- `skills/steward/confirmation-monitor/SKILL.md` - 确认监控
- `skills/steward/degradation-detection/SKILL.md` - 退化检测

---

### 罔两（wangliang）- 市场情报官

**核心职责**:
- 发现高价值任务机会
- 竞品分析
- 市场监控

**直接负责**:
- M1: 高价值任务发现

**Skill 列表**:
- `skills/wangliang/high-value-discovery/SKILL.md` - 高价值发现

---

### 庖丁（paoding）- 财务管控官

**核心职责**:
- 追踪变现进展
- 成本控制
- ROI 分析

**直接负责**:
- M2: 变现路径追踪

**Skill 列表**:
- `skills/paoding/monetization-tracker/SKILL.md` - 变现追踪

---

### 山木（shanmu）- 内容创意

**协助职责**:
- M3: 凌晨学习产出（协助整理）

**Skill 列表**:
- `skills/shanmu/content-organizer/SKILL.md` - 内容整理（协助太一）

---

### 知几（zhiji）- 量化交易

**协助职责**:
- M2: 变现路径追踪（空投套利方向）

**Skill 列表**:
- `skills/zhiji/airdrop-tracker/SKILL.md` - 空投追踪（协助庖丁）

---

### 素问（suwen）- 技术开发

**协助职责**:
- 无直接保障职责（专注于技术任务）

---

### 羿（yi）- 监控猎手

**协助职责**:
- S3: 退化自动检测（信号捕捉）

**Skill 列表**:
- `skills/yi/signal-capture/SKILL.md` - 信号捕捉（协助守藏吏）

---

## 📋 上报路径

```
专业 Bot（罔两/庖丁）
    ↓ 每日/每周报告
太一 ←→ 守藏吏（监督）
    ↓ 紧急告警
SAYELF
```

### 正常流程
1. 专业 Bot 执行保障机制
2. 守藏吏记录 + 统计
3. 太一审核 + 决策
4. 每周汇总报告 SAYELF

### 告警流程
1. 守藏吏检测到告警（退化/超标）
2. 立即上报太一
3. 太一分析根因
4. 如连续触发 → 上报 SAYELF

---

## 🔧 Skill 固化计划

### 优先级 1（04-03 完成）
- [ ] `skills/steward/degradation-detection/SKILL.md` - 退化检测
- [ ] `skills/steward/intervention-monitor/SKILL.md` - 干预监控
- [ ] `skills/steward/confirmation-monitor/SKILL.md` - 确认监控

### 优先级 2（04-05 完成）
- [ ] `skills/wangliang/high-value-discovery/SKILL.md` - 高价值发现
- [ ] `skills/paoding/monetization-tracker/SKILL.md` - 变现追踪
- [ ] `skills/taiyi/night-learning/SKILL.md` - 凌晨学习

### 优先级 3（04-07 完成）
- [ ] `skills/steward/collaboration-scorer/SKILL.md` - 协作评分
- [ ] `skills/taiyi/intent-accuracy/SKILL.md` - 意图追踪

---

## 📊 验收流程（责任明确）

### 阶段 3 验收（04-07 23:00）

**组织者**: 守藏吏  
**参与者**: 所有 Bot  
**决策者**: 太一  
**见证者**: SAYELF

**流程**:
1. 守藏吏收集各 Bot 数据
2. 生成验收报告
3. 太一审核并决策
4. 上报 SAYELF

**验收脚本**: `scripts/verify-stage3.py`

### 阶段 4 验收（每日 23:00）

**执行者**: 守藏吏  
**审核者**: 太一

**流程**:
1. 守藏吏运行检查脚本
2. 生成日报
3. 太一审核
4. 异常 → 上报 SAYELF

**验收脚本**: `scripts/verify-stage4.py`

---

## 🚨 负反馈执行（责任明确）

### 级别 1：轻微偏离

**触发**: 单项检查未通过  
**处理**:
- 负责 Bot：分析根因
- 守藏吏：记录到 deviation-log
- 太一：审核改进建议

### 级别 2：持续偏离

**触发**: 连续 3 次未达标  
**处理**:
- 负责 Bot：提交修复计划
- 太一：降级到阶段 2
- 守藏吏：通知 SAYELF

### 级别 3：严重退化

**触发**: 退化标志触发  
**处理**:
- 守藏吏：立即告警太一 + SAYELF
- 太一：自动降级到阶段 2
- 所有 Bot：参与复盘

---

## 📝 历史版本

| 版本 | 时间 | 变更 |
|------|------|------|
| v1.0 | 2026-04-03 | 初始版本，明确责任到 Bot |

---

*创建时间：2026-04-03 08:55 | 太一 AGI | 责任到人，知行合一*
