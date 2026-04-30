#!/usr/bin/env python3
"""
添加 Discord 通道到 OpenClaw 配置

用法：python3 add-discord-channel.py <bot_token> [server_id]
"""

import json
import sys
from pathlib import Path

CONFIG_FILE = Path.home() / ".openclaw" / "openclaw.json"

def add_discord_channel(bot_token: str, server_id: str = "*"):
    """添加 Discord 通道配置"""
    
    # 读取现有配置
    if not CONFIG_FILE.exists():
        print(f"❌ 配置文件不存在：{CONFIG_FILE}")
        sys.exit(1)
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 添加 Discord 通道
    if 'channels' not in config:
        config['channels'] = {}
    
    config['channels']['discord'] = {
        'enabled': True,
        'defaultAccount': 'taiyi',
        'streaming': 'partial',
        'accounts': {
            'taiyi': {
                'enabled': True,
                'botToken': bot_token,
                'dmPolicy': 'pairing',
                'groupPolicy': 'allowlist' if server_id != "*" else 'open',
                'allowFrom': [server_id] if server_id != "*" else ["*"],
                'streaming': 'partial'
            }
        }
    }
    
    # 添加 Agent 绑定
    if 'bindings' not in config:
        config['bindings'] = []
    
    # 检查是否已存在
    exists = False
    for binding in config['bindings']:
        if binding.get('agentId') == 'taiyi' and \
           binding.get('match', {}).get('channel') == 'discord':
            exists = True
            break
    
    if not exists:
        config['bindings'].append({
            'agentId': 'taiyi',
            'match': {
                'channel': 'discord',
                'accountId': 'taiyi'
            }
        })
    
    # 保存配置
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Discord 通道配置已添加到：{CONFIG_FILE}")
    print(f"   Bot Token: {bot_token[:20]}...")
    print(f"   Server ID: {server_id}")
    print()
    print("下一步：")
    print("1. 重启 Gateway: openclaw gateway restart")
    print("2. 在 Discord 测试：@Taiyi 你好")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 add-discord-channel.py <bot_token> [server_id]")
        print()
        print("示例:")
        print("  python3 add-discord-channel.py MTIzNDU2Nzg5MDEy")
        print("  python3 add-discord-channel.py MTIzNDU2Nzg5MDEy 987654321098765432")
        sys.exit(1)
    
    bot_token = sys.argv[1]
    server_id = sys.argv[2] if len(sys.argv) > 2 else "*"
    
    add_discord_channel(bot_token, server_id)
