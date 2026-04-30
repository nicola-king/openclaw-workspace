# IP 监控指南 - 避免 IP 飘浮

> **创建时间**: 2026-04-22 21:30  
> **功能**: 定期监控 IP 变化，发送告警

---

## 📋 IP 监控脚本功能

### 核心功能

| 功能 | 说明 |
|------|------|
| **定期检查** | 每 5 分钟检查出口 IP |
| **IP 变化告警** | IP 变化时发送 Telegram 告警 |
| **固定性测试** | 每次变化测试 5 次确保稳定 |
| **历史记录** | 记录所有 IP 变化历史 |
| **告警限制** | 连续 3 次变化才发送告警 |

---

## 🔧 使用方法

### 1. 手动检查 IP

```bash
# 检查当前 IP
bash /home/nicola/.openclaw/workspace/skills/01-trading/zhiji/ip_monitor.sh check

# 或简写
bash ip_monitor.sh
```

### 2. 测试节点 IP

```bash
# 测试指定节点 IP
bash ip_monitor.sh test '🇯🇵 日本 W01 | IEPL'

# 测试其他节点
bash ip_monitor.sh test '🇯🇵 日本 W02 | IEPL'
bash ip_monitor.sh test '🇯🇵 日本 W03 | IEPL'
bash ip_monitor.sh test '🇸🇬 新加坡 W01 | IEPL'
```

### 3. 查看状态

```bash
# 查看当前状态
bash ip_monitor.sh status
```

### 4. 查看历史记录

```bash
# 查看 IP 变化历史
bash ip_monitor.sh history
```

### 5. 查看帮助

```bash
# 查看帮助
bash ip_monitor.sh help
```

---

## ⏰ 自动监控配置

### 添加到 Crontab

```bash
# 编辑 crontab
crontab -e

# 添加以下行 (每 5 分钟检查一次)
*/5 * * * * /bin/bash /home/nicola/.openclaw/workspace/skills/01-trading/zhiji/ip_monitor.sh check >> /home/nicola/.openclaw/workspace/logs/ip_monitor_cron.log 2>&1
```

### 验证配置

```bash
# 查看 crontab
crontab -l

# 应该看到:
*/5 * * * * /bin/bash /home/nicola/.openclaw/workspace/skills/01-trading/zhiji/ip_monitor.sh check >> /home/nicola/.openclaw/workspace/logs/ip_monitor_cron.log 2>&1
```

---

## 📊 日志文件

### 主日志

```
位置：/home/nicola/.openclaw/workspace/logs/ip_monitor.log

内容:
[2026-04-22 21:30:00] 🔍 开始 IP 检查
[2026-04-22 21:30:00] 📊 当前出口 IP: 141.11.146.70
[2026-04-22 21:30:00] 📊 上次出口 IP: 141.11.146.70
[2026-04-22 21:30:00] ✅ IP 未变化
```

### 历史记录

```
位置：/home/nicola/.openclaw/workspace/logs/ip_monitor.log.history

内容:
2026-04-22 21:30:00,141.11.146.68,141.11.146.70
2026-04-22 21:35:00,141.11.146.70,141.11.146.70
```

### 状态文件

```
位置：/tmp/last_export_ip.txt
内容：141.11.146.70

位置：/tmp/ip_alert_count.txt
内容：0 (告警计数)
```

---

## 📱 Telegram 告警

### 告警触发条件

```
条件 1: IP 发生变化
条件 2: 连续 3 次检测到变化
条件 3: IP 测试不稳定
```

### 告警内容

```
⚠️ IP 变化告警

IP 已更新

上次 IP: 141.11.146.68
新 IP: 141.11.146.70
状态：✅ 已稳定

请在币安更新 IP 白名单
```

### 严重告警

```
⚠️ IP 变化告警

IP 持续飘浮

上次 IP: 141.11.146.68
当前 IP: 141.11.146.70
状态：不稳定

建议:
1. 检查 Clash 节点配置
2. 锁定固定节点
3. 联系代理提供商
```

---

## 🎯 使用场景

### 场景 1: 日常监控

```bash
# 添加到 crontab，自动监控
*/5 * * * * bash ip_monitor.sh check
```

### 场景 2: 测试新节点

```bash
# 1. 在 Clash 管理器选择节点
# 2. 测试 IP
bash ip_monitor.sh test '🇯🇵 日本 W01 | IEPL'

# 3. 记录 IP 地址
# 4. 在币安添加白名单
```

### 场景 3: 排查问题

```bash
# 1. 查看当前状态
bash ip_monitor.sh status

# 2. 查看历史记录
bash ip_monitor.sh history

# 3. 查看日志
tail -f /home/nicola/.openclaw/workspace/logs/ip_monitor.log
```

---

## ✅ 配置步骤

### 步骤 1: 测试脚本

```bash
# 测试脚本是否正常工作
bash ip_monitor.sh check
```

### 步骤 2: 添加到 Crontab

```bash
# 编辑 crontab
crontab -e

# 添加自动监控
*/5 * * * * bash /home/nicola/.openclaw/workspace/skills/01-trading/zhiji/ip_monitor.sh check
```

### 步骤 3: 验证配置

```bash
# 等待 5 分钟
# 查看日志
tail /home/nicola/.openclaw/workspace/logs/ip_monitor.log
```

---

## 📋 完整命令列表

| 命令 | 说明 |
|------|------|
| `bash ip_monitor.sh check` | 检查 IP (默认) |
| `bash ip_monitor.sh test 'NODE'` | 测试指定节点 |
| `bash ip_monitor.sh status` | 显示状态 |
| `bash ip_monitor.sh history` | 显示历史 |
| `bash ip_monitor.sh help` | 显示帮助 |

---

## 🔍 故障排查

### 问题 1: 脚本无法执行

```bash
# 检查权限
chmod +x /home/nicola/.openclaw/workspace/skills/01-trading/zhiji/ip_monitor.sh

# 重新运行
bash ip_monitor.sh check
```

### 问题 2: 无法获取 IP

```bash
# 检查代理是否正常
curl -x http://127.0.0.1:7890 https://api.ipify.org

# 如果失败，检查 Clash 服务
ps aux | grep clash
```

### 问题 3: Telegram 告警未发送

```bash
# 检查 Bot Token 和 Chat ID
# 在脚本中确认配置正确
TELEGRAM_BOT_TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID="7073481596"
```

---

*IP 监控指南*  
*创建时间：2026-04-22 21:30*  
*功能：定期监控 IP 变化，避免 IP 飘浮*  
*状态：✅ 已创建*
