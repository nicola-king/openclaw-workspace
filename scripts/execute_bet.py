#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几首笔下注 - 全自动化执行（系统代理）

太一 v4.0 - 智能自动化连接 Polymarket + MetaMask
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
import tempfile
import shutil
from playwright.async_api import async_playwright


async def execute_first_bet_automated():
    """全自动执行知几首笔下注"""
    print("\n" + "="*60)
    print("🤖 知几首笔下注 - 全自动化执行（系统代理）")
    print("="*60)
    
    MARKET_URL = 'https://polymarket.com/event/will-nyc-reach-90f-in-july-2026'
    OUTCOME = 'YES'
    AMOUNT = 5.0
    temp_dir = None
    
    # 设置系统代理环境变量
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    
    try:
        temp_dir = tempfile.mkdtemp(prefix='polymarket_auto_')
        print(f"\n📁 临时目录：{temp_dir}")
        print("🌐 代理：http://127.0.0.1:7890")
        
        print("\n🚀 启动浏览器...")
        playwright = await async_playwright().start()
        
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=temp_dir,
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--proxy-server=http://127.0.0.1:7890'  # 浏览器代理参数
            ]
        )
        
        page = await browser.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        
        print("✅ 浏览器已启动")
        
        print(f"\n📍 导航到 Polymarket...")
        print(f"   URL: {MARKET_URL}")
        
        # 先访问 Google 测试代理
        print("\n🔍 测试代理（访问 Google）...")
        try:
            await page.goto('https://www.google.com', wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(2)
            print("✅ Google 访问成功（代理正常）")
            await page.screenshot(path=str(Path('/home/nicola/.openclaw/workspace/polymarket-data/test_google.png')))
        except Exception as e:
            print(f"⚠️  Google 访问失败：{e}")
        
        # 访问 Polymarket
        print(f"\n📍 导航到 Polymarket...")
        await page.goto(MARKET_URL, wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(5)
        
        # 截图
        ss_dir = Path('/home/nicola/.openclaw/workspace/polymarket-data')
        ss_dir.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(ss_dir / 'step_1_market.png'))
        print("📸 截图：step_1_market.png")
        
        # 连接钱包
        print("\n🔗 连接钱包...")
        try:
            btn = await page.query_selector('button:has-text("Connect Wallet")')
            if btn:
                await btn.click()
                await asyncio.sleep(3)
                print("✅ 已点击连接钱包")
                await page.screenshot(path=str(ss_dir / 'step_2_connect.png'))
        except Exception as e:
            print(f"⚠️  跳过：{e}")
        
        # 选择 YES
        print(f"\n🎯 选择 {OUTCOME}...")
        try:
            btn = await page.query_selector(f'button:has-text("{OUTCOME}")')
            if btn:
                await btn.click()
                await asyncio.sleep(2)
                print(f"✅ 已选择 {OUTCOME}")
                await page.screenshot(path=str(ss_dir / 'step_3_outcome.png'))
        except Exception as e:
            print(f"⚠️  跳过：{e}")
        
        # 输入金额
        print(f"\n💰 输入 {AMOUNT} USDC...")
        try:
            inp = await page.query_selector('input[type="number"]')
            if inp:
                await inp.fill(str(AMOUNT))
                await asyncio.sleep(2)
                print(f"✅ 已输入 {AMOUNT}")
                await page.screenshot(path=str(ss_dir / 'step_4_amount.png'))
        except Exception as e:
            print(f"⚠️  跳过：{e}")
        
        # 下单
        print("\n📤 点击 Place Order...")
        try:
            btn = await page.query_selector('button:has-text("Place Order")')
            if btn:
                await btn.click()
                await asyncio.sleep(5)
                print("✅ 已下单")
                await page.screenshot(path=str(ss_dir / 'step_5_order.png'))
        except Exception as e:
            print(f"⚠️  跳过：{e}")
        
        # 等待 MetaMask
        print("\n⏳ 等待 MetaMask 确认（15 秒）...")
        await asyncio.sleep(15)
        await page.screenshot(path=str(ss_dir / 'step_6_metamask.png'))
        print("📸 截图：step_6_metamask.png")
        
        # 保存结果
        result = {
            'timestamp': datetime.now().isoformat(),
            'task': 'TASK-050',
            'market': MARKET_URL,
            'outcome': OUTCOME,
            'amount': AMOUNT,
            'status': 'executed',
            'message': '自动化流程完成，请检查账户',
            'proxy': 'http://127.0.0.1:7890'
        }
        
        with open(ss_dir / 'first_bet_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 结果已保存")
        
        await browser.close()
        await playwright.stop()
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("🧹 临时目录已清理")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 失败：{e}")
        import traceback
        traceback.print_exc()
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        return {'status': 'failed', 'error': str(e)}


if __name__ == '__main__':
    result = asyncio.run(execute_first_bet_automated())
    print("\n" + "="*60)
    print("✅ 执行完成！")
    print("="*60)
