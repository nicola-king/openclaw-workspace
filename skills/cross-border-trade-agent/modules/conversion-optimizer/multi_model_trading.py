#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模型交易决策模块 - 开源交易系统核心能力
太一 AGI · 2026-04-20 21:31

功能:
- 多模型决策 (GPT-5.4 + Claude 4.6)
- 交易员综合意见
- 风控团队一票否决
- 年化收益优化
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('MultiModelTrading')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
TRADING_DIR = WORKSPACE / "data" / "cross-border" / "multi_model_trading"
TRADING_DIR.mkdir(parents=True, exist_ok=True)


class MultiModelTrading:
    """多模型交易决策模块"""
    
    # 模型配置
    MODELS = {
        "GPT-5.4": {"weight": 0.4, "specialty": "市场分析"},
        "Claude-4.6": {"weight": 0.4, "specialty": "风险评估"},
        "Technical_Analyst": {"weight": 0.1, "specialty": "技术分析"},
        "Risk_Manager": {"weight": 0.1, "specialty": "风控否决"}
    }
    
    # 交易信号
    SIGNALS = {
        "strong_buy": {"score": 5, "action": "买入", "confidence": 0.9},
        "buy": {"score": 4, "action": "买入", "confidence": 0.7},
        "hold": {"score": 3, "action": "持有", "confidence": 0.5},
        "sell": {"score": 2, "action": "卖出", "confidence": 0.7},
        "strong_sell": {"score": 1, "action": "卖出", "confidence": 0.9}
    }
    
    def __init__(self):
        self.trading_file = TRADING_DIR / "multi_model_trading.json"
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        if self.trading_file.exists():
            with open(self.trading_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"decisions": [], "performance": [], "stats": {}}
    
    def make_decision(self, asset: str, market_data: Dict) -> Dict:
        """多模型交易决策"""
        logger.info(f"📊 交易决策：{asset}")
        
        decision = {
            "id": f"TRADE_DECISION_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "asset": asset,
            "timestamp": datetime.now().isoformat(),
            "model_opinions": {},
            "consensus": {},
            "final_decision": "",
            "risk_veto": False,
            "confidence": 0
        }
        
        # 各模型意见
        for model_name, config in self.MODELS.items():
            opinion = self._get_model_opinion(model_name, asset, market_data)
            decision["model_opinions"][model_name] = opinion
        
        # 综合意见
        decision["consensus"] = self._aggregate_opinions(decision["model_opinions"])
        
        # 风控否决检查
        risk_opinion = decision["model_opinions"].get("Risk_Manager", {})
        if risk_opinion.get("veto", False):
            decision["risk_veto"] = True
            decision["final_decision"] = "HOLD (风控否决)"
            decision["confidence"] = 1.0
        else:
            # 最终决策
            consensus_score = decision["consensus"]["weighted_score"]
            decision["final_decision"] = self._score_to_decision(consensus_score)
            decision["confidence"] = decision["consensus"]["confidence"]
        
        # 记录决策
        self.data["decisions"].append(decision)
        self._update_stats(decision)
        self._save_data()
        
        logger.info(f"✅ 交易决策完成：{decision['final_decision']} (置信度：{decision['confidence']*100:.0f}%)")
        
        return decision
    
    def _get_model_opinion(self, model_name: str, asset: str, market_data: Dict) -> Dict:
        """获取模型意见"""
        # 模拟模型分析 (实际应调用对应模型 API)
        import random
        
        if model_name == "Risk_Manager":
            # 风控模型有否决权
            veto = random.random() > 0.95  # 5% 概率否决
            return {
                "signal": "hold" if veto else "buy",
                "confidence": 0.95,
                "reasoning": "风险过高，建议否决" if veto else "风险可控",
                "veto": veto
            }
        else:
            signals = ["strong_buy", "buy", "hold", "sell", "strong_sell"]
            signal = random.choice(signals)
            return {
                "signal": signal,
                "confidence": self.SIGNALS[signal]["confidence"],
                "reasoning": f"{model_name}分析：基于{market_data.get('trend', '当前趋势')}",
                "veto": False
            }
    
    def _aggregate_opinions(self, opinions: Dict) -> Dict:
        """综合各模型意见"""
        weighted_score = 0
        total_weight = 0
        max_confidence = 0
        
        for model_name, opinion in opinions.items():
            if model_name == "Risk_Manager":
                continue  # 风控单独处理
            
            config = self.MODELS[model_name]
            signal_score = self.SIGNALS[opinion["signal"]]["score"]
            weight = config["weight"]
            
            weighted_score += signal_score * weight
            total_weight += weight
            max_confidence = max(max_confidence, opinion["confidence"])
        
        # 归一化
        normalized_score = weighted_score / total_weight if total_weight > 0 else 3
        
        return {
            "weighted_score": normalized_score,
            "confidence": max_confidence,
            "model_count": len([k for k in opinions.keys() if k != "Risk_Manager"])
        }
    
    def _score_to_decision(self, score: float) -> str:
        """分数转决策"""
        if score >= 4.5:
            return "STRONG_BUY"
        elif score >= 3.5:
            return "BUY"
        elif score >= 2.5:
            return "HOLD"
        elif score >= 1.5:
            return "SELL"
        else:
            return "STRONG_SELL"
    
    def track_performance(self, decision_id: str, actual_return: float) -> Dict:
        """追踪实际收益"""
        logger.info(f"📈 追踪收益：{decision_id}")
        
        # 查找决策
        decision = None
        for d in self.data["decisions"]:
            if d["id"] == decision_id:
                decision = d
                break
        
        if not decision:
            return {"error": "Decision not found"}
        
        performance = {
            "decision_id": decision_id,
            "asset": decision["asset"],
            "decision": decision["final_decision"],
            "actual_return": actual_return,
            "predicted_confidence": decision["confidence"],
            "accuracy": self._calculate_accuracy(decision["final_decision"], actual_return),
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["performance"].append(performance)
        self._save_data()
        
        logger.info(f"✅ 收益追踪完成：{actual_return*100:.1f}%")
        
        return performance
    
    def _calculate_accuracy(self, decision: str, actual_return: float) -> float:
        """计算决策准确度"""
        # 简化计算
        if "BUY" in decision and actual_return > 0:
            return min(1.0, actual_return + 0.5)
        elif "SELL" in decision and actual_return < 0:
            return min(1.0, abs(actual_return) + 0.5)
        elif "HOLD" in decision:
            return 0.5  # HOLD 默认 50% 准确
        else:
            return 0.0
    
    def _update_stats(self, decision: Dict):
        """更新统计"""
        if "total_decisions" not in self.data["stats"]:
            self.data["stats"] = {
                "total_decisions": 0,
                "buy_signals": 0,
                "sell_signals": 0,
                "risk_vetos": 0,
                "avg_confidence": 0
            }
        
        self.data["stats"]["total_decisions"] += 1
        
        if "BUY" in decision["final_decision"]:
            self.data["stats"]["buy_signals"] += 1
        elif "SELL" in decision["final_decision"]:
            self.data["stats"]["sell_signals"] += 1
        
        if decision["risk_veto"]:
            self.data["stats"]["risk_vetos"] += 1
        
        # 更新平均置信度
        total = self.data["stats"]["total_decisions"]
        prev_avg = self.data["stats"]["avg_confidence"]
        self.data["stats"]["avg_confidence"] = (prev_avg * (total - 1) + decision["confidence"]) / total
    
    def get_performance_stats(self) -> Dict:
        """获取收益统计"""
        if not self.data["performance"]:
            return {"status": "no_data"}
        
        returns = [p["actual_return"] for p in self.data["performance"]]
        accuracies = [p["accuracy"] for p in self.data["performance"]]
        
        return {
            "total_trades": len(returns),
            "avg_return": round(sum(returns) / len(returns) * 100, 2),
            "avg_accuracy": round(sum(accuracies) / len(accuracies) * 100, 2),
            "best_trade": round(max(returns) * 100, 2),
            "worst_trade": round(min(returns) * 100, 2),
            "annualized_return": round(sum(returns) / len(returns) * 12 * 100, 2)  # 简化年化
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_decisions": self.data["stats"].get("total_decisions", 0),
            "buy_signals": self.data["stats"].get("buy_signals", 0),
            "sell_signals": self.data["stats"].get("sell_signals", 0),
            "risk_vetos": self.data["stats"].get("risk_vetos", 0),
            "avg_confidence": round(self.data["stats"].get("avg_confidence", 0) * 100, 2)
        }
    
    def _save_data(self):
        TRADING_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.trading_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)


def main():
    logger.info("=" * 60)
    logger.info("📊 多模型交易决策 - 开源交易系统核心能力")
    logger.info("=" * 60)
    
    trading = MultiModelTrading()
    
    # 演示交易决策
    logger.info(f"\n📊 交易决策...")
    market_data = {
        "price": 0.9554,
        "trend": "横盘整理",
        "volume": 14.3,
        "rsi": 45
    }
    
    decision = trading.make_decision("SUI", market_data)
    logger.info(f"  资产：{decision['asset']}")
    logger.info(f"  决策：{decision['final_decision']}")
    logger.info(f"  置信度：{decision['confidence']*100:.0f}%")
    logger.info(f"  风控否决：{decision['risk_veto']}")
    
    # 演示收益追踪
    logger.info(f"\n📈 收益追踪...")
    performance = trading.track_performance(decision["id"], 0.26)  # 26% 收益
    logger.info(f"  实际收益：{performance['actual_return']*100:.1f}%")
    logger.info(f"  决策准确度：{performance['accuracy']*100:.0f}%")
    
    # 获取统计
    logger.info(f"\n📊 交易统计:")
    stats = trading.get_stats()
    logger.info(f"  总决策：{stats['total_decisions']}")
    logger.info(f"  买入信号：{stats['buy_signals']}")
    logger.info(f"  卖出信号：{stats['sell_signals']}")
    logger.info(f"  风控否决：{stats['risk_vetos']}")
    logger.info(f"  平均置信度：{stats['avg_confidence']}%")
    
    logger.info(f"\n📈 收益统计:")
    perf_stats = trading.get_performance_stats()
    if perf_stats.get("status") != "no_data":
        logger.info(f"  总交易：{perf_stats['total_trades']}")
        logger.info(f"  平均收益：{perf_stats['avg_return']}%")
        logger.info(f"  平均准确度：{perf_stats['avg_accuracy']}%")
        logger.info(f"  年化收益：{perf_stats['annualized_return']}%")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 多模型交易决策演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
