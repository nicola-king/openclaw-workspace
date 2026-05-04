#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A/B 测试优化模块 - 话术/时间/内容优化
太一 AGI · 2026-04-19 00:10

功能:
- 话术 A/B 测试
- 发送时间测试
- 内容格式测试
- 自动优胜选择

架构位置：智能决策中心 (Decision Center) → 转化优化中心

P1 任务：A/B 测试优化
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
logger = logging.getLogger('ABTestOptimizer')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data" / "cross-border" / "ab_tests"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class ABTestOptimizerModule:
    """A/B 测试优化模块"""
    
    def __init__(self):
        # A/B 测试配置
        self.test_config = {
            "min_sample_size": 100,       # 最小样本量
            "test_duration_days": 14,     # 测试周期 (天)
            "confidence_level": 0.95,     # 置信水平
            "auto_select_winner": True    # 自动选择优胜方案
        }
        
        # 活跃测试
        self.active_tests = []
        
        # 测试历史
        self.test_history = []
    
    def create_ab_test(self, test_name: str, test_type: str, variants: List[Dict]) -> Dict:
        """
        创建 A/B 测试
        
        Args:
            test_name: 测试名称
            test_type: 测试类型 (subject_line/content/send_time)
            variants: 测试变体
            
        Returns:
            测试配置
        """
        logger.info(f"🧪 创建 A/B 测试：{test_name}")
        
        test_config = {
            "test_id": f"ab_{test_name}_{datetime.now().strftime('%Y%m%d')}",
            "test_name": test_name,
            "test_type": test_type,
            "status": "active",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=self.test_config["test_duration_days"])).isoformat(),
            "variants": variants,
            "metrics": {
                "total_sent": 0,
                "total_opened": 0,
                "total_clicked": 0,
                "total_replied": 0,
                "total_converted": 0
            },
            "results": None
        }
        
        self.active_tests.append(test_config)
        
        logger.info(f"✅ A/B 测试已创建：{test_config['test_id']}")
        logger.info(f"变体数量：{len(variants)}")
        logger.info(f"测试周期：{self.test_config['test_duration_days']}天")
        
        return test_config
    
    def record_variant_metrics(self, test_id: str, variant_name: str, metrics: Dict) -> Dict:
        """
        记录变体指标
        
        Args:
            test_id: 测试 ID
            variant_name: 变体名称
            metrics: 指标数据
            
        Returns:
            记录结果
        """
        logger.info(f"📊 记录变体指标：{test_id} - {variant_name}")
        
        # 查找测试
        test = next((t for t in self.active_tests if t["test_id"] == test_id), None)
        
        if not test:
            logger.error(f"❌ 未找到测试：{test_id}")
            return {"status": "error", "message": "Test not found"}
        
        # 查找变体
        variant = next((v for v in test["variants"] if v["name"] == variant_name), None)
        
        if not variant:
            logger.error(f"❌ 未找到变体：{variant_name}")
            return {"status": "error", "message": "Variant not found"}
        
        # 更新指标
        if "metrics" not in variant:
            variant["metrics"] = {}
        
        variant["metrics"].update(metrics)
        
        # 更新测试总指标
        for key, value in metrics.items():
            if key in test["metrics"]:
                test["metrics"][key] += value
        
        logger.info(f"✅ 指标已记录：{variant_name}")
        
        return {"status": "success", "variant": variant_name, "metrics": metrics}
    
    def analyze_test_results(self, test_id: str) -> Dict:
        """
        分析测试结果
        
        Args:
            test_id: 测试 ID
            
        Returns:
            分析结果
        """
        logger.info(f"📊 分析测试结果：{test_id}")
        
        # 查找测试
        test = next((t for t in self.active_tests if t["test_id"] == test_id), None)
        
        if not test:
            logger.error(f"❌ 未找到测试：{test_id}")
            return {"status": "error", "message": "Test not found"}
        
        # 计算各变体转化率
        variant_analysis = []
        
        for variant in test["variants"]:
            metrics = variant.get("metrics", {})
            sent = metrics.get("sent", 0)
            converted = metrics.get("converted", 0)
            
            if sent > 0:
                conversion_rate = converted / sent
            else:
                conversion_rate = 0
            
            variant_analysis.append({
                "variant_name": variant.get("name"),
                "sent": sent,
                "converted": converted,
                "conversion_rate": conversion_rate,
                "is_winner": False
            })
        
        # 找出优胜者
        best_variant = max(variant_analysis, key=lambda x: x["conversion_rate"])
        
        for variant in variant_analysis:
            if variant["variant_name"] == best_variant["variant_name"]:
                variant["is_winner"] = True
        
        # 生成建议
        recommendation = {
            "test_id": test_id,
            "test_name": test["test_name"],
            "winner": best_variant["variant_name"],
            "winner_conversion_rate": best_variant["conversion_rate"],
            "variant_analysis": variant_analysis,
            "recommendation": f"建议使用 '{best_variant['variant_name']}' 方案，转化率{best_variant['conversion_rate']*100:.1f}%",
            "confidence": "high" if best_variant["conversion_rate"] > 0.15 else "medium",
            "timestamp": datetime.now().isoformat()
        }
        
        # 更新测试状态
        test["status"] = "completed"
        test["results"] = recommendation
        
        # 移动到历史记录
        self.test_history.append(test)
        self.active_tests.remove(test)
        
        logger.info(f"✅ 测试分析完成，优胜者：{best_variant['variant_name']}")
        
        return recommendation
    
    def get_test_recommendations(self) -> List[Dict]:
        """获取测试建议"""
        recommendations = []
        
        # 基于历史测试生成建议
        for test in self.test_history[-10:]:  # 最近 10 个测试
            if test.get("results"):
                recommendations.append({
                    "test_name": test["test_name"],
                    "test_type": test["test_type"],
                    "winner": test["results"]["winner"],
                    "conversion_rate": test["results"]["winner_conversion_rate"],
                    "recommendation": test["results"]["recommendation"]
                })
        
        return recommendations
    
    def generate_ab_test_report(self) -> Dict:
        """生成 A/B 测试报告"""
        logger.info("📋 生成 A/B 测试报告...")
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "active_tests": len(self.active_tests),
                "completed_tests": len(self.test_history),
                "total_variants_tested": sum(len(t.get("variants", [])) for t in self.test_history)
            },
            "active_tests": self.active_tests,
            "recent_winners": [],
            "recommendations": self.get_test_recommendations()
        }
        
        # 最近优胜者
        for test in self.test_history[-5:]:
            if test.get("results"):
                report["recent_winners"].append({
                    "test_name": test["test_name"],
                    "winner": test["results"]["winner"],
                    "conversion_rate": test["results"]["winner_conversion_rate"]
                })
        
        logger.info(f"✅ A/B 测试报告生成完成")
        
        return report
    
    def save_report(self, report: Dict) -> str:
        """保存报告"""
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"ab_test_report_{date_str}.json"
        filepath = DATA_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 报告已保存：{filepath}")
        
        return str(filepath)


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🧪 A/B 测试优化模块 - 演示")
    logger.info("=" * 60)
    
    # 初始化模块
    ab_test = ABTestOptimizerModule()
    
    # 创建 A/B 测试
    logger.info("\n🧪 创建 A/B 测试...")
    
    # 测试 1: 邮件标题
    test1 = ab_test.create_ab_test(
        test_name="email_subject_line",
        test_type="subject_line",
        variants=[
            {"name": "专业型标题", "metrics": {}},
            {"name": "价值型标题", "metrics": {}},
            {"name": "紧迫型标题", "metrics": {}}
        ]
    )
    
    # 测试 2: 发送时间
    test2 = ab_test.create_ab_test(
        test_name="send_time_optimization",
        test_type="send_time",
        variants=[
            {"name": "早上 08:00", "metrics": {}},
            {"name": "中午 12:00", "metrics": {}},
            {"name": "晚上 20:00", "metrics": {}}
        ]
    )
    
    # 记录指标
    logger.info("\n📊 记录指标...")
    
    # 模拟测试 1 结果
    ab_test.record_variant_metrics(test1["test_id"], "专业型标题", {"sent": 150, "converted": 18})
    ab_test.record_variant_metrics(test1["test_id"], "价值型标题", {"sent": 150, "converted": 25})
    ab_test.record_variant_metrics(test1["test_id"], "紧迫型标题", {"sent": 150, "converted": 12})
    
    # 模拟测试 2 结果
    ab_test.record_variant_metrics(test2["test_id"], "早上 08:00", {"sent": 100, "converted": 15})
    ab_test.record_variant_metrics(test2["test_id"], "中午 12:00", {"sent": 100, "converted": 12})
    ab_test.record_variant_metrics(test2["test_id"], "晚上 20:00", {"sent": 100, "converted": 20})
    
    # 分析结果
    logger.info("\n📊 分析测试结果...")
    
    result1 = ab_test.analyze_test_results(test1["test_id"])
    logger.info(f"\n测试 1 优胜者：{result1['winner']}")
    logger.info(f"转化率：{result1['winner_conversion_rate']*100:.1f}%")
    logger.info(f"建议：{result1['recommendation']}")
    
    result2 = ab_test.analyze_test_results(test2["test_id"])
    logger.info(f"\n测试 2 优胜者：{result2['winner']}")
    logger.info(f"转化率：{result2['winner_conversion_rate']*100:.1f}%")
    logger.info(f"建议：{result2['recommendation']}")
    
    # 生成报告
    logger.info("\n📋 生成 A/B 测试报告...")
    report = ab_test.generate_ab_test_report()
    
    logger.info(f"\n活跃测试：{report['summary']['active_tests']}个")
    logger.info(f"完成测试：{report['summary']['completed_tests']}个")
    logger.info(f"测试变体：{report['summary']['total_variants_tested']}个")
    
    logger.info(f"\n最近优胜者:")
    for winner in report['recent_winners']:
        logger.info(f"  • {winner['test_name']}: {winner['winner']} ({winner['conversion_rate']*100:.1f}%)")
    
    # 保存报告
    logger.info("\n💾 保存报告...")
    ab_test.save_report(report)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
