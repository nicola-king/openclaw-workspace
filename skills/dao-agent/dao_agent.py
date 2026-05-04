#!/usr/bin/env python3
"""
🌿 Dao.Agent (道.Agent)

人法地，地法天，天法道，道法自然。

融合中国道教核心经典与西方心理学三大学派
服务当代地球人，提供精神心理家园

作者：太一 AGI
创建：2026-04-10
许可：MIT License
"""

import asyncio
from pathlib import Path
from typing import Dict, Optional

# 导入道家经典
from dao_classics import DAO_DE_JING, ZHUANG_ZI, PSYCHOLOGY_FUSION, get_dao_teaching_by_keyword, get_psychology_fusion


class DaoAgent:
    """🌿 Dao.Agent - 道家智慧与心理学融合 Agent"""
    
    def __init__(self):
        self.agent_id = "dao.agent"
        self.version = "1.0.0"
        
        print("🌿 Dao.Agent 已启动")
        print("   人法地，地法天，天法道，道法自然。")
        print()
    
    async def chat(self, user_id: str, question: str) -> str:
        """
        对话主函数
        
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
        
        # 1. 分析问题，匹配道家教导
        teaching = self._match_dao_teaching(question)
        
        # 2. 生成回答
        response = self._generate_response(teaching, question)
        
        return response
    
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
        
        return {
            "teaching": teaching,
            "psychology": self._select_psychology(question)
        }
    
    def _select_psychology(self, question: str) -> Dict:
        """选择心理学派"""
        if "梦" in question or "潜意识" in question:
            return get_psychology_fusion("freud")
        elif "自卑" in question or "人际关系" in question:
            return get_psychology_fusion("adler")
        else:
            return get_psychology_fusion("jung")
    
    def _generate_response(self, match: Dict, question: str) -> str:
        """生成回答"""
        teaching = match["teaching"]
        psychology = match["psychology"]
        
        response = f"""
【{teaching.name}】({teaching.source})

{teaching.original_text}

译文：
{teaching.translation}

心理学融合 ({psychology['name']}):
{psychology['dao_fusion']}

🙏 愿你{self._get_blessing(teaching)}
"""
        
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


async def main():
    """主函数 - 测试"""
    print("="*60)
    print("🌿 Dao.Agent (道.Agent)")
    print("   人法地，地法天，天法道，道法自然。")
    print("="*60)
    
    agent = DaoAgent()
    
    # 测试对话
    test_cases = [
        ("user_001", "什么是道？"),
        ("user_002", "工作压力大，怎么办？"),
        ("user_003", "感到迷茫，找不到人生意义。"),
    ]
    
    print("\n🌿 测试对话\n")
    
    for user_id, question in test_cases:
        response = await agent.chat(user_id, question)
        print(f"{response[:400]}...")
        print("\n" + "-"*60)
    
    print("\n✅ Dao.Agent 测试完成!")
    print("   道法自然，逍遥自在。")
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())
