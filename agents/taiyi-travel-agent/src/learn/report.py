#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 学习报告生成器
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class LearningReportGenerator:
    """学习报告生成器"""

    def generate(
        self,
        blogger_result: Dict,
        website_result: Dict,
        guides: Dict,
        output_dir: Path = None,
    ) -> Path:
        """
        生成学习报告

        Args:
            blogger_result: 博主学习结果
            website_result: 网站学习结果
            guides: 攻略提取结果
            output_dir: 输出目录

        Returns:
            报告文件路径
        """
        output_dir = output_dir or Path(__file__).parent.parent.parent / "data" / "auto-learning"
        output_dir.mkdir(parents=True, exist_ok=True)

        report_file = output_dir / f"learning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        content = f"""# 📚 太一旅行知识学习报告

> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


## 📺 博主学习




- 学习博主数：{blogger_result.get('bloggers_learned', 0)}
- 区域：{blogger_result.get('region', 'N/A')}

"""
        for item in blogger_result.get("content", [])[:5]:
            content += f"- **{item.get('blogger', 'N/A')}** ({item.get('platform', 'N/A')})\n"

        content += f"""

## 🌐 网站学习




- 学习网站数：{website_result.get('websites_learned', 0)}
- 区域：{website_result.get('region', 'N/A')}

"""
        for item in website_result.get("content", [])[:5]:
            content += f"- **{item.get('source', 'N/A')}** ({item.get('focus', 'N/A')})\n"

        content += f"""

## 📖 攻略提取




"""
        for dest, guide in list(guides.items())[:10]:
            content += f"### {dest}\n"
            content += f"- 建议游玩：{guide.get('suggested_days', 'N/A')} 天\n"
            content += f"- 必去景点：{len(guide.get('must_visit', []))} 个\n\n"

        content += f"""

*太一旅行知识自动学习 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        with open(report_file, "w", encoding="utf-8") as f:
            f.write(content)

        return report_file








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48