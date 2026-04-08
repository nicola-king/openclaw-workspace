#!/usr/bin/env python3
"""
币安交易策略主引擎 v1.0
功能：市场状态识别 + 信号生成 + 自动交易
执行：每 5 分钟检查一次
"""

import requests
import hmac
import hashlib
import time
import json
from datetime import datetime
from pathlib import Path

# 配置 - 从配置文件读取
import json
with open('/home/nicola/.openclaw/workspace/config/binance-config.json', 'r') as f:
    config = json.load(f)
API_KEY = config['api_config']['api_key']
SECRET_KEY = config['api_config']['secret_key']
BASE_URL = 'https://api.binance.com'

# 策略参数
CONFIDENCE_THRESHOLD = 0.70
MAX_POSITION_PCT = 0.25
TAKE_PROFIT_PCT = 0.10
STOP_LOSS_PCT = -0.05

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

def get_klines(symbol, interval='1h', limit=100):
    """获取 K 线数据"""
    url = f'{BASE_URL}/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params, timeout=10)
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

def calculate_indicators(klines):
    """计算技术指标"""
    closes = [float(k[4]) for k in klines]
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]
    
    # MA20, MA60
    ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
    ma60 = sum(closes[-60:]) / 60 if len(closes) >= 60 else None
    
    # RSI (简化版)
    if len(closes) >= 15:
        gains = []
        losses = []
        for i in range(len(closes)-14, len(closes)):
            change = closes[i] - closes[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14
        rsi = 100 - (100 / (1 + avg_gain/avg_loss)) if avg_loss > 0 else 100
    else:
        rsi = 50
    
    return {
        'ma20': ma20,
        'ma60': ma60,
        'rsi': rsi,
        'current_price': closes[-1] if closes else 0
    }

def detect_market_regime(indicators):
    """识别市场状态"""
    ma20 = indicators.get('ma20')
    ma60 = indicators.get('ma60')
    rsi = indicators.get('rsi', 50)
    
    if ma20 and ma60:
        if ma20 > ma60 and indicators['current_price'] > ma20:
            if rsi < 70:
                return 'TREND_UP'
        elif ma20 < ma60 and indicators['current_price'] < ma20:
            if rsi > 30:
                return 'TREND_DOWN'
    
    if rsi < 30:
        return 'OVERSOLD'
    elif rsi > 70:
        return 'OVERBOUGHT'
    
    return 'SIDEWAYS'

def generate_signal(symbol, regime, indicators):
    """生成交易信号"""
    rsi = indicators.get('rsi', 50)
    
    if regime == 'TREND_UP' and rsi < 60:
        return {'type': 'BUY', 'confidence': 0.75, 'reason': '上涨趋势 + RSI 未超买'}
    elif regime == 'TREND_DOWN' and rsi > 40:
        return {'type': 'SELL', 'confidence': 0.75, 'reason': '下跌趋势 + RSI 未超卖'}
    elif regime == 'OVERSOLD':
        return {'type': 'BUY', 'confidence': 0.72, 'reason': 'RSI 超卖反弹'}
    elif regime == 'OVERBOUGHT':
        return {'type': 'SELL', 'confidence': 0.72, 'reason': 'RSI 超买回调'}
    
    return None

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

def run_strategy():
    """运行策略"""
    print(f'[{datetime.now().isoformat()}] 运行交易策略...')
    
    # 获取账户信息
    account = get_account()
    usdt_balance = next((b for b in account.get('balances', []) if b['asset'] == 'USDT'), {'free': '0'})
    available_usdt = float(usdt_balance['free'])
    
    print(f'  可用 USDT: {available_usdt:.2f}')
    
    # 加载持仓
    positions = load_positions()
    
    # 检查是否已有持仓
    active_positions = {k: v for k, v in positions.items() if float(v.get('quantity', 0)) > 0}
    
    if active_positions:
        print(f'  当前持仓：{len(active_positions)} 个')
        for symbol, pos in active_positions.items():
            entry_price = pos.get('entry_price', 0)
            current_price = get_price(symbol)
            pnl_pct = (current_price - entry_price) / entry_price if entry_price > 0 else 0
            print(f'    {symbol}: {pnl_pct:.2%} (成本：${entry_price:.2f} → 当前：${current_price:.2f})')
        print('')
        print('  ⏸️  已有持仓，跳过开新仓')
        return
    
    # 分析 ETH/USDT
    print('📊 分析 ETH/USDT...')
    klines = get_klines('ETHUSDT', interval='1h', limit=100)
    
    if not klines:
        print('  ❌ 无法获取 K 线数据')
        return
    
    indicators = calculate_indicators(klines)
    print(f'  当前价：${indicators["current_price"]:.2f}')
    print(f'  MA20: ${indicators["ma20"]:.2f}' if indicators['ma20'] else '  MA20: N/A')
    print(f'  MA60: ${indicators["ma60"]:.2f}' if indicators['ma60'] else '  MA60: N/A')
    print(f'  RSI: {indicators["rsi"]:.1f}')
    
    # 识别市场状态
    regime = detect_market_regime(indicators)
    print(f'  市场状态：{regime}')
    
    # 生成信号
    signal = generate_signal('ETHUSDT', regime, indicators)
    
    if signal and signal['confidence'] >= CONFIDENCE_THRESHOLD:
        print(f'  ✅ 交易信号：{signal["type"]} (置信度：{signal["confidence"]:.0%})')
        print(f'  原因：{signal["reason"]}')
        
        # 计算仓位
        position_pct = min(signal['confidence'] - 0.5, MAX_POSITION_PCT)
        position_usdt = available_usdt * position_pct
        
        if position_usdt < 10:
            print(f'  ⚠️  仓位过小 ({position_usdt:.2f} USDT)，跳过')
            return
        
        # 获取价格并下单
        current_price = get_price('ETHUSDT')
        quantity = position_usdt / current_price
        
        # 精度修正（ETH 步长 0.0001）
        import math
        quantity = math.floor(quantity / 0.0001) * 0.0001
        
        print(f'  💰 仓位：{position_usdt:.2f} USDT ({position_pct:.0%})')
        print(f'  数量：{quantity:.4f} ETH')
        print('')
        print('  ⚡ 执行下单...')
        
        order = place_market_order('ETHUSDT', 'BUY', quantity)
        
        if 'orderId' in order:
            exec_qty = float(order.get('executedQty', quantity))
            exec_amount = float(order.get('cummulativeQuoteQty', position_usdt))
            exec_price = exec_amount / exec_qty if exec_qty > 0 else current_price
            
            print(f'    ✅ 订单成交：{order["orderId"]}')
            print(f'    成交价：${exec_price:.2f}')
            print(f'    成交量：{exec_qty:.4f} ETH')
            print(f'    成交额：{exec_amount:.2f} USDT')
            
            # 保存持仓
            positions['ETHUSDT'] = {
                'symbol': 'ETHUSDT',
                'side': 'BUY',
                'entry_price': exec_price,
                'quantity': exec_qty,
                'entry_time': datetime.now().isoformat(),
                'take_profit': exec_price * (1 + TAKE_PROFIT_PCT),
                'stop_loss': exec_price * (1 + STOP_LOSS_PCT)
            }
            save_positions(positions)
            
            # 发送通知
            from notification_service import notify_trade
            notify_trade('ETHUSDT', 'BUY', exec_price, exec_qty, exec_amount)
            
            print('')
            print('  ✅ 持仓已记录')
        else:
            print(f'    ❌ 下单失败：{order.get("msg", "Unknown error")}')
    else:
        print('  ⏸️  无有效交易信号，等待下次检查')

def main():
    """主函数"""
    import sys
    
    if '--cron' in sys.argv:
        # Cron 模式：静默运行
        run_strategy()
    else:
        # 交互模式
        print('╔══════════════════════════════════════════════════════════╗')
        print('║  🚀 币安交易策略主引擎 v1.0                               ║')
        print('║  太一 AGI · 智能自动交易                                  ║')
        print('╚══════════════════════════════════════════════════════════╝')
        print('')
        run_strategy()

if __name__ == '__main__':
    main()
