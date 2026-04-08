#!/usr/bin/env python3
"""
Discord Bot - Discord 机器人核心 v1.0

作者：太一 AGI
创建：2026-04-08
"""

import os
import json
import discord
from discord.ext import commands
from pathlib import Path
from datetime import datetime

# 配置路径
CONFIG_FILE = Path(__file__).parent / "config" / "discord_config.json"


class DiscordBot:
    """Discord 机器人"""
    
    def __init__(self):
        self.config = self.load_config()
        
        # 设置 Intents
        intents = discord.Intents.default()
        intents.messages = self.config.get("intents", {}).get("messages", True)
        intents.message_content = self.config.get("intents", {}).get("message_content", True)
        
        # 创建 Bot
        self.bot = commands.Bot(
            command_prefix=self.config.get("prefix", "!"),
            intents=intents
        )
        
        # 注册事件
        @self.bot.event
        async def on_ready():
            print(f"✅ Bot 已连接!")
            print(f"   用户：{self.bot.user}")
            print(f"   ID: {self.bot.user.id}")
            print(f"   服务器：{len(self.bot.guilds)} 个")
            print(f"   频道：{len(list(self.bot.get_all_channels()))} 个")
            print()
            
            # 设置状态
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="太一 AGI"
                )
            )
        
        # 注册命令
        @self.bot.command(name="help")
        async def help_command(ctx):
            """帮助命令"""
            embed = discord.Embed(
                title="🤖 太一 AGI - 帮助",
                description="你的数字幕僚",
                color=0x00ff00
            )
            embed.add_field(name="!help", value="显示帮助信息", inline=False)
            embed.add_field(name="!status", value="查看系统状态", inline=False)
            embed.add_field(name="!ping", value="测试延迟", inline=False)
            embed.set_footer(text=f"太一 AGI v1.0 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            await ctx.send(embed=embed)
        
        @self.bot.command(name="status")
        async def status_command(ctx):
            """状态命令"""
            embed = discord.Embed(
                title="📊 系统状态",
                description="太一 AGI 运行正常",
                color=0x00ff00
            )
            embed.add_field(name="Bot", value=str(self.bot.user), inline=True)
            embed.add_field(name="服务器", value=len(self.bot.guilds), inline=True)
            embed.add_field(name="延迟", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
            await ctx.send(embed=embed)
        
        @self.bot.command(name="ping")
        async def ping_command(ctx):
            """Ping 命令"""
            latency = round(self.bot.latency * 1000)
            await ctx.send(f"🏓 Pong! 延迟：{latency}ms")
        
        # 自动响应
        @self.bot.event
        async def on_message(message):
            # 忽略自己
            if message.author == self.bot.user:
                return
            
            # 关键词自动响应
            if "你好" in message.content:
                await message.channel.send("你好！我是太一 AGI，有什么可以帮你的？")
            
            # 处理命令
            await self.bot.process_commands(message)
    
    def load_config(self) -> dict:
        """加载配置"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def run(self):
        """启动 Bot"""
        token = self.config.get("token", "")
        if not token:
            print("❌ Bot Token 未配置!")
            return
        
        print("🤖 启动 Discord Bot...")
        print(f"   Token: {token[:20]}...")
        print(f"   前缀：{self.config.get('prefix', '!')}")
        print()
        
        try:
            self.bot.run(token)
        except Exception as e:
            print(f"❌ 启动失败：{e}")
    
    def send_message(self, channel_id: int, content: str):
        """发送消息 (需要同步运行)"""
        import asyncio
        
        async def _send():
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.send(content)
                print(f"✅ 消息已发送到频道 {channel_id}")
            else:
                print(f"❌ 频道 {channel_id} 未找到")
        
        if self.bot.is_ready():
            asyncio.run(_send())
        else:
            print("⚠️ Bot 未就绪")


def main():
    """主函数"""
    bot = DiscordBot()
    bot.run()


if __name__ == "__main__":
    main()
