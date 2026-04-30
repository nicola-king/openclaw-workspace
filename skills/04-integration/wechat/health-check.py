#!/usr/bin/env python3
"""
微信通道健康检查脚本
检查账号状态、同步状态、Gateway 连接等

用法:
    python3 health-check.py [--verbose]
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_status(status: str, message: str, verbose: bool = False):
    """打印状态"""
    icons = {
        'ok': '✅',
        'warn': '⚠️',
        'error': '❌',
        'info': 'ℹ️'
    }
    colors = {
        'ok': Colors.GREEN,
        'warn': Colors.YELLOW,
        'error': Colors.RED,
        'info': Colors.BLUE
    }
    
    icon = icons.get(status, 'ℹ️')
    color = colors.get(status, '')
    
    print(f"{color}{icon} {message}{Colors.END}")

def check_weixin_dir() -> dict:
    """检查微信目录结构"""
    weixin_dir = Path.home() / '.openclaw' / 'openclaw-weixin'
    
    result = {
        'exists': weixin_dir.exists(),
        'accounts_file': False,
        'accounts_dir': False,
        'account_count': 0,
        'accounts': []
    }
    
    if not result['exists']:
        return result
    
    # 检查 accounts.json
    accounts_file = weixin_dir / 'accounts.json'
    result['accounts_file'] = accounts_file.exists()
    
    # 检查 accounts 目录
    accounts_dir = weixin_dir / 'accounts'
    result['accounts_dir'] = accounts_dir.exists()
    
    if result['accounts_dir']:
        # 统计账号
        account_files = list(accounts_dir.glob('*.json'))
        result['account_count'] = len(account_files)
        
        # 读取账号详情
        for f in account_files:
            if f.name.endswith('.json') and not f.name.endswith('.sync.json'):
                try:
                    with open(f, 'r') as fp:
                        data = json.load(fp)
                        result['accounts'].append({
                            'file': f.name,
                            'userId': data.get('userId', 'unknown'),
                            'savedAt': data.get('savedAt', 'unknown'),
                            'hasToken': 'token' in data
                        })
                except Exception as e:
                    result['accounts'].append({
                        'file': f.name,
                        'error': str(e)
                    })
    
    return result

def check_sync_status(weixin_dir: Path) -> list:
    """检查同步状态"""
    sync_files = list((weixin_dir / 'accounts').glob('*.sync.json'))
    results = []
    
    for f in sync_files:
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                results.append({
                    'file': f.name,
                    'hasBuffer': 'get_updates_buf' in data,
                    'bufferSize': len(data.get('get_updates_buf', ''))
                })
        except Exception as e:
            results.append({
                'file': f.name,
                'error': str(e)
            })
    
    return results

def check_gateway() -> dict:
    """检查 Gateway 状态"""
    import subprocess
    
    result = {
        'running': False,
        'pid': None,
        'port': '18789'
    }
    
    try:
        # 检查进程
        proc = subprocess.run(
            ['pgrep', '-f', 'openclaw.*gateway'],
            capture_output=True,
            text=True
        )
        if proc.returncode == 0 and proc.stdout.strip():
            result['running'] = True
            result['pid'] = proc.stdout.strip().split('\n')[0]
        
        # 检查端口
        proc = subprocess.run(
            ['ss', '-tlnp'],
            capture_output=True,
            text=True
        )
        if '18789' in proc.stdout:
            result['portOpen'] = True
        else:
            result['portOpen'] = False
            
    except Exception as e:
        result['error'] = str(e)
    
    return result

def main():
    verbose = '--verbose' in sys.argv
    
    print(f"\n{Colors.BOLD}=== 微信通道健康检查 ==={Colors.END}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
    
    # 1. 检查目录结构
    print(f"{Colors.BLUE}📁 目录结构{Colors.END}")
    dir_check = check_weixin_dir()
    
    if dir_check['exists']:
        print_status('ok', f"微信目录：~/.openclaw/openclaw-weixin/")
    else:
        print_status('error', "微信目录不存在")
        return 1
    
    if dir_check['accounts_file']:
        print_status('ok', "账号配置文件：存在")
    else:
        print_status('warn', "账号配置文件：缺失")
    
    if dir_check['accounts_dir']:
        print_status('ok', f"账号目录：{dir_check['account_count']} 个账号")
        
        for acc in dir_check['accounts']:
            if 'error' in acc:
                print_status('error', f"  - {acc['file']}: {acc['error']}")
            elif acc.get('hasToken'):
                print_status('ok', f"  - {acc['userId'][:20]}... ✅ 已认证")
            else:
                print_status('warn', f"  - {acc['userId'][:20]}... ⚠️ 未认证")
    else:
        print_status('error', "账号目录：缺失")
    
    print()
    
    # 2. 检查同步状态
    print(f"{Colors.BLUE}🔄 同步状态{Colors.END}")
    weixin_dir = Path.home() / '.openclaw' / 'openclaw-weixin'
    if dir_check['accounts_dir']:
        sync_status = check_sync_status(weixin_dir)
        for s in sync_status:
            if 'error' in s:
                print_status('error', f"  - {s['file']}: {s['error']}")
            elif s.get('hasBuffer'):
                print_status('ok', f"  - {s['file']}: 同步缓冲区 {s['bufferSize']} bytes")
            else:
                print_status('warn', f"  - {s['file']}: 无同步数据")
    else:
        print_status('warn', "无法检查同步状态（账号目录缺失）")
    
    print()
    
    # 3. 检查 Gateway
    print(f"{Colors.BLUE}🔌 Gateway 连接{Colors.END}")
    gateway_check = check_gateway()
    
    if gateway_check.get('running'):
        print_status('ok', f"Gateway 进程：运行中 (PID {gateway_check['pid']})")
    else:
        print_status('error', "Gateway 进程：未运行")
    
    if gateway_check.get('portOpen'):
        print_status('ok', f"Gateway 端口：{gateway_check['port']} 已监听")
    else:
        print_status('warn', f"Gateway 端口：{gateway_check['port']} 未监听")
    
    print()
    
    # 4. 总体评估
    print(f"{Colors.BOLD}📊 总体评估{Colors.END}")
    
    issues = []
    if not dir_check['accounts_file']:
        issues.append("账号配置文件缺失")
    if not dir_check['accounts_dir']:
        issues.append("账号目录缺失")
    if not gateway_check.get('running'):
        issues.append("Gateway 未运行")
    
    if not issues:
        print_status('ok', "微信通道状态：健康 ✅")
        return 0
    else:
        print_status('error', f"发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"   - {issue}")
        print(f"\n{Colors.YELLOW}建议运行：openclaw gateway restart{Colors.END}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
