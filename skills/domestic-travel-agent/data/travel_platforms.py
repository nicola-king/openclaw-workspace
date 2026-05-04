#!/usr/bin/env python3
"""
旅游平台清单 — 国内/国外 完整版
用于旅游探路者的搜索源和验证链接
"""
from typing import Dict, List

DOMESTIC_PLATFORMS = {
    "ota_travel": [
        {"name": "携程", "url": "https://www.ctrip.com", "type": "综合OTA", "features": "机票/酒店/火车票/景点门票"},
        {"name": "飞猪", "url": "https://www.fliggy.com", "type": "综合OTA", "features": "机票/酒店/度假"},
        {"name": "美团", "url": "https://www.meituan.com", "type": "本地生活", "features": "酒店/餐饮/景点门票"},
        {"name": "去哪儿", "url": "https://www.qunar.com", "type": "比价平台", "features": "机票比价/酒店比价"},
        {"name": "同程旅行", "url": "https://www.ly.com", "type": "综合OTA", "features": "机票/火车票/酒店"},
        {"name": "途牛", "url": "https://www.tuniu.com", "type": "度假旅游", "features": "跟团游/自由行/定制游"},
        {"name": "马蜂窝", "url": "https://www.mafengwo.cn", "type": "攻略社区", "features": "游记/攻略/自由行"},
        {"name": "穷游", "url": "https://www.qyer.com", "type": "攻略社区", "features": "穷游锦囊/行程助手"},
    ],
    "hotels": [
        {"name": "华住会", "url": "https://www.huazhu.com", "type": "连锁酒店", "features": "汉庭/全季/桔子酒店"},
        {"name": "如家", "url": "https://www.homeinns.com", "type": "连锁酒店", "features": "如家/莫泰/和颐"},
    ],
    "transport": [
        {"name": "12306", "url": "https://www.12306.cn", "type": "铁路官方", "features": "火车票/高铁票"},
        {"name": "携程机票", "url": "https://flights.ctrip.com", "type": "机票预订", "features": "国内/国际航班"},
        {"name": "巴士管家", "url": "https://www.busgo.com", "type": "汽车票", "features": "长途汽车票"},
        {"name": "曹操出行", "url": "https://www.caocao.com", "type": "网约车", "features": "打车/租车"},
    ],
    "social_media": [
        {"name": "小红书", "url": "https://www.xiaohongshu.com", "type": "社交分享", "features": "旅行攻略/探店/真实评价"},
        {"name": "抖音", "url": "https://www.douyin.com", "type": "短视频", "features": "景点打卡/美食探店"},
        {"name": "Bilibili", "url": "https://www.bilibili.com", "type": "视频社区", "features": "旅行Vlog/攻略视频"},
        {"name": "微博旅游", "url": "https://weibo.com", "type": "社交媒体", "features": "旅游话题/博主推荐"},
        {"name": "大众点评", "url": "https://www.dianping.com", "type": "本地评价", "features": "餐馆/酒店/景点评价"},
    ],
    "guides_tours": [
        {"name": "KLOOK客路", "url": "https://www.klook.com/zh-CN", "type": "当地体验", "features": "景点门票/一日游/特色体验"},
        {"name": "KKday", "url": "https://www.kkday.com/zh-cn", "type": "当地体验", "features": "深度游/当地活动"},
    ],
}

INTERNATIONAL_PLATFORMS = {
    "ota_global": [
        {"name": "Booking.com", "url": "https://www.booking.com", "type": "酒店预订", "features": "全球酒店/民宿/公寓"},
        {"name": "Agoda", "url": "https://www.agoda.com", "type": "酒店预订", "features": "亚洲酒店为主/价格有优势"},
        {"name": "Expedia", "url": "https://www.expedia.com", "type": "综合OTA", "features": "机票+酒店+租车套餐"},
        {"name": "Kayak", "url": "https://www.kayak.com", "type": "比价平台", "features": "机票/酒店/租车比价"},
        {"name": "Skyscanner", "url": "https://www.skyscanner.com", "type": "机票比价", "features": "全球航班比价"},
        {"name": "Trip.com", "url": "https://www.trip.com", "type": "综合OTA", "features": "携程国际版/全球服务"},
        {"name": "Hotels.com", "url": "https://www.hotels.com", "type": "酒店预订", "features": "住10晚送1晚"},
    ],
    "experiences": [
        {"name": "Viator", "url": "https://www.viator.com", "type": "当地体验", "features": "全球景点门票/一日游"},
        {"name": "GetYourGuide", "url": "https://www.getyourguide.com", "type": "当地体验", "features": "欧洲为主/导览/活动"},
        {"name": "KLOOK", "url": "https://www.klook.com", "type": "当地体验", "features": "亚太区门票/体验"},
        {"name": "Airbnb Experiences", "url": "https://www.airbnb.com/s/experiences", "type": "独特体验", "features": "当地人带玩/烹饪课/手工艺"},
    ],
    "accommodation": [
        {"name": "Airbnb", "url": "https://www.airbnb.com", "type": "民宿短租", "features": "全球民宿/整套房源/家庭友好"},
        {"name": "Hostelworld", "url": "https://www.hostelworld.com", "type": "青旅预订", "features": "青年旅舍/背包客"},
    ],
    "transport_global": [
        {"name": "Google Flights", "url": "https://www.google.com/travel/flights", "type": "机票比价", "features": "全球航班/价格追踪"},
        {"name": "Rome2Rio", "url": "https://www.rome2rio.com", "type": "路线规划", "features": "多段交通组合搜索"},
        {"name": "Omio", "url": "https://www.omio.com", "type": "交通比价", "features": "欧洲火车/巴士/飞机"},
        {"name": "Trainline", "url": "https://www.thetrainline.com", "type": "火车票", "features": "欧洲火车票/英国铁路"},
        {"name": "Uber", "url": "https://www.uber.com", "type": "网约车", "features": "全球打车/部分国家"},
        {"name": "Grab", "url": "https://www.grab.com", "type": "东南亚打车", "features": "东南亚/打车+外卖+支付"},
        {"name": "Gojek", "url": "https://www.gojek.com", "type": "东南亚打车", "features": "印尼/泰国/新加坡/越南"},
    ],
    "social_global": [
        {"name": "TripAdvisor", "url": "https://www.tripadvisor.com", "type": "旅行评价", "features": "全球景点/酒店/餐馆评价"},
        {"name": "Instagram", "url": "https://www.instagram.com", "type": "社交分享", "features": "旅行照片/网红打卡地"},
        {"name": "YouTube Travel", "url": "https://www.youtube.com", "type": "视频平台", "features": "旅行Vlog/攻略视频/博主"},
        {"name": "Reddit Travel", "url": "https://www.reddit.com/r/travel", "type": "社区讨论", "features": "真实旅行经验分享"},
        {"name": "Lonely Planet", "url": "https://www.lonelyplanet.com", "type": "旅行指南", "features": "目的地指南/攻略"},
    ],
    "travel_services": [
        {"name": "World Nomads", "url": "https://www.worldnomads.com", "type": "旅行保险", "features": "全球旅行保险"},
        {"name": "TransferWise/Wise", "url": "https://wise.com", "type": "跨境支付", "features": "汇率最好的跨境汇款"},
        {"name": "XE Currency", "url": "https://www.xe.com", "type": "汇率工具", "features": "实时汇率转换"},
    ],
}


def print_platforms(title: str, platforms: Dict[str, List[Dict]]):
    """打印平台清单"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    for category, items in platforms.items():
        print(f"\n  📂 {category}:")
        for item in items:
            print(f"    🔗 [{item['name']}]({item['url']})")
            print(f"       {item['type']} | {item['features']}")


if __name__ == "__main__":
    print_platforms("🇨🇳 国内旅游平台", DOMESTIC_PLATFORMS)
    print_platforms("🌏 国外旅游平台", INTERNATIONAL_PLATFORMS)
    print()
    print(f"{'='*60}")
    print(f" 总计: {sum(len(v) for v in DOMESTIC_PLATFORMS.values()) + sum(len(v) for v in INTERNATIONAL_PLATFORMS.values())} 个平台")
    print(f"{'='*60}")
