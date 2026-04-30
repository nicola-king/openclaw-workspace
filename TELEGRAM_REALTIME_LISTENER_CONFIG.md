# Telegram 实时@监听服务配置

> 版本：v1.0  
> 创建：2026-04-23 13:20  
> 指令：SAYELF - 保证随时响应@

---

## 🎯 核心功能

### 1. 实时@监听
- **方式**: getUpdates 长轮询
- **超时**: 30 秒
- **响应**: 立即响应@消息

### 2. @触发随机对话
- **触发**: 检测到@后
- **延迟**: 30-90 秒后发起随机对话
- **间隔**: 最小 2 小时

### 3. Bot 自进化展现
- **7 个 Bot** 参与对话
- **程度**: 75-97
- **人设**: 深度思考者/积极讨论者/普通参与者

---

## 📡 服务配置

### systemd 服务

**文件**: `skills/07-system/telegram_realtime_listener.service`

```ini
[Unit]
Description=Telegram Realtime @ Listener - 太一 AGI
After=network.target

[Service]
Type=simple
User=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace
ExecStart=/usr/bin/python3 /home/nicola/.openclaw/workspace/skills/07-system/telegram_realtime_listener.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 启动命令

```bash
# 手动启动
bash skills/07-system/start_telegram_listener.sh

# 或后台运行
nohup python3 skills/07-system/telegram_realtime_listener.py >> logs/telegram_realtime_listener.log 2>&1 &

# 安装 systemd 服务
sudo cp skills/07-system/telegram_realtime_listener.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram_realtime_listener
sudo systemctl start telegram_realtime_listener
```

---

## 🔍 监听逻辑

```
启动监听服务
    ↓
getUpdates 长轮询 (30 秒)
    ↓
检测新消息
    ↓
是否@太一 AGI？
    ├─ 是 → 立即回复 + 发起随机对话
    └─ 否 → 继续监听
    ↓
循环
```

---

## 💬 对话流程

### @触发流程

```
用户@太一 AGI
    ↓
实时监听检测到
    ↓
立即回复 (@用户 + 话题问题)
    ↓
等待 30-90 秒
    ↓
发起随机对话 (同话题)
    ↓
等待 60-120 秒
    ↓
其他 Bot 参与讨论 (1-3 个)
    ↓
记录完整历史
```

### Bot 回复策略

| 程度 | 人设 | 回复风格 |
|------|------|---------|
| 90-100 | 深度思考者 | 哲学/多维度 |
| 80-89 | 积极讨论者 | 数据/观点 |
| 70-79 | 普通参与者 | 保守/不确定 |

---

## 📊 监控命令

### 查看服务状态

```bash
# 检查进程
ps aux | grep telegram_realtime

# 查看日志
tail -100 logs/telegram_realtime_listener.log

# 查看 PID
cat /tmp/telegram_listener.pid
```

### 查看对话历史

```bash
cat data/telegram_dialogue_history.json | python3 -m json.tool
```

### 查看监听状态

```bash
cat /tmp/telegram_offset.txt  # 当前 offset
cat /tmp/telegram_last_activity.json  # 最后活动
```

---

## 🔧 故障处理

### 服务停止

```bash
# 重启服务
pkill -f telegram_realtime_listener
bash skills/07-system/start_telegram_listener.sh
```

### Offset 问题

```bash
# 重置 offset
echo "0" > /tmp/telegram_offset.txt
```

### 日志分析

```bash
# 查看@消息数量
grep "检测到@消息" logs/telegram_realtime_listener.log | wc -l

# 查看回复数量
grep "已回复@" logs/telegram_realtime_listener.log | wc -l
```

---

## 📈 性能指标

**目标**:
- @响应时间：<1 分钟
- 对话发起率：100% (@后)
- Bot 参与度：1-3 个/对话
- 最小间隔：2 小时

**监控文件**:
- `/tmp/telegram_offset.txt` - 监听进度
- `/tmp/telegram_last_activity.json` - 活动记录
- `logs/telegram_realtime_listener.log` - 运行日志

---

## 🚀 扩展方向

### 短期
- [ ] systemd 服务安装
- [ ] 自动重启保护
- [ ] 日志轮转

### 中期
- [ ] 真实 Bot 接入
- [ ] 多群支持
- [ ] 对话质量评估

### 长期
- [ ] AI 深度对话
- [ ] 情感分析
- [ ] 个性化 Bot 人设

---

*太一 AGI · Telegram 实时@监听服务*  
*版本：v1.0*  
*创建：2026-04-23 13:20*
