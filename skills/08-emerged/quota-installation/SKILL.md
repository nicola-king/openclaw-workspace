# 安装定额 Skill

> 重庆市2018安装工程计价定额
> 数据来源: 重庆2018计价定额Access 数据库
> 定额总数: **16511 条** | 更新日期: 2026-04-24

---

## 📦 定额前缀分类

  - `CA`: 机械设备安装 (1365 条)
  - `CB`: 热力设备安装 (826 条)
  - `CC`: 静止设备制作 (2082 条)
  - `CD`: 电气设备安装 (2345 条)
  - `CE`: 仪表安装 (1030 条)
  - `CF`: 自动化仪表 (980 条)
  - `CG`: 通风空调 (538 条)
  - `CH`: 工业管道 (3328 条)
  - `CJ`: 消防工程 (343 条)
  - `CK`: 给排水采暖 (1823 条)
  - `CL`: 刷油防腐保温 (1851 条)

---

## 🔧 使用方法

```python
from skills.emerged.quota_安装 import quota_data

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
