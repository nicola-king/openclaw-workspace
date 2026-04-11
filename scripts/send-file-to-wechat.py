#!/usr/bin/env python3
"""
发送文件到微信（作为邮件附件）
这样微信中可以下载文件
"""

import sys
import json
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_file_attachment(file_path: str, recipient: str = None):
    """发送文件附件到微信绑定邮箱"""
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ 文件不存在：{file_path}")
        return False
    
    # 加载 SMTP 配置
    config_path = Path('/home/nicola/.openclaw/workspace-taiyi/config/wechat.json')
    if not config_path.exists():
        print("❌ 配置文件不存在")
        return False
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    smtp_config = config.get('smtp', {})
    sender_email = smtp_config.get('sender_email')
    smtp_password = smtp_config.get('smtp_password')
    smtp_server = smtp_config.get('smtp_server', 'smtp.qq.com')
    smtp_port = smtp_config.get('smtp_port', 587)
    recipient_email = recipient or smtp_config.get('recipient_email')
    
    if not all([sender_email, smtp_password, recipient_email]):
        print("❌ SMTP 凭证未配置完整")
        return False
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"📄 {file_path.name}"
    
    # 邮件正文
    body = f"""
📄 文件已准备好

文件名：{file_path.name}
文件大小：{file_path.stat().st_size / 1024:.1f} KB

请查看附件下载文件。

---
太一 AGI | 自动生成
"""
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加文件附件
    try:
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{file_path.name}"'
        )
        msg.attach(part)
        
        print(f"✅ 附件已添加：{file_path.name}")
    except Exception as e:
        print(f"❌ 添加附件失败：{e}")
        return False
    
    # 发送邮件
    try:
        print(f"📧 发送邮件到：{recipient_email}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ 邮件已发送！")
        print(f"   收件人：{recipient_email}")
        print(f"   主题：📄 {file_path.name}")
        print(f"   附件：{file_path.name} ({file_path.stat().st_size / 1024:.1f} KB)")
        print(f"\n💡 微信中会收到邮件提醒，点击可下载附件")
        
        return True
        
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python3 send-file-to-wechat.py <文件路径> [收件人邮箱]")
        print("\n示例:")
        print("  python3 send-file-to-wechat.py /path/to/file.txt")
        print("  python3 send-file-to-wechat.py /path/to/file.pdf someone@example.com")
        sys.exit(1)
    
    file_path = sys.argv[1]
    recipient = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = send_file_attachment(file_path, recipient)
    sys.exit(0 if success else 1)
