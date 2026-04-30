#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冲刺合约系统
参考：Anthropic 多智能体框架 - 冲刺合约机制
用途：规划者 + 实现者 + 评估者之间的结构化协作
"""

from datetime import datetime
from typing import Dict, List

class SprintContract:
    """冲刺合约"""
    
    def __init__(self, sprint_id: str, name: str, description: str):
        self.sprint_id = sprint_id
        self.name = name
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.status = 'pending'  # pending, in_progress, completed, failed
        
        # 合约条款（可测试标准）
        self.acceptance_criteria = []
        
        # 参与方
        self.planner = ''
        self.generator = ''
        self.evaluator = ''
        
        # 迭代历史
        self.iterations = []
    
    def add_acceptance_criterion(self, criterion: str, weight: float = 1.0):
        """
        添加验收标准
        :param criterion: 标准描述
        :param weight: 权重 (用于评分)
        """
        self.acceptance_criteria.append({
            'criterion': criterion,
            'weight': weight,
            'passed': False,
            'feedback': '',
        })
    
    def assign_roles(self, planner: str, generator: str, evaluator: str):
        """分配角色"""
        self.planner = planner
        self.generator = generator
        self.evaluator = evaluator
    
    def start(self):
        """开始冲刺"""
        self.status = 'in_progress'
        self.started_at = datetime.now().isoformat()
    
    def complete_iteration(self, iteration: int, feedback: str, improvements: List[str]):
        """完成一次迭代"""
        self.iterations.append({
            'iteration': iteration,
            'feedback': feedback,
            'improvements': improvements,
            'timestamp': datetime.now().isoformat(),
        })
    
    def evaluate(self) -> Dict:
        """
        评估冲刺结果
        :return: 评估报告
        """
        passed_count = sum(1 for c in self.acceptance_criteria if c['passed'])
        total_count = len(self.acceptance_criteria)
        pass_rate = passed_count / total_count if total_count > 0 else 0
        
        # 加权评分
        weighted_score = sum(
            c['weight'] for c in self.acceptance_criteria if c['passed']
        ) / sum(c['weight'] for c in self.acceptance_criteria) if self.acceptance_criteria else 0
        
        return {
            'sprint_id': self.sprint_id,
            'name': self.name,
            'status': self.status,
            'pass_rate': f"{pass_rate*100:.1f}%",
            'weighted_score': f"{weighted_score*100:.1f}%",
            'iterations': len(self.iterations),
            'passed': pass_rate >= 0.8,  # 80% 通过率算完成
        }
    
    def render_contract(self) -> str:
        """渲染合约文档"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"  冲刺合约：{self.name}")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append(f"【基本信息】")
        lines.append(f"  ID: {self.sprint_id}")
        lines.append(f"  描述：{self.description}")
        lines.append(f"  状态：{self.status}")
        lines.append(f"  创建时间：{self.created_at}")
        lines.append("")
        
        lines.append(f"【角色分配】")
        lines.append(f"  规划者 (Planner): {self.planner}")
        lines.append(f"  实现者 (Generator): {self.generator}")
        lines.append(f"  评估者 (Evaluator): {self.evaluator}")
        lines.append("")
        
        lines.append(f"【验收标准】")
        for i, criterion in enumerate(self.acceptance_criteria, 1):
            status = "✅" if criterion['passed'] else "🟡"
            lines.append(f"  {i}. {status} {criterion['criterion']} (权重：{criterion['weight']})")
            if criterion['feedback']:
                lines.append(f"     反馈：{criterion['feedback']}")
        lines.append("")
        
        if self.iterations:
            lines.append(f"【迭代历史】")
            for iteration in self.iterations:
                lines.append(f"  迭代 {iteration['iteration']}: {iteration['feedback']}")
                lines.append(f"    改进：{', '.join(iteration['improvements'])}")
            lines.append("")
        
        # 评估结果
        eval_result = self.evaluate()
        lines.append(f"【评估结果】")
        lines.append(f"  通过率：{eval_result['pass_rate']}")
        lines.append(f"  加权评分：{eval_result['weighted_score']}")
        lines.append(f"  迭代次数：{eval_result['iterations']}")
        lines.append(f"  状态：{'✅ 通过' if eval_result['passed'] else '🟡 需改进'}")
        lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


class SprintSystem:
    """冲刺系统（管理多个冲刺）"""
    
    def __init__(self):
        self.sprints = []
    
    def create_sprint(self, name: str, description: str) -> SprintContract:
        """创建新冲刺"""
        sprint_id = f"SPRINT-{len(self.sprints)+1:03d}"
        sprint = SprintContract(sprint_id, name, description)
        self.sprints.append(sprint)
        return sprint
    
    def get_active_sprints(self) -> List[SprintContract]:
        """获取活跃冲刺"""
        return [s for s in self.sprints if s.status == 'in_progress']
    
    def render_dashboard(self) -> str:
        """渲染冲刺仪表板"""
        lines = []
        lines.append("=" * 60)
        lines.append("  冲刺系统仪表板")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append(f"【总览】")
        lines.append(f"  总冲刺数：{len(self.sprints)}")
        lines.append(f"  进行中：{len(self.get_active_sprints())}")
        lines.append(f"  已完成：{len([s for s in self.sprints if s.status == 'completed'])}")
        lines.append(f"  失败：{len([s for s in self.sprints if s.status == 'failed'])}")
        lines.append("")
        
        if self.sprints:
            lines.append(f"【最近冲刺】")
            for sprint in self.sprints[-5:]:
                status_icon = {"pending": "🟡", "in_progress": "🔵", "completed": "✅", "failed": "❌"}[sprint.status]
                lines.append(f"  {status_icon} {sprint.sprint_id}: {sprint.name} ({sprint.status})")
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    system = SprintSystem()
    
    # 创建冲刺（知几-E 开发）
    sprint1 = system.create_sprint(
        name="知几-E v2.2 开发",
        description="集成 LMSR+ 贝叶斯模块"
    )
    
    # 添加验收标准
    sprint1.add_acceptance_criterion("LMSR 定价模型测试通过", weight=2.0)
    sprint1.add_acceptance_criterion("贝叶斯更新模块测试通过", weight=2.0)
    sprint1.add_acceptance_criterion("策略引擎 v2.2 集成完成", weight=3.0)
    sprint1.add_acceptance_criterion("文档完善", weight=1.0)
    
    # 分配角色
    sprint1.assign_roles(
        planner='太一',
        generator='素问',
        evaluator='罔两'
    )
    
    # 开始冲刺
    sprint1.start()
    
    # 模拟迭代
    sprint1.complete_iteration(1, "LMSR 测试失败：配置文件缺失", ["创建 polymarket.json"])
    sprint1.complete_iteration(2, "贝叶斯更新正常，策略引擎需调整阈值", ["调整置信度阈值到 85%"])
    
    # 标记验收标准
    sprint1.acceptance_criteria[0]['passed'] = True
    sprint1.acceptance_criteria[1]['passed'] = True
    sprint1.acceptance_criteria[2]['passed'] = True
    sprint1.acceptance_criteria[3]['passed'] = True
    
    # 完成冲刺
    sprint1.status = 'completed'
    
    print(system.render_dashboard())
    print(sprint1.render_contract())
