#!/usr/bin/env python3
"""
自动止盈止损管理器 v1.0
功能：监控持仓，触及止盈/止损自动平仓
执行：每 60 秒检查一次
"""

import requests
import hmac
import hashlib
import time
import json
from datetime import datetime
from pathlib import Path

# 配置
# 从配置文件读取
import json
with open('/home/nicola/.openclaw/workspace/config/binance-config.json', 'r') as f:
    config = json.load(f)
API_KEY = config['api_config']['api_key']
SECRET_KEY = config['api_config']['secret_key']
BASE_URL = 'https://api.binance.com'

# 止盈止损配置
TAKE_PROFIT_PCT = 0.10  # +10%
STOP_LOSS_PCT = -0.05   # -5%

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

def load_positions():
    """加载持仓文件"""
    pos_file = Path('/home/nicola/.openclaw/workspace/data/positions.json')
    if pos_file.exists():
        with open(pos_file, 'r') as f:
            return json.load(f)
    return {}

def save_positions(positions):
    """保存持仓文件"""
    pos_file = Path('/home/nicola/.openclaw/workspace/data/positions.json')
    pos_file.parent.mkdir(parents=True, exist_ok=True)
    with open(pos_file, 'w') as f:
        json.dump(positions, f, indent=2, ensure_ascii=False)

def check_and_exit():
    """检查并执行止盈止损"""
    print(f'[{datetime.now().isoformat()}] 检查止盈止损...')
    
    # 获取账户余额
    account = get_account()
    balances = account.get('balances', [])
    
    # 加载持仓记录
    positions = load_positions()
    
    # 检查每个持仓
    for symbol, position in list(positions.items()):
        entry_price = position.get('entry_price', 0)
        quantity = float(position.get('quantity', 0))
        side = position.get('side', 'BUY')
        
        if quantity <= 0:
            continue
        
        # 获取当前价格
        current_price = get_price(symbol)
        
        # 计算盈亏比例
        if side == 'BUY':
            pnl_pct = (current_price - entry_price) / entry_price
        else:
            pnl_pct = (entry_price - current_price) / entry_price
        
        # 检查止盈
        if pnl_pct >= TAKE_PROFIT_PCT:
            print(f'  ✅ 止盈触发：{symbol} 盈利 {pnl_pct:.2%}')
            
            # 平仓
            if side == 'BUY':
                order = place_market_order(symbol, 'SELL', quantity)
            else:
                order = place_market_order(symbol, 'BUY', quantity)
            
            if 'orderId' in order:
                exec_qty = float(order.get('executedQty', quantity))
                exec_amount = float(order.get('cummulativeQuoteQty', 0))
                
                print(f'    平仓订单：{order["orderId"]}')
                print(f'    成交价：${exec_amount/exec_qty:.2f}')
                print(f'    成交额：{exec_amount:.2f} USDT')
                
                # 发送通知
                send_notification('TAKE_PROFIT', symbol, pnl_pct, exec_amount)
                
                # 更新持仓
                positions[symbol]['quantity'] = 0
                positions[symbol]['exit_price'] = exec_amount / exec_qty
                positions[symbol]['exit_time'] = datetime.now().isoformat()
                positions[symbol]['pnl'] = pnl_pct
        
        # 检查止损
        elif pnl_pct <= STOP_LOSS_PCT:
            print(f'  ❌ 止损触发：{symbol} 亏损 {pnl_pct:.2%}')
            
            # 平仓
            if side == 'BUY':
                order = place_market_order(symbol, 'SELL', quantity)
            else:
                order = place_market_order(symbol, 'BUY', quantity)
            
            if 'orderId' in order:
                exec_qty = float(order.get('executedQty', quantity))
                exec_amount = float(order.get('cummulativeQuoteQty', 0))
                
                print(f'    平仓订单：{order["orderId"]}')
                print(f'    成交价：${exec_amount/exec_qty:.2f}')
                print(f'    成交额：{exec_amount:.2f} USDT')
                
                # 发送通知
                send_notification('STOP_LOSS', symbol, pnl_pct, exec_amount)
                
                # 更新持仓
                positions[symbol]['quantity'] = 0
                positions[symbol]['exit_price'] = exec_amount / exec_qty
                positions[symbol]['exit_time'] = datetime.now().isoformat()
                positions[symbol]['pnl'] = pnl_pct
        
        else:
            print(f'  📊 {symbol}: {pnl_pct:.2%} (持有中)')
    
    # 保存持仓
    save_positions(positions)
    print('')

def send_notification(event_type, symbol, pnl_pct, amount):
    """发送通知（简化版）"""
    message = f"""
🔔 交易通知

事件：{'✅ 止盈' if event_type == 'TAKE_PROFIT' else '❌ 止损'}
交易对：{symbol}
盈亏：{pnl_pct:.2%}
金额：{amount:.2f} USDT
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    # 写入通知文件
    notify_file = Path('/home/nicola/.openclaw/workspace/data/notifications.txt')
    notify_file.parent.mkdir(parents=True, exist_ok=True)
    with open(notify_file, 'a') as f:
        f.write(f'\n{message}\n')
    
    print(f'  📬 通知已记录')

def main():
    """主函数"""
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🤖 自动止盈止损管理器 v1.0                               ║')
    print('║  太一 AGI · 币安交易策略                                  ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'止盈：+{TAKE_PROFIT_PCT:.0%} | 止损：{STOP_LOSS_PCT:.0%}')
    print('')
    
    # 持续运行
    while True:
        try:
            check_and_exit()
        except Exception as e:
            print(f'❌ 错误：{e}')
        
        time.sleep(60)  # 每 60 秒检查一次

if __name__ == '__main__':
    main()
