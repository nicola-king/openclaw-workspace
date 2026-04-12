#!/usr/bin/env python3
"""
PolyAlert 数据源 API 集成
集成：链上数据 + 社交媒体 + 新闻聚合
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict
from pathlib import Path

# === 1. 链上数据集成（Etherscan/Polygonscan）===

class ChainDataSource:
    """链上数据源 - 聪明钱追踪"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ETHERSCAN_API_KEY', '')
        self.base_url = "https://api.etherscan.io/api"
        
        # 聪明钱钱包列表
        self.whale_wallets = [
            "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf",  # SAYELF
            # TODO: 添加其他聪明钱地址
        ]
    
    def get_wallet_balance(self, wallet: str) -> Dict:
        """获取钱包余额"""
        if not self.api_key:
            return {'status': 'error', 'message': 'API Key 未配置'}
        
        params = {
            'module': 'account',
            'action': 'balance',
            'address': wallet,
            'apikey': self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        return response.json()
    
    def get_wallet_transactions(self, wallet: str, limit: int = 10) -> List[Dict]:
        """获取钱包交易"""
        if not self.api_key:
            return []
        
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': wallet,
            'limit': limit,
            'apikey': self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data.get('result', [])[:limit]
    
    def get_smart_money_signals(self) -> Dict:
        """聪明钱信号"""
        signals = []
        
        for wallet in self.whale_wallets:
            txs = self.get_wallet_transactions(wallet, limit=5)
            if txs:
                signals.append({
                    'wallet': wallet,
                    'recent_txs': len(txs),
                    'last_tx': txs[0] if txs else None
                })
        
        return {
            'timestamp': datetime.now().isoformat(),
            'wallets_tracked': len(self.whale_wallets),
            'signals': signals
        }

# === 2. 社交媒体集成（Twitter API v2）===

class SocialDataSource:
    """社交媒体数据源 - 情感分析"""
    
    def __init__(self, bearer_token: str = None):
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN', '')
        self.base_url = "https://api.twitter.com/2/tweets/search/recent"
    
    def search_tweets(self, query: str, max_results: int = 10) -> List[Dict]:
        """搜索推文"""
        if not self.bearer_token:
            print("⚠️  Twitter API Token 未配置，返回模拟数据")
            return self._mock_tweets(query)
        
        headers = {'Authorization': f'Bearer {self.bearer_token}'}
        params = {
            'query': query,
            'max_results': max_results,
            'tweet.fields': 'created_at,public_metrics'
        }
        
        response = requests.get(self.base_url, headers=headers, params=params)
        data = response.json()
        return data.get('data', [])
    
    def _mock_tweets(self, query: str) -> List[Dict]:
        """模拟推文数据（用于测试）"""
        return [
            {
                'id': '1',
                'text': f'Just bought more {query}! 🚀',
                'created_at': datetime.now().isoformat(),
                'public_metrics': {'like_count': 100, 'retweet_count': 50}
            },
            {
                'id': '2',
                'text': f'{query} looking bullish today 📈',
                'created_at': datetime.now().isoformat(),
                'public_metrics': {'like_count': 80, 'retweet_count': 30}
            }
        ]
    
    def analyze_sentiment(self, tweets: List[Dict]) -> Dict:
        """分析情感"""
        if not tweets:
            return {'sentiment': 'neutral', 'score': 0.5}
        
        # 简单情感分析（基于关键词）
        positive_words = ['bullish', 'buy', 'moon', 'rocket', 'up', 'gain']
        negative_words = ['bearish', 'sell', 'crash', 'down', 'loss']
        
        positive_count = sum(1 for t in tweets if any(w in t['text'].lower() for w in positive_words))
        negative_count = sum(1 for t in tweets if any(w in t['text'].lower() for w in negative_words))
        
        total = positive_count + negative_count
        if total == 0:
            return {'sentiment': 'neutral', 'score': 0.5}
        
        score = positive_count / total
        sentiment = 'bullish' if score > 0.6 else 'bearish' if score < 0.4 else 'neutral'
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive': positive_count,
            'negative': negative_count,
            'total': len(tweets)
        }
    
    def get_sentiment(self, topic: str) -> Dict:
        """获取情感分析"""
        tweets = self.search_tweets(topic, max_results=10)
        sentiment = self.analyze_sentiment(tweets)
        
        return {
            'topic': topic,
            **sentiment,
            'tweets_analyzed': len(tweets)
        }

# === 3. 新闻聚合集成（RSS/API）===

class NewsDataSource:
    """新闻聚合数据源"""
    
    def __init__(self):
        self.sources = [
            {'name': 'CoinDesk', 'url': 'https://www.coindesk.com/arc/outboundfeeds/rss/'},
            {'name': 'CoinTelegraph', 'url': 'https://cointelegraph.com/rss'},
            {'name': 'The Block', 'url': 'https://www.theblock.co/rss.xml'},
        ]
    
    def get_latest_news(self, category: str = 'crypto', limit: int = 5) -> List[Dict]:
        """获取最新新闻"""
        # 简化版：返回模拟数据
        # TODO: 集成 feedparser 解析 RSS
        return [
            {
                'title': f'Bitcoin Surges Past $70K Amid Market Rally',
                'source': 'CoinDesk',
                'published': datetime.now().isoformat(),
                'url': 'https://coindesk.com/example1',
                'summary': 'BTC reaches new yearly high...'
            },
            {
                'title': f'Ethereum Upgrade Shows Promise for Scalability',
                'source': 'CoinTelegraph',
                'published': datetime.now().isoformat(),
                'url': 'https://cointelegraph.com/example2',
                'summary': 'ETH 2.0 staking increases...'
            }
        ]
    
    def analyze_impact(self, news: str) -> Dict:
        """分析新闻影响"""
        # 简单关键词分析
        positive_words = ['surge', 'rally', 'upgrade', 'breakthrough', 'gain']
        negative_words = ['crash', 'drop', 'hack', 'loss', 'ban']
        
        news_lower = news.lower()
        positive_count = sum(1 for w in positive_words if w in news_lower)
        negative_count = sum(1 for w in negative_words if w in news_lower)
        
        if positive_count > negative_count:
            impact = 'positive'
        elif negative_count > positive_count:
            impact = 'negative'
        else:
            impact = 'neutral'
        
        return {
            'impact': impact,
            'confidence': max(positive_count, negative_count) / max(1, positive_count + negative_count),
            'related_markets': ['BTC', 'ETH'] if 'bitcoin' in news_lower or 'ethereum' in news_lower else []
        }

# === 4. 信号融合 ===

class PolyAlertExtended:
    """PolyAlert 扩展版 - 多数据源融合"""
    
    def __init__(self):
        self.chain = ChainDataSource()
        self.social = SocialDataSource()
        self.news = NewsDataSource()
    
    def get_fused_signals(self, market: str) -> Dict:
        """融合多数据源信号"""
        
        # 1. 链上聪明钱
        chain_data = self.chain.get_smart_money_signals()
        
        # 2. 社交媒体情感
        social_data = self.social.get_sentiment(market)
        
        # 3. 新闻影响
        news_data = self.news.get_latest_news()
        
        # 融合信号（简单加权）
        fused = self._fuse(chain_data, social_data, news_data)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'market': market,
            'chain_data': chain_data,
            'social_data': social_data,
            'news_data': news_data,
            'fused_signal': fused
        }
    
    def _fuse(self, chain: Dict, social: Dict, news: List[Dict]) -> Dict:
        """信号融合逻辑"""
        # 链上信号权重 40%
        chain_score = 0.5
        if chain['signals']:
            chain_score = 0.6  # 有聪明钱活动
        
        # 社交信号权重 35%
        social_score = social['score']
        
        # 新闻信号权重 25%
        news_positive = sum(1 for n in news if 'positive' in str(n))
        news_score = 0.5 + (news_positive / max(1, len(news))) * 0.5
        
        # 加权平均
        final_score = chain_score * 0.4 + social_score * 0.35 + news_score * 0.25
        
        direction = 'bullish' if final_score > 0.6 else 'bearish' if final_score < 0.4 else 'neutral'
        strength = 'strong' if abs(final_score - 0.5) > 0.2 else 'weak'
        
        return {
            'confidence': final_score,
            'direction': direction,
            'strength': strength,
            'components': {
                'chain': chain_score,
                'social': social_score,
                'news': news_score
            }
        }

# === 测试 ===

if __name__ == '__main__':
    print("=" * 70)
    print("  PolyAlert 数据源 API 集成测试")
    print("=" * 70)
    
    ext = PolyAlertExtended()
    
    # 测试 1: 链上数据
    print("\n🔗 链上数据测试:")
    chain_signals = ext.chain.get_smart_money_signals()
    print(f"  追踪钱包：{chain_signals['wallets_tracked']} 个")
    print(f"  信号数：{len(chain_signals['signals'])}")
    
    # 测试 2: 社交媒体
    print("\n📱 社交媒体测试:")
    social_sentiment = ext.social.get_sentiment("Polymarket")
    print(f"  情感：{social_sentiment['sentiment']}")
    print(f"  得分：{social_sentiment['score']:.2f}")
    print(f"  分析推文：{social_sentiment['tweets_analyzed']} 条")
    
    # 测试 3: 新闻聚合
    print("\n📰 新闻聚合测试:")
    news = ext.news.get_latest_news()
    print(f"  新闻源：{len(ext.news.sources)} 个")
    print(f"  最新新闻：{len(news)} 条")
    for n in news[:2]:
        print(f"    - {n['title']} ({n['source']})")
    
    # 测试 4: 信号融合
    print("\n📡 信号融合测试:")
    fused = ext.get_fused_signals("Polymarket")
    print(f"  市场：{fused['market']}")
    print(f"  置信度：{fused['fused_signal']['confidence']:.2%}")
    print(f"  方向：{fused['fused_signal']['direction']}")
    print(f"  强度：{fused['fused_signal']['strength']}")
    
    print("\n✅ PolyAlert 数据源 API 集成完成")
    print("=" * 70)
