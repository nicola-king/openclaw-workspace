---
name: google-maps-integration
version: 1.0.0
description: Google Maps 集成 - 地图/地理编码/路线/地点搜索
category: integration
tags: ['google', 'maps', 'geocoding', 'routes', 'places', 'api', '地图']
author: 太一 AGI
created: 2026-04-08
updated: 2026-04-08
status: active
priority: P1
---

# Google Maps 集成技能

> **版本**: 1.0.0 | **创建**: 2026-04-08  
> **负责**: 太一 | **状态**: ✅ 已激活

---

## 🎯 功能

- ✅ 地理编码 (地址→坐标)
- ✅ 逆地理编码 (坐标→地址)
- ✅ 地点搜索 (POI)
- ✅ 路线规划
- ✅ 距离矩阵
- ✅ 静态地图生成
- ✅ 网页自动化 (备用方案)

---

## 🔧 配置

### 1. 获取 Google Maps API Key

1. 访问 https://console.cloud.google.com/
2. 创建新项目或选择现有项目
3. 启用以下 API:
   - Maps JavaScript API
   - Geocoding API
   - Places API
   - Directions API
   - Distance Matrix API
   - Static Maps API
4. 创建 API Key
5. 保存 API Key 到安全位置

### 2. 配置 API Key

编辑 `~/.openclaw/workspace-taiyi/config/google-integration.json`:

```json
{
  "maps": {
    "enabled": true,
    "apiKey": "YOUR_API_KEY_HERE",
    "quota": {
      "maxRequestsPerDay": 1000,
      "maxRequestsPerMinute": 60
    }
  }
}
```

---

## 📋 命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `maps geocode` | 地址→坐标 | `maps geocode "北京市朝阳区"` |
| `maps reverse-geocode` | 坐标→地址 | `maps reverse-geocode 39.9042,116.4074` |
| `maps search` | 地点搜索 | `maps search "咖啡馆" --location "北京"` |
| `maps directions` | 路线规划 | `maps directions "北京" "上海"` |
| `maps distance` | 距离矩阵 | `maps distance "北京" "上海","广州"` |
| `maps static-map` | 静态地图 | `maps static-map --center "北京" --zoom 10` |

---

## 🚀 使用示例

### 地理编码
```bash
太一，查询 "北京市朝阳区" 的坐标
```

### 逆地理编码
```bash
太一，查询坐标 39.9042,116.4074 的地址
```

### 地点搜索
```bash
太一，搜索北京附近的咖啡馆
```

### 路线规划
```bash
太一，规划从北京到上海的路线
```

### 静态地图
```bash
太一，生成北京市中心的地图图片
```

---

## 💰 API 配额与成本

| API | 免费额度 | 单价 (每 1000 次) |
|-----|---------|-----------------|
| Geocoding | 200 次/天 | ¥28 |
| Places | 100 次/天 | ¥56-168 |
| Directions | 2500 次/天 | ¥28 |
| Distance Matrix | 2500 次/天 | ¥28 |
| Static Maps | 25000 次/月 | ¥14 |

**建议**: 设置预算告警，避免超额消费

---

## 🔗 相关文件

- `skills/browser-automation/google-services-automation.py` - Google 服务自动化
- `workspace-taiyi/config/google-integration.json` - Google 集成配置

---

*创建：2026-04-08 | 太一 AGI*
