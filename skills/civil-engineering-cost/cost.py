#!/usr/bin/env python3
"""
市政工程造价计算器 (Civil Engineering Cost Calculator)

功能:
1. 道路工程造价计算
2. 桥梁工程造价计算
3. 管网工程造价计算
4. 定额套用与价格分析
5. 造价预算书生成

作者：太一 AGI
创建：2026-04-10
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════

@dataclass
class CostResult:
    """造价计算结果"""
    project_type: str
    total_cost: float
    unit_price: float
    breakdown: Dict[str, float]
    quantities: Dict[str, float]
    currency: str = "CNY"
    region: str = ""
    standard: str = ""
    calculated_at: str = ""
    
    def __post_init__(self):
        if not self.calculated_at:
            self.calculated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'project_type': self.project_type,
            'total_cost': round(self.total_cost, 2),
            'unit_price': round(self.unit_price, 2),
            'breakdown': {k: round(v, 2) for k, v in self.breakdown.items()},
            'quantities': {k: round(v, 2) for k, v in self.quantities.items()},
            'currency': self.currency,
            'region': self.region,
            'standard': self.standard,
            'calculated_at': self.calculated_at
        }


# ═══════════════════════════════════════════════════════════
# 定额数据库 (示例)
# ═══════════════════════════════════════════════════════════

QUOTAS = {
    'road': {
        '路基土方': {'unit': '1000m³', 'labor': 2500, 'material': 0, 'machine': 8500},
        '路基石方': {'unit': '1000m³', 'labor': 3200, 'material': 1500, 'machine': 12000},
        '沥青混凝土路面': {'unit': '1000㎡', 'labor': 1800, 'material': 85000, 'machine': 3500},
        '水泥混凝土路面': {'unit': '1000㎡', 'labor': 2200, 'material': 72000, 'machine': 4200},
        '路缘石': {'unit': '100m', 'labor': 800, 'material': 3500, 'machine': 200},
    },
    'bridge': {
        '钻孔灌注桩': {'unit': '10m³', 'labor': 4500, 'material': 8200, 'machine': 12500},
        '预应力混凝土梁': {'unit': '10m³', 'labor': 3800, 'material': 15600, 'machine': 5200},
        '桥面铺装': {'unit': '100㎡', 'labor': 1200, 'material': 18500, 'machine': 2800},
    },
    'pipeline': {
        'HDPE 管道 DN500': {'unit': '100m', 'labor': 2800, 'material': 35000, 'machine': 4500},
        'HDPE 管道 DN800': {'unit': '100m', 'labor': 3500, 'material': 58000, 'machine': 6200},
        '砖砌检查井': {'unit': '座', 'labor': 1800, 'material': 3200, 'machine': 800},
    }
}


# ═══════════════════════════════════════════════════════════
# 计算器核心
# ═══════════════════════════════════════════════════════════

class CostCalculator:
    """工程造价计算器"""
    
    def __init__(self, region: str = "上海", standard: str = "2020 定额"):
        self.region = region
        self.standard = standard
        self.tax_rate = 0.09  # 增值税 9%
        self.regulation_rate = 0.03  # 规费 3%
        self.measure_rate = 0.05  # 措施费 5%
    
    def calculate_road(self, length: float, width: float, structure: str, grade: str = "城市主干路") -> CostResult:
        """
        计算道路工程造价
        
        Args:
            length: 道路长度 (米)
            width: 道路宽度 (米)
            structure: 路面结构类型
            grade: 道路等级
        
        Returns:
            CostResult 对象
        """
        area = length * width
        
        # 工程量计算
        quantities = {
            '路基土石方': length * width * 0.5 / 1000,  # 假设平均厚度 0.5m
            structure: area / 1000,
            '路缘石': length * 2 / 100,
        }
        
        # 直接工程费计算
        direct_cost = 0
        for item, qty in quantities.items():
            if item in QUOTAS['road']:
                quota = QUOTAS['road'][item]
                unit_price = quota['labor'] + quota['material'] + quota['machine']
                direct_cost += qty * unit_price
        
        # 费用组成
        breakdown = {
            '分部分项工程费': direct_cost,
            '措施项目费': direct_cost * self.measure_rate,
            '其他项目费': direct_cost * 0.02,
            '规费': direct_cost * self.regulation_rate,
        }
        
        # 税金
        subtotal = sum(breakdown.values())
        breakdown['税金'] = subtotal * self.tax_rate
        
        # 总造价
        total_cost = subtotal + breakdown['税金']
        unit_price = total_cost / area
        
        return CostResult(
            project_type="道路工程",
            total_cost=total_cost,
            unit_price=unit_price,
            breakdown=breakdown,
            quantities=quantities,
            region=self.region,
            standard=self.standard
        )
    
    def calculate_bridge(self, span: float, width: float, structure: str, foundation: str = "钻孔灌注桩") -> CostResult:
        """
        计算桥梁工程造价
        
        Args:
            span: 跨径 (米)
            width: 桥宽 (米)
            structure: 桥梁结构类型
            foundation: 基础类型
        
        Returns:
            CostResult 对象
        """
        area = span * width
        
        # 工程量计算 (简化)
        quantities = {
            foundation: span * width * 0.3 / 10,  # 桩基混凝土
            structure: span * width * 0.2 / 10,   # 上部结构
            '桥面铺装': area / 100,
        }
        
        # 直接工程费计算
        direct_cost = 0
        for item, qty in quantities.items():
            if item in QUOTAS['bridge']:
                quota = QUOTAS['bridge'][item]
                unit_price = quota['labor'] + quota['material'] + quota['machine']
                direct_cost += qty * unit_price
        
        # 费用组成
        breakdown = {
            '分部分项工程费': direct_cost,
            '措施项目费': direct_cost * self.measure_rate,
            '其他项目费': direct_cost * 0.03,
            '规费': direct_cost * self.regulation_rate,
        }
        
        # 税金
        subtotal = sum(breakdown.values())
        breakdown['税金'] = subtotal * self.tax_rate
        
        # 总造价
        total_cost = subtotal + breakdown['税金']
        unit_price = total_cost / area
        
        return CostResult(
            project_type="桥梁工程",
            total_cost=total_cost,
            unit_price=unit_price,
            breakdown=breakdown,
            quantities=quantities,
            region=self.region,
            standard=self.standard
        )
    
    def calculate_pipeline(self, diameter: str, length: float, material: str, depth: float = 2.5) -> CostResult:
        """
        计算管网工程造价
        
        Args:
            diameter: 管径 (DNxxx)
            length: 管道长度 (米)
            material: 管材类型
            depth: 埋深 (米)
        
        Returns:
            CostResult 对象
        """
        # 工程量计算
        quantities = {
            f'{material} {diameter}': length / 100,
            '沟槽土石方': length * 1.5 * depth / 1000,
            '回填': length * 1.2 * depth / 1000,
            '检查井': max(1, int(length / 50)),
        }
        
        # 直接工程费计算
        direct_cost = 0
        pipeline_item = f'{material} {diameter}'
        if pipeline_item in QUOTAS['pipeline']:
            quota = QUOTAS['pipeline'][pipeline_item]
            direct_cost += quantities[pipeline_item] * (quota['labor'] + quota['material'] + quota['machine'])
        
        if '检查井' in quantities:
            quota = QUOTAS['pipeline']['检查井']
            direct_cost += quantities['检查井'] * (quota['labor'] + quota['material'] + quota['machine'])
        
        # 费用组成
        breakdown = {
            '分部分项工程费': direct_cost,
            '措施项目费': direct_cost * self.measure_rate,
            '其他项目费': direct_cost * 0.02,
            '规费': direct_cost * self.regulation_rate,
        }
        
        # 税金
        subtotal = sum(breakdown.values())
        breakdown['税金'] = subtotal * self.tax_rate
        
        # 总造价
        total_cost = subtotal + breakdown['税金']
        unit_price = total_cost / length
        
        return CostResult(
            project_type="管网工程",
            total_cost=total_cost,
            unit_price=unit_price,
            breakdown=breakdown,
            quantities=quantities,
            region=self.region,
            standard=self.standard
        )


# ═══════════════════════════════════════════════════════════
# 输出格式化
# ═══════════════════════════════════════════════════════════

class OutputFormatter:
    """输出格式化器"""
    
    @staticmethod
    def format_console(result: CostResult) -> str:
        """控制台格式"""
        output = []
        
        output.append("╔═══════════════════════════════════════════════════════════╗")
        output.append(f"║  📊 市政工程造价预算书                                    ║")
        output.append(f"║  工程类型：{result.project_type:<24}║")
        output.append(f"║  地区：{result.region:<28}║")
        output.append(f"║  定额标准：{result.standard:<24}║")
        output.append("╠═══════════════════════════════════════════════════════════╣")
        
        for item, value in result.breakdown.items():
            output.append(f"║  {item:<20}¥ {value:>12,.2f}                   ║")
        
        output.append("╠═══════════════════════════════════════════════════════════╣")
        output.append(f"║  总造价                ¥ {result.total_cost:>12,.2f}                   ║")
        output.append(f"║  单位造价              ¥ {result.unit_price:>12,.2f} /单位                  ║")
        output.append("╚═══════════════════════════════════════════════════════════╝")
        
        return "\n".join(output)
    
    @staticmethod
    def format_json(result: CostResult, indent: int = 2) -> str:
        """JSON 格式"""
        return json.dumps(result.to_dict(), indent=indent, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="📊 市政工程造价计算器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--type", "-t", required=True,
                       choices=["road", "bridge", "pipeline"],
                       help="工程类型")
    parser.add_argument("--output", "-o", default="console",
                       choices=["console", "json"],
                       help="输出格式")
    parser.add_argument("--region", "-r", default="上海",
                       help="地区")
    parser.add_argument("--standard", "-s", default="2020 定额",
                       help="定额标准")
    
    # 道路工程参数
    parser.add_argument("--length", "-l", type=float, help="长度 (米)")
    parser.add_argument("--width", "-w", type=float, help="宽度 (米)")
    parser.add_argument("--structure", type=str, help="结构类型")
    parser.add_argument("--grade", type=str, default="城市主干路", help="道路等级")
    
    # 桥梁工程参数
    parser.add_argument("--span", type=float, help="跨径 (米)")
    parser.add_argument("--foundation", type=str, default="钻孔灌注桩", help="基础类型")
    
    # 管网工程参数
    parser.add_argument("--diameter", type=str, help="管径 (DNxxx)")
    parser.add_argument("--material", type=str, default="HDPE 双壁波纹管", help="管材类型")
    parser.add_argument("--depth", type=float, default=2.5, help="埋深 (米)")
    
    args = parser.parse_args()
    
    # 创建计算器
    calc = CostCalculator(region=args.region, standard=args.standard)
    
    # 根据类型计算
    if args.type == "road":
        if not all([args.length, args.width, args.structure]):
            print("❌ 道路工程需要 --length, --width, --structure 参数")
            return 1
        result = calc.calculate_road(args.length, args.width, args.structure, args.grade)
    
    elif args.type == "bridge":
        if not all([args.span, args.width, args.structure]):
            print("❌ 桥梁工程需要 --span, --width, --structure 参数")
            return 1
        result = calc.calculate_bridge(args.span, args.width, args.structure, args.foundation)
    
    elif args.type == "pipeline":
        if not all([args.diameter, args.length]):
            print("❌ 管网工程需要 --diameter, --length 参数")
            return 1
        result = calc.calculate_pipeline(args.diameter, args.length, args.material, args.depth)
    
    # 输出结果
    if args.output == "json":
        print(OutputFormatter.format_json(result))
    else:
        print(OutputFormatter.format_console(result))
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
