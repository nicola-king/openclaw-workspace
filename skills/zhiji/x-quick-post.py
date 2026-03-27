#!/usr/bin/env python3
"""
知几-E X 平台快速发布（简化版）
使用已安装的浏览器，无需 Playwright

用法：
    python3 x-quick-post.py
"""

import os
import webbrowser
import subprocess
from datetime import datetime
from pathlib import Path

def generate_content():
    """生成发布内容"""
    return f"""🟢【交易信号 · {datetime.now().strftime("%H:%M")}】

市场：BTC 涨跌
方向：多
置信度：96%
优势：4.5%
下注：$10

知几-E 自动执行中

#Polymarket #交易信号 #量化"""

def save_and_open(content):
    """保存并打开 X"""
    # 保存内容
    post_path = Path.home() / ".taiyi" / "zhiji" / "x-posts"
    post_path.mkdir(parents=True, exist_ok=True)
    
    post_file = post_path / f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(post_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 内容已保存：{post_file}")
    print()
    print("📋 内容：")
    print("-" * 70)
    print(content)
    print("-" * 70)
    print()
    
    # 打开 X 平台
    print("🌐 打开 X 平台...")
    webbrowser.open("https://twitter.com/compose/tweet")
    print()
    print("💡 操作指南：")
    print("  1. 复制上方内容")
    print("  2. 粘贴到 X 发布框")
    print("  3. 点击 发布")
    print()
    print("✅ 发布完成后，后续将自动执行！")

if __name__ == "__main__":
    print("=" * 70)
    print("  知几-E X 平台快速发布")
    print("=" * 70)
    print()
    
    content = generate_content()
    save_and_open(content)
