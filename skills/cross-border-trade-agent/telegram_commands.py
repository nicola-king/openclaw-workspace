#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot 命令处理器

功能:
- 处理 Telegram 斜杠命令
- 调用跨境贸易 Agent 功能
- 格式化输出为 Telegram 消息

作者：太一 AGI
创建：2026-05-04
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Optional

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('TelegramCommands')

# 命令映射
COMMAND_MAP = {
    "汇率": "exchange_rate",
    "市场": "market_analysis",
    "贸易": "trade_summary",
    "选品": "product_select",
    "比价": "price_compare",
    "物流": "logistics_optimize",
    "geo": "geo_audit",
    "潜客": "prospect_search",
    "帮助": "help",
}


def format_exchange_rate(result: Dict) -> str:
    """格式化汇率输出"""
    rate = result.get("rate")
    if rate:
        return f"💱 **汇率查询**\n\n{result['base']} → {result['target']}\n汇率: `{rate}`\n\n更新时间: {result.get('timestamp', '刚刚')}"
    return "❌ 汇率获取失败"


def format_product_select(result: Dict) -> str:
    """格式化选品输出"""
    product = result.get("product", "未知产品")
    score = result.get("score", 0)
    margin = result.get("profit_margin", 0)
    recommendation = result.get("recommendation", "")
    
    emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
    
    return f"""📦 **智能选品报告**

产品: {product}
出厂价: ${result.get('factory_price', 'N/A')}
海外售价: ${result.get('overseas_price', 'N/A')}
利润率: {margin*100:.1f}%

{emoji} **评分: {score}/100**
建议: {recommendation}"""


def format_logistics(result: Dict) -> str:
    """格式化物流输出"""
    destination = result.get("destination", "")
    weight = result.get("weight", 0)
    options = result.get("options", [])
    
    text = f"🚢 **物流方案**\n\n目的地: {destination}\n重量: {weight}kg\n\n"
    
    for opt in options:
        text += f"• **{opt['method']}**\n"
        text += f"  费用: ${opt['cost']:.0f}\n"
        text += f"  时效: {opt['time']}\n"
        text += f"  建议: {opt['recommendation']}\n\n"
    
    return text


def format_market_analysis(result: Dict) -> str:
    """格式化市场分析输出"""
    data = result.get("data", {})
    country = data.get("country", "")
    export_value = data.get("export_value")
    import_value = data.get("import_value")
    gdp = data.get("gdp")
    dependence = data.get("trade_dependence")
    
    text = f"📊 **市场分析: {country}**\n\n"
    
    if export_value:
        text += f"出口额: ${export_value/1e9:.0f}B\n"
    if import_value:
        text += f"进口额: ${import_value/1e9:.0f}B\n"
    if gdp:
        text += f"GDP: ${gdp/1e9:.0f}B\n"
    if dependence:
        text += f"贸易依存度: {dependence:.1f}%\n"
    
    return text


def format_help(result: Dict) -> str:
    """格式化帮助输出"""
    commands = result.get("commands", {})
    
    text = "🌍 **跨境贸易 Agent 命令列表**\n\n"
    text += "直接发送关键词即可:\n\n"
    
    for cmd, desc in commands.items():
        text += f"• `{cmd}` - {desc}\n"
    
    text += "\n示例:\n"
    text += "`汇率 base=USD target=CNY`\n"
    text += "`选品 product=蓝牙耳机 factory_price=50 overseas_price=120`\n"
    text += "`物流 destination=USA weight=500`\n"
    
    return text


def handle_message(message_text: str) -> Optional[str]:
    """
    处理 Telegram 消息
    
    Args:
        message_text: 用户消息
        
    Returns:
        回复文本
    """
    if not message_text:
        return None
    
    # 解析命令和参数
    parts = message_text.strip().split()
    if not parts:
        return None
    
    # 获取命令关键词
    keyword = parts[0].lower()
    
    # 查找命令映射
    command = COMMAND_MAP.get(keyword)
    if not command:
        return None
    
    # 解析参数
    args = {}
    for part in parts[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            try:
                value = float(value)
            except ValueError:
                pass
            args[key] = value
    
    # 执行命令
    try:
        bridge_path = Path(__file__).parent / "openclaw_bridge.py"
        cmd = ["python3", str(bridge_path), command]
        for key, value in args.items():
            cmd.append(f"{key}={value}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # 解析 JSON 输出 (过滤日志行，只取最后一个 JSON 块)
            import re
            stdout = result.stdout
            # 找到所有 JSON 对象 (非贪婪匹配，限制深度)
            json_pattern = re.compile(r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}')
            matches = json_pattern.findall(stdout)
            
            if matches:
                # 使用最后一个 JSON 对象
                data = json.loads(matches[-1])
                
                # 格式化输出
                formatters = {
                    "exchange_rate": format_exchange_rate,
                    "product_select": format_product_select,
                    "logistics_optimize": format_logistics,
                    "market_analysis": format_market_analysis,
                    "trade_summary": format_market_analysis,
                    "help": format_help,
                }
                
                formatter = formatters.get(command)
                if formatter:
                    return formatter(data)
                else:
                    return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
        else:
            return f"❌ 命令执行失败:\n```\n{result.stderr}\n```"
            
    except Exception as e:
        logger.error(f"处理消息失败: {e}")
        return f"❌ 处理失败: {e}"
    
    return None


def main():
    """测试"""
    test_messages = [
        "汇率 base=USD target=CNY",
        "选品 product=蓝牙耳机 factory_price=50 overseas_price=120",
        "物流 destination=USA weight=500",
        "帮助",
    ]
    
    for msg in test_messages:
        print(f"\n{'='*60}")
        print(f"输入: {msg}")
        print(f"{'='*60}")
        result = handle_message(msg)
        if result:
            print(result)
        else:
            print("(无响应)")


if __name__ == "__main__":
    main()
