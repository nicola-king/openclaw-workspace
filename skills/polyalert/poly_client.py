#!/usr/bin/env python3
"""
PolyAlert Polymarket 客户端
复用知几-E 的 API 配置，获取实时市场数据
"""

import requests
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from config import PROXY_CONFIG

class PolyAlertClient:
    """PolyAlert Polymarket 客户端"""
    
    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com"
        self.proxies = PROXY_CONFIG
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def get_active_events(self, limit=100):
        """获取活跃事件列表"""
        url = f"{self.base_url}/events"
        params = {"active": "true", "limit": limit}
        
        try:
            response = requests.get(
                url, 
                headers=self.headers,
                params=params, 
                proxies=self.proxies,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 获取事件失败：{e}")
            return []
    
    def get_event_by_slug(self, slug):
        """根据 slug 获取事件详情"""
        events = self.get_active_events(limit=200)
        
        for event in events:
            event_slug = event.get('slug', '')
            if slug == event_slug or slug in event_slug:
                return event
        
        return None
    
    def get_market_prices(self, event):
        """获取市场价格"""
        outcomes = event.get('outcomes', [])
        prices = event.get('outcome_prices', [])
        
        result = {}
        for i, outcome in enumerate(outcomes):
            if i < len(prices):
                try:
                    result[outcome] = float(prices[i])
                except:
                    result[outcome] = 0.0
        
        return result
    
    def search_markets(self, keywords):
        """搜索关键词相关市场"""
        events = self.get_active_events(limit=200)
        matching = []
        
        for event in events:
            title = event.get('title', '').lower()
            slug = event.get('slug', '').lower()
            
            if any(kw.lower() in title or kw.lower() in slug for kw in keywords):
                matching.append(event)
        
        return matching

# 测试
if __name__ == "__main__":
    client = PolyAlertClient()
    
    print("=" * 70)
    print("🔍 PolyAlert 客户端测试")
    print("=" * 70)
    
    # 测试获取活跃事件
    print("\n📊 获取活跃事件...")
    events = client.get_active_events(limit=10)
    
    if events:
        print(f"✅ 成功获取 {len(events)} 个事件")
        print()
        for e in events[:10]:
            slug = e.get('slug', 'N/A')
            title = e.get('title', 'N/A')[:50]
            print(f"  - {title}")
            print(f"    slug: {slug}")
            print()
    else:
        print("❌ 获取失败")
    
    print("=" * 70)
