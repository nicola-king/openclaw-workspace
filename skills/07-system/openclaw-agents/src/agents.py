#!/usr/bin/env python3
"""
OpenClaw Agents - 全域自进化智能体系统 v1.0
太一 AGI · 2026-04-15

整合 4 大智能体能力:
- Scheduler Agent: 智能调度
- Learning Agent: 强化学习
- Prediction Agent: 预测分析
- Evolution Agent: 自主进化
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class OpenClawAgents:
    """OpenClaw 全域自进化智能体系统"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.skills_dir = self.workspace_root / "skills"
        self.monitoring_dir = self.workspace_root / "monitoring"
        self.agents_dir = self.skills_dir / "07-system" / "openclaw-agents"
        self.config_path = self.agents_dir / "config" / "openclaw-agents-config.json"
        
        # 配置
        self.config = {
            "scheduler": {
                "default_interval": 3600,
                "min_interval": 1800,
                "max_interval": 7200,
                "lag_threshold": 0.5,
                "ahead_threshold": 0.2,
            },
            "learning": {
                "learning_rate": 0.1,
                "discount_factor": 0.9,
                "exploration_rate": 0.1,
            },
            "prediction": {
                "forecast_days": 7,
                "warning_threshold": 0.8,
            },
            "evolution": {
                "auto_optimize": True,
                "auto_create_skills": True,
            }
        }
        
        # 加载配置
        self._load_config()
        
        # 智能体状态
        self.agents_status = {
            "scheduler": "ready",
            "learning": "ready",
            "prediction": "ready",
            "evolution": "ready",
        }
    
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text(encoding="utf-8"))
                for key in config_data:
                    if key in self.config:
                        self.config[key].update(config_data[key])
            except:
                pass
        
        # 保存配置
        self.config_path.parent.mkdir(exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def schedule(self) -> Dict:
        """执行智能调度"""
        print("\n" + "="*60)
        print("🤖 OpenClaw Agents - 智能调度")
        print("="*60)
        
        scheduler_script = self.skills_dir / "scheduler-agent" / "src" / "scheduler.py"
        
        if not scheduler_script.exists():
            return {"status": "error", "message": "Scheduler Agent 不存在"}
        
        try:
            result = subprocess.run(
                ["python3", str(scheduler_script), "--run-all"],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(self.workspace_root)
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout[:500],
                "error": result.stderr[:500] if result.stderr else "",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def train(self, episodes: int = 100) -> Dict:
        """执行学习训练"""
        print("\n" + "="*60)
        print("🧠 OpenClaw Agents - 强化学习训练")
        print("="*60)
        
        learner_script = self.skills_dir / "learning-agent" / "src" / "learner.py"
        
        if not learner_script.exists():
            return {"status": "error", "message": "Learning Agent 不存在"}
        
        try:
            result = subprocess.run(
                ["python3", str(learner_script), "--train"],
                capture_output=True,
                text=True,
                timeout=600,
                cwd=str(self.workspace_root)
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout[:500],
                "episodes": episodes,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def forecast(self, days: int = 7) -> Dict:
        """生成预测"""
        print("\n" + "="*60)
        print("🔮 OpenClaw Agents - 预测分析")
        print("="*60)
        
        predictor_script = self.skills_dir / "prediction-agent" / "src" / "predictor.py"
        
        if not predictor_script.exists():
            return {"status": "error", "message": "Prediction Agent 不存在"}
        
        try:
            result = subprocess.run(
                ["python3", str(predictor_script), "--forecast", str(days)],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.workspace_root)
            )
            
            forecast_data = json.loads(result.stdout) if result.stdout else {}
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "forecast": forecast_data,
                "days": days,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def evolve(self) -> Dict:
        """执行自主进化"""
        print("\n" + "="*60)
        print("🧬 OpenClaw Agents - 自主进化")
        print("="*60)
        
        evolver_script = self.skills_dir / "evolution-agent" / "src" / "evolver.py"
        
        if not evolver_script.exists():
            return {"status": "error", "message": "Evolution Agent 不存在"}
        
        try:
            result = subprocess.run(
                ["python3", str(evolver_script), "--evolve"],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(self.workspace_root)
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout[:500],
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def run_full_cycle(self) -> Dict:
        """执行完整自进化循环"""
        print("\n" + "🔄"*30)
        print("🚀 OpenClaw Agents - 完整自进化循环")
        print("🔄"*30)
        
        start_time = datetime.now()
        
        results = {
            "start_time": start_time.isoformat(),
            "steps": {},
        }
        
        # 1. 智能调度
        print("\n[1/4] 智能调度...")
        results["steps"]["schedule"] = self.schedule()
        
        # 2. 学习训练
        print("\n[2/4] 学习训练...")
        results["steps"]["train"] = self.train(100)
        
        # 3. 预测分析
        print("\n[3/4] 预测分析...")
        results["steps"]["forecast"] = self.forecast(7)
        
        # 4. 自主进化
        print("\n[4/4] 自主进化...")
        results["steps"]["evolve"] = self.evolve()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        results["end_time"] = end_time.isoformat()
        results["duration_seconds"] = duration
        
        # 统计成功次数
        success_count = sum(1 for step in results["steps"].values() if step.get("status") == "success")
        results["summary"] = {
            "total_steps": 4,
            "success_steps": success_count,
            "success_rate": success_count / 4,
        }
        
        # 保存结果
        self._save_cycle_result(results)
        
        print("\n" + "🔄"*30)
        print(f"✅ 完整自进化循环完成！耗时：{duration:.1f}秒")
        print(f"📊 成功率：{success_count}/4 ({results['summary']['success_rate']:.1%})")
        print("🔄"*30)
        
        return results
    
    def _save_cycle_result(self, results: Dict):
        """保存循环结果"""
        result_path = self.monitoring_dir / "openclaw-agents-cycle.json"
        result_path.parent.mkdir(exist_ok=True)
        result_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def show_status(self):
        """显示状态"""
        print("\n" + "="*60)
        print("🤖 OpenClaw Agents 状态")
        print("="*60)
        
        for agent, status in self.agents_status.items():
            emoji = "✅" if status == "ready" else "⚠️"
            print(f"{emoji} {agent}: {status}")
        
        print(f"\n配置：{self.config_path.exists()}")
        print(f"{'='*60}")


def main():
    """主函数"""
    workspace_root = "/home/nicola/.openclaw/workspace"
    agents = OpenClawAgents(workspace_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--status":
            agents.show_status()
        elif command == "--schedule":
            agents.schedule()
        elif command == "--train":
            episodes = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            agents.train(episodes)
        elif command == "--forecast":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            agents.forecast(days)
        elif command == "--evolve":
            agents.evolve()
        elif command == "--full-cycle":
            agents.run_full_cycle()
        else:
            print(f"未知命令：{command}")
            print("用法：agents.py [--status|--schedule|--train|--forecast|--evolve|--full-cycle]")
    else:
        agents.show_status()


if __name__ == "__main__":
    main()
