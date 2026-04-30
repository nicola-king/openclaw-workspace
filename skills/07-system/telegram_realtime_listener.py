#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 实时@监听服务 - 后台常驻

功能:
1. 实时监听群消息
2. 检测@太一 AGI 消息
3. 立即响应@消息
4. 结合随机对话

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
OFFSET_FILE = Path("/tmp/telegram_offset.txt")
LAST_ACTIVITY_FILE = Path("/tmp/telegram_last_activity.json")
DIALOGUE_HISTORY_FILE = WORKSPACE / "data" / "telegram_dialogue_history.json"
BOT_EVOLUTION_FILE = WORKSPACE / "data" / "bot_evolution_levels.json"
DIALOGUE_TOPICS_FILE = WORKSPACE / "data" / "telegram_dialogue_topics.json"

class TelegramRealtimeListener:
    """Telegram 实时@监听服务"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.offset = self.load_offset()
        self.last_activity = self.load_last_activity()
        self.bot_evolution = self.load_bot_evolution()
        self.topics = self.load_topics()
        self.running = True
    
    def load_offset(self) -> int:
        """加载 offset"""
        if OFFSET_FILE.exists():
            with open(OFFSET_FILE, 'r') as f:
                return int(f.read().strip())
        return 0
    
    def save_offset(self, offset: int):
        """保存 offset"""
        with open(OFFSET_FILE, 'w') as f:
            f.write(str(offset))
    
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
    
    def load_bot_evolution(self) -> Dict[str, int]:
        """加载 Bot 进化程度"""
        if BOT_EVOLUTION_FILE.exists():
            with open(BOT_EVOLUTION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "太一 AGI": 97, "Hermes": 90, "知几": 85,
            "山木": 82, "素问": 80, "庖丁": 78, "罔两": 75
        }
    
    def load_topics(self) -> List[Dict]:
        """加载话题库"""
        if DIALOGUE_TOPICS_FILE.exists():
            with open(DIALOGUE_TOPICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        
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
    
    def get_updates(self, timeout: int = 30) -> List[Dict]:
        """获取更新"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
            
            params = {
                "offset": self.offset + 1,
                "timeout": timeout,
                "allowed_updates": ["message"]
            }
            
            response = requests.get(
                url,
                params=params,
                proxies={'http': PROXY, 'https': PROXY},
                timeout=timeout + 5
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    updates = result.get('result', [])
                    if updates:
                        self.offset = updates[-1].get('update_id', self.offset)
                        self.save_offset(self.offset)
                    return updates
            
            return []
            
        except Exception as e:
            print(f"获取更新失败：{str(e)}")
            return []
    
    def send_message(self, text: str, reply_to_message_id: Optional[int] = None) -> Optional[int]:
        """发送消息"""
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
    
    def is_mentioned(self, message: Dict) -> bool:
        """检查是否@太一 AGI"""
        text = message.get('text', '')
        
        # 检查@sayelfbot
        if '@sayelfbot' in text:
            return True
        
        # 检查@太一
        if '@太一' in text or '太一' in text:
            return True
        
        return False
    
    def get_bot_persona(self, bot_name: str) -> str:
        """获取 Bot 人设"""
        evolution = self.bot_evolution.get(bot_name, 50)
        
        if evolution >= 90:
            return "深度思考者"
        elif evolution >= 80:
            return "积极讨论者"
        elif evolution >= 70:
            return "普通参与者"
        else:
            return "初学者"
    
    def generate_response(self, context: str) -> str:
        """生成回复"""
        # 随机选择话题
        topic = random.choice(self.topics)
        question = random.choice(topic['questions'])
        
        return f"💭 **{topic['topic']}**\n\n{question}"
    
    def process_message(self, message: Dict):
        """处理消息"""
        if not self.is_mentioned(message):
            return
        
        # 提取信息
        from_user = message.get('from', {})
        from_name = from_user.get('first_name', 'Unknown')
        text = message.get('text', '')
        message_id = message.get('message_id')
        chat_id = message.get('chat', {}).get('id')
        
        # 检查是否是群组消息
        if chat_id != int(self.chat_id):
            return
        
        print(f"📣 检测到@消息：{from_name} - {text[:50]}...")
        
        # 生成回复
        response = self.generate_response(text)
        full_response = f"@{from_name} {response}"
        
        # 发送回复
        reply_id = self.send_message(full_response, reply_to_message_id=message_id)
        
        if reply_id:
            print(f"✅ 已回复@{from_name}")
            
            # 记录历史
            self.append_history({
                'timestamp': datetime.now().isoformat(),
                'type': 'mention_reply',
                'bot': '太一 AGI',
                'from': from_name,
                'original_message': text,
                'response': full_response,
                'message_id': reply_id,
                'reply_to': message_id,
                'trigger': 'mention'
            })
            
            # 更新活动
            self.last_activity['last_mention_time'] = datetime.now().isoformat()
            self.last_activity['last_message_time'] = datetime.now().isoformat()
            self.last_activity['messages_today'] += 1
            self.save_last_activity()
            
            # 延迟后发起随机对话
            time.sleep(random.uniform(30, 90))
            self.start_random_dialogue(reply_id)
    
    def start_random_dialogue(self, reply_to_id: Optional[int] = None):
        """开始随机对话"""
        # 检查间隔
        last_time = self.last_activity.get('last_message_time')
        if last_time:
            last = datetime.fromisoformat(last_time)
            hours_since = (datetime.now() - last).total_seconds() / 3600
            if hours_since < 2:
                print("⏸️ 间隔太短，跳过随机对话")
                return
        
        # 随机选择话题
        topic = random.choice(self.topics)
        question = random.choice(topic['questions'])
        
        intro = f"🎯 **{topic['category']} · {topic['topic']}**\n\n{question}"
        
        message_id = self.send_message(intro, reply_to_message_id=reply_to_id)
        
        if message_id:
            print(f"✅ 随机对话已启动：{topic['topic']}")
            
            self.append_history({
                'timestamp': datetime.now().isoformat(),
                'type': 'random_dialogue',
                'bot': '太一 AGI',
                'topic': topic['topic'],
                'message': intro,
                'message_id': message_id,
                'trigger': 'mention_followup'
            })
            
            self.last_activity['last_message_time'] = datetime.now().isoformat()
            self.last_activity['messages_today'] += 1
            self.save_last_activity()
            
            # 模拟其他 Bot 回复
            time.sleep(random.uniform(60, 120))
            self.simulate_bot_responses(message_id, topic['topic'])
    
    def simulate_bot_responses(self, reply_to_id: int, topic: str):
        """模拟其他 Bot 回复"""
        bots = list(self.bot_evolution.keys())
        bots.remove('太一 AGI')
        participating_bots = random.sample(bots, random.randint(1, 3))
        
        for bot_name in participating_bots:
            evolution = self.bot_evolution.get(bot_name, 50)
            persona = self.get_bot_persona(bot_name)
            
            responses = [
                f"🤖 **{bot_name}** ({persona})\n\n💡 关于{topic}，我认为...",
                f"🤖 **{bot_name}** ({persona})\n\n🤔 {topic}这个话题很有意思...",
                f"🤖 **{bot_name}** ({persona})\n\n📊 从我的角度看{topic}..."
            ]
            
            response = random.choice(responses)
            message_id = self.send_message(response, reply_to_message_id=reply_to_id)
            
            if message_id:
                print(f"  🤖 {bot_name} 参与讨论")
                
                self.append_history({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'bot_response',
                    'bot': bot_name,
                    'message': response,
                    'message_id': message_id,
                    'reply_to': reply_to_id,
                    'trigger': 'simulation'
                })
            
            time.sleep(random.uniform(30, 90))
        
        self.append_history_to_file()
    
    def append_history(self, entry: Dict):
        """添加到历史 (内存)"""
        if not hasattr(self, 'history_buffer'):
            self.history_buffer = []
        self.history_buffer.append(entry)
    
    def append_history_to_file(self):
        """保存到文件"""
        if hasattr(self, 'history_buffer') and self.history_buffer:
            history = self.load_history()
            history.extend(self.history_buffer)
            self.save_history(history[-200:])
            self.history_buffer = []
    
    def load_history(self) -> List[Dict]:
        """加载历史"""
        if DIALOGUE_HISTORY_FILE.exists():
            with open(DIALOGUE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self, history: List[Dict]):
        """保存历史"""
        DIALOGUE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DIALOGUE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def save_last_activity(self):
        """保存最后活动"""
        with open(LAST_ACTIVITY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.last_activity, f, indent=2, ensure_ascii=False)
    
    def run(self):
        """运行监听服务"""
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📡 Telegram 实时@监听服务启动")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"群组 ID: {self.chat_id}")
        print(f"Offset: {self.offset}")
        print(f"")
        
        while self.running:
            try:
                updates = self.get_updates(timeout=30)
                
                for update in updates:
                    message = update.get('message', {})
                    if message:
                        self.process_message(message)
                
            except KeyboardInterrupt:
                print("\n⏸️ 监听服务停止")
                self.running = False
                break
            except Exception as e:
                print(f"错误：{str(e)}")
                time.sleep(5)
        
        # 保存剩余历史
        self.append_history_to_file()

if __name__ == '__main__':
    listener = TelegramRealtimeListener()
    listener.run()
