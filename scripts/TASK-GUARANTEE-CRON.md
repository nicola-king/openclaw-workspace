# 定时任务验证及自检机制 - Cron 配置

> 配置时间：2026-04-05 00:56 | 状态：✅ 已激活

---

## 📋 Cron 任务列表

### 1. 健康检查（每小时）
```cron
0 * * * * /home/nicola/.openclaw/workspace/scripts/task-health-check.sh >> /home/nicola/.openclaw/workspace/logs/task-health-cron.log 2>&1
```

**职责：**
- 检查所有任务状态
- 发现异常立即告警
- 生成健康状态文件

---

### 2. 自愈恢复（每 30 分钟）
```cron
*/30 * * * * /home/nicola/.openclaw/workspace/scripts/task-self-heal.sh >> /home/nicola/.openclaw/workspace/logs/task-self-heal-cron.log 2>&1
```

**职责：**
- 检测故障任务
- 自动执行修复动作
- 记录修复日志

---

### 3. 每日验证（06:00）
```cron
0 6 * * * /home/nicola/.openclaw/workspace/scripts/task-verify.sh >> /home/nicola/.openclaw/workspace/logs/task-verify-cron.log 2>&1
```

**职责：**
- 检查昨日所有任务执行
- 生成每日验证报告
- 汇总告警统计

---

### 4. 告警检查（每 5 分钟）
```cron
*/5 * * * * /home/nicola/.openclaw/workspace/scripts/task-alert.sh >> /home/nicola/.openclaw/workspace/logs/task-alert-cron.log 2>&1
```

**职责：**
- 检查待发送告警
- 统一发送通知
- 清理已发送告警

---

## 🔧 配置方法

### 方式 1：直接添加到 crontab
```bash
crontab -e
# 添加上述配置
```

### 方式 2：使用配置文件
```bash
cat >> ~/.openclaw/cron/task-guarantee << 'EOF'
# 定时任务保障机制
0 * * * * /home/nicola/.openclaw/workspace/scripts/task-health-check.sh >> /home/nicola/.openclaw/workspace/logs/task-health-cron.log 2>&1
*/30 * * * * /home/nicola/.openclaw/workspace/scripts/task-self-heal.sh >> /home/nicola/.openclaw/workspace/logs/task-self-heal-cron.log 2>&1
0 6 * * * /home/nicola/.openclaw/workspace/scripts/task-verify.sh >> /home/nicola/.openclaw/workspace/logs/task-verify-cron.log 2>&1
*/5 * * * * /home/nicola/.openclaw/workspace/scripts/task-alert.sh >> /home/nicola/.openclaw/workspace/logs/task-alert-cron.log 2>&1
EOF

# 合并到系统 crontab
cat ~/.openclaw/cron/task-guarantee | crontab -
```

---

## 📊 输出文件

| 文件 | 说明 | 频率 |
|------|------|------|
| `logs/task-health-YYYYMMDD.log` | 健康检查日志 | 每日 |
| `logs/task-self-heal-YYYYMMDD.log` | 自愈修复日志 | 每日 |
| `logs/task-verify-YYYYMMDD.log` | 验证报告日志 | 每日 |
| `logs/task-alert-YYYYMMDD.log` | 告警通知日志 | 每日 |
| `reports/task-daily-report-YYYYMMDD.md` | 每日验证报告 | 每日 |
| `/tmp/task-health-status.json` | 实时健康状态 | 每小时 |
| `/tmp/task-alerts-pending.jsonl` | 待发送告警队列 | 实时 |

---

## ✅ 验证方法

### 立即测试
```bash
# 1. 运行健康检查
./scripts/task-health-check.sh

# 2. 查看状态
cat /tmp/task-health-status.json

# 3. 运行自愈
./scripts/task-self-heal.sh

# 4. 生成报告
./scripts/task-verify.sh
```

### 检查 Cron 状态
```bash
# 查看已配置的 Cron
crontab -l

# 查看 Cron 日志
tail -20 /var/log/syslog | grep CRON
```

---

## 🎯 预期效果

### 正常运行时
```
✅ 每小时：健康检查通过
✅ 每 30 分钟：自愈检查无任务
✅ 每日 06:00: 生成日报（健康率≥95%）
✅ 每 5 分钟：告警检查无待发送
```

### 故障时
```
⚠️ 07:05 健康检查发现故障
⚠️ 07:05 生成告警（P1 严重）
⚠️ 07:30 自愈脚本执行修复
✅ 07:35 验证修复成功
✅ 08:00 健康检查通过
```

---

## 📈 监控指标

| 指标 | 监控方式 | 告警阈值 |
|------|---------|---------|
| 任务启用率 | 健康检查 | <90% |
| 执行成功率 | 每日验证 | <80% |
| 自愈成功率 | 自愈日志 | <95% |
| 告警响应时间 | 告警日志 | >15 分钟 |
| 健康检查间隔 | Cron 监控 | >2 小时 |

---

## 🔗 相关文件

- `constitution/directives/TASK-GUARANTEE-v2.md` - 保障法则
- `scripts/task-health-check.sh` - 健康检查
- `scripts/task-self-heal.sh` - 自愈恢复
- `scripts/task-verify.sh` - 每日验证
- `scripts/task-alert.sh` - 告警通知

---

*配置时间：2026-04-05 00:56 | 太一 AGI*
