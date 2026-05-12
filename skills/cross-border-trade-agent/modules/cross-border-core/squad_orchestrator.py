"""
Squad Orchestrator — 动态编队引擎

复杂任务自动组建 Agent 小队 + 指定 Team Leader + 共享上下文 War Room。

架构：
  task → SquadOrchestrator.assemble() → Squad(leader, members, war_room)
       → squad.run() → parallel execution via war room
       → squad.summarize() → final output

使用：
  from squad_orchestrator import SquadOrchestrator
  orchestrator = SquadOrchestrator()
  squad = orchestrator.assemble("帮我推储能产品进沙特")
  result = squad.run()
  print(squad.summarize())
"""

import json
import time
import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


# ── 核心类型 ──

class SquadRole(Enum):
    LEADER = "leader"
    ANALYST = "analyst"       # 知几
    EXECUTOR = "executor"     # 山木
    RESEARCHER = "researcher" # 素问
    INTELLIGENCE = "intel"    # 罔两
    FINANCE = "finance"       # 庖丁


@dataclass
class SquadMember:
    bot_name: str          # 知几/山木/素问/罔两/庖丁
    role: SquadRole
    skills: list           # Skill ID 列表
    status: str = "idle"   # idle | working | done | blocked
    output: dict = field(default_factory=dict)


@dataclass
class SquadDecision:
    """待决策项 — Agent 向 Team Leader 请求裁决"""
    id: str
    question: str
    options: list
    context: str
    raised_by: str          # 提出 Agent
    resolved: bool = False
    resolution: str = ""


class WarRoom:
    """Squad 共享上下文白板 — 多 Agent 协同的公共状态"""
    
    def __init__(self, task_id: str, task_description: str):
        self.task_id = task_id
        self.task_description = task_description
        self.whiteboard = {}       # {key: {value, by, ts}}
        self.decisions = []        # 待决策 / 已决策
        self.changelog = []        # [{who, what, when}]
        self.milestones = []       # [{name, status, when}]
        self._started_at = time.time()
    
    def write(self, agent_id: str, key: str, value):
        """Agent 写入共享状态"""
        self.whiteboard[key] = {
            "value": value,
            "by": agent_id,
            "ts": time.strftime("%H:%M:%S"),
        }
        self.changelog.append({
            "who": agent_id, "what": f"写入 {key}", "when": self.changelog.__len__() + 1
        })
    
    def read(self, key: str):
        """读取共享状态"""
        entry = self.whiteboard.get(key)
        return entry["value"] if entry else None
    
    def read_all(self) -> dict:
        """当前白板快照"""
        return {k: v["value"] for k, v in self.whiteboard.items()}
    
    def request_decision(self, question: str, options: list,
                         context: str = "", raised_by: str = "") -> SquadDecision:
        """Agent 向 Team Leader 请求决策"""
        decision = SquadDecision(
            id=str(uuid.uuid4())[:8],
            question=question,
            options=options,
            context=context,
            raised_by=raised_by,
        )
        self.decisions.append(decision)
        self.changelog.append({
            "who": raised_by, "what": f"请求决策: {question}",
            "when": self.changelog.__len__() + 1,
        })
        return decision
    
    def resolve_decision(self, decision_id: str, resolution: str):
        """Team Leader 裁决"""
        for d in self.decisions:
            if d.id == decision_id:
                d.resolved = True
                d.resolution = resolution
                self.write("leader", f"decision:{decision_id}", resolution)
                break
    
    def add_milestone(self, name: str):
        self.milestones.append({
            "name": name, "status": "completed",
            "when": time.strftime("%H:%M:%S"),
        })
    
    def elapsed(self) -> str:
        s = int(time.time() - self._started_at)
        if s < 60:
            return f"{s}s"
        return f"{s//60}m{s%60}s"
    
    def summary(self) -> dict:
        return {
            "task_id": self.task_id,
            "task": self.task_description,
            "elapsed": self.elapsed(),
            "whiteboard_keys": list(self.whiteboard.keys()),
            "decisions_pending": len([d for d in self.decisions if not d.resolved]),
            "decisions_resolved": len([d for d in self.decisions if d.resolved]),
            "milestones": self.milestones,
            "changelog_count": len(self.changelog),
        }


class Squad:
    """一次动态编队的全生命周期"""
    
    def __init__(self, task_id: str, task_description: str,
                 leader: SquadMember, members: list):
        self.task_id = task_id
        self.task_description = task_description
        self.leader = leader
        self.members = members
        self.war_room = WarRoom(task_id, task_description)
        self.status = "assembled"  # assembled → running → done | failed
    
    def add_member(self, member: SquadMember):
        self.members.append(member)
    
    def run(self) -> dict:
        """执行编队任务（框架 • 实际执行由各 Bot 实现）"""
        self.status = "running"
        self.war_room.add_milestone("编队组建完成")
        self.war_room.write("leader", "squad:status", "running")
        
        # 1. Leader 拆解任务 + 写入白板
        self.war_room.write("leader", "task:breakdown",
                            f"已拆分为 {len(self.members)} 个子任务")
        
        # 2. 标记成员状态
        for m in self.members:
            m.status = "working"
        
        self.war_room.add_milestone("子任务已分派")
        
        # 3. 汇总（实际执行由具体 Bot 运行时完成）
        self.war_room.add_milestone("执行完成")
        self.status = "done"
        
        return {"status": "done", "task_id": self.task_id}
    
    def summarize(self) -> dict:
        """输出最终报告"""
        return {
            "task_id": self.task_id,
            "task": self.task_description,
            "status": self.status,
            "leader": self.leader.bot_name,
            "members": [{"bot": m.bot_name, "role": m.role.value,
                         "status": m.status} for m in self.members],
            "war_room": self.war_room.summary(),
            "decisions": [{"question": d.question, "resolution": d.resolution}
                          for d in self.war_room.decisions if d.resolved],
            "whiteboard": self.war_room.read_all(),
        }


class SquadOrchestrator:
    """编队调度引擎 — 意图→编队→执行→汇总"""
    
    # 意图 → {leader, members, pattern} 映射
    SQUAD_TEMPLATES = {
        "market_entry": {  # 市场进入
            "leader": "知几",
            "members": [
                ("知几", SquadRole.ANALYST, ["intelligence-hub.market-analysis",
                                              "intelligence-hub.policy-radar"]),
                ("山木", SquadRole.EXECUTOR, ["guike-zhilu.search-outreach",
                                               "cultural-adapter.content"]),
                ("素问", SquadRole.RESEARCHER, ["compliance-engine.regulation",
                                                  "contract-legal.generate"]),
                ("庖丁", SquadRole.FINANCE, ["quote-engine.calculate",
                                              "risk-manager.identify"]),
            ],
            "description": "全链路市场进入方案：分析→合规→触达→报价→风险",
        },
        "competitor_deep": {  # 竞品深挖
            "leader": "罔两",
            "members": [
                ("罔两", SquadRole.INTELLIGENCE, ["intelligence-hub.competitor-monitor",
                                                   "company-enricher.enrich"]),
                ("知几", SquadRole.ANALYST, ["intelligence-hub.trend-analysis",
                                              "data-integrator.multi-source"]),
            ],
            "description": "竞品深挖：监控→分析→报告",
        },
        "sourcing_full": {  # 全链路采购
            "leader": "庖丁",
            "members": [
                ("庖丁", SquadRole.FINANCE, ["supplier-matcher.match",
                                              "quote-engine.calculate"]),
                ("罔两", SquadRole.INTELLIGENCE, ["company-enricher.verify",
                                                   "real-data-verifier.five-way"]),
                ("山木", SquadRole.EXECUTOR, ["transaction-support.fulfill",
                                               "supply-chain.optimize"]),
                ("素问", SquadRole.RESEARCHER, ["compliance-engine.customs",
                                                  "contract-legal.review"]),
            ],
            "description": "全链路采购：寻源→验证→报价→合规→履约",
        },
        "diagnose": {  # 运营诊断
            "leader": "知几",
            "members": [
                ("知几", SquadRole.ANALYST, ["intelligence-hub.trend-analysis",
                                              "report-engine.report"]),
                ("罔两", SquadRole.INTELLIGENCE, ["intelligence-hub.competitor-list",
                                                   "intelligence-hub.platform-monitor"]),
                ("庖丁", SquadRole.FINANCE, ["quote-engine.profit-analysis",
                                              "risk-manager.identify"]),
                ("素问", SquadRole.RESEARCHER, ["compliance-engine.regulation"]),
            ],
            "description": "全维度运营诊断：趋势→竞品→利润→风险→合规",
        },
    }
    
    def __init__(self):
        self._active_squads = {}
    
    def detect_intent(self, task_description: str) -> str:
        """从任务描述识别意图模式"""
        text = task_description.lower()
        patterns = {
            "market_entry": ["进入", "推入", "打入", "冷启动", "市场进入",
                             "launch", "entry", "新市场"],
            "competitor_deep": ["竞品", "对手", "竞争", "谁在做",
                                "competitor", "competitive"],
            "sourcing_full": ["采购", "寻源", "找供应商", "找厂家",
                              "source", "supplier", "procurement"],
            "diagnose": ["诊断", "分析", "评估", "健康检查",
                         "audit", "review", "health"],
        }
        for intent, triggers in patterns.items():
            if any(t in text for t in triggers):
                return intent
        return "market_entry"  # 默认
    
    def assemble(self, task_description: str, intent: str = None) -> Squad:
        """根据任务组建 Squad"""
        if not intent:
            intent = self.detect_intent(task_description)
        
        template = self.SQUAD_TEMPLATES.get(intent)
        if not template:
            template = self.SQUAD_TEMPLATES["market_entry"]
        
        task_id = f"squad-{uuid.uuid4().hex[:8]}"
        
        # 创建 Leader
        leader = SquadMember(
            bot_name=template["leader"],
            role=SquadRole.LEADER,
            skills=[],
        )
        
        # 创建成员
        members = []
        for bot_name, role, skills in template["members"]:
            members.append(SquadMember(
                bot_name=bot_name,
                role=role,
                skills=skills,
            ))
        
        squad = Squad(
            task_id=task_id,
            task_description=task_description,
            leader=leader,
            members=members,
        )
        
        self._active_squads[task_id] = squad
        return squad
    
    def get_squad(self, task_id: str) -> Optional[Squad]:
        return self._active_squads.get(task_id)
    
    def active_count(self) -> int:
        return len(self._active_squads)
