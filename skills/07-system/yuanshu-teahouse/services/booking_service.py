#!/usr/bin/env python3
"""
元树茶馆 - 预订服务

作者：太一 AGI
创建：2026-04-09
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# 配置
CONFIG_DIR = Path(__file__).parent.parent / "config"
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

RESERVATIONS_FILE = DATA_DIR / "reservations.json"


@dataclass
class Reservation:
    """预订记录"""
    id: str
    space_id: str
    space_name: str
    customer_name: str
    customer_phone: str
    date: str
    time_slot: str
    party_size: int
    total_price: float
    status: str  # confirmed/cancelled/completed
    created_at: str
    notes: str = ""


class BookingService:
    """预订服务"""
    
    def __init__(self):
        self.spaces = self.load_spaces()
        self.reservations = self.load_reservations()
    
    def load_spaces(self) -> Dict:
        """加载空间配置"""
        config_file = CONFIG_DIR / "spaces.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def load_reservations(self) -> List[Dict]:
        """加载预订记录"""
        if RESERVATIONS_FILE.exists():
            with open(RESERVATIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_reservations(self):
        """保存预订记录"""
        with open(RESERVATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.reservations, f, indent=2, ensure_ascii=False)
    
    def query_spaces(
        self,
        date: str,
        time_slot: str,
        party_size: int,
        space_type: str = None
    ) -> List[Dict]:
        """
        查询可用空间
        
        Args:
            date: 日期 (YYYY-MM-DD)
            time_slot: 时段
            party_size: 人数
            space_type: 空间类型 (lounge/private_room/meeting_room)
        
        Returns:
            可用空间列表
        """
        available = []
        
        all_spaces = []
        spaces_data = self.spaces.get("spaces", {})
        
        # 调试输出
        print(f"  加载的空间类型：{list(spaces_data.keys())}")
        
        for space_type_key, spaces in spaces_data.items():
            if space_type and space_type_key != space_type:
                continue
            for space in spaces:
                space_copy = {**space, "space_type": space_type_key}
                all_spaces.append(space_copy)
        
        for space in all_spaces:
            # 检查人数匹配
            if "capacity" in space:
                if party_size > space["capacity"]:
                    continue
            elif "capacity_max" in space:
                if party_size > space["capacity_max"]:
                    continue
            
            # 检查是否已被预订
            if self.is_space_booked(space["id"], date, time_slot):
                continue
            
            # 添加到可用列表 (使用 space 中已存储的 space_type)
            available.append(space)
        
        return available
    
    def is_space_booked(self, space_id: str, date: str, time_slot: str) -> bool:
        """检查空间是否已被预订"""
        for res in self.reservations:
            if (res["space_id"] == space_id and
                res["date"] == date and
                res["time_slot"] == time_slot and
                res["status"] in ["confirmed", "completed"]):
                return True
        return False
    
    def create_reservation(
        self,
        space_id: str,
        customer_name: str,
        customer_phone: str,
        date: str,
        time_slot: str,
        party_size: int,
        notes: str = ""
    ) -> Optional[Reservation]:
        """
        创建预订
        
        Args:
            space_id: 空间 ID
            customer_name: 客户姓名
            customer_phone: 客户电话
            date: 日期
            time_slot: 时段
            party_size: 人数
            notes: 备注
        
        Returns:
            预订记录或 None
        """
        # 查找空间信息
        space_info = self.get_space_info(space_id)
        if not space_info:
            return None
        
        # 检查是否已被预订
        if self.is_space_booked(space_id, date, time_slot):
            return None
        
        # 计算价格
        total_price = self.calculate_price(space_info, time_slot, party_size)
        
        # 创建预订记录
        reservation = Reservation(
            id=f"res-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            space_id=space_id,
            space_name=space_info.get("name", ""),
            customer_name=customer_name,
            customer_phone=customer_phone,
            date=date,
            time_slot=time_slot,
            party_size=party_size,
            total_price=total_price,
            status="confirmed",
            created_at=datetime.now().isoformat(),
            notes=notes
        )
        
        # 保存
        self.reservations.append(asdict(reservation))
        self.save_reservations()
        
        return reservation
    
    def get_space_info(self, space_id: str) -> Optional[Dict]:
        """获取空间信息"""
        for space_type, spaces in self.spaces.get("spaces", {}).items():
            for space in spaces:
                if space["id"] == space_id:
                    return {**space, "space_type": space_type}
        return None
    
    def calculate_price(self, space_info: Dict, time_slot: str, party_size: int) -> float:
        """计算价格"""
        space_type = space_info.get("space_type", "")
        
        if space_type == "lounge":
            return space_info.get("price_per_person", 0) * party_size
        elif space_type in ["private_room", "meeting_room"]:
            return space_info.get("price_per_3h", space_info.get("price_per_4h", 0))
        else:
            return 0
    
    def get_reservations(self, customer_phone: str = None, date: str = None) -> List[Dict]:
        """查询预订记录"""
        results = self.reservations
        
        if customer_phone:
            results = [r for r in results if r["customer_phone"] == customer_phone]
        
        if date:
            results = [r for r in results if r["date"] == date]
        
        return results
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        """取消预订"""
        for res in self.reservations:
            if res["id"] == reservation_id:
                res["status"] = "cancelled"
                self.save_reservations()
                return True
        return False


def main():
    """测试"""
    service = BookingService()
    
    print("🍵 元树茶馆 - 预订服务测试")
    print()
    
    # 查询可用空间
    print("查询 2026-04-10 14:00-17:00 4 人可用空间:")
    spaces = service.query_spaces(
        date="2026-04-10",
        time_slot="14:00-17:00",
        party_size=4
    )
    for s in spaces:
        print(f"  - {s['name']} ({s['space_type']})")
    
    print()
    
    # 创建预订
    print("创建预订:")
    res = service.create_reservation(
        space_id="room-bamboo",
        customer_name="张三",
        customer_phone="138****1234",
        date="2026-04-10",
        time_slot="14:00-17:00",
        party_size=4
    )
    if res:
        print(f"  ✅ 预订成功：{res.id}")
        print(f"  空间：{res.space_name}")
        print(f"  价格：¥{res.total_price}")
    else:
        print("  ❌ 预订失败")


if __name__ == "__main__":
    main()
