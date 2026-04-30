#!/usr/bin/env python3
# scripts/test-skill-dehydrate.py
# 用途：测试技能卸载机制

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

STATE_FILE = Path("/tmp/skill-dehydrate-test-state.json")

class SkillDehydrateTest:
    """技能卸载机制测试"""
    
    def __init__(self):
        self.loaded_skills = {}
        self.context_tokens = 0
        self.context_limit = 131000  # 131K
        self.test_results = []
    
    def load_skill(self, name, tokens, priority=2):
        """模拟加载技能"""
        self.loaded_skills[name] = {
            "name": name,
            "tokens": tokens,
            "priority": priority,
            "loaded_at": datetime.now(),
            "last_used": datetime.now(),
            "use_count": 0
        }
        self.context_tokens += tokens
        print(f"📦 加载技能：{name} ({tokens} tokens)")
    
    def use_skill(self, name):
        """模拟使用技能"""
        if name in self.loaded_skills:
            self.loaded_skills[name]["last_used"] = datetime.now()
            self.loaded_skills[name]["use_count"] += 1
            print(f"🔧 使用技能：{name} (使用次数：{self.loaded_skills[name]['use_count']})")
    
    def dehydrate_lru(self):
        """LRU 策略：卸载最少使用的技能"""
        if not self.loaded_skills:
            return None
        
        # 找到最少使用的技能
        least_used = min(self.loaded_skills.items(), 
                        key=lambda x: x[1]["use_count"])
        
        skill_name = least_used[0]
        skill_info = least_used[1]
        
        self.context_tokens -= skill_info["tokens"]
        del self.loaded_skills[skill_name]
        
        print(f"💨 LRU 卸载：{skill_name} (使用 {skill_info['use_count']} 次，{skill_info['tokens']} tokens)")
        return skill_name
    
    def dehydrate_fifo(self):
        """FIFO 策略：卸载最早加载的技能"""
        if not self.loaded_skills:
            return None
        
        # 找到最早加载的技能
        earliest = min(self.loaded_skills.items(),
                      key=lambda x: x[1]["loaded_at"])
        
        skill_name = earliest[0]
        skill_info = earliest[1]
        
        self.context_tokens -= skill_info["tokens"]
        del self.loaded_skills[skill_name]
        
        print(f"💨 FIFO 卸载：{skill_name} (加载于 {skill_info['loaded_at'].strftime('%H:%M:%S')})")
        return skill_name
    
    def dehydrate_priority(self, target_priority=3):
        """Priority 策略：卸载低优先级技能"""
        # 找到最低优先级的技能
        low_priority = [
            (name, info) for name, info in self.loaded_skills.items()
            if info["priority"] == target_priority
        ]
        
        if not low_priority:
            print(f"⚠️  无优先级 {target_priority} 的技能可卸载")
            return None
        
        # 卸载第一个
        skill_name, skill_info = low_priority[0]
        self.context_tokens -= skill_info["tokens"]
        del self.loaded_skills[skill_name]
        
        print(f"💨 Priority 卸载：{skill_name} (优先级 {skill_info['priority']})")
        return skill_name
    
    def check_context_threshold(self):
        """检查上下文阈值"""
        usage = self.context_tokens / self.context_limit * 100
        
        if usage > 90:
            print(f"🚨 上下文占用：{usage:.1f}% (>90% 触发 FIFO)")
            return "fifo"
        elif usage > 80:
            print(f"⚠️  上下文占用：{usage:.1f}% (>80% 触发 LRU)")
            return "lru"
        else:
            print(f"✅ 上下文占用：{usage:.1f}% (正常)")
            return None
    
    def get_status(self):
        """获取当前状态"""
        return {
            "loaded_skills": len(self.loaded_skills),
            "context_tokens": self.context_tokens,
            "context_limit": self.context_limit,
            "usage_pct": round(self.context_tokens / self.context_limit * 100, 2)
        }


def run_test():
    """运行测试"""
    print("=" * 60)
    print("技能卸载机制测试")
    print("=" * 60)
    print()
    
    test = SkillDehydrateTest()
    
    # 测试场景 1: 加载多个技能
    print("[场景 1] 加载多个技能")
    print("-" * 40)
    test.load_skill("browser-automation", 5000, priority=2)
    test.load_skill("zhiji-e-strategy", 8000, priority=1)
    test.load_skill("gmgn-swap", 3000, priority=1)
    test.load_skill("qiaomu-card", 6000, priority=3)
    test.load_skill("feishu-doc", 5000, priority=2)
    print()
    
    # 测试场景 2: 使用部分技能
    print("[场景 2] 使用部分技能 (模拟 LRU 测试)")
    print("-" * 40)
    test.use_skill("browser-automation")
    test.use_skill("browser-automation")
    test.use_skill("zhiji-e-strategy")
    test.use_skill("gmgn-swap")
    test.use_skill("gmgn-swap")
    test.use_skill("gmgn-swap")
    # qiaomu-card 和 feishu-doc 未使用
    print()
    
    # 测试场景 3: LRU 卸载
    print("[场景 3] LRU 策略卸载 (最少使用)")
    print("-" * 40)
    test.dehydrate_lru()  # 应该卸载 feishu-doc (0 次使用)
    test.dehydrate_lru()  # 应该卸载 qiaomu-card (0 次使用)
    print()
    
    # 测试场景 4: 重置 + FIFO 测试
    print("[场景 4] FIFO 策略卸载 (最早加载)")
    print("-" * 40)
    test2 = SkillDehydrateTest()
    test2.load_skill("skill-A", 5000)
    import time
    time.sleep(0.1)
    test2.load_skill("skill-B", 5000)
    time.sleep(0.1)
    test2.load_skill("skill-C", 5000)
    test2.dehydrate_fifo()  # 应该卸载 skill-A
    test2.dehydrate_fifo()  # 应该卸载 skill-B
    print()
    
    # 测试场景 5: Priority 策略
    print("[场景 5] Priority 策略卸载 (低优先级优先)")
    print("-" * 40)
    test3 = SkillDehydrateTest()
    test3.load_skill("core-strategy", 8000, priority=1)
    test3.load_skill("browser-auto", 5000, priority=2)
    test3.load_skill("qiaomu-card", 6000, priority=3)
    test3.load_skill("social-share", 4000, priority=3)
    test3.dehydrate_priority(3)  # 卸载优先级 3
    test3.dehydrate_priority(3)  # 卸载另一个优先级 3
    test3.dehydrate_priority(3)  # 无更多优先级 3
    print()
    
    # 测试场景 6: 上下文阈值触发
    print("[场景 6] 上下文阈值触发")
    print("-" * 40)
    test4 = SkillDehydrateTest()
    # 加载到 >80%
    for i in range(20):
        test4.load_skill(f"skill-{i}", 6000, priority=2)
    test4.check_context_threshold()
    print()
    
    # 最终状态
    print("[最终状态]")
    print("-" * 40)
    status = test.get_status()
    print(f"  加载技能数：{status['loaded_skills']}")
    print(f"  上下文占用：{status['context_tokens']} / {status['context_limit']} ({status['usage_pct']}%)")
    print()
    
    print("=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    run_test()
