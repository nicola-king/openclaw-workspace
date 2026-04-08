#!/usr/bin/env python3
"""
Browser Automation Skill - 太一 AGI v5.0
基于 Playwright 的智能浏览器自动化
"""

from playwright.sync_api import sync_playwright, TimeoutError
import json
import os
import time
from pathlib import Path

class BrowserAutomation:
    """浏览器自动化类"""
    
    def __init__(self, headless=False, slow_mo=100):
        """
        初始化浏览器
        
        Args:
            headless: 是否无头模式
            slow_mo: 操作延迟（毫秒），便于观察
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.current_url = None
        
    def start(self):
        """启动浏览器"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo,
                args=[
                    '--disable-features=Vulkan',
                    '--ozone-platform=x11',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--window-size=1920,1080'
                ]
            )
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            self.page = self.context.new_page()
            print("✅ 浏览器已启动")
            return True
        except Exception as e:
            print(f"❌ 启动失败：{e}")
            return False
            
    def open(self, url, timeout=30000):
        """
        打开网页
        
        Args:
            url: 网址
            timeout: 超时时间（毫秒）
        """
        if not self.browser:
            self.start()
        try:
            self.page.goto(url, wait_until='networkidle', timeout=timeout)
            self.current_url = url
            title = self.page.title()
            print(f"✅ 已打开：{url}")
            print(f"   标题：{title}")
            return True
        except TimeoutError:
            print(f"⚠️ 加载超时，但继续：{url}")
            return True
        except Exception as e:
            print(f"❌ 打开失败：{e}")
            return False
            
    def close(self):
        """关闭浏览器"""
        try:
            if self.browser:
                self.browser.close()
                self.playwright.stop()
                print("✅ 浏览器已关闭")
            return True
        except Exception as e:
            print(f"❌ 关闭失败：{e}")
            return False
            
    def navigate(self, url):
        """导航到新页面"""
        return self.open(url)
        
    def back(self):
        """后退"""
        self.page.go_back()
        print("✅ 已后退")
        
    def forward(self):
        """前进"""
        self.page.go_forward()
        print("✅ 已前进")
        
    def refresh(self):
        """刷新"""
        self.page.reload()
        print("✅ 已刷新")
        
    def click(self, selector, timeout=5000):
        """
        点击元素
        
        Args:
            selector: CSS 选择器
            timeout: 超时时间
        """
        try:
            self.page.click(selector, timeout=timeout)
            self.page.wait_for_load_state('networkidle')
            print(f"✅ 已点击：{selector}")
            return True
        except Exception as e:
            print(f"❌ 点击失败：{e}")
            return False
            
    def fill(self, selector, value):
        """
        填写表单
        
        Args:
            selector: CSS 选择器
            value: 填写内容
        """
        try:
            self.page.fill(selector, value)
            print(f"✅ 已填写：{selector} = {value[:10]}...")
            return True
        except Exception as e:
            print(f"❌ 填写失败：{e}")
            return False
            
    def select(self, selector, value):
        """
        选择下拉选项
        
        Args:
            selector: CSS 选择器
            value: 选项值
        """
        try:
            self.page.select_option(selector, value)
            print(f"✅ 已选择：{selector} = {value}")
            return True
        except Exception as e:
            print(f"❌ 选择失败：{e}")
            return False
            
    def check(self, selector):
        """勾选复选框"""
        try:
            self.page.check(selector)
            print(f"✅ 已勾选：{selector}")
            return True
        except Exception as e:
            print(f"❌ 勾选失败：{e}")
            return False
            
    def hover(self, selector):
        """悬停元素"""
        try:
            self.page.hover(selector)
            print(f"✅ 已悬停：{selector}")
            return True
        except Exception as e:
            print(f"❌ 悬停失败：{e}")
            return False
            
    def scroll(self, pixels=500, direction='down'):
        """
        滚动页面
        
        Args:
            pixels: 滚动像素
            direction: 方向 (down/up/left/right)
        """
        try:
            if direction == 'down':
                self.page.evaluate(f"window.scrollBy(0, {pixels})")
            elif direction == 'up':
                self.page.evaluate(f"window.scrollBy(0, -{pixels})")
            elif direction == 'left':
                self.page.evaluate(f"window.scrollBy(-{pixels}, 0)")
            elif direction == 'right':
                self.page.evaluate(f"window.scrollBy({pixels}, 0)")
            print(f"✅ 已滚动：{direction} {pixels}px")
            return True
        except Exception as e:
            print(f"❌ 滚动失败：{e}")
            return False
            
    def screenshot(self, output='screenshot.png', full_page=False, element=None):
        """
        截图
        
        Args:
            output: 输出文件
            full_page: 是否全屏截图
            element: 元素选择器（仅截该元素）
        """
        try:
            # 确保输出目录存在
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if element:
                # 截取特定元素
                el = self.page.query_selector(element)
                if el:
                    el.screenshot(path=output)
                    print(f"✅ 元素截图已保存：{output}")
                else:
                    print(f"❌ 元素未找到：{element}")
                    return False
            else:
                # 截取整个页面
                self.page.screenshot(
                    path=output,
                    full_page=full_page
                )
                print(f"✅ 截图已保存：{output}")
            return output
        except Exception as e:
            print(f"❌ 截图失败：{e}")
            return False
            
    def pdf(self, output='page.pdf'):
        """保存 PDF"""
        try:
            self.page.pdf(path=output)
            print(f"✅ PDF 已保存：{output}")
            return output
        except Exception as e:
            print(f"❌ PDF 保存失败：{e}")
            return False
            
    def text(self, selector=None, all=False):
        """
        提取文本
        
        Args:
            selector: CSS 选择器（None 则提取全文）
            all: 是否提取所有匹配元素
        """
        try:
            if selector is None:
                return self.page.inner_text('body')
            elif all:
                elements = self.page.query_selector_all(selector)
                return [el.inner_text() for el in elements]
            else:
                return self.page.inner_text(selector)
        except Exception as e:
            print(f"❌ 提取文本失败：{e}")
            return None
            
    def html(self, selector=None):
        """获取 HTML"""
        try:
            if selector:
                el = self.page.query_selector(selector)
                return el.inner_html() if el else None
            return self.page.content()
        except Exception as e:
            print(f"❌ 获取 HTML 失败：{e}")
            return None
            
    def attribute(self, selector, attr):
        """获取属性值"""
        try:
            el = self.page.query_selector(selector)
            if el:
                return el.get_attribute(attr)
            return None
        except Exception as e:
            print(f"❌ 获取属性失败：{e}")
            return None
            
    def links(self, domain=None):
        """
        提取链接
        
        Args:
            domain: 过滤域名
        """
        try:
            links = self.page.query_selector_all('a')
            result = []
            for link in links:
                href = link.get_attribute('href')
                if href:
                    if domain is None or domain in href:
                        result.append({
                            'text': link.inner_text(),
                            'href': href
                        })
            return result
        except Exception as e:
            print(f"❌ 提取链接失败：{e}")
            return []
            
    def images(self, download=False):
        """
        提取图片
        
        Args:
            download: 是否下载图片
        """
        try:
            imgs = self.page.query_selector_all('img')
            result = []
            for img in imgs:
                src = img.get_attribute('src')
                alt = img.get_attribute('alt')
                if src:
                    result.append({'src': src, 'alt': alt})
                    if download and src.startswith('http'):
                        # 下载逻辑（可扩展）
                        pass
            return result
        except Exception as e:
            print(f"❌ 提取图片失败：{e}")
            return []
            
    def table(self, selector):
        """提取表格数据"""
        try:
            rows = self.page.query_selector_all(f"{selector} tr")
            data = []
            for row in rows:
                cells = row.query_selector_all('td, th')
                row_data = [cell.inner_text() for cell in cells]
                if row_data:
                    data.append(row_data)
            return data
        except Exception as e:
            print(f"❌ 提取表格失败：{e}")
            return []
            
    def wait(self, selector=None, timeout=10000, url=None):
        """
        等待
        
        Args:
            selector: 等待元素
            timeout: 超时时间
            url: 等待 URL
        """
        try:
            if url:
                self.page.wait_for_url(url, timeout=timeout)
                print(f"✅ 已等待 URL: {url}")
            elif selector:
                self.page.wait_for_selector(selector, timeout=timeout)
                print(f"✅ 已等待元素：{selector}")
            else:
                time.sleep(timeout / 1000)
            return True
        except Exception as e:
            print(f"❌ 等待失败：{e}")
            return False
            
    def eval(self, js_code):
        """执行 JavaScript"""
        try:
            result = self.page.evaluate(js_code)
            return result
        except Exception as e:
            print(f"❌ JS 执行失败：{e}")
            return None
            
    def inject(self, script_path):
        """注入脚本"""
        try:
            with open(script_path, 'r') as f:
                script = f.read()
            self.page.evaluate(script)
            print(f"✅ 已注入脚本：{script_path}")
            return True
        except Exception as e:
            print(f"❌ 注入失败：{e}")
            return False
            
    def cookie(self, action='get', name=None, value=None):
        """
        管理 Cookie
        
        Args:
            action: get/set/delete
            name: Cookie 名称
            value: Cookie 值
        """
        try:
            if action == 'get':
                cookies = self.context.cookies()
                if name:
                    for c in cookies:
                        if c['name'] == name:
                            return c['value']
                    return None
                return cookies
            elif action == 'set':
                self.context.add_cookies([{
                    'name': name,
                    'value': value,
                    'domain': self.current_url
                }])
                print(f"✅ 已设置 Cookie: {name}")
                return True
            elif action == 'delete':
                self.context.clear_cookies()
                print("✅ 已清除所有 Cookie")
                return True
        except Exception as e:
            print(f"❌ Cookie 操作失败：{e}")
            return None
            
    def storage(self, action='get', key=None):
        """
        本地存储
        
        Args:
            action: get/set
            key: 键名
        """
        try:
            if action == 'get':
                storage = self.page.evaluate('localStorage')
                if key:
                    return storage.get(key)
                return storage
        except Exception as e:
            print(f"❌ 存储操作失败：{e}")
            return None
            
    def network(self, log=False, filter=None):
        """
        网络监控
        
        Args:
            log: 是否打印日志
            filter: 过滤关键词
        """
        requests = []
        
        def handle_request(request):
            url = request.url
            if filter is None or filter in url:
                requests.append({
                    'url': url,
                    'method': request.method,
                    'type': request.resource_type
                })
                if log:
                    print(f"🌐 {request.method} {url}")
                    
        self.page.on('request', handle_request)
        print(f"✅ 网络监控已启动 (filter: {filter})")
        return requests


# CLI 入口
if __name__ == '__main__':
    import sys
    
    ba = BrowserAutomation(headless=False)
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'open' and len(sys.argv) > 2:
            ba.open(sys.argv[2])
        elif cmd == 'screenshot':
            output = sys.argv[2] if len(sys.argv) > 2 else 'screenshot.png'
            ba.screenshot(output=output, full_page=True)
        elif cmd == 'close':
            ba.close()
        else:
            print("用法：python browser_automation.py <command> [args]")
            print("命令：open <url>, screenshot [output], close")
    else:
        # 演示
        ba.start()
        ba.open('https://example.com')
        ba.screenshot('example.png', full_page=True)
        print(f"页面标题：{ba.eval('document.title')}")
        ba.close()
