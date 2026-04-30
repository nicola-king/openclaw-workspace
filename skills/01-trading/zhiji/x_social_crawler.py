#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) 社交媒体爬虫 - 币安广场热度监控
基于 lanaaielsa 的 AI 辅助交易系统 (2026 年 4 月最大突破)

核心逻辑:
1. 爬取币安广场帖子量数据
2. 找出每天发帖量最多的币种
3. 对应涨幅榜找异动标的
4. 自动买入同时挂止损
5. 止损逻辑：固定金额止损 (亏 200U 就出)

作者：太一 AGI
创建：2026-04-22
版本：v1.0
"""

import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
import logging

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/x_crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('XSocialCrawler')

# 数据目录
DATA_DIR = Path("/home/nicola/.openclaw/workspace/data/x-social-crawler")
DATA_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class SocialSignal:
    """社交信号"""
    symbol: str
    post_count: int  # 发帖量
    likes: int  # 点赞数
    views: int  # 浏览量
    sentiment: str  # 情绪：positive/negative/neutral
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TradingSignal:
    """交易信号"""
    symbol: str
    action: str  # BUY/SELL
    entry_price: float
    stop_loss_price: float
    stop_loss_usdt: float  # 固定金额止损 (200U)
    position_size: float  # 仓位大小 (100U 起步)
    reason: str
    social_score: int  # 社交热度评分
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class XSocialCrawler:
    """X 社交媒体爬虫"""
    
    def __init__(self):
        self.base_url = "https://x.com"
        self.binance_square_url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
        self.session = None
        self.hot_symbols = []
        self.trading_signals = []
        
        # 配置
        self.config = {
            'min_post_count': 100,  # 最小发帖量
            'min_likes': 400,  # 最小点赞数
            'min_views': 100000,  # 最小浏览量 (10 万)
            'stop_loss_usdt': 200,  # 固定止损 200U
            'initial_position': 100,  # 起始仓位 100U
        }
        
        logger.info("🕷️ X 社交媒体爬虫 v1.0 已初始化")
        logger.info(f"  最小发帖量：{self.config['min_post_count']}")
        logger.info(f"  最小点赞数：{self.config['min_likes']}")
        logger.info(f"  最小浏览量：{self.config['min_views']}")
        logger.info(f"  固定止损：{self.config['stop_loss_usdt']}U")
        logger.info(f"  起始仓位：{self.config['initial_position']}U")
    
    async def start_session(self):
        """启动 HTTP 会话"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json, text/plain, */*',
                }
            )
            logger.info("✅ HTTP 会话已启动")
    
    async def close_session(self):
        """关闭 HTTP 会话"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("✅ HTTP 会话已关闭")
    
    async def crawl_binance_square(self, limit: int = 50) -> List[Dict]:
        """爬取币安广场帖子"""
        logger.info(f"📊 开始爬取币安广场，限制：{limit} 条")
        
        posts = []
        
        try:
            # 模拟请求币安广场 API
            # 注意：实际需要逆向币安广场 API
            # 这里使用示例数据
            
            sample_posts = [
                {
                    'symbol': 'BTC',
                    'title': 'BTC 突破新高',
                    'likes': 950,
                    'views': 525000,
                    'sentiment': 'positive',
                },
                {
                    'symbol': 'ETH',
                    'title': 'ETH 生态爆发',
                    'likes': 418,
                    'views': 116000,
                    'sentiment': 'positive',
                },
                {
                    'symbol': 'SOL',
                    'title': 'SOL 链上活动激增',
                    'likes': 320,
                    'views': 89000,
                    'sentiment': 'positive',
                },
            ]
            
            posts = sample_posts
            logger.info(f"✅ 爬取到 {len(posts)} 条帖子")
            
        except Exception as e:
            logger.error(f"❌ 爬取失败：{e}")
        
        return posts
    
    async def analyze_social_signals(self, posts: List[Dict]) -> List[SocialSignal]:
        """分析社交信号"""
        logger.info("📈 开始分析社交信号...")
        
        signals = []
        
        # 按币种聚合
        symbol_stats = {}
        for post in posts:
            symbol = post.get('symbol', 'UNKNOWN')
            if symbol not in symbol_stats:
                symbol_stats[symbol] = {
                    'post_count': 0,
                    'total_likes': 0,
                    'total_views': 0,
                    'sentiment_scores': [],
                }
            
            symbol_stats[symbol]['post_count'] += 1
            symbol_stats[symbol]['total_likes'] += post.get('likes', 0)
            symbol_stats[symbol]['total_views'] += post.get('views', 0)
            
            sentiment = post.get('sentiment', 'neutral')
            sentiment_score = 1 if sentiment == 'positive' else (-1 if sentiment == 'negative' else 0)
            symbol_stats[symbol]['sentiment_scores'].append(sentiment_score)
        
        # 生成信号
        for symbol, stats in symbol_stats.items():
            avg_sentiment = sum(stats['sentiment_scores']) / len(stats['sentiment_scores'])
            sentiment_label = 'positive' if avg_sentiment > 0.3 else ('negative' if avg_sentiment < -0.3 else 'neutral')
            
            signal = SocialSignal(
                symbol=symbol,
                post_count=stats['post_count'],
                likes=stats['total_likes'],
                views=stats['total_views'],
                sentiment=sentiment_label,
            )
            
            # 过滤低质量信号
            if (signal.post_count >= self.config['min_post_count'] and
                signal.likes >= self.config['min_likes'] and
                signal.views >= self.config['min_views']):
                signals.append(signal)
                logger.info(f"✅ {symbol}: {signal.post_count}帖/{signal.likes}赞/{signal.views}览/{signal.sentiment}")
        
        # 按热度排序
        signals.sort(key=lambda x: x.post_count * 0.4 + x.likes * 0.4 + x.views * 0.2, reverse=True)
        
        self.hot_symbols = [s.symbol for s in signals[:10]]
        logger.info(f"🔥 热门币种：{self.hot_symbols}")
        
        return signals
    
    async def generate_trading_signals(self, social_signals: List[SocialSignal], 
                                       market_data: Dict) -> List[TradingSignal]:
        """生成交易信号"""
        logger.info("🎯 开始生成交易信号...")
        
        signals = []
        
        for social in social_signals[:5]:  # 只处理前 5 个热门币种
            symbol = social.symbol
            
            # 获取市场数据 (实际应从币安 API 获取)
            current_price = market_data.get(symbol, {}).get('price', 0)
            price_change_24h = market_data.get(symbol, {}).get('price_change_24h', 0)
            
            if current_price == 0:
                logger.warning(f"⚠️ {symbol} 价格数据缺失，跳过")
                continue
            
            # 生成交易信号
            # 止损逻辑：固定金额止损 (亏 200U 就出)
            position_size = self.config['initial_position']  # 100U 起步
            stop_loss_usdt = self.config['stop_loss_usdt']  # 200U 止损
            
            # 计算止损价格
            if social.sentiment == 'positive' and price_change_24h > 5:
                # 做多信号
                action = 'BUY'
                stop_loss_price = current_price * (1 - stop_loss_usdt / position_size)
                reason = f"社交热度高 (发帖{social.post_count}/点赞{social.likes}) + 涨幅{price_change_24h:.1f}%"
                
                signal = TradingSignal(
                    symbol=symbol,
                    action=action,
                    entry_price=current_price,
                    stop_loss_price=stop_loss_price,
                    stop_loss_usdt=stop_loss_usdt,
                    position_size=position_size,
                    reason=reason,
                    social_score=social.post_count * 10 + social.likes,
                )
                
                signals.append(signal)
                logger.info(f"✅ {symbol} {action}: 入场${current_price:.2f}, 止损${stop_loss_price:.2f} (-{stop_loss_usdt}U), 原因：{reason}")
        
        self.trading_signals = signals
        return signals
    
    async def run(self):
        """运行爬虫"""
        logger.info("=" * 60)
        logger.info("🕷️ X 社交媒体爬虫启动")
        logger.info("=" * 60)
        
        try:
            await self.start_session()
            
            # 1. 爬取币安广场
            posts = await self.crawl_binance_square()
            
            # 2. 分析社交信号
            social_signals = await self.analyze_social_signals(posts)
            
            # 3. 获取市场数据 (模拟)
            market_data = {
                'BTC': {'price': 78000, 'price_change_24h': 2.5},
                'ETH': {'price': 3500, 'price_change_24h': 8.2},
                'SOL': {'price': 150, 'price_change_24h': 12.5},
            }
            
            # 4. 生成交易信号
            trading_signals = await self.generate_trading_signals(social_signals, market_data)
            
            # 5. 保存数据
            await self.save_data(social_signals, trading_signals)
            
            logger.info("=" * 60)
            logger.info("✅ 爬虫运行完成")
            logger.info(f"  热门币种：{len(self.hot_symbols)}")
            logger.info(f"  交易信号：{len(trading_signals)}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ 运行失败：{e}")
        finally:
            await self.close_session()
    
    async def save_data(self, social_signals: List[SocialSignal], 
                       trading_signals: List[TradingSignal]):
        """保存数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存社交信号
        social_file = DATA_DIR / f"social_signals_{timestamp}.json"
        with open(social_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(s) for s in social_signals], f, indent=2, ensure_ascii=False)
        logger.info(f"💾 社交信号已保存：{social_file}")
        
        # 保存交易信号
        trading_file = DATA_DIR / f"trading_signals_{timestamp}.json"
        with open(trading_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(t) for t in trading_signals], f, indent=2, ensure_ascii=False)
        logger.info(f"💾 交易信号已保存：{trading_file}")
        
        # 更新最新数据
        latest_social_file = DATA_DIR / "latest_social_signals.json"
        with open(latest_social_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(s) for s in social_signals], f, indent=2, ensure_ascii=False)
        
        latest_trading_file = DATA_DIR / "latest_trading_signals.json"
        with open(latest_trading_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(t) for t in trading_signals], f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 最新数据已更新")


async def main():
    """主函数"""
    crawler = XSocialCrawler()
    await crawler.run()


if __name__ == "__main__":
    asyncio.run(main())
