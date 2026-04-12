"""
Content Creator - 统一内容创作引擎
整合排期/优化/发布/生成为一体化引擎
"""

from .scheduler.content_calendar import ContentScheduler
from .optimizer.geo_seo import GEOOptimizer
from .publisher.social_publisher import SocialPublisher
from .generator.hot_topic import HotTopicGenerator


class ContentCreator:
    """内容创作引擎主入口"""
    
    def __init__(self):
        self.scheduler = ContentScheduler()
        self.optimizer = GEOOptimizer()
        self.publisher = SocialPublisher()
        self.generator = HotTopicGenerator()


__all__ = ['ContentCreator', 'ContentScheduler', 'GEOOptimizer', 'SocialPublisher', 'HotTopicGenerator']
