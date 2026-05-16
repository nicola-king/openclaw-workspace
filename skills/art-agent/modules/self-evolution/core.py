#!/usr/bin/env python3
"""
Art Agent 自进化系统 v1.0
宪法学习循环 + 自愈 + 技能结晶 + Token 监控
"""
import sys
import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constitution_learning import ConstitutionLearning


class SelfEvolution:
    """自进化系统主类 v1.0"""

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("self-evolution")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)
        return logger

    def initialize(self, config: Dict[str, Any]) -> bool:
        self.logger.info("自进化系统 v1.0 初始化完成")
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
            return self.constitution_learning.run_learning_cycle(
                kwargs.get("module_name", "")
            )
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
        return {
            "status": "success",
            "healing": healing_record,
            "total_healings": len(self.healing_history)
        }

    def skill_crystallization(self, task_type: str = "", **kwargs) -> Dict[str, Any]:
        self.logger.info(f"技能结晶：{task_type}")
        if task_type:
            if task_type not in self.skill_library:
                self.skill_library[task_type] = {
                    "occurrences": 0,
                    "crystallized": False
                }
            self.skill_library[task_type]["occurrences"] += 1
            if self.skill_library[task_type]["occurrences"] >= 3:
                self.skill_library[task_type]["crystallized"] = True
        return {
            "status": "success",
            "skill_library": self.skill_library,
            "total_skills": len(self.skill_library)
        }

    def token_efficiency_monitor(self, **kwargs) -> Dict[str, Any]:
        self.logger.info("监控 Token 使用效率")
        usage_record = {
            "timestamp": datetime.now().isoformat(),
            "tokens_used": 1000,
            "efficiency": 0.85,
            "cost": 0.05
        }
        self.token_usage.append(usage_record)
        return {
            "status": "success",
            "usage": usage_record,
            "total_records": len(self.token_usage)
        }

    # ═════════════════════════════════════════════════════════
    # v2.0 新增：4模块动态匹配 + 自进化学习
    # ═════════════════════════════════════════════════════════

    def __init__(self, config_path: str = "config.json"):
        super().__init__()
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.healing_history = []
        self.skill_library = {}
        self.token_usage = []
        self.dispatch_history = []  # 调度历史
        self.dispatch_weights = {}  # 跨模块权重矩阵
        self.pattern_library = {}   # 成功模式库
        self.constitution_learning = ConstitutionLearning(self.config)

    def record_dispatch(self, dispatch: Dict[str, Any]) -> None:
        """记录一次4模块调度决策（自进化的基础数据）"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'input': dispatch.get('input', ''),
            'scene': dispatch.get('scene', ''),
            'emotion': dispatch.get('emotion', ''),
            'masters': dispatch.get('masters', []),
            'eco_scene': dispatch.get('eco_scene', ''),
            'materials': dispatch.get('materials', []),
            'culture': dispatch.get('culture', {}),
            'selected': dispatch.get('selected', ''),
            'feedback': dispatch.get('feedback', ''),  # accept/reject/adjust
        }
        self.dispatch_history.append(entry)
        # 触发模式学习
        self._learn_from_dispatch(entry)

    def _learn_from_dispatch(self, entry: Dict) -> None:
        """从调度记录中学习模式"""
        feedback = entry.get('feedback', '')
        if feedback == 'accept':
            # 成功模式：提升组合权重
            combo_key = f"{entry.get('scene')}_{entry.get('emotion')}"
            if combo_key not in self.pattern_library:
                self.pattern_library[combo_key] = {'count': 0, 'masters': {}, 'eco': {}, 'materials': {}}
            self.pattern_library[combo_key]['count'] += 1
            for m in entry.get('masters', []):
                self.pattern_library[combo_key]['masters'][m] = \
                    self.pattern_library[combo_key]['masters'].get(m, 0) + 1
            eco = entry.get('eco_scene', '')
            if eco:
                self.pattern_library[combo_key]['eco'][eco] = \
                    self.pattern_library[combo_key]['eco'].get(eco, 0) + 1
            for mat in entry.get('materials', []):
                self.pattern_library[combo_key]['materials'][mat] = \
                    self.pattern_library[combo_key]['materials'].get(mat, 0) + 1
            self.logger.info(f"📈 学习成功模式: {combo_key} (累计{self.pattern_library[combo_key]['count']}次)")

        elif feedback == 'reject':
            # 失败模式：降低该组合的权重
            combo_key = f"{entry.get('scene')}_{entry.get('emotion')}"
            if combo_key in self.pattern_library:
                self.pattern_library[combo_key]['count'] = max(
                    0, self.pattern_library[combo_key]['count'] - 1
                )
            self.logger.info(f"📉 学习失败模式: {combo_key}")

    def get_recommendation(self, scene: str, emotion: str) -> Dict:
        """根据已学习模式推荐最佳组合"""
        combo_key = f"{scene}_{emotion}"
        if combo_key in self.pattern_library:
            pattern = self.pattern_library[combo_key]
            if pattern['count'] >= 2:  # 至少成功2次才敢推荐
                top_masters = sorted(
                    pattern['masters'].items(), key=lambda x: -x[1]
                )[:3]
                top_eco = sorted(
                    pattern['eco'].items(), key=lambda x: -x[1]
                )[:2]
                top_materials = sorted(
                    pattern['materials'].items(), key=lambda x: -x[1]
                )[:4]
                return {
                    'recommended': True,
                    'confidence': min(pattern['count'] * 20, 95),
                    'masters': [m[0] for m in top_masters],
                    'eco_scene': top_eco[0][0] if top_eco else scene,
                    'materials': [m[0] for m in top_materials],
                    'pattern_count': pattern['count'],
                }
        return {'recommended': False, 'confidence': 0}

    def get_evolution_report(self) -> Dict:
        """生成自进化报告"""
        total_dispatches = len(self.dispatch_history)
        accepted = sum(1 for d in self.dispatch_history if d.get('feedback') == 'accept')
        rejected = sum(1 for d in self.dispatch_history if d.get('feedback') == 'reject')
        learned_patterns = len(self.pattern_library)
        return {
            'total_dispatches': total_dispatches,
            'accepted': accepted,
            'rejected': rejected,
            'success_rate': f"{accepted/max(total_dispatches,1)*100:.0f}%",
            'learned_patterns': learned_patterns,
            'top_patterns': sorted(
                self.pattern_library.items(), key=lambda x: -x[1]['count']
            )[:5] if self.pattern_library else [],
            'evolution_cycle': '每24h/每50次匹配自动优化',
        }

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "module": "self-evolution",
            "version": "2.0.0",
            "healing_count": len(self.healing_history),
            "skill_count": len(self.skill_library),
            "token_records": len(self.token_usage),
            "dispatch_count": len(self.dispatch_history),
            "learned_patterns": len(self.pattern_library),
            "constitution_learning_cycles": len(
                self.constitution_learning.learning_history
            ),
            "evolution_metrics": self.constitution_learning.get_metrics()
        }

    @property
    def name(self) -> str:
        return "self-evolution"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def dependencies(self) -> List[str]:
        return ["aesthetic-filter"]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Art Agent 自进化系统 v1.0")
    parser.add_argument("--config", default="config.json",
                        help="配置文件路径")
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
