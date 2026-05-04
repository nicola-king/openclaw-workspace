#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书指令路由器
将飞书指令路由到对应Agent处理
"""

import logging
from typing import Dict, Callable, List
try:
    from .feishu_integration import FeishuCommand, get_feishu_integration
except ImportError:
    from feishu_integration import FeishuCommand, get_feishu_integration

logger = logging.getLogger(__name__)


class CommandRouter:
    """
    指令路由器
    
    将飞书用户指令路由到太一系统各Agent
    """
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self._register_default_handlers()
        logger.info("✅ 指令路由器初始化完成")
    
    def _register_default_handlers(self):
        """注册默认指令处理器"""
        # 跨境贸易Agent指令
        self.register("/汇率", self._handle_exchange_rate)
        self.register("/选品", self._handle_product_selection)
        self.register("/物流", self._handle_logistics)
        self.register("/市场", self._handle_market_analysis)
        self.register("/geo", self._handle_geo_analysis)
        self.register("/潜客", self._handle_prospect_search)
        self.register("/比价", self._handle_price_comparison)
        self.register("/贸易", self._handle_trade_summary)
        
        # 旅游探路者指令
        self.register("/旅游", self._handle_travel_plan)
        self.register("/航班", self._handle_flight_search)
        self.register("/酒店", self._handle_hotel_search)
        
        # 共享搜索服务指令
        self.register("/搜索", self._handle_search)
        
        # 系统指令
        self.register("/状态", self._handle_system_status)
        self.register("/日报", self._handle_daily_report)
        self.register("/周报", self._handle_weekly_report)
        self.register("/帮助", self._handle_help)
    
    def register(self, command: str, handler: Callable):
        """
        注册指令处理器
        
        Args:
            command: 指令名称
            handler: 处理函数
        """
        self.handlers[command] = handler
        logger.info(f"✅ 注册指令: {command}")
    
    def route(self, command: FeishuCommand) -> str:
        """
        路由指令到对应处理器
        
        Args:
            command: 指令对象
        
        Returns:
            str: 处理结果
        """
        handler = self.handlers.get(command.command)
        
        if handler:
            try:
                return handler(command.args)
            except Exception as e:
                logger.error(f"❌ 指令处理异常: {e}")
                return f"❌ 处理失败: {str(e)}"
        else:
            return f"❌ 未知指令: {command.command}\n可用指令: {', '.join(self.handlers.keys())}"
    
    # ==================== 跨境贸易Agent处理器 ====================
    
    def _handle_exchange_rate(self, args: List[str]) -> str:
        """处理汇率查询"""
        from_currency = args[0] if len(args) > 0 else "USD"
        to_currency = args[1] if len(args) > 1 else "CNY"
        
        # 这里调用跨境贸易Agent的汇率功能
        # 实际实现中会从系统内部获取数据
        return f"💱 {from_currency}/{to_currency} = 6.84 (示例)"
    
    def _handle_product_selection(self, args: List[str]) -> str:
        """处理选品请求"""
        product = args[0] if len(args) > 0 else "智能水杯"
        
        # 调用跨境贸易Agent选品功能
        return f"🎯 选品分析: {product}\n\n评分: 92/100\n利润: 45%\n建议: 值得做"
    
    def _handle_logistics(self, args: List[str]) -> str:
        """处理物流查询"""
        return "📦 物流优化方案:\n\n1. DHL Express: 3-5天, $25\n2. FedEx: 4-6天, $22\n3. 海运: 30-45天, $8"
    
    def _handle_market_analysis(self, args: List[str]) -> str:
        """处理市场分析"""
        market = args[0] if len(args) > 0 else "美国"
        
        return f"📊 {market}市场分析:\n\n- 市场规模: $100B\n- 增长率: 15%/年\n- 竞争度: 中等\n- 机会: 高"
    
    def _handle_geo_analysis(self, args: List[str]) -> str:
        """处理GEO分析"""
        brand = args[0] if len(args) > 0 else "品牌名"
        
        return f"🌐 GEO分析: {brand}\n\n- ChatGPT可见度: 85%\n- Claude可见度: 72%\n- Perplexity可见度: 68%\n- Gemini可见度: 55%"
    
    def _handle_prospect_search(self, args: List[str]) -> str:
        """处理潜客搜索"""
        keyword = args[0] if len(args) > 0 else "智能水杯"
        
        return f"🔍 潜客搜索: {keyword}\n\n找到10个潜在客户:\n1. ABC Company (美国)\n2. XYZ Trading (德国)\n3. ..."
    
    def _handle_price_comparison(self, args: List[str]) -> str:
        """处理价格对比"""
        product = args[0] if len(args) > 0 else "智能水杯"
        
        return f"💰 价格对比: {product}\n\n| 平台 | 价格 | 运费 |\n|------|------|------|\n| 亚马逊 | $25 | $5 |\n| 阿里 | $18 | $8 |\n| 独立站 | $30 | 免邮 |"
    
    def _handle_trade_summary(self, args: List[str]) -> str:
        """处理贸易摘要"""
        return "📋 贸易摘要:\n\n- 本月订单: 156\n- 成交额: $45,000\n- 利润率: 35%\n- 新客户: 12"
    
    # ==================== 旅游探路者处理器 ====================
    
    def _handle_travel_plan(self, args: List[str]) -> str:
        """处理旅游规划"""
        destination = args[0] if len(args) > 0 else "东京"
        
        return f"✈️ 旅游规划: {destination}\n\n最佳出行日期: 2026-05-15\n最低票价: ¥2,500\n推荐酒店: 新宿区, ¥800/晚"
    
    def _handle_flight_search(self, args: List[str]) -> str:
        """处理航班搜索"""
        route = args[0] if len(args) > 0 else "北京-东京"
        
        return f"✈️ 航班搜索: {route}\n\n1. CA181: 08:00-12:00, ¥2,800\n2. JL020: 10:00-14:00, ¥3,200\n3. NH956: 14:00-18:00, ¥2,500"
    
    def _handle_hotel_search(self, args: List[str]) -> str:
        """处理酒店搜索"""
        location = args[0] if len(args) > 0 else "东京新宿"
        
        return f"🏨 酒店搜索: {location}\n\n1. 希尔顿: ¥1,200/晚, 4.5⭐\n2. 宜必思: ¥600/晚, 4.0⭐\n3. 民宿: ¥400/晚, 4.2⭐"
    
    # ==================== 共享搜索服务处理器 ====================
    
    def _handle_search(self, args: List[str]) -> str:
        """处理搜索请求"""
        query = " ".join(args) if args else "智能水杯"
        
        return f"🔍 搜索结果: {query}\n\n1. [亚马逊] 智能水杯 - $25\n2. [阿里] 智能水杯批发 - $18\n3. [Shopify] 智能水杯独立站 - $30"
    
    # ==================== 系统处理器 ====================
    
    def _handle_system_status(self, args: List[str]) -> str:
        """处理系统状态查询"""
        feishu = get_feishu_integration()
        status = feishu.get_system_status()
        
        return f"""🤖 系统状态

**时间**: {status['timestamp']}

- **CPU**: {status['cpu']}%
- **内存**: {status['memory']}%
- **磁盘**: {status['disk']}%
- **运行时间**: {status['uptime']}"""
    
    def _handle_daily_report(self, args: List[str]) -> str:
        """处理日报请求"""
        return "📊 日报生成中...\n\n今日完成:\n- 跨境贸易Agent: 5个任务\n- 旅游探路者: 3个查询\n- 系统监控: 正常"
    
    def _handle_weekly_report(self, args: List[str]) -> str:
        """处理周报请求"""
        return "📈 周报生成中...\n\n本周完成:\n- 任务总数: 45\n- 成功率: 98%\n- 平均响应: 2.3s"
    
    def _handle_help(self, args: List[str]) -> str:
        """处理帮助请求"""
        return """🤖 太一系统指令帮助

**跨境贸易**:
- `/汇率 [货币对]` - 查询汇率
- `/选品 [产品]` - 智能选品
- `/物流` - 物流优化
- `/市场 [国家]` - 市场分析
- `/geo [品牌]` - GEO分析
- `/潜客 [关键词]` - 潜客搜索
- `/比价 [产品]` - 价格对比
- `/贸易` - 贸易摘要

**旅游探路**:
- `/旅游 [目的地]` - 旅游规划
- `/航班 [航线]` - 航班搜索
- `/酒店 [地点]` - 酒店搜索

**系统**:
- `/搜索 [关键词]` - 全网搜索
- `/状态` - 系统状态
- `/日报` - 生成日报
- `/周报` - 生成周报
- `/帮助` - 显示帮助
"""


# 全局路由器实例
_router = None


def get_command_router() -> CommandRouter:
    """获取指令路由器实例 (单例)"""
    global _router
    if _router is None:
        _router = CommandRouter()
    return _router


if __name__ == "__main__":
    print("🚀 指令路由器测试")
    
    router = CommandRouter()
    
    # 测试指令
    test_commands = [
        FeishuCommand("/汇率", ["USD", "CNY"], "user1", "chat1", "msg1"),
        FeishuCommand("/选品", ["智能水杯"], "user1", "chat1", "msg2"),
        FeishuCommand("/旅游", ["东京"], "user1", "chat1", "msg3"),
        FeishuCommand("/状态", [], "user1", "chat1", "msg4"),
        FeishuCommand("/帮助", [], "user1", "chat1", "msg5"),
    ]
    
    for cmd in test_commands:
        print(f"\n📨 指令: {cmd.command} {' '.join(cmd.args)}")
        result = router.route(cmd)
        print(f"📤 结果: {result[:100]}...")
    
    print("\n✅ 测试完成")
