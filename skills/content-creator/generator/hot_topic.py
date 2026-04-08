#!/usr/bin/env python3
"""
Hot Topic Generator - 热点选题生成器
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class HotTopic:
    """热点话题"""
    id: str
    title: str
    platform: str
    heat_score: int
    trend: str  # 'rising', 'stable', 'falling'
    tags: List[str]
    url: str
    created_at: str


class HotTopicGenerator:
    """热点选题生成器"""
    
    def __init__(self, db_path: str = "/home/nicola/.openclaw/workspace/data/hot-topics.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hot_topics (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                platform TEXT NOT NULL,
                heat_score INTEGER NOT NULL,
                trend TEXT NOT NULL,
                tags TEXT,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def fetch_weibo_hot(self) -> List[HotTopic]:
        """获取微博热搜（模拟数据）"""
        mock_topics = [
            ("AI 技术突破", 9500000, "rising", ["AI", "科技"]),
            ("职场生存指南", 8200000, "stable", ["职场", "成长"]),
            ("理财入门知识", 7100000, "rising", ["理财", "副业"]),
            ("心理健康", 6500000, "stable", ["健康", "心理"]),
            ("时间管理", 5800000, "falling", ["效率", "成长"]),
        ]
        
        return [
            HotTopic(
                id=f"weibo_{i}",
                title=title,
                platform="微博",
                heat_score=heat,
                trend=trend,
                tags=tags,
                url=f"https://s.weibo.com/weibo?q={title}",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
            )
            for i, (title, heat, trend, tags) in enumerate(mock_topics)
        ]
    
    def fetch_zhihu_hot(self) -> List[HotTopic]:
        """获取知乎热榜（模拟数据）"""
        mock_topics = [
            ("如何评价 TimesFM 时间序列模型？", 8900000, "rising", ["AI", "技术"]),
            ("普通人如何通过副业月入过万？", 7600000, "stable", ["副业", "理财"]),
            ("有哪些相见恨晚的效率工具？", 6800000, "stable", ["工具", "效率"]),
            ("2026 年值得学习的技能有哪些？", 6200000, "rising", ["学习", "成长"]),
            ("如何建立个人知识管理体系？", 5500000, "falling", ["知识管理", "学习"]),
        ]
        
        return [
            HotTopic(
                id=f"zhihu_{i}",
                title=title,
                platform="知乎",
                heat_score=heat,
                trend=trend,
                tags=tags,
                url=f"https://www.zhihu.com/question/{i}",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
            )
            for i, (title, heat, trend, tags) in enumerate(mock_topics)
        ]
    
    def fetch_xiaohongshu_hot(self) -> List[HotTopic]:
        """获取小红书热点（模拟数据）"""
        mock_topics = [
            ("AI 工具推荐", 9200000, "rising", ["AI", "工具"]),
            ("副业赚钱", 8500000, "rising", ["副业", "赚钱"]),
            ("自律生活", 7300000, "stable", ["自律", "成长"]),
            ("知识付费", 6700000, "stable", ["知识付费", "学习"]),
            ("时间管理", 5900000, "falling", ["效率", "管理"]),
        ]
        
        return [
            HotTopic(
                id=f"xhs_{i}",
                title=title,
                platform="小红书",
                heat_score=heat,
                trend=trend,
                tags=tags,
                url=f"https://www.xiaohongshu.com/search/{title}",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
            )
            for i, (title, heat, trend, tags) in enumerate(mock_topics)
        ]
    
    def save_topics(self, topics: List[HotTopic]):
        """保存热点到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for topic in topics:
            cursor.execute("""
                INSERT OR REPLACE INTO hot_topics 
                (id, title, platform, heat_score, trend, tags, url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                topic.id, topic.title, topic.platform, topic.heat_score,
                topic.trend, json.dumps(topic.tags), topic.url, topic.created_at
            ))
        
        conn.commit()
        conn.close()
    
    def get_recommendations(
        self,
        niche_tags: List[str] = None,
        limit: int = 10
    ) -> List[HotTopic]:
        """获取选题推荐"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, platform, heat_score, trend, tags, url, created_at
            FROM hot_topics
            ORDER BY heat_score DESC
            LIMIT 50
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        topics = [
            HotTopic(
                id=row[0], title=row[1], platform=row[2], heat_score=row[3],
                trend=row[4], tags=json.loads(row[5]) if row[5] else [],
                url=row[6], created_at=row[7]
            )
            for row in rows
        ]
        
        # 评分排序
        def score(topic):
            heat_score = topic.heat_score / 10000000 * 60
            trend_score = {'rising': 20, 'stable': 10, 'falling': 0}[topic.trend]
            match_score = 0
            if niche_tags:
                match_score = len(set(topic.tags) & set(niche_tags)) / len(niche_tags) * 20
            return heat_score + trend_score + match_score
        
        topics.sort(key=score, reverse=True)
        return topics[:limit]
    
    def generate_titles(self, topic: HotTopic) -> List[str]:
        """基于热点生成标题"""
        templates = [
            "如何评价 {topic}？",
            "{topic} 全攻略，看这一篇就够了",
            "普通人如何通过 {topic} 改变命运？",
            "关于 {topic}，90% 的人都不知道的事",
            "2026 年，{topic} 还值得做吗？",
            "我用 {topic} 实现了财务自由",
            "{topic} 避坑指南",
            "从 0 到 1，{topic} 实战教程",
            "为什么我劝你一定要了解 {topic}？",
            "{topic} 的 10 个真相",
        ]
        
        keywords = topic.tags[:2] if topic.tags else [topic.title[:10]]
        return [t.format(topic=keywords[0]) for t in templates]
