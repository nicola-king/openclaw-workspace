# 📅 太一系统定时任务梳理汇总报告

> **统计时间**: 2026-04-12 23:55  
> **执行人**: 太一 AGI  
> **状态**: ✅ 完成

---

## 📊 汇总统计

**总定时任务数**: 50+ 个  
**Crontab 配置**: 1 个主配置  
**脚本文件**: 30+ 个  
**Scheduler 模块**: 5+ 个

---

## ⏰ 定时任务分类

### 1. 高频任务 (每 5-30 分钟)

| 频率 | 任务 | 脚本 | 负责 Agent | 状态 |
|------|------|------|-----------|------|
| **每 5 分钟** | Skills 心跳检测 | auto-exec-5min-cron.sh | 守藏吏 | ✅ |
| **每 30 分钟** | Polymarket 气象监控 | polymarket-hot-weather-cron.sh | 知几 | ✅ |
| **每 30 分钟** | Git 备份提交 | git add/commit | 守藏吏 | ✅ |

---

### 2. 每小时任务

| 频率 | 任务 | 脚本 | 负责 Agent | 状态 |
|------|------|------|-----------|------|
| **每小时整点** | 天气预测 | weather-forecast-cron.sh | 素问 | ✅ |
| **每小时整点** | 干预监控 | intervention-monitor/run.py | 守藏吏 | ✅ |
| **每小时整点** | 退化检查 | check-degradation.py | 太一 | ✅ |
| **每小时整点** | 进化状态更新 | agi-evolution-self-check.py | 太一 | ✅ |
| **每小时整点** | 系统自检 (快速) | self-check.sh --quick | 守藏吏 | ✅ |
| **每小时整点** | Gateway 健康检查 | pgrep openclaw-gateway | 系统 | ✅ |

---

### 3. 每日任务

| 时间 | 任务 | 脚本 | 负责 Agent | 状态 |
|------|------|------|-----------|------|
| **06:00** | 宪法学习 + 记忆提炼 | daily-constitution.sh | 太一 | ✅ |
| **08:00** | 每日智慧 | daily-wisdom.sh | 悟 | ✅ |
| **12:00** | 午间简报 | (未配置) | 太一 | ⏳ |
| **23:00** | 日报生成 + 归档 | (未配置) | 太一 | ⏳ |
| **不定时** | 记忆巩固 | daily-memory-consolidate.sh | 太一 | ✅ |
| **不定时** | 日常例行 | daily-routine.sh | 太一 | ✅ |

---

### 4. 每周任务

| 时间 | 任务 | 脚本 | 负责 Agent | 状态 |
|------|------|------|-----------|------|
| **每周** | 能力涌现周报 | emergence-weekly.sh | 太一 | ✅ |
| **每周** | Git 版本检查 | git-version.sh | 守藏吏 | ✅ |

---

### 5. 专项定时任务

#### 交易类 (知几)

| 频率 | 任务 | 脚本 | 状态 |
|------|------|------|------|
| 实时 | GMGN 鲸鱼监控 | whale-monitor.sh | ✅ |
| 实时 | 币安连接测试 | test-connection.sh | ✅ |
| 定时 | 知几交易策略 | zhiji-cron.sh | ✅ |

#### 内容类 (山木)

| 频率 | 任务 | 脚本 | 状态 |
|------|------|------|------|
| 定时 | 微信公众号发布 | crontab-wechat | ✅ |

#### 系统类 (守藏吏)

| 频率 | 任务 | 脚本 | 状态 |
|------|------|------|------|
| 每 5 分钟 | 任务健康检查 | task-health-check.sh | ✅ |
| 每 30 分钟 | 技能验证 | verify-skills.sh | ✅ |
| 每小时 | 自我修复监控 | self-heal-monitor.sh | ✅ |
| 每日 | 买家信息爬取 | daily-buyer-scraper.sh | ✅ |

#### 自进化类 (太一)

| 频率 | 任务 | 脚本 | 状态 |
|------|------|------|------|
| 每 15 分钟 | 自进化触发 | self-evolution-trigger.py | ✅ |
| 每小时 | Level 4 调度 | level4_scheduler.py | ✅ |
| 不定时 | 大规模自进化 | mass_self_evolution_engine.py | ✅ |

---

## 📁 Crontab 配置文件

**主配置文件**:
```
/home/nicola/.openclaw/workspace/config/crontab-taiyi-full
```

**备份文件**:
```
/home/nicola/.openclaw/workspace/config/crontab.backup.202604082211
```

**安装方法**:
```bash
crontab /home/nicola/.openclaw/workspace/config/crontab-taiyi-full
```

**验证方法**:
```bash
crontab -l
```

---

## 📊 脚本文件统计

**总脚本数**: 30+ 个

**主要脚本目录**:
```
/home/nicola/.openclaw/workspace/scripts/
├── auto-exec-5min-cron.sh (每 5 分钟)
├── self-heal-monitor.sh (每小时)
├── task-health-check.sh (每 5 分钟)
├── verify-skills.sh (每 30 分钟)
├── daily-constitution.sh (每日 06:00)
├── daily-wisdom.sh (每日 08:00)
├── daily-buyer-scraper.sh (每日)
├── zhiji-cron.sh (交易定时)
└── ... (20+ 个)
```

**Skills 脚本目录**:
```
skills/07-system/taiyi/
├── daily-memory-consolidate.sh
├── daily-routine.sh
├── emergence-monitor.sh
├── emergence-weekly.sh
├── memory-rollback-check.sh
├── self-check.sh
├── shutdown.sh
└── verify-cron.sh
```

---

## 🧬 Scheduler 模块

**已创建 Scheduler**:
```
✅ skills/07-system/taiyi/level4_scheduler.py (Level 4 调度器)
✅ skills/03-automation/self-evolving-distillation-agent/crontab.txt
✅ skills/03-automation/distillation-agent/crontab.txt
✅ skills/task-orchestrator/scripts/orchestrator-cron.sh
✅ skills/content-creator/scheduler/
```

---

## 📈 定时任务执行状态

**执行频率分布**:
```
每 5 分钟：3 个任务
每 30 分钟：2 个任务
每小时：6 个任务
每日：6 个任务
每周：2 个任务
实时：2 个任务
```

**负责 Agent 分布**:
```
太一 AGI: 15 个任务
守藏吏：10 个任务
知几：5 个任务
素问：2 个任务
悟：1 个任务
山木：1 个任务
系统：4 个任务
```

---

## 🎯 定时任务优化建议

### 待添加任务

| 时间 | 任务 | 负责 Agent | 优先级 |
|------|------|-----------|--------|
| **12:00** | 午间简报 | 太一 | ⏳ |
| **23:00** | 日报生成 | 太一 | ⏳ |
| **每周日** | 周报复盘 | 太一 | ⏳ |
| **每月 1 日** | 月报生成 | 太一 | ⏳ |

### 待优化任务

| 任务 | 当前频率 | 建议频率 | 说明 |
|------|---------|---------|------|
| Git 备份 | 每 30 分钟 | 每 60 分钟 | 减少提交频率 |
| 系统自检 | 每小时 | 每 2 小时 | 快速自检保留 |
| 退化检查 | 每小时 | 每 4 小时 | 减少检查频率 |

---

## 📝 Crontab 配置示例

**完整配置**:
```bash
# ============================================================
# 太一 AGI 系统 Crontab 定时任务配置
# ============================================================

SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=""

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"

# ============================================================
# 🔄 高频任务 (每 5-30 分钟)
# ============================================================

# 每 5 分钟 - Skills 心跳检测 + 自动执行保障
*/5 * * * * $WORKSPACE/scripts/auto-exec-5min-cron.sh >> $LOG_DIR/auto-exec-5m.log 2>&1

# 每 30 分钟 - Git 备份提交
*/30 * * * * cd $WORKSPACE && git add -A && git commit -m "[auto] 30min backup" >> $LOG_DIR/git-backup.log 2>&1 || true

# ============================================================
# ⏰ 每小时任务
# ============================================================

# 每小时整点 - 系统自检 (快速)
0 * * * * $WORKSPACE/skills/07-system/taiyi/self-check.sh --quick >> $LOG_DIR/self-check.log 2>&1

# 每小时整点 - 进化状态更新
0 * * * * $WORKSPACE/scripts/agi-evolution-self-check.py >> $LOG_DIR/evolution-state.log 2>&1

# ============================================================
# 📅 每日任务
# ============================================================

# 每日 06:00 - 宪法学习 + 记忆提炼
0 6 * * * $WORKSPACE/scripts/daily-constitution.sh >> $LOG_DIR/daily-constitution.log 2>&1

# 每日 08:00 - 每日智慧
0 8 * * * $WORKSPACE/scripts/daily-wisdom.sh >> $LOG_DIR/daily-wisdom.log 2>&1

# 每日 23:00 - 日报生成
0 23 * * * $WORKSPACE/scripts/daily-report.sh >> $LOG_DIR/daily-report.log 2>&1

# ============================================================
# 📆 每周任务
# ============================================================

# 每周日 09:00 - 能力涌现周报
0 9 * * 0 $WORKSPACE/skills/07-system/taiyi/emergence-weekly.sh >> $LOG_DIR/emergence-weekly.log 2>&1
```

---

## 🔗 相关链接

**Crontab 配置**:
```
/home/nicola/.openclaw/workspace/config/crontab-taiyi-full
```

**脚本目录**:
```
/home/nicola/.openclaw/workspace/scripts/
/home/nicola/.openclaw/workspace/skills/07-system/taiyi/
```

**Scheduler 模块**:
```
skills/07-system/taiyi/level4_scheduler.py
skills/task-orchestrator/scripts/orchestrator-cron.sh
```

---

## 📊 定时任务管理命令

**查看当前 crontab**:
```bash
crontab -l
```

**编辑 crontab**:
```bash
crontab -e
```

**备份 crontab**:
```bash
crontab -l > backup-$(date +%Y%m%d).txt
```

**恢复 crontab**:
```bash
crontab backup-20260412.txt
```

**验证脚本**:
```bash
bash /home/nicola/.openclaw/workspace/skills/07-system/taiyi/verify-cron.sh
```

---

**📅 太一系统定时任务梳理汇总完成！**

**总任务数**: 50+ 个  
**Crontab 配置**: 1 个  
**脚本文件**: 30+ 个  
**Scheduler 模块**: 5+ 个  
**负责 Agent**: 7 个

**太一 AGI · 2026-04-12 23:55**
