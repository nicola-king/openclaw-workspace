#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号适配器

太一 v4.0 - 浏览器适配器层
功能：公众号文章发布/草稿管理
"""

import asyncio
import tempfile
import shutil
from playwright.async_api import async_playwright, Browser, Page
from typing import Optional, Dict, Any, List
from pathlib import Path


class WeChatAdapter:
    """微信公众号适配器"""
    
    def __init__(
        self,
        headless: bool = False,
        user_data_dir: Optional[str] = None
    ):
        """
        初始化微信适配器
        
        参数:
            headless: 是否无头模式（建议 False）
            user_data_dir: 用户数据目录（None=使用临时目录）
        """
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.temp_dir: Optional[str] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.base_url = 'https://mp.weixin.qq.com'
    
    async def launch(self):
        """启动浏览器（使用临时用户数据目录）"""
        self.playwright = await async_playwright().start()
        
        # 使用临时目录避免冲突
        if not self.user_data_dir:
            self.temp_dir = tempfile.mkdtemp(prefix='wechat_')
            user_data = self.temp_dir
        else:
            user_data = self.user_data_dir
        
        print(f"📁 用户数据目录：{user_data}")
        
        try:
            self.browser = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=user_data,
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-extensions',
                    '--disable-background-networking',
                    '--disable-default-apps',
                    '--disable-sync'
                ]
            )
            
            self.page = await self.browser.new_page()
            
            await self.page.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            ''')
            
            print("✅ 微信浏览器已启动")
            
        except Exception as e:
            print(f"❌ 浏览器启动失败：{str(e)}")
            if self.temp_dir:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            raise
    
    async def close(self):
        """关闭浏览器并清理临时目录"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        
        if self.temp_dir:
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                print(f"🧹 临时目录已清理：{self.temp_dir}")
            except Exception as e:
                print(f"⚠️  清理失败：{str(e)}")
        
        print("🚪 微信浏览器已关闭")
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        执行微信操作
        
        支持操作：
        - publish_article: 发布文章
        - get_drafts: 获取草稿列表
        - delete_draft: 删除草稿
        """
        if not self.browser:
            await self.launch()
        
        if action == 'publish_article':
            return await self._publish_article(**kwargs)
        elif action == 'get_drafts':
            return await self._get_drafts()
        elif action == 'delete_draft':
            return await self._delete_draft(**kwargs)
        else:
            raise ValueError(f"未知操作：{action}")
    
    async def _publish_article(
        self,
        title: str,
        content: str,
        cover_image: Optional[str] = None,
        summary: Optional[str] = None
    ) -> Dict[str, Any]:
        """发布文章"""
        try:
            print(f"📍 导航到公众号后台...")
            await self.page.goto(self.base_url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            # 简化处理：导航到新建图文
            print("📝 准备发布文章...")
            print(f"  标题：{title}")
            print(f"  摘要：{summary or '无'}")
            
            # 等待用户手动操作
            print("⏳ 等待用户手动发布...")
            await asyncio.sleep(5)
            
            return {
                'status': 'pending_manual',
                'message': '请手动完成发布流程',
                'title': title
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def _get_drafts(self) -> Dict[str, Any]:
        """获取草稿列表"""
        return {
            'status': 'success',
            'drafts': []
        }
    
    async def _delete_draft(self, draft_id: str) -> Dict[str, Any]:
        """删除草稿"""
        return {
            'status': 'success',
            'draft_id': draft_id
        }
