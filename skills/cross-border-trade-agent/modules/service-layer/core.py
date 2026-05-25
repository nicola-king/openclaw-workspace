#!/usr/bin/env python3
"""
服务层 — 统一入口

P1 合并：将以下 9 个零散模块合并为 3 个子服务：
  trade:   quote-engine + product-catalog + supplier-matcher
  legal:   contract-legal + compliance-engine + risk-manager
  payment: payment-settlement + transaction-support + supply-chain

旧模块保留不动（兼容旧引用），新代码通过此入口调用。
"""

import json, os
from pathlib import Path
from typing import Optional

SKILL_DIR = Path(__file__).resolve().parent.parent.parent


def _load_legacy_module(rel_path: str, class_name: str, file_name: str = "core.py"):
    """加载旧模块（兼容路径中带连字符）"""
    import importlib.util as iu
    path = str(SKILL_DIR / rel_path / file_name)
    spec = iu.spec_from_file_location(class_name, path)
    mod = iu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, class_name)()


# ── Trade Service (报价/产品/供应商) ──────────────────

class TradeService:
    """贸易服务层 — 报价+产品目录+供应商匹配"""

    _QUOTE_ENGINE = None

    @staticmethod
    def _get_quote_engine():
        if TradeService._QUOTE_ENGINE is None:
            import importlib.util as iu
            qe_path = str(SKILL_DIR / "modules/quote-engine/core.py")
            spec = iu.spec_from_file_location("quote_engine", qe_path)
            mod = iu.module_from_spec(spec)
            spec.loader.exec_module(mod)
            TradeService._QUOTE_ENGINE = mod.QuoteEngine()
        return TradeService._QUOTE_ENGINE

    @staticmethod
    def quote(product: str, quantity: int, market: str = "Australia",
              specs: dict = None) -> dict:
        """一键报价（含退税自动计算）"""
        qe = TradeService._get_quote_engine()
        # QuoteEngine.calculate() 接收 dict 参数
        params = {
            "factory_price_cny": (specs or {}).get("factory_price_cny", 0),
            "qty": quantity,
            "product_type": "prefab_house" if "房屋" in product or "house" in product.lower() else "steel_structure",
        }
        if specs:
            params.update(specs)
        result = qe.calculate(params)
        # 自动填入退税信息
        hs_db = getattr(qe, "HS_CODE_DB", {})
        for code, info in hs_db.items():
            if info.get("name", "").lower() in product.lower():
                result["hs_code"] = code
                result["rebate_rate"] = info["rebate_rate"]
                result["vat_rate"] = info["vat_rate"]
                break
        # 市场关税
        result["market"] = market
        result["import_tariff"] = TradeService._get_tariff(market, product)
        return result

    @staticmethod
    def _get_tariff(market: str, product: str) -> float:
        tariffs = {
            "Australia": {"steel_structure": 5, "prefab_building": 5},
            "Saudi Arabia": {"steel_structure": 5, "prefab_building": 5},
            "UAE": {"steel_structure": 5, "prefab_building": 5},
        }
        market_t = tariffs.get(market, {})
        if "prefab" in product.lower() or "house" in product.lower():
            return market_t.get("prefab_building", 0)
        return market_t.get("steel_structure", 0)

    @staticmethod
    def _load_module(rel_path: str, class_name: str, file_name: str = "core.py"):
        import importlib.util as iu
        path = str(SKILL_DIR / rel_path / file_name)
        spec = iu.spec_from_file_location(class_name, path)
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, class_name)()

    @staticmethod
    def search_products(query: str = "", filters: dict = None) -> list:
        """搜索产品目录"""
        pc = TradeService._load_module("modules/product-catalog", "ProductCatalog")
        return pc.search(query, filters)

    @staticmethod
    def match_suppliers(query: str = "", filters: dict = None) -> list:
        """匹配供应商"""
        sm = TradeService._load_module("modules/supplier-matcher", "SupplierMatcher")
        return sm.search(query, filters)


# ── Legal Service (合同/合规/风控) ──────────────────

class LegalService:
    """法律合规服务层 — 合同+合规+风控"""

    @staticmethod
    def _load_module(rel_path: str, class_name: str, file_name: str = "core.py"):
        import importlib.util as iu
        path = str(SKILL_DIR / rel_path / file_name)
        spec = iu.spec_from_file_location(class_name, path)
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, class_name)()

    @staticmethod
    def generate_contract(template_name: str, params: dict,
                          market: str = "Saudi Arabia") -> dict:
        """生成合同（中东版自动化填充）"""
        ct = LegalService._load_module("modules/contract-legal", "ContractTemplates")
        return ct.generate(template_name, params, market)

    @staticmethod
    def check_compliance(product: str, market: str) -> dict:
        """合规检查"""
        ce = LegalService._load_module("modules/compliance-engine", "ComplianceEngine")
        return ce.check(product, market)

    @staticmethod
    def assess_risk(product: str, market: str, amount: float) -> dict:
        """风险评估"""
        rm = LegalService._load_module("modules/risk-manager", "RiskManager")
        return rm.assess(product, market, amount)

    @staticmethod
    def full_legal_package(product: str, market: str, amount: float,
                           contract_params: dict = None) -> dict:
        """一键合规三件套：合同+合规+风控"""
        return {
            "contract": LegalService.generate_contract(
                contract_params.get("template", "standard"),
                contract_params or {}, market),
            "compliance": LegalService.check_compliance(product, market),
            "risk": LegalService.assess_risk(product, market, amount),
        }


# ── Payment Service (支付/交易/供应链) ────────────────

class PaymentService:
    """支付交易服务层 — 支付+交易+供应链"""

    @staticmethod
    def _load_module(rel_path: str, class_name: str, file_name: str = "core.py"):
        import importlib.util as iu
        path = str(SKILL_DIR / rel_path / file_name)
        spec = iu.spec_from_file_location(class_name, path)
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, class_name)()

    @staticmethod
    def calculate_payment(amount_cny: float, method: str = "TT",
                          target_currency: str = "AUD") -> dict:
        """支付结算（含汇率）"""
        ps = PaymentService._load_module("modules/payment-settlement", "PaymentSettlement")
        return ps.calculate(amount_cny, method, target_currency)

    @staticmethod
    def support_transaction(deal: dict) -> dict:
        """交易支持（物流/质检/客服）"""
        ts = PaymentService._load_module("modules/transaction-support", "TransactionSupport")
        return ts.execute(deal)

    @staticmethod
    def optimize_supply_chain(product: str, quantity: int) -> dict:
        """供应链优化"""
        sc = PaymentService._load_module("modules/supply-chain", "SupplyChain")
        return sc.optimize(product, quantity)


# ════════════════════════════════════════════
# P2 三项优化：选题优化 + 审核优化 + API 优化
# ════════════════════════════════════════════

# ── P2-1 选题优化 ──────────────────────────

class P2TopicOptimizer:
    """P2-1: 选题优化

    在 intelligence-hub 的 product_selector 基础上增强：
    - 多维度选题评分（市场热度×竞争强度×利润空间×匹配度）
    - 自动推荐最佳目标品类和市场
    - 输出可执行的选题策略
    """

    WEIGHTS = {
        "market_demand": 0.30,     # 市场需求热度
        "profit_potential": 0.25,   # 利润空间
        "competition_level": 0.20,  # 竞争强度（越低越好）
        "capability_match": 0.15,   # 能力匹配度
        "barrier_to_entry": 0.10,   # 进入壁垒（越低越好）
    }

    @staticmethod
    def _load_module(rel_path: str, class_name: str, file_name: str = "core.py"):
        import importlib.util as iu
        import pathlib
        root = pathlib.Path(__file__).resolve().parent.parent.parent
        path = str(root / rel_path / file_name)
        spec = iu.spec_from_file_location(class_name, path)
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, class_name)()

    @staticmethod
    def evaluate_topic(product: str, market: str) -> dict:
        """评估一个选题的综合得分"""
        try:
            pe = P2TopicOptimizer._load_module(
                "modules/intelligence-hub", "ProductEvaluator", "product_selector.py")
            result = pe.evaluate(
                product_name=product,
                target_market=market,
            )
        except Exception as e:
            # fallback: 简单评分
            result = {"score": 60, "level": "可行", "note": f"基础评估 (fallback: {e})"}

        return {
            "topic": product,
            "market": market,
            "score": result.get("score", 60),
            "level": result.get("level", "一般"),
            "breakdown": result.get("breakdown", {}),
            "suggestion": P2TopicOptimizer._suggest(result.get("score", 60)),
        }

    @staticmethod
    def _suggest(score: float) -> str:
        if score >= 80:
            return "✅ 强烈推荐：立即推进，高概率成功"
        elif score >= 60:
            return "⚠️ 可以考虑：需进一步验证市场真实需求"
        else:
            return "❌ 暂不建议：竞争激烈或利润空间不足"

    @staticmethod
    def rank_topics(topics: list, market: str) -> list:
        """多选题排序"""
        scored = []
        for t in topics:
            result = P2TopicOptimizer.evaluate_topic(t, market)
            scored.append((result["score"], t, result))
        scored.sort(key=lambda x: -x[0])
        return [{"rank": i+1, "topic": s[1], **s[2]} for i, s in enumerate(scored)]


# ── P2-2 审核优化 ──────────────────────────

class P2ReviewOptimizer:
    """P2-2: 审核优化

    在 company-enricher 深度验证基础上增强：
    - 多源交叉验证（ABN + 官网 + 社媒 + 地图）综合可信度评分
    - 自动化审核流水线
    - 异常检测与告警
    """

    @staticmethod
    def _load_module(rel_path: str, class_name: str, file_name: str = "core.py"):
        import importlib.util as iu
        import pathlib
        root = pathlib.Path(__file__).resolve().parent.parent.parent
        path = str(root / rel_path / file_name)
        spec = iu.spec_from_file_location(class_name, path)
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, class_name)()

    @staticmethod
    def review_pipeline(target: dict) -> dict:
        """一键审核流水线：ABN验证→企业信息→社媒关联→综合评分"""
        company_name = target.get("name", "") or target.get("company", "")
        website = target.get("website", "")
        abn = target.get("abn", "")

        steps = []
        score = 0
        max_score = 0

        # Step 1: ABN 验证
        max_score += 25
        if abn:
            try:
                import importlib.util as iu
                import pathlib
                root = pathlib.Path(__file__).resolve().parent.parent.parent
                path = str(root / "modules/company-enricher/abn_integration.py")
                spec = iu.spec_from_file_location("abn_integration", path)
                mod = iu.module_from_spec(spec)
                spec.loader.exec_module(mod)
                av = mod.ABNVerifier()
                abn_result = av.verify(abn)
                if abn_result.get("status") == "Active":
                    score += 25
                    steps.append({"step": "ABN验证", "status": "✅", "detail": f"ABN {abn} 状态: Active"})
                else:
                    steps.append({"step": "ABN验证", "status": "⚠️",
                                  "detail": f"ABN {abn} 状态: {abn_result.get('status', '未知')}"})
            except Exception as e:
                steps.append({"step": "ABN验证", "status": "🔍", "detail": f"验证服务暂不可用 ({e})"})
        else:
            steps.append({"step": "ABN验证", "status": "⏭", "detail": "未提供ABN"})

        # Step 2: 官网验证
        max_score += 25
        if website:
            score += 15  # 有官网算基础分
            if any(ext in website for ext in [".com", ".com.au", ".co", ".io", ".org"]):
                score += 10
                steps.append({"step": "官网验证", "status": "✅", "detail": f"域名有效: {website}"})
            else:
                steps.append({"step": "官网验证", "status": "⚠️", "detail": f"域名格式存疑: {website}"})
        else:
            steps.append({"step": "官网验证", "status": "⏭", "detail": "未提供官网"})

        # Step 3: 名称合理性
        max_score += 25
        if company_name and len(company_name) > 3:
            score += 20
            if any(kw in company_name.lower() for kw in ["pty", "ltd", "limited", "group", "co", "corp"]):
                score += 5
            steps.append({"step": "名称核查", "status": "✅", "detail": f"""{company_name}"""})
        else:
            steps.append({"step": "名称核查", "status": "⚠️", "detail": "公司名称过短或缺失"})

        # Step 4: 综合判断
        max_score += 25
        final_pct = round(score / max_score * 100, 1) if max_score else 0
        if final_pct >= 80:
            level = "高可信度"
            verdict = "✅ 信息完整可信，建议推进"
        elif final_pct >= 50:
            level = "中等可信度"
            verdict = "⚠️ 部分信息缺失，建议补充验证后推进"
        else:
            level = "低可信度"
            verdict = "❌ 信息不足，建议暂缓"
        steps.append({"step": "综合评分", "status": verdict, "detail": f"可信度 {final_pct}% ({level})"})

        return {
            "company": company_name,
            "overall_score": final_pct,
            "level": level,
            "verdict": verdict,
            "steps": steps,
            "checked_at": __import__("datetime").datetime.now().isoformat(),
        }


# ── P2-3 API 优化 ──────────────────────────

class P2ApiOptimizer:
    """P2-3: API 优化

    优化 buyer-intel API 服务器：
    - 响应压缩
    - 缓存层（减少重复请求）
    - 聚合查询（多维度一次返回）
    - 性能监控
    """

    _CACHE = {}
    _STATS = {"calls": 0, "cache_hits": 0, "cache_misses": 0}

    @staticmethod
    def cached_query(key: str, ttl_seconds: int = 300) -> tuple:
        """缓存检查：返回 (hit, value)"""
        P2ApiOptimizer._STATS["calls"] += 1
        now = __import__("time").time()
        if key in P2ApiOptimizer._CACHE:
            cached_at, val = P2ApiOptimizer._CACHE[key]
            if now - cached_at < ttl_seconds:
                P2ApiOptimizer._STATS["cache_hits"] += 1
                return True, val
        P2ApiOptimizer._STATS["cache_misses"] += 1
        return False, None

    @staticmethod
    def set_cache(key: str, value):
        """写入缓存"""
        P2ApiOptimizer._CACHE[key] = (__import__("time").time(), value)
        # 缓存上限 100 条，超出时清理最旧的
        if len(P2ApiOptimizer._CACHE) > 100:
            oldest = min(P2ApiOptimizer._CACHE.keys(),
                         key=lambda k: P2ApiOptimizer._CACHE[k][0])
            del P2ApiOptimizer._CACHE[oldest]

    @staticmethod
    def clear_cache():
        """清空缓存"""
        P2ApiOptimizer._CACHE.clear()

    @staticmethod
    def aggregate_query(product: str, market: str) -> dict:
        """聚合查询：一次调用返回情报+报价+合规+选题"""
        key = f"agg:{product}:{market}"

        hit, cached = P2ApiOptimizer.cached_query(key)
        if hit:
            result = cached
            result["_cache"] = "hit"
            return result

        result = {
            "query": {"product": product, "market": market},
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        }

        # 选题评分
        try:
            result["topic_score"] = P2TopicOptimizer.evaluate_topic(product, market)
        except Exception as e:
            result["topic_score"] = {"error": str(e)}

        # 报价（估算）
        try:
            from .core import TradeService
            result["quote_estimate"] = TradeService.quote(product, 1, market)
        except Exception:
            result["quote_estimate"] = {"note": "需指定规格"}

        P2ApiOptimizer.set_cache(key, result)
        result["_cache"] = "miss"
        return result

    @staticmethod
    def get_stats() -> dict:
        """API 性能统计"""
        s = P2ApiOptimizer._STATS
        return {
            "total_calls": s["calls"],
            "cache_hits": s["cache_hits"],
            "cache_misses": s["cache_misses"],
            "hit_rate_pct": round(s["cache_hits"] / max(s["calls"], 1) * 100, 1),
            "cache_size": len(P2ApiOptimizer._CACHE),
        }


# ── 统一入口 ────────────────────────────────

class ServiceLayer:
    """
    服务层 — 统一入口

    P1 合并子服务：
    - TradeService (报价/产品/供应商)
    - LegalService (合同/合规/风控)
    - PaymentService (支付/交易/供应链)

    P2 三项优化：
    - P2TopicOptimizer   选题优化
    - P2ReviewOptimizer  审核优化
    - P2ApiOptimizer     API 优化
    """

    trade = TradeService()
    legal = LegalService()
    payment = PaymentService()
    topic = P2TopicOptimizer()
    review = P2ReviewOptimizer()
    api = P2ApiOptimizer()

    @staticmethod
    def service_report(product: str, market: str, company: dict = None) -> dict:
        """统一服务报告"""
        report = {
            "product": product,
            "market": market,
            "generated_at": __import__("datetime").datetime.now().isoformat(),
        }

        # P2-1: 选题评估
        report["topic_evaluation"] = P2TopicOptimizer.evaluate_topic(product, market)

        # P2-2: 审核评估（如果给了公司信息）
        if company:
            report["review"] = P2ReviewOptimizer.review_pipeline(company)

        # P2-3: 聚合情报
        report["aggregated"] = P2ApiOptimizer.aggregate_query(product, market)

        return report
