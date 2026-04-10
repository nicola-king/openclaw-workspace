# 市政工程造价 Skill

> **版本**: 1.2.0  
> **创建时间**: 2026-04-10  
> **地区**: 重庆  
> **定额**: 2018/2020 版

---

## 📋 功能模块

| 文件 | 功能 | 状态 |
|------|------|------|
| `cost.py` | 造价计算 | ✅ 完成 |
| `material_prices.py` | 材料价格管理 | ✅ 完成 |
| `SKILL.md` | 技能说明 | ✅ 完成 |

---

## 🔧 使用方式

### 造价计算

```bash
# 道路工程
python3 cost.py --type road -l 1000 -w 20 \
  --structure "沥青混凝土路面" \
  --region "重庆" --standard "2018 定额"

# 桥梁工程
python3 cost.py --type bridge -s 30 -w 15 \
  --structure "预应力混凝土简支梁" \
  --region "重庆"

# 管网工程
python3 cost.py --type pipeline -d DN800 -l 500 \
  --material "HDPE 双壁波纹管" \
  --region "重庆"
```

### 材料价格管理

```bash
# 查询材料价格
python3 material_prices.py --action get -m "HDPE 双壁波纹管 DN800"

# 查询可用月份
python3 material_prices.py --action months

# 查看价格趋势
python3 material_prices.py --action trend -m "HRB400E 钢筋 Φ20" -n 6

# 更新材料价格
python3 material_prices.py --action update -m "HRB400E 钢筋 Φ20" -p 4200

# 从造价站导入
python3 material_prices.py --action import -f 重庆造价站_2026 年 3 月.csv
```

---

## 📊 费用标准 (重庆地区)

| 费用项目 | 费率 | 说明 |
|---------|------|------|
| 安全文明施工费 | 2.5% | 市政工程 |
| 措施项目费 | 2.5% | 市政工程 |
| 其他项目费 | 2% | - |
| 规费 | 28% | 人工费比例 |
| 税金 | 9% | 增值税 |

---

## 📁 文件结构

```
skills/civil-engineering-cost/
├── README.md                 # 本文件
├── SKILL.md                  # 技能说明
├── cost.py                   # 造价计算器
├── material_prices.py        # 材料价格管理
└── config/
    ├── chongqing_sources.md  # 重庆地区信息来源
    ├── material_prices.json  # 材料数据库 (23 种)
    └── price_history.json    # 价格历史记录
```

---

## ⚠️ 常见问题

### 1. 模块导入错误

```bash
# 确保在正确的目录执行
cd /home/nicola/.openclaw/workspace/skills/civil-engineering-cost
python3 cost.py ...
```

### 2. 配置文件缺失

```bash
# 检查 config 目录
ls -la config/

# 如果缺失，重新初始化
python3 -c "
import json
from pathlib import Path
config_dir = Path('config')
config_dir.mkdir(exist_ok=True)
with open(config_dir / 'material_prices.json', 'w') as f:
    json.dump({}, f)
"
```

### 3. 中文材料名问题

```bash
# 使用引号包裹中文参数
python3 material_prices.py --action get -m "HDPE 双壁波纹管 DN800"
```

---

## 📞 数据来源

- 重庆市建设工程造价管理总站
- 重庆市住房和城乡建设委员会
- 重庆建设工程造价信息网

---

*文档：太一 AGI · 市政工程造价 Skill*  
*更新时间：2026-04-10*
