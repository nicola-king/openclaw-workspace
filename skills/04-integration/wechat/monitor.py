#!/usr/bin/env python3
"""
微信通道监控脚本
持续监控微信通道状态，定期输出报告

用法:
    python3 monitor.py [--interval 60] [--output report.json]
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

WEIXIN_DIR = Path.home() / '.openclaw' / 'openclaw-weixin'
ACCOUNTS_FILE = WEIXIN_DIR / 'accounts.json'
ACCOUNTS_DIR = WEIXIN_DIR / 'accounts'

def check_account_health(account_id: str) -> dict:
    """检查单个账号健康状态"""
    result = {
        'account_id': account_id,
        'timestamp': datetime.now().isoformat(),
        'status': 'unknown',
        'issues': []
    }
    
    # 检查账号文件
    account_file = ACCOUNTS_DIR / f'{account_id}.json'
    if not account_file.exists():
        result['status'] = 'error'
        result['issues'].append('账号文件缺失')
        return result
    
    try:
        with open(account_file, 'r') as f:
            acc_data = json.load(f)
        
        # 检查必要字段
        if 'token' not in acc_data:
            result['issues'].append('Token 缺失')
        
        if 'userId' not in acc_data:
            result['issues'].append('User ID 缺失')
        
        # 检查同步状态
        sync_file = ACCOUNTS_DIR / f'{account_id}.sync.json'
        if sync_file.exists():
            with open(sync_file, 'r') as f:
                sync_data = json.load(f)
            
            if 'get_updates_buf' not in sync_data:
                result['issues'].append('同步缓冲区缺失')
            else:
                result['sync_buffer_size'] = len(sync_data['get_updates_buf'])
        else:
            result['issues'].append('同步状态文件缺失')
        
        # 评估状态
        if not result['issues']:
            result['status'] = 'healthy'
        elif len(result['issues']) == 1:
            result['status'] = 'warning'
        else:
            result['status'] = 'error'
            
    except Exception as e:
        result['status'] = 'error'
        result['issues'].append(f'读取错误：{str(e)}')
    
    return result

def run_check() -> dict:
    """执行一次完整检查"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'accounts': [],
        'summary': {
            'total': 0,
            'healthy': 0,
            'warning': 0,
            'error': 0
        }
    }
    
    # 加载账号列表
    if not ACCOUNTS_FILE.exists():
        report['summary']['error'] = 1
        report['issues'] = ['账号配置文件缺失']
        return report
    
    with open(ACCOUNTS_FILE, 'r') as f:
        accounts = json.load(f)
    
    report['summary']['total'] = len(accounts)
    
    # 检查每个账号
    for acc_id in accounts:
        health = check_account_health(acc_id)
        report['accounts'].append(health)
        
        if health['status'] == 'healthy':
            report['summary']['healthy'] += 1
        elif health['status'] == 'warning':
            report['summary']['warning'] += 1
        else:
            report['summary']['error'] += 1
    
    return report

def print_report(report: dict):
    """打印报告"""
    print(f"\n{'='*60}")
    print(f"微信通道监控报告")
    print(f"时间：{report['timestamp']}")
    print(f"{'='*60}\n")
    
    summary = report['summary']
    print(f"📊 总体状态:")
    print(f"   总账号数：{summary['total']}")
    print(f"   ✅ 健康：{summary['healthy']}")
    print(f"   ⚠️  警告：{summary['warning']}")
    print(f"   ❌ 错误：{summary['error']}")
    print()
    
    if 'issues' in report:
        print(f"🚨 全局问题:")
        for issue in report['issues']:
            print(f"   - {issue}")
        print()
    
    print(f"📱 账号详情:")
    for acc in report['accounts']:
        status_icon = {'healthy': '✅', 'warning': '⚠️', 'error': '❌'}.get(acc['status'], 'ℹ️')
        print(f"\n   {status_icon} {acc['account_id']}")
        print(f"      状态：{acc['status']}")
        
        if 'sync_buffer_size' in acc:
            print(f"      同步缓冲：{acc['sync_buffer_size']} bytes")
        
        if acc['issues']:
            print(f"      问题:")
            for issue in acc['issues']:
                print(f"         - {issue}")
    
    print(f"\n{'='*60}\n")

def main():
    # 解析参数
    interval = 0  # 默认只运行一次
    output_file = None
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--interval' and i + 1 < len(sys.argv):
            interval = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if interval > 0:
        print(f"启动监控模式 (间隔：{interval}秒)")
        print("按 Ctrl+C 停止\n")
    
    try:
        while True:
            report = run_check()
            print_report(report)
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"📄 报告已保存：{output_file}\n")
            
            if interval == 0:
                break
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n监控已停止")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
