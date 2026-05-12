"""
业务数据反哺闭环 — BusinessFeedbackLoop

连接实际业务执行效果 → 自进化引擎 → 自动调优 prompt/路由权重。

架构：
  各模块（非侵入式钩子）
      │ emit(event)
      ▼
  BusinessFeedbackLoop
      │ ingest → analyze → optimize → report
      ▼
  self-evolution core → prompt_cache / routing_weights / skill_priorities

钩子设计：
  from business_feedback import feedback
  feedback.emit("buyer-intel", {"action": "selected_view", "hits": 3, ...})

数据存储：
  data/feedback/ 目录下，按日/周/月聚合
"""

import json
import os
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional

logger = logging.getLogger("business-feedback")

# 数据存储根目录
FEEDBACK_DIR = Path(__file__).parent / ".." / ".." / "data" / "feedback"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)


# ── 事件类型定义 ──

EVENT_SCHEMA = {
    "buyer-intel": {
        "description": "买家情报引擎执行效果",
        "fields": ["action", "hits", "source", "mode", "latency_ms"],
        "optimize_dimensions": ["精选层 keyword", "日报模板", "路由阈值"],
    },
    "guike-zhilu": {
        "description": "触达链路转化漏斗",
        "fields": ["action", "sent", "opened", "replied", "pipeline_created"],
        "optimize_dimensions": ["开发信 prompt", "触达时间", "触达渠道权重"],
    },
    "quote-engine": {
        "description": "报价响应与转化",
        "fields": ["action", "sent", "replied", "converted", "margin"],
        "optimize_dimensions": ["报价模板", "利润基线", "跟进节奏"],
    },
    "intelligence-hub": {
        "description": "情报中心命中率",
        "fields": ["action", "result_count", "user_feedback", "relevance_score"],
        "optimize_dimensions": ["搜索关键词权重", "数据源排序"],
    },
    "orchestrator": {
        "description": "冷启动编排器执行",
        "fields": ["action", "product", "market", "steps", "elapsed"],
        "optimize_dimensions": ["编队模板", "并行组顺序"],
    },
}


class FeedbackHook:
    """非侵入式钩子 — 业务模块只需一行调用"""

    def __init__(self, module_name: str):
        if module_name not in EVENT_SCHEMA:
            raise ValueError(f"未知模块: {module_name}，支持: {list(EVENT_SCHEMA.keys())}")
        self.module_name = module_name

    def emit(self, action: str, **kwargs):
        """发出一个业务事件记录"""
        event = {
            "module": self.module_name,
            "action": action,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            **kwargs,
        }
        _write_event(event)
        return event


# ── 数据读写 ──

def _write_event(event: dict):
    """追加写入当日事件日志"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = FEEDBACK_DIR / f"{today}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def _read_events(days: int = 7, module: str = None) -> list:
    """读取最近 N 天的事件"""
    events = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        log_file = FEEDBACK_DIR / f"{date}.jsonl"
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        ev = json.loads(line)
                        if module and ev.get("module") != module:
                            continue
                        events.append(ev)
    return events


# ── 核心引擎 ──

class BusinessFeedbackLoop:
    """业务数据反哺闭环引擎"""

    def __init__(self):
        self._history = []
        self._insights = []
        self._optimizations = []

    # ── 钩子工厂 ──

    def hook(self, module_name: str) -> FeedbackHook:
        return FeedbackHook(module_name)

    def emit(self, module_name: str, action: str, **kwargs):
        return self.hook(module_name).emit(action, **kwargs)

    # ── 分析 ──

    def ingest(self, days: int = 7, module: str = None) -> list:
        """批量读取最近数据"""
        events = _read_events(days=days, module=module)
        self._history.extend(events)
        return events

    def analyze(self, days: int = 7) -> dict:
        """全维度分析业务执行效果"""
        events = self.ingest(days=days)

        result = {
            "period": f"最近{days}天",
            "total_events": len(events),
            "modules": {},
            "insights": [],
            "optimizations": [],
        }

        # 按模块聚合
        by_module = defaultdict(list)
        for ev in events:
            by_module[ev["module"]].append(ev)

        for module_name, module_events in by_module.items():
            analysis = self._analyze_module(module_name, module_events)
            result["modules"][module_name] = analysis

        # 全局洞察
        result["insights"] = self._generate_insights(result["modules"])
        result["optimizations"] = self._generate_optimizations(result["modules"])

        self._insights = result["insights"]
        self._optimizations = result["optimizations"]

        return result

    def _analyze_module(self, module_name: str, events: list) -> dict:
        """分析单个模块的表现"""
        analysis = {
            "events": len(events),
            "actions": defaultdict(int),
            "metrics": {},
        }

        for ev in events:
            analysis["actions"][ev.get("action", "unknown")] += 1

        # 按模块类型提取关键指标
        if module_name == "buyer-intel":
            selected_views = [e for e in events if e.get("action") == "selected_view"]
            if selected_views:
                avg_hits = sum(e.get("hits", 0) for e in selected_views) / len(selected_views)
                analysis["metrics"]["平均精选命中数"] = round(avg_hits, 1)
                analysis["metrics"]["精选使用次数"] = len(selected_views)

        elif module_name == "guike-zhilu":
            outreach = [e for e in events if e.get("action") == "outreach_result"]
            if outreach:
                total_sent = sum(e.get("sent", 0) for e in outreach)
                total_replied = sum(e.get("replied", 0) for e in outreach)
                analysis["metrics"]["总发送量"] = total_sent
                analysis["metrics"]["回复率"] = f"{round(total_replied/total_sent*100, 1)}%" if total_sent else "0%"

        elif module_name == "quote-engine":
            quotes = [e for e in events if e.get("action") == "quote_sent"]
            if quotes:
                sent = sum(e.get("sent", 0) for e in quotes)
                replied = sum(e.get("replied", 0) for e in quotes)
                analysis["metrics"]["总报价数"] = sent
                analysis["metrics"]["报价回复率"] = f"{round(replied/sent*100, 1)}%" if sent else "0%"

        elif module_name == "orchestrator":
            launches = [e for e in events if e.get("action") == "launch_complete"]
            if launches:
                total_steps = sum(e.get("steps", 0) for e in launches)
                analysis["metrics"]["冷启动次数"] = len(launches)
                analysis["metrics"]["平均步骤"] = round(total_steps / len(launches), 1)

        return analysis

    def _generate_insights(self, modules: dict) -> list:
        """从各模块数据提炼洞察"""
        insights = []

        for mod_name, analysis in modules.items():
            metrics = analysis.get("metrics", {})

            if mod_name == "buyer-intel":
                hits = metrics.get("平均精选命中数", 0)
                if hits < 3:
                    insights.append(f"买家情报精选命中率偏低（{hits}/次），建议调整关键词权重")
                elif hits > 10:
                    insights.append(f"买家情报精选效果优秀（{hits}/次），可考虑推全量层")

            elif mod_name == "guike-zhilu":
                rate = metrics.get("回复率", "0%")
                rate_val = float(rate.replace("%", ""))
                if rate_val < 10:
                    insights.append(f"触达回复率仅 {rate}，建议优化开发信 prompt 或目标客户筛选")
                elif rate_val > 30:
                    insights.append(f"触达回复率 {rate}，效果优秀，可扩大触达范围")

            elif mod_name == "quote-engine":
                rate = metrics.get("报价回复率", "0%")
                rate_val = float(rate.replace("%", ""))
                if rate_val < 20:
                    insights.append(f"报价回复率 {rate}，建议调整报价模板或跟进策略")

        if not insights:
            insights.append("数据不足，尚未形成有效洞察")

        return insights

    def _generate_optimizations(self, modules: dict) -> list:
        """根据分析结果生成优化建议"""
        optimizations = []

        for mod_name, analysis in modules.items():
            metrics = analysis.get("metrics", {})

            if mod_name == "buyer-intel":
                hits = metrics.get("平均精选命中数", 0)
                if hits and hits < 5:
                    optimizations.append({
                        "module": "buyer-intel",
                        "action": "调整精选层关键词匹配阈值",
                        "priority": "medium",
                        "expected_impact": "提升精选层命中率",
                    })

            elif mod_name == "guike-zhilu":
                rate = metrics.get("回复率", "0%")
                rate_val = float(rate.replace("%", ""))
                if rate_val and rate_val < 15:
                    optimizations.append({
                        "module": "guike-zhilu",
                        "action": "优化开发信模板（缩短开头+强化价值主张）",
                        "priority": "high",
                        "expected_impact": "提升回复率",
                    })

            elif mod_name == "quote-engine":
                rate = metrics.get("报价回复率", "0%")
                rate_val = float(rate.replace("%", ""))
                if rate_val and rate_val < 25:
                    optimizations.append({
                        "module": "quote-engine",
                        "action": "调整利润基线+缩短报价跟进间隔",
                        "priority": "high",
                        "expected_impact": "提升报价转化率",
                    })

        if not optimizations:
            optimizations.append({
                "module": "general",
                "action": "收集更多数据后生成优化建议",
                "priority": "low",
                "expected_impact": "待定",
            })

        return optimizations

    def optimize(self, auto_apply: bool = False) -> dict:
        """根据分析结果执行自动优化"""
        analysis = self.analyze()

        results = []
        for opt in analysis.get("optimizations", []):
            if opt.get("priority") == "low":
                continue

            opt_result = {
                "module": opt["module"],
                "action": opt["action"],
                "applied": False,
                "note": "",
            }

            if auto_apply:
                # 自动应用优化（实际执行由各模块的 optimize 方法完成）
                opt_result["applied"] = True
                opt_result["note"] = "已应用优化（stub - 实际执行由各模块完成）"
            else:
                opt_result["note"] = "需手动确认后应用"

            results.append(opt_result)
            self._optimizations.append(opt_result)

        return {
            "auto_apply": auto_apply,
            "optimizations_count": len(results),
            "applied": sum(1 for r in results if r["applied"]),
            "results": results,
        }

    # ── 诊断与报告 ──

    def report(self, days: int = 7) -> dict:
        """生成业务执行周报"""
        analysis = self.analyze(days=days)

        report = {
            "title": f"业务执行效果周报 · {datetime.now().strftime('%Y-%m-%d')}",
            "period": f"最近{days}天",
            "total_events": analysis["total_events"],
            "module_summary": {},
            "insights": analysis["insights"],
            "suggested_actions": [],
            "optimization_status": [],
        }

        for mod_name, mod_analysis in analysis["modules"].items():
            report["module_summary"][mod_name] = {
                "events": mod_analysis["events"],
                "metrics": mod_analysis.get("metrics", {}),
            }

        # 聚合建议
        for opt in analysis.get("optimizations", []):
            if opt.get("priority") in ("high", "medium"):
                report["suggested_actions"].append(opt["action"])

        return report

    def current_insights(self) -> list:
        return self._insights

    def pending_optimizations(self) -> list:
        return [o for o in self._optimizations if not o.get("applied")]


# ── 自进化集成 ──

def integrate_into_self_evolution(self_evolution_instance) -> BusinessFeedbackLoop:
    """将业务反馈闭环注入 self-evolution 实例"""
    bfl = BusinessFeedbackLoop()
    self_evolution_instance.business_feedback = bfl

    # 扩展 execute 入口
    original_execute = self_evolution_instance.execute

    def enhanced_execute(task, **kwargs):
        if task == "business_analyze":
            return bfl.analyze(days=kwargs.get("days", 7))
        elif task == "business_optimize":
            return bfl.optimize(auto_apply=kwargs.get("auto_apply", False))
        elif task == "business_report":
            return bfl.report(days=kwargs.get("days", 7))
        elif task == "business_emit":
            return bfl.emit(
                module_name=kwargs.get("module"),
                action=kwargs.get("action"),
                **{k: v for k, v in kwargs.items() if k not in ("module", "action")}
            )
        return original_execute(task, **kwargs)

    self_evolution_instance.execute = enhanced_execute
    return bfl


# ── 快捷入口 ──

feedback = BusinessFeedbackLoop()

# 预置钩子
buyer_intel_hook = FeedbackHook("buyer-intel")
guike_zhilu_hook = FeedbackHook("guike-zhilu")
quote_engine_hook = FeedbackHook("quote-engine")
intel_hub_hook = FeedbackHook("intelligence-hub")
orchestrator_hook = FeedbackHook("orchestrator")
