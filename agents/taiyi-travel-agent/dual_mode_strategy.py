#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅行双模式策略模块 - Dual Mode Travel Strategy

功能:
1. 国内旅游模式
2. 跨国旅游模式
3. 不同市场环境分析
4. 不同旅游策略推荐
5. 风险评估与建议

作者：太一 AGI
创建：2026-04-14
"""

from typing import Dict, List
from datetime import datetime


class DualModeTravelStrategy:
    """双模式旅游策略模块"""
    
    def __init__(self):
        # 国内旅游特点
        self.domestic_features = {
            "语言": "中文，无沟通障碍",
            "货币": "人民币，无兑换需求",
            "支付": "支付宝/微信普及",
            "网络": "国内网络畅通",
            "交通": "高铁/飞机/自驾发达",
            "签证": "无需签证",
            "时差": "无时差",
            "饮食": "符合中国口味",
            "文化": "文化相近",
            "安全": "治安良好",
        }
        
        # 跨国旅游特点
        self.international_features = {
            "语言": "可能需要外语/翻译",
            "货币": "需要兑换外币",
            "支付": "信用卡/现金为主",
            "网络": "需要漫游/当地卡",
            "交通": "飞机/火车/当地交通",
            "签证": "可能需要签证",
            "时差": "可能有时差",
            "饮食": "可能需要适应",
            "文化": "文化差异大",
            "安全": "需注意当地安全",
        }
        
        # 国内热门目的地
        self.domestic_destinations = {
            "北京": {
                "类型": "历史文化",
                "建议天数": "4-5 天",
                "最佳季节": "9-11 月",
                "预算": "¥3000-5000/人",
                "亮点": ["故宫", "长城", "颐和园", "天坛"],
            },
            "上海": {
                "类型": "现代都市",
                "建议天数": "3-4 天",
                "最佳季节": "3-5 月",
                "预算": "¥4000-6000/人",
                "亮点": ["外滩", "迪士尼", "东方明珠", "豫园"],
            },
            "成都": {
                "类型": "休闲美食",
                "建议天数": "3-4 天",
                "最佳季节": "3-6 月",
                "预算": "¥2500-4000/人",
                "亮点": ["大熊猫", "宽窄巷子", "火锅", "都江堰"],
            },
            "西安": {
                "类型": "历史文化",
                "建议天数": "3-4 天",
                "最佳季节": "3-5 月",
                "预算": "¥2500-4000/人",
                "亮点": ["兵马俑", "大雁塔", "城墙", "回民街"],
            },
            "云南": {
                "类型": "自然风光",
                "建议天数": "6-8 天",
                "最佳季节": "10 月 - 次年 4 月",
                "预算": "¥4000-7000/人",
                "亮点": ["丽江", "大理", "香格里拉", "西双版纳"],
            },
        }
        
        # 国外热门目的地
        self.international_destinations = {
            "日本": {
                "类型": "文化购物",
                "建议天数": "5-7 天",
                "最佳季节": "3-5 月/10-11 月",
                "预算": "¥8000-15000/人",
                "签证": "需要 (简化)",
                "亮点": ["东京", "大阪", "京都", "富士山"],
            },
            "韩国": {
                "类型": "购物美食",
                "建议天数": "4-6 天",
                "最佳季节": "4-5 月/9-10 月",
                "预算": "¥5000-10000/人",
                "签证": "济州岛免签",
                "亮点": ["首尔", "济州岛", "釜山"],
            },
            "泰国": {
                "类型": "海岛度假",
                "建议天数": "5-7 天",
                "最佳季节": "11 月 - 次年 2 月",
                "预算": "¥4000-8000/人",
                "签证": "落地签",
                "亮点": ["曼谷", "普吉岛", "清迈"],
            },
            "新加坡": {
                "类型": "城市观光",
                "建议天数": "3-5 天",
                "最佳季节": "全年",
                "预算": "¥8000-15000/人",
                "签证": "需要",
                "亮点": ["滨海湾", "环球影城", "动物园"],
            },
            "法国": {
                "类型": "文化浪漫",
                "建议天数": "7-10 天",
                "最佳季节": "5-10 月",
                "预算": "¥15000-30000/人",
                "签证": "申根签证",
                "亮点": ["巴黎", "普罗旺斯", "尼斯"],
            },
        }
    
    def get_travel_mode(self, origin: str, destination: str) -> str:
        """
        判断旅游模式 (国内/跨国)
        
        Args:
            origin: 出发地
            destination: 目的地
        
        Returns:
            旅游模式 (domestic/international)
        """
        # 简化判断：出发地为中国则为国内，否则为跨国
        china_cities = ["北京", "上海", "广州", "深圳", "成都", "西安", "杭州", "南京"]
        
        if any(city in origin for city in china_cities):
            if any(city in destination for city in china_cities) or \
               any(province in destination for province in ["云南", "四川", "陕西", "浙江", "江苏"]):
                return "domestic"
        
        return "international"
    
    def get_domestic_strategy(self, destination: str) -> Dict:
        """
        获取国内旅游策略
        
        Args:
            destination: 目的地
        
        Returns:
            国内旅游策略
        """
        dest_info = self.domestic_destinations.get(destination, {})
        
        strategy = {
            "mode": "domestic",
            "destination": destination,
            "market_environment": {
                "语言环境": "中文，无沟通障碍",
                "支付环境": "支付宝/微信普及，几乎无需现金",
                "网络环境": "国内网络畅通，无需漫游",
                "交通环境": "高铁/飞机/自驾发达，预订方便",
                "住宿环境": "酒店/民宿选择多，价格透明",
                "餐饮环境": "符合中国口味，选择丰富",
                "安全环境": "治安良好，紧急求助方便",
            },
            "travel_strategy": {
                "行前准备": [
                    "身份证必带",
                    "手机充电宝",
                    "下载地图 App",
                    "预订酒店/机票",
                ],
                "交通建议": [
                    "优先高铁 (准点/舒适)",
                    "提前预订机票 (便宜)",
                    "市内地铁/打车方便",
                ],
                "住宿建议": [
                    "选择市中心/地铁口",
                    "连锁酒店品质稳定",
                    "民宿体验当地生活",
                ],
                "餐饮建议": [
                    "尝试当地特色",
                    "使用大众点评",
                    "注意饮食卫生",
                ],
                "购物建议": [
                    "使用支付宝/微信",
                    "注意比价",
                    "保留购物凭证",
                ],
                "预算控制": [
                    "淡季出行更便宜",
                    "提前预订有优惠",
                    "使用优惠券/会员卡",
                ],
            },
            "destination_info": dest_info,
            "tips": [
                "国内游相对轻松，无需太多准备",
                "节假日人流量大，建议错峰出行",
                "热门景点提前网上购票",
                "注意天气变化，带好相应衣物",
            ],
        }
        
        return strategy
    
    def get_international_strategy(self, destination: str) -> Dict:
        """
        获取跨国旅游策略
        
        Args:
            destination: 目的地
        
        Returns:
            跨国旅游策略
        """
        dest_info = self.international_destinations.get(destination, {})
        
        strategy = {
            "mode": "international",
            "destination": destination,
            "market_environment": {
                "语言环境": "可能需要外语/翻译 App",
                "支付环境": "信用卡/现金为主，部分可用支付宝",
                "网络环境": "需要漫游/当地电话卡",
                "交通环境": "飞机/火车，需提前规划",
                "住宿环境": "酒店/民宿，注意位置安全",
                "餐饮环境": "可能需要适应当地口味",
                "安全环境": "需注意当地安全提示",
            },
            "travel_strategy": {
                "行前准备": [
                    "护照 (有效期 6 个月以上)",
                    "签证 (如需)",
                    "兑换外币",
                    "购买旅游保险",
                    "下载翻译 App",
                    "准备国际信用卡",
                    "复印重要文件",
                ],
                "交通建议": [
                    "提前预订国际机票",
                    "了解当地交通规则",
                    "下载当地交通 App",
                    "准备交通卡",
                ],
                "住宿建议": [
                    "选择安全区域",
                    "查看住客评价",
                    "确认入住时间",
                    "保存酒店地址 (当地语言)",
                ],
                "餐饮建议": [
                    "尝试当地特色",
                    "注意饮食卫生",
                    "了解用餐礼仪",
                    "准备常用药",
                ],
                "购物建议": [
                    "了解退税政策",
                    "使用信用卡 (有汇率优势)",
                    "保留购物凭证",
                    "注意海关规定",
                ],
                "预算控制": [
                    "淡季出行更便宜",
                    "提前 3 个月订机票",
                    "使用比价网站",
                    "准备应急资金",
                ],
                "安全提示": [
                    "保管好护照和贵重物品",
                    "避免夜间单独出行",
                    "记住使领馆电话",
                    "购买旅游保险",
                    "了解当地紧急电话",
                ],
            },
            "destination_info": dest_info,
            "tips": [
                "跨国游需要更多行前准备",
                "尊重当地文化和习俗",
                "注意时差调整",
                "保持通讯畅通",
                "购买旅游保险很重要",
            ],
        }
        
        return strategy
    
    def compare_modes(self) -> Dict:
        """
        对比国内/跨国旅游模式
        
        Returns:
            对比结果
        """
        comparison = {
            "国内旅游": {
                "优势": [
                    "无语言障碍",
                    "无时差",
                    "支付方便",
                    "无需签证",
                    "安全系数高",
                    "预算相对低",
                ],
                "劣势": [
                    "文化差异小",
                    "新鲜感相对低",
                    "节假日人多",
                ],
                "适合人群": [
                    "首次旅游者",
                    "带老人/小孩出行",
                    "预算有限",
                    "时间紧张",
                ],
                "预算范围": "¥2000-8000/人",
                "建议天数": "3-8 天",
            },
            "跨国旅游": {
                "优势": [
                    "文化体验丰富",
                    "新鲜感强",
                    "购物选择多",
                    "拍照打卡点多",
                ],
                "劣势": [
                    "需要语言准备",
                    "时差影响",
                    "行前准备复杂",
                    "预算相对高",
                    "安全风险相对高",
                ],
                "适合人群": [
                    "有旅游经验者",
                    "年轻人",
                    "预算充足",
                    "时间充裕",
                ],
                "预算范围": "¥5000-30000+/人",
                "建议天数": "5-15 天",
            },
        }
        
        return comparison
    
    def generate_strategy_report(self, origin: str, destinations: List[str]) -> str:
        """
        生成旅游策略报告
        
        Args:
            origin: 出发地
            destinations: 目的地列表
        
        Returns:
            报告文本
        """
        print(f"\n📊 生成旅游策略报告")
        
        report = "# 🌏 太一旅行双模式策略报告\n\n"
        report += f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"> **出发地**: {origin}\n"
        report += f"> **目的地**: {', '.join(destinations)}\n\n"
        
        report += "---\n\n"
        
        # 判断每个目的地的模式
        for dest in destinations:
            mode = self.get_travel_mode(origin, dest)
            
            if mode == "domestic":
                strategy = self.get_domestic_strategy(dest)
                report += f"## 🇨🇳 {dest} (国内游)\n\n"
            else:
                strategy = self.get_international_strategy(dest)
                report += f"## 🌍 {dest} (跨国游)\n\n"
            
            report += "### 市场环境\n\n"
            for key, value in strategy["market_environment"].items():
                report += f"- **{key}**: {value}\n"
            report += "\n"
            
            report += "### 旅游策略\n\n"
            for category, items in strategy["travel_strategy"].items():
                report += f"#### {category}\n"
                for item in items[:5]:  # 只显示前 5 条
                    report += f"- {item}\n"
                report += "\n"
            
            report += "### 旅行贴士\n\n"
            for tip in strategy["tips"]:
                report += f"- {tip}\n"
            report += "\n"
            
            report += "---\n\n"
        
        # 添加模式对比
        comparison = self.compare_modes()
        report += "## 📊 国内游 vs 跨国游对比\n\n"
        
        report += "### 国内旅游\n\n"
        report += "**优势**:\n"
        for item in comparison["国内旅游"]["优势"]:
            report += f"- {item}\n"
        report += "\n"
        
        report += "**适合人群**:\n"
        for item in comparison["国内旅游"]["适合人群"]:
            report += f"- {item}\n"
        report += f"\n**预算**: {comparison['国内旅游']['预算范围']}\n"
        report += f"**建议天数**: {comparison['国内旅游']['建议天数']}\n\n"
        
        report += "### 跨国旅游\n\n"
        report += "**优势**:\n"
        for item in comparison["跨国旅游"]["优势"]:
            report += f"- {item}\n"
        report += "\n"
        
        report += "**适合人群**:\n"
        for item in comparison["跨国旅游"]["适合人群"]:
            report += f"- {item}\n"
        report += f"\n**预算**: {comparison['跨国旅游']['预算范围']}\n"
        report += f"**建议天数**: {comparison['跨国旅游']['建议天数']}\n\n"
        
        return report
    
    def recommend_mode(self, traveler_profile: Dict) -> str:
        """
        根据旅行者画像推荐模式
        
        Args:
            traveler_profile: 旅行者画像
                - experience: 旅游经验 (beginner/intermediate/advanced)
                - budget: 预算 (low/medium/high)
                - time: 时间 (short/medium/long)
                - preference: 偏好 (relaxed/adventurous)
        
        Returns:
            推荐模式
        """
        experience = traveler_profile.get("experience", "beginner")
        budget = traveler_profile.get("budget", "medium")
        time = traveler_profile.get("time", "medium")
        
        # 推荐逻辑
        if experience == "beginner" or budget == "low" or time == "short":
            return "domestic"
        elif experience == "advanced" and budget == "high" and time == "long":
            return "international"
        else:
            return "depends"  # 视具体情况而定


def main():
    """测试"""
    print("=" * 60)
    print("🌏 太一旅行双模式策略测试")
    print("=" * 60)
    
    strategy = DualModeTravelStrategy()
    
    # 测试 1: 判断旅游模式
    print("\n🎯 测试 1: 判断旅游模式")
    mode1 = strategy.get_travel_mode("北京", "上海")
    mode2 = strategy.get_travel_mode("北京", "东京")
    print(f"  北京→上海：{mode1} (国内)")
    print(f"  北京→东京：{mode2} (跨国)")
    
    # 测试 2: 获取国内策略
    print("\n🇨🇳 测试 2: 获取国内策略")
    domestic = strategy.get_domestic_strategy("成都")
    print(f"  目的地：{domestic['destination']}")
    print(f"  建议天数：{domestic['destination_info'].get('建议天数', 'N/A')}")
    
    # 测试 3: 获取跨国策略
    print("\n🌍 测试 3: 获取跨国策略")
    international = strategy.get_international_strategy("日本")
    print(f"  目的地：{international['destination']}")
    print(f"  签证：{international['destination_info'].get('签证', 'N/A')}")
    
    # 测试 4: 对比模式
    print("\n📊 测试 4: 对比模式")
    comparison = strategy.compare_modes()
    print(f"  国内游优势：{len(comparison['国内旅游']['优势'])} 个")
    print(f"  跨国游优势：{len(comparison['跨国旅游']['优势'])} 个")
    
    # 测试 5: 生成策略报告
    print("\n📝 测试 5: 生成策略报告")
    report = strategy.generate_strategy_report(
        origin="北京",
        destinations=["上海", "日本", "成都", "泰国"]
    )
    print(report[:1000])
    
    # 测试 6: 推荐模式
    print("\n💡 测试 6: 推荐模式")
    profile1 = {"experience": "beginner", "budget": "low", "time": "short"}
    profile2 = {"experience": "advanced", "budget": "high", "time": "long"}
    rec1 = strategy.recommend_mode(profile1)
    rec2 = strategy.recommend_mode(profile2)
    print(f"  新手/低预算/短时间：{rec1}")
    print(f"  老手/高预算/长时间：{rec2}")
    
    print("\n" + "=" * 60)
    print("✅ 双模式策略测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
