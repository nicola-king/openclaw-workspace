# Google Maps 集成 - 快速入门

## 📦 安装完成

✅ 技能文件已创建  
✅ CLI 工具已安装  
✅ 配置模板已更新

---

## 🔑 配置 API Key

### 步骤 1: 获取 Google Maps API Key

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用以下 API:
   - Maps JavaScript API
   - Geocoding API
   - Places API
   - Directions API
   - Distance Matrix API
   - Static Maps API
4. 创建 API Key
5. 复制 API Key

### 步骤 2: 配置 API Key

编辑配置文件:
```bash
nano ~/.openclaw/workspace-taiyi/config/google-integration.json
```

修改 `maps` 部分:
```json
{
  "maps": {
    "enabled": true,
    "apiKey": "YOUR_API_KEY_HERE"
  }
}
```

### 步骤 3: 测试

```bash
# 测试地理编码
python3 skills/google-maps-integration/maps.py geocode "北京市朝阳区"

# 测试路线规划
python3 skills/google-maps-integration/maps.py directions "北京" "上海"

# 测试地点搜索
python3 skills/google-maps-integration/maps.py search "咖啡馆" --location "39.9042,116.4074" --radius 1000
```

---

## 📋 可用命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `geocode` | 地址→坐标 | `maps.py geocode "北京市朝阳区"` |
| `reverse-geocode` | 坐标→地址 | `maps.py reverse-geocode 39.9042 116.4074` |
| `search` | 地点搜索 | `maps.py search "咖啡馆" -l "39.9042,116.4074" -r 1000` |
| `directions` | 路线规划 | `maps.py directions "北京" "上海"` |
| `distance` | 距离矩阵 | `maps.py distance "北京" "上海" -d "广州" "深圳"` |
| `static-map` | 静态地图 | `maps.py static-map -c "北京" -z 10` |

---

## 💰 API 配额与成本

| API | 免费额度 | 单价 (每 1000 次) |
|-----|---------|-----------------|
| Geocoding | 200 次/天 | ¥28 |
| Places | 100 次/天 | ¥56-168 |
| Directions | 2500 次/天 | ¥28 |
| Distance Matrix | 2500 次/天 | ¥28 |
| Static Maps | 25000 次/月 | ¥14 |

**建议**:
- 设置每日预算告警
- 监控 API 使用情况
- 使用缓存减少重复请求

---

## 🌐 网页自动化方案 (备用)

如果不想使用 API，可以使用网页自动化:

```python
from skills.browser_automation.google_services_automation import GoogleServicesAutomation

automation = GoogleServicesAutomation()
automation.start_browser()

# 打开 Google Maps
automation.page.goto("https://maps.google.com")
# ... 进行自动化操作
```

---

## 🔗 相关文件

- `SKILL.md` - 技能详细说明
- `maps.py` - CLI 工具
- `google-integration.json` - 配置文件

---

*创建：2026-04-08 | 太一 AGI*
