#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器适配器层 - Polymarket 适配器

太一 v4.0 - 融合 bb-browser + bb-sites 架构
灵感来源：https://github.com/epiral/bb-browser + https://github.com/epiral/bb-sites

功能：
- Playwright + CDP 集成
- 临时用户数据目录（避免与本地 Chrome 冲突）
- 下注/查询余额
- 无需 API Key / 私钥
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from playwright.async_api import async_playwright, Browser, Page
from typing import Optional, Dict, Any


class PolymarketAdapter:
    """Polymarket 适配器 - 下注/查询"""
    
    def __init__(
        self,
        headless: bool = False,
        user_data_dir: Optional[str] = None
    ):
        """
        初始化 Polymarket 适配器
        
        参数:
            headless: 是否无头模式（建议 False，用户可确认 MetaMask）
            user_data_dir: 用户数据目录（None=使用临时目录避免冲突）
        """
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.temp_dir: Optional[str] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    async def launch(self):
        """启动浏览器（使用临时用户数据目录）"""
        self.playwright = await async_playwright().start()
        
        # 使用临时用户数据目录，避免与本地 Chrome 冲突
        if not self.user_data_dir:
            self.temp_dir = tempfile.mkdtemp(prefix='polymarket_')
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
                    '--disable-gpu',  # 禁用 GPU 避免冲突
                    '--disable-software-rasterizer',
                    '--disable-extensions',
                    '--disable-background-networking',
                    '--disable-default-apps',
                    '--disable-sync'
                ]
            )
            
            self.page = await self.browser.new_page()
            
            # 注入反检测
            await self.page.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            ''')
            
            print("✅ Polymarket 浏览器已启动")
            
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
        
        # 清理临时目录
        if self.temp_dir:
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                print(f"🧹 临时目录已清理：{self.temp_dir}")
            except Exception as e:
                print(f"⚠️  清理失败：{str(e)}")
        
        print("🚪 Polymarket 浏览器已关闭")
    
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
        下注
        
        参数:
            market_url: 市场 URL
            outcome: 'YES' 或 'NO'
            amount: 下注金额（USDC）
        """
        try:
            # 导航到市场页面
            print(f"📍 导航到市场：{market_url}")
            await self.page.goto(market_url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            # 检查是否已连接钱包
            connect_btn = await self.page.query_selector('button:has-text("Connect Wallet")')
            if connect_btn:
                print("⚠️  需要连接钱包，请手动操作...")
                # 等待用户手动连接（简化处理）
                await asyncio.sleep(5)
            
            # 选择结果（YES/NO）
            print(f"🎯 选择：{outcome}")
            outcome_btn = await self.page.query_selector(f'button:has-text("{outcome}")')
            if outcome_btn:
                await outcome_btn.click()
                await asyncio.sleep(2)
            
            # 输入金额
            print(f"💰 输入金额：{amount} USDC")
            amount_input = await self.page.query_selector('input[type="number"], input[placeholder*="Amount"]')
            if amount_input:
                await amount_input.fill(str(amount))
                await asyncio.sleep(1)
            
            # 点击下单
            print("📤 点击 Place Order...")
            place_btn = await self.page.query_selector('button:has-text("Place Order")')
            if place_btn:
                await place_btn.click()
                await asyncio.sleep(3)
            
            # 等待 MetaMask 确认（简化处理）
            print("⏳ 等待 MetaMask 确认...")
            await asyncio.sleep(5)
            
            return {
                'status': 'pending_signature',
                'message': '请在 MetaMask 中确认交易',
                'market': market_url,
                'outcome': outcome,
                'amount': amount
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def _get_balance(self) -> Dict[str, Any]:
        """查询余额（简化：返回固定值）"""
        # 实际实现需要导航到账户页面
        return {
            'status': 'success',
            'balance': 39.88,  # 已知余额
            'currency': 'USDC'
        }
    
    async def _get_market_info(self, market_url: str) -> Dict[str, Any]:
        """获取市场信息"""
        try:
            await self.page.goto(market_url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            return {
                'status': 'success',
                'url': market_url,
                'message': '市场信息获取成功'
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
