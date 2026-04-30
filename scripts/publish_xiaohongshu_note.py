#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书发布脚本 - 浏览器适配器版

太一 v4.0 - 使用浏览器适配器发布小红书笔记
定时执行：21:00
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
import sys

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'skills' / 'browser-adapter'))

from xiaohongshu_adapter import XiaohongshuAdapter


async def publish_xiaohongshu_note():
    """
    发布小红书笔记
    
    笔记：《太一 AGI v4.0 融合架构》
    """
    print("\n" + "="*60)
    print("📕 小红书笔记发布 - 浏览器适配器版")
    print("="*60)
    print(f"执行时间：{datetime.now().isoformat()}")
    
    # 笔记配置
    TITLE = '太一 AGI v4.0 融合架构 | 效率提升 14x🚀'
    
    CONTENT = '''今天完成了太一 v4.0 Phase 1+2，融合 Claude Code 精华！

🎯 核心突破
- 自动循环执行器：5 次重试后上报人类
- 庖丁 ROI 计算：实时成本追踪透明化
- 浏览器适配器层：绕过 API 限制，复用本地登录

📊 执行成果
- 工时：13 分钟（原估计 185 分钟，效率提升 14x）🚀
- 文件：10 文件 / ~60KB
- Git Commits：2 次推送

🌐 浏览器适配器层
灵感来自 bb-browser + bb-sites，实现三大适配器：
- PolymarketAdapter：下注/查询余额（解决私钥阻塞）
- WeChatAdapter：公众号发布/草稿管理
- XiaohongshuAdapter：笔记发布/数据分析

✅ 解决阻塞任务
- 知几首笔下注：API→浏览器+MetaMask
- 公众号发布：手动→浏览器自动化
- 小红书发布：手动→浏览器自动化

🔧 技术架构
太一核心（宪法 +8 Bot）
    ↓
浏览器适配器层（Playwright + CDP）
    ↓
平台适配器（Polymarket/WeChat/Xiaohongshu）
    ↓
目标网站（复用本地登录状态）

📈 核心洞察
bb-browser + bb-sites 的本质：不是"绕过防护"，而是 AI Agent 与 Web 的原生交互层

人类：浏览器 → 手动操作
AI：浏览器 → CDP 操控
结果相同，效率差 100x

🚀 下一步
- 知几首笔下注确认
- 公众号/小红书发布
- GitHub 爬虫开源

#太一 AGI #OpenClaw #AI 自动化 #浏览器自动化 #ClaudeCode #效率提升 #AI 工具 #技术分享
'''
    
    TOPICS = ['太一 AGI', 'OpenClaw', 'AI 自动化', '浏览器自动化', 'ClaudeCode', '效率提升', 'AI 工具', '技术分享']
    
    print(f"\n📋 笔记信息:")
    print(f"  标题：{TITLE}")
    print(f"  话题：{len(TOPICS)} 个")
    print(f"  字数：{len(CONTENT)} 字符")
    
    # 初始化适配器
    adapter = XiaohongshuAdapter(
        headless=False,
        user_data_dir=str(Path.home() / '.config' / 'google-chrome')
    )
    
    try:
        # 启动浏览器
        print("\n🚀 启动浏览器...")
        await adapter.launch()
        
        # 发布笔记
        print("\n📝 发布笔记...")
        result = await adapter.execute(
            action='publish_note',
            title=TITLE,
            content=CONTENT,
            images=[],  # 暂不上传图片，用户可手动添加
            topics=TOPICS
        )
        
        print(f"\n📋 发布结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 记录结果
        output = {
            'timestamp': datetime.now().isoformat(),
            'task': 'TASK-013',
            'task_name': '小红书笔记发布',
            'title': TITLE,
            'result': result
        }
        
        # 保存结果
        output_file = Path(__file__).parent.parent / 'xiaohongshu-data' / 'note_publish_result.json'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 结果已保存：{output_file}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 发布失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'failed',
            'error': str(e)
        }
    
    finally:
        await adapter.close()


async def main():
    """主函数"""
    result = await publish_xiaohongshu_note()
    
    print("\n" + "="*60)
    if result.get('status') == 'success':
        print("✅ 小红书笔记发布成功！")
    else:
        print("⚠️  发布结果待确认")
    print("="*60)
    
    return result


if __name__ == '__main__':
    asyncio.run(main())
