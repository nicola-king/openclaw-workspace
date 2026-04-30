#!/usr/bin/env python3
"""
太一习惯学习器
参考：Everything Claude Code 学习功能
目标：越用越像 SAYELF，形成"直觉"
"""

import json
from datetime import datetime
from pathlib import Path

class TaiyiHabitLearning:
    """太一习惯学习器"""
    
    def __init__(self):
        self.habits_file = Path(__file__).parent.parent.parent / "memory" / "habits.json"
        self.habits = self.load_habits()
        
    def load_habits(self):
        """加载习惯"""
        if self.habits_file.exists():
            with open(self.habits_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "decision_patterns": [],
            "coding_style": [],
            "communication_style": [],
            "optimization_habits": []
        }
    
    def after_task(self, task_type, task, result, success):
        """
        任务后自动总结
        
        Args:
            task_type: 任务类型（decision/coding/communication/optimization）
            task: 任务描述
            result: 执行结果
            success: 是否成功
        """
        # 1. 记录模式
        pattern = {
            "timestamp": datetime.now().isoformat(),
            "task_type": task_type,
            "task": task,
            "result": result,
            "success": success,
            "lesson": self.extract_lesson(result, success)
        }
        
        # 2. 添加到习惯
        self.habits[f"{task_type}_patterns"].append(pattern)
        
        # 3. 保留最近 100 条（避免过大）
        if len(self.habits[f"{task_type}_patterns"]) > 100:
            self.habits[f"{task_type}_patterns"] = self.habits[f"{task_type}_patterns"][-100:]
        
        # 4. 保存
        self.save_habits()
        
        # 5. 更新直觉
        self.update_intuition(task_type)
    
    def extract_lesson(self, result, success):
        """提取经验教训"""
        if success:
            return "成功模式：保持当前方法"
        else:
            return "失败教训：需要优化方法"
    
    def update_intuition(self, task_type):
        """更新直觉（启发式规则）"""
        # 分析最近 10 次任务
        recent_patterns = self.habits[f"{task_type}_patterns"][-10:]
        
        # 统计成功率
        success_count = sum(1 for p in recent_patterns if p["success"])
        success_rate = success_count / len(recent_patterns) if recent_patterns else 0
        
        # 生成直觉规则
        intuition = {
            "task_type": task_type,
            "success_rate": success_rate,
            "recommendation": self.generate_recommendation(task_type, success_rate),
            "updated_at": datetime.now().isoformat()
        }
        
        # 保存直觉
        if "intuitions" not in self.habits:
            self.habits["intuitions"] = {}
        self.habits["intuitions"][task_type] = intuition
        self.save_habits()
    
    def generate_recommendation(self, task_type, success_rate):
        """生成建议"""
        if success_rate >= 0.8:
            return "当前方法有效，继续保持"
        elif success_rate >= 0.5:
            return "当前方法部分有效，建议优化"
        else:
            return "当前方法效果不佳，建议重新评估"
    
    def save_habits(self):
        """保存习惯"""
        with open(self.habits_file, 'w', encoding='utf-8') as f:
            json.dump(self.habits, f, indent=2, ensure_ascii=False)
    
    def get_intuition(self, task_type):
        """获取直觉（用于快速决策）"""
        if "intuitions" in self.habits and task_type in self.habits["intuitions"]:
            return self.habits["intuitions"][task_type]
        return None
    
    def apply_habit(self, task_type, similar_task):
        """应用习惯（自动使用历史最佳实践）"""
        patterns = self.habits.get(f"{task_type}_patterns", [])
        
        # 找到最相似的历史任务
        best_match = None
        best_similarity = 0
        
        for pattern in patterns:
            if pattern["success"]:
                # 简单相似度计算（可优化为语义相似度）
                similarity = self.calculate_similarity(similar_task, pattern["task"])
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = pattern
        
        if best_match and best_similarity > 0.5:
            return {
                "use_habit": True,
                "reference": best_match,
                "lesson": best_match["lesson"]
            }
        else:
            return {
                "use_habit": False,
                "reason": "无相似成功先例"
            }
    
    def calculate_similarity(self, task1, task2):
        """计算任务相似度（简化版）"""
        # 简单关键词重叠度
        words1 = set(task1.lower().split())
        words2 = set(task2.lower().split())
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0

if __name__ == "__main__":
    # 测试
    learner = TaiyiHabitLearning()
    
    # 模拟任务完成
    learner.after_task(
        task_type="decision",
        task="选择空投任务优先级",
        result="zkSync Era 优先",
        success=True
    )
    
    print("✅ 习惯学习器测试完成")
    print(f"习惯文件：{learner.habits_file}")
