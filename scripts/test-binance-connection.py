#!/usr/bin/env python3
"""
TorchTrade Phase 1 - Binance 测试网连接测试
创建时间：2026-04-04
用途：验证 Binance API 连接 + 获取账户信息 + 测试 K 线数据
"""

import os
import sys
from pathlib import Path

# 添加 workspace 到路径
workspace = Path(__file__).parent.parent
sys.path.insert(0, str(workspace))

def test_binance_connection():
    """测试 Binance 测试网连接"""
    print("=" * 60)
    print("TorchTrade Phase 1 - Binance 测试网连接测试")
    print("=" * 60)
    print()
    
    # 检查环境变量
    api_key = os.getenv('BINANCE_TESTNET_API_KEY', '')
    api_secret = os.getenv('BINANCE_TESTNET_API_SECRET', '')
    
    if not api_key or not api_secret:
        print("⚠️  未配置 Binance 测试网 API Key")
        print()
        print("请设置环境变量:")
        print("  export BINANCE_TESTNET_API_KEY='your_api_key'")
        print("  export BINANCE_TESTNET_API_SECRET='your_api_secret'")
        print()
        print("或者创建 .env 文件在 workspace 根目录:")
        print("  BINANCE_TESTNET_API_KEY=your_api_key")
        print("  BINANCE_TESTNET_API_SECRET=your_api_secret")
        return False
    
    try:
        from binance.client import Client
        from binance.exceptions import BinanceAPIException
        
        # 创建客户端（测试网）
        client = Client(api_key, api_secret, testnet=True)
        
        print("✅ Binance 客户端创建成功")
        print()
        
        # 获取账户信息
        print("[1/4] 获取账户信息...")
        account = client.get_account()
        print(f"    账户状态：{account['makerCommission']} / {account['takerCommission']}")
        
        # 获取余额
        print("\n[2/4] 获取余额...")
        balances = [b for b in account['balances'] if float(b['free']) > 0]
        if balances:
            for b in balances[:5]:  # 显示前 5 个
                print(f"    {b['asset']}: {b['free']} (可用) / {b['locked']} (冻结)")
        else:
            print("    无余额（测试网需申请测试币）")
        
        # 获取 K 线数据
        print("\n[3/4] 获取 BTCUSDT K 线数据...")
        klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, limit=5)
        print(f"    获取 {len(klines)} 条 K 线")
        for k in klines[:3]:
            timestamp = k[0]
            open_price = k[1]
            close_price = k[4]
            print(f"    时间：{timestamp}, 开盘：{open_price}, 收盘：{close_price}")
        
        # 获取交易对信息
        print("\n[4/4] 获取 BTCUSDT 交易对信息...")
        symbol_info = client.get_symbol_info("BTCUSDT")
        if symbol_info:
            print(f"    状态：{symbol_info['status']}")
            print(f"    最小交易量：{symbol_info['filters'][2]['minQty']} BTC")
            print(f"    价格精度：{symbol_info['filters'][0]['tickSize']} USDT")
        
        print()
        print("=" * 60)
        print("✅ Binance 测试网连接测试 - 通过")
        print("=" * 60)
        return True
        
    except BinanceAPIException as e:
        print(f"\n❌ Binance API 错误：{e.message}")
        print(f"   状态码：{e.status_code}")
        print(f"   错误码：{e.code}")
        return False
        
    except Exception as e:
        print(f"\n❌ 未知错误：{type(e).__name__}: {e}")
        return False


def test_torchtrade_env():
    """测试 TorchTrade 环境"""
    print()
    print("=" * 60)
    print("TorchTrade 环境测试")
    print("=" * 60)
    print()
    
    try:
        import torch
        import torchrl
        import gymnasium
        import torchtrade
        
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"✅ TorchRL: {torchrl.__version__}")
        print(f"✅ Gymnasium: {gymnasium.__version__}")
        print(f"✅ TorchTrade: 已安装")
        
        # 尝试导入 TorchTrade 环境
        try:
            from torchtrade.envs import SequentialTradingEnv
            print("✅ SequentialTradingEnv: 可导入")
        except ImportError as e:
            print(f"⚠️  SequentialTradingEnv: 导入失败 - {e}")
        
        try:
            from torchtrade.envs import OneStepTradingEnv
            print("✅ OneStepTradingEnv: 可导入")
        except ImportError as e:
            print(f"⚠️  OneStepTradingEnv: 导入失败 - {e}")
        
        print()
        print("=" * 60)
        print("✅ TorchTrade 环境测试 - 通过")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ TorchTrade 环境错误：{type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    print()
    
    # 测试 TorchTrade 环境
    env_ok = test_torchtrade_env()
    
    # 测试 Binance 连接
    binance_ok = test_binance_connection()
    
    print()
    print("测试总结:")
    print(f"  TorchTrade 环境：{'✅ 通过' if env_ok else '❌ 失败'}")
    print(f"  Binance 连接：{'✅ 通过' if binance_ok else '⚠️  需配置 API Key'}")
    print()
    
    if env_ok:
        print("🎉 Phase 1 D1 环境搭建完成！")
        print()
        print("下一步:")
        print("  1. 配置 Binance 测试网 API Key（如需要）")
        print("  2. 运行 SequentialTradingEnv 示例")
        print("  3. 验证回测功能")
        print()
