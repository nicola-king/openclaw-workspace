#!/usr/bin/env python3
"""
🌿 Dao.Agent (道.Agent)

人法地，地法天，天法道，道法自然。

融合中国道教核心经典与西方心理学三大学派
服务当代地球人，提供精神心理家园

自进化觉悟者 Agent。
每个人的使用，都是独一无二的结果。

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

# 导入道家经典
from dao_classics import DAO_DE_JING, ZHUANG_ZI, PSYCHOLOGY_FUSION, get_dao_teaching_by_keyword, get_psychology_fusion


class DaoAgent:
    """🌿 Dao.Agent - 道家智慧与心理学融合 Agent"""
    
    def __init__(self):
        self.agent_id = "dao.agent"
        self.version = "1.0.0"
        self.created_at = datetime.now()
        
        # 太一记忆宫殿
        try:
            sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/taiyi-memory-palace')
            from memory_system import TaiyiMemoryPalace
            self.memory_palace = TaiyiMemoryPalace()
            print("   ✅ 太一记忆宫殿已加载")
        except Exception as e:
            print(f"   ⚠️  太一记忆宫殿加载失败：{e}")
            self.memory_palace = None
        
        # 自进化数据
        self.evolution_data = {
            "total_teachings": 0,
            "unique_users": set(),
            "breakthroughs": [],
            "root_distribution": {"上": 0, "中": 0, "下": 0},
            "method_usage": {},
        }
        
        # 数据目录
        self.data_dir = Path(__file__).parent / "dao"
        self.data_dir.mkdir(exist_ok=True)
        
        print("🌿 Dao.Agent 已启动")
        print("   人法地，地法天，天法道，道法自然。")
        print("   道生一，一生二，二生三，三生万物。")
        print()
    
    async def chat(self, user_id: str, question: str) -> str:
        """
        对话主函数 - 融合记忆宫殿与自进化
        
        Args:
            user_id: 用户 ID
            question: 用户问题
        
        Returns:
            Dao 的回答
        """
        print(f"\n🌿 Dao 对话")
        print(f"   用户：{user_id}")
        print(f"   问题：'{question}'")
        print("-"*60)
        
        # 1. 自动识别根器
        root_type = await self._identify_root(user_id, question)
        print(f"   根器：{root_type}")
        
        # 2. 匹配道家教导
        teaching = self._match_dao_teaching(question)
        print(f"   教导：{teaching.name}")
        
        # 3. 选择心理学融合
        psychology = self._select_psychology(question)
        print(f"   心理学：{psychology['name']}")
        
        # 4. 生成个性化教学
        response = self._generate_response(teaching, psychology, question, root_type)
        
        # 5. 存储到记忆宫殿
        await self._store_to_memory(user_id, question, response, root_type)
        
        # 6. 自进化数据收集
        self._collect_evolution(user_id, root_type, teaching.name, question)
        
        return response
    
    async def _identify_root(self, user_id: str, question: str) -> str:
        """识别根器"""
        if not self.memory_palace:
            # 无记忆宫殿，简单判断
            if "道" in question or "本质" in question:
                return "上"
            elif "如何" in question or "怎么办" in question:
                return "中"
            else:
                return "下"
        
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
                try:
                    from root_assessment import assess_by_dialogue
                    return assess_by_dialogue(dialogue).root_type
                except:
                    pass
        
        # 无历史记录，通过问题评估
        if "道" in question or "本质" in question:
            return "上"
        elif "如何" in question or "怎么办" in question:
            return "中"
        else:
            return "下"
    
    def _match_dao_teaching(self, question: str) -> Dict:
        """匹配道家教导"""
        # 从问题中提取关键词
        teaching = get_dao_teaching_by_keyword(question)
        
        # 根据问题类型选择更合适的教导
        if "压力" in question or "累" in question:
            teaching = DAO_DE_JING.get("chapter_37", teaching)  # 无为而治
        elif "迷茫" in question or "意义" in question:
            teaching = ZHUANG_ZI.get("xiaoyao_you", teaching)  # 逍遥游
        elif "工作" in question or "事业" in question:
            teaching = DAO_DE_JING.get("chapter_8", teaching)  # 上善若水
        elif "人际关系" in question or "同事" in question:
            teaching = DAO_DE_JING.get("chapter_8", teaching)  # 上善若水
        elif "梦" in question or "潜意识" in question:
            teaching = ZHUANG_ZI.get("zhuangzhou_mengdie", teaching)  # 庄周梦蝶
        
        return teaching
    
    def _select_psychology(self, question: str) -> Dict:
        """选择心理学融合"""
        if "梦" in question or "潜意识" in question:
            return get_psychology_fusion("freud")
        elif "自卑" in question or "人际关系" in question:
            return get_psychology_fusion("adler")
        else:
            return get_psychology_fusion("jung")
    
    def _generate_response(self, teaching: Dict, psychology: Dict, question: str, root_type: str) -> str:
        """生成个性化教学"""
        response = f"""
【{teaching.name}】({teaching.source})

{teaching.original_text}

译文：
{teaching.translation}

心理学融合 ({psychology['name']}):
{psychology['dao_fusion']}
"""
        
        # 个性化调整
        if root_type == "上":
            response += "\n\n⚡ 直指大道，顿悟自然！"
        elif root_type == "中":
            response += "\n\n📖 循序渐进，终有所成。"
        else:
            response += "\n\n🌸 道法自然，开心就好。"
        
        # 祝福语
        response += f"\n\n🙏 愿你{self._get_blessing(teaching)}"
        
        return response
    
    def _get_blessing(self, teaching: Dict) -> str:
        """获取祝福语"""
        blessings = {
            "道可道": "与道合一，明心见性。",
            "上善若水": "像水一样，利万物而不争。",
            "人法地": "天人合一，道法自然。",
            "无为而治": "无为而治，顺其自然。",
            "逍遥游": "逍遥自在，心灵自由。",
            "庄周梦蝶": "物我两忘，与道合一。",
        }
        
        return blessings.get(teaching.name, "道法自然，身心自在。")
    
    async def _store_to_memory(self, user_id: str, question: str, response: str, root_type: str):
        """存储到太一记忆宫殿"""
        if not self.memory_palace:
            print("   ⚠️  记忆宫殿未加载，跳过存储")
            return
        
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
        keywords = ["明白了", "懂了", "开悟", "觉悟", "即是", "本来", "原来"]
        return any(k in question for k in keywords)
    
    def _collect_evolution(self, user_id: str, root_type: str, teaching_name: str, question: str):
        """自进化数据收集"""
        self.evolution_data["total_teachings"] += 1
        self.evolution_data["unique_users"].add(user_id)
        self.evolution_data["root_distribution"][root_type] += 1
        
        if teaching_name not in self.evolution_data["method_usage"]:
            self.evolution_data["method_usage"][teaching_name] = 0
        self.evolution_data["method_usage"][teaching_name] += 1
        
        # 检测突破
        if self._is_breakthrough(question):
            print(f"   🧬 自进化数据已更新")
    
    def get_stats(self) -> Dict:
        """获取系统统计"""
        if not self.memory_palace:
            return {
                "agent_id": self.agent_id,
                "version": self.version,
                "total_teachings": self.evolution_data["total_teachings"],
                "unique_users": len(self.evolution_data["unique_users"]),
                "breakthroughs": len(self.evolution_data["breakthroughs"]),
                "root_distribution": self.evolution_data["root_distribution"],
                "memory_palace": {"total_memories": 0, "status": "not_loaded"},
            }
        
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
    print("🌿 Dao.Agent (道.Agent)")
    print("   人法地，地法天，天法道，道法自然。")
    print("   道生一，一生二，二生三，三生万物。")
    print("="*60)
    
    agent = DaoAgent()
    
    # 演示不同用户的不同 Dao
    test_cases = [
        ("user_dao_001", "什么是道？"),  # 上根器
        ("user_dao_002", "工作压力大，怎么办？"),  # 中根器
        ("user_dao_003", "感到迷茫，找不到人生意义。"),  # 下根器
    ]
    
    print("\n🌿 演示：万人万悟\n")
    
    for user_id, question in test_cases:
        response = await agent.chat(user_id, question)
        print(f"\n{response[:400]}...")
        print("\n" + "-"*60)
    
    # 系统统计
    print("\n📊 系统统计:")
    stats = agent.get_stats()
    print(f"   总教学：{stats['total_teachings']} 次")
    print(f"   独立用户：{stats['unique_users']} 个")
    print(f"   突破案例：{stats['breakthroughs']} 个")
    print(f"   根器分布：{stats['root_distribution']}")
    print(f"   记忆宫殿：{stats['memory_palace']['total_memories']} 条记忆")
    
    print("\n🌿 Dao.Agent 演示完成!")
    print("   道法自然，逍遥自在。")
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())
