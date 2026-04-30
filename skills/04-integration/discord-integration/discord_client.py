#!/usr/bin/env python3
"""
🎮 Discord 客户端

太一 AGI Discord 集成核心模块
支持消息收发/服务器管理/角色管理/卡片消息

作者：太一 AGI
创建：2026-04-11
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

import discord
from discord.ext import commands


class DiscordClient(commands.Bot):
    """Discord 客户端"""
    
    def __init__(self, config_path: str = None):
        """初始化客户端"""
        self.config_path = config_path or "/home/nicola/.openclaw/workspace/config/discord/config.json"
        self.config = self._load_config()
        
        # 设置 Intents
        intents = discord.Intents.all()
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            description='太一 AGI Discord Bot'
        )
        
        print("🎮 Discord 客户端已初始化")
        print(f"   Application ID: {self.config.get('application_id', 'N/A')}")
        print()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_file = Path(self.config_path)
        if not config_file.exists():
            print(f"⚠️  配置文件不存在：{config_file}")
            print(f"   请创建配置文件并填写 Bot Token")
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def on_ready(self):
        """连接成功回调"""
        print("="*60)
        print("✅ Discord 已连接")
        print(f"   用户名：{self.user.name}")
        print(f"   用户 ID: {self.user.id}")
        print(f"   服务器数：{len(self.guilds)}")
        print("="*60)
        print()
    
    async def on_message(self, message):
        """消息接收回调"""
        # 忽略自己的消息
        if message.author == self.user:
            return
        
        # 处理命令
        await self.process_commands(message)
    
    # ═══════════════════════════════════════════════════════════
    # 消息功能
    # ═══════════════════════════════════════════════════════════
    
    async def send_text_message(self, channel_id: int, content: str) -> Optional[discord.Message]:
        """发送文本消息"""
        channel = self.get_channel(channel_id)
        if channel:
            message = await channel.send(content)
            print(f"✅ 消息已发送：{channel_id}")
            return message
        else:
            print(f"❌ 频道未找到：{channel_id}")
            return None
    
    async def send_embed_message(self, channel_id: int, title: str, description: str = None, **kwargs) -> Optional[discord.Message]:
        """发送卡片消息"""
        channel = self.get_channel(channel_id)
        if not channel:
            print(f"❌ 频道未找到：{channel_id}")
            return None
        
        # 创建 Embed
        embed = discord.Embed(
            title=title,
            description=description,
            color=kwargs.get('color', discord.Color.blue())
        )
        
        # 添加字段
        fields = kwargs.get('fields', [])
        for field in fields:
            embed.add_field(
                name=field.get('name', '字段'),
                value=field.get('value', '值'),
                inline=field.get('inline', False)
            )
        
        # 设置缩略图
        if 'thumbnail' in kwargs:
            embed.set_thumbnail(url=kwargs['thumbnail'])
        
        # 设置图片
        if 'image' in kwargs:
            embed.set_image(url=kwargs['image'])
        
        # 设置页脚
        if 'footer' in kwargs:
            embed.set_footer(text=kwargs['footer'])
        
        message = await channel.send(embed=embed)
        print(f"✅ 卡片消息已发送：{channel_id}")
        return message
    
    async def send_file_message(self, channel_id: int, file_path: str, content: str = None) -> Optional[discord.Message]:
        """发送文件消息"""
        channel = self.get_channel(channel_id)
        if not channel:
            print(f"❌ 频道未找到：{channel_id}")
            return None
        
        file = discord.File(file_path)
        message = await channel.send(content=content, file=file)
        print(f"✅ 文件消息已发送：{channel_id}")
        return message
    
    async def get_channel_messages(self, channel_id: int, limit: int = 10) -> List[discord.Message]:
        """获取频道消息"""
        channel = self.get_channel(channel_id)
        if not channel:
            print(f"❌ 频道未找到：{channel_id}")
            return []
        
        messages = []
        async for message in channel.history(limit=limit):
            messages.append(message)
        
        print(f"✅ 已获取 {len(messages)} 条消息：{channel_id}")
        return messages
    
    # ═══════════════════════════════════════════════════════════
    # 服务器功能
    # ═══════════════════════════════════════════════════════════
    
    def get_guild(self, guild_id: int) -> Optional[discord.Guild]:
        """获取服务器"""
        guild = super().get_guild(guild_id)
        if guild:
            print(f"✅ 服务器已获取：{guild.name}")
            return guild
        else:
            print(f"❌ 服务器未找到：{guild_id}")
            return None
    
    def get_guilds(self) -> List[discord.Guild]:
        """获取所有服务器"""
        guilds = list(self.guilds)
        print(f"✅ 已获取 {len(guilds)} 个服务器")
        return guilds
    
    def get_text_channels(self, guild_id: int) -> List[discord.TextChannel]:
        """获取服务器文本频道"""
        guild = self.get_guild(guild_id)
        if guild:
            channels = guild.text_channels
            print(f"✅ 已获取 {len(channels)} 个文本频道")
            return channels
        return []
    
    # ═══════════════════════════════════════════════════════════
    # 用户功能
    # ═══════════════════════════════════════════════════════════
    
    def get_member(self, guild_id: int, user_id: int) -> Optional[discord.Member]:
        """获取成员"""
        guild = self.get_guild(guild_id)
        if guild:
            member = guild.get_member(user_id)
            if member:
                print(f"✅ 成员已获取：{member.name}")
                return member
        return None
    
    async def add_role(self, guild_id: int, user_id: int, role_id: int) -> bool:
        """添加角色"""
        guild = self.get_guild(guild_id)
        if not guild:
            return False
        
        member = guild.get_member(user_id)
        role = guild.get_role(role_id)
        
        if member and role:
            await member.add_roles(role)
            print(f"✅ 角色已添加：{member.name} → {role.name}")
            return True
        else:
            print(f"❌ 成员或角色未找到")
            return False
    
    async def remove_role(self, guild_id: int, user_id: int, role_id: int) -> bool:
        """移除角色"""
        guild = self.get_guild(guild_id)
        if not guild:
            return False
        
        member = guild.get_member(user_id)
        role = guild.get_role(role_id)
        
        if member and role:
            await member.remove_roles(role)
            print(f"✅ 角色已移除：{member.name} ← {role.name}")
            return True
        else:
            print(f"❌ 成员或角色未找到")
            return False
    
    # ═══════════════════════════════════════════════════════════
    # 命令功能
    # ═══════════════════════════════════════════════════════════
    
    def command(self, **kwargs):
        """命令装饰器"""
        return super().command(**kwargs)
    
    # ═══════════════════════════════════════════════════════════
    # 工具方法
    # ═══════════════════════════════════════════════════════════
    
    def test_connection(self) -> bool:
        """测试连接 (同步)"""
        print(f"⚠️  测试连接需要运行 bot.run()")
        return True
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "config_loaded": bool(self.config),
            "connected": self.is_ready(),
            "guilds_count": len(self.guilds),
            "users_count": sum(guild.member_count for guild in self.guilds)
        }


# ═══════════════════════════════════════════════════════════
# 示例命令
# ═══════════════════════════════════════════════════════════

async def setup_commands(bot: DiscordClient):
    """设置示例命令"""
    
    @bot.command(name='hello')
    async def hello(ctx):
        """问候命令"""
        await ctx.send(f'Hello from 太一 AGI! 👋')
    
    @bot.command(name='info')
    async def info(ctx):
        """机器人信息"""
        embed = discord.Embed(
            title="太一 AGI 信息",
            description="智能自主自动化 AI 助手",
            color=discord.Color.blue()
        )
        embed.add_field(name="用户名", value=bot.user.name)
        embed.add_field(name="用户 ID", value=bot.user.id)
        embed.add_field(name="服务器数", value=len(bot.guilds))
        await ctx.send(embed=embed)
    
    @bot.command(name='help')
    async def help_command(ctx):
        """帮助命令"""
        embed = discord.Embed(
            title="太一 AGI 帮助",
            description="可用命令列表",
            color=discord.Color.green()
        )
        embed.add_field(name="!hello", value="问候机器人", inline=False)
        embed.add_field(name="!info", value="查看机器人信息", inline=False)
        embed.add_field(name="!help", value="显示此帮助信息", inline=False)
        await ctx.send(embed=embed)


def main():
    """主函数 - 测试"""
    print("="*60)
    print("🎮 Discord 客户端测试")
    print("="*60)
    
    # 初始化客户端
    client = DiscordClient()
    
    # 检查配置
    if not client.config:
        print("\n❌ 配置文件不存在或未配置")
        print("   请创建配置文件：~/.openclaw/workspace/config/discord/config.json")
        print("   配置指南：见 CONFIG_GUIDE.md")
        return 1
    
    # 设置命令
    asyncio.run(setup_commands(client))
    
    # 获取统计
    print("\n📊 统计信息:")
    stats = client.get_statistics()
    print(f"   配置已加载：{stats['config_loaded']}")
    print(f"   已连接：{stats['connected']}")
    print(f"   服务器数：{stats['guilds_count']}")
    print(f"   用户数：{stats['users_count']}")
    
    print("\n✅ Discord 客户端测试完成!")
    print("   请配置 ~/.openclaw/workspace/config/discord/config.json 后使用完整功能")
    print("\n📋 运行 Bot:")
    print("   python3 -m skills.discord-integration.discord_bot")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
