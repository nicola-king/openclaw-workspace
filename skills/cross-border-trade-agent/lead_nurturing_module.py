#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
线索培育模块 - 智能分级 + 全渠道跟进
太一 AGI · 2026-04-18

功能:
- 线索智能分级 (S/A/B/C)
- 培育流程自动化
- 多渠道协同跟进
- 转化漏斗分析
- ROI 追踪

获客之王核心:
- 深度线索清洗 → 智能分级高意向客源
- HIR (High-Intent Review) → 人工复核模式
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
logger = logging.getLogger('LeadNurturing')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
DATA_DIR = WORKSPACE / "data" / "cross-border" / "leads"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class LeadNurturingModule:
    """线索培育模块"""
    
    def __init__(self):
        # 线索分级标准
        self.grading_criteria = {
            "S": {
                "min_score": 90,
                "description": "极高意向 - 立即跟进",
                "priority": "P0",
                "follow_up_frequency": "daily",
                "human_review_required": True
            },
            "A": {
                "min_score": 75,
                "description": "高意向 - 重点跟进",
                "priority": "P1",
                "follow_up_frequency": "every_2_days",
                "human_review_required": True
            },
            "B": {
                "min_score": 50,
                "description": "中意向 - 常规跟进",
                "priority": "P2",
                "follow_up_frequency": "weekly",
                "human_review_required": False
            },
            "C": {
                "min_score": 0,
                "description": "低意向 - 培育为主",
                "priority": "P3",
                "follow_up_frequency": "monthly",
                "human_review_required": False
            }
        }
        
        # 评分维度
        self.scoring_dimensions = {
            "company_info": 20,      # 公司信息完整度
            "contact_info": 20,      # 联系信息完整度
            "engagement": 25,        # 互动程度
            "fit": 20,               # 匹配度
            "intent_signals": 15     # 意向信号
        }
        
        # 培育流程
        self.nurturing_flow = {
            "stage_1": {
                "name": "认知阶段",
                "duration_days": 7,
                "actions": ["发送公司介绍", "发送产品目录", "邀请参观网站"]
            },
            "stage_2": {
                "name": "兴趣阶段",
                "duration_days": 14,
                "actions": ["发送案例研究", "发送客户评价", "提供样品"]
            },
            "stage_3": {
                "name": "考虑阶段",
                "duration_days": 21,
                "actions": ["提供报价", "安排会议", "技术答疑"]
            },
            "stage_4": {
                "name": "决策阶段",
                "duration_days": 30,
                "actions": ["商务谈判", "合同准备", "订单确认"]
            }
        }
    
    def grade_lead(self, lead: Dict) -> Dict:
        """
        线索智能分级
        
        Args:
            lead: 线索信息
            
        Returns:
            分级结果
        """
        logger.info(f"🎯 线索分级：{lead.get('company_name', 'Unknown')}")
        
        # 计算综合评分
        total_score = self._calculate_lead_score(lead)
        
        # 确定等级
        grade = self._determine_grade(total_score)
        
        # 生成培育建议
        nurturing_suggestions = self._generate_nurturing_suggestions(lead, grade)
        
        result = {
            "lead_id": lead.get("id"),
            "company_name": lead.get("company_name"),
            "total_score": total_score,
            "grade": grade,
            "grade_description": self.grading_criteria[grade]["description"],
            "priority": self.grading_criteria[grade]["priority"],
            "follow_up_frequency": self.grading_criteria[grade]["follow_up_frequency"],
            "human_review_required": self.grading_criteria[grade]["human_review_required"],
            "dimension_scores": self._get_dimension_scores(lead),
            "nurturing_suggestions": nurturing_suggestions,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ 分级完成：{grade}级 ({total_score}分) - {self.grading_criteria[grade]['description']}")
        
        return result
    
    def _calculate_lead_score(self, lead: Dict) -> int:
        """计算线索综合评分"""
        score = 0
        
        # 1. 公司信息完整度 (20 分)
        if lead.get("company_name"):
            score += 5
        if lead.get("website"):
            score += 5
        if lead.get("industry"):
            score += 5
        if lead.get("company_size"):
            score += 5
        
        # 2. 联系信息完整度 (20 分)
        if lead.get("contact_name"):
            score += 5
        if lead.get("email"):
            score += 5
        if lead.get("phone"):
            score += 5
        if lead.get("position"):
            score += 5
        
        # 3. 互动程度 (25 分)
        email_opens = lead.get("email_opens", 0)
        if email_opens > 5:
            score += 10
        elif email_opens > 2:
            score += 5
        
        website_visits = lead.get("website_visits", 0)
        if website_visits > 3:
            score += 10
        elif website_visits > 1:
            score += 5
        
        response_rate = lead.get("response_rate", 0)
        score += min(5, response_rate * 5)
        
        # 4. 匹配度 (20 分)
        if lead.get("product_interest"):
            score += 10
        
        region = lead.get("region", "")
        if region in ["USA", "Europe", "Australia", "Canada"]:
            score += 10
        
        # 5. 意向信号 (15 分)
        intent_level = lead.get("intent_level", "low")
        if intent_level == "high":
            score += 15
        elif intent_level == "medium":
            score += 8
        elif intent_level == "low":
            score += 3
        
        return min(100, score)
    
    def _determine_grade(self, score: int) -> str:
        """确定等级"""
        if score >= 90:
            return "S"
        elif score >= 75:
            return "A"
        elif score >= 50:
            return "B"
        else:
            return "C"
    
    def _get_dimension_scores(self, lead: Dict) -> Dict:
        """获取各维度得分"""
        return {
            "company_info": self._score_company_info(lead),
            "contact_info": self._score_contact_info(lead),
            "engagement": self._score_engagement(lead),
            "fit": self._score_fit(lead),
            "intent_signals": self._score_intent_signals(lead)
        }
    
    def _score_company_info(self, lead: Dict) -> int:
        score = 0
        if lead.get("company_name"): score += 5
        if lead.get("website"): score += 5
        if lead.get("industry"): score += 5
        if lead.get("company_size"): score += 5
        return score
    
    def _score_contact_info(self, lead: Dict) -> int:
        score = 0
        if lead.get("contact_name"): score += 5
        if lead.get("email"): score += 5
        if lead.get("phone"): score += 5
        if lead.get("position"): score += 5
        return score
    
    def _score_engagement(self, lead: Dict) -> int:
        score = 0
        email_opens = lead.get("email_opens", 0)
        score += min(10, email_opens * 2)
        website_visits = lead.get("website_visits", 0)
        score += min(10, website_visits * 3)
        response_rate = lead.get("response_rate", 0)
        score += min(5, response_rate * 5)
        return score
    
    def _score_fit(self, lead: Dict) -> int:
        score = 0
        if lead.get("product_interest"): score += 10
        region = lead.get("region", "")
        if region in ["USA", "Europe", "Australia", "Canada"]: score += 10
        return score
    
    def _score_intent_signals(self, lead: Dict) -> int:
        intent_level = lead.get("intent_level", "low")
        if intent_level == "high": return 15
        elif intent_level == "medium": return 8
        else: return 3
    
    def _generate_nurturing_suggestions(self, lead: Dict, grade: str) -> List[Dict]:
        """生成培育建议"""
        suggestions = []
        
        if grade == "S":
            suggestions.append({
                "action": "立即安排电话会议",
                "priority": "P0",
                "deadline": "24 小时内"
            })
            suggestions.append({
                "action": "准备定制报价单",
                "priority": "P0",
                "deadline": "48 小时内"
            })
        elif grade == "A":
            suggestions.append({
                "action": "发送产品目录和案例",
                "priority": "P1",
                "deadline": "3 天内"
            })
            suggestions.append({
                "action": "提供免费样品",
                "priority": "P1",
                "deadline": "1 周内"
            })
        elif grade == "B":
            suggestions.append({
                "action": "定期发送行业资讯",
                "priority": "P2",
                "deadline": "每周"
            })
        else:
            suggestions.append({
                "action": "加入长期培育名单",
                "priority": "P3",
                "deadline": "每月"
            })
        
        return suggestions
    
    def batch_grade_leads(self, leads: List[Dict]) -> Dict:
        """批量线索分级"""
        logger.info(f"📊 批量分级：{len(leads)}个线索")
        
        results = {
            "total": len(leads),
            "by_grade": {"S": 0, "A": 0, "B": 0, "C": 0},
            "graded_leads": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for lead in leads:
            grade_result = self.grade_lead(lead)
            results["graded_leads"].append(grade_result)
            results["by_grade"][grade_result["grade"]] += 1
        
        logger.info(f"✅ 批量分级完成：S:{results['by_grade']['S']} A:{results['by_grade']['A']} B:{results['by_grade']['B']} C:{results['by_grade']['C']}")
        
        return results
    
    def generate_nurturing_report(self, graded_leads: List[Dict]) -> Dict:
        """生成培育报告"""
        report = {
            "summary": {
                "total_leads": len(graded_leads),
                "s_grade": len([l for l in graded_leads if l["grade"] == "S"]),
                "a_grade": len([l for l in graded_leads if l["grade"] == "A"]),
                "b_grade": len([l for l in graded_leads if l["grade"] == "B"]),
                "c_grade": len([l for l in graded_leads if l["grade"] == "C"]),
            },
            "priority_actions": [],
            "human_review_queue": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # 生成优先行动清单
        for lead in graded_leads:
            if lead["grade"] in ["S", "A"]:
                report["priority_actions"].append({
                    "company": lead["company_name"],
                    "grade": lead["grade"],
                    "score": lead["total_score"],
                    "actions": lead["nurturing_suggestions"]
                })
            
            if lead["human_review_required"]:
                report["human_review_queue"].append({
                    "company": lead["company_name"],
                    "grade": lead["grade"],
                    "score": lead["total_score"],
                    "reason": "高意向客户需要人工复核"
                })
        
        return report
    
    def save_grading_results(self, results: Dict, filename: str = None) -> str:
        """保存分级结果"""
        if filename is None:
            filename = f"lead_grading_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = DATA_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 分级结果已保存：{filepath}")
        
        return str(filepath)


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🌱 线索培育模块 - 演示")
    logger.info("=" * 60)
    
    # 初始化模块
    nurturing = LeadNurturingModule()
    
    # 示例线索
    leads = [
        {
            "id": "lead_001",
            "company_name": "ABC Trading LLC",
            "website": "www.abctrading.com",
            "industry": "建筑建材",
            "company_size": "50-100",
            "contact_name": "John Smith",
            "email": "john@abctrading.com",
            "phone": "+1-234-567-8900",
            "position": "采购经理",
            "region": "USA",
            "product_interest": "钢结构折叠房屋",
            "intent_level": "high",
            "email_opens": 8,
            "website_visits": 5,
            "response_rate": 0.8
        },
        {
            "id": "lead_002",
            "company_name": "Euro Build GmbH",
            "website": "www.eurobuild.de",
            "industry": "房地产",
            "contact_name": "Hans Mueller",
            "email": "hans@eurobuild.de",
            "region": "Europe",
            "product_interest": "轻钢别墅",
            "intent_level": "medium",
            "email_opens": 3,
            "website_visits": 2,
            "response_rate": 0.5
        },
        {
            "id": "lead_003",
            "company_name": "Aussie Homes Pty",
            "contact_name": "Sarah Johnson",
            "email": "sarah@aussiehomes.com.au",
            "phone": "+61-400-123-456",
            "region": "Australia",
            "product_interest": "活动板房",
            "intent_level": "high",
            "email_opens": 10,
            "website_visits": 8,
            "response_rate": 0.9
        },
        {
            "id": "lead_004",
            "company_name": "Unknown Company",
            "email": "info@unknown.com",
            "region": "Asia",
            "intent_level": "low",
            "email_opens": 1,
            "website_visits": 0,
            "response_rate": 0.1
        }
    ]
    
    # 批量分级
    logger.info("\n🎯 批量线索分级...")
    grading_results = nurturing.batch_grade_leads(leads)
    
    logger.info(f"\n线索总数：{grading_results['total']}")
    logger.info(f"S 级 (极高意向): {grading_results['by_grade']['S']}")
    logger.info(f"A 级 (高意向): {grading_results['by_grade']['A']}")
    logger.info(f"B 级 (中意向): {grading_results['by_grade']['B']}")
    logger.info(f"C 级 (低意向): {grading_results['by_grade']['C']}")
    
    # 生成培育报告
    logger.info("\n📊 生成培育报告...")
    report = nurturing.generate_nurturing_report(grading_results["graded_leads"])
    
    logger.info(f"\n优先行动：{len(report['priority_actions'])}个")
    for action in report['priority_actions'][:3]:
        logger.info(f"  - {action['company']} ({action['grade']}级，{action['score']}分)")
    
    logger.info(f"\n人工复核队列：{len(report['human_review_queue'])}个")
    for review in report['human_review_queue'][:3]:
        logger.info(f"  - {review['company']} ({review['grade']}级)")
    
    # 保存结果
    logger.info("\n💾 保存分级结果...")
    filepath = nurturing.save_grading_results(grading_results)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
