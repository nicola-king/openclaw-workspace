#!/usr/bin/env python3
"""
visual-workflow v2.0.0
太一可视化工作流引擎 — 重量方案

基于 React Flow / D3.js 兼容的 JSON Schema，
构建可交互的 Agent 调度面板。

功能：
- 调度拓扑 JSON 生成（React Flow 兼容）
- 执行历史追蹤 → 时间线可视化
- 节点状态追踪（待办/进行中/完成/失败）
- Mermaid 导出（兼容轻量方案）
"""

import json
import logging
import os
import uuid
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from collections import OrderedDict

# ─── React Flow 节点/边 Schema ─────────────────────────────────────

NODE_BASE = {
    "id": "",
    "type": "default",  # custom node types: taiyi, bot, tool, output
    "position": {"x": 0, "y": 0},
    "data": {
        "label": "",
        "type": "",
        "status": "idle",       # idle | running | success | error
        "domain": "",
        "timestamp": "",
        "details": {},
    },
    "style": {},
}

EDGE_BASE = {
    "id": "",
    "source": "",
    "target": "",
    "label": "",
    "animated": False,
    "style": {},
    "data": {
        "action": "",
        "status": "idle",
    },
}

# ─── DFS 布局引擎 ──────────────────────────────────────────────────

# Node type -> color palette
NODE_THEME = {
    "taiyi":  {"bg": "#6366f1", "fg": "#fff", "border": "#4338ca"},
    "bot":    {"bg": "#22c55e", "fg": "#fff", "border": "#16a34a"},
    "tool":   {"bg": "#f59e0b", "fg": "#fff", "border": "#d97706"},
    "output": {"bg": "#8b5cf6", "fg": "#fff", "border": "#7c3aed"},
    "data":   {"bg": "#06b6d4", "fg": "#fff", "border": "#0891b2"},
}

STATUS_COLORS = {
    "idle":    "#94a3b8",
    "running": "#3b82f6",
    "success": "#22c55e",
    "error":   "#ef4444",
}


class VisualWorkflowEngine:
    """
    可视化工作流引擎 — 生成 React Flow 兼容的数据结构。
    支持自动布局（DFS 拓扑排序）、状态追踪、历史回放。
    """

    def __init__(self):
        self.logger = logging.getLogger("visual-workflow")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter(
                "%(asctime)s - visual-workflow - %(levelname)s - %(message)s"
            ))
            self.logger.addHandler(h)

        self._workflows: Dict[str, dict] = {}

    # ═══════════════════════════════════════════════════════════
    # 公开 API
    # ═══════════════════════════════════════════════════════════

    def build_dispatch_workflow(
        self,
        workflow_id: str,
        domain: str,
        task_description: str,
        active_bots: List[str],
        collaborations: Optional[List[Dict]] = None,
        statuses: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict] = None,
    ) -> dict:
        """
        构建一次调度的工作流 JSON（React Flow 兼容）。

        Returns:
            {
                "id": str,
                "domain": str,
                "title": str,
                "created_at": str,
                "nodes": [...],
                "edges": [...],
                "viewport": {"x": 0, "y": 0, "zoom": 1.0}
            }
        """
        ts = datetime.now(timezone.utc).isoformat()
        domain_cfg = self._get_domain_config(domain)
        if not domain_cfg:
            raise ValueError(f"未知域: {domain}")

        nodes = []
        edges = []
        statuses = statuses or {}

        # ── 1) 太一节点 ──
        taiyi_id = f"{workflow_id}_taiyi"
        taiyi_node = self._make_node(
            nid=taiyi_id,
            label=f"🧘 太一 · {domain_cfg['label']}",
            ntype="taiyi",
            pos=self._auto_pos("center", domain_cfg, stage=0, idx=0, total=1),
            status=statuses.get("太一", "success"),
            domain=domain,
            details={"domain": domain, "task": task_description},
        )
        nodes.append(taiyi_node)

        # ── 2) Bot 节点 ──
        bot_names = active_bots or list(domain_cfg["bots"].keys())
        bot_map = {}

        for i, name in enumerate(bot_names):
            bot_cfg = domain_cfg["bots"].get(name)
            if not bot_cfg:
                continue
            bid = f"{workflow_id}_{name}"
            bot_map[name] = bid

            bot_node = self._make_node(
                nid=bid,
                label=f"{self._bot_emoji(name)} {name}",
                ntype="bot",
                pos=self._auto_pos("column", domain_cfg, stage=1, idx=i, total=len(bot_names)),
                status=statuses.get(name, "idle"),
                domain=domain,
                details={"module": bot_cfg.get("module", ""), "desc": bot_cfg.get("desc", "")},
            )
            nodes.append(bot_node)

            # 太一 → Bot 边
            edge_id = f"{taiyi_id}_to_{bid}"
            edges.append(self._make_edge(
                eid=edge_id,
                source=taiyi_id,
                target=bid,
                label="分派",
                animated=statuses.get(name) == "running",
                action="dispatch",
            ))

        # ── 3) 产出节点 ──
        output_id = f"{workflow_id}_output"
        output_node = self._make_node(
            nid=output_id,
            label="📋 聚合交付",
            ntype="output",
            pos=self._auto_pos("center", domain_cfg, stage=2, idx=0, total=1),
            domain=domain,
            details={"description": task_description},
        )
        nodes.append(output_node)

        # Bot → 产出边
        for name, bid in bot_map.items():
            edge_id = f"{bid}_to_output"
            status = statuses.get(name)
            edges.append(self._make_edge(
                eid=edge_id,
                source=bid,
                target=output_id,
                label="返回",
                animated=False,
                action="return",
            ))

        # ── 4) 协作边 ──
        if collaborations:
            for col in collaborations:
                src = bot_map.get(col["from"])
                tgt = bot_map.get(col["to"])
                if src and tgt:
                    eid = f"{src}_to_{tgt}_collab"
                    edges.append(self._make_edge(
                        eid=eid,
                        source=src,
                        target=tgt,
                        label=col.get("label", "协作"),
                        animated=True,
                        action="collaborate",
                        style={"strokeDasharray": "5 5"},
                    ))

        workflow = {
            "id": workflow_id,
            "domain": domain,
            "title": f"{domain_cfg['label']} — {task_description}",
            "created_at": ts,
            "nodes": nodes,
            "edges": edges,
            "viewport": {"x": 0, "y": 0, "zoom": 1.0},
            "metadata": metadata or {},
        }

        self._workflows[workflow_id] = workflow
        return workflow

    def build_full_system_workflow(self) -> dict:
        """
        构建全系统拓扑图（双域 + 共享工具链）。
        """
        wid = "system_landscape"
        now = datetime.now(timezone.utc).isoformat()

        nodes = []
        edges = []

        x_start = 0
        domains = [
            ("travel", "domestic", "🐾 旅游探路者"),
            ("trade", "trade", "🌐 跨境贸易"),
        ]

        for di, (domain_key, domain_type, domain_label) in enumerate(domains):
            cfg = self._get_domain_config(domain_key)
            dx = x_start + di * 400

            # Domain taiyi
            tid = f"full_{domain_key}_taiyi"
            nodes.append(self._make_node(
                nid=tid,
                label=f"🧘 太一 · {domain_label}",
                ntype="taiyi",
                pos={"x": dx + 100, "y": 50},
                domain=domain_key,
            ))

            # Domain bots
            for bi, (bname, bcfg) in enumerate(cfg["bots"].items()):
                bid = f"full_{domain_key}_{bname}"
                nodes.append(self._make_node(
                    nid=bid,
                    label=f"{self._bot_emoji(bname)} {bname}",
                    ntype="bot",
                    pos={"x": dx + 50, "y": 150 + bi * 80},
                    domain=domain_key,
                    details={"desc": bcfg.get("desc", "")},
                ))
                edges.append(self._make_edge(
                    eid=f"{tid}_to_{bid}",
                    source=tid, target=bid,
                    label="调度", action="dispatch",
                ))

        # Shared tools
        shared_x = 200
        shared_y = 600
        tools = [
            ("🔎 搜索Agent v4", "search_v4"),
            ("✅ 验证管道", "verify"),
            ("💾 缓存 + 统计", "cache"),
        ]
        for ti, (tlabel, tid_inner) in enumerate(tools):
            tid_full = f"full_tool_{tid_inner}"
            nodes.append(self._make_node(
                nid=tid_full,
                label=tlabel,
                ntype="tool",
                pos={"x": shared_x + ti * 200, "y": shared_y},
                domain="shared",
            ))

        # Cross-domain shared connections
        for domain_key, _, _ in domains:
            tid = f"full_{domain_key}_taiyi"
            for ti, (_, tid_inner) in enumerate(tools):
                tid_full = f"full_tool_{tid_inner}"
                edges.append(self._make_edge(
                    eid=f"{tid}_to_{tid_full}",
                    source=tid, target=tid_full,
                    label="共享",
                    animated=False,
                    action="share",
                    style={"strokeDasharray": "5 5"},
                ))

        return {
            "id": wid,
            "domain": "system",
            "title": "太一 Agent 系统全景拓扑",
            "created_at": now,
            "nodes": nodes,
            "edges": edges,
            "viewport": {"x": 0, "y": 0, "zoom": 0.8},
        }

    def export_mermaid(self, workflow_id: str) -> str:
        """将工作流导出为 Mermaid 代码（兼容轻量方案）"""
        wf = self._workflows.get(workflow_id)
        if not wf:
            raise KeyError(f"工作流未找到: {workflow_id}")
        return self._workflow_to_mermaid(wf)

    def export_json(self, workflow_id: str) -> dict:
        """导出工作流 JSON（React Flow 原生）"""
        wf = self._workflows.get(workflow_id)
        if not wf:
            raise KeyError(f"工作流未找到: {workflow_id}")
        return wf

    def add_timestamp(self, workflow_id: str, node_id: str,
                      status: str, message: str = "") -> dict:
        """更新某个节点的时间戳/状态（用于时间线回放）"""
        wf = self._workflows.get(workflow_id)
        if not wf:
            raise KeyError(f"工作流未找到: {workflow_id}")

        for node in wf["nodes"]:
            if node["id"] == node_id:
                ts = datetime.now(timezone.utc).isoformat()
                node["data"]["status"] = status
                node["data"]["timestamp"] = ts
                node["data"]["details"]["last_message"] = message
                break
        return wf

    def get_all_workflows(self) -> Dict[str, dict]:
        return dict(self._workflows)

    # ═══════════════════════════════════════════════════════════
    # 内部方法
    # ═══════════════════════════════════════════════════════════

    def _get_domain_config(self, domain: str) -> Optional[dict]:
        DOMAINS = {
            "travel": {
                "label": "旅游探路者",
                "bots": OrderedDict([
                    ("知几", {"module": "intelligence_hub", "desc": "情报引擎·数据分析·省钱方案·评分排序"}),
                    ("山木", {"module": "planner", "desc": "行程规划·短游/深度/团体编排·输出交付"}),
                    ("素问", {"module": "destination_guide", "desc": "目的地文化·签证·天气安全·API支持"}),
                    ("罔两", {"module": "market_intel", "desc": "真实酒店/餐馆/景点·大V博主·真实验证"}),
                    ("庖丁", {"module": "savings_engine", "desc": "三档预算·成本优化·财务风险·ROI分析"}),
                ]),
            },
            "trade": {
                "label": "跨境贸易",
                "bots": OrderedDict([
                    ("知几", {"module": "buyer_intel", "desc": "情报分析·数据挖掘·市场研究·买家情报"}),
                    ("山木", {"module": "outreach", "desc": "触达推进·开发信·供应商匹配·履约交付"}),
                    ("素问", {"module": "compliance", "desc": "合规引擎·合同模板·跨文化·搜索技术"}),
                    ("罔两", {"module": "competitor_monitor", "desc": "竞品监控·真实验证·富化Agent·监控"}),
                    ("庖丁", {"module": "pricing_risk", "desc": "报价成本·支付结算·风控·退税计算"}),
                ]),
            },
            "domestic": {
                "label": "国内旅游",
                "bots": OrderedDict(),
            },
        }
        return DOMAINS.get(domain)

    def _make_node(self, nid: str, label: str, ntype: str,
                   pos: dict, status: str = "idle",
                   domain: str = "", details: dict = None) -> dict:
        theme = NODE_THEME.get(ntype, NODE_THEME["tool"])
        ts = datetime.now(timezone.utc).isoformat()
        return {
            "id": nid,
            "type": "default" if ntype == "bot" else ntype,
            "position": pos,
            "data": {
                "label": label,
                "type": ntype,
                "status": status,
                "domain": domain,
                "timestamp": ts if status != "idle" else "",
                "details": details or {},
            },
            "style": {
                "background": theme["bg"],
                "color": theme["fg"],
                "border": f"2px solid {STATUS_COLORS.get(status, theme['border'])}",
                "borderRadius": "8px",
                "padding": "8px 16px",
                "fontSize": "14px",
                "fontWeight": 500,
            },
        }

    def _make_edge(self, eid: str, source: str, target: str,
                   label: str, animated: bool = False,
                   action: str = "", style: dict = None) -> dict:
        return {
            "id": eid,
            "source": source,
            "target": target,
            "label": label,
            "animated": animated,
            "style": style or {},
            "data": {"action": action, "status": "idle"},
            "markerEnd": {"type": "arrowclosed"},
        }

    def _auto_pos(self, layout: str, cfg: dict,
                  stage: int, idx: int, total: int) -> dict:
        """自动布局（DFS 拓扑排序）"""
        x_center = 300
        x_spacing = 350
        y_spacing = 100

        if layout == "center":
            return {"x": x_center - 75, "y": 50 + stage * y_spacing}
        elif layout == "column":
            col_width = 250
            num_per_col = max(1, total)
            y_base = 50 + stage * y_spacing
            x_off = x_center - (num_per_col * col_width) // 2 + idx * col_width
            return {"x": x_off, "y": y_base}
        return {"x": 0, "y": 0}

    def _bot_emoji(self, name: str) -> str:
        return {"知几": "🧠", "山木": "🏔️", "素问": "📚",
                "罔两": "🔍", "庖丁": "💰"}.get(name, "🤖")

    def _workflow_to_mermaid(self, wf: dict) -> str:
        """JSON workflow → Mermaid flowchart"""
        lines = ["---", f"title: {wf['title']}", "---",
                 "flowchart TD", ""]

        # Subgraphs
        taiyi_nodes = [n for n in wf["nodes"] if n["data"]["type"] == "taiyi"]
        bot_nodes = [n for n in wf["nodes"] if n["data"]["type"] == "bot"]
        output_nodes = [n for n in wf["nodes"] if n["data"]["type"] == "output"]
        tool_nodes = [n for n in wf["nodes"] if n["data"]["type"] == "tool"]

        if taiyi_nodes:
            lines.append("    subgraph 调度中枢[🧘 太一调度中枢]")
            for n in taiyi_nodes:
                lines.append(f"        {n['id']}[\"{n['data']['label']}\"]")
            lines.append("    end")
            lines.append("")

        if bot_nodes:
            lines.append("    subgraph Bot集群[🤖 Bot 集群]")
            for n in bot_nodes:
                status_icon = self._status_icon(n["data"]["status"])
                lines.append(f"        {n['id']}[\"{status_icon} {n['data']['label']}\"]")
            lines.append("    end")
            lines.append("")

        if tool_nodes:
            lines.append("    subgraph 工具链[⚙️ 共享工具链]")
            for n in tool_nodes:
                lines.append(f"        {n['id']}[\"{n['data']['label']}\"]")
            lines.append("    end")
            lines.append("")

        if output_nodes:
            lines.append("    subgraph 产出[📋 调度产出]")
            for n in output_nodes:
                lines.append(f"        {n['id']}[\"{n['data']['label']}\"]")
            lines.append("    end")
            lines.append("")

        for e in wf["edges"]:
            label = e.get("label", "")
            animated = e.get("animated", False)
            arrow = "==>" if animated else "-->"
            label_str = f"|{label}|" if label else ""
            lines.append(f"    {e['source']} {arrow}{label_str} {e['target']}")

        lines.append("")
        lines.append("%% 样式")
        for nt, theme in NODE_THEME.items():
            names = [n["id"] for n in wf["nodes"] if n["data"]["type"] == nt]
            if names:
                cls = " ".join(names)
                lines.append(
                    f"    classDef {nt} fill:{theme['bg']},color:{theme['fg']},"
                    f"stroke:{theme['border']},stroke-width:2px,rx:8px"
                )
                lines.append(f"    class {cls} {nt}")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _status_icon(status: str) -> str:
        return {"idle": "⏸️", "running": "▶️", "success": "✅",
                "error": "❌"}.get(status, "⏸️")

    # ═══════════════════════════════════════════════════════════
    # 标准接口
    # ═══════════════════════════════════════════════════════════

    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        if task == "build_dispatch":
            wf = self.build_dispatch_workflow(
                kwargs.get("workflow_id", f"wf_{uuid.uuid4().hex[:8]}"),
                kwargs.get("domain", "travel"),
                kwargs.get("task_description", ""),
                kwargs.get("active_bots", []),
                kwargs.get("collaborations"),
                kwargs.get("statuses"),
                kwargs.get("metadata"),
            )
            return {"status": "success", "module": "visual-workflow",
                    "task": task, "workflow": wf}

        elif task == "build_system":
            wf = self.build_full_system_workflow()
            return {"status": "success", "module": "visual-workflow",
                    "task": task, "workflow": wf}

        elif task == "export_mermaid":
            wf_id = kwargs.get("workflow_id", "")
            if wf_id not in self._workflows:
                return {"status": "error", "module": "visual-workflow",
                        "task": task, "error": f"工作流 {wf_id} 未找到"}
            mermaid = self.export_mermaid(wf_id)
            return {"status": "success", "module": "visual-workflow",
                    "task": task, "mermaid": mermaid}

        elif task == "export_json":
            wf_id = kwargs.get("workflow_id", "")
            if wf_id not in self._workflows:
                return {"status": "error", "module": "visual-workflow",
                        "task": task, "error": f"工作流 {wf_id} 未找到"}
            return {"status": "success", "module": "visual-workflow",
                    "task": task, "workflow": self.export_json(wf_id)}

        elif task == "update_status":
            wf_id = kwargs.get("workflow_id", "")
            node_id = kwargs.get("node_id", "")
            status = kwargs.get("status", "")
            message = kwargs.get("message", "")
            wf = self.add_timestamp(wf_id, node_id, status, message)
            return {"status": "success", "module": "visual-workflow",
                    "task": task, "workflow": wf}

        else:
            return {"status": "error", "module": "visual-workflow",
                    "task": task, "error": f"未知任务: {task}"}

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "module": "visual-workflow",
            "version": "2.0.0",
            "workflow_count": len(self._workflows),
        }

    @property
    def name(self) -> str:
        return "visual-workflow"

    @property
    def version(self) -> str:
        return "2.0.0"

    @property
    def dependencies(self) -> List[str]:
        return ["aesthetic-filter", "dispatch-viz"]


# ─── CLI 入口 ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="可视化工作流引擎")
    parser.add_argument("--task", choices=["dispatch", "system", "mermaid"],
                        default="dispatch", help="任务类型")
    parser.add_argument("--domain", choices=["travel", "trade"],
                        default="travel")
    parser.add_argument("--bots", nargs="*", help="激活的 Bot")
    parser.add_argument("--desc", default="", help="任务描述")
    parser.add_argument("--output", "-o", help="JSON 输出文件")
    parser.add_argument("--wid", default=f"wf_demo", help="工作流 ID")
    args = parser.parse_args()

    eng = VisualWorkflowEngine()
    if args.task == "system":
        result = eng.execute("build_system")
    elif args.task == "mermaid":
        result = eng.execute("build_dispatch",
                             workflow_id=args.wid,
                             domain=args.domain,
                             task_description=args.desc,
                             active_bots=args.bots or [])
        mermaid_result = eng.execute("export_mermaid", workflow_id=args.wid)
        output = mermaid_result.get("mermaid", "")
    else:
        result = eng.execute("build_dispatch",
                             workflow_id=args.wid,
                             domain=args.domain,
                             task_description=args.desc,
                             active_bots=args.bots or [])

    if args.task == "mermaid":
        if args.output:
            Path(args.output).write_text(output)
            print(f"✅ Mermaid 已写入 {args.output}")
        else:
            print(output)
    else:
        output = result.get("workflow", result)
        output_str = json.dumps(output, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(output_str)
            print(f"✅ JSON 已写入 {args.output}")
        else:
            print(output_str)
