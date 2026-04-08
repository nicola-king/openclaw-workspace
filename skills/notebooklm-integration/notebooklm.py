#!/usr/bin/env python3
"""
Google NotebookLM 集成 - 笔记/研究/知识库自动化

🆕 2026-04-08: 创建
- 创建知识库
- 添加文档源
- 自动生成摘要
- AI 问答
- 网页自动化方案

⚠️ 注意：NotebookLM 无官方 API，使用网页自动化
"""

import os
import sys
import json
import time
from typing import Dict, Any, List, Optional

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("警告：playwright 未安装，将使用基础方案")


class NotebookLMIntegration:
    """NotebookLM 集成"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.config = self.load_config()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
        if not PLAYWRIGHT_AVAILABLE:
            print("⚠️  Playwright 不可用，部分功能受限")
    
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
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright 未安装")
        
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
        
        # 创建上下文 (可复用 Chrome 配置)
        notebooklm_config = self.config.get('notebooklm', {})
        user_data_dir = notebooklm_config.get('browserProfile', '~/.config/google-chrome')
        user_data_dir = os.path.expanduser(user_data_dir)
        
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
    
    def create_notebook(self, title: str) -> Dict[str, Any]:
        """
        创建知识库
        
        Args:
            title: 知识库标题
        
        Returns:
            创建结果
        """
        if not self.page:
            self.start_browser()
        
        try:
            # 打开 NotebookLM
            print(f"🌐 打开 NotebookLM...")
            self.page.goto("https://notebooklm.google.com/", wait_until="networkidle")
            time.sleep(3)
            
            # 检查是否已登录
            if "signin" in self.page.url.lower():
                return {
                    'success': False,
                    'error': '需要登录 Google 账号',
                    'url': self.page.url,
                    'help': '请先在浏览器中登录 Google 账号'
                }
            
            # 点击"新建 Notebook"
            print("📝 创建新知识库...")
            new_button = self.page.query_selector("button:has-text('新建')") or \
                        self.page.query_selector("button:has-text('New')") or \
                        self.page.query_selector("button[aria-label*='新建']")
            
            if new_button:
                new_button.click()
                time.sleep(2)
                
                # 输入标题
                title_input = self.page.query_selector("input[placeholder*='标题']") or \
                             self.page.query_selector("input[placeholder*='title']")
                
                if title_input:
                    title_input.fill(title)
                    time.sleep(1)
                    
                    # 确认创建
                    confirm_button = self.page.query_selector("button:has-text('创建')") or \
                                    self.page.query_selector("button:has-text('Create')") or \
                                    self.page.query_selector("button[type='submit']")
                    
                    if confirm_button:
                        confirm_button.click()
                        time.sleep(2)
                        
                        # 获取 Notebook ID
                        current_url = self.page.url
                        notebook_id = current_url.split('/notebook/')[-1] if '/notebook/' in current_url else None
                        
                        print(f"✅ 知识库创建成功：{title}")
                        
                        return {
                            'success': True,
                            'title': title,
                            'notebook_id': notebook_id,
                            'url': current_url,
                            'timestamp': time.time()
                        }
            
            # 备用方案：直接返回 URL
            return {
                'success': True,
                'title': title,
                'notebook_id': None,
                'url': 'https://notebooklm.google.com/',
                'message': '请手动创建知识库',
                'timestamp': time.time()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_source(self, notebook_id: str, title: str, content: str) -> Dict[str, Any]:
        """
        添加文档源
        
        Args:
            notebook_id: 知识库 ID
            title: 文档标题
            content: 文档内容
        
        Returns:
            添加结果
        """
        if not self.page:
            self.start_browser()
        
        try:
            # 打开知识库
            url = f"https://notebooklm.google.com/notebook/{notebook_id}"
            print(f"🌐 打开知识库...")
            self.page.goto(url, wait_until="networkidle")
            time.sleep(3)
            
            # 点击"添加源"
            print("📝 添加文档源...")
            add_button = self.page.query_selector("button:has-text('添加源')") or \
                        self.page.query_selector("button:has-text('Add source')")
            
            if add_button:
                add_button.click()
                time.sleep(2)
                
                # 选择"文本"类型
                text_option = self.page.query_selector("div:has-text('文本')") or \
                             self.page.query_selector("div:has-text('Text')")
                
                if text_option:
                    text_option.click()
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
                                     self.page.query_selector("button:has-text('Save')")
                        
                        if save_button:
                            save_button.click()
                            time.sleep(2)
                            
                            print(f"✅ 文档源添加成功：{title}")
                            
                            return {
                                'success': True,
                                'title': title,
                                'notebook_id': notebook_id,
                                'timestamp': time.time()
                            }
            
            return {
                'success': False,
                'error': '找不到添加源按钮',
                'help': '请手动添加文档源'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def summarize_notebook(self, notebook_id: str) -> Dict[str, Any]:
        """
        生成知识库摘要
        
        Args:
            notebook_id: 知识库 ID
        
        Returns:
            摘要结果
        """
        if not self.page:
            self.start_browser()
        
        try:
            # 打开知识库
            url = f"https://notebooklm.google.com/notebook/{notebook_id}"
            print(f"🌐 打开知识库...")
            self.page.goto(url, wait_until="networkidle")
            time.sleep(3)
            
            # 查找摘要按钮
            print("📝 生成摘要...")
            summarize_button = self.page.query_selector("button:has-text('摘要')") or \
                              self.page.query_selector("button:has-text('Summarize')") or \
                              self.page.query_selector("button[aria-label*='摘要']")
            
            if summarize_button:
                summarize_button.click()
                time.sleep(5)  # 等待 AI 生成
                
                # 获取摘要内容
                summary_selector = "div.summary-content"
                summary_element = self.page.query_selector(summary_selector)
                
                if summary_element:
                    summary_text = summary_element.inner_text()
                    print(f"✅ 摘要生成成功 ({len(summary_text)} 字符)")
                    
                    return {
                        'success': True,
                        'notebook_id': notebook_id,
                        'summary': summary_text,
                        'timestamp': time.time()
                    }
            
            # 备用方案：返回提示
            return {
                'success': True,
                'notebook_id': notebook_id,
                'message': '请点击"摘要"按钮生成摘要',
                'url': url,
                'timestamp': time.time()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def ask_question(self, notebook_id: str, question: str) -> Dict[str, Any]:
        """
        AI 问答
        
        Args:
            notebook_id: 知识库 ID
            question: 问题
        
        Returns:
            回答结果
        """
        if not self.page:
            self.start_browser()
        
        try:
            # 打开知识库
            url = f"https://notebooklm.google.com/notebook/{notebook_id}"
            print(f"🌐 打开知识库...")
            self.page.goto(url, wait_until="networkidle")
            time.sleep(3)
            
            # 找到输入框
            print("📝 提问...")
            input_selector = "div[contenteditable='true']"
            input_box = self.page.query_selector(input_selector)
            
            if not input_box:
                input_box = self.page.query_selector("textarea")
            
            if input_box:
                input_box.fill(question)
                time.sleep(1)
                
                # 点击发送
                send_button = self.page.query_selector("button[aria-label='发送']") or \
                             self.page.query_selector("button.send-button")
                
                if send_button:
                    send_button.click()
                    time.sleep(5)  # 等待 AI 回答
                    
                    # 获取回答
                    response_selector = "div.response-content"
                    response = self.page.query_selector(response_selector)
                    
                    if response:
                        response_text = response.inner_text()
                        print(f"✅ 收到回答 ({len(response_text)} 字符)")
                        
                        return {
                            'success': True,
                            'notebook_id': notebook_id,
                            'question': question,
                            'answer': response_text,
                            'timestamp': time.time()
                        }
            
            return {
                'success': False,
                'error': '找不到输入框或发送按钮',
                'help': '请手动提问'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def export_notes(self, notebook_id: str, format: str = 'markdown') -> Dict[str, Any]:
        """
        导出笔记
        
        Args:
            notebook_id: 知识库 ID
            format: 导出格式 (markdown, pdf, text)
        
        Returns:
            导出结果
        """
        if not self.page:
            self.start_browser()
        
        try:
            # 打开知识库
            url = f"https://notebooklm.google.com/notebook/{notebook_id}"
            print(f"🌐 打开知识库...")
            self.page.goto(url, wait_until="networkidle")
            time.sleep(3)
            
            # 查找导出按钮
            print("📝 导出笔记...")
            export_button = self.page.query_selector("button:has-text('导出')") or \
                           self.page.query_selector("button:has-text('Export')")
            
            if export_button:
                export_button.click()
                time.sleep(2)
                
                # 选择格式
                if format == 'markdown':
                    md_option = self.page.query_selector("div:has-text('Markdown')")
                    if md_option:
                        md_option.click()
                elif format == 'pdf':
                    pdf_option = self.page.query_selector("div:has-text('PDF')")
                    if pdf_option:
                        pdf_option.click()
                
                time.sleep(2)
                
                # 确认导出
                confirm_button = self.page.query_selector("button:has-text('下载')") or \
                                self.page.query_selector("button:has-text('Download')")
                
                if confirm_button:
                    confirm_button.click()
                    time.sleep(2)
                    
                    print(f"✅ 导出成功 (格式：{format})")
                    
                    return {
                        'success': True,
                        'notebook_id': notebook_id,
                        'format': format,
                        'message': '下载已开始',
                        'timestamp': time.time()
                    }
            
            return {
                'success': False,
                'error': '找不到导出按钮',
                'help': '请手动导出'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='NotebookLM 集成')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # create
    p_create = subparsers.add_parser('create', help='创建知识库')
    p_create.add_argument('title', help='知识库标题')
    
    # add-source
    p_add = subparsers.add_parser('add-source', help='添加文档源')
    p_add.add_argument('notebook_id', help='知识库 ID')
    p_add.add_argument('--title', '-t', required=True, help='文档标题')
    p_add.add_argument('--content', '-c', required=True, help='文档内容')
    
    # summarize
    p_sum = subparsers.add_parser('summarize', help='生成摘要')
    p_sum.add_argument('notebook_id', help='知识库 ID')
    
    # ask
    p_ask = subparsers.add_parser('ask', help='AI 问答')
    p_ask.add_argument('notebook_id', help='知识库 ID')
    p_ask.add_argument('--question', '-q', required=True, help='问题')
    
    # export
    p_export = subparsers.add_parser('export', help='导出笔记')
    p_export.add_argument('notebook_id', help='知识库 ID')
    p_export.add_argument('--format', '-f', default='markdown', choices=['markdown', 'pdf', 'text'])
    
    args = parser.parse_args()
    
    notebooklm = NotebookLMIntegration(headless=False)
    
    try:
        if args.command == 'create':
            result = notebooklm.create_notebook(args.title)
        
        elif args.command == 'add-source':
            result = notebooklm.add_source(args.notebook_id, args.title, args.content)
        
        elif args.command == 'summarize':
            result = notebooklm.summarize_notebook(args.notebook_id)
        
        elif args.command == 'ask':
            result = notebooklm.ask_question(args.notebook_id, args.question)
        
        elif args.command == 'export':
            result = notebooklm.export_notes(args.notebook_id, args.format)
        
        else:
            parser.print_help()
            sys.exit(1)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    finally:
        notebooklm.close_browser()
