# Company Enricher — 公司信息增强引擎 v1.0

> **版本**: 1.0.0  
> **创建时间**: 2026-05-04  
> **职责**: 为贵客之路提供真实公司地址/电话/邮箱/联系人/LinkedIn  
> **位置**: 搜寻(1) → ⭐信息增强(2) → 清洗(3) → 触达(4) → 培育(5)

---

## 🎯 解决的问题

- ❌ 搜到的公司没有真实联系方式
- ✅ 从官网/ABN/Google Maps 自动提取
- ✅ 关联 LinkedIn 公司和联系人
- ✅ 存入数据库，可重复使用
- ✅ 标注数据质量等级

## 📊 数据结构

| 字段 | 来源 | 说明 |
|------|------|------|
| name | 搜索输入 | 公司名称 |
| website | 搜索/爬取 | 官网URL |
| phone | 官网/手动 | 联系电话 |
| email | 官网/手动 | 联系邮箱 |
| address | 官网/手动 | 完整地址 |
| city/state/postcode | 地址提取 | 自动解析 |
| linkedin_url | 搜索/手动 | LinkedIn公司页 |
| contacts | 手动输入 | 联系人(姓名/职位/邮箱/LinkedIn) |
| data_quality | 自动评估 | A+/A/B/C/D 等级 |

## 🔧 使用

```bash
# 列出已保存公司
python3 core.py --list

# 增强单个公司
python3 core.py --enrich "Modscape"

# 从网站提取信息
python3 core.py --website "https://modscape.com.au"

# 全流程验证
python3 core.py --verify "prefabAUS"
```

---

*太一 AGI · Company Enricher · 2026-05-04*
