# 📱 定时任务 Telegram 推送配置

> **配置时间**: 2026-04-16 23:47  
> **状态**: ✅ 已启用

---

## 🎯 已配置 Telegram 推送的任务

| 任务 | 频率 | 发送内容 | 状态 |
|------|------|----------|------|
| **日报生成** | 每日 23:00 | 日报 MD 文件 | ✅ 已配置 |
| **宪法学习** | 每日 06:00 | 学习摘要 | ✅ 已配置 |
| **健康检查** | 每小时 (整点) | 系统健康报告 | ✅ 已配置 |

---

## 📋 推送详情

### 1. 日报生成 (23:00)

**脚本**: `scripts/daily-report-generator.py`

**发送内容**:
- 📎 日报 MD 文件附件
- 📝 说明文字：日期 + 生成时间

**示例**:
```
📊 *日报 · 2026-04-16*

太一 AGI 每日工作报告
生成时间：23:00:01
```

---

### 2. 宪法学习 (06:00)

**脚本**: `scripts/daily-constitution-study.py`

**发送内容**:
- 📖 学习摘要消息
- 📝 已学习的宪法文件列表

**示例**:
```
📖 *宪法学习 · 2026-04-16*

已学习:
• CONST-ROUTER.md
• VALUE-FOUNDATION.md
• NEGENTROPY.md

太一 AGI 每日学习报告
```

---

### 3. 健康检查 (每小时整点)

**脚本**: `scripts/hourly-health-check.py`

**发送内容**:
- 🏥 系统健康报告
- 📝 Gateway/Scheduler/通道状态

**示例**:
```
🏥 *系统健康检查 · 2026-04-16 23:00*

Gateway: ✅ 正常
Scheduler: ✅ 正常
Telegram: ✅
微信：✅

太一 AGI 系统监控
```

---

## 🔧 Telegram 配置

### 环境变量

```bash
TELEGRAM_BOT_TOKEN=8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY
TELEGRAM_CHAT_ID=7073481596
```

---

### 配置文件

| 文件 | 用途 |
|------|------|
| `scripts/send-md-to-telegram.py` | 通用 MD 文件发送工具 |
| `scripts/daily-report-generator.py` | 日报生成 + Telegram |
| `scripts/daily-constitution-study.py` | 宪法学习 + Telegram |
| `scripts/hourly-health-check.py` | 健康检查 + Telegram |

---

## 🕐 Crontab 配置

```bash
# 日报生成 + Telegram - 每日 23:00
0 23 * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 scripts/daily-report-generator.py >> logs/daily-report.log 2>&1

# 宪法学习 + Telegram - 每日 06:00
0 6 * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 scripts/daily-constitution-study.py >> logs/constitution-study.log 2>&1

# 健康检查 + Telegram - 每小时整点
0 * * * * . /home/nicola/.openclaw/load-env.sh && cd /home/nicola/.openclaw/workspace && python3 scripts/hourly-health-check.py >> logs/health-check.log 2>&1
```

---

## 📊 推送时间线

### 每日推送

| 时间 | 任务 | 类型 |
|------|------|------|
| **06:00** | 宪法学习 | 文字摘要 |
| **08:00** | 晨间智慧 | 文字推送 |
| **09:00** | 微信数据报告 | 待配置 |
| **18:00** | 微信发布 | 待配置 |
| **20:00** | 晚间智慧 | 待配置 |
| **23:00** | 日报生成 | MD 文件 |

---

### 每小时推送

| 时间 | 任务 | 类型 |
|------|------|------|
| **整点** | 健康检查 | 文字报告 |

---

## 🎯 待配置推送

| 任务 | 频率 | 状态 |
|------|------|------|
| **晨间智慧** | 每日 08:00 | ⏳ 待配置 |
| **晚间智慧** | 每日 20:00 | ⏳ 待配置 |
| **微信数据报告** | 每日 09:00 | ⏳ 待配置 |
| **Scheduler 摘要** | 每 5 分钟 | ⏳ 可选 |

---

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `scripts/send-md-to-telegram.py` | 通用发送工具 |
| `scripts/daily-report-generator.py` | 日报生成 |
| `scripts/daily-constitution-study.py` | 宪法学习 |
| `scripts/hourly-health-check.py` | 健康检查 |
| `crontab -l` | 定时任务配置 |

---

## 🎊 总结

### 已启用推送

```
✅ 日报生成 (23:00) - MD 文件
✅ 宪法学习 (06:00) - 文字摘要
✅ 健康检查 (每小时) - 文字报告
```

### 推送配置

```
✅ Telegram Bot Token: 已配置
✅ Chat ID: 7073481596 (SAYELF)
✅ 发送工具：send-md-to-telegram.py
✅ 错误处理：超时/失败保护
```

---

*太一 AGI · Telegram 推送配置 v1.0 · 2026-04-16 23:47*

**📱 定时任务成果将自动发送到 Telegram！**
