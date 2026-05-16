"""
店铺寻址 Agent — 城市+商圈识别模块 v1.0
功能：多源POI分析、商圈识别、人口/交通/竞品评估
输出：商圈热力图数据 + CSV/Excel
"""
import json, csv, math, os
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# ===== 数据模型 =====

@dataclass
class District:
    """商圈数据"""
    id: str
    city: str
    name: str               # 商圈名称
    center_lat: float       # 中心纬度
    center_lng: float       # 中心经度
    radius_km: float = 1.0  # 商圈半径
    population_density: int = 0       # 人口密度(人/km²)
    foot_traffic: int = 0            # 日均人流量
    nearby_subway: int = 0           # 最近地铁站数量(1km内)
    nearby_bus: int = 0              # 公交线路数
    competitor_count: int = 0        # 竞品数量
    average_rent: float = 0.0        # 平均租金(元/月/m²)
    commercial_score: float = 0.0    # 商业活跃度(0-100)
    poi_count: int = 0               # POI数量
    industry_match: float = 0.0      # 行业匹配度(0-100)
    
    @property
    def composite_score(self) -> float:
        """综合商圈评分"""
        score = (
            self.commercial_score * 0.25 +
            min(self.foot_traffic / 100000, 1) * 20 +
            min(self.population_density / 50000, 1) * 15 +
            min(self.nearby_subway, 5) * 5 +
            (100 - self.competitor_count * 5) * 0.1 +
            self.industry_match * 0.1
        )
        return round(score, 1)


class DistrictRecognizer:
    """城市+商圈识别引擎"""

    # ===== 内置示例数据（MVP模拟） =====
    BUILTIN_CITIES = {
        "北京": [
            District("bj-cbd", "北京", "国贸/CBD", 39.9087, 116.4605, 1.5,
                    45000, 800000, 4, 30, 25, 280, 95, 1200, 90),
            District("bj-wdk", "北京", "望京", 39.9980, 116.4805, 1.5,
                    35000, 600000, 3, 20, 18, 180, 90, 800, 85),
            District("bj-wdq", "北京", "五道口/中关村", 39.9920, 116.3380, 1.2,
                    40000, 500000, 3, 25, 12, 200, 92, 600, 80),
            District("bj-szw", "北京", "三里屯", 39.9330, 116.4550, 1.0,
                    30000, 700000, 2, 15, 30, 350, 88, 500, 75),
            District("bj-xyc", "北京", "西单/金融街", 39.9130, 116.3730, 1.2,
                    25000, 400000, 3, 20, 10, 250, 85, 400, 70),
            District("bj-wh", "北京", "王府井", 39.9150, 116.4100, 1.0,
                    20000, 500000, 2, 18, 22, 320, 82, 450, 72),
            District("bj-cy", "北京", "朝阳大悦城", 39.9210, 116.5100, 1.2,
                    35000, 450000, 2, 15, 8, 150, 80, 350, 78),
            District("bj-hsf", "北京", "华熙LIVE/五棵松", 39.9100, 116.2800, 1.5,
                    28000, 350000, 2, 12, 6, 120, 78, 280, 75),
        ],
        "上海": [
            District("sh-ljx", "上海", "陆家嘴", 31.2400, 121.5000, 1.2,
                    40000, 600000, 4, 20, 20, 300, 95, 900, 85),
            District("sh-njb", "上海", "南京西路", 31.2280, 121.4520, 1.0,
                    38000, 700000, 3, 25, 28, 350, 93, 800, 82),
            District("sh-hf", "上海", "淮海路", 31.2200, 121.4650, 1.0,
                    32000, 550000, 3, 20, 20, 280, 90, 650, 80),
            District("sh-xth", "上海", "徐家汇", 31.1960, 121.4370, 1.2,
                    35000, 500000, 3, 22, 15, 220, 88, 550, 78),
            District("sh-yp", "上海", "五角场", 31.2980, 121.5150, 1.5,
                    30000, 400000, 2, 18, 10, 150, 82, 400, 75),
        ],
        "深圳": [
            District("sz-hq", "深圳", "华强北", 22.5450, 114.0850, 1.0,
                    50000, 800000, 3, 20, 30, 250, 90, 1000, 78),
            District("sz-ns", "深圳", "南山科技园", 22.5370, 113.9530, 1.5,
                    35000, 450000, 3, 18, 12, 200, 88, 600, 85),
            District("sz-ft", "深圳", "福田CBD", 22.5210, 114.0580, 1.2,
                    40000, 550000, 4, 25, 15, 260, 92, 700, 82),
            District("sz-lh", "深圳", "罗湖东门", 22.5480, 114.1200, 1.0,
                    45000, 600000, 2, 15, 25, 180, 80, 500, 70),
        ],
        "广州": [
            District("gz-tyc", "广州", "天河路/体育西", 23.1320, 113.3220, 1.5,
                    38000, 650000, 3, 25, 22, 280, 93, 800, 85),
            District("gz-zb", "广州", "珠江新城", 23.1200, 113.3200, 1.2,
                    35000, 500000, 3, 20, 15, 300, 92, 650, 82),
            District("gz-bj", "广州", "北京路", 23.1280, 113.2680, 1.0,
                    40000, 700000, 2, 18, 20, 200, 85, 500, 75),
        ],
    }

    def __init__(self):
        self.data_file = DATA_DIR / "districts.json"
        self.districts: List[District] = []
        self._load()

    def _load(self):
        """加载数据（优先从文件，次选内置）"""
        if self.data_file.exists():
            with open(self.data_file) as f:
                raw = json.load(f)
            self.districts = [District(**d) for d in raw]
        else:
            # 使用内置示例数据
            for city, dists in self.BUILTIN_CITIES.items():
                self.districts.extend(dists)
            self._save()

    def _save(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump([asdict(d) for d in self.districts], f, ensure_ascii=False, indent=2)

    def get_cities(self) -> List[str]:
        return sorted(set(d.city for d in self.districts))

    def search(self, city: str, min_score: float = 0, 
               max_rent: float = 1e9, min_traffic: int = 0,
               industry: str = "") -> List[Dict]:
        """按条件筛选商圈"""
        results = []
        for d in self.districts:
            if d.city != city:
                continue
            if d.composite_score < min_score:
                continue
            if d.average_rent > max_rent:
                continue
            if d.foot_traffic < min_traffic:
                continue
            results.append({
                **asdict(d),
                "composite_score": d.composite_score
            })
        return sorted(results, key=lambda x: -x["composite_score"])

    def export_csv(self, data: List[Dict], output: str = "") -> str:
        """导出CSV"""
        if not data:
            return ""
        output = output or str(DATA_DIR / f"districts_{data[0].get('city','export')}.csv")
        with open(output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return output

    def add_district(self, district: District):
        """添加商圈（支持用户自定义）"""
        self.districts.append(district)
        self._save()


if __name__ == "__main__":
    rec = DistrictRecognizer()
    print(f"支持城市: {', '.join(rec.get_cities())}")
    for city in rec.get_cities():
        results = rec.search(city)
        print(f"\n【{city}】商圈排名:")
        for r in results[:5]:
            print(f"  {r['name']}: {r['composite_score']}分 | 人流{r['foot_traffic']/10000:.0f}万/日 | 租金{r['average_rent']}元/m²")
