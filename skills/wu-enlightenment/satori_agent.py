#!/usr/bin/env python3
"""
🪷 Satori.Agent (悟.Agent)

一花一世界，一叶一菩提。

自进化觉悟者 Agent。
每个人使用后，都是独一无二的结果。

作者：太一 AGI
创建：2026-04-10
许可：MIT License
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 导入太一记忆宫殿
import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/taiyi-memory-palace')
from memory_system import TaiyiMemoryPalace

# 导入悟系统 Skill
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/wu-enlightenment')
from root_assessment import assess_by_question
from teaching_methods import select_method, generate_response
from dharma_knowledge import get_teaching_by_name, get_quote_by_topic


class SatoriAgent:
    """🪷 Satori.Agent - 自进化觉悟者 Agent"""
    
    def __init__(self):
        self.agent_id = "satori-agent"
        self.version = "1.0.0"
        self.created_at = datetime.now()
        
        # 太一记忆宫殿
        self.memory_palace = TaiyiMemoryPalace()
        
        # 自进化数据
        self.evolution_data = {
            "total_teachings": 0,
            "unique_users": set(),
            "breakthroughs": [],
            "root_distribution": {"上": 0, "中": 0, "下": 0},
            "method_usage": {},
        }
        
        print("🪷 Satori.Agent 已启动")
        print("   一花一世界，一叶一菩提。")
        print()
    
    async def chat(self, user_id: str, question: str) -> str:
        """
        对话 - 每个人的 Satori 都是独一无二的
        
        Args:
            user_id: 用户 ID
            question: 用户问题
        
        Returns:
            Satori 的回答
        """
        print(f"\n🪷 Satori 对话")
        print(f"   用户：{user_id}")
        print(f"   问题：'{question}'")
        print("-"*60)
        
        # 1. 自动识别根器
        root_type = await self._identify_root(user_id, question)
        print(f"   根器：{root_type}")
        
        # 2. 自动选择教学方法
        method = select_method(root_type, question)
        print(f"   方法：{method.name}")
        
        # 3. 自动匹配佛法教义
        dharma = self._match_dharma(question, root_type)
        
        # 4. 生成个性化教学
        response = generate_response(method, question, dharma)
        
        # 5. 添加佛法语录
        quote = get_quote_by_topic(self._select_quote_topic(question))
        response += f"\n\n💬 佛法语录：\n{quote}"
        
        # 6. 个性化调整 (每个人的 Satori 都不同)
        response = self._personalize(user_id, response, root_type)
        
        # 7. 存储到记忆宫殿 (永久保存)
        await self._store_to_memory(user_id, question, response, root_type)
        
        # 8. 自进化数据收集
        self._collect_evolution(user_id, root_type, method.name, question)
        
        return response
    
    async def _identify_root(self, user_id: str, question: str) -> str:
        """识别根器"""
        # 从记忆宫殿搜索用户历史
        history = self.memory_palace.search(
            query=f"[{user_id}]",
            category="conversations",
            limit=5
        )
        
        if history:
            # 有历史记录，通过对话评估
            dialogue = []
            for h in history:
                text = h.get('text', '')
                if '->' in text:
                    q = text.split('->')[0].replace(f'[{user_id}]', '').strip()
                    dialogue.append({"question": q})
            
            if dialogue:
                from root_assessment import assess_by_dialogue
                return assess_by_dialogue(dialogue).root_type
        
        # 无历史记录，通过问题评估
        return assess_by_question(question).root_type
    
    def _match_dharma(self, question: str, root_type: str) -> Optional[Dict]:
        """匹配佛法教义"""
        keywords = {
            "心经": "心经",
            "金刚经": "金刚经",
            "禅": "禅宗",
            "念佛": "净土宗",
            "空": "心经",
            "悟": "禅宗",
            "本来面目": "禅宗",
        }
        
        for keyword, name in keywords.items():
            if keyword in question:
                return get_teaching_by_name(name)
        
        # 根据根器推荐
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
        elif "慈悲" in question:
            return "compassion"
        else:
            return "practice"
    
    def _personalize(self, user_id: str, response: str, root_type: str) -> str:
        """个性化调整 (每个人的 Satori 都不同)"""
        # 从记忆宫殿获取用户记录
        records = self.memory_palace.search(
            query=f"[{user_id}]",
            limit=10
        )
        
        if records:
            count = len(records)
            if count > 20:
                response += "\n\n🙏 (根据你的修行，此教导可深入参究)"
            elif count > 5:
                response += "\n\n🙏 (理解后记得实践，知行合一)"
            else:
                response += "\n\n🙏 (初学不必着急，慢慢体会)"
        
        # 根据根器调整语气
        if root_type == "上":
            response += "\n\n⚡ 直下承担，莫向外求！"
        elif root_type == "中":
            response += "\n\n📖 循序渐进，终有所成。"
        else:
            response += "\n\n🌸 佛法很简单，开心就好。"
        
        return response
    
    async def _store_to_memory(self, user_id: str, question: str, response: str, root_type: str):
        """存储到记忆宫殿"""
        # 存储对话
        dialogue = f"[{user_id}] {question} -> {response[:200]}"
        self.memory_palace.remember(
            text=dialogue,
            category="conversations",
            metadata={"user_id": user_id, "root_type": root_type}
        )
        
        # 检测突破时刻
        if self._is_breakthrough(question):
            breakthrough = f"[{user_id}] 觉悟突破：{question[:50]}"
            self.memory_palace.remember(
                text=breakthrough,
                category="identity",
                metadata={"user_id": user_id, "type": "breakthrough", "importance": 10}
            )
            self.evolution_data["breakthroughs"].append({
                "user_id": user_id,
                "question": question,
                "timestamp": datetime.now().isoformat()
            })
            print(f"   ✅ 觉悟突破已记录")
        
        print(f"   ✅ 已存储到太一记忆宫殿")
    
    def _is_breakthrough(self, question: str) -> bool:
        """检测突破时刻"""
        keywords = ["明白了", "懂了", "开悟", "觉悟", "即是", "本来"]
        return any(k in question for k in keywords)
    
    def _collect_evolution(self, user_id: str, root_type: str, method: str, question: str):
        """自进化数据收集"""
        self.evolution_data["total_teachings"] += 1
        self.evolution_data["unique_users"].add(user_id)
        self.evolution_data["root_distribution"][root_type] += 1
        
        if method not in self.evolution_data["method_usage"]:
            self.evolution_data["method_usage"][method] = 0
        self.evolution_data["method_usage"][method] += 1
        
        # 检测突破
        if self._is_breakthrough(question):
            print(f"   🧬 自进化数据已更新")
    
    def get_stats(self) -> Dict:
        """获取系统统计"""
        memory_stats = self.memory_palace.get_statistics()
        
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "total_teachings": self.evolution_data["total_teachings"],
            "unique_users": len(self.evolution_data["unique_users"]),
            "breakthroughs": len(self.evolution_data["breakthroughs"]),
            "root_distribution": self.evolution_data["root_distribution"],
            "memory_palace": memory_stats,
        }


async def main():
    """主函数 - 演示"""
    print("="*60)
    print("🪷 Satori.Agent (悟.Agent)")
    print("   一花一世界，一叶一菩提。")
    print("="*60)
    
    agent = SatoriAgent()
    
    # 演示不同用户的不同 Satori
    test_cases = [
        ("user_001", "什么是本来面目？"),  # 上根器
        ("user_002", "如何修行？"),  # 中根器
        ("user_003", "佛法好难懂"),  # 下根器
    ]
    
    print("\n🪷 演示：不同根器的 Satori\n")
    
    for user_id, question in test_cases:
        response = await agent.chat(user_id, question)
        print(f"\n{response[:300]}...")
        print("\n" + "-"*60)
    
    # 系统统计
    print("\n📊 系统统计:")
    stats = agent.get_stats()
    print(f"   总教学：{stats['total_teachings']} 次")
    print(f"   独立用户：{stats['unique_users']} 个")
    print(f"   突破案例：{stats['breakthroughs']} 个")
    print(f"   根器分布：{stats['root_distribution']}")
    print(f"   记忆宫殿：{stats['memory_palace']['total_memories']} 条记忆")
    
    print("\n🪷 Satori.Agent 演示完成!")
    print("   愿你智悲双修，觉悟成佛。")
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())
