# 配置文件说明

> **目录**: `skills/civil-engineering-cost/config/`

---

## 📁 文件列表

| 文件 | 说明 | 大小 |
|------|------|------|
| `chongqing_sources.md` | 重庆地区信息来源 | ~4KB |
| `material_prices.json` | 材料价格数据库 | ~2KB |
| `price_history.json` | 价格历史记录 | ~0KB (初始) |
| `README.md` | 本说明文件 | ~1KB |

---

## 📊 material_prices.json

**材料数据库格式**:

```json
{
  "钢材": {
    "HRB400E 钢筋 Φ10": {"unit": "t", "price": 4250, "previous": 4200},
    "HRB400E 钢筋 Φ20": {"unit": "t", "price": 4180, "previous": 4150}
  },
  "水泥": {
    "P.O 42.5 水泥": {"unit": "t", "price": 520, "previous": 510}
  }
}
```

**材料类别**:
- 钢材 (4 种)
- 水泥 (3 种)
- 砂石 (4 种)
- 沥青 (3 种)
- 管材 (4 种)
- 商品混凝土 (5 种)

**总计**: 23 种材料

---

## 📈 price_history.json

**价格历史记录格式**:

```json
{
  "HRB400E 钢筋 Φ20": [
    {
      "date": "2026-04-10T16:20:00",
      "old_price": 4150,
      "new_price": 4180,
      "change_rate": 0.72
    }
  ]
}
```

**更新机制**:
- 每次更新价格时自动记录
- 保留历史变动记录
- 支持价格趋势分析

---

## 🔄 数据更新流程

### 从重庆造价站导入

```bash
# 1. 下载造价站 Excel/CSV
# 2. 导入系统
python3 material_prices.py --action import -f 重庆造价站_2026 年 5 月.csv

# 3. 验证导入
python3 material_prices.py --action months
```

### 手动更新价格

```bash
# 更新单个材料价格
python3 material_prices.py --action update -m "HRB400E 钢筋 Φ20" -p 4200

# 验证更新
python3 material_prices.py --action get -m "HRB400E 钢筋 Φ20"
```

---

## ⚠️ 注意事项

1. **不要手动编辑 JSON 文件** - 使用命令行工具更新
2. **定期备份** - 每月导入新数据前备份
3. **检查格式** - 确保 JSON 格式正确

---

*文档：太一 AGI · 市政工程造价 Skill*  
*创建时间：2026-04-10*
