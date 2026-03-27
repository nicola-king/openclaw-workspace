# PolyAlert - Polymarket 价格监控技能

> 7x24 小时监控 Polymarket 市场概率波动，触发条件时自动推送 Telegram 通知

---

## 📋 技能信息

| 项目 | 内容 |
|------|------|
| **名称** | PolyAlert |
| **版本** | v0.1.0 |
| **创建时间** | 2026-03-26 |
| **作者** | 太一 |
| **状态** | 🟡 测试中 |
| **Bot** | @TrueListenBot (谛听) |

---

## 🎯 功能描述

**核心功能**:
- 7x24 小时监控 Polymarket 市场
- 60 秒轮询一次概率变化
- 触发条件自动推送 Telegram 通知
- 支持多种触发条件（高置信度/低置信度/剧烈波动）

**监控条件**:
| 条件 | 阈值 | 说明 |
|------|------|------|
| 高置信度 | 概率 > 90% | 市场高度确定 |
| 低置信度 | 概率 < 10% | 市场高度不确定 |
| 剧烈波动 | 变化 > 20% | 概率大幅变化 |

---

## 🔧 技术架构

```
PolyAlert
├── config.py          # 配置（市场列表/触发条件）
├── monitor.py         # 监控服务（轮询/触发判断）
├── notifier.py        # 通知服务（Telegram 推送）
├── storage.py         # 数据存储（SQLite）
├── poly_client.py     # Polymarket API 客户端
└── main.py            # 入口文件
```

**依赖**:
- Python 3.8+
- requests
- SQLite3
- Telegram Bot API

---

## 📖 使用方法

### 启动监控

```bash
cd ~/.openclaw/workspace
python3 -m skills.polyalert.monitor
```

### 后台运行

```bash
nohup python3 -m skills.polyalert.monitor > skills/polyalert/logs/polyalert-run.log 2>&1 &
```

### 查看日志

```bash
tail -f skills/polyalert/logs/polyalert.log
```

### 停止服务

```bash
pkill -f "polyalert.monitor"
```

---

## ⚙️ 配置说明

### config.py

```python
# 监控市场列表
MARKETS_TO_MONITOR = [
    "will-btc-reach-100k-by-end-of-2026",
    "will-eth-reach-5000-by-end-of-2026",
    # 从 polymarket.com 复制 slug
]

# 触发条件
TRIGGER_HIGH_PROBABILITY = 0.90  # 概率>90%
TRIGGER_LOW_PROBABILITY = 0.10   # 概率<10%
TRIGGER_LARGE_CHANGE = 0.20      # 变化>20%

# 轮询间隔（秒）
MONITOR_INTERVAL_SECONDS = 60

# Telegram Bot 配置
TELEGRAM_BOT_TOKEN = "你的 Token"
TELEGRAM_ADMIN_ID = "你的用户 ID"
```

---

## 📊 数据示例

### 触发通知示例

```
🚨 PolyAlert 触发提醒

🔴 高置信度
市场：Will BTC reach $100K by end of 2026?
方向：YES
概率：85.0% → 92.0% (📈+8.2%)
触发条件：概率 > 90%

📊 市场链接：https://polymarket.com/event/...

⏰ 时间：2026-03-26 21:45:32
```

### 数据库表结构

```sql
-- 监控市场表
CREATE TABLE markets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    category TEXT,
    current_prob REAL,
    last_checked TIMESTAMP
);

-- 提醒记录表
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT,
    trigger_type TEXT,
    old_prob REAL,
    new_prob REAL,
    sent_at TIMESTAMP
);
```

---

## 🎯 使用场景

### 场景 1：交易机会发现
```
监控热门市场 → 概率剧烈波动 → 立即通知 → 抓住交易机会
```

### 场景 2：高置信度套利
```
监控概率>90% 市场 → 接近结算 → 低价买入 → 等待结算
```

### 场景 3：新闻事件跟踪
```
重大新闻发布 → 市场概率变化 → 立即通知 → 快速反应
```

---

## ⚠️ 注意事项

1. **API 限制**: Polymarket API 有速率限制，建议轮询间隔≥60 秒
2. **代理配置**: 需要配置 Clash 代理（端口 7890）
3. **市场 slug**: 从 polymarket.com 官网复制真实有效的市场
4. **Bot 配对**: 用户需先在 Telegram 启动 @TrueListenBot

---

## 📈 性能指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 轮询间隔 | 60 秒 | 60 秒 ✅ |
| 通知延迟 | <1 分钟 | <1 分钟 ✅ |
| 监控市场 | 10 个 | 6 个 🟡 |
| 触发准确率 | >95% | 待验证 ⏳ |

---

## 🚀 待办事项

### P0 紧急
- [ ] 替换为知几-E CLOB API（获取实时数据）
- [ ] 验证第一次真实触发
- [ ] 邀请 5-10 个测试用户

### P1 重要
- [ ] PNG 卡片通知（集成 ljj-card）
- [ ] 聪明钱排行榜
- [ ] 订阅付费系统

### P2 一般
- [ ] 多账号支持
- [ ] 自定义触发条件
- [ ] 历史数据导出

---

## 📞 支持与反馈

**问题反馈**: Telegram @TrueListenBot
**GitHub**: github.com/nicola-king/polyalert
**文档**: skills/polyalert/README.md

---

*版本：v0.1.0 | 更新时间：2026-03-26 | 状态：测试中*
