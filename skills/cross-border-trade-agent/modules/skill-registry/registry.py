"""
太一 Skill Registry — 动态发现、注册、查询、延迟加载

基于 SKILL-REGISTRY.md 和 skill-manifest.schema.json 提供的标准，
扫描 modules/ 和 agents/ 目录发现所有 Skill，支持按 Owner/触发词/依赖 筛选。
"""

import json
import os
import re
from pathlib import Path
from typing import Optional

SKILL_BASE = Path(__file__).parent.parent  # cross-border-trade-agent/
REGISTRY_FILE = SKILL_BASE / "SKILL-REGISTRY.md"
SCHEMA_FILE = SKILL_BASE / "skill-manifest.schema.json"

# 内置注册表（从 SKILL-REGISTRY.md 解析的静态快照）
# 完整注册表在 SKILL-REGISTRY.md 中维护，此处提供编程查询接口
_BUILTIN_REGISTRY = {
    # 知几
    "intelligence-hub.market-analysis": {
        "name": "市场分析", "owner": "知几",
        "triggers": ["市场分析", "市场机会", "趋势"],
        "execution_mode": "async", "cost_estimate": "medium",
        "entry_point": "modules/intelligence-hub/core.py",
    },
    "intelligence-hub.competitor-monitor": {
        "name": "竞品监控", "owner": "知几",
        "triggers": ["竞品", "对手", "monitor"],
        "execution_mode": "async", "cost_estimate": "high",
        "entry_point": "modules/intelligence-hub/competitor_monitor.py",
    },
    "intelligence-hub.product-scoring": {
        "name": "选品评分", "owner": "知几",
        "triggers": ["选品", "评分", "产品机会"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "intelligence-hub.trend-analysis": {
        "name": "趋势预测", "owner": "知几",
        "triggers": ["趋势", "预测", "方向"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "intelligence-hub.bidding-radar": {
        "name": "招标雷达", "owner": "知几",
        "triggers": ["招标", "采购", "RFQ"],
        "execution_mode": "async", "cost_estimate": "medium",
    },
    "intelligence-hub.policy-radar": {
        "name": "政策监控", "owner": "知几",
        "triggers": ["政策", "关税", "法规变动"],
        "execution_mode": "async", "cost_estimate": "medium",
    },
    "buyer-intel.selected": {
        "name": "买家情报·精选", "owner": "知几",
        "triggers": ["买家", "项目", "采购机会"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/buyer-intel/core.py",
    },
    "buyer-intel.daily": {
        "name": "买家情报·日报", "owner": "知几",
        "triggers": ["日报", "雷达"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/buyer-intel/rss_feed.py",
    },
    "buyer-intel.full": {
        "name": "买家情报·全量", "owner": "知几",
        "triggers": ["全部", "全量", "所有"],
        "execution_mode": "sync", "cost_estimate": "medium",
    },
    "geo-outbound.market-analysis": {
        "name": "GEO 市场分析", "owner": "知几",
        "triggers": ["GEO", "市场分析"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/geo-outbound/core.py",
    },
    "data-integrator.multi-source": {
        "name": "多源数据整合", "owner": "知几",
        "triggers": ["数据整合", "数据源"],
        "execution_mode": "sync", "cost_estimate": "medium",
        "entry_point": "modules/data-integrator/core.py",
    },
    "report-engine.report": {
        "name": "智能报告生成", "owner": "知几",
        "triggers": ["报告", "简报", "分析报告"],
        "execution_mode": "async", "cost_estimate": "medium",
        "entry_point": "modules/report-engine/core.py",
    },
    # 山木
    "guike-zhilu.search-outreach": {
        "name": "搜索+触达", "owner": "山木",
        "triggers": ["找买家", "触达", "开发信"],
        "execution_mode": "async", "cost_estimate": "high",
        "entry_point": "modules/guike-zhilu/full_pipeline.py",
    },
    "guike-zhilu.outreach": {
        "name": "主动触达", "owner": "山木",
        "triggers": ["开发信", "联系", "outreach"],
        "execution_mode": "async", "cost_estimate": "medium",
    },
    "guike-zhilu.nurture": {
        "name": "线索培育", "owner": "山木",
        "triggers": ["培育", "跟进", "维护"],
        "execution_mode": "async", "cost_estimate": "medium",
    },
    "supply-chain.optimize": {
        "name": "供应链优化", "owner": "山木",
        "triggers": ["供应链", "物流", "库存"],
        "execution_mode": "async", "cost_estimate": "medium",
        "entry_point": "modules/supply-chain/core.py",
    },
    "transaction-support.fulfill": {
        "name": "订单履约", "owner": "山木",
        "triggers": ["履约", "发货", "订单"],
        "execution_mode": "async", "cost_estimate": "medium",
    },
    "transaction-support.localization": {
        "name": "多语言内容", "owner": "山木",
        "triggers": ["本地化", "翻译", "多语言"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "cultural-adapter.content": {
        "name": "跨文化适配", "owner": "山木",
        "triggers": ["文化适配", "本地化"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/cultural-adapter/core.py",
    },
    # 素问
    "compliance-engine.vat-check": {
        "name": "VAT/退税查询", "owner": "素问",
        "triggers": ["退税", "HS", "合规"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/compliance-engine/core.py",
    },
    "compliance-engine.regulation": {
        "name": "法规追踪", "owner": "素问",
        "triggers": ["法规", "合规变动"],
        "execution_mode": "async", "cost_estimate": "medium",
    },
    "compliance-engine.customs": {
        "name": "清关自动化", "owner": "素问",
        "triggers": ["清关", "海关", "关税"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "contract-legal.generate": {
        "name": "合同生成", "owner": "素问",
        "triggers": ["合同", "协议", "条款"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/contract-legal/core.py",
    },
    "contract-legal.review": {
        "name": "法律审查", "owner": "素问",
        "triggers": ["审查", "法律风险"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "cultural-adapter.compliance": {
        "name": "跨文化合规", "owner": "素问",
        "triggers": ["文化合规", "习俗"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "product-catalog.match": {
        "name": "产品目录匹配", "owner": "素问",
        "triggers": ["产品匹配", "目录"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    # 罔两
    "company-enricher.verify": {
        "name": "公司验证", "owner": "罔两",
        "triggers": ["验证", "查公司", "靠谱吗"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/company-enricher/core.py",
    },
    "company-enricher.enrich": {
        "name": "信息富化", "owner": "罔两",
        "triggers": ["富化", "详情", "增强"],
        "execution_mode": "async", "cost_estimate": "medium",
    },
    "real-data-verifier.five-way": {
        "name": "五项验证", "owner": "罔两",
        "triggers": ["验证", "查真伪"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/real-data-verifier/core.py",
    },
    "intelligence-hub.competitor-list": {
        "name": "竞品列表", "owner": "罔两",
        "triggers": ["竞品列表", "谁在做"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "intelligence-hub.platform-monitor": {
        "name": "平台监控", "owner": "罔两",
        "triggers": ["平台监控", "价格监控"],
        "execution_mode": "async", "cost_estimate": "high",
    },
    # 庖丁
    "quote-engine.calculate": {
        "name": "报价计算", "owner": "庖丁",
        "triggers": ["报价", "成本", "核算"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/quote-engine/core.py",
    },
    "quote-engine.profit-analysis": {
        "name": "利润分析", "owner": "庖丁",
        "triggers": ["利润", "盈利"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "payment-settlement.channel": {
        "name": "支付通道", "owner": "庖丁",
        "triggers": ["支付", "收款", "结算"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/payment-settlement/core.py",
    },
    "payment-settlement.forex": {
        "name": "汇率管理", "owner": "庖丁",
        "triggers": ["汇率", "换汇"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "risk-manager.identify": {
        "name": "风险识别", "owner": "庖丁",
        "triggers": ["风险", "预警"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/risk-manager/core.py",
    },
    "risk-manager.hedge": {
        "name": "对冲策略", "owner": "庖丁",
        "triggers": ["对冲", "规避风险"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    "supplier-matcher.match": {
        "name": "供应商匹配", "owner": "庖丁",
        "triggers": ["供应商", "工厂", "找厂家"],
        "execution_mode": "sync", "cost_estimate": "low",
    },
    # 太一
    "cross-border-core.route": {
        "name": "意图路由", "owner": "太一",
        "triggers": ["路由", "调度"],
        "execution_mode": "sync", "cost_estimate": "low",
        "entry_point": "modules/cross-border-core/core.py",
    },
    "cross-border-core.squad": {
        "name": "动态编队", "owner": "太一",
        "triggers": ["squad", "编队"],
        "execution_mode": "async", "cost_estimate": "high",
        "entry_point": "modules/cross-border-core/squad_orchestrator.py",
    },
    "task-scheduler.jobs": {
        "name": "定时任务", "owner": "太一",
        "triggers": ["定时", "自动", "监控"],
        "execution_mode": "async", "cost_estimate": "low",
        "entry_point": "modules/task-scheduler/core.py",
    },
    "self-evolution.heal": {
        "name": "自愈", "owner": "太一",
        "triggers": ["自愈", "修复"],
        "execution_mode": "async", "cost_estimate": "low",
        "entry_point": "modules/self-evolution/core.py",
    },
    "self-evolution.crystallize": {
        "name": "技能结晶", "owner": "太一",
        "triggers": ["结晶", "固化"],
        "execution_mode": "async", "cost_estimate": "low",
    },
    "self-evolution.optimize": {
        "name": "Token 优化", "owner": "太一",
        "triggers": ["优化", "压缩"],
        "execution_mode": "async", "cost_estimate": "low",
    },
    "orchestrator.launch": {
        "name": "冷启动编排", "owner": "太一",
        "triggers": ["启动", "推入", "冷启动"],
        "execution_mode": "async", "cost_estimate": "high",
        "entry_point": "modules/orchestrator/launch_engine.py",
    },
    "orchestrator.diagnose": {
        "name": "运营诊断", "owner": "太一",
        "triggers": ["诊断", "分析", "评估"],
        "execution_mode": "async", "cost_estimate": "medium",
        "entry_point": "modules/orchestrator/launch_engine.py",
    },
}


class SkillRegistry:
    """动态 Skill 注册表 — 查询 + 延迟加载"""

    def __init__(self, registry: Optional[dict] = None):
        self._registry = registry or _BUILTIN_REGISTRY

    # ── 查询 ──

    def all(self) -> dict:
        return dict(self._registry)

    def search(self, owner: str = None, trigger: str = None,
               dependency: str = None, mode: str = None) -> list:
        results = []
        for skill_id, info in self._registry.items():
            if owner and info.get("owner") != owner:
                continue
            if trigger and not any(t in info.get("triggers", [])
                                   for t in [trigger, trigger.lower()]):
                continue
            if mode and info.get("execution_mode") != mode:
                continue
            if dependency and dependency not in info.get("dependencies", []):
                continue
            results.append({"id": skill_id, **info})
        return results

    def get(self, skill_id: str) -> dict:
        return self._registry.get(skill_id)

    def detect_triggers(self, text: str) -> list:
        """从自然语言文本中匹配触发词，返回匹配的 Skill 列表"""
        results = []
        for skill_id, info in self._registry.items():
            for trigger in info.get("triggers", []):
                if trigger in text:
                    results.append({"id": skill_id, **info})
                    break
        return results

    # ── 加载执行（入口） ──

    def load(self, skill_id: str):
        """返回 Skill 执行器的桩位（延迟加载模式）"""
        info = self._registry.get(skill_id)
        if not info:
            raise KeyError(f"Skill '{skill_id}' not registered")
        return SkillExecutor(skill_id, info)

    # ── 注册管理 ──

    def register(self, skill_id: str, manifest: dict):
        """运行时注册新 Skill"""
        self._registry[skill_id] = manifest

    def count_by_owner(self) -> dict:
        counts = {}
        for info in self._registry.values():
            owner = info.get("owner", "未知")
            counts[owner] = counts.get(owner, 0) + 1
        return counts


class SkillExecutor:
    """Skill 执行器桩 — 按需导入 + 执行"""

    def __init__(self, skill_id: str, manifest: dict):
        self.id = skill_id
        self.manifest = manifest
        self._module = None

    def execute(self, params: dict = None, **kwargs):
        """执行 Skill（延迟加载模式，参数由继承类实际实现）"""
        entry = self.manifest.get("entry_point")
        if entry:
            return {"status": "deferred", "skill_id": self.id,
                    "entry": entry, "params": params or kwargs}
        return {"status": "stub", "skill_id": self.id,
                "note": f"执行器桩 — {self.manifest.get('name', self.id)}",
                "params": params or kwargs}

    def __repr__(self):
        return f"<SkillExecutor: {self.id} ({self.manifest.get('name', '?')})>"


# ── 快速入口 ──

_registry_instance = None


def get_registry() -> SkillRegistry:
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = SkillRegistry()
    return _registry_instance


def find(text: str) -> list:
    """快捷查询：从文本匹配 Skill"""
    return get_registry().detect_triggers(text)


def load(skill_id: str) -> SkillExecutor:
    """快捷加载"""
    return get_registry().load(skill_id)
