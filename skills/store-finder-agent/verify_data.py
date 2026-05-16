"""验证数据真实性——使用太一共享搜索获取重庆真实数据"""
import sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from data_layer.search_adapter import search_poi, search_economic, is_available

print(f"🔗 共享搜索可用: {is_available()}")
print()

# 重庆江北区/渝北区真实数据
cities = ["重庆", "重庆江北区", "重庆渝北区"]
for city in cities:
    pois = search_poi(city)
    if pois and len(pois) > 2:
        print(f"📍 {city}: 搜索到 {len(pois)} 个POI")
        for p in pois[:5]:
            name = p.get("name", str(p))[:40]
            print(f"   - {name}")
    else:
        print(f"📍 {city}: 无实时数据（使用后备）")

eco = search_economic("重庆")
print(f"\n💰 重庆经济数据: {eco}")
