#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书消息模板库
提供常用的消息模板
"""

from typing import Dict, List, Any
from datetime import datetime


class MessageTemplates:
    """消息模板类"""
    
    @staticmethod
    def system_status_card(status: Dict) -> Dict:
        """
        系统状态卡片
        
        Args:
            status: 系统状态字典
        
        Returns:
            Dict: 卡片内容
        """
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**时间**: {status.get('timestamp', datetime.now().isoformat())}"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**CPU**: {status.get('cpu', 'N/A')}%\n**内存**: {status.get('memory', 'N/A')}%\n**磁盘**: {status.get('disk', 'N/A')}%\n**运行时间**: {status.get('uptime', 'N/A')}"
                }
            }
        ]
        
        # Agent状态
        if 'agents' in status:
            elements.append({"tag": "hr"})
            agent_text = "**Agent状态**:\n"
            for name, agent in status['agents'].items():
                emoji = "🟢" if agent.get('running') else "🔴"
                agent_text += f"{emoji} {name}: {agent.get('status', '未知')}\n"
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": agent_text}
            })
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "🤖 太一系统状态"},
                "template": "blue"
            },
            "elements": elements
        }
    
    @staticmethod
    def task_completion_card(task: Dict) -> Dict:
        """
        任务完成卡片
        
        Args:
            task: 任务信息字典
        
        Returns:
            Dict: 卡片内容
        """
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**任务**: {task.get('name', '未知')}\n**耗时**: {task.get('duration', 'N/A')}s\n**结果**: {task.get('result', '成功')}"
                }
            }
        ]
        
        if task.get('details'):
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**详情**: {task['details']}"
                }
            })
        
        # 添加操作按钮
        if task.get('actions'):
            actions = []
            for action in task['actions']:
                actions.append({
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": action['label']},
                    "type": action.get('type', 'default'),
                    "url": action.get('url', '')
                })
            elements.append({
                "tag": "action",
                "actions": actions
            })
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "✅ 任务完成"},
                "template": "green"
            },
            "elements": elements
        }
    
    @staticmethod
    def alert_card(alert: Dict) -> Dict:
        """
        告警卡片
        
        Args:
            alert: 告警信息字典
        
        Returns:
            Dict: 卡片内容
        """
        level = alert.get('level', 'warning')
        level_colors = {
            'info': 'blue',
            'warning': 'yellow',
            'error': 'red',
            'critical': 'red'
        }
        level_emojis = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'critical': '🚨'
        }
        
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**类型**: {alert.get('type', '未知')}\n**级别**: {level.upper()}\n**消息**: {alert.get('message', '')}"
                }
            }
        ]
        
        if alert.get('suggestion'):
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**建议**: {alert['suggestion']}"
                }
            })
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{level_emojis.get(level, '⚠️')} 系统告警"
                },
                "template": level_colors.get(level, 'yellow')
            },
            "elements": elements
        }
    
    @staticmethod
    def daily_report_card(report: Dict) -> Dict:
        """
        日报卡片
        
        Args:
            report: 日报数据字典
        
        Returns:
            Dict: 卡片内容
        """
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**日期**: {report.get('date', datetime.now().strftime('%Y-%m-%d'))}"
                }
            },
            {"tag": "hr"}
        ]
        
        # 已完成
        if report.get('completed'):
            completed_text = "**已完成**:\n"
            for item in report['completed']:
                completed_text += f"- ✅ {item}\n"
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": completed_text}
            })
        
        # 进行中
        if report.get('in_progress'):
            elements.append({"tag": "hr"})
            progress_text = "**进行中**:\n"
            for item in report['in_progress']:
                progress_text += f"- 🔄 {item}\n"
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": progress_text}
            })
        
        # 待处理
        if report.get('pending'):
            elements.append({"tag": "hr"})
            pending_text = "**待处理**:\n"
            for item in report['pending']:
                pending_text += f"- ⏳ {item}\n"
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": pending_text}
            })
        
        # 统计
        elements.append({"tag": "hr"})
        stats_text = f"""**统计**:
- 完成: {len(report.get('completed', []))}
- 进行中: {len(report.get('in_progress', []))}
- 待处理: {len(report.get('pending', []))}"""
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": stats_text}
        })
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "📊 太一日报"},
                "template": "blue"
            },
            "elements": elements
        }
    
    @staticmethod
    def product_analysis_card(product: Dict) -> Dict:
        """
        产品分析卡片
        
        Args:
            product: 产品信息字典
        
        Returns:
            Dict: 卡片内容
        """
        score = product.get('score', 0)
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**产品**: {product.get('name', '未知')}\n**评分**: {score}/100\n**利润**: {product.get('profit', 'N/A')}%"
                }
            }
        ]
        
        # BOC四维度评分
        if 'boc_scores' in product:
            elements.append({"tag": "hr"})
            boc_text = "**BOC评估**:\n"
            for dimension, score in product['boc_scores'].items():
                boc_text += f"- {dimension}: {score}分\n"
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": boc_text}
            })
        
        # 建议
        if product.get('suggestion'):
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**建议**: {product['suggestion']}"
                }
            })
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "🎯 选品分析"},
                "template": score_color
            },
            "elements": elements
        }
    
    @staticmethod
    def travel_plan_card(plan: Dict) -> Dict:
        """
        旅游规划卡片
        
        Args:
            plan: 旅游规划字典
        
        Returns:
            Dict: 卡片内容
        """
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**目的地**: {plan.get('destination', '未知')}\n**最佳日期**: {plan.get('best_date', 'N/A')}\n**最低票价**: {plan.get('lowest_price', 'N/A')}"
                }
            }
        ]
        
        # 推荐酒店
        if plan.get('hotels'):
            elements.append({"tag": "hr"})
            hotel_text = "**推荐酒店**:\n"
            for hotel in plan['hotels']:
                hotel_text += f"- {hotel['name']}: {hotel['price']}/晚, {hotel['rating']}⭐\n"
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": hotel_text}
            })
        
        # 省钱技巧
        if plan.get('tips'):
            elements.append({"tag": "hr"})
            tips_text = "**省钱技巧**:\n"
            for tip in plan['tips']:
                tips_text += f"- 💡 {tip}\n"
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": tips_text}
            })
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "✈️ 旅游规划"},
                "template": "blue"
            },
            "elements": elements
        }


# 便捷函数
def get_template(template_name: str, data: Dict) -> Dict:
    """
    获取消息模板
    
    Args:
        template_name: 模板名称
        data: 模板数据
    
    Returns:
        Dict: 模板内容
    """
    templates = {
        "system_status": MessageTemplates.system_status_card,
        "task_completion": MessageTemplates.task_completion_card,
        "alert": MessageTemplates.alert_card,
        "daily_report": MessageTemplates.daily_report_card,
        "product_analysis": MessageTemplates.product_analysis_card,
        "travel_plan": MessageTemplates.travel_plan_card,
    }
    
    template_func = templates.get(template_name)
    if template_func:
        return template_func(data)
    else:
        return {"error": f"未知模板: {template_name}"}


if __name__ == "__main__":
    print("🚀 消息模板测试")
    
    # 测试系统状态模板
    status = {
        "cpu": 45,
        "memory": 60,
        "disk": 30,
        "uptime": "24:00:00",
        "agents": {
            "cross_border_trade": {"running": True, "status": "运行中"},
            "travel_explorer": {"running": True, "status": "运行中"},
            "maigret": {"running": False, "status": "待机"}
        }
    }
    
    card = MessageTemplates.system_status_card(status)
    print(f"\n📊 系统状态卡片: {card['header']['title']['content']}")
    
    # 测试任务完成模板
    task = {
        "name": "选品分析",
        "duration": 2.3,
        "result": "成功",
        "details": "找到3个高潜力产品"
    }
    
    card = MessageTemplates.task_completion_card(task)
    print(f"\n✅ 任务完成卡片: {card['header']['title']['content']}")
    
    # 测试告警模板
    alert = {
        "type": "资源不足",
        "level": "warning",
        "message": "磁盘空间不足80%",
        "suggestion": "建议清理日志文件"
    }
    
    card = MessageTemplates.alert_card(alert)
    print(f"\n⚠️ 告警卡片: {card['header']['title']['content']}")
    
    print("\n✅ 测试完成")
