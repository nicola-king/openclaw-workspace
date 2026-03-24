#!/usr/bin/env python3
"""
Polymarket 鲸鱼钱包追踪器
监控高收益钱包，学习策略
"""

import requests
import json
from datetime import datetime
from pathlib import Path

class WhaleTracker:
    """鲸鱼钱包追踪器"""
    
    def __init__(self):
        self.api_base = "https://gamma-api.polymarket.com"
        self.data_dir = Path(__file__).parent.parent.parent / "polymarket-data" / "whale-scans"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_leaderboard(self, limit=100):
        """获取排行榜 - 尝试多个 API endpoint"""
        endpoints = [
            f"{self.api_base}/leaderboard",
            "https://polymarket.com/api/leaderboard",
            "https://gamma-api.polymarket.com/ranking",
        ]
        
        for url in endpoints:
            try:
                params = {"limit": limit, "period": "all"}
                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                continue
        
        print("All leaderboard endpoints failed")
        return []
    
    def get_wallet_history(self, wallet_address):
        """获取钱包交易历史"""
        url = f"{self.api_base}/user/{wallet_address}/history"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching history for {wallet_address}: {e}")
            return []
    
    def analyze_top_traders(self, limit=10):
        """分析 Top 交易员"""
        leaderboard = self.get_leaderboard(limit=limit)
        
        if not leaderboard:
            print("No leaderboard data")
            return []
        
        analysis = []
        for trader in leaderboard[:limit]:
            wallet = trader.get("user", "")
            pnl = trader.get("pnl", 0)
            volume = trader.get("volume", 0)
            win_rate = trader.get("winRate", 0)
            
            print(f"🐋 {wallet[:10]}...{wallet[-8:]}")
            print(f"   PnL: ${pnl:,.2f}")
            print(f"   Volume: ${volume:,.2f}")
            print(f"   Win Rate: {win_rate:.1f}%")
            
            analysis.append({
                "wallet": wallet,
                "pnl": pnl,
                "volume": volume,
                "win_rate": win_rate,
                "scanned_at": datetime.utcnow().isoformat()
            })
        
        # 保存扫描结果
        output_file = self.data_dir / f"leaderboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=2)
        
        print(f"\n✅ Saved to {output_file}")
        return analysis

if __name__ == "__main__":
    tracker = WhaleTracker()
    print("🎯 Polymarket 鲸鱼追踪器")
    print("=" * 50)
    tracker.analyze_top_traders(limit=10)
