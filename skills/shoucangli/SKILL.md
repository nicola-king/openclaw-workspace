# Shoucangli (守藏吏) - 用户管理 Bot

> 版本：v1.0 | 创建：2026-03-27 | 状态：✅ 激活

---

## 🎯 职责定位

**Shoucangli (守藏吏)** = 付费用户管理专家

- **主责**: 付费用户数据库 + 订阅跟踪 + 交付自动化
- **数据源**: Gumroad API + Telegram + 本地数据库
- **输出**: 自动交付 + 续费提醒 + 收入报表
- **协作**: 猎手 (信号推送)、山木 (内容交付)、太一 (统筹)

---

## 📋 核心功能

### 1. 付费用户数据库

**用户信息**:
```python
{
    "user_id": "telegram_user_id",
    "email": "user@email.com",
    "name": "用户名称",
    "subscription": {
        "product": "Hunter Pro",  # 或 PolyAlert Pro
        "status": "active",  # active/expired/cancelled
        "start_date": "2026-03-27",
        "end_date": "2026-04-27",
        "auto_renew": True
    },
    "gumroad_purchase_id": "xxx",
    "joined_vip_group": True
}
```

**数据库**: SQLite 本地存储 (`~/.openclaw/workspace/data/steward_users.db`)

---

### 2. Gumroad 交付自动化

**Webhook 接入**:
```python
# Gumroad Webhook 处理
@app.route('/webhook/gumroad', methods=['POST'])
def gumroad_webhook():
    data = request.json
    
    if data['event'] == 'purchase':
        # 新用户购买
        user = create_user(data)
        send_welcome_message(user)
        invite_to_vip_group(user)
        
    elif data['event'] == 'subscription_renewal':
        # 续费成功
        user = update_subscription(data)
        send_renewal_confirmation(user)
        
    elif data['event'] == 'subscription_cancelled':
        # 订阅取消
        user = cancel_subscription(data)
        send_farewell_message(user)
```

**自动交付流程**:
```
用户购买 Gumroad 产品
    ↓
Gumroad Webhook 触发
    ↓
守藏吏 Bot 接收通知
    ↓
创建/更新用户数据库
    ↓
发送欢迎消息 (Telegram)
    ↓
邀请加入 VIP 群
    ↓
推送交付内容
```

---

### 3. 订阅管理

**到期提醒**:
```python
# 每日检查到期用户
def check_expiring_subscriptions():
    today = datetime.now()
    
    # 到期前 7 天提醒
    expiring_soon = db.query(
        "SELECT * FROM users WHERE end_date - ? = 7",
        (today,)
    )
    
    for user in expiring_soon:
        send_renewal_reminder(user)
```

**过期处理**:
```python
# 每日检查过期用户
def check_expired_subscriptions():
    today = datetime.now()
    
    expired = db.query(
        "SELECT * FROM users WHERE end_date < ?",
        (today,)
    )
    
    for user in expired:
        downgrade_to_free(user)
        remove_from_vip_group(user)
        send_expiry_notice(user)
```

---

### 4. 收入报表

**日报表**:
```python
def generate_daily_report():
    today = datetime.now().date()
    
    new_users = db.count_new_users(today)
    renewals = db.count_renewals(today)
    cancellations = db.count_cancellations(today)
    revenue = db.sum_revenue(today)
    
    report = f"""
【守藏吏日报 · {today}】

新增用户：{new_users}
续费用户：{renewals}
取消订阅：{cancellations}
今日收入：${revenue}

累计活跃用户：{db.count_active_users()}
累计收入：${db.sum_total_revenue()}
"""
    return report
```

**月报表**:
- 月收入统计
- 续费率分析
- 产品收益对比
- 用户增长趋势

---

## 🚀 启动命令

```bash
# 启动守藏吏 Bot
cd ~/.openclaw/workspace/skills/steward
python steward_bot.py &

# 查看状态
ps aux | grep steward
```

---

## 📊 与猎手 Bot 协作

```
猎手发现信号 → 推送给付费用户
                ↓
守藏吏检查用户订阅状态
                ↓
仅推送给 active 用户
                ↓
记录推送日志
```

---

## 🔧 配置项

```yaml
steward:
  bot_token: "待注册"
  database: "~/.openclaw/workspace/data/steward_users.db"
  vip_group_id: "@taiyi_vip"  # VIP 群 ID
  gumroad_webhook_port: 5000
  renewal_reminder_days: 7  # 到期前 N 天提醒
  daily_report_time: "20:00"  # 日报表发送时间
```

---

## 📝 运行日志

**日志位置**: `~/.openclaw/workspace/logs/steward.log`

**日志格式**:
```
[2026-03-27 20:05:00] INFO: Shoucangli Bot started
[2026-03-27 20:06:12] PURCHASE: New user - user@email.com
[2026-03-27 20:06:13] INVITED: user123 joined VIP group
[2026-03-27 20:00:00] REPORT: Daily revenue $0, Active users 0
```

---

## 🎯 KPI 指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 交付自动化率 | 100% | 待测试 |
| 续费率 | >80% | 待测试 |
| 用户满意度 | >95% | 待测试 |
| 月收入 | $5,000 | $0 |

---

## 📋 P1-P6 检查

| 原则 | 状态 | 说明 |
|------|------|------|
| P1 蒸馏来源 | ✅ 通过 | 内部涌现 |
| P2 查看本地 | ✅ 通过 | 无功能重叠 |
| P3 比对差异 | ✅ 通过 | 全新职责域 |
| P4 取其精华 | ✅ 通过 | 策略 C 并列 |
| P5 验证实名 | ✅ 通过 | 内部技能 |
| P6 安全评估 | ✅ 通过 | A 级安全 |

**审查级别**: L2 标准 (太一+SAYELF 告知)

**审查结果**: ✅ 批准激活

---

*版本：v1.0 | 创建时间：2026-03-27 20:05*
*状态：✅ 激活待运行*
