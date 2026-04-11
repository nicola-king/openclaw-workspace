#!/usr/bin/env python3
"""
发送 MD 文件到微信
通过山木微信助手发送邮件到微信
"""

import sys
import json
from pathlib import Path

# 添加山木微信助手路径
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/shanmu/wechat-assistant')

FILE_PATH = '/home/nicola/.openclaw/workspace/reports/taiyi-achievement-report-20260411.txt'
RECIPIENT = '285915125@qq.com'  # 微信绑定邮箱

def read_file():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def create_email_content(md_content):
    """创建邮件内容"""
    subject = "📊 太一工作成果汇报 - 2026-04-11"
    
    # 邮件正文
    body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .highlight {{ background: #e8f5e9; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #4CAF50; color: white; }}
        pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #4CAF50; padding-left: 20px; color: #666; }}
    </style>
</head>
<body>

<h1>📊 太一工作成果汇报</h1>
<p><strong>汇报时间：</strong>2026-04-11 21:10 | <strong>汇报人：</strong>太一 AGI</p>

<div class="highlight">
<h2>📋 执行摘要</h2>
<ul>
    <li>✅ P0 核心任务：5/5 完成 (100%)</li>
    <li>✅ 技能总数：384+</li>
    <li>✅ 系统健康度：100%</li>
    <li>✅ 学习循环：14 次</li>
    <li>✅ 融合创新：56 个</li>
</ul>
</div>

<h2>🚀 10 大成就</h2>
<ol>
    <li>太一镜像 v2.0 (用户数字分身)</li>
    <li>情景 Agent (384 Skills)</li>
    <li>心理学框架 (CBT/正念/习惯)</li>
    <li>MarkItDown (文档转换)</li>
    <li>错误自愈系统 (100% 健康)</li>
    <li>Cost.Agent (市政工程造价)</li>
    <li>太一记忆宫殿 v2.0</li>
    <li>自进化自动化</li>
    <li>OpenClaw 4.10 融合</li>
    <li>多平台集成 (微信/Telegram/飞书)</li>
</ol>

<h2>📝 完整内容</h2>
<div style="background: #f9f9f9; padding: 20px; border: 1px solid #ddd; border-radius: 5px; white-space: pre-wrap; font-family: monospace; font-size: 13px;">
{md_content[:15000]}
</div>

<div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px;">
<p><strong>太一 AGI</strong> | 自动生成</p>
<p>完整文件路径：/home/nicola/.openclaw/workspace/reports/taiyi-achievement-report-20260411.txt</p>
</div>

</body>
</html>
"""
    return subject, body

def send_email(subject, body):
    """发送邮件"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # 加载配置
    config_path = Path('/home/nicola/.openclaw/workspace-taiyi/config/wechat.json')
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        print("❌ 未找到 SMTP 配置文件")
        return False
    
    smtp_config = config.get('smtp', {})
    sender_email = smtp_config.get('sender_email')
    smtp_password = smtp_config.get('smtp_password')
    recipient_email = smtp_config.get('recipient_email', RECIPIENT)
    
    if not sender_email or not smtp_password:
        print("❌ SMTP 凭证未配置")
        return False
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, [RECIPIENT], msg.as_string())
        server.quit()
        
        print(f"✅ 邮件已发送到：{recipient_email}")
        print(f"主题：{subject}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")
        return False

def main():
    print("="*60)
    print("📱 发送 MD 文件到微信")
    print("="*60)
    
    # 1. 读取文件
    print("\n1. 读取 MD 文件...")
    md_content = read_file()
    print(f"✅ 文件已读取 ({len(md_content)} 字符)")
    
    # 2. 创建邮件内容
    print("\n2. 创建邮件内容...")
    subject, body = create_email_content(md_content)
    print(f"✅ 邮件内容已创建")
    
    # 3. 发送邮件
    print("\n3. 发送邮件...")
    success = send_email(subject, body)
    
    if success:
        print("\n✅ 完成！邮件已发送到微信绑定邮箱")
        print(f"   收件人：{RECIPIENT}")
        print(f"   主题：{subject}")
    else:
        print("\n❌ 发送失败")
        print("\n配置方法：")
        print("1. 创建 ~/.taiyi/wechat-assistant/config.json")
        print("2. 添加 sender_email 和 smtp_password")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
