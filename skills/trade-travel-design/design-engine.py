#!/usr/bin/env python3
"""
DesignMD 智能应用引擎 — 为跨境贸易 Agent + 旅游探路者提供品牌设计能力

将 awesome-design-md 的 70 个品牌设计规范，自动转化为：
- 跨境贸易：品牌落地页、营销邮件、社媒海报
- 旅游探路者：旅行手册、目的地指南、行程单
"""

import json
import os
from pathlib import Path
import random

DESIGN_DIR = Path(os.path.expanduser("~/.openclaw/workspace/notes/awesome-design-md/design-md"))

# 品牌 → 场景映射
BRAND_MAP = {
    # 跨境贸易场景推荐品牌
    "trade_luxury": ["apple", "tesla", "stripe", "ferrari", "bugatti"],
    "trade_tech": ["vercel", "linear.app", "sentry", "notion", "cursor"],
    "trade_finance": ["stripe", "binance", "coinbase", "mastercard", "wise"],
    "trade_ecommerce": ["shopify", "airbnb", "airtable", "nike", "zapier"],
    "trade_social": ["spotify", "pinterest", "miro", "intercom"],
    # 旅游探路者场景推荐品牌
    "travel_hotel": ["airbnb", "starbucks", "nike"],
    "travel_tech": ["uber", "tesla", "vercel"],
    "travel_luxury": ["ferrari", "lamborghini", "bugatti", "bmw-m"],
    "travel_nature": ["patagonia", "north-face", "airbnb"],
}

# 品牌中文标签
BRAND_LABELS = {
    "airbnb": "爱彼迎 - 温暖旅行风",
    "apple": "苹果 - 极简高端",
    "binance": "币安 - 金融科技暗色",
    "stripe": "Stripe - 金融质感",
    "tesla": "特斯拉 - 极简工业",
    "uber": "优步 - 自信黑白",
    "notion": "Notion - 知识清爽",
    "vercel": "Vercel - 开发者极简",
    "spotify": "Spotify - 音乐活力",
    "shopify": "Shopify - 电商实用",
    "ferrari": "法拉利 - 奢华运动",
    "bmw": "宝马 - 德系精密",
    "nike": "耐克 - 运动激情",
    "meta": "Meta - 社交自信",
    "claude": "Claude - 温暖AI",
}


def list_brands(category=None):
    """列出可用品牌"""
    all_brands = sorted([d.name for d in DESIGN_DIR.iterdir() if d.is_dir() and (d / "DESIGN.md").exists()])
    if category and category in BRAND_MAP:
        rec = BRAND_MAP[category]
        return [b for b in all_brands if b in rec] + [b for b in all_brands if b not in rec]
    return all_brands


def get_design(name):
    """获取特定品牌的设计规范"""
    path = DESIGN_DIR / name / "DESIGN.md"
    if not path.exists():
        return {"error": f"品牌 '{name}' 未找到。可用品牌: {', '.join(list_brands()[:10])}"}
    content = path.read_text(encoding="utf-8")
    
    # 提取元数据
    meta = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            content = parts[2]
    
    label = BRAND_LABELS.get(name, name.capitalize())
    
    return {
        "brand": name,
        "label": label,
        "meta": meta,
        "design": content,
    }


def generate_prompt_for_trade(brand, product, market, content_type="landing"):
    """为跨境贸易生成品牌提示词"""
    design = get_design(brand)
    if "error" in design:
        return design
    
    prompts = {
        "landing": f"""你是一个顶级UI/品牌设计师。请根据以下设计规范，生成一个{market}市场的{product}品牌落地页：

设计要求：
{design['design'][:1500]}

请输出：
1. 页面的HTML/CSS代码（内联样式，可直接运行）
2. 色彩方案（提取主色/辅助色）
3. 字体层级
4. 排版布局建议
5. 文案风格指南""",

        "email": f"""请根据以下品牌设计规范，生成一封{market}市场的{product}营销邮件：

品牌规范：
{design['design'][:1000]}

邮件要求：
- 符合品牌色调
- 适合{market}市场文化
- 有CTA按钮
- 移动端适配""",

        "social": f"""请根据以下设计规范，为{product}生成{market}市场的社媒帖子（含配色方案）：

品牌规范：
{design['design'][:800]}

输出：
- 帖子文案
- 配色方案（RGB/HEX）
- 图片描述（可用于生成图片）
- Hashtags""",
    }
    
    return prompts.get(content_type, prompts["landing"])


def generate_prompt_for_travel(brand, destination, content_type="brochure"):
    """为旅游探路者生成品牌提示词"""
    design = get_design(brand)
    if "error" in design:
        return design
    
    prompts = {
        "brochure": f"""请根据以下品牌设计规范，生成{destination}的旅行宣传册：

品牌规范：
{design['design'][:1500]}

输出：
1. 宣传册整体设计风格描述
2. 色彩方案
3. 封面设计
4. 内页布局
5. 推荐行程
6. 文案语调""",

        "itinerary": f"""请根据以下品牌设计规范，生成{destination}的每日行程单：

品牌规范：
{design['design'][:1000]}

输出：
- 行程标题设计
- 每日时间线布局
- 活动卡片样式
- 配色方案""",

        "review": f"""请根据以下品牌设计规范，生成{destination}的攻略/评测页面：

品牌规范：
{design['design'][:800]}

输出：
- 页面结构
- 评分卡设计
- 图片展示方式
- 排版建议""",
    }
    
    return prompts.get(content_type, prompts["brochure"])


if __name__ == "__main__":
    import sys
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "list":
        brands = list_brands()
        print(f"📐 可用品牌 ({len(brands)} 个):")
        for b in brands:
            label = BRAND_LABELS.get(b, b.capitalize())
            print(f"  {b:20s} - {label}")
        print()
        print("场景推荐:")
        for scene, recs in BRAND_MAP.items():
            print(f"  {scene:20s}: {', '.join(recs[:4])}")
    
    elif cmd == "show" and len(sys.argv) > 2:
        result = get_design(sys.argv[2])
        if "error" in result:
            print(result["error"])
        else:
            print(f"品 牌: {result['brand']}")
            print(f"标 签: {result['label']}")
            print()
            print(result['design'][:2000])
            print("...(以下省略)")
    
    elif cmd == "trade" and len(sys.argv) > 3:
        prompt = generate_prompt_for_trade(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "global")
        if isinstance(prompt, dict) and "error" in prompt:
            print(prompt["error"])
        else:
            print(prompt)
    
    elif cmd == "travel" and len(sys.argv) > 3:
        prompt = generate_prompt_for_travel(sys.argv[2], sys.argv[3])
        if isinstance(prompt, dict) and "error" in prompt:
            print(prompt["error"])
        else:
            print(prompt)
    
    else:
        print("用法:")
        print("  python3 design-engine.py list              # 列出品牌")
        print("  python3 design-engine.py show <brand>      # 查看设计规范")
        print("  python3 design-engine.py trade <brand> <product> [market]  # 跨境贸易生成")
        print("  python3 design-engine.py travel <brand> <destination>       # 旅游推广生成")
