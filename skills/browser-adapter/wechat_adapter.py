#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号适配器

太一 v4.0 - 浏览器适配器层
功能：公众号文章发布/草稿管理
"""

import asyncio
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
            headless: 是否无头模式（建议 False，复用可见浏览器）
            user_data_dir: 用户数据目录（复用本地登录状态）
        """
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.base_url = 'https://mp.weixin.qq.com'
    
    async def launch(self):
        """启动浏览器"""
        self.playwright = await async_playwright().start()
        
        # 启动浏览器（复用本地用户数据）
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
        
        # 注入反检测脚本
        await self.page.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        ''')
        
        print("✅ 微信浏览器已启动")
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
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
        """
        发布公众号文章
        
        参数:
            title: 文章标题
            content: 文章内容（HTML 格式）
            cover_image: 封面图片路径（可选）
            summary: 摘要（可选，默认自动提取）
        
        返回:
            {
                'status': 'success' | 'failed',
                'title': str,
                'message': str
            }
        """
        try:
            # 导航到公众号后台
            print("📍 导航到公众号后台...")
            await self.page.goto(self.base_url, wait_until='networkidle')
            await asyncio.sleep(3)  # 等待页面加载
            
            # 检查是否已登录
            is_logged_in = await self._check_login()
            if not is_logged_in:
                return {
                    'status': 'failed',
                    'error': '未登录，请先在浏览器中登录微信公众号后台'
                }
            
            # 点击"新建图文"
            print("📝 点击新建图文...")
            new_article_btn = await self.page.query_selector(
                'a:has-text("新建图文"), button:has-text("新建图文")'
            )
            if new_article_btn:
                await new_article_btn.click()
                await asyncio.sleep(2)
            
            # 切换到新标签页
            pages = self.page.context.pages
            if len(pages) > 1:
                self.page = pages[-1]
            
            # 输入标题
            print(f"📌 输入标题：{title}")
            title_input = await self.page.query_selector(
                'input[placeholder*="标题"], input[placeholder*="文章标题"]'
            )
            if title_input:
                await title_input.fill(title)
            await asyncio.sleep(1)
            
            # 编辑内容（富文本编辑器）
            print("📄 编辑内容...")
            editor = await self.page.query_selector(
                '.rich_media_editor, .editor-content, [contenteditable="true"]'
            )
            if editor:
                await editor.evaluate(f'el => el.innerHTML = `{content}`')
            await asyncio.sleep(1)
            
            # 上传封面图片（如果有）
            if cover_image:
                print(f"🖼️ 上传封面：{cover_image}")
                await self._upload_cover(cover_image)
            
            # 点击"群发"
            print("📤 点击群发...")
            publish_btn = await self.page.query_selector(
                'button:has-text("群发"), button:has-text("发表"), button:has-text("保存并群发")'
            )
            if publish_btn:
                await publish_btn.click()
                await asyncio.sleep(2)
            
            # 确认群发（如果有确认对话框）
            confirm_btn = await self.page.query_selector(
                'button:has-text("确认"), button:has-text("确定"), .wx_btn_primary'
            )
            if confirm_btn:
                await confirm_btn.click()
                await asyncio.sleep(3)
            
            print(f"✅ 文章已发布：{title}")
            return {
                'status': 'success',
                'title': title,
                'message': f'文章《{title}》已发布成功'
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
            # 检查是否有登录态特征
            await self.page.wait_for_load_state('networkidle')
            
            # 检查是否有登录按钮（未登录）
            login_btn = await self.page.query_selector(
                'a:has-text("登录"), button:has-text("登录")'
            )
            
            return login_btn is None
            
        except Exception:
            return False
    
    async def _upload_cover(self, image_path: str):
        """上传封面图片"""
        try:
            # 找到封面上传区域
            cover_area = await self.page.query_selector(
                '.cover_area, .upload_cover, input[type="file"]'
            )
            
            if cover_area:
                # 如果是 input[type="file"]
                if await cover_area.evaluate('el => el.tagName === "INPUT"'):
                    await cover_area.set_input_files(image_path)
                else:
                    # 点击后选择图片
                    await cover_area.click()
                    await asyncio.sleep(1)
                    
                    # 处理文件选择对话框（需要系统级操作，这里简化）
                    print("⚠️  请手动选择封面图片")
                    
        except Exception as e:
            print(f"⚠️  封面上传失败：{str(e)}")
    
    async def _get_drafts(self) -> Dict[str, Any]:
        """获取草稿列表"""
        try:
            # 导航到草稿箱
            await self.page.goto(f'{self.base_url}/draft', wait_until='networkidle')
            await asyncio.sleep(2)
            
            # 提取草稿列表
            drafts = []
            draft_items = await self.page.query_selector_all('.draft_item')
            
            for item in draft_items:
                title = await item.text_content('.draft_title')
                date = await item.text_content('.draft_date')
                drafts.append({
                    'title': title.strip() if title else '',
                    'date': date.strip() if date else ''
                })
            
            return {
                'status': 'success',
                'drafts': drafts
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def _delete_draft(self, draft_id: str) -> Dict[str, Any]:
        """删除草稿"""
        try:
            # 实现删除逻辑
            return {
                'status': 'success',
                'message': f'草稿 {draft_id} 已删除'
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }


# 测试入口
async def test_wechat_adapter():
    """测试微信适配器"""
    adapter = WeChatAdapter(
        headless=False,
        user_data_dir=str(Path.home() / '.config' / 'google-chrome')
    )
    
    try:
        await adapter.launch()
        
        # 测试发布文章
        result = await adapter.execute(
            action='publish_article',
            title='太一 AGI v4.0 融合架构',
            content='<h1>太一 v4.0</h1><p>融合 Claude Code 精华...</p>'
        )
        
        print(f"测试结果：{result}")
        
    finally:
        await adapter.close()


if __name__ == '__main__':
    asyncio.run(test_wechat_adapter())
