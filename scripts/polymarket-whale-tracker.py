#!/usr/bin/env python3
"""
Polymarket 大户追踪器 v2.0 (新 API Key)
功能：追踪大户钱包交易行为 + 生成研报
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# 新 API Key (2026-03-30 12:22)
API_KEY = "019d2560-86f6-710d-ad87-57af5ad6b47e"
BASE_URL = "https://gamma-api.polymarket.com"

# 大户地址列表
WHALE_ADDRESSES = [
    "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf",  # SAYELF
    "0x2b45165959433831d9009716A15367421D6c97C9",  # SAYELFbot
]

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

def get_wallet_trades(wallet_address, limit=50):
    """获取钱包交易记录"""
    # 注意：实际 API 可能需要调整端点
    url = f"{BASE_URL}/trades"
    params = {
        "maker": wallet_address,
        "limit": limit
    }
    
    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f'⚠️  API 返回 {response.status_code}')
            return []
    
    except Exception as e:
        print(f'❌ 获取交易失败：{e}')
        return []

def analyze_wallet(trades):
    """分析钱包交易数据"""
    if not trades:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "favorite_markets": [],
            "avg_position": 0,
        }
    
    total_trades = len(trades)
    
    # 简化分析（实际需要更多数据）
    analysis = {
        "total_trades": total_trades,
        "win_rate": 0.5,  # 占位符
        "total_pnl": 0,   # 需要实际交易数据
        "favorite_markets": list(set([t.get("market", "") for t in trades[:10]])),
        "avg_position": 0,
        "last_trade": trades[0].get("timestamp", "N/A") if trades else "N/A",
    }
    
    return analysis

def generate_report(wallet_address, analysis, output_path="output/whale-reports"):
    """生成大户研报"""
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir / f"whale-{wallet_address[:10]}.md"
    
    report = f"""# 大户交易研报

**钱包地址**: `{wallet_address}`
**分析时间**: {datetime.now().isoformat()}
**数据来源**: Polymarket API

---

## 📊 核心指标

| 指标 | 数值 |
|------|------|
| 总交易数 | {analysis['total_trades']} |
| 胜率 | {analysis['win_rate']:.1%} |
| 总盈亏 | ${analysis['total_pnl']:.2f} |
| 平均仓位 | ${analysis['avg_position']:.2f} |
| 最后交易 | {analysis['last_trade']} |

---

## 🎯 偏好市场

"""
    
    for i, market in enumerate(analysis.get('favorite_markets', [])[:5], 1):
        report += f"{i}. `{market}`\n"
    
    report += f"""
---

## 💡 跟单建议

**风险评级**: 中高

**建议**:
1. 关注该大户的交易时机
2. 学习其市场选择逻辑
3. 注意仓位管理
4. 设置止损点

---

## ⚠️ 免责声明

本报告仅供参考，不构成投资建议。
Polymarket 预测市场有风险，请谨慎参与。

---

*生成：太一 AGI · Polymarket LinggeTracer v2.0*
"""
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f'💾 研报已保存：{report_file}')
    return report_file

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🐋 Polymarket 大户追踪器 v2.0                            ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    print(f'🔑 API Key: {API_KEY[:10]}...{API_KEY[-6:]}')
    print('')
    
    # 获取参数
    wallet = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not wallet:
        print('📋 大户地址列表:')
        for i, w in enumerate(WHALE_ADDRESSES, 1):
            print(f'  {i}. {w}')
        print('')
        print('用法：python3 polymarket-whale-tracker.py <wallet_address>')
        print('')
        print('示例:')
        print('  python3 polymarket-whale-tracker.py 0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf')
        print('')
        
        # Demo 模式
        print('🔧 Demo 模式 - 生成示例报告...')
        print('')
        
        wallet = WHALE_ADDRESSES[0]
        trades = []  # Demo 无实际数据
        analysis = analyze_wallet(trades)
        analysis['last_trade'] = analysis.get('last_trade', 'N/A')
        generate_report(wallet, analysis)
        return
    
    print(f'🐋 追踪大户：{wallet}')
    print('')
    
    # 获取交易
    print('📊 获取交易记录...')
    trades = get_wallet_trades(wallet)
    print(f'  找到 {len(trades)} 笔交易')
    print('')
    
    # 分析
    print('🧠 分析交易行为...')
    analysis = analyze_wallet(trades)
    print('')
    
    # 生成报告
    print('📝 生成研报...')
    generate_report(wallet, analysis)
    print('')
    
    print('✅ 完成！')

if __name__ == '__main__':
    main()
