#!/usr/bin/env python3
"""
Brand Studio v1.0.0
品牌工作室 - 集成 awesome-design-md 70个品牌设计规范到艺术Agent集群
自动为 aesthetic-filter / brand-guardian / design-system 提供品牌参考
"""

import json
import os
import yaml
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("brand-studio")

DESIGN_DIR = Path(__file__).parent / "brand-specs" / "design-md"
TOKEN_FILE = Path(__file__).parent / "design-tokens.json"
CSS_DIR = Path(__file__).parent / "css"


class BrandStudio:
    """品牌工作室 - 连接awesome-design-md 与 art-agent"""
    
    def __init__(self):
        self.brands = {}
        self._load_all()
    
    def _load_all(self):
        """加载所有品牌数据"""
        # 尝试加载结构化token
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE) as f:
                self.brands = json.load(f)
            logger.info(f"已加载 {len(self.brands)} 个品牌结构化Token")
        
        # 尝试加载原始设计规范
        if DESIGN_DIR.exists():
            raw_count = len([d for d in DESIGN_DIR.iterdir() if d.is_dir() and (d / "DESIGN.md").exists()])
            logger.info(f"原始设计规范: {raw_count} 个品牌可用")
    
    def list_brands(self) -> List[Dict]:
        """列出所有可用品牌"""
        results = []
        if DESIGN_DIR.exists():
            for d in sorted(DESIGN_DIR.iterdir()):
                if d.is_dir() and (d / "DESIGN.md").exists():
                    results.append({
                        "name": d.name,
                        "has_tokens": d.name in self.brands,
                        "spec_path": str(d / "DESIGN.md")
                    })
        return results
    
    def get_spec(self, brand: str, mode: str = "auto") -> Dict[str, Any]:
        """获取品牌设计规范
        
        mode: auto=智能选择, tokens=仅结构化数据, full=完整描述
        """
        if brand in self.brands and mode != "full":
            # 返回结构化token
            return {
                "brand": brand,
                "source": "tokens",
                "colors": self.brands[brand].get("colors", {}),
                "typography": self.brands[brand].get("typography", {}),
                "spacing": self.brands[brand].get("spacing", {}),
                "radius": self.brands[brand].get("radius", {}),
            }
        
        # 返回完整设计描述
        spec_path = DESIGN_DIR / brand / "DESIGN.md"
        if spec_path.exists():
            content = spec_path.read_text(encoding="utf-8")
            # 提取 YAML 元数据
            meta = {}
            design_text = content
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        meta = yaml.safe_load(parts[1]) or {}
                    except:
                        pass
                    design_text = parts[2]
            
            return {
                "brand": brand,
                "source": "raw",
                "meta": meta,
                "colors": meta.get("colors", {}),
                "typography": meta.get("typography", {}),
                "description": design_text[:2000],
            }
        
        return {"error": f"品牌 '{brand}' 未找到"}
    
    def get_css(self, brand: str) -> Optional[str]:
        """获取品牌CSS变量"""
        css_path = CSS_DIR / f"{brand}.css"
        if css_path.exists():
            return css_path.read_text()
        return None
    
    def recommend_for_context(self, context: str) -> List[str]:
        """根据使用场景推荐品牌
        
        context: trade_luxury / trade_tech / trade_finance / trade_ecommerce
                travel_hotel / travel_luxury / design_minimal / design_creative
        """
        RECOMMENDATIONS = {
            "trade_luxury": ["apple", "tesla", "stripe", "ferrari", "bugatti"],
            "trade_tech": ["vercel", "linear.app", "sentry", "notion", "cursor"],
            "trade_finance": ["stripe", "binance", "coinbase", "mastercard", "wise"],
            "trade_ecommerce": ["shopify", "airbnb", "airtable", "nike", "zapier"],
            "trade_social": ["spotify", "pinterest", "miro", "intercom"],
            "travel_hotel": ["airbnb", "starbucks", "nike"],
            "travel_luxury": ["ferrari", "lamborghini", "bugatti", "bmw-m"],
            "design_minimal": ["apple", "tesla", "vercel", "linear.app"],
            "design_creative": ["pinterest", "spotify", "framer", "figma"],
            "design_fintech": ["stripe", "binance", "coinbase", "revolut"],
        }
        return RECOMMENDATIONS.get(context, [])
    
    def generate_prompt(self, brand: str, content_type: str = "landing") -> str:
        """生成品牌化创作提示词
        
        content_type: landing / email / social / brochure / ui
        """
        spec = self.get_spec(brand, "full")
        if "error" in spec:
            return spec["error"]
        
        prompt_templates = {
            "landing": "根据以下品牌设计规范生成品牌落地页HTML/CSS",
            "email": "根据以下品牌设计规范生成营销邮件",
            "social": "根据以下品牌设计规范生成社媒帖子（含配色）",
            "brochure": "根据以下品牌设计规范生成宣传物料",
            "ui": "根据以下品牌设计规范生成UI组件库",
        }
        
        tpl = prompt_templates.get(content_type, prompt_templates["landing"])
        colors = spec.get("colors", {})
        color_block = "\n".join([f"  {k}: {v}" for k, v in list(colors.items())[:10]])
        
        return f"""{tpl}

品牌: {spec.get('brand', brand)}
描述: {spec.get('description', '')[:500]}

核心颜色:
{color_block}

Typography: {json.dumps(spec.get('typography', {}), ensure_ascii=False)[:200]}"""


if __name__ == "__main__":
    import sys
    bs = BrandStudio()
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "list":
        brands = bs.list_brands()
        print(f"🎨 可用品牌: {len(brands)} 个\n")
        for b in brands[:10]:
            token = "✅" if b["has_tokens"] else "📝"
            print(f"  {token} {b['name']}")
        if len(brands) > 10:
            print(f"  ... 还有 {len(brands)-10} 个")
    
    elif cmd == "show" and len(sys.argv) > 2:
        spec = bs.get_spec(sys.argv[2], "tokens")
        if "error" in spec:
            print(spec["error"])
        else:
            print(f"品牌: {sys.argv[2]}")
            print(f"颜色: {len(spec.get('colors', {}))} 个")
            for k, v in list(spec.get("colors", {}).items())[:8]:
                print(f"  {k}: {v}")
    
    elif cmd == "recommend" and len(sys.argv) > 2:
        recs = bs.recommend_for_context(sys.argv[2])
        print(f"场景 '{sys.argv[2]}' 推荐品牌: {', '.join(recs)}")
    
    elif cmd == "prompt" and len(sys.argv) > 2:
        prompt = bs.generate_prompt(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "landing")
        print(prompt[:800])
    
    else:
        print("用法:")
        print("  list              — 列出品牌")
        print("  show <brand>      — 查看设计Token")
        print("  recommend <场景>   — 场景推荐")
        print("  prompt <brand>    — 生成创作提示词")
