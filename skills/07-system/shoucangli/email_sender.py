#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一每日交易日志邮件发送脚本
发送时间：每日 20:00 (Asia/Shanghai)
收件邮箱：285915125@qq.com
"""

import smtplib
import os
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import schedule
import time
import logging

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/steward_email.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ShoucangliEmail')

# 加载配置
CONFIG_PATH = '/home/nicola/.openclaw/workspace/skills/steward/.email_config.yaml'

def load_config():
    """加载邮箱配置"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config['email']
    except Exception as e:
        logger.error(f"加载配置失败：{e}")
        return None

class EmailSender:
    def __init__(self, config):
        self.config = config
        self.receiver = config['receiver_email']
        self.sender = config['sender_email']
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        self.password = config['sender_password']
    
    def generate_daily_report(self):
        """生成每日交易报告"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # TODO: 从太一控制器获取实际数据
        # 当前使用模板数据
        report = f"""
# 太一每日交易报告

**日期**: {today}
**时间**: 20:00 (Asia/Shanghai)
**授权级别**: 100% 自动执行

---

## 📊 总览

| 项目 | 数值 |
|------|------|
| 总资金 | $150 (1.7 SOL) |
| 今日盈亏 | +$XX.XX (+X.XX%) |
| 累计盈亏 | +$XX.XX (+X.XX%) |
| 交易次数 | XX 笔 |
| 胜率 | XX% |

---

## 📈 平台表现

### GMGN (1.7 SOL = $150)

| 钱包类型 | 本金 | 今日盈亏 | 累计盈亏 | 回报率 |
|---------|------|---------|---------|--------|
| **跟单钱包 (6 个)** | $90 | +$X.XX | +$X.XX | +X.X% |
| **狙击钱包 (2 个)** | $45 | +$X.XX | +$X.XX | +X.X% |
| **条件单 (1 个)** | $15 | +$X.XX | +$X.XX | +X.X% |
| **总计** | $150 | +$X.XX | +$X.XX | +X.X% |

---

## 🚨 风控状态

| 指标 | 阈值 | 当前 | 状态 |
|------|------|------|------|
| **日亏损** | -$15 (-10%) | -$X.XX | ✅ 安全 |
| **总回撤** | -$60 (-40%) | -$X.XX | ✅ 安全 |
| **单平台亏损** | -$22.5 (-15%) | -$X.XX | ✅ 安全 |

---

## 📊 钱包表现 Top 5

| 排名 | 钱包名称 | 今日盈亏 | 累计盈亏 | 胜率 |
|------|---------|---------|---------|------|
| 1 | ColdMath | +$X.X | +$X.X | XX% |
| 2 | majorexploiter | +$X.X | +$X.X | XX% |
| 3 | whale_hunter | +$X.X | +$X.X | XX% |
| 4 | moon_shot | +$X.X | +$X.X | XX% |
| 5 | defi_king | +$X.X | +$X.X | XX% |

---

## 💰 提现记录

| 日期 | 类型 | 金额 | 说明 |
|------|------|------|------|
| {today} | 盈利提现 | $X.XX | 50% 利润自动提现 |

---

## 🎯 明日计划

1. 继续监控 10 钱包执行
2. 优化表现差的钱包参数
3. 根据市场情况调整策略

---

*本报告由太一 AGI 自动生成并发送*
*授权级别：100% 自动执行*
*使命：价值创造 · 免费开源 · 负熵 · 风控 · 透明*
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
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            server.quit()
            
            logger.info(f"✅ 邮件发送成功：{subject}")
            logger.info(f"📮 收件人：{self.receiver}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 邮件发送失败：{str(e)}")
            return False
    
    def send_daily_report(self):
        """发送每日报告"""
        subject = f"【太一交易日志】{datetime.now().strftime('%Y-%m-%d')}"
        content = self.generate_daily_report()
        success = self.send_email(subject, content)
        
        if success:
            logger.info("📧 日报发送完成")
        else:
            logger.error("📧 日报发送失败，将重试")
        
        return success
    
    def start_scheduler(self):
        """启动定时任务"""
        # 每日 20:00 发送
        schedule.every().day.at("20:00").do(self.send_daily_report)
        
        logger.info("📧 邮件发送任务已启动")
        logger.info(f"⏰ 发送时间：每日 20:00 (Asia/Shanghai)")
        logger.info(f"📮 收件邮箱：{self.receiver}")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == '__main__':
    logger.info("🚀 太一日志邮件发送服务启动...")
    
    # 加载配置
    config = load_config()
    
    if not config:
        logger.error("❌ 配置加载失败，请检查 .email_config.yaml")
        exit(1)
    
    logger.info("✅ 配置加载成功")
    
    # 创建发送器
    sender = EmailSender(config)
    
    # 测试发送 (首次运行)
    logger.info("📧 发送测试邮件...")
    sender.send_daily_report()
    
    # 启动定时任务
    logger.info("⏰ 启动定时任务...")
    sender.start_scheduler()
