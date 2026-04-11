#!/usr/bin/env python3
"""
📱 微信公众号自动发布脚本

短期方案：邮件发送 + 手动发布
中期方案：API 自动发布 + 定时任务

作者：太一 AGI
创建：2026-04-11
"""

import os
import sys
import json
import smtplib
import requests
import argparse
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class WechatAutoPublisher:
    """微信公众号自动发布器"""
    
    def __init__(self, config_path: str = None):
        """初始化发布器"""
        self.config_path = config_path or "/home/nicola/.openclaw/workspace-taiyi/config/wechat.json"
        self.config = self._load_config()
        
        print("📱 微信公众号自动发布器已初始化")
        print(f"   公众号：{self.config.get('official_account', {}).get('name', '未配置')}")
        print()
    
    def _load_config(self) -> dict:
        """加载配置"""
        config_file = Path(self.config_path)
        if not config_file.exists():
            print(f"⚠️  配置文件不存在：{config_file}")
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_access_token(self) -> str:
        """获取微信公众号访问令牌"""
        app_id = self.config['official_account']['app_id']
        app_secret = self.config['official_account']['app_secret']
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": app_id,
            "secret": app_secret
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'access_token' in data:
            print(f"✅ 访问令牌已获取 (有效期：{data.get('expires_in', 7200)}秒)")
            return data['access_token']
        else:
            print(f"❌ 获取访问令牌失败：{data}")
            return None
    
    def send_email_draft(self, article: dict) -> bool:
        """
        短期方案：发送邮件草稿
        
        Args:
            article: 文章字典 {title, content, cover_suggestion}
        
        Returns:
            bool: 发送成功与否
        """
        print("📧 发送邮件草稿...")
        
        smtp_config = self.config.get('smtp', {})
        if not smtp_config.get('enabled', False):
            print("⚠️  SMTP 未启用")
            return False
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = smtp_config['sender_email']
        msg['To'] = smtp_config['recipient_email']
        msg['Subject'] = f"【公众号草稿】{article.get('title', '新文章')}"
        
        # 邮件正文
        body = f"""
# {article.get('title', '新文章')}

**摘要**: {article.get('summary', '')}

**封面建议**: {article.get('cover_suggestion', '')}

---

{article.get('content', '')}

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**发布状态**: ⏳ 待发布

操作步骤:
1. 复制以上内容
2. 登录公众号后台：https://mp.weixin.qq.com/
3. 创建新图文 → 粘贴内容
4. 设置封面图
5. 发布/定时发布
"""
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 发送邮件
        try:
            server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
            server.starttls()
            server.login(smtp_config['sender_email'], smtp_config['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ 邮件草稿已发送：{smtp_config['recipient_email']}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败：{e}")
            return False
    
    def create_draft_via_api(self, article: dict) -> str:
        """
        中期方案：通过 API 创建草稿
        
        Args:
            article: 文章字典 {title, content, thumb_media_id}
        
        Returns:
            str: 草稿 ID
        """
        print("📝 通过 API 创建草稿...")
        
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
        
        payload = {
            "articles": [{
                "title": article.get('title', '新文章'),
                "content": article.get('content', ''),
                "thumb_media_id": article.get('thumb_media_id', ''),
                "author": "SAYELF",
                "show_cover_pic": 1
            }]
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if 'media_id' in data:
            print(f"✅ 草稿已创建：{data['media_id']}")
            return data['media_id']
        else:
            print(f"❌ 创建草稿失败：{data}")
            return None
    
    def schedule_publish(self, media_id: str, publish_time: str) -> bool:
        """
        定时发布
        
        Args:
            media_id: 草稿媒体 ID
            publish_time: 发布时间 (格式：2026-04-11 18:00)
        
        Returns:
            bool: 成功与否
        """
        print(f"⏰ 设置定时发布：{publish_time}")
        
        access_token = self.get_access_token()
        if not access_token:
            return False
        
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
        
        # 解析发布时间
        dt = datetime.strptime(publish_time, "%Y-%m-%d %H:%M")
        
        payload = {
            "media_id": media_id,
            "preview": False,
            "send_time": dt.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get('errcode', 1) == 0:
            print(f"✅ 定时发布已设置：{publish_time}")
            return True
        else:
            print(f"❌ 定时发布失败：{data}")
            return False
    
    def get_metrics(self, begin_date: str, end_date: str) -> dict:
        """
        获取文章数据
        
        Args:
            begin_date: 开始日期 (格式：20260411)
            end_date: 结束日期 (格式：20260411)
        
        Returns:
            dict: 数据统计
        """
        print(f"📊 获取文章数据：{begin_date} ~ {end_date}")
        
        access_token = self.get_access_token()
        if not access_token:
            return {}
        
        url = "https://api.weixin.qq.com/datacube/getarticlesummary"
        params = {
            "access_token": access_token,
            "begin_date": begin_date,
            "end_date": end_date
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'list' in data:
            print(f"✅ 获取到 {len(data['list'])} 篇文章数据")
            return data['list']
        else:
            print(f"❌ 获取数据失败：{data}")
            return {}
    
    def save_metrics(self, metrics: list, output_file: str):
        """保存数据到文件"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 数据已保存：{output_file}")
    
    def generate_article(self, topic: str) -> dict:
        """生成文章 (简化版)"""
        articles = {
            "AI 管家": {
                "title": "我用 AI 管家，把重复工作都交给它了",
                "summary": "不是替代你，是帮你把时间花在值得的事上",
                "content": "# 我用 AI 管家，把重复工作都交给它了\n\n这里是文章内容...",
                "cover_suggestion": "AI 机器人 + 办公桌 + 温馨风格"
            }
        }
        
        return articles.get(topic, {
            "title": topic,
            "summary": f"关于{topic}的深度分享",
            "content": f"# {topic}\n\n这里是文章内容...",
            "cover_suggestion": "与主题相关的图片"
        })


def main():
    """主函数"""
    print("="*60)
    print("📱 微信公众号自动发布器")
    print("="*60)
    
    parser = argparse.ArgumentParser(description='微信公众号自动发布器')
    parser.add_argument('--topic', type=str, help='文章主题')
    parser.add_argument('--mode', type=str, default='email', choices=['email', 'api'], help='发布模式')
    parser.add_argument('--publish-time', type=str, help='定时发布时间 (YYYY-MM-DD HH:MM)')
    parser.add_argument('--metrics', action='store_true', help='获取文章数据')
    
    args = parser.parse_args()
    
    # 初始化发布器
    publisher = WechatAutoPublisher()
    
    if args.metrics:
        # 获取文章数据
        print("\n1. 获取文章数据...")
        today = datetime.now().strftime("%Y%m%d")
        metrics = publisher.get_metrics(today, today)
        
        if metrics:
            output_file = f"/home/nicola/.openclaw/workspace/content/wechat-metrics-{today}.json"
            publisher.save_metrics(metrics, output_file)
        
        return 0
    
    # 生成文章
    print("\n1. 生成文章...")
    topic = args.topic or "AI 管家"
    article = publisher.generate_article(topic)
    print(f"   标题：{article['title']}")
    print(f"   摘要：{article['summary']}")
    
    # 发布
    print(f"\n2. 发布模式：{args.mode}")
    
    if args.mode == 'email':
        # 短期方案：邮件发送
        success = publisher.send_email_draft(article)
    else:
        # 中期方案：API 发布
        media_id = publisher.create_draft_via_api(article)
        
        if media_id and args.publish_time:
            publisher.schedule_publish(media_id, args.publish_time)
    
    print("\n✅ 微信公众号自动发布器测试完成!")
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
