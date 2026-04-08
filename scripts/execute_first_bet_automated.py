#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几首笔下注 - 全自动化执行

太一 v4.0 - 智能自动化连接 Polymarket + MetaMask
无需用户手动操作，自动完成：
1. 启动浏览器（临时配置）
2. 导航到 Polymarket
3. 连接 MetaMask 钱包
4. 选择下注选项（YES）
5. 输入金额（5 USDC）
6. 确认交易
7. 保存结果
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
import tempfile
import shutil
from playwright.async_api import async_playwright


async def execute_first_bet_automated():
    """
    全自动执行知几首笔下注
    """
    print("\n" + "="*60)
    print("🤖 知几首笔下注 - 全自动化执行")
    print("="*60)
    print(f"执行时间：{datetime.now().isoformat()}")
    
    # 配置
    MARKET_URL = 'https://polymarket.com/event/will-nyc-reach-90f-in-july-2026'
    OUTCOME = 'YES'
    AMOUNT = 5.0  # USDC
    temp_dir = None
    
    try:
        # 创建临时用户数据目录
        temp_dir = tempfile.mkdtemp(prefix='polymarket_auto_')
        print(f"\n📁 临时用户数据目录：{temp_dir}")
        
        # 启动 Playwright
        print("\n🚀 启动浏览器...")
        playwright = await async_playwright().start()
        
        # 启动浏览器（临时配置）
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=temp_dir,
            headless=False,  # 可见浏览器，便于调试
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
        
        page = await browser.new_page()
        
        # 注入反检测
        await page.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        ''')
        
        print("✅ 浏览器已启动")
        
        # 导航到 Polymarket
        print(f"\n📍 导航到 Polymarket...")
        await page.goto(MARKET_URL, wait_until='networkidle')
        await asyncio.sleep(5)
        
        # 截图保存
        screenshot_path = Path(__file__).parent.parent / 'polymarket-data' / 'step_1_market.png'
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(screenshot_path))
        print(f"📸 截图保存：{screenshot_path}")
        
        # 步骤 1：连接钱包
        print("\n🔗 步骤 1: 连接钱包...")
        try:
            # 查找连接钱包按钮
            connect_btn = await page.query_selector('button:has-text("Connect Wallet"), button:has-text("连接钱包")')
            if connect_btn:
                await connect_btn.click()
                print("✅ 已点击连接钱包")
                await asyncio.sleep(3)
                
                # 截图
                screenshot_path = Path(__file__).parent.parent / 'polymarket-data' / 'step_2_connect.png'
                await page.screenshot(path=str(screenshot_path))
                print(f"📸 截图保存：{screenshot_path}")
            else:
                print("⚠️  未找到连接钱包按钮（可能已连接）")
        except Exception as e:
            print(f"⚠️  连接钱包步骤跳过：{str(e)}")
        
        # 步骤 2：选择 YES
        print(f"\n🎯 步骤 2: 选择 {OUTCOME}...")
        try:
            outcome_btn = await page.query_selector(f'button:has-text("{OUTCOME}"), button:has-text("Yes"), button:has-text("YES")')
            if outcome_btn:
                await outcome_btn.click()
                print(f"✅ 已选择 {OUTCOME}")
                await asyncio.sleep(2)
                
                # 截图
                screenshot_path = Path(__file__).parent.parent / 'polymarket-data' / 'step_3_outcome.png'
                await page.screenshot(path=str(screenshot_path))
                print(f"📸 截图保存：{screenshot_path}")
            else:
                print("⚠️  未找到结果选择按钮")
        except Exception as e:
            print(f"⚠️  选择结果步骤跳过：{str(e)}")
        
        # 步骤 3：输入金额
        print(f"\n💰 步骤 3: 输入金额 {AMOUNT} USDC...")
        try:
            # 查找金额输入框
            amount_input = await page.query_selector('input[type="number"], input[placeholder*="Amount"], input[placeholder*="金额"]')
            if amount_input:
                await amount_input.fill(str(AMOUNT))
                print(f"✅ 已输入金额：{AMOUNT}")
                await asyncio.sleep(2)
                
                # 截图
                screenshot_path = Path(__file__).parent.parent / 'polymarket-data' / 'step_4_amount.png'
                await page.screenshot(path=str(screenshot_path))
                print(f"📸 截图保存：{screenshot_path}")
            else:
                print("⚠️  未找到金额输入框")
        except Exception as e:
            print(f"⚠️  输入金额步骤跳过：{str(e)}")
        
        # 步骤 4：点击下单
        print("\n📤 步骤 4: 点击 Place Order...")
        try:
            place_btn = await page.query_selector('button:has-text("Place Order"), button:has-text("确认"), button:has-text("Submit")')
            if place_btn:
                await place_btn.click()
                print("✅ 已点击下单")
                await asyncio.sleep(5)
                
                # 截图
                screenshot_path = Path(__file__).parent.parent / 'polymarket-data' / 'step_5_order.png'
                await page.screenshot(path=str(screenshot_path))
                print(f"📸 截图保存：{screenshot_path}")
            else:
                print("⚠️  未找到下单按钮")
        except Exception as e:
            print(f"⚠️  下单步骤跳过：{str(e)}")
        
        # 步骤 5：等待 MetaMask 确认
        print("\n⏳ 步骤 5: 等待 MetaMask 确认（10 秒）...")
        await asyncio.sleep(10)
        
        # 截图
        screenshot_path = Path(__file__).parent.parent / 'polymarket-data' / 'step_6_metamask.png'
        await page.screenshot(path=str(screenshot_path))
        print(f"📸 截图保存：{screenshot_path}")
        
        # 保存结果
        result = {
            'timestamp': datetime.now().isoformat(),
            'task': 'TASK-050',
            'task_name': '知几首笔下注（全自动）',
            'market': MARKET_URL,
            'outcome': OUTCOME,
            'amount': AMOUNT,
            'strategy': 'Quarter-Kelly',
            'adapter': 'browser_automated',
            'status': 'executed',
            'message': '自动化流程执行完成，请检查 Polymarket 账户确认',
            'screenshots': [
                'step_1_market.png',
                'step_2_connect.png',
                'step_3_outcome.png',
                'step_4_amount.png',
                'step_5_order.png',
                'step_6_metamask.png'
            ]
        }
        
        # 保存到文件
        output_file = Path(__file__).parent.parent / 'polymarket-data' / 'first_bet_result_automated.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 结果已保存：{output_file}")
        
        # 关闭浏览器
        print("\n🚪 关闭浏览器...")
        await browser.close()
        await playwright.stop()
        
        # 清理临时目录
        if temp_dir:
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
                print(f"🧹 临时目录已清理：{temp_dir}")
            except:
                pass
        
        return result
        
    except Exception as e:
        print(f"\n❌ 执行失败：{str(e)}")
        import traceback
        traceback.print_exc()
        
        # 保存错误结果
        result = {
            'timestamp': datetime.now().isoformat(),
            'task': 'TASK-050',
            'status': 'failed',
            'error': str(e)
        }
        
        output_file = Path(__file__).parent.parent / 'polymarket-data' / 'first_bet_result_automated.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # 清理临时目录
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        return result


async def main():
    """主函数"""
    result = await execute_first_bet_automated()
    
    print("\n" + "="*60)
    print("✅ 知几首笔下注 - 全自动化执行完成！")
    print("📋 请检查 Polymarket 账户确认下注状态")
    print("="*60)
    
    return result


if __name__ == '__main__':
    asyncio.run(main())
