#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨渠道记忆关联脚本
功能：自动关联不同渠道的相似话题
渠道：Telegram/微信/飞书
"""

import os
import json
import logging
from datetime import datetime
from difflib import SequenceMatcher
import hashlib

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/cross-channel-memory.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CrossChannelMemory')

# 配置
CONFIG = {
    'memory_dir': '/home/nicola/.openclaw/workspace/memory',
    'session_dir': '/home/nicola/.openclaw/workspace/sessions',
    'similarity_threshold': 0.6,  # 60% 相似度触发关联
}

class CrossChannelMemory:
    def __init__(self):
        self.memory_dir = CONFIG['memory_dir']
        self.session_dir = CONFIG['session_dir']
        self.topics = {}  # 话题索引
        self.channel_messages = []  # 多渠道消息缓存
    
    def load_recent_memories(self, days=7):
        """加载最近 N 天的记忆"""
        memories = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            memory_file = os.path.join(self.memory_dir, f'{date}.md')
            
            if os.path.exists(memory_file):
                with open(memory_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    memories.append({
                        'date': date,
                        'file': memory_file,
                        'content': content,
                    })
        
        logger.info(f"📚 加载 {len(memories)} 天记忆")
        return memories
    
    def extract_topics(self, text):
        """提取文本中的话题关键词"""
        # 简单实现：提取中文关键词
        import re
        
        # 匹配中文关键词 (2-4 字)
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        
        # 匹配英文关键词
        keywords.extend(re.findall(r'[a-zA-Z]{3,}', text))
        
        # 去重
        keywords = list(set(keywords))
        
        return keywords[:20]  # 限制最多 20 个关键词
    
    def calculate_similarity(self, text1, text2):
        """计算两段文本的相似度"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def detect_cross_channel_topic(self, message, channel):
        """检测跨渠道话题关联"""
        logger.info(f"🔍 检测跨渠道话题：{channel}")
        
        # 提取当前消息话题
        current_topics = self.extract_topics(message)
        
        # 加载最近记忆
        memories = self.load_recent_memories(days=7)
        
        # 查找相似话题
        related_memories = []
        for memory in memories:
            memory_topics = self.extract_topics(memory['content'])
            
            # 计算话题重叠度
            overlap = set(current_topics) & set(memory_topics)
            overlap_score = len(overlap) / max(len(current_topics), 1)
            
            if overlap_score >= CONFIG['similarity_threshold']:
                related_memories.append({
                    'date': memory['date'],
                    'file': memory['file'],
                    'topics': list(overlap),
                    'score': overlap_score,
                })
        
        # 生成关联报告
        if related_memories:
            association = {
                'timestamp': datetime.now().isoformat(),
                'channel': channel,
                'message': message[:200],
                'topics': current_topics,
                'related_memories': related_memories,
            }
            
            logger.info(f"✅ 发现 {len(related_memories)} 个关联记忆")
            return association
        else:
            logger.debug("✓ 无关联记忆")
            return None
    
    def generate_association_report(self, association):
        """生成关联报告"""
        report = f"""
【跨渠道记忆关联 · {association['timestamp']}】

📱 来源渠道：{association['channel']}
💬 消息摘要：{association['message']}
🏷️ 话题标签：{', '.join(association['topics'][:10])}

📚 关联记忆 ({len(association['related_memories'])} 个):
"""
        
        for mem in association['related_memories']:
            report += f"""
- 日期：{mem['date']}
  文件：{mem['file']}
  重叠话题：{', '.join(mem['topics'][:5])}
  相似度：{mem['score']*100:.1f}%
"""
        
        report += "\n---\n太一 · 跨渠道记忆系统\n"
        
        return report
    
    def save_association(self, association):
        """保存关联记录"""
        report = self.generate_association_report(association)
        
        # 写入当日记忆文件
        today = datetime.now().strftime('%Y-%m-%d')
        memory_file = os.path.join(self.memory_dir, f'{today}.md')
        
        with open(memory_file, 'a', encoding='utf-8') as f:
            f.write("\n")
            f.write(report)
        
        logger.info(f"📝 关联记录已保存：{memory_file}")
    
    def process_message(self, message, channel):
        """处理单条消息"""
        association = self.detect_cross_channel_topic(message, channel)
        
        if association:
            self.save_association(association)
            return True
        return False
    
    def batch_process_sessions(self):
        """批量处理会话记录"""
        logger.info("🔄 开始批量处理会话记录...")
        
        # 扫描会话目录
        if not os.path.exists(self.session_dir):
            logger.warning(f"会话目录不存在：{self.session_dir}")
            return
        
        processed = 0
        for filename in os.listdir(self.session_dir):
            if filename.endswith('.json'):
                session_file = os.path.join(self.session_dir, filename)
                
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # 提取消息
                messages = session_data.get('messages', [])
                channel = session_data.get('channel', 'unknown')
                
                for msg in messages[-10:]:  # 只处理最近 10 条
                    message = msg.get('content', '')
                    if len(message) > 20:  # 忽略短消息
                        self.process_message(message, channel)
                        processed += 1
        
        logger.info(f"✅ 批量处理完成：{processed} 条消息")

def main():
    """主函数"""
    logger.info("🚀 跨渠道记忆关联启动...")
    
    memory = CrossChannelMemory()
    
    # 批量处理历史会话
    memory.batch_process_sessions()
    
    logger.info("✅ 跨渠道记忆关联初始化完成")
    
    # 持续监控模式 (可选)
    # while True:
    #     # 监控新消息...
    #     time.sleep(60)

if __name__ == '__main__':
    from datetime import timedelta
    main()
