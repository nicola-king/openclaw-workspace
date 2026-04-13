#!/usr/bin/env python3
"""
📋 commands.list RPC

OpenClaw 4.10 智能调度核心功能
运行时命令发现/表面感知命名/参数元数据

作者：太一 AGI
创建：2026-04-11
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class CommandsListRPC:
    """commands.list RPC 实现"""
    
    def __init__(self):
        """初始化 RPC"""
        self.commands = self._discover_commands()
        
        print("📋 commands.list RPC 已初始化")
        print(f"   发现命令：{len(self.commands)} 个")
        print()
    
    def _discover_commands(self) -> List[Dict]:
        """发现运行时命令"""
        commands = []
        
        # 1. 内置命令
        builtin_commands = [
            {
                "name": "help",
                "type": "runtime",
                "description": "显示帮助信息",
                "arguments": [],
                "surface_aware": True
            },
            {
                "name": "status",
                "type": "runtime",
                "description": "显示系统状态",
                "arguments": [],
                "surface_aware": True
            },
            {
                "name": "memory",
                "type": "runtime",
                "description": "记忆管理",
                "arguments": [
                    {"name": "action", "type": "string", "required": True},
                    {"name": "query", "type": "string", "required": False}
                ],
                "surface_aware": True
            },
            {
                "name": "config",
                "type": "runtime",
                "description": "配置管理",
                "arguments": [
                    {"name": "key", "type": "string", "required": True},
                    {"name": "value", "type": "any", "required": False}
                ],
                "surface_aware": True
            }
        ]
        commands.extend(builtin_commands)
        
        # 2. 文本命令
        text_commands = [
            {
                "name": "reply",
                "type": "text",
                "description": "回复消息",
                "arguments": [
                    {"name": "message_id", "type": "string", "required": True},
                    {"name": "content", "type": "string", "required": True}
                ],
                "surface_aware": True
            },
            {
                "name": "quote",
                "type": "text",
                "description": "引用回复",
                "arguments": [
                    {"name": "message_id", "type": "string", "required": True},
                    {"name": "content", "type": "string", "required": True}
                ],
                "surface_aware": True
            }
        ]
        commands.extend(text_commands)
        
        # 3. Skill 命令
        skill_commands = [
            {
                "name": "cost.estimate",
                "type": "skill",
                "skill": "cost-agent",
                "description": "造价估算",
                "arguments": [
                    {"name": "project_type", "type": "string", "required": True},
                    {"name": "parameters", "type": "object", "required": False}
                ],
                "surface_aware": True
            },
            {
                "name": "memory.search",
                "type": "skill",
                "skill": "taiyi-memory-palace",
                "description": "记忆搜索",
                "arguments": [
                    {"name": "query", "type": "string", "required": True},
                    {"name": "limit", "type": "integer", "required": False}
                ],
                "surface_aware": True
            }
        ]
        commands.extend(skill_commands)
        
        # 4. 插件命令
        plugin_commands = [
            {
                "name": "feishu.send",
                "type": "plugin",
                "plugin": "feishu",
                "description": "发送飞书消息",
                "arguments": [
                    {"name": "user_id", "type": "string", "required": True},
                    {"name": "content", "type": "string", "required": True}
                ],
                "surface_aware": True
            },
            {
                "name": "telegram.send",
                "type": "plugin",
                "plugin": "telegram",
                "description": "发送 Telegram 消息",
                "arguments": [
                    {"name": "chat_id", "type": "string", "required": True},
                    {"name": "content", "type": "string", "required": True}
                ],
                "surface_aware": True
            }
        ]
        commands.extend(plugin_commands)
        
        return commands
    
    def list(self, filter_type: str = None) -> Dict:
        """
        列出所有命令
        
        Args:
            filter_type: 命令类型过滤 (runtime/text/skill/plugin)
        
        Returns:
            命令列表及元数据
        """
        if filter_type:
            filtered = [c for c in self.commands if c['type'] == filter_type]
        else:
            filtered = self.commands
        
        return {
            "commands": filtered,
            "total": len(filtered),
            "by_type": self._count_by_type(filtered),
            "discovered_at": datetime.now().isoformat()
        }
    
    def _count_by_type(self, commands: List[Dict]) -> Dict:
        """按类型统计"""
        counts = {}
        for cmd in commands:
            cmd_type = cmd['type']
            if cmd_type not in counts:
                counts[cmd_type] = 0
            counts[cmd_type] += 1
        return counts
    
    def get_command(self, name: str) -> Dict:
        """获取单个命令详情"""
        for cmd in self.commands:
            if cmd['name'] == name:
                return cmd
        return {"error": f"Command '{name}' not found"}
    
    def export_to_json(self, output_file: str):
        """导出到 JSON"""
        data = self.list()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 命令列表已导出：{output_file}")


def main():
    """主函数 - 测试"""
    print("="*60)
    print("📋 commands.list RPC 测试")
    print("="*60)
    
    # 初始化 RPC
    rpc = CommandsListRPC()
    
    # 列出所有命令
    print("\n1. 列出所有命令...")
    result = rpc.list()
    print(f"   总命令数：{result['total']}")
    print(f"   按类型统计：{result['by_type']}")
    
    # 按类型过滤
    print("\n2. 按类型过滤...")
    for cmd_type in ['runtime', 'text', 'skill', 'plugin']:
        filtered = rpc.list(filter_type=cmd_type)
        print(f"   {cmd_type}: {filtered['total']} 个")
    
    # 获取单个命令
    print("\n3. 获取单个命令...")
    cmd = rpc.get_command("help")
    print(f"   名称：{cmd['name']}")
    print(f"   类型：{cmd['type']}")
    print(f"   描述：{cmd['description']}")
    
    # 导出
    print("\n4. 导出到 JSON...")
    output_file = "/home/nicola/.openclaw/workspace/skills/commands-list/commands.json"
    rpc.export_to_json(output_file)
    
    print("\n✅ commands.list RPC 测试完成!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
