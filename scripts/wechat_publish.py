#!/usr/bin/env python3
"""
微信公众号发布脚本 - Token 方式
支持代理绕过 IP 白名单限制

用法：
    python3 wechat_publish.py --markdown content/wechat_first_post.md --title "文章标题"
"""

import os
import sys
import json
import requests
import markdown
from pathlib import Path
from datetime import datetime

# 微信凭证（从环境变量读取）
APPID = os.getenv("WECHAT_APPID", "wx720a4c489fec9df3")
APPSECRET = os.getenv("WECHAT_APP_SECRET", "94066275ad79af78b29b3c5f1ef7660c")

# 代理配置（可选，用于绕过 IP 白名单）
PROXY = os.getenv("WECHAT_PROXY", "")  # 例如：http://proxy.example.com:7890

# 微信 API 端点
API_BASE = "https://api.weixin.qq.com"


def get_access_token():
    """获取 access_token"""
    url = f"{API_BASE}/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": APPID,
        "secret": APPSECRET
    }
    
    proxies = {"http": PROXY, "https": PROXY} if PROXY else {}
    
    response = requests.get(url, params=params, proxies=proxies)
    data = response.json()
    
    if "access_token" in data:
        print(f"✓ Token 获取成功：{data['access_token'][:16]}...")
        return data["access_token"]
    else:
        print(f"✗ Token 获取失败：{data}")
        sys.exit(1)


def upload_image(access_token, image_path):
    """上传图片到微信素材库"""
    url = f"{API_BASE}/cgi-bin/material/add_material"
    params = {
        "access_token": access_token,
        "type": "image"
    }
    
    with open(image_path, "rb") as f:
        files = {"media": f}
        proxies = {"http": PROXY, "https": PROXY} if PROXY else {}
        response = requests.post(url, params=params, files=files, proxies=proxies)
    
    data = response.json()
    
    if "media_id" in data:
        print(f"✓ 图片上传成功：{data['media_id']}")
        return data["media_id"]
    else:
        print(f"✗ 图片上传失败：{data}")
        return None


def create_draft(access_token, title, content, thumb_media_id, summary="", author=""):
    """创建草稿箱文章"""
    url = f"{API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    # 构建文章数据
    articles = {
        "title": title,
        "author": author,
        "digest": summary,
        "content": content,
        "thumb_media_id": thumb_media_id,
        "show_cover_pic": 1,
        "need_open_comment": 0,  # 关闭评论
        "only_fans_can_comment": 0
    }
    
    data = {
        "articles": [articles]
    }
    
    proxies = {"http": PROXY, "https": PROXY} if PROXY else {}
    response = requests.post(url, params=params, json=data, proxies=proxies)
    result = response.json()
    
    if "media_id" in result:
        print(f"✓ 草稿创建成功：{result['media_id']}")
        return result["media_id"]
    else:
        print(f"✗ 草稿创建失败：{result}")
        return None


def markdown_to_html(md_path):
    """将 Markdown 转换为 HTML"""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # 使用 markdown 库转换
    html = markdown.markdown(
        md_content,
        extensions=["extra", "codehilite", "toc"],
        output_format="html5"
    )
    
    # 添加简单的样式
    styled_html = f"""
    <section>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
            h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
            h2 {{ color: #555; margin-top: 30px; }}
            code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
            pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background: #4CAF50; color: white; }}
            blockquote {{ border-left: 4px solid #4CAF50; margin: 20px 0; padding-left: 20px; color: #666; }}
        </style>
        {html}
    </section>
    """
    
    return styled_html


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号发布脚本")
    parser.add_argument("--markdown", required=True, help="Markdown 文件路径")
    parser.add_argument("--title", required=True, help="文章标题（最多 64 字符）")
    parser.add_argument("--summary", default="", help="文章摘要")
    parser.add_argument("--author", default="太一", help="作者名")
    parser.add_argument("--cover", default="", help="封面图片路径")
    parser.add_argument("--proxy", default="", help="代理地址（可选）")
    
    args = parser.parse_args()
    
    # 更新代理配置
    global PROXY
    if args.proxy:
        PROXY = args.proxy
    
    print("=" * 60)
    print("微信公众号发布脚本")
    print("=" * 60)
    print(f"标题：{args.title}")
    print(f"Markdown: {args.markdown}")
    print(f"代理：{PROXY if PROXY else '无'}")
    print("=" * 60)
    
    # 1. 获取 Token
    print("\n[1/4] 获取 access_token...")
    access_token = get_access_token()
    
    # 2. 转换 Markdown 为 HTML
    print("\n[2/4] 转换 Markdown 为 HTML...")
    html_content = markdown_to_html(args.markdown)
    print(f"✓ HTML 生成成功，长度：{len(html_content)} 字符")
    
    # 3. 上传封面图
    print("\n[3/4] 上传封面图片...")
    cover_path = args.cover if args.cover else "content/images/cover.jpg"
    if os.path.exists(cover_path):
        thumb_media_id = upload_image(access_token, cover_path)
        if not thumb_media_id:
            print("⚠️ 封面图上传失败，尝试继续...")
            thumb_media_id = "default_cover"  # 使用默认
    else:
        print(f"⚠️ 封面图不存在：{cover_path}")
        thumb_media_id = "default_cover"
    
    # 4. 创建草稿
    print("\n[4/4] 创建草稿箱文章...")
    media_id = create_draft(
        access_token=access_token,
        title=args.title,
        content=html_content,
        thumb_media_id=thumb_media_id,
        summary=args.summary,
        author=args.author
    )
    
    # 完成
    print("\n" + "=" * 60)
    if media_id:
        print(f"✅ 发布成功！")
        print(f"草稿 ID: {media_id}")
        print(f"登录 https://mp.weixin.qq.com 查看草稿箱")
    else:
        print(f"❌ 发布失败，请检查错误信息")
    print("=" * 60)


if __name__ == "__main__":
    main()
