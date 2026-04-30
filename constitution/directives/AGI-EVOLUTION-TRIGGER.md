# AGI 进化保障 · 智能自动化触发机制

> 版本：v1.0 | 创建：2026-04-03 09:10  
> 状态：✅ 已配置完整 Cron 触发

---

## 🎯 核心原则

**Cron 触发 > 人工触发 · Bot 自主执行 > 等待指令 · 事件驱动 > 定时轮询**

---

## 📊 触发机制总览

### 完全自动化（Cron + Bot Skill）

| 机制 | 负责 Bot | Cron 频率 | 触发脚本 | 状态 |
|------|---------|----------|---------|------|
| M1 高价值发现 | 罔两 | 每日 01:00 | `skills/wangliang/high-value-discovery/run.py` | ✅ 已配置 |
| M2 变现追踪 | 庖丁 | 每日 23:00 | `skills/paoding/monetization-tracker/run.py` | 🟡 待创建 |
| M3 凌晨学习 | 太一 | 每日 01:00 | `skills/taiyi/night-learning/run.py` | 🟡 待创建 |
| M4 干预监控 | 守藏吏 | 每小时 | `skills/steward/intervention-monitor/run.py` | ✅ 已配置 |
| M5 协作评分 | 守藏吏 | 事件驱动 | `skills/steward/collaboration-scorer/run.py` | 🟡 待创建 |
| S1 事前确认 | 守藏吏 | 每小时 | `skills/steward/confirmation-monitor/run.py` | 🟡 待创建 |
| S2 意图准确 | 太一 | 事件驱动 | `skills/taiyi/intent-accuracy/run.py` | 🟡 待创建 |
| S3 退化检测 | 守藏吏 | 每小时 | `skills/steward/degradation-detection/run.py` | ✅ 已配置 |

**自动化率**: 3/8 = 37.5%（今日目标 100%）

---

## 🤖 触发流程图

### 层级 1：Cron 定时触发（无人值守）

```
Cron 调度器
    ↓ 每日 01:00
罔两 Skill → 扫描 GitHub/竞品/用户兴趣 → 生成机会报告 → 上报太一
    ↓ 每小时
守藏吏 Skill → 检查干预/退化 → 告警 → 更新状态面板
    ↓ 每日 23:00
阶段 4 验收 → 检查指标 → 生成日报 → 上报太一
```

### 层级 2：事件驱动触发（实时响应）

```
SAYELF 消息 → 意图识别 → 自动记录（意图准确率）
    ↓
多 Bot 协作完成 → 自动评分（协作流畅度）
    ↓
变现收入产生 → 自动追踪（庖丁 Skill）
```

---

## 📋 已配置 Cron（09:10 更新）

```bash
# === AGI 进化保障自动化 ===

# 罔两高价值发现（每日 01:00）
0 1 * * * cd /home/nicola/.openclaw/workspace && python3 skills/wangliang/high-value-discovery/run.py >> logs/high-value-discovery.log 2>&1

# 守藏吏干预监控（每小时）
0 * * * * cd /home/nicola/.openclaw/workspace && python3 skills/steward/intervention-monitor/run.py >> logs/intervention-monitor.log 2>&1

# 状态面板更新（每小时）
0 * * * * cd /home/nicola/.openclaw/workspace && python3 scripts/update-evolution-state.py >> logs/evolution-state.log 2>&1

# 退化检测（每小时）
0 * * * * cd /home/nicola/.openclaw/workspace && python3 scripts/check-degradation.py >> logs/degradation-check.log 2>&1

# 阶段 4 验收（每日 23:00）
0 23 * * * cd /home/nicola/.openclaw/workspace && python3 scripts/verify-stage4.py >> logs/verify-stage4.log 2>&1

# 阶段 3 验收（04-07 23:00）
0 23 7 4 * cd /home/nicola/.openclaw/workspace && python3 scripts/verify-stage3.py >> logs/verify-stage3.log 2>&1
```

**总计**: 6 项 Cron，全部配置完成 ✅

---

## 🔧 执行流程详解

### 流程 1：高价值发现（罔两）

```
01:00 Cron 触发
    ↓
run.py 启动
    ↓
1. 分析竞品（PolyCop Bot 等）
2. 提取用户兴趣（MEMORY.md）
3. 生成机会报告
    ↓
写入 memory/high-value-opportunities.md
    ↓
发送太一消息（A 级机会摘要）
    ↓
太一决策 → 山木执行 → 写入 HEARTBEAT.md
```

### 流程 2：干预监控（守藏吏）

```
每小时 Cron 触发
    ↓
run.py 启动
    ↓
1. 读取 intervention-log.md
2. 统计今日/本周干预次数
3. 检查阈值（≥3 次/日，>1 次/周）
    ↓
超标 → 发送太一告警
不超标 → 记录日志
    ↓
更新状态面板
```

### 流程 3：退化检测（守藏吏）

```
每小时 Cron 触发
    ↓
check-degradation.py 启动
    ↓
1. 检查等待指令（连续 3 任务）
2. 检查事前确认（>5 次/天）
3. 检查价值创造（连续 7 天无）
4. 检查人工干预（>3 次/周）
    ↓
发现风险 → 写入 degradation-alert.md → 告警太一 + SAYELF
无风险 → 记录"✅ 无退化风险"
```

---

## 📊 自动化程度对比

### 创建前（08:50）
- Cron 配置：2 项
- Skill 固化：0 项
- Bot 自主：0%
- 人工触发：100%

### 创建后（09:10）
- Cron 配置：6 项 ✅
- Skill 固化：2 项 ✅
- Bot 自主：37.5% 🟡
- 人工触发：62.5%

### 目标（今日 23:00 前）
- Cron 配置：8 项
- Skill 固化：5 项
- Bot 自主：100%
- 人工触发：0%

---

## 🚨 异常处理

### Cron 执行失败
```
检测：日志文件>1 小时未更新
动作：守藏吏告警太一
修复：手动执行 + 检查 Cron 状态
```

### Bot Skill 执行失败
```
检测：输出文件未生成
动作：重试 3 次，失败则告警
修复：检查依赖 + 重新执行
```

### 阈值超标
```
检测：守藏吏实时监控
动作：立即告警太一
修复：太一决策 + 根因分析
```

---

## 📝 日志文件清单

| 文件 | 内容 | 频率 | 大小 |
|------|------|------|------|
| `high-value-discovery.log` | 罔两执行日志 | 每日 | ~1KB/天 |
| `intervention-monitor.log` | 守藏吏检查日志 | 每小时 | ~500B/天 |
| `evolution-state.log` | 状态更新日志 | 每小时 | ~200B/天 |
| `degradation-check.log` | 退化检测日志 | 每小时 | ~200B/天 |
| `verify-stage4.log` | 阶段 4 验收日志 | 每日 | ~1KB/天 |
| `verify-stage3.log` | 阶段 3 验收日志 | 04-07 | ~5KB |

---

## ✅ 验收标准

### Cron 配置
- [x] 6 项 Cron 全部配置 ✅
- [x] 语法正确（crontab -l 验证）✅
- [x] 日志路径正确 ✅
- [ ] 执行成功（等待首次运行）🟡

### Skill 固化
- [x] 罔两高价值发现 ✅
- [x] 守藏吏干预监控 ✅
- [ ] 庖丁变现追踪 🟡
- [ ] 太一凌晨学习 🟡
- [ ] 守藏吏协作评分 🟡
- [ ] 太一意图准确 🟡

### Bot 自主执行
- [ ] 无需人工触发 🟡
- [ ] 自动上报结果 🟡
- [ ] 异常自动告警 🟡

---

## 🔗 相关文件

| 文件 | 职责 |
|------|------|
| `constitution/directives/AGI-EVOLUTION-GUARANTEE.md` | 保障机制宪法 |
| `constitution/directives/AGI-EVOLUTION-RESPONSIBILITY.md` | 责任分配表 |
| `constitution/directives/AGI-EVOLUTION-AUTOMATION.md` | 自动化程度分析 |
| `constitution/directives/AGI-EVOLUTION-TRIGGER.md` | 本文件（触发机制） |
| `skills/wangliang/high-value-discovery/SKILL.md` | 罔两 Skill |
| `skills/steward/intervention-monitor/SKILL.md` | 守藏吏 Skill |

---

*创建时间：2026-04-03 09:10 | 太一 AGI | 智能自动化触发机制*
