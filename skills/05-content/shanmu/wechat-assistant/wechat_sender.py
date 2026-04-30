#!/usr/bin/env python3
"""
山木 - 公众号助手
自动撰写 + 排版 + 发送邮件，复制粘贴即可发布

用法：
    python3 wechat_sender.py --topic "AI 管家" --recipient 285915125@qq.com
"""

import os
import sys
import json
import smtplib
import argparse
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class WechatAssistant:
    """公众号助手"""
    
    def __init__(self):
        self.config_path = Path.home() / ".taiyi" / "wechat-assistant" / "config.json"
        self.config = self.load_config()
        
    def load_config(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {
            "recipient_email": "285915125@qq.com",
            "sender_email": "",
            "smtp_password": "",
            "publish_guide": True
        }
    
    def generate_article(self, topic, style="科普"):
        """生成文章（简化版，实际可调用 AI）"""
        articles = {
            "AI 管家": {
                "titles": [
                    "我用 AI 管家，把重复工作都交给它了",
                    "AI 管家：把重复工作交给它，你专注值得的事",
                    "打工人必备！这个 AI 管家让我每天少工作 2 小时"
                ],
                "summary": "不是替代你，是帮你把时间花在值得的事上",
                "content": self.get_article_content(topic),
                "cover_suggestion": "AI 机器人 + 办公桌 + 温馨风格"
            }
        }
        return articles.get(topic, {
            "titles": [f"{topic}"],
            "summary": f"关于{topic}的深度分享",
            "content": f"# {topic}\n\n这里是文章内容...",
            "cover_suggestion": "与主题相关的图片"
        })
    
    def get_article_content(self, topic):
        """获取文章内容（从文件读取）"""
        content_dir = Path.home() / ".openclaw" / "workspace" / "content"
        
        # 查找匹配的文章
        if "AI 管家" in topic:
            article_path = content_dir / "wechat_first_post_v2.md"
        elif "7 个场景" in topic:
            article_path = content_dir / "wechat_7_scenarios.md"
        else:
            return None
        
        if article_path.exists():
            with open(article_path, "r", encoding="utf-8") as f:
                return f.read()
        return None
    
    def format_for_wechat(self, content):
        """格式化为微信公众号格式"""
        # 将 Markdown 转换为简单 HTML
        html = content
        html = html.replace("# ", "<h1>")
        html = html.replace("## ", "<h2>")
        html = html.replace("### ", "<h3>")
        html = html.replace("\n", "<br>")
        html = html.replace("- ", "• ")
        
        return f"""
<section>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #4CAF50; color: white; }}
        blockquote {{ border-left: 4px solid #4CAF50; padding-left: 20px; color: #666; }}
    </style>
    {html}
</section>
"""
    
    def send_email(self, topic):
        """发送邮件"""
        # 生成文章
        article = self.generate_article(topic)
        
        if not article["content"]:
            print(f"❌ 未找到文章：{topic}")
            return False
        
        # 格式化
        html_content = self.format_for_wechat(article["content"])
        
        # 创建邮件
        msg = MIMEMultipart()
        msg["From"] = self.config.get("sender_email", "山木公众号助手")
        msg["To"] = self.config.get("recipient_email")
        msg["Subject"] = f"📝 公众号文章就绪：{topic}"
        
        # 邮件正文
        body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .highlight {{ background: #e8f5e9; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0; }}
        .step {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; }}
        .copy-btn {{ background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
    </style>
</head>
<body>

<h1>📝 公众号文章就绪</h1>
<p><strong>主题：</strong>{topic}</p>
<p><strong>生成时间：</strong>{datetime.now().strftime("%Y-%m-%d %H:%M")}</p>

<div class="highlight">
<h2>📋 快速发布指南</h2>
<div class="step">1️⃣ 复制下方「文章标题」（3 选 1）</div>
<div class="step">2️⃣ 登录 <a href="https://mp.weixin.qq.com">公众号后台</a></div>
<div class="step">3️⃣ 内容与图片 → 新建图文 → 粘贴标题</div>
<div class="step">4️⃣ 复制「文章正文」→ 粘贴到编辑器</div>
<div class="step">5️⃣ 上传封面图（建议：{article['cover_suggestion']}）</div>
<div class="step">6️⃣ 填写摘要：{article['summary']}</div>
<div class="step">7️⃣ 预览 → 发布</div>
<p><strong>全程约 5 分钟</strong></p>
</div>

<h2>📌 文章标题（3 选 1）</h2>
<ul>
    {"</li><li>".join(article['titles'])}
</ul>

<h2>📄 文章摘要</h2>
<p>{article['summary']}</p>

<h2>📝 文章正文</h2>
<div style="background: #f9f9f9; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
{html_content}
</div>

<h2>🎨 封面图建议</h2>
<p>{article['cover_suggestion']}</p>
<p>可使用 AI 生成或从免费图库选择：</p>
<ul>
    <li><a href="https://unsplash.com">Unsplash</a> - 免费高清图片</li>
    <li><a href="https://www.pexels.com">Pexels</a> - 免费素材</li>
    <li><a href="https://pixabay.com">Pixabay</a> - 免费图片</li>
</ul>

<div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px;">
<p><strong>山木公众号助手</strong> | 太一军团</p>
<p>有问题？公众号：SAYELF 山野精灵</p>
</div>

</body>
</html>
"""
        
        msg.attach(MIMEText(body, "html", "utf-8"))
        
        # 发送
        try:
            if not self.config.get("sender_email") or not self.config.get("smtp_password"):
                print("❌ 未配置 SMTP 凭证")
                print("\n配置方法：")
                print("1. 创建 ~/.taiyi/wechat-assistant/config.json")
                print("2. 添加 sender_email 和 smtp_password")
                print("\n示例配置：")
                print(json.dumps({
                    "sender_email": "your-qq-email@qq.com",
                    "smtp_password": "your-smtp-auth-code",
                    "recipient_email": "285915125@qq.com"
                }, indent=2))
                return False
            
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(self.config["sender_email"], self.config["smtp_password"])
            server.sendmail(self.config["sender_email"], [self.config["recipient_email"]], msg.as_string())
            server.quit()
            
            print(f"✅ 邮件发送成功！")
            print(f"收件人：{self.config['recipient_email']}")
            print(f"主题：{topic}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败：{e}")
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="山木公众号助手")
    parser.add_argument("--topic", required=True, help="文章主题")
    parser.add_argument("--recipient", default="285915125@qq.com", help="收件人邮箱")
    
    args = parser.parse_args()
    
    assistant = WechatAssistant()
    if args.recipient:
        assistant.config["recipient_email"] = args.recipient
    assistant.send_email(args.topic)
