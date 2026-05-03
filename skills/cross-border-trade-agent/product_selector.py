#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一外贸选品评估工具 v1.0
基于 BOC 四大关键逻辑

太一 AGI · 2026-04-22 00:05
"""

import json
from datetime import datetime
from pathlib import Path


class ProductEvaluator:
    """外贸选品评估器 - BOC 四大逻辑"""
    
    def __init__(self):
        self.weights = {
            'volume': 0.25,      # 体积小 - 25%
            'profit': 0.30,      # 利润足 - 30%
            'repurchase': 0.25,  # 复购强 - 25%
            'after_sales': 0.20  # 零售后 - 20%
        }
    
    def evaluate_volume(self, volume_m3: float, weight_kg: float = None) -> dict:
        """
        评估体积小
        
        Args:
            volume_m3: 单件体积 (立方米)
            weight_kg: 单件重量 (公斤，可选)
        
        Returns:
            dict: 评估结果
        """
        # 评分标准
        if volume_m3 < 0.01:
            score = 100
            level = "优秀"
            comment = "体积优秀，运费成本低"
        elif volume_m3 < 0.03:
            score = 80
            level = "良好"
            comment = "体积可接受，运费适中"
        elif volume_m3 < 0.05:
            score = 60
            level = "一般"
            comment = "体积偏大，运费较高"
        else:
            score = 30
            level = "差"
            comment = "体积过大，运费刺客，建议避免"
        
        # 重量评估 (如有)
        weight_comment = ""
        if weight_kg:
            if weight_kg < 1:
                weight_comment = "重量轻，运费优"
            elif weight_kg < 5:
                weight_comment = "重量适中"
            else:
                weight_comment = "重量偏大，运费增加"
        
        return {
            "dimension": "体积小",
            "weight": self.weights['volume'],
            "score": score,
            "level": level,
            "comment": comment,
            "weight_comment": weight_comment,
            "data": {
                "volume_m3": volume_m3,
                "weight_kg": weight_kg
            }
        }
    
    def evaluate_profit(self, factory_price: float, overseas_price: float, 
                       monthly_sales: int = 0, reviews: int = 0) -> dict:
        """
        评估利润足
        
        Args:
            factory_price: 出厂价 (人民币)
            overseas_price: 海外售价 (人民币)
            monthly_sales: 月销量
            reviews: 评价数量
        
        Returns:
            dict: 评估结果
        """
        # 利润率计算
        if factory_price > 0:
            profit_ratio = overseas_price / factory_price
            profit_margin = (overseas_price - factory_price) / overseas_price * 100
        else:
            profit_ratio = 0
            profit_margin = 0
        
        # 评分标准
        if profit_ratio >= 2.5:
            score = 100
            level = "优秀"
            comment = f"利润充足 ({profit_ratio:.1f}倍)，值得做"
        elif profit_ratio >= 2.0:
            score = 85
            level = "良好"
            comment = f"利润达标 ({profit_ratio:.1f}倍)，可以做"
        elif profit_ratio >= 1.5:
            score = 60
            level = "一般"
            comment = f"利润偏低 ({profit_ratio:.1f}倍)，需谨慎"
        else:
            score = 30
            level = "差"
            comment = f"利润不足 ({profit_ratio:.1f}倍)，不建议"
        
        # 市场验证
        market_comment = ""
        if monthly_sales > 500 and reviews > 500:
            market_comment = "✅ 市场验证充分 (月销 500+，评价 500+)"
        elif monthly_sales > 100 and reviews > 100:
            market_comment = "🟡 市场验证中等 (月销 100+，评价 100+)"
        else:
            market_comment = "⚠️ 市场验证不足，需进一步调研"
        
        return {
            "dimension": "利润足",
            "weight": self.weights['profit'],
            "score": score,
            "level": level,
            "comment": comment,
            "market_comment": market_comment,
            "data": {
                "factory_price": factory_price,
                "overseas_price": overseas_price,
                "profit_ratio": profit_ratio,
                "profit_margin": profit_margin,
                "monthly_sales": monthly_sales,
                "reviews": reviews
            }
        }
    
    def evaluate_repurchase(self, product_type: str, 
                           is_consumable: bool = False,
                           is_accessory: bool = False,
                           estimated_monthly_repurchase: float = 0) -> dict:
        """
        评估复购强
        
        Args:
            product_type: 产品类型
            is_consumable: 是否耗材
            is_accessory: 是否配件
            estimated_monthly_repurchase: 预估月复购率
        
        Returns:
            dict: 评估结果
        """
        # 耗材/配件自动加分
        base_score = 50
        if is_consumable:
            base_score += 30
        if is_accessory:
            base_score += 20
        
        # 复购率评分
        if estimated_monthly_repurchase > 30:
            score = min(100, base_score + 20)
            level = "优秀"
            comment = "复购率极高，持续消耗品"
        elif estimated_monthly_repurchase > 20:
            score = min(100, base_score + 10)
            level = "良好"
            comment = "复购率良好，稳定消耗"
        elif estimated_monthly_repurchase > 10:
            score = base_score
            level = "一般"
            comment = "复购率一般"
        else:
            score = max(30, base_score - 10)
            level = "差"
            comment = "复购率低，一次性购买"
        
        # 产品类型建议
        type_comment = ""
        high_repurchase_types = [
            "打印耗材", "滤芯", "配件", "耗材", 
            "办公用品", "个人护理耗材", "清洁用品"
        ]
        if product_type in high_repurchase_types:
            type_comment = f"✅ {product_type} 属于高复购品类"
        else:
            type_comment = f"ℹ️ {product_type} 复购率待验证"
        
        return {
            "dimension": "复购强",
            "weight": self.weights['repurchase'],
            "score": score,
            "level": level,
            "comment": comment,
            "type_comment": type_comment,
            "data": {
                "product_type": product_type,
                "is_consumable": is_consumable,
                "is_accessory": is_accessory,
                "estimated_monthly_repurchase": estimated_monthly_repurchase
            }
        }
    
    def evaluate_after_sales(self, is_fragile: bool = False,
                            is_food: bool = False,
                            requires_maintenance: bool = False,
                            is_electronic: bool = False,
                            estimated_defect_rate: float = 0) -> dict:
        """
        评估零售后
        
        Args:
            is_fragile: 是否易碎
            is_food: 是否食品
            requires_maintenance: 是否需维修
            is_electronic: 是否电子产品
            estimated_defect_rate: 预估次品率
        
        Returns:
            dict: 评估结果
        """
        # 基础分
        score = 100
        
        # 扣分项
        comments = []
        
        if is_fragile:
            score -= 40
            comments.append("❌ 易碎品，运输风险高")
        
        if is_food:
            score -= 30
            comments.append("❌ 食品，保质期/海关风险")
        
        if requires_maintenance:
            score -= 30
            comments.append("❌ 需维修，海外售后成本高")
        
        if is_electronic:
            score -= 15
            comments.append("⚠️ 电子产品，可能有售后问题")
        
        # 次品率扣分
        if estimated_defect_rate > 5:
            score -= 20
            comments.append(f"❌ 次品率高 ({estimated_defect_rate}%)")
        elif estimated_defect_rate > 2:
            score -= 10
            comments.append(f"⚠️ 次品率偏高 ({estimated_defect_rate}%)")
        
        # 评分等级
        if score >= 85:
            level = "优秀"
            comment = "售后风险低，适合外贸"
        elif score >= 70:
            level = "良好"
            comment = "售后风险可控"
        elif score >= 50:
            level = "一般"
            comment = "售后风险中等，需谨慎"
        else:
            level = "差"
            comment = "售后风险高，不建议做"
        
        if not comments:
            comments = ["✅ 无售后风险因素"]
        
        return {
            "dimension": "零售后",
            "weight": self.weights['after_sales'],
            "score": max(30, score),
            "level": level,
            "comment": comment,
            "risk_comments": comments,
            "data": {
                "is_fragile": is_fragile,
                "is_food": is_food,
                "requires_maintenance": requires_maintenance,
                "is_electronic": is_electronic,
                "estimated_defect_rate": estimated_defect_rate
            }
        }
    
    def evaluate_product(self, product_name: str, **kwargs) -> dict:
        """
        综合评估产品
        
        Args:
            product_name: 产品名称
            **kwargs: 各维度参数
        
        Returns:
            dict: 综合评估结果
        """
        # 各维度评估
        volume_result = self.evaluate_volume(
            kwargs.get('volume_m3', 0.05),
            kwargs.get('weight_kg')
        )
        
        profit_result = self.evaluate_profit(
            kwargs.get('factory_price', 0),
            kwargs.get('overseas_price', 0),
            kwargs.get('monthly_sales', 0),
            kwargs.get('reviews', 0)
        )
        
        repurchase_result = self.evaluate_repurchase(
            kwargs.get('product_type', '通用'),
            kwargs.get('is_consumable', False),
            kwargs.get('is_accessory', False),
            kwargs.get('estimated_monthly_repurchase', 0)
        )
        
        after_sales_result = self.evaluate_after_sales(
            kwargs.get('is_fragile', False),
            kwargs.get('is_food', False),
            kwargs.get('requires_maintenance', False),
            kwargs.get('is_electronic', False),
            kwargs.get('estimated_defect_rate', 0)
        )
        
        # 计算加权总分
        total_score = (
            volume_result['score'] * volume_result['weight'] +
            profit_result['score'] * profit_result['weight'] +
            repurchase_result['score'] * repurchase_result['weight'] +
            after_sales_result['score'] * after_sales_result['weight']
        )
        
        # 总体评价
        if total_score >= 85:
            recommendation = "✅ 强烈推荐"
            comment = "四维度表现优秀，值得立即行动"
        elif total_score >= 75:
            recommendation = "🟡 推荐"
            comment = "整体良好，可以推进"
        elif total_score >= 60:
            recommendation = "🟠 谨慎考虑"
            comment = "有明显短板，需优化后再做"
        else:
            recommendation = "❌ 不推荐"
            comment = "多维度不达标，建议放弃"
        
        return {
            "product_name": product_name,
            "evaluation_time": datetime.now().isoformat(),
            "dimensions": [
                volume_result,
                profit_result,
                repurchase_result,
                after_sales_result
            ],
            "total_score": round(total_score, 1),
            "recommendation": recommendation,
            "comment": comment,
            "weights": self.weights
        }
    
    def generate_report(self, result: dict) -> str:
        """生成评估报告"""
        report = []
        report.append("=" * 60)
        report.append(f"📊 外贸选品评估报告")
        report.append("=" * 60)
        report.append(f"产品：{result['product_name']}")
        report.append(f"时间：{result['evaluation_time']}")
        report.append("")
        
        report.append("-" * 60)
        report.append("🎯 四大维度评估")
        report.append("-" * 60)
        
        for dim in result['dimensions']:
            report.append(f"\n{dim['dimension']} (权重 {dim['weight']*100:.0f}%)")
            report.append(f"  得分：{dim['score']}/100")
            report.append(f"  等级：{dim['level']}")
            report.append(f"  评价：{dim['comment']}")
            
            # 详细评论
            if 'market_comment' in dim:
                report.append(f"  市场：{dim['market_comment']}")
            if 'type_comment' in dim:
                report.append(f"  类型：{dim['type_comment']}")
            if 'risk_comments' in dim:
                for risk in dim['risk_comments']:
                    report.append(f"  风险：{risk}")
        
        report.append("")
        report.append("-" * 60)
        report.append("📈 综合评估")
        report.append("-" * 60)
        report.append(f"总分：{result['total_score']}/100")
        report.append(f"建议：{result['recommendation']}")
        report.append(f"说明：{result['comment']}")
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """主函数 - 测试"""
    evaluator = ProductEvaluator()
    
    # 测试产品 1: 打印机滤芯 (理想产品)
    print("\n" + "=" * 60)
    print("测试产品 1: 打印机滤芯")
    print("=" * 60)
    
    result1 = evaluator.evaluate_product(
        product_name="打印机滤芯",
        volume_m3=0.005,      # 体积小
        weight_kg=0.3,        # 重量轻
        factory_price=20,     # 出厂价 20 元
        overseas_price=60,    # 海外售价 60 元 (3 倍)
        monthly_sales=800,    # 月销 800 单
        reviews=600,          # 评价 600+
        product_type="打印耗材",
        is_consumable=True,   # 耗材
        is_accessory=True,    # 配件
        estimated_monthly_repurchase=25,  # 月复购 25%
        is_fragile=False,
        is_food=False,
        requires_maintenance=False,
        is_electronic=False,
        estimated_defect_rate=1
    )
    
    print(evaluator.generate_report(result1))
    
    # 保存报告
    output_dir = Path("/home/nicola/.openclaw/workspace/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"product_evaluation_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result1, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 报告已保存：{output_file}")
    
    # 测试产品 2: 玻璃花瓶 (不理想产品)
    print("\n" + "=" * 60)
    print("测试产品 2: 玻璃花瓶")
    print("=" * 60)
    
    result2 = evaluator.evaluate_product(
        product_name="玻璃花瓶",
        volume_m3=0.08,       # 体积大
        weight_kg=2,          # 重量大
        factory_price=30,     # 出厂价 30 元
        overseas_price=50,    # 海外售价 50 元 (1.67 倍)
        monthly_sales=200,    # 月销 200 单
        reviews=150,          # 评价 150
        product_type="家居装饰",
        is_consumable=False,
        is_accessory=False,
        estimated_monthly_repurchase=5,  # 月复购 5%
        is_fragile=True,      # 易碎
        is_food=False,
        requires_maintenance=False,
        is_electronic=False,
        estimated_defect_rate=8  # 次品率 8%
    )
    
    print(evaluator.generate_report(result2))
    
    print("\n" + "=" * 60)
    print("✅ 产品评估工具测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
