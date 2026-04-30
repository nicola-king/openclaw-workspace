#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人微信 RPA 适配器 - 修复版

太一 v4.0 - 浏览器适配器层
功能：个人微信消息发送/接收/自动化

作者：太一 AGI
修复：2026-04-08 19:00
"""

import asyncio
import tempfile
import shutil
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext


class WeChatPersonalAdapter:
    """个人微信 RPA 适配器 (修复版)"""
    
    def __init__(
        self,
        account: str = "main",
        headless: bool = False,
        session_dir: Optional[str] = None
    ):
        """
        初始化个人微信适配器
        
        参数:
            account: 账号标识 (main/secondary)
            headless: 是否无头模式 (建议 False)
            session_dir: Session 存储目录
        """
        self.account = account
        self.headless = headless
        self.session_dir = session_dir or f"~/.taiyi/wechat/{account}"
        self.session_dir = Path(self.session_dir).expanduser()
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.base_url = "https://wx.qq.com"
        
        print(f"📱 个人微信适配器已初始化")
        print(f"   账号：{account}")
        print(f"   Session 目录：{self.session_dir}")
    
    def launch(self):
        """启动浏览器"""
        print("🚀 启动浏览器...")
        
        self.playwright = sync_playwright().start()
        
        # 启动 Chromium
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        
        # 创建浏览器上下文 (带持久化存储)
        self.context = self.browser.new_context(
            storage_state=self._load_storage_state(),
            viewport={'width': 1200, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 创建页面
        self.page = self.context.new_page()
        
        print("✅ 浏览器已启动")
    
    def _load_storage_state(self) -> Optional[Dict]:
        """加载存储状态 (Cookie/LocalStorage)"""
        state_file = self.session_dir / "storage_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                print(f"📦 已加载存储状态：{state_file}")
                return state
            except Exception as e:
                print(f"⚠️ 加载存储状态失败：{e}")
        return None
    
    def _save_storage_state(self):
        """保存存储状态"""
        if self.context:
            state_file = self.session_dir / "storage_state.json"
            try:
                state = self.context.storage_state()
                with open(state_file, 'w', encoding='utf-8') as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
                print(f"💾 已保存存储状态：{state_file}")
            except Exception as e:
                print(f"⚠️ 保存存储状态失败：{e}")
    
    def login(self, timeout: int = 120):
        """扫码登录"""
        print("📱 打开微信网页版...")
        
        self.page.goto(self.base_url, wait_until='domcontentloaded')
        
        # 等待二维码出现
        print("⏳ 等待二维码...")
        try:
            self.page.wait_for_selector('.img_qrcode', timeout=10000)
            print("✅ 二维码已显示，请扫码登录")
        except:
            print("⚠️ 未检测到二维码，可能已登录")
        
        # 等待登录成功 (检测主界面)
        print(f"⏳ 等待登录 (超时：{timeout}秒)...")
        try:
            # 等待主界面出现 (聊天列表)
            self.page.wait_for_selector('.chat_list', timeout=timeout * 1000)
            print("✅ 登录成功！")
            
            # 保存登录状态
            self._save_storage_state()
            
            return True
        except Exception as e:
            print(f"❌ 登录超时或失败：{e}")
            return False
    
    def send_message(self, contact: str, message: str) -> bool:
        """发送消息"""
        if not self.page:
            print("❌ 浏览器未启动")
            return False
        
        print(f"📤 发送消息给 {contact}: {message[:50]}...")
        
        try:
            # 1. 搜索联系人
            search_box = self.page.locator('.search_input').first
            search_box.fill(contact)
            time.sleep(1)
            
            # 2. 点击联系人
            self.page.locator('.chat_list_item').first.click()
            time.sleep(0.5)
            
            # 3. 输入消息
            input_box = self.page.locator('.editor_input').first
            input_box.fill(message)
            
            # 4. 发送 (Ctrl+Enter)
            input_box.press('Control+Enter')
            
            print("✅ 消息已发送")
            return True
            
        except Exception as e:
            print(f"❌ 发送失败：{e}")
            return False
    
    def get_recent_messages(self, contact: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """获取最近消息"""
        messages = []
        
        if not self.page:
            return messages
        
        try:
            # 如果有联系人，先打开对话
            if contact:
                search_box = self.page.locator('.search_input').first
                search_box.fill(contact)
                time.sleep(0.5)
                self.page.locator('.chat_list_item').first.click()
                time.sleep(0.5)
            
            # 获取消息列表
            message_elements = self.page.locator('.message_item').all()
            
            for elem in message_elements[:limit]:
                try:
                    msg_text = elem.text_content()
                    msg_time = elem.locator('.message_time').text_content() if elem.locator('.message_time').count() > 0 else ""
                    msg_type = "received" if "message_received" in elem.get_attribute('class') else "sent"
                    
                    messages.append({
                        'text': msg_text,
                        'time': msg_time,
                        'type': msg_type
                    })
                except:
                    continue
            
        except Exception as e:
            print(f"⚠️ 获取消息失败：{e}")
        
        return messages
    
    def close(self):
        """关闭浏览器"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("👋 浏览器已关闭")
    
    def __enter__(self):
        """上下文管理器进入"""
        self.launch()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.close()


def main():
    """主函数 - 测试用"""
    import argparse
    
    parser = argparse.ArgumentParser(description='个人微信 RPA 适配器')
    parser.add_argument('--account', default='main', help='账号标识 (main/secondary)')
    parser.add_argument('--login', action='store_true', help='扫码登录')
    parser.add_argument('--message', type=str, help='发送消息')
    parser.add_argument('--contact', type=str, default='filehelper', help='联系人')
    
    args = parser.parse_args()
    
    with WeChatPersonalAdapter(account=args.account) as wechat:
        if args.login:
            wechat.login()
        
        if args.message:
            wechat.send_message(args.contact, args.message)
        
        if not args.login and not args.message:
            # 仅启动，不操作
            print("✅ 微信已启动，请在浏览器中操作")
            print("⏳ 按 Ctrl+C 退出...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 退出")


if __name__ == "__main__":
    main()
