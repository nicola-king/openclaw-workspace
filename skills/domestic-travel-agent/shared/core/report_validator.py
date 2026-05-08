#!/usr/bin/env python3
"""
报告完整度验证器 v1.0
强制所有报告输出包含: 电话/地址/营业时间/验证链接
"""
import json, re
from pathlib import Path
from typing import Dict, List, Tuple

class ReportValidator:
    """报告完整度验证器"""
    
    REQUIRED_FIELDS = {
        "hotel": ["name", "address", "phone", "verification_links"],
        "restaurant": ["name", "address", "phone", "cuisine", "hours", "verification_links"],
        "attraction": ["name", "address", "phone", "hours", "price", "verification_links"],
        "service": ["name", "phone", "license_no", "verification_links"],
        "transport": ["provider", "route", "departure", "arrival", "price", "verification_links"],
        "embassy": ["name", "phone", "address", "hours", "verification_links"],
        "hospital": ["name", "phone", "address", "hours", "verification_links"],
    }
    
    @staticmethod
    def check_markdown_completeness(md_content: str) -> Dict:
        """检查Markdown报告完整度"""
        issues = []
        
        # 检查酒店是否有电话
        if "🏨" in md_content or "hotel" in md_content.lower():
            if not re.search(r'\+?\d[\d\s\-]{6,}', md_content):
                issues.append("❌ 缺少酒店联系电话")
            if not re.search(r'https?://(?:www\.)?google\..*/maps', md_content, re.I):
                issues.append("⚠️ 建议添加Google Maps验证链接")
        
        # 检查餐馆是否有电话/营业时间
        if "🍜" in md_content or "restaurant" in md_content.lower():
            if not re.search(r'\+?\d[\d\s\-]{6,}', md_content):
                issues.append("❌ 缺少餐馆联系电话")
            if not re.search(r'(?:周一|周二|每日|Mon|Tue|Daily|24小时)', md_content):
                issues.append("⚠️ 建议添加营业时间")
        
        # 检查是否有验证链接
        link_count = len(re.findall(r'https?://[^\s]+', md_content))
        if link_count < 3:
            issues.append(f"❌ 验证链接过少 (仅{link_count}个, 建议至少10+)")
        
        # 检查是否有地址
        if not re.search(r'(?:地址|Street|Road|Lane|Drive|Singapore|NSW|VIC|北京|上海)', md_content):
            issues.append("❌ 缺少地址信息")
        
        score = max(0, 100 - len(issues) * 20)
        
        return {
            "score": score,
            "is_complete": score >= 80,
            "issues": issues,
            "verdict": "✅ 完整" if score >= 80 else "❌ 不完整，需补充",
        }
    
    @staticmethod
    def format_entry(name: str, phone: str, address: str, hours: str,
                     links: List[Tuple[str, str]]) -> str:
        """标准格式输出"""
        lines = [
            f"**{name}**",
            f"📞 {phone}" if phone else "📞 待补充",
            f"📍 {address}" if address else "📍 待补充",
            f"🕐 {hours}" if hours else "🕐 待补充",
        ]
        if links:
            link_str = " | ".join([f"[{l[0]}]({l[1]})" for l in links])
            lines.append(f"🔗 {link_str}")
        return "\n".join(lines) + "\n"

# CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="报告完整度验证器")
    parser.add_argument("--file", help="检查MD文件完整度")
    args = parser.parse_args()
    
    if args.file:
        content = Path(args.file).read_text(encoding='utf-8')
        result = ReportValidator.check_markdown_completeness(content)
        print(f"得分: {result['score']}/100")
        print(f" verdict: {result['verdict']}")
        if result['issues']:
            print("\n问题:")
            for i in result['issues']:
                print(f"  {i}")
