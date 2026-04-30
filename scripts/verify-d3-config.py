#!/usr/bin/env python3
"""
TorchTrade Phase 1 - D3 配置验证脚本
创建时间：2026-04-04
用途：检查 .env 配置 + 验证 Binance API 连接
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加 workspace 到路径
workspace = Path(__file__).parent.parent
sys.path.insert(0, str(workspace))

def check_env_file():
    """检查 .env 文件配置"""
    print("=" * 60)
    print("TorchTrade Phase 1 - D3 配置检查")
    print("=" * 60)
    print()
    
    env_path = workspace / ".env"
    
    if not env_path.exists():
        print("❌ .env 文件不存在")
        print()
        print("请创建 .env 文件:")
        print(f"  路径：{env_path}")
        print()
        print("参考模板:")
        print(f"  cp {workspace}/.env.example {env_path}")
        print()
        return False
    
    # 加载 .env
    load_dotenv(env_path)
    
    api_key = os.getenv('BINANCE_TESTNET_API_KEY', '').strip()
    api_secret = os.getenv('BINANCE_TESTNET_API_SECRET', '').strip()
    
    print(f"📁 .env 文件：{env_path}")
    print()
    
    # 检查 API Key
    if not api_key:
        print("❌ BINANCE_TESTNET_API_KEY 未配置")
        print()
        print("请在 .env 文件中添加:")
        print("  BINANCE_TESTNET_API_KEY=your_api_key")
        return False
    else:
        print(f"✅ BINANCE_TESTNET_API_KEY: {api_key[:8]}...{api_key[-4:]}")
    
    if not api_secret:
        print("❌ BINANCE_TESTNET_API_SECRET 未配置")
        print()
        print("请在 .env 文件中添加:")
        print("  BINANCE_TESTNET_API_SECRET=your_api_secret")
        return False
    else:
        print(f"✅ BINANCE_TESTNET_API_SECRET: {api_secret[:8]}...{api_secret[-4:]}")
    
    print()
    return True


def test_binance_testnet():
    """测试 Binance 测试网连接"""
    print()
    print("=" * 60)
    print("Binance 测试网连接测试")
    print("=" * 60)
    print()
    
    api_key = os.getenv('BINANCE_TESTNET_API_KEY', '')
    api_secret = os.getenv('BINANCE_TESTNET_API_SECRET', '')
    
    if not api_key or not api_secret:
        print("⚠️  API Key 未配置，跳过连接测试")
        return False
    
    try:
        from binance.client import Client
        from binance.exceptions import BinanceAPIException
        
        # 创建测试网客户端
        client = Client(api_key, api_secret, testnet=True)
        
        print("✅ 客户端创建成功")
        print()
        
        # 获取账户信息
        print("[1/3] 获取账户状态...")
        account = client.get_account()
        print(f"     Maker 佣金：{account['makerCommission']}")
        print(f"    Taker 佣金：{account['takerCommission']}")
        
        # 获取余额
        print("\n[2/3] 获取余额...")
        balances = [b for b in account['balances'] if float(b['free']) > 0]
        if balances:
            print(f"    找到 {len(balances)} 个有余额的资产:")
            for b in balances[:5]:
                print(f"      {b['asset']}: {b['free']}")
        else:
            print("    无余额（测试网需申请测试币）")
            print("    访问 https://testnet.binance.vision 获取测试币")
        
        # 获取 K 线
        print("\n[3/3] 获取 BTCUSDT K 线...")
        klines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, limit=3)
        print(f"    成功获取 {len(klines)} 条 K 线")
        for i, k in enumerate(klines):
            timestamp = k[0]
            open_price = float(k[1])
            close_price = float(k[4])
            high_price = float(k[2])
            low_price = float(k[3])
            print(f"    [{i+1}] O:{open_price} H:{high_price} L:{low_price} C:{close_price}")
        
        print()
        print("=" * 60)
        print("✅ Binance 测试网连接测试 - 通过")
        print("=" * 60)
        return True
        
    except BinanceAPIException as e:
        print(f"\n❌ Binance API 错误")
        print(f"   消息：{e.message}")
        print(f"   状态码：{e.status_code}")
        print(f"   错误码：{e.code}")
        print()
        print("可能原因:")
        print("  1. API Key 无效或已过期")
        print("  2. IP 地址未在白名单")
        print("  3. 测试网服务暂时不可用")
        return False
        
    except Exception as e:
        print(f"\n❌ 未知错误：{type(e).__name__}: {e}")
        return False


def test_torchtrade_imports():
    """测试 TorchTrade 关键模块导入"""
    print()
    print("=" * 60)
    print("TorchTrade 模块导入测试")
    print("=" * 60)
    print()
    
    modules = [
        ("torch", "PyTorch"),
        ("torchrl", "TorchRL"),
        ("gymnasium", "Gymnasium"),
        ("torchtrade", "TorchTrade"),
    ]
    
    imports_ok = True
    
    for module, name in modules:
        try:
            __import__(module)
            mod = sys.modules[module]
            version = getattr(mod, '__version__', 'unknown')
            print(f"✅ {name}: {version}")
        except ImportError as e:
            print(f"❌ {name}: 导入失败 - {e}")
            imports_ok = False
    
    # 测试 TorchTrade 环境
    print()
    print("TorchTrade 环境:")
    try:
        from torchtrade.envs import SequentialTradingEnv
        print("✅ SequentialTradingEnv")
    except ImportError as e:
        print(f"⚠️  SequentialTradingEnv: {e}")
        imports_ok = False
    
    try:
        from torchtrade.envs import OneStepTradingEnv
        print("✅ OneStepTradingEnv")
    except ImportError as e:
        print(f"⚠️  OneStepTradingEnv: {e}")
        imports_ok = False
    
    try:
        from torchtrade.actors import RuleBasedActor
        print("✅ RuleBasedActor")
    except ImportError as e:
        print(f"⚠️  RuleBasedActor: {e}")
    
    try:
        from torchtrade.actors import FrontierLLMActor
        print("✅ FrontierLLMActor")
    except ImportError as e:
        print(f"⚠️  FrontierLLMActor: {e}")
    
    print()
    return imports_ok


if __name__ == "__main__":
    print()
    
    # 检查 .env 配置
    env_ok = check_env_file()
    
    # 测试 Binance 连接
    if env_ok:
        binance_ok = test_binance_testnet()
    else:
        binance_ok = False
        print()
        print("⚠️  跳过 Binance 连接测试（.env 未配置）")
    
    # 测试 TorchTrade 导入
    imports_ok = test_torchtrade_imports()
    
    # 总结
    print()
    print("=" * 60)
    print("D3 配置验证总结")
    print("=" * 60)
    print()
    print(f"  .env 配置：{'✅ 完成' if env_ok else '❌ 待配置'}")
    print(f"  Binance 连接：{'✅ 通过' if binance_ok else '⚠️  需配置/测试'}")
    print(f"  TorchTrade 导入：{'✅ 通过' if imports_ok else '❌ 失败'}")
    print()
    
    if env_ok and binance_ok and imports_ok:
        print("🎉 D3 配置验证 - 全部通过！")
        print()
        print("下一步:")
        print("  1. 运行 SequentialTradingEnv 示例")
        print("  2. 测试回测功能")
        print("  3. 准备 Phase 1 验收")
        sys.exit(0)
    elif env_ok and binance_ok:
        print("✅ 配置完成，可继续执行")
        sys.exit(0)
    else:
        print("⚠️  部分检查未通过，请配置 .env 文件")
        print()
        print("快速配置:")
        print(f"  cp {workspace}/.env.example {workspace}/.env")
        print("  # 编辑 .env 填入 API Key")
        sys.exit(1)
