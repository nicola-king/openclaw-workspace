# ⏰ 智慧调度器 - 定时推送配置

> **配置时间**: 2026-04-15 00:58  
> **时区**: 北京时间 (Asia/Shanghai)

---

## 📋 定时任务

### 道 Agent (🌿)
```
⏰ 时间：每日 08:00 (北京时间)
📍 内容：道之智慧
📖 来源：道德经、庄子等
📤 推送：Telegram 信息卡片
```

### 悟 Agent (🪷)
```
⏰ 时间：每日 20:00 (北京时间)
📍 内容：悟之智慧
📖 来源：心经、金刚经等
📤 推送：Telegram 信息卡片
```

---

## 🔧 Cron 配置

### Linux Cron

```bash
# 编辑 crontab
crontab -e

# 添加以下行

# 道 Agent - 每日 08:00 (北京时间)
0 8 * * * cd /home/nicola/.openclaw/workspace && python3 skills/05-content/wisdom-scheduler/src/scheduler.py --dao >> logs/wisdom-scheduler/dao-cron.log 2>&1

# 悟 Agent - 每日 20:00 (北京时间)
0 20 * * * cd /home/nicola/.openclaw/workspace && python3 skills/05-content/wisdom-scheduler/src/scheduler.py --wu >> logs/wisdom-scheduler/wu-cron.log 2>&1
```

### Systemd Timer (推荐)

**道 Agent Timer** (`~/.config/systemd/user/dao-agent.timer`):
```ini
[Unit]
Description=Dao Agent Daily Wisdom Timer

[Timer]
OnCalendar=*-*-* 08:00:00
Timezone=Asia/Shanghai
Persistent=true

[Install]
WantedBy=timers.target
```

**悟 Agent Timer** (`~/.config/systemd/user/wu-agent.timer`):
```ini
[Unit]
Description=Wu Agent Daily Wisdom Timer

[Timer]
OnCalendar=*-*-* 20:00:00
Timezone=Asia/Shanghai
Persistent=true

[Install]
WantedBy=timers.target
```

**Service 文件** (`~/.config/systemd/user/dao-agent.service`):
```ini
[Unit]
Description=Dao Agent Daily Wisdom Service

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/nicola/.openclaw/workspace/skills/05-content/dao-agent/src/dao_agent.py --daily
WorkingDirectory=/home/nicola/.openclaw/workspace
```

**启用 Timer**:
```bash
# 重新加载 systemd
systemctl --user daemon-reload

# 启用并启动 Timer
systemctl --user enable dao-agent.timer
systemctl --user start dao-agent.timer

systemctl --user enable wu-agent.timer
systemctl --user start wu-agent.timer

# 查看状态
systemctl --user list-timers
```

---

## 🚀 手动测试

```bash
# 立即发送道 Agent
python3 skills/05-content/wisdom-scheduler/src/scheduler.py --dao

# 立即发送悟 Agent
python3 skills/05-content/wisdom-scheduler/src/scheduler.py --wu

# 立即发送两者
python3 skills/05-content/wisdom-scheduler/src/scheduler.py --now

# 后台运行守护进程
nohup python3 skills/05-content/wisdom-scheduler/src/scheduler.py --daemon > logs/wisdom-scheduler/daemon.log 2>&1 &
```

---

## 📊 日志查看

```bash
# 查看道 Agent 日志
cat logs/wisdom-scheduler/dao-*.log

# 查看悟 Agent 日志
cat logs/wisdom-scheduler/wu-*.log

# 查看守护进程日志
tail -f logs/wisdom-scheduler/daemon.log
```

---

## ✅ 验证配置

```bash
# 测试道 Agent
python3 skills/05-content/dao-agent/src/dao_agent.py --daily

# 测试悟 Agent
python3 skills/05-content/wu-agent/src/wu_agent.py --daily

# 查看 Systemd Timer
systemctl --user list-timers | grep agent
```

---

*太一 AGI · 智慧调度器 · 2026-04-15*

**⏰ 北京时间每日 08:00 和 20:00 自动推送！**
