#!/usr/bin/env python3
"""
🎮 Discord Bot 启动脚本

运行此脚本启动 Discord Bot

作者：太一 AGI
创建：2026-04-11
"""

import asyncio
from discord_client import DiscordClient


def main():
    """主函数"""
    print("="*60)
    print("🎮 启动 Discord Bot")
    print("="*60)
    
    # 初始化客户端
    client = DiscordClient()
    
    # 检查配置
    if not client.config:
        print("\n❌ 配置文件不存在")
        print("   请创建：~/.openclaw/workspace/config/discord/config.json")
        return 1
    
    # 获取 Token
    token = client.config.get('token')
    if not token:
        print("\n❌ Bot Token 未配置")
        print("   请在配置文件中填写 token 字段")
        return 1
    
    print("\n🚀 启动 Bot...")
    print("   按 Ctrl+C 停止")
    print()
    
    # 运行 Bot
    client.run(token)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
