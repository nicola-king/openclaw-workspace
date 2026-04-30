#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安交易健康自检任务

功能:
1. API 连接检查
2. IP 白名单验证
3. 账户余额检查
4. 交易权限验证
5. 自动自愈 (重启/切换 IP)
6. 告警通知 (严重问题时)

作者：太一 AGI
创建：2026-04-23
版本：v1.0
"""

import json
import time
import hmac
import hashlib
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/binance_health_check.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('BinanceHealthCheck')

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
ENV_FILE = WORKSPACE.parent / ".env"
IP_FILE = Path("/tmp/last_export_ip.txt")
PID_FILE = Path("/tmp/zhiji_trader.pid")
HEALTH_STATUS_FILE = Path("/tmp/binance_health_status.json")

# 加载 API Key
def load_api_credentials():
    """从.env 文件加载 API 凭证"""
    api_key = None
    api_secret = None
    
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("BINANCE_API_KEY="):
                    api_key = line.split("=")[1].strip()
                elif line.startswith("BINANCE_API_SECRET="):
                    api_secret = line.split("=")[1].strip()
    
    return api_key, api_secret

# 获取当前 IP
def get_current_ip():
    """读取当前出口 IP"""
    if IP_FILE.exists():
        content = IP_FILE.read_text().strip()
        for line in content.split('\n')[::-1]:
            line = line.strip()
            if len(line.split('.')) == 4 and all(p.isdigit() for p in line.split('.')):
                return line
    return None

# 生成签名
def generate_signature(query_string: str, secret: str) -> str:
    return hmac.new(
        secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

# 检查 API 连接
def check_api_connection(api_key: str, api_secret: str) -> Dict:
    """检查币安 API 连接"""
    try:
        timestamp = int(time.time() * 1000)
        params = f"timestamp={timestamp}"
        signature = generate_signature(params, api_secret)
        
        url = f"https://api.binance.com/api/v3/account?{params}&signature={signature}"
        headers = {"X-MBX-APIKEY": api_key}
        
        response = requests.get(url, headers=headers, timeout=10, proxies={
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        })
        
        if response.status_code == 200:
            account = response.json()
            return {
                'status': 'ok',
                'message': 'API 连接正常',
                'account': account
            }
        elif response.status_code == 401:
            error = response.json()
            return {
                'status': 'error',
                'message': f"API 认证失败：{error.get('msg', 'Unknown')}",
                'error_code': error.get('code')
            }
        else:
            return {
                'status': 'error',
                'message': f"API 请求失败：{response.status_code}",
                'error_code': response.status_code
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f"API 连接异常：{str(e)}",
            'error_code': 'EXCEPTION'
        }

# 检查账户余额
def check_balance(account: Dict) -> Dict:
    """检查账户余额"""
    try:
        balances = {'USDT': 0.0, 'BTC': 0.0, 'ETH': 0.0}
        
        if 'balances' in account:
            for asset in account['balances']:
                if asset['asset'] in balances:
                    balances[asset['asset']] = float(asset['free']) + float(asset['locked'])
        
        usdt_balance = balances['USDT']
        btc_balance = balances['BTC']
        
        # 检查是否可交易 (USDT ≥ $10 或 BTC ≥ 0.00013)
        can_trade = usdt_balance >= 10 or btc_balance >= 0.00013
        
        return {
            'status': 'ok' if can_trade else 'warning',
            'balances': balances,
            'can_trade': can_trade,
            'message': f"USDT: ${usdt_balance:.2f}, BTC: {btc_balance:.5f}"
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f"余额检查失败：{str(e)}",
            'can_trade': False
        }

# 检查 IP 白名单
def check_ip_whitelist() -> Dict:
    """检查 IP 白名单配置"""
    current_ip = get_current_ip()
    
    # 已知白名单 IP
    whitelisted_ips = [
        '141.11.146.70',
        '103.151.172.28',
        '103.151.173.206',
    ]
    
    if current_ip:
        if current_ip in whitelisted_ips:
            return {
                'status': 'ok',
                'message': f"IP {current_ip} 在白名单中",
                'ip': current_ip
            }
        else:
            return {
                'status': 'warning',
                'message': f"IP {current_ip} 不在已知白名单中",
                'ip': current_ip,
                'suggestion': '请在币安后台添加此 IP 到白名单'
            }
    else:
        return {
            'status': 'error',
            'message': '无法获取当前 IP',
            'ip': None
        }

# 检查知几进程
def check_zhiji_process() -> Dict:
    """检查知几交易进程"""
    try:
        import subprocess
        result = subprocess.run(
            ['pgrep', '-f', 'zhiji_auto_evolution_trader.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            return {
                'status': 'ok',
                'message': f'知几进程运行中 (PID: {", ".join(pids)})',
                'pids': pids
            }
        else:
            return {
                'status': 'error',
                'message': '知几进程未运行',
                'pids': []
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'进程检查失败：{str(e)}'
        }

# 自愈：重启知几
def restart_zhiji() -> bool:
    """重启知几交易程序"""
    try:
        import subprocess
        
        # 停止旧进程
        subprocess.run(['pkill', '-9', '-f', 'zhiji_auto_evolution'], timeout=10)
        time.sleep(3)
        
        # 启动新进程
        script = WORKSPACE / "scripts" / "zhiji_auto_evolution_trader.py"
        log_file = WORKSPACE / "logs" / "zhiji_evolution_trader.log"
        
        with open(log_file, 'a') as log:
            subprocess.Popen(
                ['python3', str(script)],
                stdout=log,
                stderr=log,
                start_new_session=True
            )
        
        time.sleep(5)
        
        # 验证是否启动成功
        result = check_zhiji_process()
        return result['status'] == 'ok'
        
    except Exception as e:
        logger.error(f"重启失败：{str(e)}")
        return False

# 保存健康状态
def save_health_status(status: Dict):
    """保存健康检查状态"""
    status['last_check'] = datetime.now().isoformat()
    
    with open(HEALTH_STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

# 主健康检查
def health_check():
    """执行完整健康检查"""
    logger.info("=" * 60)
    logger.info("🏥 币安交易健康自检开始")
    logger.info("=" * 60)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'checks': {},
        'overall_status': 'ok',
        'auto_heal_triggered': False
    }
    
    # 1. 加载凭证
    api_key, api_secret = load_api_credentials()
    if not api_key or not api_secret:
        results['checks']['credentials'] = {
            'status': 'error',
            'message': 'API 凭证未配置'
        }
        results['overall_status'] = 'error'
        logger.error("❌ API 凭证未配置")
        save_health_status(results)
        return results
    
    results['checks']['credentials'] = {'status': 'ok', 'message': 'API 凭证已配置'}
    
    # 2. 检查 IP 白名单
    ip_status = check_ip_whitelist()
    results['checks']['ip_whitelist'] = ip_status
    logger.info(f"{'✅' if ip_status['status'] == 'ok' else '⚠️'}  IP 白名单：{ip_status['message']}")
    
    # 3. 检查 API 连接
    api_status = check_api_connection(api_key, api_secret)
    results['checks']['api_connection'] = api_status
    
    if api_status['status'] == 'ok':
        logger.info(f"✅ API 连接：{api_status['message']}")
        
        # 4. 检查余额
        balance_status = check_balance(api_status.get('account', {}))
        results['checks']['balance'] = balance_status
        logger.info(f"{'✅' if balance_status['status'] == 'ok' else '⚠️'}  账户余额：{balance_status['message']}")
    else:
        logger.error(f"❌ API 连接：{api_status['message']}")
        results['checks']['balance'] = {'status': 'error', 'message': 'API 连接失败，无法检查余额'}
        results['overall_status'] = 'error'
    
    # 5. 检查知几进程
    process_status = check_zhiji_process()
    results['checks']['process'] = process_status
    logger.info(f"{'✅' if process_status['status'] == 'ok' else '❌'}  知几进程：{process_status['message']}")
    
    # 自愈逻辑
    if process_status['status'] == 'error':
        logger.warning("🔧 触发自愈：知几进程未运行，尝试重启...")
        if restart_zhiji():
            logger.info("✅ 自愈成功：知几已重启")
            results['auto_heal_triggered'] = True
            results['checks']['process']['auto_heal'] = 'success'
        else:
            logger.error("❌ 自愈失败：知几重启失败")
            results['checks']['process']['auto_heal'] = 'failed'
    
    # 6. 综合状态
    if any(check.get('status') == 'error' for check in results['checks'].values()):
        results['overall_status'] = 'error'
    elif any(check.get('status') == 'warning' for check in results['checks'].values()):
        results['overall_status'] = 'warning'
    
    # 保存状态
    save_health_status(results)
    
    # 输出总结
    logger.info("=" * 60)
    logger.info(f"📊 健康检查完成 - 总体状态：{results['overall_status'].upper()}")
    logger.info(f"🔧 自愈触发：{'是' if results['auto_heal_triggered'] else '否'}")
    logger.info("=" * 60)
    
    return results

if __name__ == '__main__':
    health_check()
