#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一备份邮件发送脚本
使用 QQ 邮箱 SMTP 发送备份文件
"""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header

# 配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
FROM_EMAIL = "285915125@qq.com"
TO_EMAIL = "285915125@qq.com"

# 从环境变量获取授权码 (非密码)
SMTP_PASSWORD = os.getenv('QQ_SMTP_AUTH_CODE', '')

def send_backup_email(backup_file, backup_date):
    """发送备份邮件"""
    
    if not SMTP_PASSWORD:
        print("❌ 错误：未配置 QQ 邮箱 SMTP 授权码")
        print("获取方式:")
        print("1. 登录 QQ 邮箱")
        print("2. 设置→账户")
        print("3. 开启 SMTP 服务")
        print("4. 获取授权码")
        print("5. 设置环境变量：export QQ_SMTP_AUTH_CODE='你的授权码'")
        return False
    
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL
        msg["Subject"] = Header(f"太一记忆体备份 - {backup_date}", "utf-8")
        
        # 邮件正文
        body = f"""
太一记忆体备份已完成

备份日期：{backup_date}
备份文件：{os.path.basename(backup_file)}
备份大小：{os.path.getsize(backup_file) / 1024 / 1024:.2f} MB

用途:
- OpenClaw 重新安装
- 升级失败恢复
- 系统损坏恢复

恢复指南见备份包内 README-RESTORE.md

---
太一 AGI · 自动备份系统
        """
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # 添加附件
        with open(backup_file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(backup_file)}"
            )
            msg.attach(part)
        
        # 发送邮件
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(FROM_EMAIL, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        
        print(f"✅ 邮件发送成功！")
        print(f"发送到：{TO_EMAIL}")
        print(f"附件：{os.path.basename(backup_file)}")
        return True
    
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python3 send-backup-email.py <备份文件> <备份日期>")
        print("示例：python3 send-backup-email.py /tmp/taiyi-backup.tar.gz 20260328")
        sys.exit(1)
    
    backup_file = sys.argv[1]
    backup_date = sys.argv[2]
    
    if not os.path.exists(backup_file):
        print(f"❌ 备份文件不存在：{backup_file}")
        sys.exit(1)
    
    success = send_backup_email(backup_file, backup_date)
    sys.exit(0 if success else 1)
