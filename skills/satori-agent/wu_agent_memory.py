#!/usr/bin/env python3
"""
悟.Agent - 融合太一记忆宫殿系统

使用太一最新记忆 Skill (memory_system.py)
融合佛法觉悟追踪与艾宾浩斯复习机制

作者：太一 AGI
创建：2026-04-10
更新：2026-04-10 (融合太一记忆宫殿)
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 导入太一记忆宫殿系统
import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/taiyi-memory-palace')
from memory_system import TaiyiMemoryPalace

# 导入悟系统 Skill
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/wu-enlightenment')
from root_assessment import assess_by_question, get_user_profile, update_enlightenment_stage
from teaching_methods import select_method, generate_response, TEACHING_METHODS
from dharma_knowledge import get_teaching_by_name, get_teachings_by_root, get_quote_by_topic


class WuEnlightenmentAgent:
    """悟.Agent - 融合太一记忆宫殿的觉悟者 Agent"""
    
    def __init__(self):
        self.agent_id = "wu-enlightenment-agent"
        self.version = "2.0.0"  # v2.0: 融合记忆宫殿
        self.created_at = datetime.now()
        
        # 太一记忆宫殿
        self.memory_palace = TaiyiMemoryPalace()
        
        # 用户状态缓存
        self.users_cache: Dict[str, Dict] = {}
        
        # 自进化数据
        self.evolution_data = {
            "total_interactions": 0,
            "successful_breakthroughs": 0,
            "method_usage": {},
            "root_distribution": {"上": 0, "中": 0, "下": 0},
        }
        
        # 数据目录
        self.data_dir = Path(__file__).parent / "agents" / "wu"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载自进化数据
        self._load_evolution_data()
    
    async def chat(self, user_id: str, question: str) -> str:
        """
        对话主函数 - 融合记忆宫殿
        
        Args:
            user_id: 用户 ID
            question: 用户问题
        
        Returns:
            回答内容
        """
        print(f"\n🪷 悟.Agent 对话 (融合记忆宫殿)")
        print(f"   用户：{user_id}")
        print(f"   问题：'{question}'")
        print("-"*60)
        
        # 1. 获取/评估用户根器
        root_type = await self._get_root_type(user_id, question)
        print(f"   根器：{root_type}")
        
        # 2. 选择教学方法
        method = select_method(root_type, question)
        print(f"   方法：{method.name} ({method.style})")
        
        # 3. 查找相关佛法教义
        dharma_teaching = self._find_relevant_dharma(question, root_type)
        if dharma_teaching:
            print(f"   教义：{dharma_teaching.name}")
        
        # 4. 生成回答
        response = generate_response(method, question, dharma_teaching)
        
        # 5. 添加佛法语录
        quote_topic = self._select_quote_topic(question)
        quote = get_quote_by_topic(quote_topic)
        response += f"\n💬 佛法语录：\n{quote}\n"
        
        # 6. 存储到太一记忆宫殿 (融合点)
        await self._store_to_memory_palace(user_id, question, response, root_type)
        
        # 7. 更新觉悟进度
        stage = await self._update_progress(user_id, question, response, root_type)
        print(f"   觉悟阶段：{stage}")
        
        # 8. 检查是否需要复习 (艾宾浩斯机制)
        review_reminder = await self._check_review_due(user_id)
        if review_reminder:
            response += f"\n\n🔔 复习提醒：\n{review_reminder}"
        
        # 9. 更新自进化数据
        self._update_evolution_data(user_id, root_type, method.name)
        
        return response
    
    async def _store_to_memory_palace(self, user_id: str, question: str, response: str, root_type: str):
        """存储到太一记忆宫殿"""
        # 1. 存储对话到"对话记忆"房间
        dialogue_text = f"[{user_id}] {question} -> {response[:200]}"
        self.memory_palace.remember(
            text=dialogue_text,
            category="conversations",
            metadata={
                "user_id": user_id,
                "root_type": root_type,
                "type": "dialogue"
            }
        )
        
        # 2. 存储觉悟进度到"学习记忆"房间
        progress_text = f"[{user_id}] 觉悟阶段追踪"
        self.memory_palace.remember(
            text=progress_text,
            category="learning",
            metadata={
                "user_id": user_id,
                "root_type": root_type,
                "type": "progress"
            }
        )
        
        # 3. 存储关键教义到"身份记忆"房间 (重要觉悟)
        if self._is_breakthrough(question, response):
            breakthrough_text = f"[{user_id}] 觉悟突破：{question[:50]}"
            self.memory_palace.remember(
                text=breakthrough_text,
                category="identity",
                metadata={
                    "user_id": user_id,
                    "type": "breakthrough",
                    "importance": 10
                }
            )
            print(f"   ✅ 觉悟突破已存储到记忆宫殿")
        
        print(f"   ✅ 对话已存储到太一记忆宫殿")
    
    async def _check_review_due(self, user_id: str) -> Optional[str]:
        """检查是否需要复习 (艾宾浩斯机制)"""
        # 从记忆宫殿获取用户的对话记录
        user_records = self.memory_palace.search(
            query=f"[{user_id}]",
            category="learning",
            limit=5
        )
        
        if user_records and len(user_records) > 2:
            # 有学习记录，生成复习提醒
            reminder = "📚 根据艾宾浩斯遗忘曲线，建议你复习以下佛法教义：\n\n"
            for record in user_records[:3]:
                text = record.get('text', '')[:80]
                reminder += f"- {text}...\n"
            
            reminder += "\n🙏 温故而知新，可以为师矣。"
            return reminder
        
        return None
    
    async def _get_root_type(self, user_id: str, question: str) -> str:
        """获取用户根器"""
        # 先从记忆宫殿搜索用户历史
        user_history = self.memory_palace.search(
            query=f"[{user_id}]",
            category="conversations",
            limit=5
        )
        
        if user_history:
            # 有历史记录，通过对话评估
            dialogue = [{"question": h.get('text', '').split('->')[0].strip()} for h in user_history]
            from root_assessment import assess_by_dialogue
            assessment = assess_by_dialogue(dialogue)
            return assessment.root_type
        
        # 无历史记录，通过问题评估
        assessment = assess_by_question(question)
        return assessment.root_type
    
    def _find_relevant_dharma(self, question: str, root_type: str) -> Optional[dict]:
        """查找相关佛法教义"""
        keywords = {
            "心经": "心经",
            "金刚经": "金刚经",
            "四圣谛": "四圣谛",
            "八正道": "八正道",
            "禅": "禅宗",
            "念佛": "净土宗",
            "空": "心经",
            "悟": "禅宗",
            "本来面目": "禅宗",
            "修行": "八正道",
        }
        
        for keyword, teaching_name in keywords.items():
            if keyword in question:
                return get_teaching_by_name(teaching_name)
        
        if root_type == "上":
            return get_teaching_by_name("禅宗")
        elif root_type == "中":
            return get_teaching_by_name("心经")
        else:
            return get_teaching_by_name("净土宗")
    
    def _select_quote_topic(self, question: str) -> str:
        """选择佛法语录主题"""
        if "空" in question or "相" in question:
            return "emptiness"
        elif "心" in question or "佛" in question:
            return "mind"
        elif "苦" in question or "烦恼" in question:
            return "suffering"
        elif "慈悲" in question or "利他" in question:
            return "compassion"
        else:
            return "practice"
    
    async def _update_progress(self, user_id: str, question: str, response: str, root_type: str) -> str:
        """更新觉悟进度"""
        stage = update_enlightenment_stage(user_id, {
            "question": question,
            "response": response,
            "root_type": root_type,
        })
        return stage
    
    def _is_breakthrough(self, question: str, response: str) -> bool:
        """检测是否是突破时刻"""
        breakthrough_keywords = ["明白了", "懂了", "开悟", "觉悟", "即是", "本来"]
        for keyword in breakthrough_keywords:
            if keyword in question:
                return True
        return False
    
    def _update_evolution_data(self, user_id: str, root_type: str, method_name: str):
        """更新自进化数据"""
        self.evolution_data["total_interactions"] += 1
        self.evolution_data["root_distribution"][root_type] += 1
        
        if method_name not in self.evolution_data["method_usage"]:
            self.evolution_data["method_usage"][method_name] = 0
        self.evolution_data["method_usage"][method_name] += 1
        
        if self.evolution_data["total_interactions"] % 10 == 0:
            self._save_evolution_data()
    
    def _load_evolution_data(self):
        """加载自进化数据"""
        evolution_file = self.data_dir / "evolution.json"
        if evolution_file.exists():
            with open(evolution_file, "r", encoding="utf-8") as f:
                self.evolution_data = json.load(f)
    
    def _save_evolution_data(self):
        """保存自进化数据"""
        evolution_file = self.data_dir / "evolution.json"
        with open(evolution_file, "w", encoding="utf-8") as f:
            json.dump(self.evolution_data, f, ensure_ascii=False, indent=2)
    
    def get_enlightenment_progress(self, user_id: str) -> Dict:
        """获取用户觉悟进度 (从记忆宫殿)"""
        # 从记忆宫殿搜索用户所有记录
        user_records = self.memory_palace.search(
            query=f"[{user_id}]",
            limit=20
        )
        
        # 统计觉悟阶段
        stages = {"信": 0, "解": 0, "行": 0, "证": 0}
        for record in user_records:
            metadata = record.get('metadata', {})
            # 简化：根据互动次数推断阶段
            if len(user_records) < 5:
                stage = "信"
            elif len(user_records) < 20:
                stage = "解"
            elif len(user_records) < 50:
                stage = "行"
            else:
                stage = "证"
            stages[stage] += 1
        
        current_stage = max(stages, key=stages.get)
        
        return {
            "user_id": user_id,
            "enlightenment_stage": current_stage,
            "interactions": len(user_records),
            "records": user_records[:10],  # 返回前 10 条记录
        }
    
    async def proactive_guidance(self, user_id: str) -> Optional[str]:
        """主动引导 (融合记忆宫殿)"""
        # 从记忆宫殿获取用户上次互动时间
        user_records = self.memory_palace.search(
            query=f"[{user_id}]",
            limit=1
        )
        
        if user_records:
            # 简化处理：假设有记录就是近期互动
            stage = self.get_enlightenment_progress(user_id)["enlightenment_stage"]
            
            if stage == "信":
                message = "🙏 愿你保持信心，佛法如灯，照亮前行路。"
            elif stage == "解":
                message = "🙏 理解教义后，记得实践哦。知行合一，方得真谛。"
            elif stage == "行":
                message = "🙏 修行如逆水行舟，不进则退。继续精进！"
            else:
                message = "🙏 随喜你的觉悟，愿你智悲双修，利益众生。"
            
            return message
        
        return None
    
    def get_stats(self) -> Dict:
        """获取 Agent 统计"""
        # 从记忆宫殿获取统计
        memory_stats = self.memory_palace.get_statistics()
        
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "total_interactions": self.evolution_data["total_interactions"],
            "successful_breakthroughs": self.evolution_data["successful_breakthroughs"],
            "root_distribution": self.evolution_data["root_distribution"],
            "top_methods": sorted(
                self.evolution_data["method_usage"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "memory_palace_stats": memory_stats,
        }


async def main():
    """主函数 - 测试融合记忆宫殿的 Agent"""
    print("🪷 悟.Agent v2.0 - 融合太一记忆宫殿系统")
    print("="*60)
    
    agent = WuEnlightenmentAgent()
    
    # 测试对话
    test_cases = [
        ("user_memory_001", "什么是佛法？"),
        ("user_memory_002", "如何是本来面目？"),
        ("user_memory_003", "佛法好难懂，怎么办？"),
        ("user_memory_001", "我明白了，心即是佛！"),  # 二次对话
    ]
    
    for user_id, question in test_cases:
        response = await agent.chat(user_id, question)
        print(f"\n{response[:300]}...")
    
    # 测试记忆宫殿统计
    print("\n📊 记忆宫殿统计:")
    stats = agent.get_stats()
    print(f"   总互动：{stats['total_interactions']} 次")
    print(f"   记忆宫殿总记忆：{stats['memory_palace_stats']['total_memories']} 条")
    for cat, count in stats['memory_palace_stats']['by_category'].items():
        print(f"   {cat}: {count} 条")
    
    # 测试觉悟进度
    print("\n🙏 觉悟进度:")
    progress = agent.get_enlightenment_progress("user_memory_001")
    print(f"   用户：{progress['user_id']}")
    print(f"   阶段：{progress['enlightenment_stage']}")
    print(f"   互动：{progress['interactions']} 次")
    
    print("\n✅ 悟.Agent v2.0 (融合记忆宫殿) 测试完成!")
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())
