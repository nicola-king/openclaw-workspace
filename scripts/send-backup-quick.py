#!/usr/bin/env python3
"""
快速发送备份邮件
用法：python3 send-backup-quick.py
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# 配置
FROM_EMAIL = "285915125@qq.com"
TO_EMAIL = "285915125@qq.com"
SUBJECT = "太一宪法备份 - 20260327"
BACKUP_FILE = "/opt/taiyi-backup/taiyi-backup-20260327-000824.tar.gz"
SIMPLE_BACKUP = "/home/nicola/taiyi-simple-backup-20260327-000801.tar.gz"

# 邮件内容
body = """太一宪法备份

序列号：TY-CONSTITUTION-20260327-000824
创建时间：2026-03-27 00:08:24
版本：v1.0.0

备份内容:
- 宪法文档 (constitution/)
- 记忆体系 (memory/)
- 核心文件 (MEMORY.md, HEARTBEAT.md, SOUL.md, ...)
- 技能目录 (skills/)
- 脚本目录 (scripts/)

恢复指南:
  tar -xzf taiyi-backup-20260327-000824.tar.gz
  cd 20260327-000824
  bash restore.sh

请妥善保存此备份文件，用于系统恢复。

--
太一 AGI 自动备份系统
"""

def send_email(password):
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = SUBJECT
        
        # 添加正文
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 附加完整系统备份
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(BACKUP_FILE)}')
                msg.attach(part)
            print(f"✅ 已附加：{os.path.basename(BACKUP_FILE)}")
        
        # 附加简单打包
        if os.path.exists(SIMPLE_BACKUP):
            with open(SIMPLE_BACKUP, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(SIMPLE_BACKUP)}')
                msg.attach(part)
            print(f"✅ 已附加：{os.path.basename(SIMPLE_BACKUP)}")
        
        # 发送
        print(f"正在发送到 {TO_EMAIL}...")
        server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=60)
        server.set_debuglevel(0)
        try:
            server.login(FROM_EMAIL, password)
            server.send_message(msg)
            server.quit()
            print(f"✅ 邮件已成功发送到 {TO_EMAIL}!")
            return True
        except Exception as e:
            print(f"❌ 登录或发送失败：{e}")
            print("请检查 QQ 邮箱授权码是否正确")
            return False
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

if __name__ == '__main__':
    import getpass
    print("=" * 60)
    print("太一备份邮件发送")
    print("=" * 60)
    print()
    print(f"收件人：{TO_EMAIL}")
    print(f"附件 1: {os.path.basename(BACKUP_FILE)} (542K)")
    print(f"附件 2: {os.path.basename(SIMPLE_BACKUP)} (2.3M)")
    print()
    
    # 获取授权码
    password = getpass.getpass("请输入 QQ 邮箱授权码 (不是 QQ 密码): ")
    
    # 发送
    success = send_email(password)
    
    if success:
        print()
        print("✅ 发送完成！请检查收件箱确认。")
    else:
        print()
        print("❌ 发送失败")
        print()
        print("获取授权码方法:")
        print("1. 登录 QQ 邮箱 (mail.qq.com)")
        print("2. 设置 → 账户")
        print("3. 开启 POP3/SMTP 服务")
        print("4. 生成授权码")
