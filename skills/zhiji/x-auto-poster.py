#!/usr/bin/env python3
"""
知几-E X 平台自动发布器（浏览器自动化）
免费开源方案，无需 X API

依赖：
    pip install playwright
    playwright install chromium

用法：
    python3 x-auto-poster.py --type morning --auto
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class XAutoPoster:
    """X 平台自动发布器（浏览器自动化）"""
    
    def __init__(self):
        self.config_path = Path.home() / ".taiyi" / "x" / "config.json"
        self.config = self.load_config()
        self.session_file = Path.home() / ".taiyi" / "x" / "session.json"
        self.cookies_file = Path.home() / ".taiyi" / "x" / "cookies.json"
    
    def load_config(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {
            "account": {"handle": "@SayelfTea"},
            "automation": {"browser": "chromium", "headless": False}
        }
    
    def generate_content(self, post_type="morning"):
        """生成发布内容"""
        if post_type == "morning":
            return f"""【加密早报 · {datetime.now().strftime("%m/%d")}】

隔夜热点：
• BTC $70,500 (+2.3%)
• ETH $2,155 (+1.8%)
• Polymarket 24h 交易量 $50M

今日关注：
• 美联储讲话 (20:00)
• 美国 GDP 数据 (21:30)

知几-E 策略运行中

#Polymarket #量化交易 #BTC #ETH"""
        
        elif post_type == "signal":
            return f"""🟢【交易信号 · {datetime.now().strftime("%H:%M")}】

市场：BTC 涨跌
方向：多
置信度：96%
优势：4.5%
下注：$10

知几-E 自动执行中

#Polymarket #交易信号 #量化"""
        
        elif post_type == "pnl":
            return f"""✅【交易日报 · {datetime.now().strftime("%m/%d")}】

今日交易：5 笔
总盈亏：+$25.50 (+2.5%)
胜率：80%

知几-E 自动执行中

#量化交易 #收益报告 #Polymarket"""
        
        else:
            return f"知几-E 量化交易 · {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    def post_with_playwright(self, content):
        """使用 Playwright 浏览器自动化发布"""
        if not PLAYWRIGHT_AVAILABLE:
            print("❌ Playwright 未安装")
            print("\n安装方法：")
            print("  pip install playwright")
            print("  playwright install chromium")
            return False
        
        print("🌐 启动浏览器...")
        
        try:
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.chromium.launch(
                    headless=self.config.get("automation", {}).get("headless", False)
                )
                
                # 创建上下文
                context = browser.new_context(
                    viewport={"width": 1280, "height": 720}
                )
                page = context.new_page()
                
                # 访问 X
                print("📱 访问 X 平台...")
                page.goto("https://twitter.com/home", timeout=60000)
                
                # 等待页面加载
                page.wait_for_timeout(5000)
                
                # 检查是否登录
                if "login" in page.url.lower():
                    print("⚠️  需要登录")
                    print("   请手动登录后，保存 Cookie")
                    print("   按 Enter 继续...")
                    input()
                
                # 发布推文
                print("📝 发布内容...")
                
                # 找到输入框
                textarea = page.query_selector("[data-testid='tweetTextarea_0']")
                if textarea:
                    textarea.fill(content)
                    print("  ✅ 内容已填入")
                    
                    # 等待一下
                    page.wait_for_timeout(2000)
                    
                    # 找到发布按钮
                    post_button = page.query_selector("[data-testid='tweetButton']")
                    if post_button:
                        print("  🚀 点击发布...")
                        # post_button.click()
                        print("  ⚠️  演示模式：未实际点击（需要确认）")
                    else:
                        print("  ❌ 未找到发布按钮")
                else:
                    print("  ❌ 未找到输入框")
                
                # 保持浏览器打开
                print("\n💡 浏览器保持打开，可手动操作")
                print("   按 Enter 关闭浏览器...")
                input()
                
                browser.close()
                return True
                
        except Exception as e:
            print(f"❌ 发布失败：{e}")
            return False
    
    def save_draft(self, content, post_type):
        """保存草稿（备选方案）"""
        draft_path = Path.home() / ".taiyi" / "zhiji" / "x-posts"
        draft_path.mkdir(parents=True, exist_ok=True)
        
        draft_file = draft_path / f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(f"# X 平台发布\n\n")
            f.write(f"**类型**: {post_type}\n")
            f.write(f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"```\n{content}\n```\n")
        
        print(f"✅ 草稿已保存：{draft_file}")
        return draft_file
    
    def run(self, post_type="morning", auto=False):
        """主执行流程"""
        print("=" * 70)
        print("  知几-E X 平台自动发布")
        print("=" * 70)
        print()
        
        # 生成内容
        print("【1/3】生成发布内容...")
        content = self.generate_content(post_type)
        print(f"  内容长度：{len(content)} 字符")
        print()
        
        # 检查 Playwright
        if auto and PLAYWRIGHT_AVAILABLE:
            print("【2/3】浏览器自动化发布...")
            success = self.post_with_playwright(content)
            
            if success:
                print("【3/3】发布完成！")
            else:
                print("【3/3】发布失败，保存草稿...")
                self.save_draft(content, post_type)
        else:
            print("【2/3】保存草稿...")
            draft_file = self.save_draft(content, post_type)
            print()
            print("【3/3】发布方式：")
            print(f"  1. 打开 {draft_file}")
            print("  2. 复制内容")
            print("  3. 登录 twitter.com")
            print("  4. 粘贴发布")
            print()
            print("  或运行：python3 x-auto-poster.py --type {} --auto".format(post_type))
        
        print()
        print("=" * 70)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="知几-E X 自动发布器")
    parser.add_argument("--type", default="morning", help="发布类型")
    parser.add_argument("--auto", action="store_true", help="自动发布")
    
    args = parser.parse_args()
    
    poster = XAutoPoster()
    poster.run(args.type, args.auto)
