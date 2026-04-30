#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 目的地注意事项

包含：民俗习惯、宗教信仰、法律法规、禁忌事项、礼仪规范、
      消费提示、安全提示、最佳季节、建议天数、预算范围
"""

from typing import Dict, List, Any
from datetime import datetime


class DestinationNotices:
    """目的地注意事项"""

    NOTICES_DB: Dict[str, Dict] = {
        "日本": {
            "民俗习惯": ["进入室内需脱鞋", "泡温泉前需洗净身体", "用餐时说'我开动了'", "公共场所保持安静", "垃圾分类严格"],
            "法律法规": ["禁止边走边吃", "禁止在地铁打电话", "禁止乱扔垃圾(罚款最高5万日元)", "20岁以下禁止饮酒"],
            "禁忌事项": ["不要给现金小费", "不要用筷子传递食物", "不要指着别人说话"],
            "礼仪规范": ["见面鞠躬问候", "双手递接物品", "排队守秩序"],
            "消费提示": ["消费税10%", "大部分商店不讲价", "便利店可取现金"],
            "安全提示": ["地震多发，了解避难路线", "紧急电话：110/119", "中国驻日使领馆：+81-3-3403-3065"],
            "最佳季节": "3-5月(樱花)/10-11月(红叶)",
            "建议天数": "5-7天",
        },
        "韩国": {
            "民俗习惯": ["进入室内需脱鞋", "长辈先动筷", "倒酒时双手"],
            "法律法规": ["禁止随地吐痰(罚款)", "禁止在地铁饮食", "19岁以下禁止吸烟饮酒"],
            "禁忌事项": ["不要用红笔写名字", "不要插筷子在饭里"],
            "礼仪规范": ["对长辈用敬语", "双手递接物品"],
            "消费提示": ["增值税10%", "明洞可讲价", "支付宝/微信普及"],
            "安全提示": ["紧急电话：112/119", "中国驻韩使领馆：+82-2-755-0572"],
            "最佳季节": "4-5月/9-10月",
            "建议天数": "4-6天",
        },
        "泰国": {
            "民俗习惯": ["双手合十问候(Wai)", "进入寺庙需脱鞋", "不要摸别人头"],
            "法律法规": ["禁止批评王室(严重犯罪)", "禁止赌博", "禁止携带电子烟"],
            "禁忌事项": ["不要触摸他人头部", "不要用脚指向人或佛像"],
            "礼仪规范": ["双手合十问候", "脱鞋进入室内"],
            "消费提示": ["增值税7%", "可讲价(市场/夜市)", "小费普遍(20-100泰铢)"],
            "安全提示": ["紧急电话：191/1669", "谨防出租车宰客"],
            "最佳季节": "11月-次年2月(凉季)",
            "建议天数": "5-7天",
        },
        "新加坡": {
            "民俗习惯": ["多元文化融合", "公共场所保持安静"],
            "法律法规": ["禁止随地吐痰(罚款1000新元)", "禁止乱扔垃圾", "禁止在地铁饮食", "毒品犯罪可判死刑"],
            "禁忌事项": ["不要闯红灯", "不要在禁烟区吸烟"],
            "礼仪规范": ["排队守秩序", "尊重多元文化"],
            "消费提示": ["消费税9%", "大部分商店不讲价"],
            "安全提示": ["紧急电话：999/995", "治安良好"],
            "最佳季节": "全年适宜",
            "建议天数": "3-5天",
        },
    }

    def get_notices(self, destination: str) -> Dict[str, Any]:
        """获取目的地注意事项"""
        matched = None
        for name in self.NOTICES_DB:
            if name in destination or destination in name:
                matched = name
                break

        if not matched:
            return {"success": False, "message": f"未找到 {destination} 的注意事项", "available": list(self.NOTICES_DB.keys())}

        notices = self.NOTICES_DB[matched]
        return {
            "success": True,
            "destination": matched,
            "notices": notices,
            "retrieved_at": datetime.now().isoformat(),
        }

    def get_summary(self, destination: str) -> str:
        """获取风俗摘要"""
        result = self.get_notices(destination)
        if not result["success"]:
            return result["message"]
        notices = result["notices"]
        lines = [f"📋 {destination} 旅行注意事项\n"]
        for category in ["民俗习惯", "法律法规", "禁忌事项", "安全提示"]:
            lines.append(f"\n{category}:")
            for item in notices.get(category, [])[:5]:
                lines.append(f"  • {item}")
        lines.append(f"\n最佳季节：{notices.get('最佳季节', 'N/A')}")
        lines.append(f"建议天数：{notices.get('建议天数', 'N/A')}")
        return "\n".join(lines)

    def add_destination(self, destination: str, notices: Dict) -> None:
        """添加新目的地"""
        self.NOTICES_DB[destination] = notices








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48