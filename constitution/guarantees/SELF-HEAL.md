# 自愈系统宪法

> 版本：v1.0 | 创建：2026-04-03 17:55 | 级别：宪法级 | 负责 Bot：守藏吏

---

## 🎯 核心原则

**自愈 > 告警 · 自动 > 手动 · 预防 > 修复**

系统应具备自我诊断、自我修复能力，最小化人工介入。

---

## 🔄 自愈流程

### 触发条件
| 条件 | 检测频率 | 响应时间 |
|------|---------|---------|
| Gateway 进程消失 | 5 分钟 | <60 秒 |
| Gateway HTTP 不可达 | 5 分钟 | <60 秒 |
| Cron 服务停止 | 5 分钟 | <30 秒 |
| 磁盘>90% | 5 分钟 | 自动清理 |
| 内存>85% | 5 分钟 | 告警 |

### 自愈层级

```
Level 1: 自动重启 (Gateway/Cron)
    ↓ 失败
Level 2: 清理资源 (临时文件/缓存)
    ↓ 失败
Level 3: 告警 + 人工介入
```

---

## 🛠️ 自愈脚本清单

| 脚本 | 职责 | 触发方式 |
|------|------|---------|
| `gateway-quick-restart.sh` | Gateway 快速重启 (15 秒) | 手动/自动 |
| `gateway-self-heal.sh` | Gateway 自愈 (最多 3 次尝试) | 自动 |
| `self-heal-monitor.sh` | 监控守护进程 (5 分钟周期) | 后台运行 |
| `self-check.sh` | 系统自检 (每小时) | Cron |

---

## ⚙️ 配置说明

### Gateway 自愈参数
```bash
MAX_RESTART_ATTEMPTS=3      # 最大重启尝试次数
RESTART_INTERVAL=5          # 尝试间隔 (秒)
HEALTH_CHECK_TIMEOUT=10     # 健康检查超时 (秒)
```

### 监控参数
```bash
MONITOR_INTERVAL=300        # 监控周期 (5 分钟)
DISK_THRESHOLD=90           # 磁盘告警阈值 (%)
MEM_THRESHOLD=85            # 内存告警阈值 (%)
```

---

## 📊 自愈记录

### 日志文件
| 日志 | 内容 | 保留周期 |
|------|------|---------|
| `logs/gateway-restart.log` | 重启记录 | 7 天 |
| `logs/gateway-self-heal.log` | 自愈记录 | 30 天 |
| `logs/self-heal-monitor.log` | 监控日志 | 7 天 |

### 记录格式
```
[耗时] 事件描述
示例：
[0s] ========== Gateway 自愈流程启动 ==========
[0s] 检测到 Gateway 异常，开始自愈...
[0s] 尝试第 1/3 次重启...
[15s] ✅ 自愈成功 (PID: 12345, 总耗时：15s, 尝试次数：1)
```

---

## 🚨 告警规则

### 立即通知 SAYELF
- [!] 自愈失败 >3 次/小时
- [!] Gateway 连续重启 >5 次
- [!] 磁盘>95% 且清理无效
- [!] 内存>90% 持续 10 分钟

### 通知方式
- 微信消息 (优先)
- Telegram 备用
- 邮件 (严重故障)

---

## 🔍 诊断命令

### 查看自愈历史
```bash
# 最近 10 次自愈记录
tail -n 20 /home/nicola/.openclaw/logs/gateway-self-heal.log

# 统计自愈成功率
grep "自愈成功" /home/nicola/.openclaw/logs/gateway-self-heal.log | wc -l
grep "自愈失败" /home/nicola/.openclaw/logs/gateway-self-heal.log | wc -l
```

### 手动触发自愈
```bash
# 立即执行自愈
/home/nicola/.openclaw/workspace/scripts/gateway-self-heal.sh

# 查看监控状态
ps aux | grep self-heal-monitor
```

### 测试自愈系统
```bash
# 模拟 Gateway 故障
pkill -9 openclaw-gateway

# 观察自愈日志
tail -f /home/nicola/.openclaw/logs/gateway-self-heal.log
```

---

## 📈 监控指标

### 核心指标
| 指标 | 目标 | 当前 |
|------|------|------|
| 自愈成功率 | >95% | 待统计 |
| 平均恢复时间 | <30 秒 | ~15 秒 |
| 误报率 | <1% | 待统计 |
| 人工介入频率 | <1 次/周 | 待统计 |

### 数据收集
```bash
# 每日统计 (添加到 Cron)
0 23 * * * echo "$(date '+%Y-%m-%d'), 成功: $(grep '自愈成功' logs/gateway-self-heal.log | wc -l), 失败: $(grep '自愈失败' logs/gateway-self-heal.log | wc -l)" >> logs/self-heal-stats.csv
```

---

## 🔄 持续优化

### v1.1 (计划)
- [ ] 集成通知系统
- [ ] 自愈成功率统计
- [ ] 根因分析报告

### v2.0 (计划)
- [ ] 预测性自愈 (基于日志模式)
- [ ] 多服务自愈 (扩展到其他 Bot)
- [ ] 自愈策略机器学习

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `constitution/guarantees/SELF-HEAL.md` | 本文档 |
| `constitution/guarantees/CRON-GUARANTEE.md` | Cron 保障 |
| `constitution/directives/TASK-GUARANTEE.md` | 任务保障 (六层防护) |
| `scripts/gateway-self-heal.sh` | Gateway 自愈脚本 |
| `scripts/self-heal-monitor.sh` | 监控守护进程 |
| `skills/self-check/SKILL.md` | 自检 Skill |

---

## 📜 修订历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-03 | 初始创建 (Gateway 自愈 + 监控) |

---

*创建：2026-04-03 17:55 | 太一 AGI · 守藏吏主责 · 自愈系统激活*
