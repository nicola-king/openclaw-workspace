#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书账号主页截图工具
太一 AGI 标准小红书账号自动化脚本

用法:
    python3 scripts/xiaohongshu-profile.py <账号 ID 或主页 URL> [输出目录]
    
示例:
    python3 scripts/xiaohongshu-profile.py https://www.xiaohongshu.com/user/profile/5d3c7b8a00000000120387fa
    python3 scripts/xiaohongshu-profile.py 5d3c7b8a00000000120387fa /tmp
"""

from playwright.sync_api import sync_playwright
import sys
import os
import re
from datetime import datetime

def extract_user_id(url_or_id: str) -> str:
    """从 URL 或 ID 中提取用户 ID"""
    # 如果已经是 ID 格式，直接返回
    if re.match(r'^[a-f0-9]{24}$', url_or_id):
        return url_or_id
    
    # 从 URL 中提取 ID
    patterns = [
        r'user/profile/([a-f0-9]+)',
        r'user/([a-f0-9]+)',
        r'/([a-f0-9]{24})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    # 如果是用户名（@xxx 格式）
    if url_or_id.startswith('@'):
        print(f'⚠️ 用户名搜索功能暂不支持，请使用用户 ID')
        return None
    
    return url_or_id

def xiaohongshu_profile(url_or_id: str, output_dir: str = "/tmp"):
    """
    访问小红书账号主页并截图
    
    Args:
        url_or_id: 账号 ID 或主页 URL
        output_dir: 输出目录
    """
    print('🚀 小红书账号截图开始...\n')
    
    # 提取用户 ID
    user_id = extract_user_id(url_or_id)
    if not user_id:
        print('❌ 无法解析用户 ID')
        return None
    
    profile_url = f'https://www.xiaohongshu.com/user/profile/{user_id}'
    print(f'👤 用户 ID: {user_id}')
    print(f'🔗 主页：{profile_url}\n')
    
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
                locale='zh-CN'
            )
            
            page = context.new_page()
            
            # 注入反检测脚本
            page.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
            ''')
            
            # 访问账号主页
            print(f'🔗 访问：{profile_url}')
            try:
                page.goto(profile_url, wait_until='domcontentloaded', timeout=30000)
            except Exception as e:
                print(f'⚠️ 页面加载超时，尝试继续... ({str(e)})')
            
            # 等待内容加载
            print('⏳ 等待内容加载...')
            page.wait_for_timeout(5000)
            
            # 获取页面标题
            title = page.title()
            print(f'📊 页面标题：{title}')
            
            # 尝试获取账号信息
            try:
                # 查找用户名
                username_elem = page.query_selector('span.user-name, .user-name, h1')
                if username_elem:
                    username = username_elem.inner_text()
                    print(f'👤 用户名：{username}')
                
                # 查找粉丝数
                fans_elem = page.query_selector('span.fans-num, .fans-count')
                if fans_elem:
                    fans = fans_elem.inner_text()
                    print(f'📊 粉丝数：{fans}')
                
            except Exception as e:
                print(f'ℹ️  无法提取账号信息：{str(e)}')
            
            # 截图
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            filename = f'xiaohongshu-profile-{user_id}-{timestamp}.png'
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
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    url_or_id = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp"
    
    xiaohongshu_profile(url_or_id, output_dir)
