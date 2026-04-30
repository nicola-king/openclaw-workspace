#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安数量格式修复工具

问题：Python 使用科学计数法 (5e-05) 不被币安接受
解决：使用固定小数点格式 (0.00005000)

币安要求：
- 数量格式：^([0-9]{1,20})(\.[0-9]{1,20})?$
- 不接受科学计数法
"""

def format_quantity(quantity: float, symbol: str) -> str:
    """
    格式化交易数量
    
    Args:
        quantity: 原始数量
        symbol: 交易对
    
    Returns:
        格式化后的数量字符串
    """
    # 币安精度要求
    precision_map = {
        'BTC': 8,   # BTC 精度 8 位小数
        'ETH': 8,   # ETH 精度 8 位小数
        'SOL': 2,   # SOL 精度 2 位小数
        'BNB': 3,   # BNB 精度 3 位小数
    }
    
    # 提取基础币种
    base_symbol = symbol.replace('USDT', '')
    precision = precision_map.get(base_symbol, 8)
    
    # 格式化数量 (不使用科学计数法)
    formatted = "{:.{}f}".format(quantity, precision)
    
    # 移除末尾的 0
    formatted = formatted.rstrip('0').rstrip('.')
    
    # 确保至少有一位小数
    if '.' not in formatted:
        formatted += ".0"
    
    return formatted


# 测试
if __name__ == "__main__":
    test_cases = [
        (0.00005, 'BTCUSDT'),
        (0.0016, 'ETHUSDT'),
        (0.04, 'SOLUSDT'),
        (0.006, 'BNBUSDT'),
        (5e-05, 'BTCUSDT'),  # 科学计数法
        (1.6e-03, 'ETHUSDT'),
    ]
    
    print("=== 数量格式修复测试 ===\n")
    
    for quantity, symbol in test_cases:
        formatted = format_quantity(quantity, symbol)
        print(f"{symbol}:")
        print(f"  原始：{quantity} ({type(quantity).__name__})")
        print(f"  修复：{formatted} ({type(formatted).__name__})")
        print()


def format_quantity_for_binance(quantity: float, symbol: str) -> str:
    """
    为币安格式化数量 (集成到交易系统)
    
    Args:
        quantity: 原始数量
        symbol: 交易对 (如 BTCUSDT)
    
    Returns:
        格式化后的数量字符串
    """
    return format_quantity(quantity, symbol)


def ensure_min_notional(quantity: float, price: float, symbol: str, min_notional: float = 10.0) -> float:
    """
    确保满足币安最小交易额要求
    
    Args:
        quantity: 数量
        price: 价格
        symbol: 交易对
        min_notional: 最小交易额 (默认 10 USDT)
    
    Returns:
        调整后的数量
    """
    current_notional = quantity * price
    
    if current_notional < min_notional:
        # 调整数量以满足最小交易额
        new_quantity = min_notional / price
        print(f"⚠️ {symbol}: 交易额 ${current_notional:.2f} < ${min_notional}, 调整为 {new_quantity}")
        return new_quantity
    
    return quantity


# 测试
if __name__ == "__main__":
    test_cases = [
        (0.04, 88.0, 'SOLUSDT'),
        (0.006, 642.0, 'BNBUSDT'),
        (0.00005, 78000.0, 'BTCUSDT'),
        (0.0016, 2390.0, 'ETHUSDT'),
    ]
    
    print("=== 最小交易额检查测试 ===\n")
    
    for quantity, price, symbol in test_cases:
        adjusted = ensure_min_notional(quantity, price, symbol)
        print(f"{symbol}:")
        print(f"  原始：{quantity} × ${price} = ${quantity*price:.2f}")
        print(f"  调整后：{adjusted} × ${price} = ${adjusted*price:.2f}")
        print()
