# 全域自进化系统定时自检自愈配置

> 版本：v1.0  
> 创建：2026-04-23 13:10  
> 指令：SAYELF - 定时自检自愈配置

---

## 🎯 自检频率配置

| 层级 | 频率 | 任务 |
|------|------|------|
| **L1: 任务级自检** | 每 5-10 分钟 | 各任务独立运行 |
| **L2: 系统级自检** | 每 2 小时 | 全域自进化系统检查 |
| **L3: 日报总结** | 每日 23:00 | 系统健康日报 |

---

## 📋 定时任务配置

### Crontab 配置

```bash
# 全域自进化系统定时自检 (每 2 小时)
*/120 * * * * /bin/bash /home/nicola/.openclaw/workspace/skills/07-system/self_evolving_system_cron.sh
```

### 任务级自检频率

| 任务 | 频率 | 文件 |
|------|------|------|
| **IP 监控** | 每 5 分钟 | `ip_self_evolving_cron.sh` |
| **交易监控** | 每 5 分钟 | `trade_self_evolving_cron.sh` |
| **X 爬虫** | 每小时 | `x_crawler_cron.sh` |
| **自动交易** | 每 10 分钟 | `auto_trade_self_evolving_cron.sh` |
| **系统自检** | 每 2 小时 | `self_evolving_system_cron.sh` |

---

## 🧬 系统自检内容

### 检查项目

1. **任务健康度**
   - 运行次数
   - 自愈成功率
   - 学习模式数

2. **进化指标**
   - total_runs (总运行次数)
   - issues_found (发现问题数)
   - auto_healed (自愈成功数)
   - success_rate (成功率)

3. **问题检测**
   - 任务未运行
   - 自愈成功率低 (<50%)
   - 进化停滞

### 健康度评估

| 健康度 | 状态 | 说明 |
|--------|------|------|
| **100-80%** | ✅ 健康 | 正常运行 |
| **79-50%** | ⚠️ 警告 | 需要关注 |
| **<50%** | ❌ 异常 | 需要干预 |

---

## 🔧 自愈流程

```
系统自检 (每 2 小时)
    ↓
发现问题 (健康度<80%)
    ↓
记录到 PITFALLS.md
    ↓
太一观察者通知
    ↓
人工干预 (如需要)
```

---

## 📊 健康报告

**文件位置**: `monitoring/self_evolution_health.json`

**内容**:
```json
{
  "timestamp": "2026-04-23T13:10:00",
  "overall_health": 95.0,
  "tasks": {...},
  "issues": [],
  "healthy_count": 4,
  "total_tasks": 4
}
```

---

## 🔍 查询命令

### 查看当前健康状态

```bash
cat /home/nicola/.openclaw/workspace/monitoring/self_evolution_health.json | python3 -m json.tool
```

### 手动触发系统自检

```bash
python3 /home/nicola/.openclaw/workspace/skills/07-system/self_evolving_system_check.py
```

### 查看自检日志

```bash
tail -100 /home/nicola/.openclaw/workspace/logs/self_evolving_system_check.log
```

### 查看定时任务

```bash
crontab -l | grep self_evolving
```

---

## 📈 进化指标趋势

**监控文件**: `monitoring/self_evolution_health.json`

**关键指标**:
- overall_health (总体健康度)
- healthy_count (健康任务数)
- success_rate (自愈成功率)

**目标**:
- overall_health ≥ 90%
- success_rate ≥ 80%
- 问题数持续下降

---

*太一 AGI · 全域自进化系统定时自检自愈*  
*版本：v1.0*  
*创建：2026-04-23 13:10*
