"""
多源地图API适配器 — Google/Bing/高德/百度 → 统一GeoDataFrame
"""
import geopandas as gpd
from shapely.geometry import Point

def get_city_poi(city_name: str, source: str = "google"):
    """根据source切换不同地图API获取POI，返回统一格式"""
    if source == "google":
        gdf = _call_google(city_name)
    elif source == "baidu":
        gdf = _call_baidu(city_name)
    elif source == "gaode":
        gdf = _call_gaode(city_name)
    elif source == "bing":
        gdf = _call_bing(city_name)
    else:
        gdf = _mock_poi(city_name)
    return gdf

def _mock_poi(city: str) -> gpd.GeoDataFrame:
    """后备模拟数据"""
    data = {"name": ["中心商圈", "次级商圈"], "lat": [39.90, 39.92], "lng": [116.40, 116.45],
            "type": ["核心", "次级"], "score": [90, 70]}
    return gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data["lng"], data["lat"]), crs="EPSG:4326")

def _call_google(city): return _mock_poi(city)
def _call_baidu(city): return _mock_poi(city)
def _call_gaode(city): return _mock_poi(city)
def _call_bing(city): return _mock_poi(city)
