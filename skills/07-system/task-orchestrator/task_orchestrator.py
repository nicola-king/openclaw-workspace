#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一智能任务调度系统 v1.0

功能:
1. 智能任务分解 - 将复杂任务分解为可执行的子任务
2. 智能 Agent 匹配 - 根据任务类型匹配最适合的 Agent
3. 智能任务分配 - 分配任务给 Agent 并追踪执行
4. 结果汇总 - 汇总所有 Agent 的执行结果

作者：太一 AGI
创建：2026-04-18
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('TaskOrchestrator')


class TaskPriority(Enum):
    """任务优先级"""
    P0 = "P0 - 紧急重要"
    P1 = "P1 - 重要"
    P2 = "P2 - 普通"
    P3 = "P3 - 低优先级"


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "待执行"
    RUNNING = "执行中"
    COMPLETED = "已完成"
    FAILED = "失败"
    CANCELLED = "已取消"


@dataclass
class SubTask:
    """子任务"""
    id: str
    name: str
    description: str
    assigned_agent: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.P2
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None


@dataclass
class Task:
    """主任务"""
    id: str
    name: str
    description: str
    original_request: str
    subtasks: List[SubTask] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.P2
    result: Optional[Dict] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None


class AgentRegistry:
    """Agent 注册表"""
    
    def __init__(self):
        self.agents = {
            # 核心 Agent
            "taiyi": {"name": "太一", "role": "CEO", "capabilities": ["decision", "coordination", "planning"]},
            "zhiji": {"name": "知几", "role": "Trader", "capabilities": ["trading", "analysis", "quant"]},
            "shanmu": {"name": "山木", "role": "Content", "capabilities": ["writing", "creative", "marketing"]},
            "suwen": {"name": "素问", "role": "Coder", "capabilities": ["coding", "development", "review"]},
            "paoding": {"name": "庖丁", "role": "Analyst", "capabilities": ["cost", "analysis", "finance"]},
            "wangliang": {"name": "王良", "role": "Knowledge", "capabilities": ["search", "qa", "knowledge"]},
            "design": {"name": "太一设计", "role": "Designer", "capabilities": ["design", "visual", "art"]},
            "voice": {"name": "太一语音", "role": "Voice", "capabilities": ["voice", "audio", "tts"]},
            
            # 专业 Agent
            "cross-border-trade": {"name": "跨境贸易 Agent", "role": "Trade", "capabilities": ["trade", "import-export", "customs"]},
            "travel": {"name": "旅行探路者", "role": "Travel", "capabilities": ["travel", "planning", "booking"]},
            "cost": {"name": "造价 Agent", "role": "Cost", "capabilities": ["cost", "estimate", "budget"]},
            "dao": {"name": "道 Agent", "role": "DAO", "capabilities": ["dao", "governance", "decision"]},
            "wu": {"name": "悟 Agent", "role": "Enlightenment", "capabilities": ["philosophy", "insight", "wisdom"]},
            
            # 多角色 Agent
            "pm": {"name": "PM Agent", "role": "PM", "capabilities": ["product", "planning", "requirement"]},
            "qa": {"name": "QA Agent", "role": "QA", "capabilities": ["testing", "quality", "bug"]},
            "release": {"name": "Release Manager", "role": "Release", "capabilities": ["deploy", "version", "changelog"]},
        }
        
        # 任务类型到 Agent 的映射
        self.task_agent_mapping = {
            "trade": ["cross-border-trade", "zhiji", "paoding"],
            "travel": ["travel", "shanmu"],
            "cost": ["cost", "paoding"],
            "coding": ["suwen", "qa"],
            "design": ["design", "shanmu"],
            "writing": ["shanmu", "wu"],
            "analysis": ["zhiji", "paoding", "wangliang"],
            "product": ["pm", "taiyi"],
            "testing": ["qa", "suwen"],
            "deploy": ["release", "suwen"],
            "dao": ["dao", "taiyi"],
            "philosophy": ["wu", "dao"],
            "voice": ["voice", "shanmu"],
            "knowledge": ["wangliang", "wu"],
        }
    
    def get_agent_for_task(self, task_type: str) -> List[str]:
        """根据任务类型获取合适的 Agent"""
        return self.task_agent_mapping.get(task_type, ["taiyi"])
    
    def get_agent_info(self, agent_id: str) -> Dict:
        """获取 Agent 信息"""
        return self.agents.get(agent_id, {"name": "Unknown", "role": "Unknown", "capabilities": []})
    
    def list_agents(self) -> List[Dict]:
        """列出所有 Agent"""
        return [
            {"id": agent_id, **info}
            for agent_id, info in self.agents.items()
        ]


class TaskDecomposer:
    """任务分解器"""
    
    def __init__(self):
        # 任务分解规则
        self.decomposition_rules = {
            "跨境贸易": self._decompose_trade_task,
            "旅行": self._decompose_travel_task,
            "造价": self._decompose_cost_task,
            "开发": self._decompose_dev_task,
            "设计": self._decompose_design_task,
            "写作": self._decompose_writing_task,
            "分析": self._decompose_analysis_task,
            "默认": self._decompose_default_task,
        }
    
    def decompose(self, task_description: str) -> List[Dict]:
        """
        分解任务为子任务
        
        Args:
            task_description: 任务描述
            
        Returns:
            子任务列表
        """
        # 识别任务类型
        task_type = self._identify_task_type(task_description)
        
        # 获取对应的分解函数
        decompose_func = self.decomposition_rules.get(
            task_type, 
            self.decomposition_rules["默认"]
        )
        
        # 执行分解
        subtasks = decompose_func(task_description)
        
        logger.info(f"📋 任务分解完成：{len(subtasks)} 个子任务")
        
        return subtasks
    
    def _identify_task_type(self, description: str) -> str:
        """识别任务类型"""
        description_lower = description.lower()
        
        if any(kw in description_lower for kw in ["跨境", "贸易", "进出口", "外贸"]):
            return "跨境贸易"
        elif any(kw in description_lower for kw in ["旅行", "旅游", "游玩", "行程"]):
            return "旅行"
        elif any(kw in description_lower for kw in ["造价", "成本", "预算", "估价"]):
            return "造价"
        elif any(kw in description_lower for kw in ["开发", "代码", "编程", "软件"]):
            return "开发"
        elif any(kw in description_lower for kw in ["设计", "图片", "视觉", "ui"]):
            return "设计"
        elif any(kw in description_lower for kw in ["写作", "文章", "文案", "内容"]):
            return "写作"
        elif any(kw in description_lower for kw in ["分析", "研究", "调查", "数据"]):
            return "分析"
        else:
            return "默认"
    
    def _decompose_trade_task(self, description: str) -> List[Dict]:
        """分解跨境贸易任务"""
        return [
            {"name": "市场分析", "agent": "zhiji", "description": "分析目标市场趋势和需求"},
            {"name": "产品选品", "agent": "cross-border-trade", "description": "选择合适的产品"},
            {"name": "供应商匹配", "agent": "cross-border-trade", "description": "寻找和评估供应商"},
            {"name": "成本核算", "agent": "paoding", "description": "计算成本和利润"},
            {"name": "物流方案", "agent": "cross-border-trade", "description": "设计物流方案"},
            {"name": "营销内容", "agent": "shanmu", "description": "生成营销内容"},
        ]
    
    def _decompose_travel_task(self, description: str) -> List[Dict]:
        """分解旅行任务"""
        return [
            {"name": "行程规划", "agent": "travel", "description": "规划旅行行程"},
            {"name": "交通预订", "agent": "travel", "description": "预订机票/车票"},
            {"name": "住宿推荐", "agent": "travel", "description": "推荐和预订酒店"},
            {"name": "景点规划", "agent": "travel", "description": "规划景点游览"},
            {"name": "餐饮推荐", "agent": "travel", "description": "推荐当地美食"},
            {"name": "预算估算", "agent": "paoding", "description": "估算旅行预算"},
        ]
    
    def _decompose_cost_task(self, description: str) -> List[Dict]:
        """分解造价任务"""
        return [
            {"name": "材料成本", "agent": "cost", "description": "计算材料成本"},
            {"name": "人工成本", "agent": "cost", "description": "计算人工成本"},
            {"name": "设备成本", "agent": "cost", "description": "计算设备成本"},
            {"name": "管理费用", "agent": "paoding", "description": "计算管理费用"},
            {"name": "利润分析", "agent": "paoding", "description": "分析利润率"},
        ]
    
    def _decompose_dev_task(self, description: str) -> List[Dict]:
        """分解开发任务"""
        return [
            {"name": "需求分析", "agent": "pm", "description": "分析产品需求"},
            {"name": "技术方案", "agent": "suwen", "description": "设计技术方案"},
            {"name": "代码开发", "agent": "suwen", "description": "编写代码"},
            {"name": "代码审查", "agent": "suwen", "description": "审查代码质量"},
            {"name": "测试验证", "agent": "qa", "description": "测试功能"},
            {"name": "部署发布", "agent": "release", "description": "部署上线"},
        ]
    
    def _decompose_design_task(self, description: str) -> List[Dict]:
        """分解设计任务"""
        return [
            {"name": "需求理解", "agent": "design", "description": "理解设计需求"},
            {"name": "创意构思", "agent": "shanmu", "description": "创意构思"},
            {"name": "视觉设计", "agent": "design", "description": "视觉设计"},
            {"name": "方案评审", "agent": "design", "description": "评审设计方案"},
            {"name": "修改完善", "agent": "design", "description": "修改完善"},
        ]
    
    def _decompose_writing_task(self, description: str) -> List[Dict]:
        """分解写作任务"""
        return [
            {"name": "主题确定", "agent": "shanmu", "description": "确定写作主题"},
            {"name": "大纲编写", "agent": "shanmu", "description": "编写文章大纲"},
            {"name": "内容创作", "agent": "shanmu", "description": "创作内容"},
            {"name": "润色修改", "agent": "shanmu", "description": "润色修改"},
            {"name": "审核发布", "agent": "wu", "description": "审核发布"},
        ]
    
    def _decompose_analysis_task(self, description: str) -> List[Dict]:
        """分解分析任务"""
        return [
            {"name": "数据收集", "agent": "wangliang", "description": "收集相关数据"},
            {"name": "数据分析", "agent": "zhiji", "description": "分析数据"},
            {"name": "趋势研判", "agent": "zhiji", "description": "研判趋势"},
            {"name": "报告撰写", "agent": "shanmu", "description": "撰写分析报告"},
        ]
    
    def _decompose_default_task(self, description: str) -> List[Dict]:
        """默认任务分解"""
        return [
            {"name": "任务分析", "agent": "taiyi", "description": "分析任务需求"},
            {"name": "方案制定", "agent": "taiyi", "description": "制定执行方案"},
            {"name": "执行任务", "agent": "taiyi", "description": "执行任务"},
            {"name": "结果汇总", "agent": "taiyi", "description": "汇总结果"},
        ]


class TaskOrchestrator:
    """任务调度器"""
    
    def __init__(self):
        self.registry = AgentRegistry()
        self.decomposer = TaskDecomposer()
        self.tasks: Dict[str, Task] = {}
        self.task_history: List[Task] = []
    
    def receive_task(self, request: str, priority: TaskPriority = TaskPriority.P2) -> Task:
        """
        接收任务
        
        Args:
            request: 用户请求
            priority: 任务优先级
            
        Returns:
            创建的任务
        """
        logger.info(f"📥 接收任务：{request[:50]}...")
        
        # 创建任务 ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 分解任务
        subtasks_data = self.decomposer.decompose(request)
        
        # 创建子任务
        subtasks = []
        for i, subtask_data in enumerate(subtasks_data):
            subtask = SubTask(
                id=f"{task_id}_sub{i+1}",
                name=subtask_data["name"],
                description=subtask_data["description"],
                assigned_agent=subtask_data["agent"],
                priority=priority,
            )
            subtasks.append(subtask)
        
        # 创建主任务
        task = Task(
            id=task_id,
            name=f"任务_{task_id}",
            description=request,
            original_request=request,
            subtasks=subtasks,
            priority=priority,
        )
        
        # 保存任务
        self.tasks[task_id] = task
        
        logger.info(f"✅ 任务创建完成：{task_id} ({len(subtasks)} 个子任务)")
        
        return task
    
    def execute_task(self, task_id: str) -> Dict:
        """
        执行任务
        
        Args:
            task_id: 任务 ID
            
        Returns:
            执行结果
        """
        if task_id not in self.tasks:
            return {"status": "error", "message": f"任务不存在：{task_id}"}
        
        task = self.tasks[task_id]
        logger.info(f"🚀 开始执行任务：{task_id}")
        
        task.status = TaskStatus.RUNNING
        
        # 执行所有子任务
        results = []
        for subtask in task.subtasks:
            result = self._execute_subtask(subtask)
            results.append(result)
            subtask.result = result
            subtask.status = TaskStatus.COMPLETED if result.get("success") else TaskStatus.FAILED
            subtask.completed_at = datetime.now().isoformat()
        
        # 汇总结果
        task.result = self._summarize_results(results)
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now().isoformat()
        
        # 移动到历史记录
        self.task_history.append(task)
        del self.tasks[task_id]
        
        logger.info(f"✅ 任务执行完成：{task_id}")
        
        return task.result
    
    def _execute_subtask(self, subtask: SubTask) -> Dict:
        """执行子任务"""
        logger.info(f"  📍 执行子任务：{subtask.name} (Agent: {subtask.assigned_agent})")
        
        # 获取 Agent 信息
        agent_info = self.registry.get_agent_info(subtask.assigned_agent)
        
        # 模拟执行 (实际应用中会调用真实的 Agent)
        result = {
            "success": True,
            "agent": agent_info["name"],
            "task": subtask.name,
            "description": subtask.description,
            "output": f"{agent_info['name']}已完成：{subtask.description}",
            "timestamp": datetime.now().isoformat(),
        }
        
        logger.info(f"  ✅ 子任务完成：{subtask.name}")
        
        return result
    
    def _summarize_results(self, results: List[Dict]) -> Dict:
        """汇总结果"""
        return {
            "total_subtasks": len(results),
            "completed": sum(1 for r in results if r.get("success")),
            "failed": sum(1 for r in results if not r.get("success")),
            "details": results,
            "summary": f"完成{len(results)}个子任务",
            "timestamp": datetime.now().isoformat(),
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            return {
                "id": task.id,
                "name": task.name,
                "status": task.status.value,
                "progress": f"{sum(1 for s in task.subtasks if s.status == TaskStatus.COMPLETED)}/{len(task.subtasks)}",
                "subtasks": [
                    {
                        "name": s.name,
                        "agent": s.assigned_agent,
                        "status": s.status.value,
                    }
                    for s in task.subtasks
                ],
            }
        return None
    
    def list_agents(self) -> List[Dict]:
        """列出所有可用 Agent"""
        return self.registry.list_agents()


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🧠 太一智能任务调度系统 v1.0 - 演示")
    logger.info("=" * 60)
    
    # 初始化调度器
    orchestrator = TaskOrchestrator()
    
    # 显示可用 Agent
    logger.info("\n📋 可用 Agent:")
    agents = orchestrator.list_agents()
    for agent in agents[:10]:  # 显示前 10 个
        logger.info(f"  • {agent['name']} ({agent['role']}) - {', '.join(agent['capabilities'][:3])}")
    logger.info(f"  ... 共{len(agents)}个 Agent")
    
    # 示例 1: 跨境贸易任务
    logger.info("\n" + "=" * 60)
    logger.info("📦 示例 1: 跨境贸易任务")
    logger.info("=" * 60)
    
    task1 = orchestrator.receive_task(
        "帮我做美国市场的跨境贸易，选品智能水杯",
        TaskPriority.P1
    )
    logger.info(f"任务 ID: {task1.id}")
    logger.info(f"子任务数：{len(task1.subtasks)}")
    for subtask in task1.subtasks:
        logger.info(f"  • {subtask.name} → {subtask.assigned_agent}")
    
    result1 = orchestrator.execute_task(task1.id)
    logger.info(f"\n执行结果：{result1['summary']}")
    
    # 示例 2: 旅行任务
    logger.info("\n" + "=" * 60)
    logger.info("✈️ 示例 2: 旅行任务")
    logger.info("=" * 60)
    
    task2 = orchestrator.receive_task(
        "帮我规划三亚 7 日游，预算 1 万元",
        TaskPriority.P2
    )
    logger.info(f"任务 ID: {task2.id}")
    logger.info(f"子任务数：{len(task2.subtasks)}")
    for subtask in task2.subtasks:
        logger.info(f"  • {subtask.name} → {subtask.assigned_agent}")
    
    result2 = orchestrator.execute_task(task2.id)
    logger.info(f"\n执行结果：{result2['summary']}")
    
    # 示例 3: 造价任务
    logger.info("\n" + "=" * 60)
    logger.info("💰 示例 3: 造价任务")
    logger.info("=" * 60)
    
    task3 = orchestrator.receive_task(
        "帮我估算这个项目的造价，包括材料和人工",
        TaskPriority.P1
    )
    logger.info(f"任务 ID: {task3.id}")
    logger.info(f"子任务数：{len(task3.subtasks)}")
    for subtask in task3.subtasks:
        logger.info(f"  • {subtask.name} → {subtask.assigned_agent}")
    
    result3 = orchestrator.execute_task(task3.id)
    logger.info(f"\n执行结果：{result3['summary']}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
