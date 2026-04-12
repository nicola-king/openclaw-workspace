#!/usr/bin/env python3
"""
微信账号管理工具
管理微信账号配置、查看状态、删除账号等

用法:
    python3 account-manager.py list              # 列出所有账号
    python3 account-manager.py show <id>         # 查看账号详情
    python3 account-manager.py remove <id>       # 删除账号
    python3 account-manager.py status            # 查看同步状态
"""

import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

WEIXIN_DIR = Path.home() / '.openclaw' / 'openclaw-weixin'
ACCOUNTS_FILE = WEIXIN_DIR / 'accounts.json'
ACCOUNTS_DIR = WEIXIN_DIR / 'accounts'

def load_accounts() -> list:
    """加载账号列表"""
    if not ACCOUNTS_FILE.exists():
        return []
    
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)

def save_accounts(accounts: list):
    """保存账号列表"""
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=2)

def load_account(account_id: str) -> dict:
    """加载账号详情"""
    account_file = ACCOUNTS_DIR / f'{account_id}.json'
    if not account_file.exists():
        return {}
    
    with open(account_file, 'r') as f:
        return json.load(f)

def load_sync_status(account_id: str) -> dict:
    """加载同步状态"""
    sync_file = ACCOUNTS_DIR / f'{account_id}.sync.json'
    if not sync_file.exists():
        return {}
    
    with open(sync_file, 'r') as f:
        return json.load(f)

def cmd_list():
    """列出所有账号"""
    accounts = load_accounts()
    
    if not accounts:
        print("未配置任何微信账号")
        return
    
    print(f"\n=== 微信账号列表 ({len(accounts)} 个) ===\n")
    
    for acc_id in accounts:
        acc_data = load_account(acc_id)
        sync_data = load_sync_status(acc_id)
        
        user_id = acc_data.get('userId', 'unknown')
        saved_at = acc_data.get('savedAt', 'unknown')
        has_sync = 'get_updates_buf' in sync_data
        
        print(f"📱 {acc_id}")
        print(f"   用户 ID: {user_id}")
        print(f"   认证时间：{saved_at}")
        print(f"   同步状态：{'✅ 正常' if has_sync else '⚠️  未同步'}")
        print()

def cmd_show(account_id: str):
    """查看账号详情"""
    accounts = load_accounts()
    
    if account_id not in accounts:
        print(f"❌ 账号不存在：{account_id}")
        print(f"可用账号：{', '.join(accounts)}")
        return
    
    acc_data = load_account(account_id)
    sync_data = load_sync_status(account_id)
    
    print(f"\n=== 账号详情：{account_id} ===\n")
    print(f"用户 ID:     {acc_data.get('userId', 'N/A')}")
    print(f"Base URL:    {acc_data.get('baseUrl', 'N/A')}")
    print(f"认证时间：   {acc_data.get('savedAt', 'N/A')}")
    print(f"Token:       {'✅ 已配置' if 'token' in acc_data else '❌ 缺失'}")
    print()
    print(f"同步状态：   {'✅ 正常' if 'get_updates_buf' in sync_data else '⚠️  未同步'}")
    if 'get_updates_buf' in sync_data:
        buf_size = len(sync_data['get_updates_buf'])
        print(f"同步缓冲区：{buf_size} bytes")
    print()

def cmd_remove(account_id: str):
    """删除账号"""
    accounts = load_accounts()
    
    if account_id not in accounts:
        print(f"❌ 账号不存在：{account_id}")
        return
    
    # 确认删除
    confirm = input(f"⚠️  确定要删除账号 {account_id} 吗？(y/N): ")
    if confirm.lower() != 'y':
        print("已取消")
        return
    
    # 删除账号文件
    account_file = ACCOUNTS_DIR / f'{account_id}.json'
    sync_file = ACCOUNTS_DIR / f'{account_id}.sync.json'
    context_file = ACCOUNTS_DIR / f'{account_id}.context-tokens.json'
    
    files_deleted = []
    
    if account_file.exists():
        account_file.unlink()
        files_deleted.append(str(account_file))
    
    if sync_file.exists():
        sync_file.unlink()
        files_deleted.append(str(sync_file))
    
    if context_file.exists():
        context_file.unlink()
        files_deleted.append(str(context_file))
    
    # 从列表移除
    accounts.remove(account_id)
    save_accounts(accounts)
    
    print(f"✅ 已删除账号 {account_id}")
    print(f"   删除文件：{', '.join(files_deleted)}")
    print(f"   剩余账号：{len(accounts)} 个")

def cmd_status():
    """查看所有账号同步状态"""
    accounts = load_accounts()
    
    if not accounts:
        print("未配置任何微信账号")
        return
    
    print(f"\n=== 同步状态 ({len(accounts)} 个账号) ===\n")
    
    for acc_id in accounts:
        sync_data = load_sync_status(acc_id)
        has_buffer = 'get_updates_buf' in sync_data
        buffer_size = len(sync_data.get('get_updates_buf', ''))
        
        status = "✅ 正常" if has_buffer else "⚠️  未同步"
        print(f"{acc_id}: {status} (缓冲区：{buffer_size} bytes)")
    
    print()

def print_usage():
    """打印使用说明"""
    print("""
微信账号管理工具

用法:
    python3 account-manager.py <command> [args]

命令:
    list              列出所有账号
    show <id>         查看账号详情
    remove <id>       删除账号
    status            查看同步状态
    help              显示此帮助信息

示例:
    python3 account-manager.py list
    python3 account-manager.py show 1947559cd522-im-bot
    python3 account-manager.py remove 3df0dca14cc5-im-bot
    python3 account-manager.py status
""")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return 1
    
    command = sys.argv[1]
    
    if command == 'list':
        cmd_list()
    elif command == 'show':
        if len(sys.argv) < 3:
            print("❌ 错误：缺少账号 ID")
            print_usage()
            return 1
        cmd_show(sys.argv[2])
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("❌ 错误：缺少账号 ID")
            print_usage()
            return 1
        cmd_remove(sys.argv[2])
    elif command == 'status':
        cmd_status()
    elif command == 'help':
        print_usage()
    else:
        print(f"❌ 未知命令：{command}")
        print_usage()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
