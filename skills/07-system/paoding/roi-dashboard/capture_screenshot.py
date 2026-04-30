#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
庖丁 ROI Dashboard 截图工具
捕获 Web Dashboard 可视化效果
"""

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 访问 ROI Dashboard
    print("🦞 正在访问 ROI Dashboard...")
    page.goto("http://localhost:8080", wait_until="networkidle")
    
    # 等待图表加载
    time.sleep(2)
    
    # 截图
    screenshot_path = "/home/nicola/.openclaw/workspace/roi-dashboard-screenshot.png"
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"✅ 截图已保存：{screenshot_path}")
    
    # 获取页面标题
    title = page.title()
    print(f"📊 页面标题：{title}")
    
    browser.close()
