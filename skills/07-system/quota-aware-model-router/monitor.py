#!/usr/bin/env python3
"""
额度监控器 - 每 5 分钟检查一次并自动切换
"""

import asyncio
import time
from datetime import datetime
from quota_router import QuotaRouter


class QuotaMonitor:
    """额度监控器"""
    
    def __init__(self):
        self.router = QuotaRouter()
        self.running = False
    
    async def monitor_loop(self):
        """监控循环 (每 5 分钟)"""
        print(f"🔍 启动额度监控器...")
        print(f"   检查间隔：{self.router.config['monitor']['check_interval']}秒")
        
        while self.running:
            try:
                # 检查并切换
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 检查额度...")
                self.router.check_and_switch()
                
                # 获取状态
                status = self.router.get_status()
                print(f"   百炼：{status['bailian']['usage_rate']} ({'✅' if status['bailian']['available'] else '❌'})")
                print(f"   Gemini: {status['gemini']['usage_rate']} ({'✅' if status['gemini']['available'] else '❌'})")
                print(f"   当前模型：{status['current_model']}")
                
            except Exception as e:
                print(f"❌ 监控错误：{e}")
            
            # 等待下一次检查
            await asyncio.sleep(self.router.config["monitor"]["check_interval"])
    
    def start(self):
        """启动监控"""
        self.running = True
        try:
            asyncio.run(self.monitor_loop())
        except KeyboardInterrupt:
            print("\n👋 监控器已停止")
            self.running = False


if __name__ == "__main__":
    monitor = QuotaMonitor()
    print("=== Quota Monitor v1.0 ===")
    print("按 Ctrl+C 停止监控")
    monitor.start()
