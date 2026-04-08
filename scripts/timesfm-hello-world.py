#!/usr/bin/env python3
"""
TimesFM 气象预测器 - Hello World 测试
用途：验证 TimesFM 安装和基本功能
"""

import sys
import subprocess
import numpy as np
from datetime import datetime, timedelta

def check_installation():
    """检查 TimesFM 是否已安装"""
    try:
        import timesfm
        print(f"✅ TimesFM 已安装")
        print(f"   版本：{timesfm.__version__ if hasattr(timesfm, '__version__') else 'unknown'}")
        return True
    except ImportError:
        print("❌ TimesFM 未安装")
        return False

def install_timesfm():
    """安装 TimesFM"""
    print("\n📦 安装 TimesFM...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "timesfm"])
    print("✅ TimesFM 安装完成")

def hello_world():
    """TimesFM Hello World 测试"""
    print("\n" + "="*60)
    print("🧪 TimesFM Hello World 测试")
    print("="*60)
    
    try:
        import timesfm
        
        # 创建模拟气象数据（30 天温度序列）
        print("\n📊 生成模拟气象数据...")
        np.random.seed(42)
        days = 30
        base_temp = 25  # 基础温度 25°C
        trend = np.linspace(0, 5, days)  # 逐渐升温趋势
        seasonal = 5 * np.sin(np.linspace(0, 2*np.pi, days))  # 季节性波动
        noise = np.random.normal(0, 2, days)  # 随机噪声
        temperature = base_temp + trend + seasonal + noise
        
        print(f"   数据点数：{len(temperature)}")
        print(f"   温度范围：{temperature.min():.1f}°C - {temperature.max():.1f}°C")
        print(f"   平均温度：{temperature.mean():.1f}°C")
        
        # 注意：由于 TimesFM 需要实际加载模型，这里仅做数据结构测试
        # 实际模型推理需要下载模型文件（~500MB）
        
        print("\n📈 数据结构验证...")
        context = temperature.reshape(1, -1, 1)
        print(f"   输入形状：{context.shape}")
        print(f"   数据类型：{context.dtype}")
        
        print("\n✅ 数据结构验证通过")
        print("\n⚠️  完整模型测试需要：")
        print("   1. 下载模型文件 (~500MB)")
        print("   2. 首次加载需要 2-5 分钟")
        print("   3. 建议运行完整测试脚本：timesfm-full-test.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        return False

def show_next_steps():
    """显示下一步操作"""
    print("\n" + "="*60)
    print("📋 下一步操作")
    print("="*60)
    print("""
1. 安装 TimesFM:
   pip install timesfm

2. 运行完整测试:
   python3 timesfm-full-test.py

3. 集成到知几-E 策略:
   python3 zhiji-e-with-timesfm.py

4. 查看技术验证报告:
   cat reports/timesfm-validation-report.md
    """)

def main():
    print('╔══════════════════════════════════════════════════════════╗')
    print('║  🤖 TimesFM Hello World 测试                              ║')
    print('║  TASK-101: TimesFM 集成评估                               ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print('')
    print(f'⏰ 时间：{datetime.now().isoformat()}')
    
    # 检查安装
    if not check_installation():
        response = input("\n是否立即安装 TimesFM? (y/n): ").strip().lower()
        if response == 'y':
            install_timesfm()
        else:
            print("\n❌ 请先安装 TimesFM 后重试")
            return 1
    
    # 运行 Hello World 测试
    success = hello_world()
    
    # 显示下一步
    show_next_steps()
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
