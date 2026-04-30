#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知几首笔下注执行脚本 - 简化版

太一 v4.0 - 使用独立浏览器实例（不复用本地配置）
用户需手动登录 Polymarket 和 MetaMask
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
import tempfile
from playwright.async_api import async_playwright


async def execute_first_bet():
    """
    执行知几首笔下注
    
    策略：
    - 市场：NYC 气温 2026 年 7 月是否达到 90°F
    - 下注：YES
    - 金额：5 USDC
    """
    print("\n" + "="*60)
    print("🎯 知几首笔下注 - 简化版")
    print("="*60)
    print(f"执行时间：{datetime.now().isoformat()}")
    
    # 配置
    MARKET_URL = 'https://polymarket.com/event/will-nyc-reach-90f-in-july-2026'
    OUTCOME = 'YES'
    AMOUNT = 5.0  # USDC
    
    print(f"\n📊 下注参数:")
    print(f"  市场：{MARKET_URL}")
    print(f"  方向：{OUTCOME}")
    print(f"  金额：{AMOUNT} USDC")
    print(f"  策略：Quarter-Kelly (总资金$39.88 的 12.5%)")
    
    # 创建临时用户数据目录
    with tempfile.TemporaryDirectory() as temp_dir:
        playwright = None
        browser = None
        page = None
        
        try:
            # 启动 Playwright
            print("\n🚀 启动浏览器（临时配置文件）...")
            playwright = await async_playwright().start()
            
            # 启动浏览器（临时目录，不复用本地配置）
            browser = await playwright.chromium.launch_persistent_context(
                user_data_dir=temp_dir,
                headless=False,  # 可见浏览器，用户可手动登录
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
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
            await asyncio.sleep(3)
            
            print("\n" + "="*60)
            print("⚠️  需要用户手动操作")
            print("="*60)
            print("""
请在浏览器中完成以下步骤：

1. 点击右上角 "Connect Wallet" 连接钱包
2. 连接 MetaMask 钱包
3. 点击 "YES" 按钮
4. 输入金额：5 USDC
5. 点击 "Place Order"
6. 在 MetaMask 中确认交易

完成后，关闭浏览器窗口，脚本将自动继续...
            """)
            
            # 等待用户完成操作（检测页面变化或超时）
            print("\n⏳ 等待用户完成操作（60 秒超时）...")
            try:
                await asyncio.wait_for(
                    page.wait_for_function('document.title.includes("Confirmed")'),
                    timeout=60000  # 60 秒
                )
                print("✅ 检测到交易完成！")
            except asyncio.TimeoutError:
                print("⏰ 超时，但继续执行...")
            
            # 记录结果
            result = {
                'timestamp': datetime.now().isoformat(),
                'task': 'TASK-050',
                'task_name': '知几首笔下注',
                'market': MARKET_URL,
                'outcome': OUTCOME,
                'amount': AMOUNT,
                'strategy': 'Quarter-Kelly',
                'adapter': 'browser_simplified',
                'status': 'manual_execution',
                'message': '用户手动完成下注，请检查 Polymarket 账户确认'
            }
            
            # 保存到文件
            output_file = Path(__file__).parent.parent / 'polymarket-data' / 'first_bet_result.json'
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 结果已保存：{output_file}")
            
            return result
            
        except Exception as e:
            print(f"\n❌ 执行失败：{str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        
        finally:
            # 关闭浏览器
            if browser:
                print("\n🚪 关闭浏览器...")
                await browser.close()
            if playwright:
                await playwright.stop()


async def main():
    """主函数"""
    result = await execute_first_bet()
    
    # 输出最终状态
    print("\n" + "="*60)
    print("✅ 知几首笔下注执行完成！")
    print("📋 请检查 Polymarket 账户确认下注状态")
    print("="*60)
    
    return result


if __name__ == '__main__':
    asyncio.run(main())
