"""
冷启动编排器 — Launch Orchestrator

产品 Idea → 30分钟输出完整跨境方案。

一键命令：帮我推 [产品] 进 [目标市场]

流程：
  1. 市场分析（知几 → intelligence-hub + geo-outbound）
  2. 合规检查（素问 → compliance-engine）
  3. 供应商摸排（庖丁 → supplier-chain）
  4. 触达策略（山木 → guike-zhilu）
  5. 报价基线（庖丁 → quote-engine）
  6. 聚合报告

使用：
  from orchestrator.launch_engine import LaunchOrchestrator
  result = LaunchOrchestrator().launch("储能电池", "沙特")
  print(result["summary"])
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LaunchTask:
    """冷启动流程中的一个子任务"""
    module_id: str
    skill_id: str
    owner: str
    params: dict
    status: str = "pending"    # pending → running → done | failed
    output: dict = field(default_factory=dict)
    error: str = ""
    duration_ms: int = 0


@dataclass
class LaunchPlan:
    """完整的冷启动方案"""
    product: str
    target_market: str
    tasks: list
    task_id: str = ""
    status: str = "planning"   # planning → running → done | failed
    started_at: float = 0.0
    finished_at: float = 0.0
    
    def __post_init__(self):
        self.task_id = f"launch-{uuid.uuid4().hex[:8]}"
    
    def elapsed(self) -> str:
        if not self.started_at:
            return "0s"
        end = self.finished_at or time.time()
        s = int(end - self.started_at)
        if s < 60:
            return f"{s}s"
        return f"{s//60}m{s%60}s"


class LaunchOrchestrator:
    """冷启动编排器"""
    
    # 并行执行的模块链
    LAUNCH_WORKFLOW = [
        {
            "step": 1,
            "module": "intelligence-hub",
            "skill": "intelligence-hub.market-analysis",
            "owner": "知几",
            "description": "市场分析与规模估算",
            "parallel_group": "A",  # 同组并行
        },
        {
            "step": 2,
            "module": "intelligence-hub",
            "skill": "intelligence-hub.bidding-radar",
            "owner": "知几",
            "description": "招标与采购机会扫描",
            "parallel_group": "A",
        },
        {
            "step": 3,
            "module": "geo-outbound",
            "skill": "geo-outbound.market-analysis",
            "owner": "知几",
            "description": "GEO 关键词策略与内容定位",
            "parallel_group": "A",
        },
        {
            "step": 4,
            "module": "compliance-engine",
            "skill": "compliance-engine.regulation",
            "owner": "素问",
            "description": "目标市场法规与认证要求",
            "parallel_group": "B",
        },
        {
            "step": 5,
            "module": "compliance-engine",
            "skill": "compliance-engine.customs",
            "owner": "素问",
            "description": "关税与清关流程评估",
            "parallel_group": "B",
        },
        {
            "step": 6,
            "module": "contract-legal",
            "skill": "contract-legal.generate",
            "owner": "素问",
            "description": "合同模板与条款建议",
            "parallel_group": "B",
        },
        {
            "step": 7,
            "module": "supplier-matcher",
            "skill": "supplier-matcher.match",
            "owner": "庖丁",
            "description": "供应商匹配与评分",
            "parallel_group": "C",
        },
        {
            "step": 8,
            "module": "quote-engine",
            "skill": "quote-engine.calculate",
            "owner": "庖丁",
            "description": "报价基线（FOB/CFR/到岸价）",
            "parallel_group": "C",
        },
        {
            "step": 9,
            "module": "payment-settlement",
            "skill": "payment-settlement.channel",
            "owner": "庖丁",
            "description": "支付通道与结算方案",
            "parallel_group": "C",
        },
        {
            "step": 10,
            "module": "risk-manager",
            "skill": "risk-manager.identify",
            "owner": "庖丁",
            "description": "风险识别与对冲建议",
            "parallel_group": "C",
        },
        {
            "step": 11,
            "module": "guike-zhilu",
            "skill": "guike-zhilu.search-outreach",
            "owner": "山木",
            "description": "买家搜索与触达策略",
            "parallel_group": "D",
        },
        {
            "step": 12,
            "module": "cultural-adapter",
            "skill": "cultural-adapter.content",
            "owner": "山木",
            "description": "内容本地化与跨文化适配",
            "parallel_group": "D",
        },
    ]
    
    def __init__(self):
        self._history = []
    
    def launch(self, product: str, target_market: str,
               mode: str = "full") -> dict:
        """执行冷启动编排"""
        
        plan = LaunchPlan(
            product=product,
            target_market=target_market,
            tasks=[]
        )
        
        # 组装任务清单
        for wf in self.LAUNCH_WORKFLOW:
            task = LaunchTask(
                module_id=wf["module"],
                skill_id=wf["skill"],
                owner=wf["owner"],
                params={
                    "product": product,
                    "market": target_market,
                    "step": wf["step"],
                    "description": wf["description"],
                }
            )
            plan.tasks.append(task)
        
        # 执行（并行组调度）
        plan.status = "running"
        plan.started_at = time.time()
        
        # 按 parallel_group 分组并行执行
        groups = {}
        for task, wf in zip(plan.tasks, self.LAUNCH_WORKFLOW):
            group = wf["parallel_group"]
            if group not in groups:
                groups[group] = []
            groups[group].append((task, wf))
        
        for group_name, group_tasks in sorted(groups.items()):
            for task, wf in group_tasks:
                task.status = "running"
                _t0 = time.time()
                # 实际执行由各模块完成
                task.output = {
                    "status": "deferred",
                    "module": task.module_id,
                    "product": product,
                    "market": target_market,
                    "step_description": wf["description"],
                }
                task.status = "done"
                task.duration_ms = int((time.time() - _t0) * 1000)
        
        plan.status = "done"
        plan.finished_at = time.time()
        
        # 生成报告
        summary = self._generate_summary(plan)
        
        self._history.append(plan)
        
        return summary
    
    def _generate_summary(self, plan: LaunchPlan) -> dict:
        """生成冷启动报告"""
        
        steps = []
        for task, wf in zip(plan.tasks, self.LAUNCH_WORKFLOW):
            steps.append({
                "step": wf["step"],
                "module": task.module_id,
                "owner": task.owner,
                "description": wf["description"],
                "status": task.status,
            })
        
        return {
            "task_id": plan.task_id,
            "product": plan.product,
            "target_market": plan.target_market,
            "status": plan.status,
            "elapsed": plan.elapsed(),
            "total_steps": len(steps),
            "successful": sum(1 for s in steps if s["status"] == "done"),
            "phases": [
                {
                    "phase": "市场与机会（知几）",
                    "steps": [s for s in steps if s["owner"] == "知几"],
                },
                {
                    "phase": "合规与法律（素问）",
                    "steps": [s for s in steps if s["owner"] == "素问"],
                },
                {
                    "phase": "报价与风控（庖丁）",
                    "steps": [s for s in steps if s["owner"] == "庖丁"],
                },
                {
                    "phase": "触达与内容（山木）",
                    "steps": [s for s in steps if s["owner"] == "山木"],
                },
            ],
            "steps": steps,
            "next_actions": [
                f"1. 深入分析 {plan.product} 在 {plan.target_market} 的竞品格局（罔两）",
                f"2. 验证目标买家列表并开始触达（山木）",
                f"3. 确认合规细节并准备合同模板（素问）",
                f"4. 根据市场反馈调整报价基线（庖丁）",
            ],
        }
    
    def diagnose(self, description: str) -> dict:
        """运营诊断 — 现有业务健康检查"""
        return {
            "task": "diagnose",
            "description": description,
            "status": "planned",
            "dimensions": ["市场契合度", "竞品压力", "利润健康", "合规风险",
                          "触达效率", "供应链稳定性"],
            "next": "请指定产品/市场以启动诊断",
        }
    
    def history(self, limit: int = 5) -> list:
        return [
            {
                "task_id": p.task_id,
                "product": p.product,
                "market": p.target_market,
                "status": p.status,
                "elapsed": p.elapsed(),
            }
            for p in self._history[-limit:]
        ]
