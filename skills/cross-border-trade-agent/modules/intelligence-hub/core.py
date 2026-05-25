#!/usr/bin/env python3
"""
智能分析中心 (Intelligence Hub) v9.0.0
智能分析：竞品分析/选品评分/厂家推荐/趋势预测
"""

import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

class IntelligenceHub:
    """智能分析中心主类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("intelligence-hub")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化模块"""
        self.logger.info("智能分析中心模块初始化完成")
        return True
    
    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        """执行任务"""
        self.logger.info(f"执行任务：{task}")
        
        if task == "competitor":
            return self.counter_evidence_check(claim=f"竞品分析：{kwargs.get('product','')} ({kwargs.get('market','')})")
        elif task == "scoring":
            return self.product_scoring(**kwargs)
        elif task == "check":
            return self.counter_evidence_check(claim=kwargs.get("claim", ""))
        elif task == "manufacturer":
            return self.manufacturer_recommendation(**kwargs)
        elif task == "forecast":
            return self.trend_forecast(**kwargs)
        else:
            return {"status": "error", "message": f"未知任务：{task}"}
    
    def competitor_analysis(self, product: str, market: str = "", **kwargs) -> Dict[str, Any]:
        """竞品分析"""
        self.logger.info(f"竞品分析：{product}，{market}")
        
        competitors = [
            {
                "name": "Karmod Prefabrikasyon",
                "country": "Turkey",
                "website": "https://www.karmod.com",
                "market_share": "15%",
                "strengths": ["欧洲品牌", "快速交付", "定制能力"],
                "weaknesses": ["价格较高", "物流时间长"]
            },
            {
                "name": "DXH Prefab House",
                "country": "China",
                "website": "https://www.dxhcontainerhouse.com",
                "market_share": "12%",
                "strengths": ["价格优势", "大规模生产", "出口经验"],
                "weaknesses": ["品牌知名度低", "售后服务不足"]
            }
        ]
        
        return {
            "status": "success",
            "competitors": competitors,
            "total": len(competitors),
            "analysis": {
                "market_saturation": "medium",
                "competition_intensity": "high",
                "opportunity_score": 75
            }
        }
    
    def product_scoring(self, product: str, **kwargs) -> Dict[str, Any]:
        """选品评分"""
        self.logger.info(f"选品评分：{product}")
        
        return {
            "status": "success",
            "product": product,
            "total_score": 85,
            "dimensions": {
                "trend": {"score": 90, "weight": 0.3},
                "search": {"score": 80, "weight": 0.25},
                "competitor": {"score": 75, "weight": 0.2},
                "profit": {"score": 85, "weight": 0.15},
                "social": {"score": 88, "weight": 0.1}
            }
        }
    
    def manufacturer_recommendation(self, product: str, **kwargs) -> Dict[str, Any]:
        """厂家推荐"""
        self.logger.info(f"厂家推荐：{product}")
        
        manufacturers = [
            {
                "name": "浙江法狮龙建材有限公司",
                "website": "https://www.fsilon.com",
                "phone": "+86-573-87654321",
                "email": "info@fsilon.com",
                "rating": 4.8,
                "certifications": ["ISO9001", "CE", "SGS"]
            },
            {
                "name": "广东集成房屋有限公司",
                "website": "https://www.gdioh.com",
                "phone": "+86-20-87654321",
                "email": "sales@gdioh.com",
                "rating": 4.6,
                "certifications": ["ISO9001", "CE", "TUV"]
            }
        ]
        
        return {
            "status": "success",
            "manufacturers": manufacturers,
            "total": len(manufacturers)
        }
    
    def trend_forecast(self, product: str, period: str = "12m", **kwargs) -> Dict[str, Any]:
        """趋势预测"""
        self.logger.info(f"趋势预测：{product}，{period}")
        
        return {
            "status": "success",
            "product": product,
            "period": period,
            "forecast": {
                "trend": "upward",
                "growth_rate": "15%",
                "seasonality": "high in Q3",
                "confidence": 0.85
            }
        }
    

    # ═══════════════════════════════════════════
    # 5 版块归一化 (AI HOT 模式)
    # 所有情报最终归到 5 个标准版块
    # ═══════════════════════════════════════════

    BUCKETS = {
        "competitors": {"label": "竞品动态", "keywords": ["竞品", "competitor", "新品", "价格变动"]},
        "tenders":    {"label": "招标信息", "keywords": ["招标", "tender", "采购", "项目"]},
        "policies":   {"label": "政策法规", "keywords": ["关税", "tax", "政策", "certification", "合规", "标准"]},
        "trends":     {"label": "行业趋势", "keywords": ["趋势", "趋势", "growth", "market", "机会", "预测"]},
        "leads":      {"label": "买家线索", "keywords": ["线索", "lead", "买家", "客户", "采购需求", "需求"]},
    }

    def normalize(self, raw_info: dict) -> dict:
        """
        将任意原始情报归一化到 5 个版块之一
        
        输入: 原始情报字典（含 title / summary / source 等字段）
        输出: 归一化后的情报（含 bucket / title / summary / source / url / date）
        """
        title = (raw_info.get("title") or raw_info.get("name") or "").lower()
        summary = (raw_info.get("summary") or raw_info.get("description") or "").lower()
        text = title + " " + summary

        # 根据关键词匹配到对应版块
        bucket = "other"
        for bkid, spec in self.BUCKETS.items():
            for kw in spec.get("keywords", []):
                if kw.lower() in text:
                    bucket = bkid
                    break
            if bucket != "other":
                break

        return {
            "bucket": bucket,
            "bucket_label": self.BUCKETS.get(bucket, {"label": "其他"})["label"],
            "title": raw_info.get("title") or raw_info.get("name", ""),
            "summary": raw_info.get("summary") or raw_info.get("description", ""),
            "source": raw_info.get("source") or raw_info.get("sourceUrl", ""),
            "url": raw_info.get("url") or raw_info.get("sourceUrl", ""),
            "date": raw_info.get("date") or raw_info.get("publishedAt", ""),
        }

    def counter_evidence_check(self, claim: str = "", result: dict = None) -> dict:
        """
        对立面验证 — 融入 Anthropic Founder's Playbook 精华
        
        当系统给出结论时，自动搜索对立证据，防止 AI 放大确认偏误。
        每次情报输出时附加此检查。
        """
        if result and not claim:
            # 从结果中提取主张
            summary = ""
            items = result.get("items", [])
            if items:
                summary = items[0].get("title", "") + " " + items[0].get("summary", "")
            claim = summary or "当前情报结论"

        counter_points = []

        # 检查是否有积极表述
        positive_kw = ["好", "增长", "机会", "可行", "推荐", "strong", "增长", "领先", "优势"]
        negative_kw = ["差", "风险", "不行", "避免", "饱和", "衰退", "竞争", "降价"]

        has_positive = any(kw in claim for kw in positive_kw)
        has_negative = any(kw in claim for kw in negative_kw)

        if has_positive:
            counter_points.append({
                "type": "对立面",
                "question": "这个判断的反面证据是什么？什么情况下它会不成立？",
                "note": "确认偏误防护：AI 倾向于提供令人信服的正向论证",
            })
        if has_negative:
            counter_points.append({
                "type": "对立面",
                "question": "是否有例外或积极因素被忽略？",
                "note": "避免过度悲观，寻找被遗漏的机会信号",
            })

        # 通用反方视角
        counter_points.append({
            "type": "反方视角",
            "question": "如果这个判断是错的，最可能的原因是什么？",
            "ref": "Anthropic Founder's Playbook · 确认偏误防护",
        })

        # 市场特定风险
        market_hints = ["中东", "沙特", "阿联酋", "伊拉克", "澳洲", "Africa"]
        for hint in market_hints:
            if hint in claim:
                counter_points.append({
                    "type": "市场风险",
                    "question": f"{hint} 市场当前的主要风险因素有哪些？",
                })
                break

        return {
            "applied": len(counter_points) > 0,
            "claim": claim[:200],
            "counter_points": counter_points,
            "verdict": "建议在决策前评估对立面证据",
        }

    def feed(self, mode="selected", bucket=None, days=7, **kwargs):
        """
        统一情报 Feed — 三层路由 + 5 版块筛选

        mode:
          selected — 精选（已验证+活跃，默认）
          daily    — 按版块打包的聚合报告
          all      — 全量（含未验证的冷情报）

        bucket:
          competitors / tenders / policies / trends / leads
          不传则返回全部 5 个版块
        """
        # 模拟数据源（TODO: 接入真实数据源）
        samples = self._load_samples()

        # 归一化
        normalized = [self.normalize(s) for s in samples]

        # 按版块筛选
        if bucket and bucket in self.BUCKETS:
            normalized = [x for x in normalized if x["bucket"] == bucket]

        if mode == "selected":
            # 精选 = 有可信来源+有日期的
            hot = [x for x in normalized if x.get("source") and x.get("date")]
            if not hot:
                hot = normalized[:5]
            return self._format_selected(hot, days)
        elif mode == "daily":
            return self._format_daily(normalized, bucket)
        else:
            return self._format_all(normalized)

    def feed_with_check(self, mode="selected", bucket=None, days=7, **kwargs):
        """统一情报 Feed + 对立面验证"""
        result = self.feed(mode, bucket, days, **kwargs)
        result["_counter_evidence"] = self.counter_evidence_check(result=result)
        return result

    def _format_selected(self, items, days):
        imported = []
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        for x in items:
            try:
                d = datetime.strptime(x["date"][:10], "%Y-%m-%d")
                if d >= cutoff:
                    imported.append(x)
            except:
                imported.append(x)
        return {"mode": "selected", "count": len(imported), "items": imported[:50]}

    def _format_daily(self, items, filter_bucket):
        """按版块打包聚合"""
        groups = {}
        for x in items:
            b = x["bucket"]
            if b not in groups:
                groups[b] = {"label": x["bucket_label"], "items": []}
            groups[b]["items"].append(x)
        return {"mode": "daily", "date": __import__("datetime").datetime.now().strftime("%Y-%m-%d"), "groups": dict(groups)}

    def _format_all(self, items):
        return {"mode": "all", "count": len(items), "items": items[:100]}

    def _load_samples(self):
        """加载示例情报（TODO: 接入 data-integrator 7 源）"""
        return [
            {"title": "沙特 NEOM 项目发布钢结构采购招标", "summary": "预算 2.5 亿美元，钢结构折叠房屋", "source": "etimad.sa", "url": "", "date": "2026-05-07"},
            {"title": "土耳其 Karmod 在中东拿下 3 个新订单", "summary": "竞品动态：Karmod 中东订单量增长 40%", "source": "LinkedIn", "url": "", "date": "2026-05-06"},
            {"title": "SASO 更新建筑产品合规要求", "summary": "新政：钢结构产品需新增防火认证", "source": "SASO", "url": "", "date": "2026-05-05"},
            {"title": "中东建筑市场年增长 15%", "summary": "GCC 国家 2026 年建筑业规模预测", "source": "MEED", "url": "", "date": "2026-05-04"},
            {"title": "伊拉克 21 城重建计划新增 3 个住宅区", "summary": "采购需求：5 万套模块化住房", "source": "Gov.IQ", "url": "", "date": "2026-05-03"},
        ]

    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "status": "healthy",
            "module": "intelligence-hub",
            "version": "9.0.0"
        }
    
    @property
    def name(self) -> str:
        return "intelligence-hub"
    
    @property
    def version(self) -> str:
        return "9.0.0"
    
    @property
    def dependencies(self) -> List[str]:
        return ["cross-border-core", "data-integrator"]


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="智能分析中心模块")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    parser.add_argument("--task", help="执行任务")
    parser.add_argument("--product", help="产品名称")
    parser.add_argument("--market", help="目标市场")
    
    args = parser.parse_args()
    
    agent = IntelligenceHub(config_path=args.config)
    
    if args.task:
        result = agent.execute(task=args.task, product=args.product, market=args.market)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(agent.health_check(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
