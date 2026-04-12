#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio, tempfile, shutil
from playwright.async_api import async_playwright
from typing import Optional, Dict, Any
from pathlib import Path

class WeChatAdapter:
    def __init__(self, headless=False, user_data_dir=None):
        self.headless = headless
        self.user_data_dir = user_data_dir or '/home/nicola/.openclaw/wechat-session3'
        self.browser = None
        self.page = None
        self.playwright = None
        self.base_url = 'https://mp.weixin.qq.com'

    async def launch(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            viewport={'width': 1280, 'height': 900},
            args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
        self.page = await self.browser.new_page()
        await self.page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        print("✅ 浏览器已启动")

    async def close(self):
        if self.browser: await self.browser.close()
        if self.playwright: await self.playwright.stop()

    async def _get_token(self) -> str:
        """从当前页面URL提取token"""
        url = self.page.url
        if 'token=' in url:
            return url.split('token=')[1].split('&')[0]
        return ''

    async def _ensure_logged_in(self) -> bool:
        await self.page.goto(self.base_url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(2)
        if 'passport' in self.page.url or 'login' in self.page.url:
            print("🔐 需要扫码登录，请在浏览器中扫码...")
            for _ in range(60):
                await asyncio.sleep(1)
                if 'token=' in self.page.url:
                    print("✅ 登录成功")
                    return True
            return False
        print("✅ 已登录")
        return True

    async def publish_article(self, title: str, content: str,
                               summary: str = '', author: str = '',
                               cover_image: str = '',
                               auto_publish: bool = False) -> Dict[str, Any]:
        if not self.browser:
            await self.launch()

        if not await self._ensure_logged_in():
            return {'status': 'failed', 'error': '登录失败'}

        token = await self._get_token()
        if not token:
            return {'status': 'failed', 'error': '获取token失败'}

        print(f"🔑 Token: {token}")
        editor_url = f'{self.base_url}/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&token={token}&lang=zh_CN'
        await self.page.goto(editor_url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(5)

        if 'appmsg_edit' not in self.page.url:
            return {'status': 'failed', 'error': f'无法打开编辑器，当前URL: {self.page.url}'}

        # 填写标题
        print(f"✏️  填写标题：{title}")
        await self.page.fill('textarea#title', title)

        # 填写作者
        if author:
            await self.page.fill('input#author', author)

        # 填写正文（ProseMirror 编辑器）
        print("✏️  填写正文...")
        editor = await self.page.wait_for_selector('div.ProseMirror', timeout=10000)
        await editor.click()
        await asyncio.sleep(1)
        # 清空并注入 HTML
        await self.page.evaluate("""
            () => {
                const editor = document.querySelector('div.ProseMirror');
                if (editor) {
                    editor.focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('delete', false, null);
                }
            }
        """)
        await self.page.keyboard.type(content)
        print("✅ 正文已填写")

        # 填写摘要
        if summary:
            print("✏️  填写摘要...")
            await self.page.fill('textarea#js_description', summary)

        # 上传封面
        if cover_image:
            print(f"🖼️  上传封面：{cover_image}")
            try:
                await self.page.set_input_files('input[type="file"]', cover_image)
                await asyncio.sleep(3)
            except Exception as e:
                print(f"⚠️  封面上传失败：{e}")

        if not auto_publish:
            print("✅ 内容填写完毕，请手动点击【发表】或【存草稿】")
            print("⏳ 等待 180 秒...")
            await asyncio.sleep(180)
            return {'status': 'pending_manual', 'title': title}

        # 自动点发表
        print("🚀 点击发表...")
        for sel in ['text=发表', '#js_send_btn', 'button.js_send']:
            try:
                await self.page.click(sel, timeout=3000)
                await asyncio.sleep(2)
                for csel in ['text=确定', 'text=群发给所有用户', '.weui-dialog__ft .primary']:
                    try:
                        await self.page.click(csel, timeout=3000)
                        await asyncio.sleep(3)
                        print("✅ 发表成功")
                        return {'status': 'success', 'title': title}
                    except: continue
            except: continue

        return {'status': 'pending_manual', 'title': title, 'message': '请手动点击发表'}


async def main():
    import argparse
    parser = argparse.ArgumentParser(description='微信公众号发布')
    parser.add_argument('--title', required=True)
    parser.add_argument('--content', default='')
    parser.add_argument('--content-file', default='')
    parser.add_argument('--summary', default='')
    parser.add_argument('--author', default='')
    parser.add_argument('--cover', default='')
    parser.add_argument('--auto', action='store_true')
    parser.add_argument('--user-data-dir', default='/home/nicola/.openclaw/wechat-session3')
    args = parser.parse_args()

    content = args.content
    if args.content_file:
        content = Path(args.content_file).read_text(encoding='utf-8')
    if not content:
        print("❌ 需要 --content 或 --content-file"); return

    adapter = WeChatAdapter(headless=False, user_data_dir=args.user_data_dir)
    try:
        result = await adapter.publish_article(
            title=args.title, content=content,
            summary=args.summary, author=args.author,
            cover_image=args.cover, auto_publish=args.auto)
        print(f"\n📊 结果：{result}")
    finally:
        await adapter.close()

if __name__ == '__main__':
    asyncio.run(main())
