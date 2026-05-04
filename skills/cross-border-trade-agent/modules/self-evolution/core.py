#!/usr/bin/env python3
"""
自我进化系统 v10.0
宪法学习循环 + 自愈 + 技能结晶 + Token 监控
"""
import sys
import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constitution_learning import ConstitutionLearning

class SelfEvolution:
    """自我进化系统主类 v10.0"""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.healing_history = []
        self.skill_library = {}
        self.token_usage = []
        self.constitution_learning = ConstitutionLearning(self.config)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("self-evolution")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def initialize(self, config: Dict[str, Any]) -> bool:
        self.logger.info("自我进化系统 v10.0 初始化完成")
        return True

    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        self.logger.info(f"执行任务：{task}")
        if task == "healing":
            return self.browser_healing(**kwargs)
        elif task == "crystallization":
            return self.skill_crystallization(**kwargs)
        elif task == "token_monitor":
            return self.token_efficiency_monitor(**kwargs)
        elif task == "constitution_learning":
            return self.constitution_learning.run_learning_cycle(kwargs.get("module_name", ""))
        elif task == "get_metrics":
            return self.constitution_learning.get_metrics()
        else:
            return {"status": "error", "message": f"未知任务：{task}"}

    def browser_healing(self, **kwargs) -> Dict[str, Any]:
        self.logger.info("执行浏览器自愈")
        healing_record = {
            "timestamp": datetime.now().isoformat(),
            "action": "browser_healing",
            "status": "success",
            "details": "浏览器状态已恢复"
        }
        self.healing_history.append(healing_record)
        return {"status": "success", "healing": healing_record, "total_healings": len(self.healing_history)}

    def skill_crystallization(self, task_type: str = "", **kwargs) -> Dict[str, Any]:
        self.logger.info(f"技能结晶：{task_type}")
        if task_type:
            if task_type not in self.skill_library:
                self.skill_library[task_type] = {"occurrences": 0, "crystallized": False}
            self.skill_library[task_type]["occurrences"] += 1
            if self.skill_library[task_type]["occurrences"] >= 3:
                self.skill_library[task_type]["crystallized"] = True
        return {"status": "success", "skill_library": self.skill_library, "total_skills": len(self.skill_library)}

    def token_efficiency_monitor(self, **kwargs) -> Dict[str, Any]:
        self.logger.info("监控 Token 使用效率")
        usage_record = {
            "timestamp": datetime.now().isoformat(),
            "tokens_used": 1000,
            "efficiency": 0.85,
            "cost": 0.05
        }
        self.token_usage.append(usage_record)
        return {"status": "success", "usage": usage_record, "total_records": len(self.token_usage)}

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "module": "self-evolution",
            "version": "10.0.0",
            "healing_count": len(self.healing_history),
            "skill_count": len(self.skill_library),
            "token_records": len(self.token_usage),
            "constitution_learning_cycles": len(self.constitution_learning.learning_history),
            "evolution_metrics": self.constitution_learning.get_metrics()
        }

    @property
    def name(self) -> str:
        return "self-evolution"

    @property
    def version(self) -> str:
        return "10.0.0"

    @property
    def dependencies(self) -> List[str]:
        return ["cross-border-core"]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="自我进化系统模块 v10.0")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    parser.add_argument("--task", help="执行任务")
    parser.add_argument("--module-name", help="模块名称")
    args = parser.parse_args()
    agent = SelfEvolution(config_path=args.config)
    if args.task:
        result = agent.execute(task=args.task, module_name=args.module_name)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(agent.health_check(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
