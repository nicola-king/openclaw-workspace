#!/usr/bin/env python3
"""
悟.Agent - 自进化觉悟者 Agent

融合各派真谛，根据根器选择方法
直击人心，一语惊醒梦中人
渐悟和顿悟根据不同根器选择
最终成为智悲双修的觉悟者

作者：太一 AGI
创建：2026-04-10
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 导入 Skill 模块
from root_assessment import assess_by_question, get_user_profile, update_enlightenment_stage
from teaching_methods import select_method, generate_response, TEACHING_METHODS
from dharma_knowledge import get_teaching_by_name, get_teachings_by_root, get_quote_by_topic


class WuEnlightenmentAgent:
    """悟.Agent - 自进化觉悟者 Agent"""
    
    def __init__(self):
        self.agent_id = "wu-enlightenment-agent"
        self.version = "1.0.0"
        self.created_at = datetime.now()
        
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
        self.data_dir.mkdir(parents=True, exist_ok=True)  # parents=True 确保创建所有父目录
        
        # 加载自进化数据
        self._load_evolution_data()
    
    async def chat(self, user_id: str, question: str) -> str:
        """
        对话主函数
        
        Args:
            user_id: 用户 ID
            question: 用户问题
        
        Returns:
            回答内容
        """
        print(f"\n🪷 悟.Agent 对话")
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
        
        # 6. 更新觉悟进度
        stage = await self._update_progress(user_id, question, response, root_type)
        print(f"   觉悟阶段：{stage}")
        
        # 7. 更新自进化数据
        self._update_evolution_data(user_id, root_type, method.name)
        
        # 8. 保存到记忆系统
        await self._save_to_memory(user_id, question, response, root_type, stage)
        
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
    
    def _find_relevant_dharma(self, question: str, root_type: str) -> Optional[dict]:
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
            "本来面目": "禅宗",
            "修行": "八正道",
        }
        
        for keyword, teaching_name in keywords.items():
            if keyword in question:
                return get_teaching_by_name(teaching_name)
        
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
    
    async def _save_to_memory(self, user_id: str, question: str, response: str, root_type: str, stage: str):
        """保存到记忆系统"""
        user_file = self.data_dir / "users" / f"{user_id}.json"
        user_file.parent.mkdir(exist_ok=True)
        
        # 加载或创建用户档案
        if user_file.exists():
            with open(user_file, "r", encoding="utf-8") as f:
                user_data = json.load(f)
        else:
            user_data = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "root_type": root_type,
                "enlightenment_stage": stage,
                "interactions": 0,
                "dialogue_history": [],
                "breakthroughs": [],
            }
        
        # 更新数据
        user_data["interactions"] += 1
        user_data["root_type"] = root_type
        user_data["enlightenment_stage"] = stage
        user_data["dialogue_history"].append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "response": response[:500],  # 只保存前 500 字
        })
        
        # 检测突破时刻
        if self._is_breakthrough(question, response, stage):
            user_data["breakthroughs"].append({
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "stage": stage,
            })
            self.evolution_data["successful_breakthroughs"] += 1
        
        # 保存
        with open(user_file, "w", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
    
    def _is_breakthrough(self, question: str, response: str, stage: str) -> bool:
        """检测是否是突破时刻"""
        # 简单判断：从"信"到"解"，或从"解"到"行"
        if stage in ["解", "行", "证"]:
            return True
        
        # 或者问题显示深度理解
        breakthrough_keywords = ["明白了", "懂了", "开悟", "觉悟"]
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
        
        # 定期保存
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
        """获取用户觉悟进度"""
        user_file = self.data_dir / "users" / f"{user_id}.json"
        if user_file.exists():
            with open(user_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    async def proactive_guidance(self, user_id: str) -> Optional[str]:
        """主动引导 (定期关怀)"""
        user_data = self.get_enlightenment_progress(user_id)
        if not user_data:
            return None
        
        # 检查上次互动时间
        last_interaction = user_data.get("dialogue_history", [])[-1]
        if last_interaction:
            last_time = datetime.fromisoformat(last_interaction["timestamp"])
            days_since = (datetime.now() - last_time).days
            
            if days_since >= 3:  # 3 天未对话
                stage = user_data.get("enlightenment_stage", "信")
                
                # 根据阶段发送不同开示
                if stage == "信":
                    message = "🙏 愿你保持信心，佛法如灯，照亮前行路。"
                elif stage == "解":
                    message = "🙏 理解教义后，记得实践哦。知行合一，方得真谛。"
                elif stage == "行":
                    message = "🙏 修行如逆水行舟，不进则退。继续精进！"
                else:
                    message = "🙏 随喜你的觉悟，愿你智悲双修，利益众生。"
                
                # 保存到记忆
                await self._save_to_memory(
                    user_id,
                    "[主动关怀]",
                    message,
                    user_data.get("root_type", "中"),
                    stage
                )
                
                return message
        
        return None
    
    def get_stats(self) -> Dict:
        """获取 Agent 统计"""
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
        }


async def main():
    """主函数 - 测试 Agent"""
    print("🪷 悟.Agent - 自进化觉悟者 Agent 测试")
    print("="*60)
    
    agent = WuEnlightenmentAgent()
    
    # 测试对话
    test_cases = [
        ("user_001", "什么是佛法？"),
        ("user_002", "如何是本来面目？"),
        ("user_003", "佛法好难懂，怎么办？"),
        ("user_004", "念佛的是谁？"),
        ("user_001", "我明白了，心即是佛！"),  # 二次对话
    ]
    
    for user_id, question in test_cases:
        response = await agent.chat(user_id, question)
        print(f"\n{response[:300]}...")
    
    # 测试统计
    print("\n📊 Agent 统计:")
    stats = agent.get_stats()
    print(f"   总互动：{stats['total_interactions']} 次")
    print(f"   突破案例：{stats['successful_breakthroughs']} 个")
    print(f"   根器分布：{stats['root_distribution']}")
    print(f"   热门方法：{stats['top_methods']}")
    
    # 测试主动引导
    print("\n🙏 主动引导测试:")
    guidance = await agent.proactive_guidance("user_001")
    if guidance:
        print(f"   {guidance}")
    else:
        print("   暂无需引导")
    
    print("\n✅ 悟.Agent 测试完成!")
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())
