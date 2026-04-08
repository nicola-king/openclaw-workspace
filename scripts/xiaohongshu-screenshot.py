#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书截图工具 - 已登录状态
太一 AGI 标准小红书自动化脚本

前提：小红书已授权登录（浏览器 Cookie 已保存）

用法:
    python3 scripts/xiaohongshu-screenshot.py [输出目录]
    
示例:
    python3 scripts/xiaohongshu-screenshot.py /tmp
"""

from playwright.sync_api import sync_playwright
import sys
import os
from datetime import datetime

def xiaohongshu_screenshot(output_dir: str = "/tmp"):
    """
    访问小红书首页并截图（已登录状态）
    
    Args:
        output_dir: 输出目录
    """
    print('🚀 小红书截图开始...\n')
    
    try:
        with sync_playwright() as p:
            # 启动浏览器 - 带反检测配置
            print('🌐 启动浏览器...')
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            
            # 创建上下文 - 模拟真实用户 + 保持登录状态
            print('📄 创建页面 (保持登录状态)...')
            context = browser.new_context(
                viewport={'width': 1200, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='zh-CN',
                # 保持 Cookie 和 LocalStorage
                storage_state=None  # 如有保存的登录状态可在此指定
            )
            
            page = context.new_page()
            
            # 注入反检测脚本
            page.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
            ''')
            
            # 访问小红书
            print('🔗 访问：https://www.xiaohongshu.com')
            try:
                page.goto('https://www.xiaohongshu.com', wait_until='domcontentloaded', timeout=30000)
            except Exception as e:
                print(f'⚠️ 页面加载超时，尝试继续... ({str(e)})')
            
            # 等待内容加载
            print('⏳ 等待内容加载...')
            page.wait_for_timeout(5000)
            
            # 获取页面标题
            title = page.title()
            print(f'📊 页面标题：{title}')
            
            # 检查是否登录
            try:
                # 尝试查找登录用户的头像或用户名
                user_avatar = page.query_selector('img[alt="用户头像"]')
                if user_avatar:
                    print('✅ 检测到已登录状态')
                else:
                    print('⚠️ 未检测到登录状态，可能需要手动登录')
            except:
                print('ℹ️  无法检测登录状态')
            
            # 截图
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            filename = f'xiaohongshu-{timestamp}.png'
            screenshot_path = os.path.join(output_dir, filename)
            
            print('📸 执行截图...')
            page.screenshot(path=screenshot_path, full_page=True)
            
            # 文件信息
            size_mb = os.path.getsize(screenshot_path) / 1024 / 1024
            from PIL import Image
            img = Image.open(screenshot_path)
            
            print(f'\n✅ 截图完成！')
            print(f'📁 保存位置：{screenshot_path}')
            print(f'📦 文件大小：{size_mb:.2f} MB')
            print(f'🖼️  图片尺寸：{img.size[0]} x {img.size[1]} px')
            
            browser.close()
            
            return screenshot_path
            
    except Exception as e:
        print(f'❌ 执行失败：{str(e)}')
        if 'net::ERR' in str(e):
            print('\n💡 提示：网络连接问题，可能需要代理')
        return None

if __name__ == '__main__':
    # 命令行参数解析
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
    
    xiaohongshu_screenshot(output_dir)
