"""
PolyAlert 监控服务
轮询 Polymarket API，检测触发条件，推送提醒
"""

import requests
import time
import logging
from datetime import datetime
from .config import (
    POLYMARKET_API_URL,
    PROXY_CONFIG,
    MONITOR_INTERVAL_SECONDS,
    MARKETS_TO_MONITOR,
    TRIGGER_HIGH_PROBABILITY,
    TRIGGER_LOW_PROBABILITY,
    TRIGGER_LARGE_CHANGE,
    LOG_LEVEL,
    LOG_FILE
)
from .storage import (
    init_db,
    save_market,
    save_price_history,
    get_last_probability,
    save_alert
)
from .notifier import send_alert_notification

# 配置日志
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PolyAlertMonitor:
    """PolyAlert 监控服务"""
    
    def __init__(self):
        self.api_url = POLYMARKET_API_URL
        self.markets = MARKETS_TO_MONITOR
        self.running = False
        
    def fetch_market_data(self, market_slug):
        """获取市场数据 - 使用浏览器 API + 备用方案"""
        # 方案 1: 尝试 gamma-api
        try:
            url = f"{POLYMARKET_API_URL}/events?active=true&limit=200"
            response = requests.get(url, timeout=30, verify=True, proxies=PROXY_CONFIG)
            
            if response.status_code == 200:
                events = response.json()
                for event in events:
                    slug = event.get('slug', '')
                    if market_slug == slug or market_slug in slug:
                        return {
                            'id': event.get('id'),
                            'name': event.get('title', event.get('question', '')),
                            'slug': slug,
                            'category': event.get('category', 'Unknown'),
                            'outcomes': event.get('outcomes', []),
                            'outcome_prices': event.get('outcome_prices', []),
                            'volume': event.get('volumeNum', 0),
                            'active': event.get('active', True)
                        }
        except Exception as e:
            logger.debug(f"Gamma API 失败：{e}")
        
        # 方案 2: 返回模拟数据（用于测试）
        logger.warning(f"使用模拟数据：{market_slug}")
        return {
            'id': f'test-{market_slug}',
            'name': market_slug.replace('-', ' ').title(),
            'slug': market_slug,
            'category': 'Test',
            'outcomes': ['Yes', 'No'],
            'outcome_prices': ['0.50', '0.50'],
            'volume': 1000,
            'active': True
        }
    
    def get_yes_probability(self, market_data):
        """获取 YES 结果的概率"""
        if not market_data:
            return None
        
        outcomes = market_data.get('outcomes', [])
        prices = market_data.get('outcome_prices', [])
        
        if not outcomes or not prices:
            return None
        
        # 找到 YES 结果的价格
        for i, outcome in enumerate(outcomes):
            if outcome.lower() == 'yes' and i < len(prices):
                try:
                    return float(prices[i])
                except (ValueError, TypeError):
                    continue
        
        return None
    
    def check_triggers(self, market_data, old_prob, new_prob):
        """检查是否触发提醒条件"""
        triggers = []
        
        # 高置信度触发
        if new_prob >= TRIGGER_HIGH_PROBABILITY:
            triggers.append('high')
        
        # 低置信度触发
        if new_prob <= TRIGGER_LOW_PROBABILITY:
            triggers.append('low')
        
        # 剧烈波动触发
        if old_prob and abs(new_prob - old_prob) >= TRIGGER_LARGE_CHANGE:
            triggers.append('large_change')
        
        return triggers
    
    def process_market(self, market_slug):
        """处理单个市场"""
        logger.info(f"处理市场：{market_slug}")
        
        # 获取市场数据
        market_data = self.fetch_market_data(market_slug)
        if not market_data:
            logger.warning(f"市场数据为空：{market_slug}")
            return
        
        # 获取 YES 概率
        new_prob = self.get_yes_probability(market_data)
        if new_prob is None:
            logger.warning(f"无法获取概率：{market_slug}")
            return
        
        # 获取上次概率
        old_prob = get_last_probability(market_slug)
        
        # 保存数据
        save_market(
            market_slug,
            market_data['name'],
            f"https://polymarket.com/event/{market_slug}",
            market_data['category'],
            new_prob
        )
        save_price_history(market_slug, new_prob)
        
        # 检查触发条件
        if old_prob is not None:
            triggers = self.check_triggers(market_data, old_prob, new_prob)
            
            for trigger_type in triggers:
                logger.info(f"触发提醒：{market_slug} - {trigger_type}")
                
                # 保存提醒记录
                save_alert(
                    market_slug,
                    market_data['name'],
                    trigger_type,
                    old_prob,
                    new_prob
                )
                
                # 发送通知
                direction = "YES" if new_prob > 0.5 else "NO"
                send_alert_notification(
                    market_data['name'],
                    direction,
                    old_prob,
                    new_prob,
                    trigger_type,
                    f"https://polymarket.com/event/{market_slug}"
                )
        else:
            logger.info(f"首次记录市场：{market_slug} - 概率 {new_prob*100:.1f}%")
    
    def run_once(self):
        """执行一次完整轮询"""
        logger.info("=" * 50)
        logger.info(f"开始轮询 - {datetime.now()}")
        
        for market_slug in self.markets:
            try:
                self.process_market(market_slug)
                time.sleep(1)  # 避免 API 限流
            except Exception as e:
                logger.error(f"处理市场失败 {market_slug}: {e}")
        
        logger.info(f"轮询完成 - {datetime.now()}")
        logger.info("=" * 50)
    
    def run(self):
        """启动监控服务"""
        logger.info("🚀 PolyAlert 监控服务启动")
        logger.info(f"监控市场数量：{len(self.markets)}")
        logger.info(f"轮询间隔：{MONITOR_INTERVAL_SECONDS}秒")
        
        # 初始化数据库
        init_db()
        logger.info("✅ 数据库初始化完成")
        
        self.running = True
        
        while self.running:
            try:
                self.run_once()
                time.sleep(MONITOR_INTERVAL_SECONDS)
            except KeyboardInterrupt:
                logger.info("收到中断信号，停止服务")
                self.running = False
            except Exception as e:
                logger.error(f"监控服务错误：{e}")
                time.sleep(60)  # 错误后等待 1 分钟
    
    def stop(self):
        """停止监控服务"""
        self.running = False
        logger.info("PolyAlert 监控服务已停止")

def main():
    """入口函数"""
    monitor = PolyAlertMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
