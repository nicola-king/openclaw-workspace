#!/usr/bin/env python3
"""
鲸鱼追踪器 v1.0
太一 AGI · 罔两数据分析军团

功能:
- 监控目标鲸鱼钱包交易
- 识别大额买入/卖出信号
- 推送告警到微信/Telegram

目标鲸鱼：majorexploiter ($2.4M 盈利)
状态：🟡 20% 进度
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class WhaleTracker:
    """鲸鱼钱包追踪器"""
    
    def __init__(self, config_path: str = "config/whale-tracker-config.json"):
        """
        初始化追踪器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.data_dir = Path("whale-data")
        self.data_dir.mkdir(exist_ok=True)
        
    def _load_config(self) -> dict:
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "enabled": True,
            "target_whales": [
                {
                    "name": "majorexploiter",
                    "address": "PENDING",  # 待填充
                    "chain": "solana",
                    "min_trade_usd": 10000,
                    "notify": True
                }
            ],
            "check_interval_seconds": 300,  # 5 分钟
            "notification_channels": ["wechat", "telegram"],
            "data_retention_days": 30
        }
    
    def save_config(self):
        """保存配置文件"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置文件已保存：{self.config_path}")
    
    def get_whale_transactions(self, whale_address: str, chain: str = "solana") -> List[dict]:
        """
        获取鲸鱼钱包交易记录
        
        Args:
            whale_address: 钱包地址
            chain: 区块链 (solana/bsc/base)
        
        Returns:
            交易列表
        """
        print(f"📡 获取鲸鱼 {whale_address[:8]}... 交易记录")
        
        # GMGN API 获取鲸鱼交易
        # API: https://api.gmgn.ai/defi/swap/v1/transactions?chain={chain}&user_addr={address}
        url = f"https://api.gmgn.ai/defi/swap/v1/transactions"
        params = {
            "chain": chain,
            "user_addr": whale_address,
            "limit": 20
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and data.get('data'):
                    transactions = []
                    for tx in data['data'].get('swap_transactions', [])[:10]:
                        # 解析 GMGN 交易数据
                        tx_type = "BUY" if tx.get('action') == 'buy' else "SELL"
                        amount_usd = float(tx.get('usd_amount', 0))
                        
                        transactions.append({
                            "hash": tx.get('tx_hash', ''),
                            "timestamp": datetime.fromtimestamp(tx.get('time', 0)).isoformat(),
                            "type": tx_type,
                            "token": tx.get('token_symbol', 'UNKNOWN'),
                            "amount_usd": amount_usd,
                            "price": float(tx.get('token_price', 0)),
                            "status": "confirmed"
                        })
                    
                    print(f"✅ 获取到 {len(transactions)} 条交易记录")
                    return transactions
            
            print(f"⚠️ API 返回异常：{response.status_code}")
        except Exception as e:
            print(f"⚠️ API 请求失败：{e}")
        
        # 返回空列表 (无数据)
        return []
    
    def analyze_transaction(self, tx: dict) -> dict:
        """
        分析交易信号
        
        Args:
            tx: 交易数据
        
        Returns:
            分析结果
        """
        amount_usd = tx.get('amount_usd', 0)
        tx_type = tx.get('type', 'UNKNOWN')
        
        # 判断是否为大额交易
        is_whale_move = amount_usd >= 10000
        
        # 判断信号强度
        if amount_usd >= 100000:
            signal_strength = "STRONG"
        elif amount_usd >= 50000:
            signal_strength = "MEDIUM"
        elif amount_usd >= 10000:
            signal_strength = "WEAK"
        else:
            signal_strength = "IGNORE"
        
        return {
            "is_whale_move": is_whale_move,
            "signal_strength": signal_strength,
            "recommendation": "WATCH" if is_whale_move else "IGNORE",
            "analysis_time": datetime.now().isoformat()
        }
    
    def send_notification(self, whale_name: str, tx: dict, analysis: dict):
        """
        发送告警通知
        
        Args:
            whale_name: 鲸鱼名称
            tx: 交易数据
            analysis: 分析结果
        """
        message = f"""
🚨 鲸鱼追踪告警

📛 鲸鱼：{whale_name}
💰 交易：{tx.get('type')} {tx.get('token')}
💵 金额：${tx.get('amount_usd'):,.2f}
📊 信号：{analysis.get('signal_strength')}
🔗 Hash: `{tx.get('hash')}`
⏰ 时间：{tx.get('timestamp')}

建议：{analysis.get('recommendation')}
"""
        
        print("📬 发送告警...")
        print(message)
        
        # 实际发送逻辑 (待实现)
        # - 微信通知
        # - Telegram 通知
    
    def check_whale(self, whale_config: dict):
        """
        检查单个鲸鱼钱包
        
        Args:
            whale_config: 鲸鱼配置
        """
        name = whale_config.get('name', 'unknown')
        address = whale_config.get('address', '')
        chain = whale_config.get('chain', 'solana')
        min_trade = whale_config.get('min_trade_usd', 10000)
        
        if not address:
            print(f"⚠️ 鲸鱼 {name} 地址未配置，跳过")
            return
        
        print(f"🔍 检查鲸鱼：{name} ({address[:8]}...)")
        
        # 获取交易
        transactions = self.get_whale_transactions(address, chain)
        
        # 分析交易
        for tx in transactions:
            if tx.get('amount_usd', 0) >= min_trade:
                analysis = self.analyze_transaction(tx)
                
                if analysis.get('is_whale_move'):
                    print(f"🚨 发现大额交易!")
                    
                    if whale_config.get('notify', True):
                        self.send_notification(name, tx, analysis)
                    
                    # 保存记录
                    self._save_transaction(name, tx, analysis)
    
    def _save_transaction(self, whale_name: str, tx: dict, analysis: dict):
        """保存交易记录"""
        date = datetime.now().strftime("%Y-%m-%d")
        file_path = self.data_dir / f"whale_{whale_name}_{date}.json"
        
        records = []
        if file_path.exists():
            with open(file_path, 'r') as f:
                records = json.load(f)
        
        records.append({
            "whale": whale_name,
            "transaction": tx,
            "analysis": analysis,
            "recorded_at": datetime.now().isoformat()
        })
        
        with open(file_path, 'w') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    
    def run_once(self):
        """执行一次检查"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║  鲸鱼追踪器 - 检查开始                                   ║")
        print("╚═══════════════════════════════════════════════════════════")
        print()
        
        for whale_config in self.config.get('target_whales', []):
            self.check_whale(whale_config)
            print()
        
        print("✅ 检查完成")
    
    def run_continuous(self):
        """持续监控"""
        interval = self.config.get('check_interval_seconds', 300)
        
        print(f"🚀 鲸鱼追踪器启动 (检查间隔：{interval}秒)")
        print("按 Ctrl+C 停止")
        
        try:
            while True:
                self.run_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 鲸鱼追踪器已停止")


def main():
    """主函数 - 测试鲸鱼追踪器"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  鲸鱼追踪器 v1.0                                          ║")
    print("║  太一 AGI · 罔两数据分析军团                               ║")
    print("╚═══════════════════════════════════════════════════════════")
    print()
    
    # 创建追踪器实例
    tracker = WhaleTracker()
    
    # 保存配置
    tracker.save_config()
    
    # 执行一次检查
    tracker.run_once()
    
    print()
    print("═══════════════════════════════════════════════════════════")
    print("下一步:")
    print("1. 配置目标鲸鱼钱包地址 (config/whale-tracker-config.json)")
    print("2. 集成 GMGN API 或 Solscan API")
    print("3. 配置通知通道 (微信/Telegram)")
    print("4. 启动持续监控 (python3 scripts/whale-tracker.py --continuous)")
    print("═══════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()
