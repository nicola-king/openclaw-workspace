#!/usr/bin/env python3
"""
X 平台登录脚本（仅首次运行）
用法：python3 x-login.py
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import json

def login_to_x():
    """登录 X 并保存浏览器配置"""
    user_data_dir = Path.home() / ".taiyi" / "x" / "browser-profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("  X 平台登录工具（首次配置）")
    print("=" * 70)
    print()
    print("📱 浏览器即将打开...")
    print()
    print("操作步骤：")
    print("  1. 在打开的浏览器中访问 twitter.com")
    print("  2. 登录你的 Twitter 账号 (@SayelfTea)")
    print("  3. 登录成功后，关闭浏览器窗口")
    print()
    print("🚀 浏览器将在 3 秒后打开...")
    import time
    time.sleep(3)
    
    with sync_playwright() as p:
        # 启动持久化浏览器
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # 访问 Twitter
        print("🌐 访问 Twitter...")
        page.goto("https://twitter.com/home", timeout=60000)
        
        print()
        print("✅ 浏览器已打开")
        print("   请在浏览器中登录 Twitter")
        print("   登录后关闭浏览器窗口...")
        
        # 等待浏览器关闭
        try:
            context.pages[0].wait_for_event("close", timeout=300000)
        except:
            pass
        
        context.close()
    
    print()
    print("=" * 70)
    print("  ✅ 登录配置已保存！")
    print("=" * 70)
    print()
    print(f"浏览器配置：{user_data_dir}")
    print()
    print("下次运行自动发布时将自动使用此登录状态。")
    print()

if __name__ == "__main__":
    login_to_x()
