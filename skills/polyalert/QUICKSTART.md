# PolyAlert 快速启动指南

## 📋 前置条件

1. Python 3.8+
2. Telegram 账号
3. Polymarket 账号（可选）

---

## 🚀 第一步：创建 Telegram Bot

1. 打开 Telegram，搜索 `@BotFather`
2. 发送 `/newbot` 命令
3. 按提示输入 Bot 名称（如：PolyAlert Bot）
4. 输入 Bot Username（如：@PolyAlertBot）
5. BotFather 会返回 Token，格式如：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. 复制 Token，粘贴到 `config.py` 的 `TELEGRAM_BOT_TOKEN`

```python
# config.py
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # 粘贴你的 Token
TELEGRAM_ADMIN_ID = "7073481596"  # 你的 Telegram 用户 ID
```

---

## 🔧 第二步：获取 Telegram 用户 ID

1. 在 Telegram 搜索 `@userinfobot`
2. 发送任意消息
3. Bot 会回复你的用户 ID（如：7073481596）
4. 复制到 `config.py` 的 `TELEGRAM_ADMIN_ID`

---

## ▶️ 第三步：启动监控服务

```bash
# 进入工作目录
cd ~/.openclaw/workspace

# 启动 PolyAlert
python3 -m skills.polyalert.monitor
```

或者后台运行：

```bash
# 使用 nohup
nohup python3 -m skills.polyalert.monitor > polyalert.log 2>&1 &

# 查看日志
tail -f polyalert.log
```

---

## 📊 第四步：验证运行状态

### 检查日志

```bash
cat skills/polyalert/logs/polyalert.log
```

### 检查数据库

```bash
sqlite3 skills/polyalert/data/polyalert.db "SELECT * FROM markets LIMIT 5;"
```

### 检查 Telegram 通知

等待第一次触发提醒，或手动测试：

```python
# 测试 Telegram 通知
python3 -c "
from skills.polyalert.notifier import send_welcome_message
send_welcome_message()
print('✅ 测试消息已发送')
"
```

---

## ⚙️ 配置说明

### 监控市场配置

编辑 `config.py` 的 `MARKETS_TO_MONITOR`：

```python
MARKETS_TO_MONITOR = [
    "bitcoin-price-2026",      # BTC 价格市场
    "ethereum-price-2026",     # ETH 价格市场
    "trump-approval-rating",   # 特朗普支持率
    # 添加更多市场...
]
```

### 触发条件配置

```python
TRIGGER_HIGH_PROBABILITY = 0.90  # 概率>90% 触发
TRIGGER_LOW_PROBABILITY = 0.10   # 概率<10% 触发
TRIGGER_LARGE_CHANGE = 0.20      # 变化>20% 触发
```

### 轮询间隔配置

```python
MONITOR_INTERVAL_SECONDS = 60  # 60 秒轮询一次
```

---

## 🔍 常见问题

### Q: Telegram 消息发送失败？

A: 检查：
1. Token 是否正确
2. 用户 ID 是否正确
3. 是否已启动 Bot（发送 /start）

### Q: API 请求失败？

A: 检查：
1. 网络连接
2. Polymarket API 是否正常
3. 是否触发限流（降低轮询频率）

### Q: 如何添加新市场？

A: 
1. 在 Polymarket 找到市场
2. 复制 URL slug（如 `bitcoin-price-2026`）
3. 添加到 `MARKETS_TO_MONITOR` 列表

---

## 📈 监控仪表板（开发中）

访问：`http://localhost:8000`（待实现）

功能：
- 实时监控市场
- 提醒历史记录
- 订阅管理
- 数据统计

---

## 💰 订阅付费（开发中）

当前状态：免费试用

付费计划（即将上线）：
- 基础版：$5/月
- 专业版：$15/月
- 企业版：$50/月

---

## 📞 支持与反馈

Telegram: @PolyAlertBot
Email: support@polyalert.io
GitHub: github.com/polyalert

---

*版本：v0.1.0 | 更新时间：2026-03-26*
