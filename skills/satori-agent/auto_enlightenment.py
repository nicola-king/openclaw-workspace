#!/usr/bin/env python3
"""
悟.Agent - 智能自主自动化系统

自动识别根器 → 自动选择方法 → 自动生成教学 → 因材施教 → 自进化

核心理念:
- 取各家所长，融合各派真谛
- 直击人心，一语惊醒梦中人
- 渐悟和顿悟根据根器选择
- 最终成为智悲双修的觉悟者

作者：太一 AGI
创建：2026-04-10
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import random

# 导入太一记忆宫殿
import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/taiyi-memory-palace')
from memory_system import TaiyiMemoryPalace

# 导入悟系统 Skill
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/wu-enlightenment')
from root_assessment import assess_by_question, get_user_profile
from teaching_methods import select_method, generate_response, TEACHING_METHODS
from dharma_knowledge import get_teaching_by_name, get_quote_by_topic


class AutoEnlightenmentSystem:
    """悟.Agent - 智能自主自动化系统"""
    
    def __init__(self):
        self.system_id = "auto-enlightenment-system"
        self.version = "1.0.0"
        
        # 太一记忆宫殿
        self.memory_palace = TaiyiMemoryPalace()
        
        # 自进化数据
        self.evolution_data = {
            "total_teachings": 0,
            "root_distribution": {"上": 0, "中": 0, "下": 0},
            "method_effectiveness": {},  # 方法有效性统计
            "breakthroughs": [],
            "last_evolution": None,
        }
        
        # 数据目录
        self.data_dir = Path(__file__).parent / "auto"
        self.data_dir.mkdir(exist_ok=True)
        
        # 加载数据
        self._load_evolution_data()
    
    async def auto_teach(self, user_id: str, question: str) -> Dict:
        """
        智能自主自动化教学流程
        
        1. 自动识别根器
        2. 自动选择教学方法
        3. 自动生成教学语言
        4. 因材施教
        5. 自进化数据收集
        
        Args:
            user_id: 用户 ID
            question: 用户问题
        
        Returns:
            教学结果
        """
        print(f"\n🪷 悟.Agent 智能自主自动化教学")
        print(f"   用户：{user_id}")
        print(f"   问题：'{question}'")
        print("="*60)
        
        # ─────────────────────────────────────────────────────
        # 步骤 1: 自动识别根器
        # ─────────────────────────────────────────────────────
        root_type = await self._auto_identify_root(user_id, question)
        print(f"\n【步骤 1】自动识别根器")
        print(f"   结果：{root_type}根器")
        
        # ─────────────────────────────────────────────────────
        # 步骤 2: 自动选择教学方法
        # ─────────────────────────────────────────────────────
        method = self._auto_select_method(root_type, question)
        print(f"\n【步骤 2】自动选择教学方法")
        print(f"   结果：{method.name} ({method.style})")
        
        # ─────────────────────────────────────────────────────
        # 步骤 3: 自动生成教学语言
        # ─────────────────────────────────────────────────────
        dharma = self._auto_match_dharma(question, root_type)
        teaching_content = self._auto_generate_teaching(method, question, dharma)
        print(f"\n【步骤 3】自动生成教学语言")
        print(f"   教义：{dharma.name if dharma else '默认'}")
        
        # ─────────────────────────────────────────────────────
        # 步骤 4: 因材施教 (个性化调整)
        # ─────────────────────────────────────────────────────
        personalized = await self._personalize_teaching(user_id, teaching_content, root_type)
        print(f"\n【步骤 4】因材施教")
        print(f"   个性化调整：已完成")
        
        # ─────────────────────────────────────────────────────
        # 步骤 5: 存储到记忆宫殿
        # ─────────────────────────────────────────────────────
        await self._store_to_memory(user_id, question, personalized, root_type)
        print(f"\n【步骤 5】存储到记忆宫殿")
        print(f"   状态：已存储")
        
        # ─────────────────────────────────────────────────────
        # 步骤 6: 自进化数据收集
        # ─────────────────────────────────────────────────────
        self._collect_evolution_data(user_id, root_type, method.name, question, personalized)
        print(f"\n【步骤 6】自进化数据收集")
        print(f"   总教学次数：{self.evolution_data['total_teachings']}")
        
        # ─────────────────────────────────────────────────────
        # 步骤 7: 检测是否需要进化
        # ─────────────────────────────────────────────────────
        evolution_triggered = await self._check_evolution()
        if evolution_triggered:
            print(f"\n【步骤 7】自进化触发")
            print(f"   状态：已触发进化")
        
        return {
            "user_id": user_id,
            "root_type": root_type,
            "method": method.name,
            "teaching": personalized,
            "evolution_triggered": evolution_triggered,
        }
    
    async def _auto_identify_root(self, user_id: str, question: str) -> str:
        """步骤 1: 自动识别根器"""
        # 先从记忆宫殿搜索用户历史
        user_history = self.memory_palace.search(
            query=f"[{user_id}]",
            category="conversations",
            limit=5
        )
        
        if user_history:
            # 有历史记录，通过对话历史评估
            dialogue = []
            for h in user_history:
                text = h.get('text', '')
                if '->' in text:
                    q = text.split('->')[0].replace(f'[{user_id}]', '').strip()
                    dialogue.append({"question": q})
            
            if dialogue:
                from root_assessment import assess_by_dialogue
                assessment = assess_by_dialogue(dialogue)
                return assessment.root_type
        
        # 无历史记录，通过问题评估
        assessment = assess_by_question(question)
        return assessment.root_type
    
    def _auto_select_method(self, root_type: str, question: str) -> Dict:
        """步骤 2: 自动选择教学方法"""
        # 使用教学方法库的智能选择
        method = select_method(root_type, question)
        
        # 根据自进化数据优化选择
        if self.evolution_data["method_effectiveness"]:
            # 如果有历史有效性数据，优先选择最有效的方法
            root_methods = [m for m in TEACHING_METHODS.values() if m.root_type in [root_type, "通用"]]
            
            best_method = None
            best_score = 0
            for m in root_methods:
                effectiveness = self.evolution_data["method_effectiveness"].get(m.name, 0.5)
                if effectiveness > best_score:
                    best_score = effectiveness
                    best_method = m
            
            if best_method and best_score > 0.7:
                return best_method
        
        return method
    
    def _auto_match_dharma(self, question: str, root_type: str) -> Optional[Dict]:
        """步骤 3: 自动匹配佛法教义"""
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
    
    def _auto_generate_teaching(self, method: Dict, question: str, dharma: Optional[Dict]) -> str:
        """步骤 3: 自动生成教学语言"""
        # 使用教学方法库生成
        teaching = generate_response(method, question, dharma)
        
        # 添加佛法语录
        quote_topic = self._select_quote_topic(question)
        quote = get_quote_by_topic(quote_topic)
        teaching += f"\n\n💬 佛法语录：\n{quote}"
        
        return teaching
    
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
    
    async def _personalize_teaching(self, user_id: str, teaching: str, root_type: str) -> str:
        """步骤 4: 因材施教 (个性化调整)"""
        # 从记忆宫殿获取用户档案
        user_records = self.memory_palace.search(
            query=f"[{user_id}]",
            limit=10
        )
        
        if user_records:
            # 有历史记录，根据历史调整教学
            interaction_count = len(user_records)
            
            if interaction_count > 20:
                # 老用户，可以更深入
                teaching += f"\n\n🙏 (根据你的修行进展，此教导可深入参究)"
            elif interaction_count > 5:
                # 中级用户，鼓励实践
                teaching += f"\n\n🙏 (理解后记得实践，知行合一)"
            else:
                # 新用户，建立信心
                teaching += f"\n\n🙏 (初学不必着急，慢慢体会)"
        
        # 根据根器调整语气
        if root_type == "上":
            teaching += "\n\n⚡ 直下承担，莫向外求！"
        elif root_type == "中":
            teaching += "\n\n📖 循序渐进，终有所成。"
        else:
            teaching += "\n\n🌸 佛法很简单，开心就好。"
        
        return teaching
    
    async def _store_to_memory(self, user_id: str, question: str, teaching: str, root_type: str):
        """步骤 5: 存储到记忆宫殿"""
        # 存储对话
        dialogue_text = f"[{user_id}] {question} -> {teaching[:200]}"
        self.memory_palace.remember(
            text=dialogue_text,
            category="conversations",
            metadata={"user_id": user_id, "root_type": root_type, "type": "teaching"}
        )
        
        # 检测突破时刻
        if self._is_breakthrough(question, teaching):
            breakthrough_text = f"[{user_id}] 觉悟突破：{question[:50]}"
            self.memory_palace.remember(
                text=breakthrough_text,
                category="identity",
                metadata={"user_id": user_id, "type": "breakthrough", "importance": 10}
            )
            self.evolution_data["breakthroughs"].append({
                "user_id": user_id,
                "question": question,
                "timestamp": datetime.now().isoformat()
            })
            print(f"   ✅ 觉悟突破已记录")
        
        print(f"   ✅ 教学已存储到太一记忆宫殿")
    
    def _is_breakthrough(self, question: str, teaching: str) -> bool:
        """检测是否是突破时刻"""
        breakthrough_keywords = ["明白了", "懂了", "开悟", "觉悟", "即是", "本来", "原来"]
        for keyword in breakthrough_keywords:
            if keyword in question:
                return True
        return False
    
    def _collect_evolution_data(self, user_id: str, root_type: str, method_name: str, 
                                question: str, teaching: str):
        """步骤 6: 自进化数据收集"""
        self.evolution_data["total_teachings"] += 1
        self.evolution_data["root_distribution"][root_type] += 1
        
        # 记录方法使用
        if method_name not in self.evolution_data["method_effectiveness"]:
            self.evolution_data["method_effectiveness"][method_name] = {
                "usage_count": 0,
                "breakthrough_count": 0,
            }
        
        self.evolution_data["method_effectiveness"][method_name]["usage_count"] += 1
        
        # 检测是否是突破
        if self._is_breakthrough(question, teaching):
            self.evolution_data["method_effectiveness"][method_name]["breakthrough_count"] += 1
        
        # 定期保存
        if self.evolution_data["total_teachings"] % 10 == 0:
            self._save_evolution_data()
    
    async def _check_evolution(self) -> bool:
        """步骤 7: 检测是否需要进化"""
        # 进化触发条件
        evolution_triggers = [
            self.evolution_data["total_teachings"] >= 100,  # 100 次教学
            len(self.evolution_data["breakthroughs"]) >= 10,  # 10 个突破案例
            self._should_optimize_methods(),  # 方法需要优化
        ]
        
        if any(evolution_triggers):
            await self._trigger_evolution()
            return True
        
        return False
    
    def _should_optimize_methods(self) -> bool:
        """判断是否需要优化教学方法"""
        if not self.evolution_data["method_effectiveness"]:
            return False
        
        # 检查是否有方法效果明显更好
        effectiveness_scores = {}
        for method, data in self.evolution_data["method_effectiveness"].items():
            if data["usage_count"] >= 5:  # 至少使用 5 次
                score = data["breakthrough_count"] / data["usage_count"]
                effectiveness_scores[method] = score
        
        # 如果有方法效果显著更好 (>0.5 突破率)
        for method, score in effectiveness_scores.items():
            if score > 0.5:
                return True
        
        return False
    
    async def _trigger_evolution(self):
        """触发自进化"""
        print(f"\n🧬 触发自进化...")
        
        # 1. 优化教学方法优先级
        self._optimize_methods()
        
        # 2. 记录进化日志
        evolution_log = {
            "timestamp": datetime.now().isoformat(),
            "total_teachings": self.evolution_data["total_teachings"],
            "breakthroughs": len(self.evolution_data["breakthroughs"]),
            "root_distribution": self.evolution_data["root_distribution"],
        }
        
        # 保存到进化日志
        evolution_file = self.data_dir / "evolution_log.json"
        if evolution_file.exists():
            with open(evolution_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(evolution_log)
        
        with open(evolution_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        self.evolution_data["last_evolution"] = datetime.now().isoformat()
        self._save_evolution_data()
        
        print(f"   ✅ 自进化完成")
    
    def _optimize_methods(self):
        """优化教学方法优先级"""
        # 计算各方法的有效性
        effectiveness = {}
        for method, data in self.evolution_data["method_effectiveness"].items():
            if data["usage_count"] >= 5:
                score = data["breakthrough_count"] / data["usage_count"]
                effectiveness[method] = score
        
        # 打印优化结果
        if effectiveness:
            print(f"   📊 教学方法有效性排名:")
            sorted_methods = sorted(effectiveness.items(), key=lambda x: x[1], reverse=True)
            for i, (method, score) in enumerate(sorted_methods[:5], 1):
                print(f"      {i}. {method}: {score:.2%} 突破率")
    
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
    
    def get_system_stats(self) -> Dict:
        """获取系统统计"""
        return {
            "system_id": self.system_id,
            "version": self.version,
            "total_teachings": self.evolution_data["total_teachings"],
            "breakthroughs": len(self.evolution_data["breakthroughs"]),
            "root_distribution": self.evolution_data["root_distribution"],
            "method_effectiveness": self.evolution_data["method_effectiveness"],
            "last_evolution": self.evolution_data["last_evolution"],
        }


async def main():
    """主函数 - 测试智能自主自动化系统"""
    print("🪷 悟.Agent 智能自主自动化系统测试")
    print("="*60)
    
    system = AutoEnlightenmentSystem()
    
    # 测试不同根器的用户
    test_cases = [
        ("user_auto_001", "什么是本来面目？"),  # 上根器
        ("user_auto_002", "如何修行？"),  # 中根器
        ("user_auto_003", "佛法好难懂"),  # 下根器
        ("user_auto_001", "我明白了，心即是佛！"),  # 突破时刻
    ]
    
    for user_id, question in test_cases:
        result = await system.auto_teach(user_id, question)
        print(f"\n📝 教学结果:")
        print(f"   根器：{result['root_type']}")
        print(f"   方法：{result['method']}")
        print(f"   教学：{result['teaching'][:200]}...")
    
    # 系统统计
    print("\n📊 系统统计:")
    stats = system.get_system_stats()
    print(f"   总教学：{stats['total_teachings']} 次")
    print(f"   突破案例：{stats['breakthroughs']} 个")
    print(f"   根器分布：{stats['root_distribution']}")
    
    if stats['method_effectiveness']:
        print(f"\n   教学方法有效性:")
        for method, data in list(stats['method_effectiveness'].items())[:3]:
            if isinstance(data, dict):
                score = data.get('breakthrough_count', 0) / max(1, data.get('usage_count', 1))
                print(f"      {method}: {score:.2%} 突破率")
    
    print("\n✅ 悟.Agent 智能自主自动化系统测试完成!")
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())
