"""可视化Agent — 地图热力图/对比图表/报告可视化"""
from pathlib import Path
import folium
def generate_map(gdf, stores, output="static/decision_map.html"):
    m = folium.Map(zoom_start=13)
    m.save(output); return output
