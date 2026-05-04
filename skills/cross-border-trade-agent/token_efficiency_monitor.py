#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 效率监控模块 - GenericAgent 核心机制融合
太一 AGI · 2026-04-19 00:28

功能:
- Token 消耗统计
- 技能复用率监控
- Token 效率分析
- 优化建议生成
- 6 倍效率目标追踪

架构位置：智能决策中心 (Decision Center) → 转化优化中心

P1 任务：Token 效率监控
灵感来源：GenericAgent (GitHub 4149⭐)
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('TokenEfficiencyMonitor')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data" / "cross-border" / "token_monitor"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class TokenEfficiencyMonitorModule:
    """Token 效率监控模块"""
    
    def __init__(self):
        # 监控配置
        self.config = {
            "efficiency_target": 6.0,  # 6 倍效率目标
            "tracking_period_days": 30,  # 追踪周期
            "alert_threshold": 0.5,  # 低于目标 50% 告警
            "auto_optimize": True  # 自动优化建议
        }
        
        # Token 消耗记录
        self.token_records = self._load_token_records()
        
        # 技能复用记录
        self.skill_reuse_records = []
        
        # 统计
        self.stats = {
            "total_tokens_used": 0,
            "total_tokens_saved": 0,
            "current_efficiency": 1.0,
            "target_efficiency": self.config["efficiency_target"],
            "skill_reuse_rate": 0.0
        }
    
    def _load_token_records(self) -> Dict:
        """加载 Token 记录"""
        records_file = DATA_DIR / "token_records.json"
        
        if records_file.exists():
            with open(records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {"records": [], "total": 0, "updated_at": None}
    
    def record_token_usage(self, task_id: str, task_type: str, tokens_used: int, 
                          skill_reused: bool = False, saved_tokens: int = 0) -> Dict:
        """
        记录 Token 使用
        
        Args:
            task_id: 任务 ID
            task_type: 任务类型
            tokens_used: 使用的 Token
            skill_reused: 是否复用技能
            saved_tokens: 节省的 Token
            
        Returns:
            记录结果
        """
        logger.info(f"📊 记录 Token 使用：{task_type} - {tokens_used} tokens")
        
        record = {
            "task_id": task_id,
            "task_type": task_type,
            "tokens_used": tokens_used,
            "skill_reused": skill_reused,
            "saved_tokens": saved_tokens,
            "timestamp": datetime.now().isoformat()
        }
        
        self.token_records["records"].append(record)
        self.token_records["total"] += 1
        self.token_records["updated_at"] = datetime.now().isoformat()
        
        # 更新统计
        self._update_stats()
        
        # 保存记录
        self._save_token_records()
        
        logger.info(f"✅ Token 使用已记录")
        
        return record
    
    def _update_stats(self):
        """更新统计信息"""
        # 计算总 Token 使用
        total_used = sum(r["tokens_used"] for r in self.token_records["records"])
        total_saved = sum(r["saved_tokens"] for r in self.token_records["records"])
        
        # 计算技能复用率
        reused_count = len([r for r in self.token_records["records"] if r["skill_reused"]])
        reuse_rate = reused_count / max(1, len(self.token_records["records"]))
        
        # 计算当前效率
        if total_saved > 0:
            current_efficiency = (total_used + total_saved) / total_used
        else:
            current_efficiency = 1.0
        
        self.stats["total_tokens_used"] = total_used
        self.stats["total_tokens_saved"] = total_saved
        self.stats["current_efficiency"] = current_efficiency
        self.stats["skill_reuse_rate"] = reuse_rate
        
        logger.info(f"📊 统计已更新：效率{current_efficiency:.2f}x, 复用率{reuse_rate:.2%}")
    
    def _save_token_records(self):
        """保存 Token 记录"""
        records_file = DATA_DIR / "token_records.json"
        
        with open(records_file, 'w', encoding='utf-8') as f:
            json.dump(self.token_records, f, indent=2, ensure_ascii=False)
    
    def analyze_efficiency(self) -> Dict:
        """分析 Token 效率"""
        logger.info("📊 分析 Token 效率...")
        
        analysis = {
            "generated_at": datetime.now().isoformat(),
            "current_stats": self.stats,
            "efficiency_gap": self.config["efficiency_target"] - self.stats["current_efficiency"],
            "efficiency_percentage": (self.stats["current_efficiency"] / self.config["efficiency_target"]) * 100,
            "trend": self._analyze_trend(),
            "recommendations": self._generate_recommendations()
        }
        
        logger.info(f"✅ 效率分析完成")
        
        return analysis
    
    def _analyze_trend(self) -> Dict:
        """分析趋势"""
        records = self.token_records["records"]
        
        if len(records) < 2:
            return {"status": "insufficient_data", "message": "数据不足"}
        
        # 按日期分组
        daily_stats = {}
        for record in records:
            date = record["timestamp"][:10]
            if date not in daily_stats:
                daily_stats[date] = {"used": 0, "saved": 0}
            daily_stats[date]["used"] += record["tokens_used"]
            daily_stats[date]["saved"] += record["saved_tokens"]
        
        # 计算最近 7 天趋势
        sorted_dates = sorted(daily_stats.keys())[-7:]
        
        trend_data = []
        for date in sorted_dates:
            stats = daily_stats[date]
            efficiency = (stats["used"] + stats["saved"]) / max(1, stats["used"])
            trend_data.append({
                "date": date,
                "efficiency": efficiency
            })
        
        # 判断趋势
        if len(trend_data) >= 2:
            recent_efficiency = trend_data[-1]["efficiency"]
            previous_efficiency = trend_data[-2]["efficiency"]
            
            if recent_efficiency > previous_efficiency:
                trend = "improving"
            elif recent_efficiency < previous_efficiency:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "trend": trend,
            "daily_data": trend_data,
            "average_efficiency": sum(d["efficiency"] for d in trend_data) / max(1, len(trend_data))
        }
    
    def _generate_recommendations(self) -> List[Dict]:
        """生成优化建议"""
        recommendations = []
        
        current_efficiency = self.stats["current_efficiency"]
        target_efficiency = self.config["efficiency_target"]
        reuse_rate = self.stats["skill_reuse_rate"]
        
        # 效率低于目标
        if current_efficiency < target_efficiency:
            gap = target_efficiency - current_efficiency
            recommendations.append({
                "priority": "P0",
                "type": "efficiency_gap",
                "message": f"当前效率{current_efficiency:.1f}x，距离目标{target_efficiency}x 还有{gap:.1f}x 差距",
                "action": "增加技能复用，减少重复任务"
            })
        
        # 技能复用率低
        if reuse_rate < 0.3:
            recommendations.append({
                "priority": "P1",
                "type": "low_reuse_rate",
                "message": f"技能复用率{reuse_rate:.1%}，建议提升至 30%+",
                "action": "启用技能结晶机制，自动复用类似任务"
            })
        
        # Token 消耗过高
        recent_records = self.token_records["records"][-10:]
        if recent_records:
            avg_tokens = sum(r["tokens_used"] for r in recent_records) / len(recent_records)
            if avg_tokens > 10000:
                recommendations.append({
                    "priority": "P2",
                    "type": "high_token_usage",
                    "message": f"平均每次任务消耗{avg_tokens:.0f} tokens，偏高",
                    "action": "优化任务描述，减少冗余信息"
                })
        
        # 效率趋势下降
        trend = self._analyze_trend()
        if trend.get("trend") == "declining":
            recommendations.append({
                "priority": "P1",
                "type": "declining_trend",
                "message": "Token 效率呈下降趋势",
                "action": "检查新增任务类型，优化执行路径"
            })
        
        if not recommendations:
            recommendations.append({
                "priority": "P3",
                "type": "info",
                "message": "Token 效率良好，继续保持",
                "action": "持续监控"
            })
        
        return recommendations
    
    def check_alerts(self) -> List[Dict]:
        """检查告警"""
        alerts = []
        
        current_efficiency = self.stats["current_efficiency"]
        target_efficiency = self.config["efficiency_target"]
        
        # 效率低于阈值
        if current_efficiency < target_efficiency * self.config["alert_threshold"]:
            alerts.append({
                "level": "critical",
                "type": "efficiency_critical",
                "message": f"Token 效率严重偏低 ({current_efficiency:.1f}x < {target_efficiency * self.config['alert_threshold']:.1f}x)",
                "action": "立即优化任务执行路径"
            })
        
        # 技能复用率过低
        if self.stats["skill_reuse_rate"] < 0.1:
            alerts.append({
                "level": "warning",
                "type": "reuse_rate_low",
                "message": f"技能复用率过低 ({self.stats['skill_reuse_rate']:.1%})",
                "action": "启用技能结晶机制"
            })
        
        return alerts
    
    def generate_efficiency_report(self) -> Dict:
        """生成效率报告"""
        logger.info("📊 生成 Token 效率报告...")
        
        analysis = self.analyze_efficiency()
        alerts = self.check_alerts()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_tokens_used": self.stats["total_tokens_used"],
                "total_tokens_saved": self.stats["total_tokens_saved"],
                "current_efficiency": self.stats["current_efficiency"],
                "target_efficiency": self.stats["target_efficiency"],
                "efficiency_percentage": analysis["efficiency_percentage"],
                "skill_reuse_rate": self.stats["skill_reuse_rate"]
            },
            "analysis": analysis,
            "alerts": alerts,
            "recommendations": analysis["recommendations"]
        }
        
        logger.info(f"✅ 效率报告生成完成")
        
        return report
    
    def save_report(self, report: Dict) -> str:
        """保存报告"""
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"token_efficiency_report_{date_str}.json"
        filepath = DATA_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 报告已保存：{filepath}")
        
        return str(filepath)


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("📊 Token 效率监控模块 - 演示")
    logger.info("=" * 60)
    
    # 初始化模块
    monitor = TokenEfficiencyMonitorModule()
    
    # 记录 Token 使用
    logger.info("\n📊 记录 Token 使用...")
    
    # 模拟任务
    tasks = [
        {"task_id": "task_001", "type": "daily_intelligence", "tokens": 5000, "reused": False},
        {"task_id": "task_002", "type": "daily_intelligence", "tokens": 1000, "reused": True, "saved": 4000},
        {"task_id": "task_003", "type": "competitor_monitor", "tokens": 3000, "reused": False},
        {"task_id": "task_004", "type": "competitor_monitor", "tokens": 800, "reused": True, "saved": 2200},
        {"task_id": "task_005", "type": "trend_alert", "tokens": 2000, "reused": False},
        {"task_id": "task_006", "type": "daily_intelligence", "tokens": 900, "reused": True, "saved": 4100},
    ]
    
    for task in tasks:
        monitor.record_token_usage(
            task_id=task["task_id"],
            task_type=task["type"],
            tokens_used=task["tokens"],
            skill_reused=task.get("reused", False),
            saved_tokens=task.get("saved", 0)
        )
    
    # 分析效率
    logger.info("\n📊 分析 Token 效率...")
    analysis = monitor.analyze_efficiency()
    
    logger.info(f"当前效率：{analysis['current_stats']['current_efficiency']:.2f}x")
    logger.info(f"目标效率：{analysis['current_stats']['target_efficiency']}x")
    logger.info(f"效率差距：{analysis['efficiency_gap']:.2f}x")
    logger.info(f"完成度：{analysis['efficiency_percentage']:.1f}%")
    
    # 检查告警
    logger.info("\n🚨 检查告警...")
    alerts = monitor.check_alerts()
    
    if alerts:
        for alert in alerts:
            logger.info(f"  {alert['level']}: {alert['message']}")
    else:
        logger.info("  ✅ 无告警")
    
    # 生成建议
    logger.info("\n💡 优化建议:")
    for rec in analysis["recommendations"]:
        logger.info(f"  [{rec['priority']}] {rec['message']}")
        logger.info(f"      行动：{rec['action']}")
    
    # 生成报告
    logger.info("\n📊 生成效率报告...")
    report = monitor.generate_efficiency_report()
    
    logger.info(f"\n总 Token 使用：{report['summary']['total_tokens_used']:,}")
    logger.info(f"总 Token 节省：{report['summary']['total_tokens_saved']:,}")
    logger.info(f"技能复用率：{report['summary']['skill_reuse_rate']:.1%}")
    
    # 保存报告
    logger.info("\n💾 保存报告...")
    monitor.save_report(report)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
