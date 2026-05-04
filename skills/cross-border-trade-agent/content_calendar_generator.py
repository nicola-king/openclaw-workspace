#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容日历生成模块 - 6 个月内容规划
太一 AGI · 2026-04-19 19:46

功能:
- 6 个月内容日历生成
- 多平台内容排期
- 内容主题规划
- 节假日/活动整合
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('ContentCalendarGenerator')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
CALENDAR_DIR = WORKSPACE / "data" / "cross-border" / "content_calendar"
CALENDAR_DIR.mkdir(parents=True, exist_ok=True)


class ContentCalendarGenerator:
    """内容日历生成模块"""
    
    CONTENT_THEMES = {
        "Monday": "industry_insight",      # 周一：行业见解
        "Tuesday": "company_news",          # 周二：公司动态
        "Wednesday": "case_study",          # 周三：成功案例
        "Thursday": "faq",                  # 周四：常见问题
        "Friday": "weekly_summary",         # 周五：本周总结
        "Saturday": "team_culture",         # 周六：团队文化
        "Sunday": "rest"                    # 周日：休息
    }
    
    PLATFORM_STRATEGY = {
        "LinkedIn": ["industry_insight", "case_study", "weekly_summary"],
        "Facebook": ["company_news", "faq", "team_culture"],
        "YouTube": ["tutorial", "factory_tour", "product_review"]
    }
    
    def __init__(self):
        self.calendar_file = CALENDAR_DIR / "content_calendar.json"
        self.calendar = self._load_calendar()
    
    def _load_calendar(self) -> Dict:
        if self.calendar_file.exists():
            with open(self.calendar_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"start_date": None, "months": 6, "weeks": [], "special_events": []}
    
    def generate_calendar(self, months: int = 6, start_date: str = None) -> Dict:
        """生成 6 个月内容日历"""
        if not start_date:
            start_date = datetime.now()
        elif isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        
        self.calendar["start_date"] = start_date.isoformat()
        self.calendar["months"] = months
        self.calendar["weeks"] = []
        
        current_date = start_date
        week_num = 1
        
        for month in range(months):
            for week in range(4):  # 每月 4 周
                week_calendar = self._generate_week_calendar(current_date, week_num)
                self.calendar["weeks"].append(week_calendar)
                week_num += 1
                current_date += timedelta(days=7)
        
        # 添加特殊事件
        self.calendar["special_events"] = self._add_special_events()
        
        self._save_calendar()
        
        logger.info(f"✅ {months}个月内容日历已生成")
        logger.info(f"  开始日期：{start_date.strftime('%Y-%m-%d')}")
        logger.info(f"  总周数：{len(self.calendar['weeks'])}周")
        
        return self.calendar
    
    def _generate_week_calendar(self, start_date: datetime, week_num: int) -> Dict:
        """生成单周日历"""
        week = {
            "week": week_num,
            "date_range": f"{start_date.strftime('%Y-%m-%d')} - {(start_date + timedelta(days=6)).strftime('%Y-%m-%d')}",
            "posts": []
        }
        
        for day_offset in range(7):
            current_day = start_date + timedelta(days=day_offset)
            day_name = current_day.strftime("%A")
            theme = self.CONTENT_THEMES.get(day_name, "rest")
            
            if theme != "rest":
                post = {
                    "date": current_day.strftime('%Y-%m-%d'),
                    "day": day_name,
                    "theme": theme,
                    "platforms": self._get_platforms_for_theme(theme),
                    "status": "planned",
                    "content_brief": f"{theme} 内容规划"
                }
                week["posts"].append(post)
        
        return week
    
    def _get_platforms_for_theme(self, theme: str) -> List[str]:
        """根据主题获取适合平台"""
        platforms = []
        for platform, themes in self.PLATFORM_STRATEGY.items():
            if theme in themes:
                platforms.append(platform)
        return platforms if platforms else ["LinkedIn", "Facebook"]
    
    def _add_special_events(self) -> List[Dict]:
        """添加特殊事件"""
        events = [
            {"date": "2026-05-01", "event": "劳动节", "content_suggestion": "团队文化/放假通知"},
            {"date": "2026-07-04", "event": "美国独立日", "content_suggestion": "节日祝福"},
            {"date": "2026-10-01", "event": "中国国庆节", "content_suggestion": "放假通知/节日祝福"},
            {"date": "2026-11-26", "event": "感恩节", "content_suggestion": "感谢客户"},
            {"date": "2026-12-25", "event": "圣诞节", "content_suggestion": "节日祝福/年度总结"}
        ]
        return events
    
    def export_calendar(self, format: str = "json") -> str:
        """导出日历"""
        if format == "json":
            return json.dumps(self.calendar, indent=2, ensure_ascii=False)
        elif format == "csv":
            return self._export_csv()
        return ""
    
    def _export_csv(self) -> str:
        """导出为 CSV 格式"""
        csv_lines = ["Week,Date,Day,Theme,Platform,Status"]
        for week in self.calendar["weeks"]:
            for post in week["posts"]:
                csv_lines.append(f"{week['week']},{post['date']},{post['day']},{post['theme']},{','.join(post['platforms'])},{post['status']}")
        return "\n".join(csv_lines)
    
    def _save_calendar(self):
        with open(self.calendar_file, 'w', encoding='utf-8') as f:
            json.dump(self.calendar, f, indent=2, ensure_ascii=False)
    
    def get_calendar_summary(self) -> Dict:
        """获取日历摘要"""
        total_posts = sum(len(w["posts"]) for w in self.calendar["weeks"])
        return {
            "start_date": self.calendar["start_date"],
            "months": self.calendar["months"],
            "total_weeks": len(self.calendar["weeks"]),
            "total_posts": total_posts,
            "special_events": len(self.calendar["special_events"]),
            "posts_per_week": round(total_posts / len(self.calendar["weeks"]), 1) if self.calendar["weeks"] else 0
        }


def main():
    logger.info("=" * 60)
    logger.info("📅 内容日历生成模块 - 6 个月内容规划")
    logger.info("=" * 60)
    
    generator = ContentCalendarGenerator()
    
    # 生成日历
    logger.info(f"\n📋 生成 6 个月内容日历...")
    calendar = generator.generate_calendar(months=6)
    
    # 显示前 4 周
    logger.info(f"\n📅 前 4 周内容安排:")
    for week in calendar["weeks"][:4]:
        logger.info(f"  第{week['week']}周 ({week['date_range']}):")
        for post in week["posts"]:
            logger.info(f"    {post['day']}: {post['theme']} → {', '.join(post['platforms'])}")
    
    # 显示特殊事件
    logger.info(f"\n🎉 特殊事件:")
    for event in calendar["special_events"]:
        logger.info(f"  {event['date']}: {event['event']} - {event['content_suggestion']}")
    
    # 获取摘要
    logger.info(f"\n📊 日历摘要:")
    summary = generator.get_calendar_summary()
    logger.info(f"  开始日期：{summary['start_date']}")
    logger.info(f"  总月数：{summary['months']}个月")
    logger.info(f"  总周数：{summary['total_weeks']}周")
    logger.info(f"  总帖子数：{summary['total_posts']}个")
    logger.info(f"  每周平均：{summary['posts_per_week']}个")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
