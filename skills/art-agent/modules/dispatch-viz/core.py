#!/usr/bin/env python3
"""
dispatch-viz v1.0.0
调度拓扑可视化引擎 — 轻量方案

每次太一执行 Agent 调度后，自动生成 Mermaid 拓扑图：
1. 采集本次调度的 Agent 拓扑结构
2. 生成 Mermaid flowchart 代码
3. 写入飞书画板（lark-whiteboard）或本地文件

兼容两个调度体系：
- travel-dispatch（旅游探路者）
- cross-border-trade（跨境贸易）
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# ─── Mermaid 模板 ──────────────────────────────────────────────────

MERMAID_TEMPLATE_TITLE = """---
title: {title}
---
flowchart TD
{subgraph_decls}

{flow_lines}

%% 样式
classDef taiyi fill:#6366f1,color:#fff,stroke:#4338ca,stroke-width:2px,rx:8px
classDef bot fill:#22c55e,color:#fff,stroke:#16a34a,stroke-width:2px,rx:8px
classDef tool fill:#f59e0b,color:#fff,stroke:#d97706,stroke-width:1px,rx:4px
classDef output fill:#8b5cf6,color:#fff,stroke:#7c3aed,stroke-width:2px,rx:8px
classDef data fill:#06b6d4,color:#fff,stroke:#0891b2,stroke-width:1px,rx:4px

class {taiyi_id} taiyi
class {bot_ids} bot
class {output_id} output
"""


class DispatchVizModule:
    """调度拓扑可视化引擎"""

    DOMAINS = {
        "travel": {
            "title": "太一 · 旅游探路者调度拓扑",
            "taiyi_id": "taiyi_travel",
            "output_id": "travel_output",
            "bots": {
                "知几": {"id": "zhiji_t", "desc": "情报引擎·数据分析·省钱方案·评分排序"},
                "山木": {"id": "shanmu_t", "desc": "行程规划·短游/深度/团体编排·输出交付"},
                "素问": {"id": "suwen_t", "desc": "目的地文化·签证·天气安全·API支持"},
                "罔两": {"id": "wangliang_t", "desc": "真实酒店/餐馆/景点·大V博主·真实验证"},
                "庖丁": {"id": "paoding_t", "desc": "三档预算·成本优化·财务风险·ROI分析"},
            },
        },
        "trade": {
            "title": "太一 · 跨境贸易调度拓扑",
            "taiyi_id": "taiyi_trade",
            "output_id": "trade_output",
            "bots": {
                "知几": {"id": "zhiji_tr", "desc": "情报分析·数据挖掘·市场研究·买家情报"},
                "山木": {"id": "shanmu_tr", "desc": "触达推进·开发信·供应商匹配·履约交付"},
                "素问": {"id": "suwen_tr", "desc": "合规引擎·合同模板·跨文化·搜索技术"},
                "罔两": {"id": "wangliang_tr", "desc": "竞品监控·真实验证·富化Agent·监控"},
                "庖丁": {"id": "paoding_tr", "desc": "报价成本·支付结算·风控·退税计算"},
            },
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger("dispatch-viz")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter(
                "%(asctime)s - dispatch-viz - %(levelname)s - %(message)s"
            ))
            self.logger.addHandler(h)

    def generate_topology(self, domain: str = "travel",
                          active_bots: Optional[List[str]] = None,
                          task_description: str = "",
                          metadata: Optional[Dict[str, Any]] = None) -> str:
        """生成 Mermaid 拓扑图代码。"""
        cfg = self.DOMAINS.get(domain)
        if not cfg:
            raise ValueError(f"未知域: {domain}, 可选: {list(self.DOMAINS.keys())}")

        bots = cfg["bots"]
        if active_bots:
            bots = {k: v for k, v in bots.items() if k in active_bots}

        title = cfg["title"]
        if task_description:
            title += f" — {task_description}"

        taiyi_id = cfg["taiyi_id"]
        output_id = cfg["output_id"]

        subgraph_lines = []
        subgraph_lines.append(f"    subgraph 太一[太一 · 调度中枢]")
        subgraph_lines.append(f"        {taiyi_id}(\"🧘 太一\")")
        subgraph_lines.append(f"    end")

        bot_nodes = []
        for name, info in bots.items():
            nid = info["id"]
            desc = info["desc"]
            bot_nodes.append((name, nid, desc))

        if bot_nodes:
            subgraph_lines.append(f"    subgraph Bot集群[Bot 集群]")
            for name, nid, desc in bot_nodes:
                emoji = self._bot_emoji(name)
                subgraph_lines.append(f"        {nid}[\"{emoji} {name}\"]")
            subgraph_lines.append(f"    end")

        subgraph_lines.append(f"    subgraph 产出[调度产出]")
        subgraph_lines.append(f"        {output_id}(\"📋 聚合交付\")")
        subgraph_lines.append(f"    end")

        flow_lines = []
        for name, nid, _ in bot_nodes:
            flow_lines.append(f"    {taiyi_id} -->|\"分派\"| {nid}")

        if bot_nodes:
            for _, nid, _ in bot_nodes:
                flow_lines.append(f"    {nid} -->|\"返回\"| {output_id}")

        if metadata:
            ts = metadata.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M"))
            flow_lines.append(
                f"    {taiyi_id} -.->|\"{ts}\"| {output_id}"
            )

        if metadata and "collaborations" in metadata:
            for col in metadata["collaborations"]:
                a_id = self._bot_to_id(col["from"], cfg)
                b_id = self._bot_to_id(col["to"], cfg)
                if a_id and b_id:
                    flow_lines.append(
                        f"    {a_id} -.->|\"{col.get('label', '协作')}\"| {b_id}"
                    )

        taiyi_class = taiyi_id
        bot_class = ",".join(info["id"] for info in bots.values())
        output_class = output_id

        mermaid = MERMAID_TEMPLATE_TITLE.format(
            title=title,
            subgraph_decls="\n".join(subgraph_lines),
            flow_lines="\n".join(flow_lines),
            taiyi_id=taiyi_class,
            bot_ids=bot_class,
            output_id=output_class,
        )

        return mermaid

    def generate_landscape(self) -> str:
        """生成完整系统全景拓扑。"""
        return '''---
title: 太一 Agent 系统全景拓扑
---
flowchart LR

    %% ===== 域 1: 旅游探路者 =====
    subgraph 旅游["🐾 旅游探路者"]
        direction TB
        taiyi_t("🧘 太一 · 旅游")
        zhiji_t["🧠 知几 · 情报"]
        shanmu_t["🏔️ 山木 · 规划"]
        suwen_t["📚 素问 · 研究"]
        wangliang_t["🔍 罔两 · 验证"]
        paoding_t["💰 庖丁 · 预算"]
    end

    %% ===== 域 2: 跨境贸易 =====
    subgraph 贸易["🌐 跨境贸易"]
        direction TB
        taiyi_tr("🧘 太一 · 贸易")
        zhiji_tr["🧠 知几 · 情报"]
        shanmu_tr["🏔️ 山木 · 执行"]
        suwen_tr["📚 素问 · 合规"]
        wangliang_tr["🔍 罔两 · 监控"]
        paoding_tr["💰 庖丁 · 风控"]
    end

    %% ===== 共享工具链 =====
    subgraph 工具["⚙️ 共享工具链"]
        direction TB
        search["🔎 搜索Agent v4"]
        verify["✅ 验证管道"]
        cache["💾 缓存 + 统计"]
    end

    %% ===== 跨域连接 =====
    taiyi_t -.->|共享| search
    taiyi_tr -.->|共享| search

%% 样式
classDef taiyi fill:#6366f1,color:#fff,stroke:#4338ca,stroke-width:2px,rx:8px
classDef bot fill:#22c55e,color:#fff,stroke:#16a34a,stroke-width:2px,rx:8px
classDef tool fill:#f59e0b,color:#fff,stroke:#d97706,stroke-width:1px,rx:4px
classDef output fill:#8b5cf6,color:#fff,stroke:#7c3aed,stroke-width:2px,rx:8px

class taiyi_t,taiyi_tr taiyi
class zhiji_t,shanmu_t,suwen_t,wangliang_t,paoding_t,zhiji_tr,shanmu_tr,suwen_tr,wangliang_tr,paoding_tr bot
class search,verify,cache tool
'''

    def _bot_emoji(self, name: str) -> str:
        return {"知几": "🧠", "山木": "🏔️", "素问": "📚",
                "罔两": "🔍", "庖丁": "💰"}.get(name, "🤖")

    def _bot_to_id(self, name: str, cfg: dict) -> Optional[str]:
        info = cfg["bots"].get(name)
        return info["id"] if info else None

    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        if task == "generate_topology":
            domain = kwargs.get("domain", "travel")
            active = kwargs.get("active_bots")
            desc = kwargs.get("task_description", "")
            meta = kwargs.get("metadata")
            mermaid = self.generate_topology(domain, active, desc, meta)
            return {"status": "success", "module": "dispatch-viz",
                    "task": task, "output": mermaid}
        elif task == "generate_landscape":
            mermaid = self.generate_landscape()
            return {"status": "success", "module": "dispatch-viz",
                    "task": task, "output": mermaid}
        else:
            return {"status": "error", "module": "dispatch-viz",
                    "task": task, "error": f"未知任务: {task}"}

    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "module": "dispatch-viz",
                "version": "1.0.0"}

    @property
    def name(self) -> str:
        return "dispatch-viz"

    @property
    def version(self) -> str:
        return "1.0.0"


# ─── CLI 入口 ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="调度拓扑可视化引擎")
    parser.add_argument("--domain", choices=["travel", "trade"],
                        default="travel", help="调度域")
    parser.add_argument("--bots", nargs="*", help="激活的 Bot 列表")
    parser.add_argument("--desc", default="", help="任务描述")
    parser.add_argument("--task", choices=["topology", "landscape"],
                        default="topology", help="输出类型")
    parser.add_argument("--output", "-o", help="输出文件路径")
    args = parser.parse_args()

    mod = DispatchVizModule()
    if args.task == "landscape":
        result = mod.execute("generate_landscape")
    else:
        result = mod.execute("generate_topology",
                             domain=args.domain,
                             active_bots=args.bots,
                             task_description=args.desc)

    output = result.get("output", "")
    if args.output:
        Path(args.output).write_text(output)
        print(f"✅ 已写入 {args.output}")
    else:
        print(output)
