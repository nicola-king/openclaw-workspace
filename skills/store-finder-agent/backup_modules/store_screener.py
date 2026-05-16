"""
店铺寻址 Agent — 店面候选筛选模块 v1.0
功能：面积/租金/人流/交通/竞品评分 → 候选排序 + 热力图数据
"""
import json, csv, math, random
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

@dataclass
class StoreCandidate:
    id: str
    district: str
    name: str
    address: str
    lat: float
    lng: float
    area_sqm: float
    monthly_rent: float
    rent_per_sqm: float
    foot_traffic: int
    nearby_subway_m: int
    nearby_bus_stops: int
    competitor_500m: int
    floor: int = 1
    decoration: str = "简装"
    available: bool = True

    @property
    def traffic_score(self) -> float:
        return min(self.foot_traffic / 20000, 1) * 30

    @property
    def rent_score(self) -> float:
        return max(0, 1 - self.rent_per_sqm / 500) * 25

    @property
    def transport_score(self) -> float:
        subway = max(0, 1 - self.nearby_subway_m / 1000) * 15
        bus = min(self.nearby_bus_stops, 5) * 3
        return min(subway + bus, 25)

    @property
    def competition_score(self) -> float:
        return max(0, 1 - self.competitor_500m / 10) * 20

    @property
    def total_score(self) -> float:
        return round(self.traffic_score + self.rent_score + 
                     self.transport_score + self.competition_score, 1)


def make_store(id, district, name, address, lat, lng, 
               area, rent, rent_per, traffic, subway_m, 
               bus, comp, floor=1, deco="简装", avail=True):
    """工厂函数：确保字段顺序正确"""
    return StoreCandidate(
        id=id, district=district, name=name, address=address,
        lat=lat, lng=lng, area_sqm=area, monthly_rent=rent,
        rent_per_sqm=rent_per, foot_traffic=traffic,
        nearby_subway_m=subway_m, nearby_bus_stops=bus,
        competitor_500m=comp, floor=floor, decoration=deco,
        available=avail
    )


class StoreScreener:
    """店面筛选引擎"""

    BUILTIN_STORES = {
        "北京-国贸/CBD": [
            make_store("bj-cbd-1", "国贸/CBD", "国贸大厦A座B1", "国贸商圈", 39.9095, 116.4620,
                       120, 42000, 350, 25000, 50, 8, 3, -1, "精装"),
            make_store("bj-cbd-2", "国贸/CBD", "建外SOHO 3号楼", "国贸商圈", 39.9070, 116.4580,
                       85, 25500, 300, 18000, 200, 5, 5, 2, "精装"),
            make_store("bj-cbd-3", "国贸/CBD", "银泰中心B1层", "国贸商圈", 39.9100, 116.4650,
                       200, 80000, 400, 35000, 100, 6, 6, -1, "豪装"),
            make_store("bj-cbd-4", "国贸/CBD", "华贸中心1层", "国贸商圈", 39.9060, 116.4700,
                       150, 52500, 350, 22000, 150, 4, 4, 1, "精装"),
            make_store("bj-cbd-5", "国贸/CBD", "万达广场1层", "国贸商圈", 39.9110, 116.4600,
                       180, 63000, 350, 20000, 300, 5, 2, 1, "中装"),
        ],
        "北京-望京": [
            make_store("bj-wk-1", "望京", "望京SOHO T1", "望京商圈", 39.9970, 116.4790,
                       130, 26000, 200, 15000, 100, 6, 2, 5, "精装"),
            make_store("bj-wk-2", "望京", "新荟城1层", "望京商圈", 39.9990, 116.4820,
                       100, 18000, 180, 12000, 50, 4, 3, 1, "简装"),
            make_store("bj-wk-3", "望京", "望京国际商业中心", "望京商圈", 40.0010, 116.4750,
                       160, 32000, 200, 18000, 200, 5, 4, 2, "中装"),
        ],
        "上海-南京西路": [
            make_store("sh-nj-1", "南京西路", "恒隆广场B1", "静安商圈", 31.2290, 121.4530,
                       100, 60000, 600, 40000, 50, 8, 5, -1, "豪装"),
            make_store("sh-nj-2", "南京西路", "兴业太古汇LG1", "静安商圈", 31.2260, 121.4560,
                       150, 82500, 550, 35000, 100, 6, 4, -1, "豪装"),
            make_store("sh-nj-3", "南京西路", "丰盛里1层", "静安商圈", 31.2270, 121.4500,
                       80, 32000, 400, 22000, 300, 4, 3, 1, "精装"),
        ],
    }

    def __init__(self):
        self.data_file = DATA_DIR / "stores.json"
        self.stores: List[StoreCandidate] = []
        self._load()

    def _load(self):
        if self.data_file.exists():
            with open(self.data_file) as f:
                raw = json.load(f)
            self.stores = [StoreCandidate(**s) for s in raw]
        else:
            for dist, ss in self.BUILTIN_STORES.items():
                self.stores.extend(ss)
            self._save()

    def _save(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump([asdict(s) for s in self.stores], f, ensure_ascii=False, indent=2)

    def search(self, city: str = "", district: str = "", min_area: float = 0,
               max_rent: float = 1e9, min_traffic: int = 0,
               max_competitors: int = 99) -> List[Dict]:
        results = []
        for s in self.stores:
            if not s.available: continue
            store_city = ""
            if s.id.startswith("bj-"): store_city = "北京"
            elif s.id.startswith("sh-"): store_city = "上海"
            elif s.id.startswith("sz-"): store_city = "深圳"
            elif s.id.startswith("gz-"): store_city = "广州"
            if city and store_city and store_city != city: continue
            if district and s.district not in district and district not in s.district: continue
            if s.area_sqm < min_area: continue
            if s.monthly_rent > max_rent: continue
            if s.foot_traffic < min_traffic: continue
            if s.competitor_500m > max_competitors: continue
            results.append({**asdict(s), "city": store_city, "total_score": s.total_score})
        return sorted(results, key=lambda x: -x["total_score"])

    def export_csv(self, data: List[Dict], output: str = "") -> str:
        if not data: return ""
        output = output or str(DATA_DIR / "stores_export.csv")
        with open(output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return output


if __name__ == "__main__":
    sc = StoreScreener()
    for dist in ["北京-国贸/CBD", "北京-望京", "上海-南京西路"]:
        print(f"\n【{dist}】候选排名:")
        results = sc.search("北京" if "北京" in dist else "上海", district=dist.split("-")[-1])
        for r in results[:5]:
            print(f"  {r['name']}: {r['total_score']}分 | {r['area_sqm']}m² | ¥{r['monthly_rent']:,}/月 | 人流{r['foot_traffic']:,}/日")
