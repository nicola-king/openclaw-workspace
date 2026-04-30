#!/usr/bin/env python3
"""
太一邮件发送器
发送日报、文章、报告到 SAYELF 邮箱

配置：
    ~/.taiyi/email/config.json

用法：
    python3 email_sender.py --to 285915125@qq.com --subject "主题" --content "内容"
"""

import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSender:
    """太一邮件发送器"""
    
    def __init__(self):
        # 从环境变量或配置文件读取
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.qq.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "465"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
        
        # 配置文件路径
        config_path = Path.home() / ".taiyi" / "email" / "config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
                self.smtp_server = config.get("smtp_server", self.smtp_server)
                self.smtp_port = config.get("smtp_port", self.smtp_port)
                self.sender_email = config.get("sender_email", self.sender_email)
                self.sender_password = config.get("sender_password", self.sender_password)
    
    def send_email(self, to_email, subject, content, html=False):
        """发送邮件"""
        if not self.sender_email or not self.sender_password:
            print("❌ 错误：未配置 SMTP 凭证")
            print("\n配置方法：")
            print("1. 创建 ~/.taiyi/email/config.json")
            print("2. 或设置环境变量 SMTP_SERVER, SENDER_EMAIL, SENDER_PASSWORD")
            return False
        
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            
            # 添加内容
            content_type = "html" if html else "plain"
            msg.attach(MIMEText(content, content_type, "utf-8"))
            
            # 连接 SMTP 服务器
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, [to_email], msg.as_string())
            server.quit()
            
            print(f"✅ 邮件发送成功！")
            print(f"收件人：{to_email}")
            print(f"主题：{subject}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败：{e}")
            return False

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="太一邮件发送器")
    parser.add_argument("--to", required=True, help="收件人邮箱")
    parser.add_argument("--subject", required=True, help="邮件主题")
    parser.add_argument("--content", required=True, help="邮件内容")
    parser.add_argument("--html", action="store_true", help="HTML 格式")
    
    args = parser.parse_args()
    
    sender = EmailSender()
    sender.send_email(args.to, args.subject, args.content, args.html)
