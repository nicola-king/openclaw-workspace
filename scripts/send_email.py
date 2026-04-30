#!/usr/bin/env python3
"""
邮件发送脚本 - 使用 QQ 邮箱 SMTP
用法：python3 send_email.py <收件人> <主题> <内容文件> [附件]
"""

import smtplib
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# QQ 邮箱 SMTP 配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SENDER_EMAIL = "285915125@qq.com"  # 需要配置为实际发件邮箱
SENDER_PASSWORD = ""  # 需要配置授权码

def send_email(recipient, subject, content_file, attachments=None):
    """发送邮件"""
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # 读取内容
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加正文
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    
    # 添加附件
    if attachments:
        for file_path in attachments:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={os.path.basename(file_path)}'
                    )
                    msg.attach(part)
                    print(f"✅ 添加附件：{file_path}")
    
    # 发送邮件
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ 邮件已发送至：{recipient}")
        return True
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法：python3 send_email.py <收件人> <主题> <内容文件> [附件 1] [附件 2] ...")
        sys.exit(1)
    
    recipient = sys.argv[1]
    subject = sys.argv[2]
    content_file = sys.argv[3]
    attachments = sys.argv[4:] if len(sys.argv) > 4 else None
    
    send_email(recipient, subject, content_file, attachments)
