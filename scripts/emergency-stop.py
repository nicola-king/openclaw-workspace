#!/usr/bin/env python3
"""
紧急停止开关 v1.0
功能：一键平仓所有持仓，停止所有交易
使用场景：极端行情/系统异常/人工干预
"""

import requests
import hmac
import hashlib
import time
import json
from datetime import datetime
from pathlib import Path

# 配置
API_KEY = 'ufHaoQRuMLI0HScM99mt3ZGUMc7xFJt0hwZGsKqS9MYRW7Y2SzQ7jzsuN834JcVe'
SECRET_KEY = 'PGilezOeAzuNq4ZwrNGIUgpVYDMOBUjhhp10SGMKRoTrpoqHqkTvs86qJWqvhox3'
BASE_URL = 'https://api.binance.com'

def get_signature(params):
    return hmac.new(SECRET_KEY.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest()

def get_account():
    """获取账户信息"""
    timestamp = int(time.time() * 1000)
    params = f'timestamp={timestamp}'
    signature = get_signature(params)
    headers = {'X-MBX-APIKEY': API_KEY}
    url = f'{BASE_URL}/api/v3/account?{params}&signature={signature}'
    response = requests.get(url, headers=headers, timeout=10)
    return response.json()

def get_price(symbol):
    """获取实时价格"""
    url = f'{BASE_URL}/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url, timeout=10)
    data = response.json()
    return float(data['price'])

def place_market_order(symbol, side, quantity):
    """下市价单"""
    timestamp = int(time.time() * 1000)
    recv_window = 5000
    
    params_dict = {
        'quantity': quantity,
        'recvWindow': recv_window,
        'side': side,
        'symbol': symbol,
        'timestamp': timestamp,
        'type': 'MARKET'
    }
    
    params_str = '&'.join([f'{k}={params_dict[k]}' for k in sorted(params_dict.keys())])
    signature = get_signature(params_str)
    
    headers = {'X-MBX-APIKEY': API_KEY}
    url = f'{BASE_URL}/api/v3/order'
    data = params_str + '&signature=' + signature
    
    response = requests.post(url, headers=headers, data=data, timeout=10)
    return response.json()

def emergency_close_all():
    """紧急平仓所有持仓"""
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🚨 紧急停止 - 平仓所有持仓                               ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('')
    
    # 确认
    print('⚠️  警告：此操作将立即平仓所有持仓！')
    print('')
    
    # 获取账户余额
    print('📊 查询账户持仓...')
    account = get_account()
    balances = account.get('balances', [])
    
    # 找出所有非零持仓
    positions = []
    for b in balances:
        asset = b['asset']
        free = float(b['free'])
        
        if free > 0 and asset not in ['USDT', 'USDC', 'BUSD']:
            # 获取价格
            try:
                price = get_price(f'{asset}USDT')
                value = free * price
                
                if value > 10:  # 只平仓价值>10 USDT 的持仓
                    positions.append({
                        'asset': asset,
                        'quantity': free,
                        'price': price,
                        'value': value
                    })
            except:
                pass
    
    if not positions:
        print('✅ 无持仓需要平仓')
        return
    
    print(f'📦 发现 {len(positions)} 个持仓:')
    for pos in positions:
        print(f'  - {pos["asset"]}: {pos["quantity"]:.6f} @ ${pos["price"]:.2f} = ${pos["value"]:.2f}')
    print('')
    
    # 执行平仓
    print('⚡ 执行平仓...')
    results = []
    
    for pos in positions:
        symbol = f'{pos["asset"]}USDT'
        
        # 市价卖出
        order = place_market_order(symbol, 'SELL', pos['quantity'])
        
        if 'orderId' in order:
            exec_qty = float(order.get('executedQty', pos['quantity']))
            exec_amount = float(order.get('cummulativeQuoteQty', 0))
            
            results.append({
                'asset': pos['asset'],
                'status': 'SUCCESS',
                'quantity': exec_qty,
                'amount': exec_amount
            })
            
            print(f'  ✅ {pos["asset"]}: 已平仓 {exec_qty:.6f} @ ${exec_amount/exec_qty:.2f} = ${exec_amount:.2f}')
        else:
            results.append({
                'asset': pos['asset'],
                'status': 'FAILED',
                'error': order.get('msg', 'Unknown error')
            })
            
            print(f'  ❌ {pos["asset"]}: 平仓失败 - {order.get("msg", "Unknown error")}')
    
    print('')
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  📋 紧急停止完成                                          ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    print(f'成功：{success_count}/{len(positions)}')
    print(f'失败：{len(positions) - success_count}/{len(positions)}')
    print('')
    
    # 记录日志
    log_file = Path('/home/nicola/.openclaw/workspace/logs/emergency-stop.log')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(f'\n[{datetime.now().isoformat()}] 紧急停止\n')
        for r in results:
            f.write(f'  {r["asset"]}: {r["status"]}\n')
    
    print('📝 日志已记录')
    
    # 停止所有交易脚本
    print('')
    print('⚠️  请手动停止以下运行中的脚本:')
    print('  - auto-exit-manager.py')
    print('  - trading-strategy.py')
    print('')
    print('命令：pkill -f auto-exit-manager.py')


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--confirm':
        emergency_close_all()
    else:
        print('╔══════════════════════════════════════════════════════════╗')
        print('║  🚨 紧急停止开关 v1.0                                     ║')
        print('╚══════════════════════════════════════════════════════════╝')
        print('')
        print('⚠️  警告：此操作将立即平仓所有持仓！')
        print('')
        print('使用方法:')
        print('  python3 emergency-stop.py --confirm')
        print('')
        print('或者添加快捷命令到 ~/.bashrc:')
        print("  alias binance-emergency='python3 /home/nicola/.openclaw/workspace/scripts/emergency-stop.py --confirm'")
        print('')
