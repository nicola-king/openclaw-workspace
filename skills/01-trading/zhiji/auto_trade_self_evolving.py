#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动交易自进化智能体 - 统一架构版本

功能:
1. 条件触发 (交易失败/余额不足/API 错误时触发)
2. 自动自愈 (重试/切换策略/调整参数)
3. 学习能力 (分析交易失败模式)
4. 知识固化 (写入 PITFALLS.md)

作者：太一 AGI
创建：2026-04-23
版本：v2.0 (自进化智能体)
"""

import sys
import requests
import hmac
import hashlib
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
ENV_FILE = WORKSPACE.parent / ".env"
sys.path.insert(0, str(WORKSPACE / "skills" / "07-system"))
from self_evolving_task_base import SelfEvolvingTask, TaskResult

# 币安配置
BINANCE_API_URL = "https://api.binance.com"
PROXY = "http://127.0.0.1:7890"
MIN_ORDER_VALUE = 10  # 最小交易额 $10

class AutoTradeSelfEvolving(SelfEvolvingTask):
    """自动交易自进化智能体"""
    
    def __init__(self):
        super().__init__("auto_trade")
        self.api_key = None
        self.api_secret = None
        self.balance = {}
        self.load_credentials()
    
    def load_credentials(self):
        """加载 API 凭证"""
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("BINANCE_API_KEY="):
                        self.api_key = line.split("=")[1].strip()
                    elif line.startswith("BINANCE_API_SECRET="):
                        self.api_secret = line.split("=")[1].strip()
    
    def get_balance(self) -> Dict:
        """获取账户余额"""
        try:
            timestamp = int(time.time() * 1000)
            params = f"timestamp={timestamp}"
            signature = hmac.new(
                self.api_secret.encode('utf-8'),
                params.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            url = f"{BINANCE_API_URL}/api/v3/account?{params}&signature={signature}"
            headers = {"X-MBX-APIKEY": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10, proxies={
                'http': PROXY,
                'https': PROXY,
            })
            
            if response.status_code == 200:
                account = response.json()
                balances = {'USDT': 0.0, 'BTC': 0.0, 'ETH': 0.0}
                
                if 'balances' in account:
                    for asset in account['balances']:
                        if asset['asset'] in balances:
                            balances[asset['asset']] = float(asset['free']) + float(asset['locked'])
                
                self.balance = balances
                return balances
            else:
                return {}
                
        except Exception as e:
            return {}
    
    def check(self) -> TaskResult:
        """条件检查 - 交易条件是否满足"""
        try:
            if not self.api_key or not self.api_secret:
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error='API 凭证未配置'
                )
            
            balance = self.get_balance()
            
            if not balance:
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error='无法获取余额'
                )
            
            usdt_balance = balance.get('USDT', 0.0)
            btc_balance = balance.get('BTC', 0.0)
            
            # 检查是否可交易
            can_trade = usdt_balance >= MIN_ORDER_VALUE or btc_balance >= 0.00013
            
            if can_trade:
                return TaskResult(
                    task_id=self.task_id,
                    success=True,
                    need_heal=False,
                    error=None
                )
            else:
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error=f'余额不足：USDT=${usdt_balance:.2f}, BTC={btc_balance:.5f} (需要≥${MIN_ORDER_VALUE})'
                )
                
        except Exception as e:
            return TaskResult(
                task_id=self.task_id,
                success=False,
                need_heal=True,
                error=f'检查失败：{str(e)}'
            )
    
    def heal(self, error: str) -> bool:
        """自动自愈 - 根据问题类型处理"""
        try:
            if 'API 凭证' in error:
                self.write_to_pitfalls(error, "请在.env 文件中配置 BINANCE_API_KEY 和 BINANCE_API_SECRET")
                return False
            
            elif '无法获取余额' in error:
                # 重试 3 次
                for i in range(3):
                    time.sleep(2 ** i)
                    balance = self.get_balance()
                    if balance:
                        self.write_to_pitfalls(
                            error,
                            f'重试 {i+1} 次后恢复'
                        )
                        return True
                return False
            
            elif '余额不足' in error:
                self.write_to_pitfalls(
                    error,
                    f'需要充值 USDT ≥${MIN_ORDER_VALUE} 或等待 BTC 升值'
                )
                return False
            
            else:
                return False
                
        except Exception as e:
            print(f"自愈失败：{str(e)}")
            return False
    
    def get_status(self) -> dict:
        """获取状态"""
        status = super().get_status()
        status['balance'] = self.balance
        status['can_trade'] = self.balance.get('USDT', 0) >= MIN_ORDER_VALUE or self.balance.get('BTC', 0) >= 0.00013
        return status

if __name__ == '__main__':
    trader = AutoTradeSelfEvolving()
    result = trader.execute()
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"💰 自动交易自进化智能体")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"账户余额:")
    for asset, amount in trader.balance.items():
        if asset == 'USDT':
            print(f"  {asset}: ${amount:.2f}")
        else:
            print(f"  {asset}: {amount:.5f}")
    print(f"")
    print(f"可交易：{'✅ 是' if trader.balance.get('USDT', 0) >= MIN_ORDER_VALUE or trader.balance.get('BTC', 0) >= 0.00013 else '❌ 否'}")
    print(f"最小交易额：${MIN_ORDER_VALUE}")
    print(f"")
    print(f"执行结果：{'✅ 成功' if result.success else '❌ 失败'}")
    print(f"需要自愈：{'🔧 是' if result.need_heal else '❌ 否'}")
    if result.error:
        print(f"错误信息：{result.error}")
    print(f"")
    print(f"进化指标:")
    print(f"  总运行次数：{trader.metrics.total_runs}")
    print(f"  发现问题：{trader.metrics.issues_found}")
    print(f"  自愈成功：{trader.metrics.auto_healed}")
    print(f"  成功率：{trader.metrics.success_rate:.1f}%")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
