#!/usr/bin/env python3
"""
Google 服务网页自动化
Gemini / NotebookLM / Google Sheets 等自动操作

🆕 2026-04-08: 创建
- Gemini 自动对话
- NotebookLM 自动笔记
- Google Sheets 自动同步
"""

import os
import sys
import json
import time
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from typing import Dict, Any, Optional

class GoogleServicesAutomation:
    """Google 服务网页自动化"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.config = self.load_config()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    def load_config(self) -> Dict:
        """加载配置"""
        config_path = os.path.expanduser("~/.openclaw/workspace-taiyi/config/google-integration.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"警告：无法加载配置文件 {e}")
            return {}
    
    def start_browser(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        
        # 使用 Chromium
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080',
            ]
        )
        
        # 创建上下文
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = self.context.new_page()
        print("✅ 浏览器启动成功")
    
    def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("✅ 浏览器已关闭")
    
    def gemini_chat(self, prompt: str, model: str = "gemini-2.5-flash") -> Dict[str, Any]:
        """
        Gemini 自动对话
        
        Args:
            prompt: 提示词
            model: 模型版本
        
        Returns:
            响应结果
        """
        if not self.page:
            self.start_browser()
        
        try:
            # 打开 Gemini
            print(f"🌐 打开 Gemini ({model})...")
            self.page.goto("https://gemini.google.com/", wait_until="networkidle")
            time.sleep(3)  # 等待页面加载
            
            # 检查是否已登录
            if "signin" in self.page.url.lower():
                return {
                    'success': False,
                    'error': '需要登录 Google 账号',
                    'url': self.page.url
                }
            
            # 找到输入框并输入
            print("📝 输入提示词...")
            input_selector = "div[contenteditable='true']"
            input_box = self.page.query_selector(input_selector)
            
            if not input_box:
                # 尝试其他选择器
                input_box = self.page.query_selector("textarea")
            
            if input_box:
                input_box.fill(prompt)
                time.sleep(1)
                
                # 点击发送按钮
                print("🚀 发送消息...")
                send_button = self.page.query_selector("button[aria-label='发送']") or \
                             self.page.query_selector("button.send-button") or \
                             self.page.query_selector("div.submit-button")
                
                if send_button:
                    send_button.click()
                    time.sleep(2)
                    
                    # 等待响应
                    print("⏳ 等待响应...")
                    max_wait = 60  # 最多等待 60 秒
                    start_time = time.time()
                    
                    while time.time() - start_time < max_wait:
                        # 查找响应内容
                        response_selector = "div.response-content"
                        response = self.page.query_selector(response_selector)
                        
                        if response:
                            response_text = response.inner_text()
                            print(f"✅ 收到响应 ({len(response_text)} 字符)")
                            
                            return {
                                'success': True,
                                'response': response_text,
                                'model': model,
                                'timestamp': time.time()
                            }
                        
                        time.sleep(1)
                    
                    return {
                        'success': False,
                        'error': '等待响应超时',
                        'timeout': max_wait
                    }
                else:
                    return {'success': False, 'error': '找不到发送按钮'}
            else:
                return {'success': False, 'error': '找不到输入框'}
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def notebooklm_create_source(self, title: str, content: str) -> Dict[str, Any]:
        """
        NotebookLM 创建笔记源
        
        Args:
            title: 标题
            content: 内容
        
        Returns:
            创建结果
        """
        if not self.page:
            self.start_browser()
        
        try:
            # 打开 NotebookLM
            print("🌐 打开 NotebookLM...")
            self.page.goto("https://notebooklm.google.com/", wait_until="networkidle")
            time.sleep(3)
            
            # 检查是否已登录
            if "signin" in self.page.url.lower():
                return {
                    'success': False,
                    'error': '需要登录 Google 账号',
                    'url': self.page.url
                }
            
            # 点击添加源
            print("📝 添加新源...")
            add_button = self.page.query_selector("button[aria-label*='添加']") or \
                        self.page.query_selector("button:has-text('添加源')")
            
            if add_button:
                add_button.click()
                time.sleep(2)
                
                # 输入标题和内容
                title_input = self.page.query_selector("input[placeholder*='标题']")
                content_input = self.page.query_selector("textarea[placeholder*='内容']")
                
                if title_input and content_input:
                    title_input.fill(title)
                    content_input.fill(content)
                    time.sleep(1)
                    
                    # 保存
                    save_button = self.page.query_selector("button:has-text('保存')") or \
                                 self.page.query_selector("button[type='submit']")
                    
                    if save_button:
                        save_button.click()
                        time.sleep(2)
                        print("✅ 笔记源创建成功")
                        
                        return {
                            'success': True,
                            'title': title,
                            'timestamp': time.time()
                        }
            
            return {'success': False, 'error': '找不到添加源按钮'}
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def gemini_api_chat(self, prompt: str, model: str = "gemini-2.5-flash") -> Dict[str, Any]:
        """
        使用 API 调用 Gemini（推荐方式）
        
        Args:
            prompt: 提示词
            model: 模型版本
        
        Returns:
            响应结果
        """
        gemini_config = self.config.get('gemini', {})
        api_key = gemini_config.get('apiKey', '')
        
        if not api_key:
            return {
                'success': False,
                'error': '未配置 Gemini API Key'
            }
        
        import requests
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        params = {"key": api_key}
        
        # 使用代理
        proxy = os.environ.get('HTTP_PROXY', 'http://127.0.0.1:7890')
        proxies = {"http": proxy, "https": proxy}
        
        try:
            print(f"🚀 调用 Gemini API ({model})...")
            response = requests.post(url, json=payload, headers=headers, params=params, proxies=proxies, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            candidates = result.get('candidates', [])
            
            if not candidates:
                return {
                    'success': False,
                    'error': 'No candidates in response'
                }
            
            content = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            usage = result.get('usageMetadata', {})
            
            print(f"✅ 收到响应 ({len(content)} 字符)")
            
            return {
                'success': True,
                'response': content,
                'model': model,
                'tokens_in': usage.get('promptTokenCount', 0),
                'tokens_out': usage.get('candidatesTokenCount', 0),
                'timestamp': time.time()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# 使用示例
if __name__ == "__main__":
    automation = GoogleServicesAutomation(headless=False)
    
    # 示例 1: 使用 API 调用 Gemini
    print("\n=== 测试 Gemini API ===")
    result = automation.gemini_api_chat("你好，请介绍一下你自己")
    print(f"结果：{json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 示例 2: 网页自动化 Gemini（备用方案）
    # print("\n=== 测试 Gemini 网页自动化 ===")
    # result = automation.gemini_chat("你好，请介绍一下你自己")
    # print(f"结果：{json.dumps(result, ensure_ascii=False, indent=2)}")
    
    automation.close_browser()
