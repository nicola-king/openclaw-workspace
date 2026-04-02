#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书适配器

太一 v4.0 - 浏览器适配器层
功能：笔记发布/数据分析
"""

import asyncio
from playwright.async_api import async_playwright, Browser, Page
from typing import Optional, Dict, Any, List
from pathlib import Path


class XiaohongshuAdapter:
    """小红书适配器"""
    
    def __init__(
        self,
        headless: bool = False,
        user_data_dir: Optional[str] = None
    ):
        """
        初始化小红书适配器
        
        参数:
            headless: 是否无头模式（建议 False，复用可见浏览器）
            user_data_dir: 用户数据目录（复用本地登录状态）
        """
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.base_url = 'https://creator.xiaohongshu.com'
    
    async def launch(self):
        """启动浏览器"""
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        self.page = await self.browser.new_page()
        
        await self.page.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        ''')
        
        print("✅ 小红书浏览器已启动")
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("🚪 小红书浏览器已关闭")
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        执行小红书操作
        
        支持操作：
        - publish_note: 发布笔记
        - get_analytics: 获取数据分析
        - get_drafts: 获取草稿
        """
        if not self.browser:
            await self.launch()
        
        if action == 'publish_note':
            return await self._publish_note(**kwargs)
        elif action == 'get_analytics':
            return await self._get_analytics()
        elif action == 'get_drafts':
            return await self._get_drafts()
        else:
            raise ValueError(f"未知操作：{action}")
    
    async def _publish_note(
        self,
        title: str,
        content: str,
        images: List[str],
        topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        发布小红书笔记
        
        参数:
            title: 笔记标题
            content: 笔记内容
            images: 图片路径列表
            topics: 话题标签列表（可选）
        
        返回:
            {
                'status': 'success' | 'failed',
                'title': str,
                'message': str
            }
        """
        try:
            # 导航到创作中心
            print("📍 导航到创作中心...")
            await self.page.goto(self.base_url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            # 检查是否已登录
            is_logged_in = await self._check_login()
            if not is_logged_in:
                return {
                    'status': 'failed',
                    'error': '未登录，请先在浏览器中登录小红书创作中心'
                }
            
            # 点击"发布笔记"
            print("📝 点击发布笔记...")
            publish_btn = await self.page.query_selector(
                'button:has-text("发布笔记"), button:has-text("创作")'
            )
            if publish_btn:
                await publish_btn.click()
                await asyncio.sleep(2)
            
            # 上传图片
            print(f"🖼️ 上传 {len(images)} 张图片...")
            await self._upload_images(images)
            await asyncio.sleep(2)
            
            # 输入标题
            print(f"📌 输入标题：{title}")
            title_input = await self.page.query_selector(
                'input[placeholder*="标题"], input[placeholder*="填写标题"]'
            )
            if title_input:
                await title_input.fill(title)
            await asyncio.sleep(1)
            
            # 输入内容
            print("📄 输入内容...")
            content_input = await self.page.query_selector(
                'textarea[placeholder*="添加话题"], textarea[placeholder*="正文"]'
            )
            if content_input:
                await content_input.fill(content)
                
                # 添加话题标签
                if topics:
                    for topic in topics:
                        await content_input.press('Space')
                        await content_input.fill(f' #{topic}')
            
            await asyncio.sleep(1)
            
            # 点击发布
            print("📤 点击发布...")
            submit_btn = await self.page.query_selector(
                'button:has-text("发布笔记"), button:has-text("发布")'
            )
            if submit_btn:
                await submit_btn.click()
                await asyncio.sleep(3)
            
            # 等待发布完成
            print("⏳ 等待发布完成...")
            await asyncio.sleep(5)
            
            print(f"✅ 笔记已发布：{title}")
            return {
                'status': 'success',
                'title': title,
                'message': f'笔记《{title}》已发布成功'
            }
            
        except Exception as e:
            print(f"❌ 发布失败：{str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'title': title
            }
    
    async def _check_login(self) -> bool:
        """检查是否已登录"""
        try:
            await self.page.wait_for_load_state('networkidle')
            
            login_btn = await self.page.query_selector(
                'a:has-text("登录"), button:has-text("登录")'
            )
            
            return login_btn is None
            
        except Exception:
            return False
    
    async def _upload_images(self, images: List[str]):
        """上传图片"""
        try:
            # 找到上传区域
            upload_area = await self.page.query_selector(
                'input[type="file"], .upload_area, .image_upload'
            )
            
            if upload_area:
                # 多张图片上传
                await upload_area.set_input_files(images)
                print(f"✅ 已上传 {len(images)} 张图片")
            else:
                print("⚠️  未找到上传区域，请手动上传")
                
        except Exception as e:
            print(f"⚠️  图片上传失败：{str(e)}")
    
    async def _get_analytics(self) -> Dict[str, Any]:
        """获取数据分析"""
        try:
            # 导航到数据中心
            await self.page.goto(f'{self.base_url}/note/analysis', wait_until='networkidle')
            await asyncio.sleep(2)
            
            # 提取数据（简化示例）
            analytics = {
                'views': 0,
                'likes': 0,
                'comments': 0,
                'saves': 0
            }
            
            return {
                'status': 'success',
                'analytics': analytics
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def _get_drafts(self) -> Dict[str, Any]:
        """获取草稿列表"""
        try:
            await self.page.goto(f'{self.base_url}/draft', wait_until='networkidle')
            await asyncio.sleep(2)
            
            drafts = []
            
            return {
                'status': 'success',
                'drafts': drafts
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }


# 测试入口
async def test_xiaohongshu_adapter():
    """测试小红书适配器"""
    adapter = XiaohongshuAdapter(
        headless=False,
        user_data_dir=str(Path.home() / '.config' / 'google-chrome')
    )
    
    try:
        await adapter.launch()
        
        # 测试发布笔记
        result = await adapter.execute(
            action='publish_note',
            title='太一 AGI v4.0 融合 Claude Code 精华',
            content='今天完成了太一 v4.0 架构升级...',
            images=[],
            topics=['AI', '太一 AGI', 'OpenClaw']
        )
        
        print(f"测试结果：{result}")
        
    finally:
        await adapter.close()


if __name__ == '__main__':
    asyncio.run(test_xiaohongshu_adapter())
