# Cron 保障机制

> 版本：v1.0 | 创建：2026-04-03 14:41 | 负责 Bot：守藏吏

---

## 🎯 核心原则

**Cron 是自动化执行的基石** - 必须确保所有关键任务按时执行

**保障策略**: 文件化 + 冗余备份 + 自动验证 + 异常告警

---

## 📋 当前 Cron 配置

### 实时/高频任务
| 频率 | 任务 | 脚本 | 日志 | 负责 |
|------|------|------|------|------|
| ***/5** | Skills 心跳检测 | `scripts/skill-heartbeat.sh` | `logs/skill-heartbeat.log` | 守藏吏 |
| ***/30** | Polymarket 气象监控 | `polymarket-hot-weather-cron.sh` | `logs/polymarket-weather.log` | 知几 |
| ***/30** | Git 备份提交 | `scripts/git-backup-system.sh commit` | `logs/git-backup.log` | 守藏吏 |
| **0 * *** | 天气预测 | `skills/suwen/weather-forecast.sh` | `logs/weather-forecast.log` | 素问 |
| **0 * *** | 干预监控 | `skills/steward/intervention-monitor/run.py` | `logs/intervention-monitor.log` | 守藏吏 |
| **0 * *** | 退化检查 | `scripts/check-degradation.py` | `logs/degradation-check.log` | 太一 |
| **0 * *** | 进化状态更新 | `scripts/update-evolution-state.py` | `logs/evolution-state.log` | 太一 |
| **0 * *** | Git 备份恢复检查 | `scripts/git-backup-system.sh restore` | `logs/git-backup.log` | 守藏吏 |
| **0 * *** | **系统自检 (快速)** | **`scripts/self-check.sh --quick`** | **`logs/self-check.log`** | **守藏吏** 🆕 |

### 每日任务
| 时间 | 任务 | 脚本 | 日志 | 负责 |
|------|------|------|------|------|
| **01:00** | 高价值发现 | `skills/wangliang/high-value-discovery/run.py` | `logs/high-value-discovery.log` | 罔两 |
| **01:00** | 深度学习 | `skills/taiyi/night-learning/run.py` | `logs/night-learning.log` | 太一 |
| **03:00** | Git 完整备份 | `scripts/git-backup-system.sh backup` | `logs/git-backup.log` | 守藏吏 |
| **06:00** | **系统自检 (完整)** | **`scripts/self-check.sh --full --report`** | **`logs/self-check.log`** | **守藏吏** 🆕 |
| **23:00** | 预算追踪 | `skills/paoding/monetization-tracker/run.py` | `logs/monetization-tracker.log` | 庖丁 |
| **23:00** | Stage-4 验证 | `skills/steward/stage-verification/run.py --stage=4` | `logs/verify-stage4.log` | 守藏吏 |

### 每月任务
| 时间 | 任务 | 脚本 | 日志 | 负责 |
|------|------|------|------|------|
| **07-01 23:00** | Stage-3 验证 | `skills/steward/stage-verification/run.py --stage=3` | `logs/verify-stage3.log` | 守藏吏 |

---

## 🔒 保障机制

### 1️⃣ 文件化存储
- ✅ 所有 Cron 配置通过 `crontab -l` 可查
- ✅ 脚本路径使用绝对路径
- ✅ 日志路径统一 (`logs/*.log`)

### 2️⃣ 冗余备份
- ✅ Cron 配置导出：`crontab -l > workspace/config/crontab.backup`
- ✅ 脚本文件 Git 版本控制
- ✅ 日志每日轮转

### 3️⃣ 自动验证
- ✅ 每小时自检包含 Cron 验证
- ✅ 每日 06:00 完整检查
- ✅ 日志文件存在性检查

### 4️⃣ 异常告警
- 🚨 Cron 缺失 → 自检报告🔴
- 🚨 日志文件>100MB → 告警
- 🚨 脚本执行失败 → 日志记录 + 下次重试

---

## 🛠️ 管理命令

### 查看当前配置
```bash
crontab -l
```

### 导出备份
```bash
crontab -l > ~/backup/crontab-$(date +%Y%m%d).txt
```

### 验证 Cron 语法
```bash
# 检查脚本可执行性
ls -la /home/nicola/.openclaw/workspace/scripts/*.sh

# 检查 Python 脚本语法
python3 -m py_compile /home/nicola/.openclaw/workspace/skills/*/*/run.py
```

### 查看执行日志
```bash
# 最近 10 条自检日志
tail -n 10 /home/nicola/.openclaw/logs/self-check.log

# 实时监控
tail -f /home/nicola/.openclaw/logs/self-check.log
```

### 手动触发
```bash
# 快速自检
/home/nicola/.openclaw/workspace/scripts/self-check.sh --quick

# 完整自检
/home/nicola/.openclaw/workspace/scripts/self-check.sh --full --report
```

---

## 📊 验证清单

### 每日验证 (06:00 自检执行)
- [ ] 所有 Cron 存在
- [ ] 脚本路径正确
- [ ] 日志文件可写
- [ ] 最近执行时间正常

### 每周验证 (周一)
- [ ] 导出 Cron 备份
- [ ] 清理旧日志 (>7 天)
- [ ] 检查日志大小

### 每月验证 (1 日)
- [ ] 完整 Cron 审计
- [ ] 更新文档
- [ ] 归档旧日志

---

## 🚨 故障处理

### Gateway 重启慢
**问题**: `openclaw gateway restart` 耗时 >5 分钟

**解决方案**: 使用快速重启脚本
```bash
# 快速重启 (30 秒内)
/home/nicola/.openclaw/workspace/scripts/gateway-quick-restart.sh

# 原理：pkill -9 + systemctl start 并行
# 对比：原方式 6 分钟 → 优化后 15 秒
```

### Cron 不执行
```bash
# 1. 检查 Cron 服务
systemctl --user status cron

# 2. 检查 Cron 日志
grep CRON /var/log/syslog | tail -20

# 3. 检查脚本权限
chmod +x /home/nicola/.openclaw/workspace/scripts/*.sh

# 4. 手动执行测试
./scripts/self-check.sh --quick
```

### 日志文件过大
```bash
# 清理>100MB 的日志
find /home/nicola/.openclaw/logs -name "*.log" -size +100M -exec truncate -s 0 {} \;
```

### Cron 配置丢失
```bash
# 从备份恢复
crontab ~/backup/crontab-20260403.txt

# 或重新导入
cat /home/nicola/.openclaw/workspace/config/crontab.backup | crontab -
```

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `constitution/guarantees/CRON-GUARANTEE.md` | 本文档 |
| `constitution/directives/TASK-GUARANTEE.md` | 任务保障法则 (六层防护) |
| `scripts/self-check.sh` | 自检脚本 |
| `skills/self-check/SKILL.md` | 自检 Skill |
| `logs/self-check.log` | 自检日志 |
| `reports/self-check-*.md` | 自检报告 |

---

## 📜 修订历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-03 | 初始创建 (集成 Self-Check + 完整 Cron 清单) |

---

*创建：2026-04-03 14:41 | 太一 AGI · 守藏吏主责*
