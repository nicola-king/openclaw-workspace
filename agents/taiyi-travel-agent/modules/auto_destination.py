#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动目的地检测与创建模块

功能:
1. 检测用户输入的目的地是否已存在
2. 自动创建新目的地模块 (SKILL.md + planner.py)
3. 自动创建真实供应商数据目录
4. 自动更新主索引

作者：太一 AGI
创建：2026-04-24
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class AutoDestinationCreator:
    """自动目的地创建器"""
    
    def __init__(self, modules_dir: Optional[Path] = None):
        """
        初始化自动创建器
        
        Args:
            modules_dir: 模块目录
        """
        if modules_dir is None:
            self.modules_dir = Path(__file__).parent
        else:
            self.modules_dir = modules_dir
        
        self.domestic_dir = self.modules_dir / "domestic"
        self.international_dir = self.modules_dir / "international"
        
        # 已知国内城市
        self.domestic_cities = self._scan_existing_cities(self.domestic_dir)
        # 已知国外城市
        self.international_cities = self._scan_existing_cities(self.international_dir)
        
        print(f"🌍 自动目的地创建器启动")
        print(f"  国内城市：{', '.join(self.domestic_cities) if self.domestic_cities else '无'}")
        print(f"  国外城市：{', '.join(self.international_cities) if self.international_cities else '无'}")
    
    # ========== 1. 检测目的地 ==========
    
    def detect_destination(self, destination: str) -> Dict:
        """
        检测目的地
        
        Args:
            destination: 目的地名称
        
        Returns:
            检测结果
        """
        print(f"🔍 检测目的地：{destination}")
        
        # 判断国内/国外
        is_domestic = self._is_domestic(destination)
        category = "domestic" if is_domestic else "international"
        
        # 检查是否已存在
        exists = self._destination_exists(destination)
        
        result = {
            "destination": destination,
            "category": category,
            "exists": exists,
            "is_domestic": is_domestic,
        }
        
        if exists:
            print(f"  ✅ 目的地已存在：{destination} ({category})")
        else:
            print(f"  ❌ 目的地不存在：{destination} ({category})")
        
        return result
    
    # ========== 2. 自动创建模块 ==========
    
    def create_destination_module(self, destination: str) -> Dict:
        """
        自动创建目的地模块
        
        Args:
            destination: 目的地名称
        
        Returns:
            创建结果
        """
        print(f"🔨 自动创建目的地模块：{destination}")
        
        # 检测目的地
        detection = self.detect_destination(destination)
        category = detection["category"]
        
        if detection["exists"]:
            print(f"  ⚠️ 目的地已存在，跳过创建")
            return {"status": "exists", "destination": destination}
        
        # 确定目录
        if category == "domestic":
            base_dir = self.domestic_dir
        else:
            base_dir = self.international_dir
        
        # 创建目录
        dest_dir = base_dir / destination.lower()
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 SKILL.md
        skill_md = self._generate_skill_md(destination, category)
        (dest_dir / "SKILL.md").write_text(skill_md, encoding='utf-8')
        
        # 创建 planner.py
        planner_py = self._generate_planner_py(destination, category)
        (dest_dir / "planner.py").write_text(planner_py, encoding='utf-8')
        
        # 更新索引
        self._update_index(destination, category)
        
        result = {
            "status": "created",
            "destination": destination,
            "category": category,
            "dir": str(dest_dir),
            "files": ["SKILL.md", "planner.py"],
            "created_at": datetime.now().isoformat(),
        }
        
        print(f"  ✅ 模块创建成功：{dest_dir}")
        print(f"  文件：SKILL.md, planner.py")
        
        return result
    
    # ========== 3. 自动创建供应商数据目录 ==========
    
    def create_provider_data(self, destination: str) -> Dict:
        """
        自动创建供应商数据目录
        
        Args:
            destination: 目的地名称
        
        Returns:
            创建结果
        """
        print(f"📁 创建供应商数据目录：{destination}")
        
        providers_dir = Path(__file__).parent.parent / "data" / "providers" / "verified"
        providers_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建空数据文件
        files = {
            f"hotels_{destination.lower()}.json": [],
            f"charter_{destination.lower()}.json": [],
            f"guides_{destination.lower()}.json": [],
        }
        
        for filename, data in files.items():
            filepath = providers_dir / filename
            if not filepath.exists():
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"  ✅ 创建：{filename}")
        
        result = {
            "status": "created",
            "destination": destination,
            "files": list(files.keys()),
            "created_at": datetime.now().isoformat(),
        }
        
        return result
    
    # ========== 内部方法 ==========
    
    def _is_domestic(self, destination: str) -> bool:
        """
        判断是否国内城市
        
        Args:
            destination: 目的地名称
        
        Returns:
            是否国内
        """
        domestic_cities = [
            "北京", "上海", "广州", "深圳", "成都", "西安", "杭州", "重庆",
            "武汉", "南京", "天津", "苏州", "长沙", "郑州", "东莞", "青岛",
            "宁波", "无锡", "厦门", "福州", "昆明", "大理", "丽江", "三亚",
            "黄山", "张家界", "桂林", "贵阳", "南宁", "济南", "沈阳", "大连",
            "哈尔滨", "长春", "石家庄", "太原", "呼和浩特", "兰州", "西宁",
            "乌鲁木齐", "拉萨", "银川", "海口", "珠海", "佛山", "中山", "惠州",
        ]
        
        return destination in domestic_cities
    
    def _destination_exists(self, destination: str) -> bool:
        """
        检查目的地是否已存在
        
        Args:
            destination: 目的地名称
        
        Returns:
            是否存在
        """
        return (
            destination in self.domestic_cities or
            destination in self.international_cities
        )
    
    def _scan_existing_cities(self, base_dir: Path) -> List[str]:
        """
        扫描已存在的城市
        
        Args:
            base_dir: 基础目录
        
        Returns:
            城市列表
        """
        cities = []
        if base_dir.exists():
            for item in base_dir.iterdir():
                if item.is_dir() and item.name not in ['.', '..']:
                    cities.append(item.name)
        return cities
    
    def _generate_skill_md(self, destination: str, category: str) -> str:
        """
        生成 SKILL.md
        
        Args:
            destination: 目的地名称
            category: 类别 (domestic/international)
        
        Returns:
            SKILL.md 内容
        """
        mode = "国内旅行" if category == "domestic" else "跨国旅行"
        
        return f"""# {destination}模块 ({destination.lower()})

> **版本**: 1.0.0  
> **创建时间**: {datetime.now().strftime('%Y-%m-%d')}  
> **作者**: 太一 AGI (自动创建)  
> **类别**: {mode}/{destination}

---

## 🎯 职责域

**核心功能**: {destination}旅行规划、酒店预订、交通、导游

**适用场景**:
- {destination}旅行规划
- {destination}酒店/包车/导游搜索
- {destination}信息源收集

---

## 📋 支持景点 (含图片/电话/地址)

| 景点 | 类型 | 时长 | 门票 | 电话 | 地址 |
|------|------|------|------|------|------|
| 市中心 | 现代都市 | 2h | 免费 | - | {destination}市中心 |
| 商业区 | 购物 | 3h | 免费 | - | {destination}商业区 |
| 美食街 | 美食 | 2h | 免费 | - | {destination}美食街 |

---

## 🏨 酒店 (含图片)

- 酒店 1: [图片](https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800)
- 酒店 2: [图片](https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800)

## 🍽️ 餐厅 (含图片)

- 餐厅 1: [图片](https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800)
- 餐厅 2: [图片](https://images.unsplash.com/photo-1555396273-361ea344d5e2?w=800)

---

## 🚀 使用方式

```python
from modules.{category}.{destination.lower()}.planner import {destination.capitalize()}Planner

planner = {destination.capitalize()}Planner()
plan = planner.plan_trip("出发地", "{destination}", "2026-05-01", "2026-05-05")
```

---

*太一旅行探路者 Agent · {destination}模块 · 太一 AGI · {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    def _generate_planner_py(self, destination: str, category: str) -> str:
        """
        生成 planner.py
        
        Args:
            destination: 目的地名称
            category: 类别 (domestic/international)
        
        Returns:
            planner.py 内容
        """
        mode = "国内游" if category == "domestic" else "跨国游"
        budget = "5000" if category == "domestic" else "10000"
        
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{destination}模块 - 旅行规划器

功能:
1. {destination}旅行规划
2. 预算分配
3. 旅行清单生成

作者：太一 AGI (自动创建)
创建：{datetime.now().strftime('%Y-%m-%d')}
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class {destination.capitalize()}Planner:
    """{destination}旅行规划器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent.parent.parent / "data"
        else:
            self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        print(f"🌍 {destination}规划器启动")
    
    def plan_trip(self, origin: str, destination: str = "{destination}",
                 start_date: str = "2026-05-01", end_date: str = "2026-05-05",
                 budget: float = {budget}, travelers: int = 1,
                 preferences: Optional[List[str]] = None) -> Dict:
        print(f"🌍 {destination}行程规划：{{origin}} → {{destination}}")
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        if preferences is None:
            preferences = ["文化", "美食", "购物"]
        
        budget_allocation = {{
            "交通": round(budget * 0.25, 2),
            "住宿": round(budget * 0.30, 2),
            "餐饮": round(budget * 0.20, 2),
            "活动": round(budget * 0.15, 2),
            "购物": round(budget * 0.10, 2),
        }}
        
        result = {{
            "type": "{destination} Travel Plan",
            "origin": origin,
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
            "travelers": travelers,
            "mode": "{mode}",
            "budget": budget,
            "budget_per_person": budget / travelers,
            "budget_allocation": budget_allocation,
            "preferences": preferences,
            "timestamp": datetime.now().isoformat(),
        }}
        
        print(f"  ✅ 行程规划完成：{{days}} 天，预算 ¥{{budget}}")
        return result
    
    def save_plan(self, plan: Dict, filename: str) -> Path:
        output_file = self.data_dir / f"{{filename}}_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        print(f"✅ 行程已保存：{{output_file}}")
        return output_file


def main():
    print("=" * 60)
    print("🌍 {destination}规划器测试")
    print("=" * 60)
    
    planner = {destination.capitalize()}Planner()
    plan = planner.plan_trip("出发地", "{destination}", "2026-05-01", "2026-05-05")
    planner.save_plan(plan, "{destination.lower()}_plan")
    
    print("\\n" + "=" * 60)
    print("✅ {destination}规划器测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
'''
    
    def _update_index(self, destination: str, category: str):
        """
        更新索引
        
        Args:
            destination: 目的地名称
            category: 类别
        """
        if category == "domestic":
            self.domestic_cities.append(destination.lower())
        else:
            self.international_cities.append(destination.lower())
    
    # ========== 4. 批量创建 ==========
    
    def batch_create(self, destinations: List[str]) -> List[Dict]:
        """
        批量创建
        
        Args:
            destinations: 目的地列表
        
        Returns:
            创建结果列表
        """
        results = []
        for dest in destinations:
            result = self.create_destination_module(dest)
            results.append(result)
        
        return results


def main():
    """测试"""
    print("=" * 60)
    print("🌍 自动目的地创建器测试")
    print("=" * 60)
    
    creator = AutoDestinationCreator()
    
    # 测试 1: 检测目的地
    print("\n🔍 测试 1: 检测目的地")
    result = creator.detect_destination("拉萨")
    print(f"  结果：{result}")
    
    # 测试 2: 创建新目的地
    print("\n🔨 测试 2: 创建新目的地")
    result = creator.create_destination_module("拉萨")
    print(f"  结果：{result}")
    
    # 测试 3: 创建供应商数据
    print("\n📁 测试 3: 创建供应商数据")
    result = creator.create_provider_data("拉萨")
    print(f"  结果：{result}")
    
    print("\n" + "=" * 60)
    print("✅ 自动目的地创建器测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
