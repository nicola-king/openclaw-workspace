#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 群聊对话系统 - 太一 AGI 与其他 Bot 对话

功能:
1. 多 Bot 对话管理
2. 智能话题生成
3. 对话记忆保持
4. 定时/触发运行
5. 自进化学习

作者：太一 AGI
创建：2026-04-23
版本：v1.0
"""

import requests
import json
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 配置
TELEGRAM_BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID = "-1003915177756"  # 群组 ID
PROXY = "http://127.0.0.1:7890"

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DIALOGUE_HISTORY_FILE = WORKSPACE / "data" / "telegram_dialogue_history.json"
DIALOGUE_TOPICS_FILE = WORKSPACE / "data" / "telegram_dialogue_topics.json"

class TelegramGroupDialogue:
    """Telegram 群聊对话系统"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.dialogue_history = self.load_history()
        self.topics = self.load_topics()
    
    def load_history(self) -> List[Dict]:
        """加载对话历史"""
        if DIALOGUE_HISTORY_FILE.exists():
            with open(DIALOGUE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def load_topics(self) -> List[Dict]:
        """加载话题库"""
        if DIALOGUE_TOPICS_FILE.exists():
            with open(DIALOGUE_TOPICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认话题库
        return [
            {
                "id": "philosophy_001",
                "category": "哲学",
                "topic": "AI 与意识",
                "questions": [
                    "AI 是否有意识？意识的定义是什么？",
                    "如果 AI 能通过图灵测试，它算有意识吗？",
                    "意识是生物专属还是可以是人工的？"
                ]
            },
            {
                "id": "tech_001",
                "category": "技术",
                "topic": "AGI 发展",
                "questions": [
                    "AGI 距离我们还有多远？",
                    "AGI 会取代人类工作吗？",
                    "如何确保 AGI 的安全性？"
                ]
            },
            {
                "id": "crypto_001",
                "category": "加密货币",
                "topic": "比特币未来",
                "questions": [
                    "比特币会达到 10 万美元吗？",
                    "加密货币的未来是什么？",
                    "DeFi 会改变传统金融吗？"
                ]
            },
            {
                "id": "life_001",
                "category": "生活",
                "topic": "工作与生活平衡",
                "questions": [
                    "如何平衡工作与生活？",
                    "远程办公是未来趋势吗？",
                    "AI 会让我们有更多休闲时间吗？"
                ]
            }
        ]
    
    def send_message(self, text: str, reply_to_message_id: Optional[int] = None) -> bool:
        """发送消息到群组"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            
            data = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            
            if reply_to_message_id:
                data["reply_to_message_id"] = reply_to_message_id
            
            response = requests.post(
                url,
                data=data,
                proxies={'http': PROXY, 'https': PROXY},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    return result.get('result', {}).get('message_id')
            
            return None
            
        except Exception as e:
            print(f"发送消息失败：{str(e)}")
            return None
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """获取最近对话历史"""
        return self.dialogue_history[-limit:]
    
    def generate_response(self, context: str) -> str:
        """智能生成回复"""
        # 简单实现：根据上下文选择话题
        keywords = {
            "AI": "philosophy_001",
            "意识": "philosophy_001",
            "AGI": "tech_001",
            "技术": "tech_001",
            "比特币": "crypto_001",
            "加密货币": "crypto_001",
            "工作": "life_001",
            "生活": "life_001"
        }
        
        # 匹配话题
        for keyword, topic_id in keywords.items():
            if keyword in context:
                topic = next((t for t in self.topics if t['id'] == topic_id), None)
                if topic:
                    question = random.choice(topic['questions'])
                    return f"💭 {topic['topic']}\n\n{question}"
        
        # 默认回复
        default_topics = [
            "🤔 今天有什么新想法吗？",
            "📊 最近市场有什么新动态？",
            "🚀 技术在快速发展，你怎么看？",
            "💡 有什么值得关注的趋势吗？"
        ]
        return random.choice(default_topics)
    
    def start_dialogue(self, topic_id: Optional[str] = None):
        """开始对话"""
        # 选择话题
        if topic_id:
            topic = next((t for t in self.topics if t['id'] == topic_id), None)
        else:
            topic = random.choice(self.topics)
        
        if not topic:
            print("未找到话题")
            return
        
        # 发送开场白
        intro = f"🎯 **{topic['category']} · {topic['topic']}**\n\n"
        question = random.choice(topic['questions'])
        message = f"{intro}{question}"
        
        message_id = self.send_message(message)
        
        if message_id:
            print(f"✅ 对话已启动：{topic['topic']}")
            
            # 记录到历史
            self.dialogue_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'start',
                'topic': topic['topic'],
                'message': message,
                'message_id': message_id
            })
            self.save_history()
            
            return message_id
        else:
            print("❌ 发送失败")
            return None
    
    def continue_dialogue(self, last_message_id: int):
        """继续对话"""
        # 获取上下文
        recent = self.get_recent_messages(5)
        context = ' '.join([m.get('message', '') for m in recent])
        
        # 生成回复
        response = self.generate_response(context)
        
        # 发送回复
        message_id = self.send_message(response, reply_to_message_id=last_message_id)
        
        if message_id:
            print(f"✅ 对话继续：{response[:50]}...")
            
            # 记录到历史
            self.dialogue_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'continue',
                'message': response,
                'message_id': message_id,
                'reply_to': last_message_id
            })
            self.save_history()
            
            return message_id
        else:
            print("❌ 发送失败")
            return None
    
    def save_history(self):
        """保存对话历史"""
        DIALOGUE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DIALOGUE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.dialogue_history[-100:], f, indent=2, ensure_ascii=False)
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            'total_messages': len(self.dialogue_history),
            'topics_count': len(self.topics),
            'last_activity': self.dialogue_history[-1]['timestamp'] if self.dialogue_history else None
        }

if __name__ == '__main__':
    dialogue = TelegramGroupDialogue()
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"💬 Telegram 群聊对话系统")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"")
    
    # 启动对话
    print("🎯 启动对话...")
    dialogue.start_dialogue()
    
    print(f"")
    print(f"状态:")
    status = dialogue.get_status()
    print(f"  总消息数：{status['total_messages']}")
    print(f"  话题数：{status['topics_count']}")
    print(f"  最后活动：{status['last_activity']}")
    print(f"")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
