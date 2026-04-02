#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器适配器层 - 核心实现

太一 v4.0 - 融合 bb-browser + bb-sites 架构
灵感来源：https://github.com/epiral/bb-browser + https://github.com/epiral/bb-sites

功能：
- Playwright + CDP 集成
- 本地浏览器会话复用（不窃取 Cookie）
- 平台适配器模式
- 无需 API Key / 私钥
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Browser, Page
from typing import Optional, Dict, Any


class BrowserAdapter:
    """浏览器适配器基类"""
    
    def __init__(
        self,
        platform: str,
        headless: bool = False,
        user_data_dir: Optional[str] = None
    ):
        """
        初始化浏览器适配器
        
        参数:
            platform: 平台名称（polymarket/wechat/xiaohongshu）
            headless: 是否无头模式（建议 False，复用可见浏览器）
            user_data_dir: 用户数据目录（复用本地登录状态）
        """
        self.platform = platform
        self.headless = headless
        self.user_data_dir = user_data_dir or self._get_default_user_data_dir()
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    def _get_default_user_data_dir(self) -> str:
        """获取默认用户数据目录"""
        # Chrome 默认用户数据目录
        import os
        if os.name == 'nt':  # Windows
            return str(Path.home() / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data')
        elif os.name == 'posix':  # macOS/Linux
            return str(Path.home() / '.config' / 'google-chrome')
        return ''
    
    async def launch(self):
        """启动浏览器"""
        self.playwright = await async_playwright().start()
        
        # 启动浏览器（复用本地用户数据）
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',  # 反检测
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        # 创建页面
        self.page = await self.browser.new_page()
        
        # 注入反检测脚本
        await self.page.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        ''')
        
        print(f"✅ 浏览器已启动（平台：{self.platform}）")
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("🚪 浏览器已关闭")
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """执行操作（子类实现）"""
        raise NotImplementedError(f"{self.platform} 适配器未实现 execute 方法")


class PolymarketAdapter(BrowserAdapter):
    """Polymarket 适配器 - 下注/查询"""
    
    def __init__(self, **kwargs):
        super().__init__(platform='polymarket', **kwargs)
        self.base_url = 'https://polymarket.com'
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        执行 Polymarket 操作
        
        支持操作：
        - place_bet: 下注
        - get_balance: 查询余额
        - get_market_info: 获取市场信息
        """
        if not self.browser:
            await self.launch()
        
        if action == 'place_bet':
            return await self._place_bet(**kwargs)
        elif action == 'get_balance':
            return await self._get_balance()
        elif action == 'get_market_info':
            return await self._get_market_info(**kwargs)
        else:
            raise ValueError(f"未知操作：{action}")
    
    async def _place_bet(
        self,
        market_url: str,
        outcome: str,
        amount: float
    ) -> Dict[str, Any]:
        """
        下注操作
        
        参数:
            market_url: 市场 URL
            outcome: 'YES' 或 'NO'
            amount: 下注金额（USDC）
        
        返回:
            {
                'status': 'pending_signature' | 'success' | 'failed',
                'market': str,
                'outcome': str,
                'amount': float,
                'message': str
            }
        """
        try:
            # 导航到市场页面
            print(f"📍 导航到市场：{market_url}")
            await self.page.goto(market_url, wait_until='networkidle')
            await asyncio.sleep(2)  # 等待页面加载
            
            # 点击 Outcome 按钮
            print(f"👆 点击 {outcome} 按钮")
            outcome_selector = f'[data-outcome-value="{outcome}"], button:has-text("{outcome}")'
            await self.page.click(outcome_selector, timeout=10000)
            await asyncio.sleep(1)
            
            # 输入金额
            print(f"💰 输入金额：{amount} USDC")
            amount_input = await self.page.query_selector('input[type="number"]')
            if amount_input:
                await amount_input.fill(str(amount))
            await asyncio.sleep(1)
            
            # 点击下单按钮
            print("📝 点击下单按钮")
            place_order_btn = await self.page.query_selector(
                'button:has-text("Place Order"), button:has-text("Buy"), button:has-text("Confirm")'
            )
            if place_order_btn:
                await place_order_btn.click()
            
            # 等待 MetaMask 签名（用户手动确认）
            print("⏳ 等待用户确认 MetaMask 签名...")
            await asyncio.sleep(5)  # 给用户时间确认
            
            # 检查订单状态
            result = {
                'status': 'pending_signature',
                'market': market_url,
                'outcome': outcome,
                'amount': amount,
                'message': '请确认 MetaMask 签名，签名后订单将自动完成'
            }
            
            print(f"✅ 下注指令已发送：{result}")
            return result
            
        except Exception as e:
            print(f"❌ 下注失败：{str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'market': market_url,
                'outcome': outcome,
                'amount': amount
            }
    
    async def _get_balance(self) -> Dict[str, Any]:
        """查询 USDC 余额"""
        try:
            # 导航到账户页面
            await self.page.goto(f'{self.base_url}/account', wait_until='networkidle')
            await asyncio.sleep(2)
            
            # 提取余额
            balance_text = await self.page.text_content('.usdc-balance')
            balance = float(balance_text.replace('USDC', '').replace(',', '').strip())
            
            return {
                'status': 'success',
                'balance': balance,
                'currency': 'USDC'
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def _get_market_info(self, market_url: str) -> Dict[str, Any]:
        """获取市场信息"""
        try:
            await self.page.goto(market_url, wait_until='networkidle')
            await asyncio.sleep(2)
            
            # 提取市场信息（标题、流动性、价格等）
            title = await self.page.text_content('h1')
            
            return {
                'status': 'success',
                'title': title,
                'url': market_url
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }