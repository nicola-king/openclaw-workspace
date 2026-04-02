#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 网页浏览工具
太一 AGI 标准网页自动化脚本

用法:
    python3 playwright-browser.py <URL> [操作]
    
示例:
    python3 playwright-browser.py https://www.xiaohongshu.com 截图
    python3 playwright-browser.py https://github.com 导航
"""

from playwright.sync_api import sync_playwright
import sys
import os
from datetime import datetime

def browse(url: str, action: str = "截图", output_dir: str = "/tmp"):
    """
    使用 Playwright 访问网页并执行操作
    
    Args:
        url: 目标网址
        action: 操作类型 (截图/导航/观察)
        output_dir: 输出目录
    """
    print(f'🚀 Playwright 浏览开始...')
    print(f'🔗 目标：{url}')
    print(f'🎯 操作：{action}\n')
    
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
            
            # 创建上下文 - 模拟真实用户
            print('📄 创建页面...')
            context = browser.new_context(
                viewport={'width': 1200, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='zh-CN'
            )
            
            page = context.new_page()
            
            # 注入反检测脚本
            page.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
            ''')
            
            # 访问网页
            print(f'🔗 访问：{url}')
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
            except Exception as e:
                print(f'⚠️ 页面加载超时，尝试继续... ({str(e)})')
            
            # 等待内容加载
            print('⏳ 等待内容加载...')
            page.wait_for_timeout(3000)
            
            # 获取页面标题
            title = page.title()
            print(f'📊 页面标题：{title}')
            
            # 执行操作
            if action == "截图":
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                filename = f'screenshot-{timestamp}.png'
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
                
                return screenshot_path
                
            elif action == "导航":
                print('✅ 导航完成！')
                return True
                
            elif action == "观察":
                print('👀 观察页面...')
                content = page.content()
                print(f'📊 页面 HTML 长度：{len(content)} 字符')
                return content
                
            else:
                print(f'⚠️ 未知操作：{action}')
                return None
            
            browser.close()
            
    except Exception as e:
        print(f'❌ 执行失败：{str(e)}')
        if 'net::ERR' in str(e):
            print('\n💡 提示：网络连接问题，可能需要代理')
        return None

if __name__ == '__main__':
    # 命令行参数解析
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    url = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "截图"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "/tmp"
    
    browse(url, action, output_dir)
