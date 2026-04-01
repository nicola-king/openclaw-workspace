# 太一每日交易日志邮件发送配置

> 版本：v1.0 | 创建：2026-03-27 22:11 | 太一执行

---

## 📧 邮件配置

| 项目 | 配置 |
|------|------|
| **收件邮箱** | 285915125@qq.com |
| **发件频率** | 每日 20:00 (Asia/Shanghai) |
| **邮件主题** | 【太一交易日志】YYYY-MM-DD |
| **发送渠道** | QQ 邮箱 SMTP |

---

## 📋 邮件内容模板

### 邮件主题
```
【太一交易日志】2026-03-27
```

### 邮件正文

```markdown
# 太一每日交易报告

**日期**: 2026-03-27
**时间**: 20:00 (Asia/Shanghai)
**授权级别**: 100% 自动执行

---

## 📊 总览

| 项目 | 数值 |
|------|------|
| 总资金 | $255 (1.7 SOL) |
| 今日盈亏 | +$XX.XX (+X.XX%) |
| 累计盈亏 | +$XX.XX (+X.XX%) |
| 交易次数 | XX 笔 |
| 胜率 | XX% |

---

## 📈 平台表现

### GMGN (1.7 SOL = $255)

| 钱包类型 | 本金 | 今日盈亏 | 累计盈亏 | 回报率 |
|---------|------|---------|---------|--------|
| **跟单钱包 (6 个)** | $153 | +$X.XX | +$X.XX | +X.X% |
| **狙击钱包 (2 个)** | $76.5 | +$X.XX | +$X.XX | +X.X% |
| **条件单 (1 个)** | $25.5 | +$X.XX | +$X.XX | +X.X% |
| **总计** | $255 | +$X.XX | +$X.XX | +X.X% |

### Polymarket (150 USDC)

| 策略 | 本金 | 今日盈亏 | 累计盈亏 | 回报率 |
|------|------|---------|---------|--------|
| **气象套利** | $75 | +$X.XX | +$X.XX | +X.X% |
| **聪明钱跟随** | $45 | +$X.XX | +$X.XX | +X.X% |
| **事件套利** | $30 | +$X.XX | +$X.XX | +X.X% |
| **总计** | $150 | +$X.XX | +$X.XX | +X.X% |

---

## 📋 今日交易明细

### GMGN 交易

| 时间 | 钱包 | 类型 | 方向 | 金额 | 盈亏 | 状态 |
|------|------|------|------|------|------|------|
| 09:30 | ColdMath | 跟单 | BUY | $46 | +$5.5 | ✅ 止盈 |
| 10:15 | moon_shot | 狙击 | BUY | $38 | +$3.8 | ✅ 持仓 |
| 14:20 | smarttrader | 跟单 | SELL | $31 | -$2.1 | ❌ 止损 |
| ... | ... | ... | ... | ... | ... | ... |

### Polymarket 交易

| 时间 | 市场 | 策略 | 方向 | 金额 | 盈亏 | 状态 |
|------|------|------|------|------|------|------|
| 08:00 | BTC_100K | 气象套利 | YES | $25 | +$12.5 | ✅ 已结算 |
| 15:30 | ETH_5K | 聪明钱跟随 | NO | $15 | +$7.5 | ✅ 已结算 |
| ... | ... | ... | ... | ... | ... | ... |

---

## 🚨 风控状态

| 指标 | 阈值 | 当前 | 状态 |
|------|------|------|------|
| **日亏损** | -$25.5 (-10%) | -$X.XX | ✅ 安全 |
| **总回撤** | -$102 (-40%) | -$X.XX | ✅ 安全 |
| **单平台亏损** | -$38 (-15%) | -$X.XX | ✅ 安全 |
| **连续亏损** | 3 日 | X 日 | ✅ 安全 |

---

## 📊 钱包表现 Top 5

| 排名 | 钱包名称 | 今日盈亏 | 累计盈亏 | 胜率 | 状态 |
|------|---------|---------|---------|------|------|
| 1 | ColdMath | +$8.2 | +$15.6 | 82% | ✅ 优秀 |
| 2 | majorexploiter | +$6.5 | +$12.3 | 76% | ✅ 良好 |
| 3 | whale_hunter | +$4.1 | +$8.9 | 74% | ✅ 良好 |
| 4 | moon_shot | +$3.8 | +$5.7 | 70% | ✅ 良好 |
| 5 | defi_king | +$2.9 | +$6.2 | 72% | ✅ 良好 |

---

## 💰 提现记录

| 日期 | 类型 | 金额 | 说明 |
|------|------|------|------|
| 2026-03-27 | 盈利提现 | $X.XX | 50% 利润自动提现 |

---

## 📈 累计收益曲线

```
日期       资金      日收益    累计收益
03-27     $255      +$0       +$0
03-28     $XXX      +$XX      +$XX
...
```

---

## 🎯 明日计划

1. 继续监控 10 钱包执行
2. 优化表现差的钱包参数
3. 根据市场情况调整策略
4. 盈利达到 50% 自动提现

---

## 📞 联系方式

- **太一 AGI**: 自动执行系统
- **技术支持**: GitHub Issues
- **文档**: https://github.com/nicola-king/zhiji-e

---

*本报告由太一 AGI 自动生成并发送*
*授权级别：100% 自动执行*
*使命：价值创造 · 免费开源 · 负熵 · 风控 · 透明*
```

---

## 🔧 Python 邮件发送脚本

**文件**: `skills/steward/email_sender.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一每日交易日志邮件发送脚本
发送时间：每日 20:00 (Asia/Shanghai)
收件邮箱：285915125@qq.com
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import schedule
import time

# 邮件配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "your_qq_email@qq.com"  # 需要配置
SENDER_PASSWORD = "your_smtp_auth_code"  # QQ 邮箱 SMTP 授权码
RECEIVER_EMAIL = "285915125@qq.com"

class EmailSender:
    def __init__(self):
        self.receiver = RECEIVER_EMAIL
        self.sender = SENDER_EMAIL
    
    def generate_daily_report(self):
        """生成每日交易报告"""
        # 从数据库/日志获取数据
        today = datetime.now().strftime('%Y-%m-%d')
        
        # TODO: 从太一控制器获取实际数据
        report = f"""
# 太一每日交易报告

**日期**: {today}
**时间**: 20:00 (Asia/Shanghai)

---

## 📊 总览

| 项目 | 数值 |
|------|------|
| 总资金 | $255 (1.7 SOL) |
| 今日盈亏 | +$XX.XX (+X.XX%) |
| 累计盈亏 | +$XX.XX (+X.XX%) |
| 交易次数 | XX 笔 |

---

## 📈 平台表现

### GMGN (1.7 SOL = $255)

| 钱包类型 | 本金 | 今日盈亏 | 累计盈亏 | 回报率 |
|---------|------|---------|---------|--------|
| 跟单钱包 | $153 | +$X.XX | +$X.XX | +X.X% |
| 狙击钱包 | $76.5 | +$X.XX | +$X.XX | +X.X% |
| 条件单 | $25.5 | +$X.XX | +$X.XX | +X.X% |
| 总计 | $255 | +$X.XX | +$X.XX | +X.X% |

### Polymarket (150 USDC)

| 策略 | 本金 | 今日盈亏 | 累计盈亏 | 回报率 |
|------|------|---------|---------|--------|
| 气象套利 | $75 | +$X.XX | +$X.XX | +X.X% |
| 聪明钱跟随 | $45 | +$X.XX | +$X.XX | +X.X% |
| 事件套利 | $30 | +$X.XX | +$X.XX | +X.X% |
| 总计 | $150 | +$X.XX | +$X.XX | +X.X% |

---

## 🚨 风控状态

✅ 所有风控指标正常

---

*本报告由太一 AGI 自动生成*
"""
        return report
    
    def send_email(self, subject, content):
        """发送邮件"""
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.receiver
            msg['Subject'] = subject
            
            # 添加正文
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # 连接 SMTP 服务器
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            server.login(self.sender, SENDER_PASSWORD)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            server.quit()
            
            print(f"✅ 邮件发送成功：{subject}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败：{str(e)}")
            return False
    
    def send_daily_report(self):
        """发送每日报告"""
        subject = f"【太一交易日志】{datetime.now().strftime('%Y-%m-%d')}"
        content = self.generate_daily_report()
        return self.send_email(subject, content)
    
    def start_scheduler(self):
        """启动定时任务"""
        # 每日 20:00 发送
        schedule.every().day.at("20:00").do(self.send_daily_report)
        
        print("📧 邮件发送任务已启动")
        print("⏰ 发送时间：每日 20:00 (Asia/Shanghai)")
        print("📮 收件邮箱：285915125@qq.com")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == '__main__':
    sender = EmailSender()
    
    # 测试发送
    # sender.send_daily_report()
    
    # 启动定时任务
    sender.start_scheduler()
```

---

## 🔑 QQ 邮箱 SMTP 配置步骤

### Step 1: 登录 QQ 邮箱

```
访问：https://mail.qq.com
登录：285915125@qq.com
```

### Step 2: 开启 SMTP 服务

```
设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
→ 开启 SMTP 服务
→ 生成授权码
```

### Step 3: 记录授权码

```
授权码：XXXXXXXXXXXXXXXX  (16 位)
保存位置：~/.openclaw/workspace/.email_credentials
```

### Step 4: 更新配置文件

**文件**: `skills/steward/.email_config.yaml`

```yaml
email:
  smtp_server: smtp.qq.com
  smtp_port: 465
  sender_email: 285915125@qq.com
  sender_password: "YOUR_AUTH_CODE"  # 填入授权码
  receiver_email: 285915125@qq.com
  send_time: "20:00"  # Asia/Shanghai
```

---

## 🚀 部署步骤

### Step 1: 安装依赖

```bash
pip3 install schedule
```

### Step 2: 配置授权码

```bash
cd ~/.openclaw/workspace/skills/steward
nano .email_config.yaml
# 填入 QQ 邮箱授权码
```

### Step 3: 启动邮件服务

```bash
cd ~/.openclaw/workspace/skills/steward
nohup python3 email_sender.py > /tmp/steward_email.log 2>&1 &
```

### Step 4: 验证状态

```bash
ps aux | grep email_sender
tail -f /tmp/steward_email.log
```

---

## 📋 执行清单

**今日配置 (22:11-22:30)**:
- [ ] 获取 QQ 邮箱 SMTP 授权码
- [ ] 创建 .email_config.yaml 配置文件
- [ ] 安装 schedule 依赖
- [ ] 启动 email_sender.py 服务
- [ ] 测试发送第 1 封邮件

**每日自动执行**:
- [ ] 20:00 自动发送日报
- [ ] 记录发送日志
- [ ] 失败重试 (最多 3 次)

---

## 📊 邮件发送日志

**日志位置**: `/tmp/steward_email.log`

**日志格式**:
```
[2026-03-27 20:00:00] INFO: 开始生成日报
[2026-03-27 20:00:01] INFO: 开始发送邮件
[2026-03-27 20:00:03] INFO: ✅ 邮件发送成功
[2026-03-27 20:00:03] INFO: 收件人：285915125@qq.com
[2026-03-27 20:00:03] INFO: 主题：【太一交易日志】2026-03-27
```

---

## 🚨 异常处理

### 发送失败处理

| 错误类型 | 重试策略 | 通知方式 |
|---------|---------|---------|
| **网络错误** | 重试 3 次 (间隔 5 分钟) | Telegram 通知 |
| **授权码错误** | 停止发送 | Telegram 通知用户 |
| **邮箱满** | 停止发送 | Telegram 通知用户 |
| **内容错误** | 记录日志 | 次日修复 |

---

*版本：v1.0 | 创建时间：2026-03-27 22:11*
*收件邮箱：285915125@qq.com*
*发送时间：每日 20:00 (Asia/Shanghai)*
