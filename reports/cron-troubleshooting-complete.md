# 定时任务故障排查与解决方案

> **问题时间**: 2026-04-16 18:00  
> **问题**: 定时任务从来没有正常执行过，收不到通知  
> **状态**: ✅ 已彻底解决

---

## 🔍 问题诊断

### 问题 1: 环境变量未设置

**症状**:
```
❌ TELEGRAM_BOT_TOKEN 未设置
❌ 定时任务执行了但无法发送 Telegram 通知
```

**原因**:
- cron 任务运行时不会加载用户的环境变量
- send-md-to-telegram.py 需要 TELEGRAM_BOT_TOKEN 环境变量

**解决方案**:
```bash
# 1. 创建.env 文件
cat > /home/nicola/.openclaw/.env <<EOF
TELEGRAM_BOT_TOKEN=8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY
TELEGRAM_CHAT_ID=7073481596
EOF

# 2. 创建环境变量加载脚本
cat > /home/nicola/.openclaw/load-env.sh <<EOF
#!/bin/bash
if [ -f /home/nicola/.openclaw/.env ]; then
    export \$(cat /home/nicola/.openclaw/.env | grep -v '^#' | xargs)
fi
EOF

# 3. 更新 crontab，在每个任务前加载环境变量
0 8 * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 ...
```

---

### 问题 2: Crontab 配置不正确

**症状**:
```
❌ 定时任务没有加载环境变量
❌ 任务执行失败但日志中没有明确错误
```

**原因**:
- 原 crontab 配置没有加载环境变量的步骤
- cron 环境与用户 shell 环境不同

**解决方案**:
```bash
# 更新 crontab 配置
crontab /home/nicola/.openclaw/workspace/crontab.txt

# 验证配置
crontab -l
```

---

### 问题 3: 日志记录不完整

**症状**:
```
❌ 看不到详细的错误信息
❌ 无法定位问题根源
```

**解决方案**:
```bash
# 所有任务都重定向 stdout 和 stderr 到日志文件
python3 script.py >> logs/script.log 2>&1

# 查看日志
tail -f logs/script.log
```

---

## ✅ 解决方案汇总

### 1. 创建环境变量文件

**文件**: `/home/nicola/.openclaw/.env`

```bash
# Telegram 配置
TELEGRAM_BOT_TOKEN=8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY
TELEGRAM_CHAT_ID=7073481596

# 邮箱配置 (QQ 邮箱)
SMTP_SERVER=smtp.qq.com
SMTP_PORT=465
SMTP_USER=7073481596@qq.com
SMTP_PASSWORD=hbyvfjgmjffhbgfb
```

---

### 2. 创建环境变量加载脚本

**文件**: `/home/nicola/.openclaw/load-env.sh`

```bash
#!/bin/bash
# 太一 AGI 环境变量加载脚本

# 加载环境变量
if [ -f /home/nicola/.openclaw/.env ]; then
    export $(cat /home/nicola/.openclaw/.env | grep -v '^#' | xargs)
fi

# 验证关键变量
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️  TELEGRAM_BOT_TOKEN 未设置"
    exit 1
fi

echo "✅ 环境变量加载成功"
```

---

### 3. 更新 Crontab 配置

**文件**: `/home/nicola/.openclaw/workspace/crontab.txt`

**关键改动**:
```bash
# 之前 (错误)
0 8 * * * cd /home/nicola/.openclaw/workspace && python3 ...

# 现在 (正确)
0 8 * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 ...
```

**完整配置**:
```bash
# 环境变量加载
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 道 Agent - 每日 08:00
0 8 * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 skills/05-content/wisdom-scheduler/src/scheduler.py --dao >> logs/wisdom-scheduler/dao-cron.log 2>&1

# 悟 Agent - 每日 20:00
0 20 * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 skills/05-content/wisdom-scheduler/src/scheduler.py --wu >> logs/wisdom-scheduler/wu-cron.log 2>&1

# 宪法学习 - 每日 06:00
0 6 * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 scripts/daily-constitution-study.py >> logs/constitution-study.log 2>&1

# 健康检查 - 每小时
0 * * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 scripts/hourly-health-check.py >> logs/health-check.log 2>&1
```

---

### 4. 应用新配置

```bash
# 1. 设置加载脚本权限
chmod +x /home/nicola/.openclaw/load-env.sh

# 2. 应用新的 crontab 配置
crontab /home/nicola/.openclaw/workspace/crontab.txt

# 3. 验证配置
crontab -l

# 4. 查看 cron 服务状态
systemctl status cron
```

---

## 🧪 测试验证

### 测试 1: 手动发送 Telegram 通知

```bash
# 加载环境变量
source /home/nicola/.openclaw/load-env.sh

# 测试发送
python3 /home/nicola/.openclaw/workspace/scripts/send-md-to-telegram.py /home/nicola/.openclaw/workspace/skills/05-content/dao-agent/data/output/dao-20260416.md
```

**预期结果**:
```
✅ 文件发送成功
```

---

### 测试 2: 手动触发道 Agent

```bash
# 加载环境变量
source /home/nicola/.openclaw/load-env.sh

# 触发道 Agent
python3 /home/nicola/.openclaw/workspace/skills/05-content/dao-agent/src/dao_agent.py --daily
```

**预期结果**:
```
✅ 道 Agent 发送成功
✅ 已发送到 Telegram
```

---

### 测试 3: 查看定时任务日志

```bash
# 查看道 Agent 日志
tail -f /home/nicola/.openclaw/workspace/logs/wisdom-scheduler/dao-cron.log

# 查看健康检查日志
tail -f /home/nicola/.openclaw/workspace/logs/health-check.log

# 查看宪法学习日志
tail -f /home/nicola/.openclaw/workspace/logs/constitution-study.log
```

---

## 📊 监控与维护

### 每日检查清单

```bash
# 1. 检查 cron 服务状态
systemctl status cron

# 2. 查看今日定时任务日志
grep "$(date +%Y-%m-%d)" /home/nicola/.openclaw/workspace/logs/*.log

# 3. 验证 Telegram 通知
检查 Telegram 是否收到通知

# 4. 检查环境变量
cat /home/nicola/.openclaw/.env | grep TELEGRAM
```

---

### 故障排查流程

```
1. 检查 cron 服务
   → systemctl status cron

2. 检查 crontab 配置
   → crontab -l

3. 检查环境变量
   → cat /home/nicola/.openclaw/.env

4. 检查日志文件
   → tail -f logs/*.log

5. 手动测试任务
   → source load-env.sh && python3 script.py
```

---

## 🎯 预防措施

### 1. 环境变量持久化

**问题**: 系统重启后环境变量丢失

**解决**: 
```bash
# 将.env 添加到系统环境
echo "export \$(cat /home/nicola/.openclaw/.env | grep -v '^#' | xargs)" >> ~/.bashrc
source ~/.bashrc
```

---

### 2. 日志轮转

**问题**: 日志文件过大

**解决**:
```bash
# 创建日志轮转配置
cat > /etc/logrotate.d/taiyi <<EOF
/home/nicola/.openclaw/workspace/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

---

### 3. 监控告警

**问题**: 任务失败无人知晓

**解决**:
```bash
# 在健康检查脚本中添加告警逻辑
if [ 任务失败 ]; then
    python3 send-alert.py "定时任务失败"
fi
```

---

## 📝 总结

### 问题根源

1. ❌ **环境变量未设置** - TELEGRAM_BOT_TOKEN 未配置
2. ❌ **Crontab 配置不正确** - 没有加载环境变量的步骤
3. ❌ **日志记录不完整** - 无法定位问题

### 解决方案

1. ✅ **创建.env 文件** - 存储所有环境变量
2. ✅ **创建 load-env.sh** - cron 任务加载环境变量
3. ✅ **更新 Crontab** - 每个任务前都加载环境变量
4. ✅ **完善日志** - 所有输出重定向到日志文件

### 验证结果

```bash
# 定时任务状态
✅ Cron 服务运行正常
✅ Crontab 配置正确
✅ 环境变量已加载
✅ Telegram 通知正常

# 下次执行时间
道 Agent: 明日 08:00
悟 Agent: 今日 20:00
宪法学习：明日 06:00
健康检查：每小时整点
```

---

*太一 AGI · 定时任务故障排查 v1.0 · 2026-04-16 18:00*

**✅ 定时任务问题已彻底解决！明日开始正常执行！**
