#!/usr/bin/env python3
"""
元树茶馆 - 销售服务模块

作者：太一 AGI
创建：2026-04-09
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# 配置
CONFIG_DIR = Path(__file__).parent.parent / "config"
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

SALES_FILE = DATA_DIR / "sales.json"
INVENTORY_FILE = DATA_DIR / "inventory.json"


@dataclass
class Sale:
    """销售记录"""
    id: str
    customer_phone: str
    items: List[Dict]
    subtotal: float
    discount: float
    points_used: int
    total: float
    payment_method: str  # wechat/alipay/cash/card
    status: str  # completed/refunded
    created_at: str
    notes: str = ""


class SalesService:
    """销售服务"""
    
    def __init__(self):
        self.teas = self.load_teas()
        self.sales = self.load_sales()
        self.inventory = self.load_inventory()
    
    def load_teas(self) -> Dict:
        """加载茶叶产品配置"""
        config_file = CONFIG_DIR / "teas.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def load_sales(self) -> List[Dict]:
        """加载销售记录"""
        if SALES_FILE.exists():
            with open(SALES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_sales(self):
        """保存销售记录"""
        with open(SALES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.sales, f, indent=2, ensure_ascii=False)
    
    def load_inventory(self) -> Dict:
        """加载库存数据"""
        if INVENTORY_FILE.exists():
            with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # 初始化库存
        inventory = {}
        products = self.teas.get("products", {})
        for category, items in products.items():
            for item in items:
                inventory[item["id"]] = item.get("stock", 0)
        
        return inventory
    
    def save_inventory(self):
        """保存库存数据"""
        with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, indent=2, ensure_ascii=False)
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """获取产品信息"""
        products = self.teas.get("products", {})
        for category, items in products.items():
            for item in items:
                if item["id"] == product_id:
                    return {**item, "category": category}
        return None
    
    def get_member_discount(self, phone: str) -> float:
        """获取会员折扣 (简化版)"""
        # 实际应调用会员服务
        return 1.0
    
    def create_sale(
        self,
        customer_phone: str,
        items: List[Dict],
        payment_method: str = "wechat",
        points_used: int = 0,
        notes: str = ""
    ) -> Optional[Sale]:
        """
        创建销售记录
        
        Args:
            customer_phone: 客户电话
            items: 商品列表 [{"product_id": "xxx", "quantity": 1, "spec": "100g"}]
            payment_method: 支付方式
            points_used: 使用积分
            notes: 备注
        
        Returns:
            销售记录或 None
        """
        # 计算金额
        subtotal = 0
        for item in items:
            product = self.get_product(item["product_id"])
            if not product:
                return None
            
            # 检查库存
            if self.inventory.get(item["product_id"], 0) < item["quantity"]:
                return None
            
            price = product["prices"].get(item.get("spec", "100g"), 0)
            subtotal += price * item["quantity"]
        
        # 会员折扣
        discount = self.get_member_discount(customer_phone)
        
        # 积分抵扣 (100 积分 = ¥1)
        points_discount = points_used / 100
        
        # 总金额
        total = subtotal * discount - points_discount
        
        # 创建销售记录
        sale = Sale(
            id=f"sale-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            customer_phone=customer_phone,
            items=items,
            subtotal=subtotal,
            discount=discount,
            points_used=points_used,
            total=total,
            payment_method=payment_method,
            status="completed",
            created_at=datetime.now().isoformat(),
            notes=notes
        )
        
        # 扣减库存
        for item in items:
            self.inventory[item["product_id"]] -= item["quantity"]
        
        # 保存
        self.sales.append(asdict(sale))
        self.save_sales()
        self.save_inventory()
        
        return sale
    
    def get_sales(self, customer_phone: str = None, date: str = None) -> List[Dict]:
        """查询销售记录"""
        results = self.sales
        
        if customer_phone:
            results = [s for s in results if s["customer_phone"] == customer_phone]
        
        if date:
            results = [s for s in results if s["created_at"].startswith(date)]
        
        return results
    
    def get_inventory(self) -> Dict:
        """获取库存"""
        return self.inventory
    
    def check_low_stock(self, threshold: int = 10) -> List[Dict]:
        """检查低库存商品"""
        low_stock = []
        for product_id, stock in self.inventory.items():
            if stock <= threshold:
                product = self.get_product(product_id)
                if product:
                    low_stock.append({
                        "product_id": product_id,
                        "name": product["name"],
                        "stock": stock,
                        "threshold": threshold
                    })
        return low_stock
    
    def get_sales_stats(self, start_date: str = None, end_date: str = None) -> Dict:
        """获取销售统计"""
        filtered = self.sales
        
        if start_date:
            filtered = [s for s in filtered if s["created_at"] >= start_date]
        if end_date:
            filtered = [s for s in filtered if s["created_at"] <= end_date]
        
        total_sales = len(filtered)
        total_revenue = sum(s["total"] for s in filtered)
        
        # 按支付方式统计
        payment_stats = {}
        for s in filtered:
            method = s["payment_method"]
            payment_stats[method] = payment_stats.get(method, 0) + 1
        
        return {
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "payment_stats": payment_stats,
            "date_range": f"{start_date or 'N/A'} ~ {end_date or 'N/A'}"
        }


def main():
    """测试"""
    service = SalesService()
    
    print("🍵 元树茶馆 - 销售服务测试")
    print()
    
    # 查询库存
    print("当前库存:")
    inventory = service.get_inventory()
    for product_id, stock in list(inventory.items())[:5]:
        product = service.get_product(product_id)
        if product:
            print(f"  {product['name']}: {stock}")
    
    print()
    
    # 创建销售
    print("创建销售记录:")
    sale = service.create_sale(
        customer_phone="138****1234",
        items=[
            {"product_id": "tea-zhuyeqing-lidao", "quantity": 1, "spec": "100g"},
            {"product_id": "tea-bitanpiaoxue", "quantity": 2, "spec": "50g"}
        ],
        payment_method="wechat"
    )
    if sale:
        print(f"  ✅ 销售成功：{sale.id}")
        print(f"  小计：¥{sale.subtotal}")
        print(f"  总计：¥{sale.total}")
    else:
        print("  ❌ 销售失败 (库存不足或产品不存在)")
    
    print()
    
    # 低库存检查
    print("低库存预警:")
    low_stock = service.check_low_stock(threshold=30)
    if low_stock:
        for item in low_stock:
            print(f"  ⚠️ {item['name']}: 剩余{item['stock']}")
    else:
        print("  ✅ 库存充足")


if __name__ == "__main__":
    main()
