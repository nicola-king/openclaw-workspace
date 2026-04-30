#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Agent - 产品管理专家

职责:
- 产品规划 (PRD/路线图)
- 需求分析 (用户故事/功能列表)
- 项目管理 (任务分解/进度追踪)
- 数据分析 (用户反馈/指标监控)

灵感：Garry Tan/gstack - PM 角色
作者：太一 AGI
创建：2026-04-18
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('PMAgent')


@dataclass
class UserStory:
    """用户故事"""
    title: str
    description: str
    acceptance_criteria: List[str]
    priority: str  # P0/P1/P2/P3
    estimate: int  # 故事点


@dataclass
class Feature:
    """功能特性"""
    name: str
    description: str
    user_stories: List[UserStory] = field(default_factory=list)
    status: str = "planning"  # planning/developing/testing/released
    priority: str = "P1"


@dataclass
class ProductTask:
    """产品任务"""
    task_type: str  # prd/roadmap/requirement/analysis
    product_name: str
    description: str
    target_users: List[str] = None
    deadline: str = None


class PMAgent:
    """PM Agent - 产品管理专家"""
    
    def __init__(self):
        self.tools = [
            "prd_generator",      # PRD 生成
            "roadmap_planner",    # 路线图规划
            "requirement_analyzer",  # 需求分析
            "data_analyzer",      # 数据分析
        ]
        
        self.products = {}
        self.task_history = []
    
    def execute(self, task: ProductTask) -> Dict:
        """
        执行产品任务
        
        Args:
            task: 产品任务
            
        Returns:
            任务结果
        """
        logger.info(f"📋 执行产品任务：{task.task_type}")
        logger.info(f"   产品：{task.product_name}")
        logger.info(f"   描述：{task.description}")
        
        # 根据任务类型分发
        if task.task_type == "prd":
            result = self._generate_prd(task)
        elif task.task_type == "roadmap":
            result = self._create_roadmap(task)
        elif task.task_type == "requirement":
            result = self._analyze_requirement(task)
        elif task.task_type == "analysis":
            result = self._analyze_data(task)
        else:
            result = {"status": "error", "message": f"未知任务类型：{task.task_type}"}
        
        # 记录历史
        self.task_history.append({
            "task": task,
            "result": result,
            "timestamp": datetime.now().isoformat(),
        })
        
        logger.info(f"✅ 产品任务完成")
        
        return result
    
    def _generate_prd(self, task: ProductTask) -> Dict:
        """生成产品需求文档 (PRD)"""
        logger.info("  生成 PRD...")
        
        prd = {
            "title": f"{task.product_name} 产品需求文档",
            "version": "1.0",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "overview": {
                "product_name": task.product_name,
                "description": task.description,
                "target_users": task.target_users or ["一般用户"],
                "goals": [
                    "解决用户核心痛点",
                    "提供卓越用户体验",
                    "实现商业目标",
                ],
            },
            "features": [
                {
                    "name": "核心功能 1",
                    "description": "描述核心功能 1",
                    "priority": "P0",
                    "user_stories": [
                        {
                            "title": "用户故事 1",
                            "description": "作为用户，我希望...，以便...",
                            "acceptance_criteria": ["标准 1", "标准 2"],
                        }
                    ],
                },
                {
                    "name": "核心功能 2",
                    "description": "描述核心功能 2",
                    "priority": "P1",
                },
            ],
            "non_functional_requirements": {
                "performance": "响应时间<1 秒",
                "availability": "99.9% 可用性",
                "security": "数据加密传输",
                "scalability": "支持 10 万并发",
            },
            "timeline": {
                "phase1": "需求分析 (2 周)",
                "phase2": "设计开发 (6 周)",
                "phase3": "测试优化 (2 周)",
                "phase4": "上线发布 (1 周)",
            },
            "success_metrics": [
                "日活跃用户>1000",
                "用户留存率>60%",
                "NPS>50",
            ],
        }
        
        # 保存 PRD
        output_file = f"output/products/{task.product_name}_PRD.md"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        prd_content = self._format_prd_markdown(prd)
        Path(output_file).write_text(prd_content, encoding='utf-8')
        
        result = {
            "status": "completed",
            "type": "prd",
            "output_file": output_file,
            "product_name": task.product_name,
            "features_count": len(prd["features"]),
        }
        
        logger.info(f"  ✅ PRD 生成完成：{output_file}")
        
        return result
    
    def _format_prd_markdown(self, prd: Dict) -> str:
        """格式化 PRD 为 Markdown"""
        content = f"# {prd['title']}\n\n"
        content += f"**版本**: {prd['version']}  \n"
        content += f"**日期**: {prd['date']}  \n\n"
        
        content += "## 📋 概述\n\n"
        overview = prd["overview"]
        content += f"- **产品名称**: {overview['product_name']}\n"
        content += f"- **产品描述**: {overview['description']}\n"
        content += f"- **目标用户**: {', '.join(overview['target_users'])}\n\n"
        
        content += "## 🎯 产品目标\n\n"
        for goal in overview["goals"]:
            content += f"- {goal}\n"
        content += "\n"
        
        content += "## ✨ 功能特性\n\n"
        for feature in prd["features"]:
            content += f"### {feature['name']}\n\n"
            content += f"{feature['description']}\n\n"
            content += f"**优先级**: {feature.get('priority', 'P1')}\n\n"
            
            if "user_stories" in feature:
                content += "**用户故事**:\n\n"
                for story in feature["user_stories"]:
                    content += f"- {story.get('title', '用户故事')}\n"
                    content += f"  - {story.get('description', '')}\n"
                content += "\n"
        
        content += "## 📊 非功能性需求\n\n"
        for key, value in prd["non_functional_requirements"].items():
            content += f"- **{key}**: {value}\n"
        content += "\n"
        
        content += "## 📅 时间线\n\n"
        for phase, timeline in prd["timeline"].items():
            content += f"- **{phase}**: {timeline}\n"
        content += "\n"
        
        content += "## 📈 成功指标\n\n"
        for metric in prd["success_metrics"]:
            content += f"- {metric}\n"
        
        return content
    
    def _create_roadmap(self, task: ProductTask) -> Dict:
        """创建产品路线图"""
        logger.info("  创建产品路线图...")
        
        roadmap = {
            "product_name": task.product_name,
            "timeline": "Q2-Q4 2026",
            "quarters": {
                "Q2": {
                    "theme": "基础功能建设",
                    "features": [
                        {"name": "用户系统", "status": "completed"},
                        {"name": "核心功能", "status": "in_progress"},
                        {"name": "支付系统", "status": "planned"},
                    ],
                },
                "Q3": {
                    "theme": "增长与优化",
                    "features": [
                        {"name": "数据分析", "status": "planned"},
                        {"name": "营销工具", "status": "planned"},
                        {"name": "性能优化", "status": "planned"},
                    ],
                },
                "Q4": {
                    "theme": "规模化扩张",
                    "features": [
                        {"name": "国际化", "status": "planned"},
                        {"name": "企业版", "status": "planned"},
                        {"name": "API 开放", "status": "planned"},
                    ],
                },
            },
            "milestones": [
                {"name": "MVP 发布", "date": "2026-06-30", "status": "upcoming"},
                {"name": "1 万用户", "date": "2026-09-30", "status": "upcoming"},
                {"name": "盈利", "date": "2026-12-31", "status": "upcoming"},
            ],
        }
        
        # 保存路线图
        output_file = f"output/products/{task.product_name}_Roadmap.md"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        roadmap_content = self._format_roadmap_markdown(roadmap)
        Path(output_file).write_text(roadmap_content, encoding='utf-8')
        
        result = {
            "status": "completed",
            "type": "roadmap",
            "output_file": output_file,
            "product_name": task.product_name,
            "quarters_count": len(roadmap["quarters"]),
            "milestones_count": len(roadmap["milestones"]),
        }
        
        logger.info(f"  ✅ 路线图创建完成：{output_file}")
        
        return result
    
    def _format_roadmap_markdown(self, roadmap: Dict) -> str:
        """格式化路线图为 Markdown"""
        content = f"# {roadmap['product_name']} 产品路线图\n\n"
        content += f"**时间范围**: {roadmap['timeline']}  \n\n"
        
        for quarter, data in roadmap["quarters"].items():
            content += f"## {quarter} - {data['theme']}\n\n"
            for feature in data["features"]:
                status_icon = {"completed": "✅", "in_progress": "🔄", "planned": "⏳"}.get(feature["status"], "⏳")
                content += f"- {status_icon} {feature['name']}\n"
            content += "\n"
        
        content += "## 🎯 里程碑\n\n"
        for milestone in roadmap["milestones"]:
            status_icon = {"completed": "✅", "in_progress": "🔄", "upcoming": "⏳"}.get(milestone["status"], "⏳")
            content += f"- {status_icon} **{milestone['name']}**: {milestone['date']}\n"
        
        return content
    
    def _analyze_requirement(self, task: ProductTask) -> Dict:
        """分析需求"""
        logger.info("  分析需求...")
        
        # 需求分析框架
        analysis = {
            "product_name": task.product_name,
            "requirement_type": "functional",
            "stakeholders": task.target_users or ["用户", "业务方", "技术团队"],
            "pain_points": [
                "现有解决方案效率低",
                "用户体验不佳",
                "功能不完善",
            ],
            "user_needs": [
                {"need": "快速完成任务", "priority": "high"},
                {"need": "简单易用", "priority": "high"},
                {"need": "数据可视化", "priority": "medium"},
                {"need": "多平台支持", "priority": "medium"},
            ],
            "technical_requirements": [
                {"requirement": "响应时间<1 秒", "priority": "high"},
                {"requirement": "支持 10 万并发", "priority": "high"},
                {"requirement": "99.9% 可用性", "priority": "high"},
            ],
            "business_requirements": [
                {"requirement": "6 个月内盈利", "priority": "high"},
                {"requirement": "获取 1 万用户", "priority": "medium"},
            ],
            "risks": [
                {"risk": "技术实现难度大", "mitigation": "提前技术预研"},
                {"risk": "市场竞争激烈", "mitigation": "差异化定位"},
            ],
        }
        
        # 保存分析结果
        output_file = f"output/products/{task.product_name}_Requirement_Analysis.md"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        analysis_content = self._format_analysis_markdown(analysis)
        Path(output_file).write_text(analysis_content, encoding='utf-8')
        
        result = {
            "status": "completed",
            "type": "requirement_analysis",
            "output_file": output_file,
            "product_name": task.product_name,
            "user_needs_count": len(analysis["user_needs"]),
            "risks_count": len(analysis["risks"]),
        }
        
        logger.info(f"  ✅ 需求分析完成：{output_file}")
        
        return result
    
    def _format_analysis_markdown(self, analysis: Dict) -> str:
        """格式化分析结果为 Markdown"""
        content = f"# {analysis['product_name']} 需求分析\n\n"
        
        content += "## 📋 概述\n\n"
        content += f"- **产品类型**: {analysis['requirement_type']}\n"
        content += f"- **利益相关者**: {', '.join(analysis['stakeholders'])}\n\n"
        
        content += "## 😫 痛点分析\n\n"
        for pain in analysis["pain_points"]:
            content += f"- {pain}\n"
        content += "\n"
        
        content += "## 🎯 用户需求\n\n"
        for need in analysis["user_needs"]:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(need["priority"], "⚪")
            content += f"- {priority_icon} {need['need']}\n"
        content += "\n"
        
        content += "## 🔧 技术需求\n\n"
        for req in analysis["technical_requirements"]:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(req["priority"], "⚪")
            content += f"- {priority_icon} {req['requirement']}\n"
        content += "\n"
        
        content += "## 💼 业务需求\n\n"
        for req in analysis["business_requirements"]:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(req["priority"], "⚪")
            content += f"- {priority_icon} {req['requirement']}\n"
        content += "\n"
        
        content += "## ⚠️ 风险与应对\n\n"
        for risk in analysis["risks"]:
            content += f"- **风险**: {risk['risk']}\n"
            content += f"  - **应对**: {risk['mitigation']}\n"
        
        return content
    
    def _analyze_data(self, task: ProductTask) -> Dict:
        """数据分析"""
        logger.info("  分析数据...")
        
        # 模拟数据分析
        analysis = {
            "product_name": task.product_name,
            "metrics": {
                "dau": {"current": 5000, "target": 10000, "growth": "+15%"},
                "retention": {"current": "55%", "target": "60%", "growth": "+5%"},
                "conversion": {"current": "3.5%", "target": "5%", "growth": "+10%"},
                "nps": {"current": 45, "target": 50, "growth": "+5"},
            },
            "insights": [
                "用户留存率有待提升",
                "转化率有增长空间",
                "NPS 分数接近目标",
            ],
            "recommendations": [
                "优化 onboarding 流程",
                "增加用户激励体系",
                "改进核心功能体验",
            ],
        }
        
        result = {
            "status": "completed",
            "type": "data_analysis",
            "product_name": task.product_name,
            "metrics": analysis["metrics"],
            "insights": analysis["insights"],
            "recommendations": analysis["recommendations"],
        }
        
        logger.info(f"  ✅ 数据分析完成")
        
        return result
    
    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """获取任务历史"""
        return self.task_history[-limit:]
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        task_types = {}
        for item in self.task_history:
            task_type = item["task"].task_type
            task_types[task_type] = task_types.get(task_type, 0) + 1
        
        return {
            "total_tasks": len(self.task_history),
            "task_types": task_types,
        }


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("📋 PM Agent - 产品管理专家演示")
    logger.info("=" * 60)
    
    # 初始化 Agent
    agent = PMAgent()
    
    # 创建产品任务
    tasks = [
        ProductTask(
            task_type="prd",
            product_name="智能水杯",
            description="智能温控水杯，可追踪饮水量",
            target_users=["健康意识用户", "上班族"],
        ),
        ProductTask(
            task_type="roadmap",
            product_name="智能水杯",
            description="产品发展路线图",
            deadline="2026-12-31",
        ),
        ProductTask(
            task_type="requirement",
            product_name="智能水杯",
            description="需求分析",
            target_users=["用户", "业务方", "技术团队"],
        ),
    ]
    
    # 执行任务
    for task in tasks:
        result = agent.execute(task)
        logger.info(f"   状态：{result['status']}")
        logger.info(f"   输出：{result.get('output_file', 'N/A')}")
        logger.info("")
    
    # 显示统计
    stats = agent.get_statistics()
    logger.info(f"📊 统计信息:")
    logger.info(f"   总任务数：{stats['total_tasks']}")
    logger.info(f"   任务类型：{stats['task_types']}")
    
    logger.info("\n✅ 演示完成！")


if __name__ == "__main__":
    main()
