#!/usr/bin/env python3
"""
Agent Spawner - 子代理创建与委派

作者：太一 AGI
创建：2026-04-09
"""

import uuid
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 导入 Brain/Hands
import sys
sys.path.insert(0, "/home/nicola/.openclaw/workspace/skills/brain-hands-separator")

from brain import Brain, Decision
from hands import Hands
from session import Session


@dataclass
class AgentConfig:
    """Agent 配置"""
    task: str
    tools: List[str]
    timeout: int = 300
    success_criteria: str = ""
    resources: Dict = field(default_factory=dict)


@dataclass
class AgentResult:
    """Agent 执行结果"""
    agent_id: str
    success: bool
    output: str
    error: Optional[str]
    duration_ms: int
    events_count: int


class AgentSpawner:
    """Agent 创建器"""
    
    def __init__(self, parent_id: str):
        """
        初始化
        
        Args:
            parent_id: 父 Agent ID
        """
        self.parent_id = parent_id
        self.children: Dict[str, Dict] = {}
        self.results: Dict[str, AgentResult] = {}
    
    def spawn(self, task: str, tools: List[str], timeout: int = 300, **kwargs) -> str:
        """
        创建子代理
        
        Args:
            task: 任务描述
            tools: 可用工具列表
            timeout: 超时时间 (秒)
        
        Returns:
            子代理 ID
        """
        agent_id = f"{self.parent_id}-child-{uuid.uuid4().hex[:8]}"
        
        # 创建独立 Session
        session = Session(agent_id)
        
        # 创建 Brain/Hands
        brain = Brain()
        hands = Hands()
        
        # 存储配置
        config = AgentConfig(
            task=task,
            tools=tools,
            timeout=timeout,
            **kwargs
        )
        
        self.children[agent_id] = {
            "config": config,
            "session": session,
            "brain": brain,
            "hands": hands,
            "status": "created",
            "created_at": datetime.now()
        }
        
        return agent_id
    
    def run(self, agent_id: str) -> AgentResult:
        """
        运行单个 Agent
        
        Args:
            agent_id: Agent ID
        
        Returns:
            AgentResult: 执行结果
        """
        if agent_id not in self.children:
            return AgentResult(
                agent_id=agent_id,
                success=False,
                output="",
                error="Agent 不存在",
                duration_ms=0,
                events_count=0
            )
        
        child = self.children[agent_id]
        start_time = datetime.now()
        
        try:
            # 更新状态
            child["status"] = "running"
            
            # 执行任务
            config = child["config"]
            session = child["session"]
            brain = child["brain"]
            hands = child["hands"]
            
            # 初始决策
            decision = brain.decide(config.task, [])
            
            # 执行循环
            max_iterations = 20
            for i in range(max_iterations):
                # 执行行动
                for action in decision.actions:
                    result = hands.execute(action)
                    session.log_event(
                        action_type=action.tool,
                        action_data={"command": action.command},
                        result={"success": result.success, "output": result.output}
                    )
                    
                    # 检查是否完成
                    if decision.next_step == "done":
                        break
                
                # 下一步决策
                events = session.get_events()
                decision = brain.decide(config.task, events)
                
                if decision.next_step in ["done", "error"]:
                    break
            
            # 计算结果
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            events = session.get_events()
            
            result = AgentResult(
                agent_id=agent_id,
                success=decision.next_step == "done",
                output=session.get_state("final_output") or "任务完成",
                error=None if decision.next_step != "error" else "任务失败",
                duration_ms=duration_ms,
                events_count=len(events)
            )
            
            # 存储结果
            self.results[agent_id] = result
            child["status"] = "completed"
            
            return result
            
        except Exception as e:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            result = AgentResult(
                agent_id=agent_id,
                success=False,
                output="",
                error=str(e),
                duration_ms=duration_ms,
                events_count=0
            )
            
            self.results[agent_id] = result
            child["status"] = "error"
            
            return result
    
    def run_parallel(self, max_workers: int = 5) -> Dict[str, AgentResult]:
        """
        并行运行所有子代理
        
        Args:
            max_workers: 最大并发数
        
        Returns:
            所有结果
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.run, agent_id): agent_id
                for agent_id in self.children.keys()
            }
            
            for future in as_completed(futures):
                agent_id = futures[future]
                try:
                    future.result()
                except Exception as e:
                    self.results[agent_id] = AgentResult(
                        agent_id=agent_id,
                        success=False,
                        output="",
                        error=str(e),
                        duration_ms=0,
                        events_count=0
                    )
        
        return self.results
    
    def aggregate(self, results: Dict[str, AgentResult] = None) -> Dict:
        """
        汇总结果
        
        Args:
            results: 结果字典 (默认使用 self.results)
        
        Returns:
            汇总结果
        """
        if results is None:
            results = self.results
        
        # 统计
        total = len(results)
        success = sum(1 for r in results.values() if r.success)
        failed = total - success
        
        # 合并输出
        outputs = [r.output for r in results.values() if r.success]
        errors = [r.error for r in results.values() if r.error]
        
        # 总耗时
        total_duration = sum(r.duration_ms for r in results.values())
        
        return {
            "summary": {
                "total": total,
                "success": success,
                "failed": failed,
                "success_rate": success / total if total > 0 else 0
            },
            "outputs": outputs,
            "errors": errors,
            "total_duration_ms": total_duration,
            "aggregated_at": datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict:
        """获取所有子代理状态"""
        return {
            agent_id: {
                "status": child["status"],
                "task": child["config"].task,
                "created_at": child["created_at"].isoformat()
            }
            for agent_id, child in self.children.items()
        }


def main():
    """测试"""
    spawner = AgentSpawner("parent-001")
    
    print("👥 Agent Spawner 测试")
    print()
    
    # 创建子代理
    child1 = spawner.spawn(
        task="测试任务 1",
        tools=["shell"]
    )
    
    child2 = spawner.spawn(
        task="测试任务 2",
        tools=["shell"]
    )
    
    print(f"创建子代理：{child1}, {child2}")
    
    # 并行运行
    results = spawner.run_parallel()
    
    print(f"执行完成：{len(results)} 个")
    
    # 汇总
    summary = spawner.aggregate()
    print(f"汇总：{summary['summary']}")


if __name__ == "__main__":
    main()
