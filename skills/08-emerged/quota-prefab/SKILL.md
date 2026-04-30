# 装配定额 Skill

> 重庆市2018装配式建筑工程计价定额
> 数据来源: 重庆2018计价定额Access 数据库
> 定额总数: **368 条** | 更新日期: 2026-04-24

---

## 📦 定额前缀分类

  - `MA`: 预制构件安装 (49 条)
  - `MB`: 预制混凝土 (134 条)
  - `MC`: 钢结构安装 (29 条)
  - `MD`: 连接工程 (70 条)
  - `ME`: 其他装配 (86 条)

---

## 🔧 使用方法

```python
from skills.emerged.quota_装配 import quota_data

# 搜索定额
results = quota_data.search(keyword="混凝土")

# 按编号查询
item = quota_data.get_by_code("AA0001")

# 获取材料明细
materials = quota_data.get_materials("AA0001")

# 加载全部数据
data = quota_data.load()
```

---

## 📊 数据结构

```json
{
  "deh": "定额编号",
  "xmmc": "项目名称",
  "dw": "单位",
  "dj": "单价(元)",
  "rgf": "人工费(元)",
  "clf": "材料费(元)",
  "jxf": "机械费(元)",
  "chapter": "所属章节",
  "materials": [
    {"code": "材料编码", "name": "材料名称", "amount": 数量}
  ]
}
```

---

## ⚠️ 数据隐私

本 Skill 包含的定额数据**不发布到 GitHub**，仅限本地使用。
数据来源: 重庆市建设工程计价定额（2018版）

---

*太一 AGI · 定额知识库 · 2026.4.24*
