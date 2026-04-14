#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一旅行落地城市注意事项模块 - Destination Notices

功能:
1. 民俗习惯
2. 宗教信仰
3. 法律法规
4. 禁忌事项
5. 安全提示
6. 礼仪规范
7. 消费提示
8. 紧急联系方式

作者：太一 AGI
创建：2026-04-14
"""

from typing import Dict, List
from datetime import datetime


class DestinationNotices:
    """落地城市注意事项模块"""
    
    def __init__(self):
        # 目的地注意事项数据库
        self.notices_db = {
            "日本": {
                "民俗习惯": [
                    "进入室内需脱鞋",
                    "泡温泉前需洗净身体",
                    "用餐时说'我开动了'(Itadakimasu)",
                    "公共场所保持安静",
                    "垃圾分类严格",
                ],
                "宗教信仰": [
                    "神道教和佛教为主要宗教",
                    "进入神社需洗手漱口",
                    "寺庙内禁止拍照",
                    "参拜时投币许愿",
                ],
                "法律法规": [
                    "禁止边走边吃",
                    "禁止在地铁打电话",
                    "禁止乱扔垃圾 (罚款最高 5 万日元)",
                    "禁止在公共场所吸烟 (指定区域除外)",
                    "20 岁以下禁止饮酒",
                ],
                "禁忌事项": [
                    "不要给现金小费 (被视为不礼貌)",
                    "不要用筷子传递食物 (类似葬礼仪式)",
                    "不要指着别人说话",
                    "不要大声喧哗",
                ],
                "礼仪规范": [
                    "见面鞠躬问候",
                    "双手递接物品",
                    "排队守秩序",
                    "电梯靠左站立 (东京)",
                ],
                "消费提示": [
                    "消费税 10%",
                    "大部分商店不接受讲价",
                    "便利店可取现金",
                    "信用卡普及率高",
                ],
                "安全提示": [
                    "地震多发国家，了解避难路线",
                    "台风季节注意天气预警",
                    "紧急电话：110(报警)/119(急救)",
                    "中国驻日使领馆电话：+81-3-3403-3065",
                ],
                "最佳季节": "3-5 月 (樱花) / 10-11 月 (红叶)",
                "建议天数": "5-7 天",
                "预算范围": {
                    "经济": "¥5000-8000/人/天",
                    "舒适": "¥8000-15000/人/天",
                    "豪华": "¥15000-30000/人/天",
                },
            },
            "韩国": {
                "民俗习惯": [
                    "进入室内需脱鞋",
                    "长辈先动筷",
                    "倒酒时双手",
                    "公共场所不大声喧哗",
                ],
                "宗教信仰": [
                    "佛教、基督教为主要宗教",
                    "进入寺庙需脱鞋",
                    "寺庙内保持安静",
                ],
                "法律法规": [
                    "禁止随地吐痰 (罚款)",
                    "禁止在地铁饮食",
                    "垃圾分类严格",
                    "19 岁以下禁止吸烟饮酒",
                ],
                "禁忌事项": [
                    "不要用红笔写名字 (象征死亡)",
                    "不要踩踏门槛",
                    "不要插筷子在饭里 (类似祭祀)",
                ],
                "礼仪规范": [
                    "对长辈用敬语",
                    "双手递接物品",
                    "见面鞠躬",
                    "电梯内面向门站立",
                ],
                "消费提示": [
                    "增值税 10%",
                    "明洞等地可讲价",
                    "T-money 卡可用于交通",
                    "支付宝/微信普及",
                ],
                "安全提示": [
                    "紧急电话：112(报警)/119(急救)",
                    "中国驻韩使领馆：+82-2-755-0572",
                    "注意交通安全",
                ],
                "最佳季节": "4-5 月 / 9-10 月",
                "建议天数": "4-6 天",
                "预算范围": {
                    "经济": "¥3000-5000/人/天",
                    "舒适": "¥5000-10000/人/天",
                    "豪华": "¥10000-20000/人/天",
                },
            },
            "泰国": {
                "民俗习惯": [
                    "双手合十问候 (Wai)",
                    "进入寺庙需脱鞋",
                    "不要摸别人头 (头部神圣)",
                    "不要用脚指东西",
                ],
                "宗教信仰": [
                    "佛教为国教",
                    "进入寺庙着装得体",
                    "女性不要触碰僧侣",
                    "寺庙内禁止拍照",
                ],
                "法律法规": [
                    "禁止批评王室 (严重犯罪)",
                    "禁止赌博",
                    "禁止携带电子烟",
                    "禁止在公共场所吸烟",
                ],
                "禁忌事项": [
                    "不要触摸他人头部",
                    "不要用脚指向人或佛像",
                    "不要穿着暴露进入寺庙",
                    "不要 disrespect 王室",
                ],
                "礼仪规范": [
                    "双手合十问候",
                    "脱鞋进入室内",
                    "尊重长辈",
                    "微笑待人",
                ],
                "消费提示": [
                    "增值税 7%",
                    "可讲价 (市场/夜市)",
                    "小费普遍 (20-100 泰铢)",
                    "7-11 便利店遍布",
                ],
                "安全提示": [
                    "紧急电话：191(报警)/1669(急救)",
                    "中国驻泰使领馆：+66-2-245-7044",
                    "注意水上安全",
                    "谨防出租车宰客",
                ],
                "最佳季节": "11 月 - 次年 2 月 (凉季)",
                "建议天数": "5-7 天",
                "预算范围": {
                    "经济": "¥2000-4000/人/天",
                    "舒适": "¥4000-8000/人/天",
                    "豪华": "¥8000-15000/人/天",
                },
            },
            "新加坡": {
                "民俗习惯": [
                    "多元文化融合",
                    "进入室内需脱鞋",
                    "公共场所保持安静",
                    "垃圾分类",
                ],
                "宗教信仰": [
                    "佛教、伊斯兰教、基督教、印度教",
                    "尊重各宗教习俗",
                    "进入宗教场所着装得体",
                ],
                "法律法规": [
                    "禁止随地吐痰 (罚款最高 1000 新元)",
                    "禁止乱扔垃圾 (罚款最高 1000 新元)",
                    "禁止在地铁饮食 (罚款最高 500 新元)",
                    "禁止携带口香糖入境",
                    "禁止在公共场所吸烟",
                    "毒品犯罪可判死刑",
                ],
                "禁忌事项": [
                    "不要闯红灯",
                    "不要在禁烟区吸烟",
                    "不要携带违禁品",
                ],
                "礼仪规范": [
                    "排队守秩序",
                    "公共场所不大声喧哗",
                    "尊重多元文化",
                    "使用礼貌用语",
                ],
                "消费提示": [
                    "消费税 9%",
                    "大部分商店不讲价",
                    "信用卡普及",
                    "支付宝/微信可用",
                ],
                "安全提示": [
                    "紧急电话：999(报警)/995(急救)",
                    "中国驻新使领馆：+65-6471-2117",
                    "治安良好",
                    "注意防暑",
                ],
                "最佳季节": "全年适宜",
                "建议天数": "3-5 天",
                "预算范围": {
                    "经济": "¥5000-8000/人/天",
                    "舒适": "¥8000-15000/人/天",
                    "豪华": "¥15000-30000/人/天",
                },
            },
            "法国": {
                "民俗习惯": [
                    "见面贴面礼",
                    "用餐礼仪讲究",
                    "商店周日休息",
                    "午餐时间较长 (12:00-14:00)",
                ],
                "宗教信仰": [
                    "天主教为主要宗教",
                    "进入教堂着装得体",
                    "保持安静",
                ],
                "法律法规": [
                    "禁止在公共场所吸烟",
                    "禁止携带危险品",
                    "禁止拍照的地方遵守规定",
                    "21 岁以下禁止饮酒",
                ],
                "禁忌事项": [
                    "不要讨论宗教/政治敏感话题",
                    "不要不尊重艺术品",
                    "不要插队",
                ],
                "礼仪规范": [
                    "见面说 Bonjour(你好)",
                    "离开说 Au revoir(再见)",
                    "用餐时手放桌上",
                    "小费 10-15%",
                ],
                "消费提示": [
                    "增值税 20%",
                    "可退税 (消费满 100 欧)",
                    "餐厅服务费已包含",
                    "信用卡普及",
                ],
                "安全提示": [
                    "紧急电话：112(欧盟通用)",
                    "中国驻法使领馆：+33-1-5375-8840",
                    "注意扒手 (尤其景点/地铁)",
                    "避免夜间单独出行",
                ],
                "最佳季节": "5-10 月",
                "建议天数": "7-10 天",
                "预算范围": {
                    "经济": "¥8000-12000/人/天",
                    "舒适": "¥12000-20000/人/天",
                    "豪华": "¥20000-40000/人/天",
                },
            },
            "美国": {
                "民俗习惯": [
                    "见面握手",
                    "小费文化",
                    "公共场所保持距离",
                    "守时",
                ],
                "宗教信仰": [
                    "基督教为主要宗教",
                    "宗教自由",
                    "尊重各宗教信仰",
                ],
                "法律法规": [
                    "各州法律不同",
                    "禁止酒驾",
                    "禁止携带违禁品",
                    "21 岁以下禁止饮酒",
                    "禁止在公共场所吸烟",
                ],
                "禁忌事项": [
                    "不要讨论种族敏感话题",
                    "不要不尊重国旗",
                    "不要插队",
                    "不要大声喧哗",
                ],
                "礼仪规范": [
                    "见面握手",
                    "说 Please/Thank you",
                    "为他人扶门",
                    "小费 15-20%",
                ],
                "消费提示": [
                    "各州消费税不同 (0-10%)",
                    "可讲价 ( flea market)",
                    "小费文化 (餐厅 15-20%)",
                    "信用卡普及",
                ],
                "安全提示": [
                    "紧急电话：911",
                    "中国驻美使领馆：+1-202-495-2266",
                    "注意枪支安全",
                    "避免危险区域",
                ],
                "最佳季节": "5-10 月",
                "建议天数": "10-15 天",
                "预算范围": {
                    "经济": "¥10000-15000/人/天",
                    "舒适": "¥15000-25000/人/天",
                    "豪华": "¥25000-50000/人/天",
                },
            },
        }
    
    def get_destination_notices(self, destination: str) -> Dict:
        """
        获取目的地注意事项
        
        Args:
            destination: 目的地名称
        
        Returns:
            注意事项信息
        """
        print(f"\n📋 获取目的地注意事项：{destination}")
        
        # 模糊匹配目的地
        matched = None
        for dest_name in self.notices_db.keys():
            if dest_name in destination or destination in dest_name:
                matched = dest_name
                break
        
        if not matched:
            return {
                "success": False,
                "message": f"未找到 {destination} 的注意事项信息",
                "available_destinations": list(self.notices_db.keys()),
            }
        
        notices = self.notices_db[matched]
        
        result = {
            "success": True,
            "destination": matched,
            "notices": notices,
            "retrieved_at": datetime.now().isoformat(),
        }
        
        # 打印摘要
        print(f"  民俗习惯：{len(notices.get('民俗习惯', []))} 条")
        print(f"  法律法规：{len(notices.get('法律法规', []))} 条")
        print(f"  禁忌事项：{len(notices.get('禁忌事项', []))} 条")
        print(f"  安全提示：{len(notices.get('安全提示', []))} 条")
        
        return result
    
    def get_customs_summary(self, destination: str) -> str:
        """
        获取风俗摘要
        
        Args:
            destination: 目的地
        
        Returns:
            风俗摘要文本
        """
        result = self.get_destination_notices(destination)
        
        if not result["success"]:
            return result["message"]
        
        notices = result["notices"]
        
        summary = f"""📋 {destination} 旅行注意事项

🏮 民俗习惯:
"""
        for item in notices.get("民俗习惯", [])[:5]:
            summary += f"  • {item}\n"
        
        summary += f"""
⚖️ 法律法规:
"""
        for item in notices.get("法律法规", [])[:5]:
            summary += f"  • {item}\n"
        
        summary += f"""
⚠️ 禁忌事项:
"""
        for item in notices.get("禁忌事项", [])[:5]:
            summary += f"  • {item}\n"
        
        summary += f"""
🛡️ 安全提示:
"""
        for item in notices.get("安全提示", [])[:5]:
            summary += f"  • {item}\n"
        
        summary += f"""
ℹ️ 基本信息:
  • 最佳季节：{notices.get('最佳季节', 'N/A')}
  • 建议天数：{notices.get('建议天数', 'N/A')}
"""
        
        return summary
    
    def generate_notices_report(self, destinations: List[str]) -> str:
        """
        生成注意事项报告
        
        Args:
            destinations: 目的地列表
        
        Returns:
            报告文本
        """
        print(f"\n📊 生成注意事项报告")
        
        report = "# 📋 旅行目的地注意事项报告\n\n"
        report += f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"> **目的地数量**: {len(destinations)}\n\n"
        
        report += "---\n\n"
        
        for dest in destinations:
            result = self.get_destination_notices(dest)
            if result["success"]:
                notices = result["notices"]
                
                report += f"## 📍 {result['destination']}\n\n"
                
                report += "### 🏮 民俗习惯\n"
                for item in notices.get("民俗习惯", []):
                    report += f"- {item}\n"
                report += "\n"
                
                report += "### ⚖️ 法律法规\n"
                for item in notices.get("法律法规", []):
                    report += f"- {item}\n"
                report += "\n"
                
                report += "### ⚠️ 禁忌事项\n"
                for item in notices.get("禁忌事项", []):
                    report += f"- {item}\n"
                report += "\n"
                
                report += "### 🛡️ 安全提示\n"
                for item in notices.get("安全提示", []):
                    report += f"- {item}\n"
                report += "\n"
                
                report += "---\n\n"
        
        return report
    
    def add_destination(self, destination: str, notices: Dict):
        """
        添加新目的地注意事项
        
        Args:
            destination: 目的地名称
            notices: 注意事项字典
        """
        print(f"\n➕ 添加目的地注意事项：{destination}")
        
        self.notices_db[destination] = notices
        
        print(f"  ✅ 已添加 {destination} 的注意事项")
        print(f"  包含：{len(notices)} 项内容")
    
    def update_destination(self, destination: str, notices: Dict):
        """
        更新目的地注意事项
        
        Args:
            destination: 目的地名称
            notices: 注意事项字典
        """
        print(f"\n🔄 更新目的地注意事项：{destination}")
        
        if destination in self.notices_db:
            self.notices_db[destination].update(notices)
            print(f"  ✅ 已更新 {destination} 的注意事项")
        else:
            print(f"  ⚠️ {destination} 不存在，使用 add_destination 添加")


def main():
    """测试"""
    print("=" * 60)
    print("📋 太一旅行落地城市注意事项测试")
    print("=" * 60)
    
    notices = DestinationNotices()
    
    # 测试 1: 获取日本注意事项
    print("\n📍 测试 1: 获取日本注意事项")
    result = notices.get_destination_notices("日本")
    
    # 测试 2: 获取风俗摘要
    print("\n📝 测试 2: 获取风俗摘要")
    summary = notices.get_customs_summary("泰国")
    print(summary[:500])
    
    # 测试 3: 生成多目的地报告
    print("\n📊 测试 3: 生成多目的地报告")
    report = notices.generate_notices_report(["日本", "韩国", "泰国"])
    print(report[:1000])
    
    # 测试 4: 添加新目的地
    print("\n➕ 测试 4: 添加新目的地")
    notices.add_destination("越南", {
        "民俗习惯": ["进入寺庙脱鞋", "双手合十问候"],
        "法律法规": ["禁止赌博", "禁止携带违禁品"],
        "安全提示": ["紧急电话：113", "注意交通安全"],
    })
    
    # 测试 5: 更新目的地
    print("\n🔄 测试 5: 更新目的地")
    notices.update_destination("越南", {
        "消费提示": ["可讲价", "小费自愿"],
    })
    
    print("\n" + "=" * 60)
    print("✅ 落地城市注意事项测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
