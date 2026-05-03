#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转化漏斗分析模块 - 全链路追踪
太一 AGI · 2026-04-18

功能:
- 转化漏斗可视化
- 各阶段转化率分析
- 流失原因分析
- 优化建议生成
- ROI 计算

获客之王核心:
- 转化漏斗分析 (P2)
- ROI 追踪 (P2)
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
logger = logging.getLogger('ConversionFunnel')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data" / "cross-border" / "funnel"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class ConversionFunnelModule:
    """转化漏斗分析模块"""
    
    def __init__(self):
        # 漏斗阶段定义
        self.funnel_stages = {
            "stage_1": {
                "name": "线索获取",
                "description": "全网搜寻获取线索",
                "source": "prospect_search.py"
            },
            "stage_2": {
                "name": "线索清洗",
                "description": "数据验证 + 智能分级",
                "source": "data_verification.py"
            },
            "stage_3": {
                "name": "首次触达",
                "description": "自动触达模块",
                "source": "auto_outreach_module.py"
            },
            "stage_4": {
                "name": "互动培育",
                "description": "线索培育模块",
                "source": "lead_nurturing_module.py"
            },
            "stage_5": {
                "name": "商机确认",
                "description": "确认采购意向",
                "source": "lead_nurturing_module.py"
            },
            "stage_6": {
                "name": "报价谈判",
                "description": "商务谈判",
                "source": "lead_nurturing_module.py"
            },
            "stage_7": {
                "name": "成交",
                "description": "订单确认",
                "source": "order_management.py"
            }
        }
        
        # 行业基准转化率
        self.industry_benchmarks = {
            "stage_1_to_2": 0.70,  # 线索获取→清洗：70%
            "stage_2_to_3": 0.90,  # 清洗→触达：90%
            "stage_3_to_4": 0.40,  # 触达→互动：40%
            "stage_4_to_5": 0.30,  # 互动→商机：30%
            "stage_5_to_6": 0.60,  # 商机→报价：60%
            "stage_6_to_7": 0.50,  # 报价→成交：50%
            "overall": 0.019  # 总体转化率：1.9%
        }
    
    def analyze_funnel(self, leads: List[Dict]) -> Dict:
        """
        分析转化漏斗
        
        Args:
            leads: 线索列表 (包含各阶段状态)
            
        Returns:
            漏斗分析报告
        """
        logger.info(f"📊 分析转化漏斗：{len(leads)}个线索")
        
        # 统计各阶段线索数量
        stage_counts = self._count_by_stage(leads)
        
        # 计算各阶段转化率
        conversion_rates = self._calculate_conversion_rates(stage_counts)
        
        # 对比行业基准
        benchmark_comparison = self._compare_with_benchmarks(conversion_rates)
        
        # 识别瓶颈
        bottlenecks = self._identify_bottlenecks(conversion_rates)
        
        # 生成优化建议
        optimization_suggestions = self._generate_suggestions(bottlenecks)
        
        report = {
            "summary": {
                "total_leads": len(leads),
                "converted_leads": stage_counts.get("stage_7", 0),
                "overall_conversion_rate": conversion_rates.get("overall", 0),
                "analysis_date": datetime.now().strftime("%Y-%m-%d")
            },
            "stage_counts": stage_counts,
            "conversion_rates": conversion_rates,
            "benchmark_comparison": benchmark_comparison,
            "bottlenecks": bottlenecks,
            "optimization_suggestions": optimization_suggestions,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ 漏斗分析完成，总体转化率：{conversion_rates.get('overall', 0):.2%}")
        
        return report
    
    def _count_by_stage(self, leads: List[Dict]) -> Dict:
        """统计各阶段线索数量"""
        counts = {
            "stage_1": 0,
            "stage_2": 0,
            "stage_3": 0,
            "stage_4": 0,
            "stage_5": 0,
            "stage_6": 0,
            "stage_7": 0
        }
        
        for lead in leads:
            current_stage = lead.get("current_stage", "stage_1")
            if current_stage in counts:
                counts[current_stage] += 1
        
        # 计算累积数量 (漏斗从上到下)
        cumulative = {}
        total = len(leads)
        cumulative["stage_1"] = total
        
        remaining = total
        for stage in ["stage_2", "stage_3", "stage_4", "stage_5", "stage_6", "stage_7"]:
            remaining -= counts.get(stage, 0)
            cumulative[stage] = remaining
        
        return cumulative
    
    def _calculate_conversion_rates(self, stage_counts: Dict) -> Dict:
        """计算各阶段转化率"""
        rates = {}
        
        stages = ["stage_1", "stage_2", "stage_3", "stage_4", "stage_5", "stage_6", "stage_7"]
        
        for i in range(len(stages) - 1):
            current = stages[i]
            next_stage = stages[i + 1]
            
            current_count = stage_counts.get(current, 0)
            next_count = stage_counts.get(next_stage, 0)
            
            if current_count > 0:
                rate = next_count / current_count
            else:
                rate = 0
            
            rates[f"{current}_to_{next_stage}"] = rate
        
        # 总体转化率
        total = stage_counts.get("stage_1", 0)
        converted = stage_counts.get("stage_7", 0)
        
        if total > 0:
            rates["overall"] = converted / total
        else:
            rates["overall"] = 0
        
        return rates
    
    def _compare_with_benchmarks(self, conversion_rates: Dict) -> Dict:
        """对比行业基准"""
        comparison = {}
        
        for key, rate in conversion_rates.items():
            if key in self.industry_benchmarks:
                benchmark = self.industry_benchmarks[key]
                diff = rate - benchmark
                performance = "above" if diff > 0 else "below"
                
                comparison[key] = {
                    "actual": rate,
                    "benchmark": benchmark,
                    "difference": diff,
                    "performance": performance
                }
        
        return comparison
    
    def _identify_bottlenecks(self, conversion_rates: Dict) -> List[Dict]:
        """识别瓶颈"""
        bottlenecks = []
        
        for key, rate in conversion_rates.items():
            if key == "overall":
                continue
            
            benchmark = self.industry_benchmarks.get(key, 0)
            if rate < benchmark * 0.7:  # 低于基准 70% 视为瓶颈
                severity = "critical" if rate < benchmark * 0.5 else "warning"
                
                bottlenecks.append({
                    "stage_transition": key,
                    "actual_rate": rate,
                    "benchmark": benchmark,
                    "gap": benchmark - rate,
                    "severity": severity
                })
        
        # 按严重程度排序
        bottlenecks.sort(key=lambda x: x["gap"], reverse=True)
        
        return bottlenecks
    
    def _generate_suggestions(self, bottlenecks: List[Dict]) -> List[Dict]:
        """生成优化建议"""
        suggestions = []
        
        for bottleneck in bottlenecks:
            stage = bottleneck["stage_transition"]
            
            suggestion = {
                "stage": stage,
                "severity": bottleneck["severity"],
                "suggestions": []
            }
            
            # 根据瓶颈阶段生成建议
            if "stage_1_to_2" in stage:
                suggestion["suggestions"] = [
                    "优化线索筛选标准",
                    "提高数据验证质量",
                    "增加线索来源渠道"
                ]
            elif "stage_2_to_3" in stage:
                suggestion["suggestions"] = [
                    "完善联系信息",
                    "优化触达时机",
                    "提高话术质量"
                ]
            elif "stage_3_to_4" in stage:
                suggestion["suggestions"] = [
                    "优化首次触达话术",
                    "增加跟进频率",
                    "提供更有价值的内容"
                ]
            elif "stage_4_to_5" in stage:
                suggestion["suggestions"] = [
                    "加强培育内容",
                    "提供案例研究",
                    "安排产品演示"
                ]
            elif "stage_5_to_6" in stage:
                suggestion["suggestions"] = [
                    "优化报价策略",
                    "加强商务谈判技巧",
                    "提供灵活付款方式"
                ]
            elif "stage_6_to_7" in stage:
                suggestion["suggestions"] = [
                    "简化签约流程",
                    "提供优惠政策",
                    "加强售后服务承诺"
                ]
            
            suggestions.append(suggestion)
        
        return suggestions
    
    def calculate_roi(self, leads: List[Dict], costs: Dict) -> Dict:
        """
        计算 ROI
        
        Args:
            leads: 线索列表
            costs: 成本数据
            
        Returns:
            ROI 分析报告
        """
        logger.info(f"💰 计算 ROI...")
        
        # 统计成交线索
        converted_leads = [l for l in leads if l.get("current_stage") == "stage_7"]
        
        # 计算总收入
        total_revenue = sum(l.get("order_value", 0) for l in converted_leads)
        
        # 计算总成本
        total_cost = sum(costs.values())
        
        # 计算 ROI
        if total_cost > 0:
            roi = (total_revenue - total_cost) / total_cost
        else:
            roi = 0
        
        # 计算单个线索成本
        cost_per_lead = total_cost / len(leads) if leads else 0
        
        # 计算单个成交成本
        cost_per_conversion = total_cost / len(converted_leads) if converted_leads else 0
        
        report = {
            "summary": {
                "total_leads": len(leads),
                "converted_leads": len(converted_leads),
                "conversion_rate": len(converted_leads) / len(leads) if leads else 0,
                "total_revenue": total_revenue,
                "total_cost": total_cost,
                "roi": roi,
                "roi_percentage": f"{roi * 100:.2f}%",
                "analysis_date": datetime.now().strftime("%Y-%m-%d")
            },
            "cost_breakdown": costs,
            "efficiency_metrics": {
                "cost_per_lead": cost_per_lead,
                "cost_per_conversion": cost_per_conversion,
                "average_order_value": total_revenue / len(converted_leads) if converted_leads else 0
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ ROI 计算完成：{roi * 100:.2f}%")
        
        return report
    
    def generate_funnel_visualization(self, funnel_data: Dict) -> str:
        """生成漏斗可视化 (文本格式)"""
        stages = [
            ("线索获取", funnel_data["stage_counts"].get("stage_1", 0)),
            ("线索清洗", funnel_data["stage_counts"].get("stage_2", 0)),
            ("首次触达", funnel_data["stage_counts"].get("stage_3", 0)),
            ("互动培育", funnel_data["stage_counts"].get("stage_4", 0)),
            ("商机确认", funnel_data["stage_counts"].get("stage_5", 0)),
            ("报价谈判", funnel_data["stage_counts"].get("stage_6", 0)),
            ("成交", funnel_data["stage_counts"].get("stage_7", 0))
        ]
        
        max_count = max(s[1] for s in stages) if stages else 1
        
        visualization = "📊 转化漏斗可视化\n"
        visualization += "=" * 60 + "\n\n"
        
        for stage_name, count in stages:
            bar_length = int((count / max_count) * 40) if max_count > 0 else 0
            bar = "█" * bar_length
            percentage = (count / stages[0][1] * 100) if stages[0][1] > 0 else 0
            
            visualization += f"{stage_name:10} {bar:40} {count:5} ({percentage:5.1f}%)\n"
        
        visualization += "\n" + "=" * 60
        
        return visualization
    
    def save_report(self, report: Dict, filename: str = None) -> str:
        """保存报告"""
        if filename is None:
            filename = f"funnel_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = DATA_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 报告已保存：{filepath}")
        
        return str(filepath)


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("📊 转化漏斗分析模块 - 演示")
    logger.info("=" * 60)
    
    # 初始化模块
    funnel = ConversionFunnelModule()
    
    # 示例线索数据
    leads = [
        {"id": "lead_001", "current_stage": "stage_7", "order_value": 50000},
        {"id": "lead_002", "current_stage": "stage_7", "order_value": 30000},
        {"id": "lead_003", "current_stage": "stage_6", "order_value": 0},
        {"id": "lead_004", "current_stage": "stage_6", "order_value": 0},
        {"id": "lead_005", "current_stage": "stage_5", "order_value": 0},
        {"id": "lead_006", "current_stage": "stage_5", "order_value": 0},
        {"id": "lead_007", "current_stage": "stage_5", "order_value": 0},
        {"id": "lead_008", "current_stage": "stage_4", "order_value": 0},
        {"id": "lead_009", "current_stage": "stage_4", "order_value": 0},
        {"id": "lead_010", "current_stage": "stage_4", "order_value": 0},
        {"id": "lead_011", "current_stage": "stage_4", "order_value": 0},
        {"id": "lead_012", "current_stage": "stage_3", "order_value": 0},
        {"id": "lead_013", "current_stage": "stage_3", "order_value": 0},
        {"id": "lead_014", "current_stage": "stage_3", "order_value": 0},
        {"id": "lead_015", "current_stage": "stage_2", "order_value": 0},
        {"id": "lead_016", "current_stage": "stage_2", "order_value": 0},
        {"id": "lead_017", "current_stage": "stage_1", "order_value": 0},
        {"id": "lead_018", "current_stage": "stage_1", "order_value": 0},
        {"id": "lead_019", "current_stage": "stage_1", "order_value": 0},
        {"id": "lead_020", "current_stage": "stage_1", "order_value": 0},
    ]
    
    # 分析漏斗
    logger.info("\n📊 分析转化漏斗...")
    funnel_report = funnel.analyze_funnel(leads)
    
    logger.info(f"\n线索总数：{funnel_report['summary']['total_leads']}")
    logger.info(f"成交线索：{funnel_report['summary']['converted_leads']}")
    logger.info(f"总体转化率：{funnel_report['summary']['overall_conversion_rate']:.2%}")
    
    # 显示漏斗可视化
    logger.info("\n" + funnel.generate_funnel_visualization(funnel_report))
    
    # 识别瓶颈
    logger.info(f"\n🔍 瓶颈分析:")
    for bottleneck in funnel_report['bottlenecks'][:3]:
        logger.info(f"  - {bottleneck['stage_transition']}: {bottleneck['severity']} (差距：{bottleneck['gap']:.2%})")
    
    # 计算 ROI
    logger.info("\n💰 计算 ROI...")
    costs = {
        "marketing": 5000,
        "tools": 2000,
        "labor": 8000,
        "other": 1000
    }
    
    roi_report = funnel.calculate_roi(leads, costs)
    
    logger.info(f"\n总收入：${roi_report['summary']['total_revenue']:,.2f}")
    logger.info(f"总成本：${roi_report['summary']['total_cost']:,.2f}")
    logger.info(f"ROI: {roi_report['summary']['roi_percentage']}")
    logger.info(f"单个线索成本：${roi_report['efficiency_metrics']['cost_per_lead']:.2f}")
    logger.info(f"单个成交成本：${roi_report['efficiency_metrics']['cost_per_conversion']:.2f}")
    
    # 保存报告
    logger.info("\n💾 保存报告...")
    funnel.save_report(funnel_report)
    funnel.save_report(roi_report, "roi_analysis_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
