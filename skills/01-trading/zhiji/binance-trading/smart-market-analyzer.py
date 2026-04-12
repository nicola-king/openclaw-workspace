#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能行情判断系统

功能:
- 自动识别震荡市 vs 单边市
- 智能调整杠杆倍数
- 自适应交易策略
- 动态止损止盈
"""

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SmartMarketAnalyzer')

class SmartMarketAnalyzer:
    """智能行情分析器"""
    
    def __init__(self):
        self.market_state = 'unknown'  # trending_up, trending_down, ranging
        self.suggested_leverage = 1    # 1-3 倍
        self.confidence = 0.0
    
    def analyze_market(self, price_data: dict) -> dict:
        """
        分析市场状态
        
        输入:
        {
            'symbol': 'BTCUSDT',
            'current_price': 50000,
            'ma_20': 49500,
            'ma_50': 48000,
            'ma_200': 45000,
            'rsi': 55,
            'atr': 2000,  # 平均真实波动范围
            'volume_ratio': 1.2,  # 成交量比率
            'price_change_24h': 0.03  # 24 小时涨跌幅
        }
        
        输出:
        {
            'market_state': 'trending_up',  # trending_up, trending_down, ranging
            'suggested_leverage': 2,  # 1-3 倍
            'stop_loss': -0.02,
            'take_profit': 0.50,
            'confidence': 0.85,
            'reason': '均线多头排列，RSI 中性，成交量放大'
        }
        """
        symbol = price_data.get('symbol', 'UNKNOWN')
        current_price = price_data.get('current_price', 0)
        ma_20 = price_data.get('ma_20', 0)
        ma_50 = price_data.get('ma_50', 0)
        ma_200 = price_data.get('ma_200', 0)
        rsi = price_data.get('rsi', 50)
        atr = price_data.get('atr', 0)
        volume_ratio = price_data.get('volume_ratio', 1.0)
        price_change_24h = price_data.get('price_change_24h', 0)
        
        logger.info(f"分析 {symbol} 市场状态...")
        
        # 1. 判断趋势 (均线排列)
        if ma_20 > ma_50 > ma_200:
            trend = 'up'
            trend_strength = (ma_20 - ma_200) / ma_200  # 趋势强度
        elif ma_20 < ma_50 < ma_200:
            trend = 'down'
            trend_strength = abs((ma_20 - ma_200) / ma_200)
        else:
            trend = 'ranging'
            trend_strength = 0
        
        # 2. 判断震荡 vs 单边
        # 使用 ATR 和价格波动判断
        price_volatility = abs(price_change_24h)
        
        if price_volatility < 0.02 and trend_strength < 0.05:
            market_state = 'ranging'  # 震荡市
        elif trend == 'up' and price_volatility >= 0.02:
            market_state = 'trending_up'  # 单边上涨
        elif trend == 'down' and price_volatility >= 0.02:
            market_state = 'trending_down'  # 单边下跌
        else:
            market_state = 'ranging'
        
        # 3. 智能推荐杠杆
        if market_state == 'ranging':
            # 震荡市：低杠杆或无杠杆
            suggested_leverage = 1
            stop_loss = -0.015  # -1.5%
            take_profit = 0.20  # +20%
        elif market_state in ['trending_up', 'trending_down']:
            # 单边市：根据趋势强度和 RSI 调整杠杆
            if trend_strength > 0.1 and 30 < rsi < 70:
                # 强趋势 + RSI 中性 → 高杠杆
                suggested_leverage = 3
            elif trend_strength > 0.05 and 20 < rsi < 80:
                # 中等趋势 → 中杠杆
                suggested_leverage = 2
            else:
                # 弱趋势或 RSI 极端 → 低杠杆
                suggested_leverage = 1
            
            stop_loss = -0.02  # -2%
            take_profit = 0.50  # +50%
        else:
            suggested_leverage = 1
            stop_loss = -0.02
            take_profit = 0.50
        
        # 4. 计算置信度
        confidence_factors = []
        
        # 均线排列一致性
        if (trend == 'up' and ma_20 > ma_50 > ma_200) or \
           (trend == 'down' and ma_20 < ma_50 < ma_200):
            confidence_factors.append(0.3)
        else:
            confidence_factors.append(0.1)
        
        # RSI 合理性
        if 30 < rsi < 70:
            confidence_factors.append(0.3)
        elif 20 < rsi < 80:
            confidence_factors.append(0.2)
        else:
            confidence_factors.append(0.1)
        
        # 成交量确认
        if volume_ratio > 1.2:
            confidence_factors.append(0.2)
        elif volume_ratio > 1.0:
            confidence_factors.append(0.1)
        else:
            confidence_factors.append(0.05)
        
        # 趋势强度
        if trend_strength > 0.1:
            confidence_factors.append(0.2)
        elif trend_strength > 0.05:
            confidence_factors.append(0.1)
        else:
            confidence_factors.append(0.05)
        
        confidence = sum(confidence_factors)
        confidence = min(confidence, 1.0)  # 上限 1.0
        
        # 5. 生成原因
        reason_parts = []
        if trend == 'up':
            reason_parts.append('均线多头排列')
        elif trend == 'down':
            reason_parts.append('均线空头排列')
        else:
            reason_parts.append('均线纠缠')
        
        if rsi < 30:
            reason_parts.append('RSI 超卖')
        elif rsi > 70:
            reason_parts.append('RSI 超买')
        else:
            reason_parts.append('RSI 中性')
        
        if volume_ratio > 1.2:
            reason_parts.append('成交量放大')
        elif volume_ratio < 0.8:
            reason_parts.append('成交量萎缩')
        
        if market_state == 'ranging':
            reason_parts.append('震荡市')
        else:
            reason_parts.append('单边市')
        
        reason = '，'.join(reason_parts)
        
        result = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'market_state': market_state,
            'suggested_leverage': suggested_leverage,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'confidence': confidence,
            'reason': reason,
            'metrics': {
                'trend': trend,
                'trend_strength': trend_strength,
                'rsi': rsi,
                'volume_ratio': volume_ratio,
                'price_volatility': price_volatility
            }
        }
        
        logger.info(f"市场分析完成：{market_state}, 推荐杠杆：{suggested_leverage}x, 置信度：{confidence:.2f}")
        
        return result


def main():
    """测试主函数"""
    analyzer = SmartMarketAnalyzer()
    
    # 测试用例 1: 单边上涨
    print("\n=== 测试用例 1: 单边上涨 ===")
    test_data_1 = {
        'symbol': 'BTCUSDT',
        'current_price': 52000,
        'ma_20': 51000,
        'ma_50': 49000,
        'ma_200': 45000,
        'rsi': 55,
        'atr': 2000,
        'volume_ratio': 1.5,
        'price_change_24h': 0.05
    }
    result_1 = analyzer.analyze_market(test_data_1)
    print(f"市场状态：{result_1['market_state']}")
    print(f"推荐杠杆：{result_1['suggested_leverage']}x")
    print(f"置信度：{result_1['confidence']:.2f}")
    print(f"原因：{result_1['reason']}")
    
    # 测试用例 2: 震荡市
    print("\n=== 测试用例 2: 震荡市 ===")
    test_data_2 = {
        'symbol': 'BTCUSDT',
        'current_price': 50000,
        'ma_20': 49800,
        'ma_50': 50200,
        'ma_200': 49500,
        'rsi': 48,
        'atr': 800,
        'volume_ratio': 0.9,
        'price_change_24h': 0.01
    }
    result_2 = analyzer.analyze_market(test_data_2)
    print(f"市场状态：{result_2['market_state']}")
    print(f"推荐杠杆：{result_2['suggested_leverage']}x")
    print(f"置信度：{result_2['confidence']:.2f}")
    print(f"原因：{result_2['reason']}")
    
    # 测试用例 3: 单边下跌
    print("\n=== 测试用例 3: 单边下跌 ===")
    test_data_3 = {
        'symbol': 'BTCUSDT',
        'current_price': 48000,
        'ma_20': 49000,
        'ma_50': 51000,
        'ma_200': 53000,
        'rsi': 35,
        'atr': 2500,
        'volume_ratio': 1.8,
        'price_change_24h': -0.06
    }
    result_3 = analyzer.analyze_market(test_data_3)
    print(f"市场状态：{result_3['market_state']}")
    print(f"推荐杠杆：{result_3['suggested_leverage']}x")
    print(f"置信度：{result_3['confidence']:.2f}")
    print(f"原因：{result_3['reason']}")


if __name__ == '__main__':
    main()
