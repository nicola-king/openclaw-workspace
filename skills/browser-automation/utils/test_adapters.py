#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器适配器层 - 测试脚本

太一 v4.0 - 测试所有平台适配器
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime


async def test_polymarket():
    """测试 Polymarket 适配器"""
    print("\n" + "="*60)
    print("🎯 测试 Polymarket 适配器")
    print("="*60)
    
    from polymarket_adapter import PolymarketAdapter
    
    adapter = PolymarketAdapter(
        headless=False,
        user_data_dir=str(Path.home() / '.config' / 'google-chrome')
    )
    
    try:
        await adapter.launch()
        
        # 测试查询余额
        print("\n📊 测试查询余额...")
        balance_result = await adapter.execute(action='get_balance')
        print(f"余额查询结果：{json.dumps(balance_result, indent=2, ensure_ascii=False)}")
        
        # 测试下注（示例市场）
        print("\n💰 测试下注...")
        bet_result = await adapter.execute(
            action='place_bet',
            market_url='https://polymarket.com/event/will-nyc-reach-90f-in-july-2026',
            outcome='YES',
            amount=5
        )
        print(f"下注结果：{json.dumps(bet_result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
    finally:
        await adapter.close()


async def test_wechat():
    """测试微信适配器"""
    print("\n" + "="*60)
    print("💬 测试微信适配器")
    print("="*60)
    
    from wechat_adapter import WeChatAdapter
    
    adapter = WeChatAdapter(
        headless=False,
        user_data_dir=str(Path.home() / '.config' / 'google-chrome')
    )
    
    try:
        await adapter.launch()
        
        # 测试发布文章
        print("\n📝 测试发布文章...")
        publish_result = await adapter.execute(
            action='publish_article',
            title='太一 AGI v4.0 融合架构',
            content='<h1>太一 v4.0</h1><p>融合 Claude Code 精华...</p>'
        )
        print(f"发布结果：{json.dumps(publish_result, indent=2, ensure_ascii=False)}")
        
        # 测试获取草稿
        print("\n📋 测试获取草稿...")
        drafts_result = await adapter.execute(action='get_drafts')
        print(f"草稿列表：{json.dumps(drafts_result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
    finally:
        await adapter.close()


async def test_xiaohongshu():
    """测试小红书适配器"""
    print("\n" + "="*60)
    print("📕 测试小红书适配器")
    print("="*60)
    
    from xiaohongshu_adapter import XiaohongshuAdapter
    
    adapter = XiaohongshuAdapter(
        headless=False,
        user_data_dir=str(Path.home() / '.config' / 'google-chrome')
    )
    
    try:
        await adapter.launch()
        
        # 测试发布笔记
        print("\n📝 测试发布笔记...")
        publish_result = await adapter.execute(
            action='publish_note',
            title='太一 AGI v4.0 融合 Claude Code 精华',
            content='今天完成了太一 v4.0 架构升级，融合了 Claude Code 的自动重试机制和 ROI 透明化理念...',
            images=[],
            topics=['AI', '太一 AGI', 'OpenClaw']
        )
        print(f"发布结果：{json.dumps(publish_result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
    finally:
        await adapter.close()


async def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🚀 浏览器适配器层 - 综合测试")
    print("="*60)
    print(f"测试时间：{datetime.now().isoformat()}")
    
    # 选择测试
    print("\n选择测试:")
    print("1. Polymarket 适配器")
    print("2. 微信适配器")
    print("3. 小红书适配器")
    print("4. 全部测试")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == '1':
        await test_polymarket()
    elif choice == '2':
        await test_wechat()
    elif choice == '3':
        await test_xiaohongshu()
    elif choice == '4':
        await test_polymarket()
        await test_wechat()
        await test_xiaohongshu()
    else:
        print("❌ 无效选择")
    
    print("\n" + "="*60)
    print("✅ 测试完成")
    print("="*60)


if __name__ == '__main__':
    asyncio.run(main())
