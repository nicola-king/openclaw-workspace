# ⚙️ systemd 自进化调度配置

> **配置时间**: 2026-04-16 23:51  
> **状态**: ✅ 已启用  
> **模式**: systemd timer 自进化调度

---

## 🎯 已配置的 Timer

| Timer | 频率 | 下次执行 | 状态 |
|-------|------|----------|------|
| **taiyi-scheduler.timer** | 每 5 分钟 | 23:55:41 | ✅ active |
| **taiyi-scheduler-monitor.timer** | 每 5 分钟 | 23:55:53 | ✅ active |
| **taiyi-health-check.timer** | 每小时整点 | 00:00:11 | ✅ active |
| **taiyi-constitution-study.timer** | 每日 06:00 | 明天 06:00 | ✅ active |
| **taiyi-daily-report.timer** | 每日 23:00 | 明天 23:00 | ✅ active |

---

## 📋 Timer 配置详情

### 1. Scheduler Agent Timer

**文件**: `/etc/systemd/system/taiyi-scheduler.timer`

**触发频率**: 每 5 分钟

**配置**:
```ini
[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
RandomizedDelaySec=30
Persistent=true
```

**触发服务**: `taiyi-scheduler.service`

**任务**:
- PDCA 循环
- 自进化引擎
- 技能标准化

---

### 2. Scheduler Monitor Timer

**文件**: `/etc/systemd/system/taiyi-scheduler-monitor.timer`

**触发频率**: 每 5 分钟

**配置**:
```ini
[Timer]
OnBootSec=2min
OnUnitActiveSec=5min
RandomizedDelaySec=30
Persistent=true
```

**触发服务**: `taiyi-scheduler-monitor.service`

**任务**: Scheduler Agent 健康检查

---

### 3. Health Check Timer

**文件**: `/etc/systemd/system/taiyi-health-check.timer`

**触发频率**: 每小时整点

**配置**:
```ini
[Timer]
OnCalendar=*:00:00
RandomizedDelaySec=30
Persistent=true
```

**触发服务**: `taiyi-health-check.service`

**任务**: 系统健康检查 (Gateway/Scheduler/通道)

---

### 4. Constitution Study Timer

**文件**: `/etc/systemd/system/taiyi-constitution-study.timer`

**触发频率**: 每日 06:00

**配置**:
```ini
[Timer]
OnCalendar=*-*-* 06:00:00
RandomizedDelaySec=60
Persistent=true
```

**触发服务**: `taiyi-constitution-study.service`

**任务**: 宪法学习 + Telegram 推送

---

### 5. Daily Report Timer

**文件**: `/etc/systemd/system/taiyi-daily-report.timer`

**触发频率**: 每日 23:00

**配置**:
```ini
[Timer]
OnCalendar=*-*-* 23:00:00
RandomizedDelaySec=60
Persistent=true
```

**触发服务**: `taiyi-daily-report.service`

**任务**: 日报生成 + Telegram 推送

---

## 🔧 Service 配置

### 通用配置

所有服务使用以下通用配置:

```ini
[Service]
Type=oneshot
User=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace
EnvironmentFile=/home/nicola/.openclaw/.env
RemainAfterExit=no

Restart=on-failure
RestartSec=60

MemoryMax=256M
CPUQuota=25%

StandardOutput=journal
StandardError=journal
```

---

## 📊 执行时间线

### 每 5 分钟

| 时间 | 任务 |
|------|------|
| **:00, :05, :10, ...** | Scheduler Agent + Monitor |

---

### 每小时

| 时间 | 任务 |
|------|------|
| **整点** | 健康检查 + Telegram 推送 |

---

### 每日

| 时间 | 任务 |
|------|------|
| **06:00** | 宪法学习 + Telegram 推送 |
| **23:00** | 日报生成 + Telegram 推送 |

---

## 🎯 systemd vs Crontab

### systemd Timer 优势

```
✅ 集中管理 - 所有任务在 systemd 统一管理
✅ 状态可见 - systemctl list-timers 查看状态
✅ 日志集成 - journalctl 统一日志
✅ 持久化 - 系统重启后自动恢复错过的任务
✅ 资源限制 - MemoryMax/CPUQuota 精确控制
✅ 依赖管理 - After=network.target 等
✅ 自进化 - 无需手动 crontab 编辑
```

---

### Crontab 状态

```
⚠️ Crontab 配置保留作为备用
✅ systemd Timer 为主要调度机制
✅ 两者可共存，systemd 优先
```

---

## 🔍 管理命令

### 查看 Timer 状态

```bash
# 查看所有活跃 timer
systemctl list-timers | grep taiyi

# 查看所有 timer (包括未激活)
systemctl list-timers --all | grep taiyi
```

---

### 查看 Timer 详情

```bash
# 查看特定 timer 状态
systemctl status taiyi-scheduler.timer

# 查看 timer 日志
journalctl -u taiyi-scheduler.timer

# 查看服务日志
journalctl -u taiyi-scheduler.service
```

---

### 控制 Timer

```bash
# 启动 timer
sudo systemctl start taiyi-scheduler.timer

# 停止 timer
sudo systemctl stop taiyi-scheduler.timer

# 启用 timer (开机自启)
sudo systemctl enable taiyi-scheduler.timer

# 禁用 timer
sudo systemctl disable taiyi-scheduler.timer

# 重启 timer
sudo systemctl restart taiyi-scheduler.timer
```

---

### 立即触发任务

```bash
# 立即执行服务 (不等待 timer)
sudo systemctl start taiyi-scheduler.service
```

---

## 📁 文件清单

### Timer 文件

| 文件 | 用途 |
|------|------|
| `/etc/systemd/system/taiyi-scheduler.timer` | 每 5 分钟调度 |
| `/etc/systemd/system/taiyi-scheduler-monitor.timer` | 每 5 分钟监控 |
| `/etc/systemd/system/taiyi-health-check.timer` | 每小时健康检查 |
| `/etc/systemd/system/taiyi-constitution-study.timer` | 每日 06:00 学习 |
| `/etc/systemd/system/taiyi-daily-report.timer` | 每日 23:00 日报 |

---

### Service 文件

| 文件 | 用途 |
|------|------|
| `/etc/systemd/system/taiyi-scheduler.service` | Scheduler Agent |
| `/etc/systemd/system/taiyi-scheduler-monitor.service` | Scheduler Monitor |
| `/etc/systemd/system/taiyi-health-check.service` | 健康检查 |
| `/etc/systemd/system/taiyi-constitution-study.service` | 宪法学习 |
| `/etc/systemd/system/taiyi-daily-report.service` | 日报生成 |

---

## 🎊 总结

### 配置状态

```
✅ 5 个 Timer 已配置并启用
✅ 5 个 Service 已配置并启用
✅ 所有 Timer 状态：active (waiting)
✅ 下次执行时间已确认
✅ systemd 自进化调度已激活
✅ 无需手动 crontab 执行
```

---

### 下次执行时间

| 任务 | 下次执行 |
|------|----------|
| Scheduler Agent | 23:55:41 (4 分钟后) |
| Scheduler Monitor | 23:55:53 (4 分钟后) |
| 健康检查 | 00:00:11 (8 分钟后) |
| 宪法学习 | 明天 06:00:33 |
| 日报生成 | 明天 23:00:59 |

---

### 自进化特性

```
✅ 持久化 - 系统重启后自动恢复
✅ 自动重试 - 失败后 60 秒重试
✅ 资源限制 - 防止资源耗尽
✅ 日志集成 - journalctl 统一查询
✅ Telegram 推送 - 关键任务自动通知
```

---

*太一 AGI · systemd 自进化调度 v1.0 · 2026-04-16 23:51*

**⚙️ systemd 自进化调度已激活！无需手动执行！**
