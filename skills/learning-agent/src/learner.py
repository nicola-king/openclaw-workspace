#!/usr/bin/env python3
"""
Learning Agent - 强化学习智能体 v1.0
太一 AGI · 2026-04-15

Q-learning 强化学习优化调度策略
"""

import os
import json
import random
import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import numpy as np

class QLearningAgent:
    """Q-learning 强化学习智能体"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.config_path = self.workspace_root / "skills" / "learning-agent" / "config" / "learning-config.json"
        self.model_path = self.workspace_root / "skills" / "learning-agent" / "models" / "q-table.pkl"
        self.training_log_path = self.workspace_root / "skills" / "learning-agent" / "models" / "training-log.json"
        
        # 超参数
        self.config = {
            "learning_rate": 0.1,
            "discount_factor": 0.9,
            "exploration_rate": 0.1,
            "exploration_decay": 0.995,
            "min_exploration": 0.01,
            "replay_buffer_size": 1000,
            "batch_size": 32,
            "training_frequency": 100,
        }
        
        # 加载配置
        self._load_config()
        
        # Q-table: state -> action -> value
        self.q_table = {}
        
        # 经验回放缓冲区
        self.replay_buffer = []
        
        # 训练统计
        self.training_stats = {
            "episodes": 0,
            "total_reward": 0.0,
            "average_reward": 0.0,
            "best_reward": -float("inf"),
        }
        
        # 加载模型
        self._load_model()
    
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text(encoding="utf-8"))
                self.config.update(config_data)
            except:
                pass
    
    def _load_model(self):
        """加载模型"""
        if self.model_path.exists():
            try:
                with open(self.model_path, "rb") as f:
                    data = pickle.load(f)
                    self.q_table = data.get("q_table", {})
                    self.training_stats = data.get("training_stats", self.training_stats)
                print(f"✅ 加载模型：{len(self.q_table)} 个状态")
            except:
                print("⚠️  模型加载失败，使用空模型")
    
    def _save_model(self):
        """保存模型"""
        self.model_path.parent.mkdir(exist_ok=True)
        data = {
            "q_table": self.q_table,
            "training_stats": self.training_stats,
            "saved_at": datetime.now().isoformat(),
        }
        with open(self.model_path, "wb") as f:
            pickle.dump(data, f)
        print(f"💾 模型已保存：{len(self.q_table)} 个状态")
    
    def discretize_state(self, state: Dict) -> Tuple:
        """离散化状态"""
        # 将连续状态转换为离散元组
        progress = state.get("progress", 0.0)
        hour = state.get("hour", 12)
        resource = state.get("resource", 0.5)
        success = state.get("success", 0)
        frequency = state.get("frequency", 1)
        
        # 离散化
        progress_bin = min(int(progress * 10), 20)  # 0-20
        hour_bin = hour // 2  # 0-11
        resource_bin = min(int(resource * 10), 10)  # 0-10
        success_bin = min(success, 10)  # 0-10
        frequency_bin = min(frequency, 12)  # 0-12
        
        return (progress_bin, hour_bin, resource_bin, success_bin, frequency_bin)
    
    def get_action(self, state: Dict, training: bool = False) -> Dict:
        """获取动作 (ε-greedy 策略)"""
        state_key = self.discretize_state(state)
        
        # 探索 vs 利用
        if training and random.random() < self.config["exploration_rate"]:
            # 探索：随机动作
            action = self._random_action()
        else:
            # 利用：最优动作
            if state_key not in self.q_table:
                action = self._random_action()
            else:
                q_values = self.q_table[state_key]
                best_action = max(q_values.items(), key=lambda x: x[1])[0]
                action = self._decode_action(best_action)
        
        return action
    
    def _random_action(self) -> Dict:
        """生成随机动作"""
        return {
            "interval": random.choice([1800, 3600, 7200]),  # 30min/1h/2h
            "concurrent": random.choice([1, 2, 3]),
            "memory": random.choice(["256MB", "512MB", "1GB"]),
        }
    
    def _encode_action(self, action: Dict) -> int:
        """编码动作为整数"""
        interval_map = {1800: 0, 3600: 1, 7200: 2}
        concurrent_map = {1: 0, 2: 1, 3: 2}
        memory_map = {"256MB": 0, "512MB": 1, "1GB": 2}
        
        return (
            interval_map.get(action["interval"], 1) * 9 +
            concurrent_map.get(action["concurrent"], 1) * 3 +
            memory_map.get(action["memory"], 1)
        )
    
    def _decode_action(self, action_code: int) -> Dict:
        """解码整数为动作"""
        interval_map = {0: 1800, 1: 3600, 2: 7200}
        concurrent_map = {0: 1, 1: 2, 2: 3}
        memory_map = {0: "256MB", 1: "512MB", 2: "1GB"}
        
        interval = action_code // 9
        concurrent = (action_code % 9) // 3
        memory = action_code % 3
        
        return {
            "interval": interval_map.get(interval, 3600),
            "concurrent": concurrent_map.get(concurrent, 2),
            "memory": memory_map.get(memory, "512MB"),
        }
    
    def update_q_value(self, state: Dict, action: Dict, reward: float, next_state: Dict):
        """更新 Q 值"""
        state_key = self.discretize_state(state)
        next_state_key = self.discretize_state(next_state)
        action_code = self._encode_action(action)
        
        # 初始化 Q 值
        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in range(27)}  # 3*3*3=27 种动作
        
        # Q-learning 更新公式
        current_q = self.q_table[state_key].get(action_code, 0.0)
        
        if next_state_key in self.q_table:
            max_next_q = max(self.q_table[next_state_key].values())
        else:
            max_next_q = 0.0
        
        new_q = current_q + self.config["learning_rate"] * (
            reward + self.config["discount_factor"] * max_next_q - current_q
        )
        
        self.q_table[state_key][action_code] = new_q
        
        # 添加到经验回放缓冲区
        self.replay_buffer.append((state_key, action_code, reward, next_state_key))
        if len(self.replay_buffer) > self.config["replay_buffer_size"]:
            self.replay_buffer.pop(0)
    
    def calculate_reward(self, execution_result: Dict) -> float:
        """计算奖励"""
        # 奖励 = 目标达成率*0.5 + 执行成功率*0.3 + 资源效率*0.2
        goal_progress = execution_result.get("goal_progress", 0.0)
        success_rate = execution_result.get("success_rate", 0.0)
        resource_efficiency = execution_result.get("resource_efficiency", 0.5)
        
        reward = (
            goal_progress * 0.5 +
            success_rate * 0.3 +
            resource_efficiency * 0.2
        )
        
        return reward
    
    def train_episode(self, state: Dict, execution_result: Dict) -> float:
        """训练一个回合"""
        # 获取动作
        action = self.get_action(state, training=True)
        
        # 执行动作 (模拟)
        reward = self.calculate_reward(execution_result)
        
        # 假设 next_state (简化)
        next_state = state.copy()
        next_state["progress"] = min(state.get("progress", 0) + 0.01, 2.0)
        
        # 更新 Q 值
        self.update_q_value(state, action, reward, next_state)
        
        # 更新统计
        self.training_stats["episodes"] += 1
        self.training_stats["total_reward"] += reward
        self.training_stats["average_reward"] = self.training_stats["total_reward"] / self.training_stats["episodes"]
        self.training_stats["best_reward"] = max(self.training_stats["best_reward"], reward)
        
        # 衰减探索率
        self.config["exploration_rate"] = max(
            self.config["min_exploration"],
            self.config["exploration_rate"] * self.config["exploration_decay"]
        )
        
        # 定期保存
        if self.training_stats["episodes"] % 10 == 0:
            self._save_model()
        
        return reward
    
    def show_status(self):
        """显示训练状态"""
        print("\n" + "="*60)
        print("📊 Learning Agent 训练状态")
        print("="*60)
        print(f"状态数：{len(self.q_table)}")
        print(f"训练轮次：{self.training_stats['episodes']}")
        print(f"平均奖励：{self.training_stats['average_reward']:.3f}")
        print(f"最佳奖励：{self.training_stats['best_reward']:.3f}")
        print(f"探索率：{self.config['exploration_rate']:.3f}")
        print(f"经验回放：{len(self.replay_buffer)} 条")
        print(f"{'='*60}")
    
    def train_batch(self, batch_size: int = 100):
        """批量训练"""
        print(f"\n🎓 开始批量训练：{batch_size} 轮")
        
        for i in range(batch_size):
            # 生成随机状态
            state = {
                "progress": random.uniform(0.0, 2.0),
                "hour": random.randint(0, 23),
                "resource": random.uniform(0.0, 1.0),
                "success": random.randint(0, 10),
                "frequency": random.randint(1, 12),
            }
            
            # 生成随机执行结果
            execution_result = {
                "goal_progress": random.uniform(0.0, 2.0),
                "success_rate": random.uniform(0.5, 1.0),
                "resource_efficiency": random.uniform(0.5, 1.0),
            }
            
            # 训练
            reward = self.train_episode(state, execution_result)
            
            if (i + 1) % 20 == 0:
                print(f"  轮次 {i+1}/{batch_size}, 平均奖励：{self.training_stats['average_reward']:.3f}")
        
        # 保存模型
        self._save_model()
        print(f"\n✅ 批量训练完成！")
        self.show_status()


def main():
    """主函数"""
    workspace_root = "/home/nicola/.openclaw/workspace"
    agent = QLearningAgent(workspace_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--status":
            agent.show_status()
        elif command == "--train":
            agent.train_batch(100)
        elif command == "--evaluate":
            print("策略评估功能开发中...")
        else:
            print(f"未知命令：{command}")
    else:
        # 默认显示状态
        agent.show_status()


if __name__ == "__main__":
    import sys
    main()
