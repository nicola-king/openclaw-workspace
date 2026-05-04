#!/usr/bin/env python3
"""
悟 - 对话系统

融合各派真谛，根据根器选择方法
直击人心，一语惊醒梦中人

作者：太一 AGI
创建：2026-04-10
"""

import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/wu-enlightenment')

from root_assessment import assess_by_question, get_user_profile, update_enlightenment_stage
from teaching_methods import select_method, generate_response
from dharma_knowledge import get_teaching_by_name, get_teachings_by_root, get_quote_by_topic


class WuChat:
    """悟 - 对话系统"""
    
    def __init__(self):
        self.users = {}  # 用户状态缓存
    
    async def chat(self, user_id: str, question: str) -> str:
        """
        对话主函数
        
        Args:
            user_id: 用户 ID
            question: 用户问题
        
        Returns:
            回答内容
        """
        # 1. 获取/评估用户根器
        root_type = await self._get_root_type(user_id, question)
        
        # 2. 选择教学方法
        method = select_method(root_type, question)
        
        # 3. 查找相关佛法教义
        dharma_teaching = self._find_relevant_dharma(question)
        
        # 4. 生成回答
        response = generate_response(method, question, dharma_teaching)
        
        # 5. 更新觉悟进度
        await self._update_progress(user_id, question, response)
        
        return response
    
    async def _get_root_type(self, user_id: str, question: str) -> str:
        """获取用户根器"""
        # 先尝试从档案获取
        profile = get_user_profile(user_id)
        if profile.get("root_type"):
            return profile["root_type"]
        
        # 否则通过问题评估
        assessment = assess_by_question(question)
        return assessment.root_type
    
    def _find_relevant_dharma(self, question: str) -> dict:
        """查找相关佛法教义"""
        # 关键词匹配
        keywords = {
            "心经": "心经",
            "金刚经": "金刚经",
            "四圣谛": "四圣谛",
            "八正道": "八正道",
            "禅": "禅宗",
            "念佛": "净土宗",
            "空": "心经",
            "悟": "禅宗",
        }
        
        for keyword, teaching_name in keywords.items():
            if keyword in question:
                return get_teaching_by_name(teaching_name)
        
        # 默认返回心经
        return get_teaching_by_name("心经")
    
    async def _update_progress(self, user_id: str, question: str, response: str):
        """更新觉悟进度"""
        stage = update_enlightenment_stage(user_id, {
            "question": question,
            "response": response,
        })
        print(f"   [觉悟阶段：{stage}]")


async def main():
    """主函数 - 测试对话"""
    print("🪷 悟 - 对话系统测试")
    print("="*60)
    
    wu = WuChat()
    
    # 测试对话
    test_cases = [
        ("user_001", "什么是佛法？"),
        ("user_002", "如何是本来面目？"),
        ("user_003", "佛法好难懂，怎么办？"),
        ("user_004", "念佛的是谁？"),
    ]
    
    for user_id, question in test_cases:
        print(f"\n🙋 用户:{user_id} 问:'{question}'")
        print("-"*60)
        
        response = await wu.chat(user_id, question)
        print(response)
    
    print("\n✅ 悟 - 对话系统测试完成!")
    
    return 0


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
