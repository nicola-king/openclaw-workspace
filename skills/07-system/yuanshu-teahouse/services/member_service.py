#!/usr/bin/env python3
"""
元树茶馆 - 会员服务模块

作者：太一 AGI
创建：2026-04-09
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# 配置
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

MEMBERS_FILE = DATA_DIR / "members.json"
POINTS_FILE = DATA_DIR / "points.json"


@dataclass
class Member:
    """会员信息"""
    id: str
    name: str
    phone: str
    level: str  # normal/silver/gold/vip
    total_consumption: float
    points: int
    join_date: str
    last_visit: str
    birthday: str = ""
    notes: str = ""


class MemberService:
    """会员服务"""
    
    def __init__(self):
        self.members = self.load_members()
        self.points_records = self.load_points()
    
    def load_members(self) -> List[Dict]:
        """加载会员数据"""
        if MEMBERS_FILE.exists():
            with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_members(self):
        """保存会员数据"""
        with open(MEMBERS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.members, f, indent=2, ensure_ascii=False)
    
    def load_points(self) -> List[Dict]:
        """加载积分记录"""
        if POINTS_FILE.exists():
            with open(POINTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_points(self):
        """保存积分记录"""
        with open(POINTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.points_records, f, indent=2, ensure_ascii=False)
    
    def get_level(self, total_consumption: float) -> str:
        """根据消费金额判断会员等级"""
        if total_consumption >= 20000:
            return "gold"
        elif total_consumption >= 5000:
            return "silver"
        else:
            return "normal"
    
    def get_discount(self, level: str) -> float:
        """获取会员折扣"""
        discounts = {
            "normal": 1.0,
            "silver": 0.95,
            "gold": 0.9,
            "vip": 0.85
        }
        return discounts.get(level, 1.0)
    
    def get_points_rate(self, level: str) -> float:
        """获取积分倍率"""
        rates = {
            "normal": 1.0,
            "silver": 1.2,
            "gold": 1.5,
            "vip": 2.0
        }
        return rates.get(level, 1.0)
    
    def create_member(
        self,
        name: str,
        phone: str,
        birthday: str = "",
        notes: str = ""
    ) -> Optional[Member]:
        """创建新会员"""
        # 检查是否已存在
        for m in self.members:
            if m["phone"] == phone:
                return None
        
        member = Member(
            id=f"mem-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=name,
            phone=phone,
            level="normal",
            total_consumption=0,
            points=0,
            join_date=datetime.now().strftime("%Y-%m-%d"),
            last_visit=datetime.now().strftime("%Y-%m-%d"),
            birthday=birthday,
            notes=notes
        )
        
        self.members.append(asdict(member))
        self.save_members()
        
        return member
    
    def get_member(self, phone: str) -> Optional[Dict]:
        """查询会员信息"""
        for m in self.members:
            if m["phone"] == phone:
                return m
        return None
    
    def update_consumption(self, phone: str, amount: float) -> Optional[Dict]:
        """更新消费记录"""
        for m in self.members:
            if m["phone"] == phone:
                # 更新消费总额
                m["total_consumption"] += amount
                m["last_visit"] = datetime.now().strftime("%Y-%m-%d")
                
                # 更新等级
                old_level = m["level"]
                new_level = self.get_level(m["total_consumption"])
                m["level"] = new_level
                
                # 计算积分
                points_rate = self.get_points_rate(new_level)
                points_earned = int(amount * points_rate)
                m["points"] += points_earned
                
                # 记录积分变动
                self.points_records.append({
                    "member_phone": phone,
                    "type": "earn",
                    "points": points_earned,
                    "reason": f"消费 ¥{amount}",
                    "date": datetime.now().isoformat()
                })
                
                # 等级提升通知
                level_up = False
                if old_level != new_level:
                    level_up = True
                
                self.save_members()
                self.save_points()
                
                return {
                    **m,
                    "level_up": level_up,
                    "points_earned": points_earned
                }
        
        return None
    
    def redeem_points(self, phone: str, points: int, item: str) -> bool:
        """积分兑换"""
        for m in self.members:
            if m["phone"] == phone:
                if m["points"] >= points:
                    m["points"] -= points
                    
                    self.points_records.append({
                        "member_phone": phone,
                        "type": "redeem",
                        "points": -points,
                        "reason": f"兑换：{item}",
                        "date": datetime.now().isoformat()
                    })
                    
                    self.save_members()
                    self.save_points()
                    return True
                else:
                    return False
        return False
    
    def get_points_history(self, phone: str) -> List[Dict]:
        """查询积分记录"""
        return [
            r for r in self.points_records
            if r["member_phone"] == phone
        ]
    
    def get_all_members(self) -> List[Dict]:
        """获取所有会员"""
        return self.members
    
    def get_level_stats(self) -> Dict:
        """获取会员等级统计"""
        stats = {"normal": 0, "silver": 0, "gold": 0, "vip": 0}
        for m in self.members:
            stats[m["level"]] = stats.get(m["level"], 0) + 1
        return stats


def main():
    """测试"""
    service = MemberService()
    
    print("🍵 元树茶馆 - 会员服务测试")
    print()
    
    # 创建会员
    print("创建新会员:")
    member = service.create_member(
        name="李四",
        phone="139****5678",
        birthday="1990-05-15"
    )
    if member:
        print(f"  ✅ 会员创建成功：{member.id}")
        print(f"  姓名：{member.name}")
        print(f"  等级：{member.level}")
    else:
        print("  ❌ 会员已存在")
    
    print()
    
    # 查询会员
    print("查询会员信息:")
    info = service.get_member("139****5678")
    if info:
        print(f"  姓名：{info['name']}")
        print(f"  等级：{info['level']}")
        print(f"  消费总额：¥{info['total_consumption']}")
        print(f"  积分：{info['points']}")
    
    print()
    
    # 更新消费
    print("更新消费记录 (消费¥1000):")
    result = service.update_consumption("139****5678", 1000)
    if result:
        print(f"  ✅ 消费已记录")
        print(f"  获得积分：{result['points_earned']}")
        if result.get('level_up'):
            print(f"  🎉 等级提升！")
    
    print()
    
    # 等级统计
    print("会员等级统计:")
    stats = service.get_level_stats()
    for level, count in stats.items():
        print(f"  {level}: {count}人")


if __name__ == "__main__":
    main()
