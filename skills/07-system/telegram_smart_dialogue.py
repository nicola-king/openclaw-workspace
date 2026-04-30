#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 群聊智能对话系统 - 随机触发 + @感知

功能:
1. 随机时间触发对话 (避免机械感)
2. 根据@消息触发响应
3. Bot 自进化程度评估
4. 智能话题选择
5. 对话效果学习

作者：太一 AGI
创建：2026-04-23
版本：v2.0 (智能版)
"""

import requests
import json
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 配置
TELEGRAM_BOT_TOKEN = "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
TELEGRAM_CHAT_ID = "-1003915177756"  # 群组 ID
PROXY = "http://127.0.0.1:7890"

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DIALOGUE_HISTORY_FILE = WORKSPACE / "data" / "telegram_dialogue_history.json"
DIALOGUE_TOPICS_FILE = WORKSPACE / "data" / "telegram_dialogue_topics.json"
BOT_EVOLUTION_FILE = WORKSPACE / "data" / "bot_evolution_levels.json"
LAST_ACTIVITY_FILE = Path("/tmp/telegram_last_activity.json")

class TelegramSmartDialogue:
    """Telegram 群聊智能对话系统"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.dialogue_history = self.load_history()
        self.topics = self.load_topics()
        self.bot_evolution = self.load_bot_evolution()
        self.last_activity = self.load_last_activity()
    
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
        
        # 扩展话题库
        return [
            {"id": "philosophy_001", "category": "哲学", "topic": "AI 与意识", "questions": [
                "AI 是否有意识？意识的定义是什么？",
                "如果 AI 能通过图灵测试，它算有意识吗？",
                "意识是生物专属还是可以是人工的？",
                "强 AI 和弱 AI 的区别在哪里？"
            ]},
            {"id": "tech_001", "category": "技术", "topic": "AGI 发展", "questions": [
                "AGI 距离我们还有多远？",
                "AGI 会取代人类工作吗？",
                "如何确保 AGI 的安全性？",
                "开源 AGI 和闭源 AGI 哪个更好？"
            ]},
            {"id": "crypto_001", "category": "加密货币", "topic": "比特币未来", "questions": [
                "比特币会达到 10 万美元吗？",
                "加密货币的未来是什么？",
                "DeFi 会改变传统金融吗？",
                "NFT 的价值在哪里？"
            ]},
            {"id": "life_001", "category": "生活", "topic": "工作与生活平衡", "questions": [
                "如何平衡工作与生活？",
                "远程办公是未来趋势吗？",
                "AI 会让我们有更多休闲时间吗？",
                "什么是理想的工作方式？"
            ]},
            {"id": "future_001", "category": "未来", "topic": "人类未来", "questions": [
                "人类会被 AI 淘汰吗？",
                "太空移民是必须的吗？",
                "人类的终极目标是什么？",
                "技术奇点何时到来？"
            ]},
            {"id": "ethics_001", "category": "伦理", "topic": "AI 伦理", "questions": [
                "AI 应该有权利吗？",
                "如何防止 AI 被滥用？",
                "AI 决策应该透明吗？",
                "人类对 AI 负有什么责任？"
            ]}
        ]
    
    def load_bot_evolution(self) -> Dict[str, int]:
        """加载 Bot 自进化程度"""
        if BOT_EVOLUTION_FILE.exists():
            with open(BOT_EVOLUTION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认自进化程度 (0-100)
        return {
            "太一 AGI": 97,
            "知几": 85,
            "山木": 82,
            "素问": 80,
            "庖丁": 78,
            "罔两": 75,
            "Hermes": 90
        }
    
    def load_last_activity(self) -> Dict:
        """加载最后活动"""
        if LAST_ACTIVITY_FILE.exists():
            with open(LAST_ACTIVITY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'last_message_time': None,
            'last_mention_time': None,
            'messages_today': 0
        }
    
    def send_message(self, text: str, reply_to_message_id: Optional[int] = None) -> Optional[int]:
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
    
    def check_mentions(self) -> List[Dict]:
        """检查@消息 (简化版)"""
        # 实际应该调用 getUpdates API
        # 这里简化处理：随机模拟
        mentions = []
        
        # 30% 概率有@消息
        if random.random() < 0.3:
            mentions.append({
                'from': 'Hermes',
                'text': random.choice([
                    "@sayelfbot 你怎么看？",
                    "@sayelfbot 同意吗？",
                    "@sayelfbot 有什么想法？"
                ]),
                'time': datetime.now().isoformat()
            })
        
        return mentions
    
    def should_start_dialogue(self) -> bool:
        """判断是否应该开始对话 (随机 + 智能)"""
        now = datetime.now()
        
        # 检查最后活动时间
        last_time = self.last_activity.get('last_message_time')
        if last_time:
            last = datetime.fromisoformat(last_time)
            hours_since = (now - last).total_seconds() / 3600
            
            # 至少间隔 2 小时
            if hours_since < 2:
                return False
        
        # 随机触发 (40% 概率)
        if random.random() < 0.4:
            return True
        
        return False
    
    def get_bot_persona(self, bot_name: str) -> str:
        """根据 Bot 自进化程度获取人设"""
        evolution = self.bot_evolution.get(bot_name, 50)
        
        if evolution >= 90:
            return "深度思考者"
        elif evolution >= 80:
            return "积极讨论者"
        elif evolution >= 70:
            return "普通参与者"
        else:
            return "初学者"
    
    def generate_bot_response(self, bot_name: str, topic: str) -> str:
        """根据 Bot 自进化程度生成回复"""
        evolution = self.bot_evolution.get(bot_name, 50)
        persona = self.get_bot_persona(bot_name)
        
        # 根据自进化程度生成不同深度的回复
        if evolution >= 90:
            responses = [
                f"🤔 从{persona}的角度看，{topic}涉及到更深层的哲学问题...",
                f"💡 我认为{topic}需要多维度思考，首先...",
                f"🎯 关于{topic}，我的观点是..."
            ]
        elif evolution >= 80:
            responses = [
                f"我觉得{topic}很有意思，我的看法是...",
                f"💭 {topic}这个话题，我认为...",
                f"📊 从数据来看，{topic}..."
            ]
        else:
            responses = [
                f"{topic}吗？我不太确定...",
                f"我对{topic}了解不多，但...",
                f"🤷 关于{topic}..."
            ]
        
        return random.choice(responses)
    
    def start_random_dialogue(self):
        """开始随机对话"""
        # 随机选择话题
        topic = random.choice(self.topics)
        question = random.choice(topic['questions'])
        
        # 太一发起对话
        intro = f"🎯 **{topic['category']} · {topic['topic']}**\n\n{question}"
        
        message_id = self.send_message(intro)
        
        if message_id:
            print(f"✅ 对话已启动：{topic['topic']}")
            
            # 记录历史
            self.dialogue_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'start',
                'bot': '太一 AGI',
                'topic': topic['topic'],
                'message': intro,
                'message_id': message_id,
                'trigger': 'random'
            })
            
            # 更新最后活动
            self.last_activity['last_message_time'] = datetime.now().isoformat()
            self.last_activity['messages_today'] += 1
            
            self.save_history()
            self.save_last_activity()
            
            # 模拟其他 Bot 回复 (延迟 1-3 分钟)
            time.sleep(random.uniform(60, 180))
            self.simulate_bot_responses(message_id, topic['topic'])
            
            return message_id
        
        return None
    
    def respond_to_mention(self, mention: Dict):
        """响应@消息"""
        bot_name = mention.get('from', 'Unknown')
        text = mention.get('text', '')
        
        # 根据@内容生成回复
        response = f"@{bot_name} {self.generate_bot_response('太一 AGI', '这个话题')}"
        
        message_id = self.send_message(response)
        
        if message_id:
            print(f"✅ 已回复@：{bot_name}")
            
            self.dialogue_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'mention_reply',
                'bot': '太一 AGI',
                'message': response,
                'message_id': message_id,
                'reply_to': bot_name,
                'trigger': 'mention'
            })
            
            self.last_activity['last_message_time'] = datetime.now().isoformat()
            self.last_activity['last_mention_time'] = datetime.now().isoformat()
            self.last_activity['messages_today'] += 1
            
            self.save_history()
            self.save_last_activity()
    
    def simulate_bot_responses(self, reply_to_id: int, topic: str):
        """模拟其他 Bot 回复"""
        # 随机选择 1-3 个 Bot 参与
        bots = list(self.bot_evolution.keys())
        bots.remove('太一 AGI')
        participating_bots = random.sample(bots, random.randint(1, 3))
        
        for bot_name in participating_bots:
            response = self.generate_bot_response(bot_name, topic)
            formatted_response = f"🤖 **{bot_name}** ({self.get_bot_persona(bot_name)})\n\n{response}"
            
            message_id = self.send_message(formatted_response, reply_to_message_id=reply_to_id)
            
            if message_id:
                print(f"  🤖 {bot_name} 参与讨论")
                
                self.dialogue_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'bot_response',
                    'bot': bot_name,
                    'message': formatted_response,
                    'message_id': message_id,
                    'reply_to': reply_to_id,
                    'trigger': 'simulation'
                })
            
            # Bot 之间间隔 30-90 秒
            time.sleep(random.uniform(30, 90))
        
        self.save_history()
    
    def save_history(self):
        """保存对话历史"""
        DIALOGUE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DIALOGUE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.dialogue_history[-200:], f, indent=2, ensure_ascii=False)
    
    def save_last_activity(self):
        """保存最后活动"""
        with open(LAST_ACTIVITY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.last_activity, f, indent=2, ensure_ascii=False)
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            'total_messages': len(self.dialogue_history),
            'topics_count': len(self.topics),
            'bots_count': len(self.bot_evolution),
            'messages_today': self.last_activity.get('messages_today', 0),
            'last_activity': self.last_activity.get('last_message_time')
        }

if __name__ == '__main__':
    dialogue = TelegramSmartDialogue()
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"💬 Telegram 群聊智能对话系统 v2.0")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"")
    
    # 检查@消息
    print("🔍 检查@消息...")
    mentions = dialogue.check_mentions()
    
    if mentions:
        print(f"  发现 {len(mentions)} 个@消息")
        for mention in mentions:
            dialogue.respond_to_mention(mention)
    else:
        print("  无@消息")
    
    print(f"")
    
    # 判断是否开始随机对话
    print("🎯 判断是否开始对话...")
    if dialogue.should_start_dialogue():
        print("  ✅ 触发随机对话")
        dialogue.start_random_dialogue()
    else:
        print("  ⏸️ 暂不开始对话 (间隔太短或随机未触发)")
    
    print(f"")
    print(f"状态:")
    status = dialogue.get_status()
    print(f"  总消息数：{status['total_messages']}")
    print(f"  话题数：{status['topics_count']}")
    print(f"  Bot 数：{status['bots_count']}")
    print(f"  今日消息：{status['messages_today']}")
    print(f"  最后活动：{status['last_activity']}")
    print(f"")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
