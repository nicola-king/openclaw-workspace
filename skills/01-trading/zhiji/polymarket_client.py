#!/usr/bin/env python3
"""
Polymarket API 客户端
支持市场数据读取和下注
"""

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
env_path = Path(__file__).parent.parent.parent / ".env.polymarket"
load_dotenv(env_path)

class PolymarketClient:
    """Polymarket API 客户端"""
    
    def __init__(self):
        self.api_key = os.getenv("POLYMARKET_API_KEY")
        self.wallet = os.getenv("POLYMARKET_WALLET")
        self.base_url = "https://gamma-api.polymarket.com"
        self.relayer_url = "https://relayer.polymarket.com"
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_market(self, market_id):
        """获取市场详情"""
        url = f"{self.base_url}/event/{market_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching market {market_id}: {e}")
            return None
    
    def get_markets(self, category=None, limit=50):
        """获取市场列表"""
        url = f"{self.base_url}/events"
        params = {"limit": limit}
        if category:
            params["category"] = category
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []
    
    def get_weather_markets(self):
        """获取天气/气象相关市场"""
        # 天气相关关键词
        keywords = [
            "temperature", "rain", "snow", "forecast", "weather",
            "celsius", "fahrenheit", "precipitation", "degree",
            "hot", "cold", "winter", "summer", "climate"
        ]
        
        markets = self.get_markets(limit=200)
        weather_markets = []
        
        for market in markets:
            title = market.get("title", "").lower()
            desc = market.get("description", "").lower()
            
            # 检查关键词
            if any(kw in title or kw in desc for kw in keywords):
                weather_markets.append(market)
        
        return weather_markets
    
    def get_odds(self, market_id):
        """获取市场赔率"""
        url = f"{self.base_url}/orderbook/{market_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("bids", []), data.get("asks", [])
        except Exception as e:
            print(f"Error fetching odds for {market_id}: {e}")
            return [], []
    
    def place_order(self, market_id, side, price, size):
        """
        下注订单
        
        Args:
            market_id: 市场 ID
            side: "buy" 或 "sell"
            price: 价格 (0-1)
            size: 数量 (USDC)
        """
        url = f"{self.relayer_url}/orders"
        payload = {
            "market": market_id,
            "side": side,
            "price": price,
            "size": size,
            "wallet": self.wallet
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error placing order: {e}")
            return None
    
    def get_balance(self):
        """获取账户余额"""
        url = f"{self.base_url}/balance/{self.wallet}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None

# 测试
if __name__ == "__main__":
    client = PolymarketClient()
    
    print("🎯 Polymarket 客户端测试")
    print("=" * 50)
    
    # 测试连接
    if client.api_key:
        print(f"✅ API Key 配置成功：{client.api_key[:10]}...")
    else:
        print("❌ API Key 未配置")
    
    if client.wallet:
        print(f"✅ 钱包地址：{client.wallet[:10]}...{client.wallet[-8:]}")
    else:
        print("❌ 钱包地址未配置")
    
    # 获取天气市场
    print("\n📊 获取天气相关市场...")
    weather_markets = client.get_weather_markets()
    print(f"找到 {len(weather_markets)} 个天气市场")
    
    for market in weather_markets[:5]:
        print(f"  - {market.get('title', 'Unknown')}")
    
    print("=" * 50)
