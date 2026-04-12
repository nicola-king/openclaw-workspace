# 📊 飞书多维表格文件导入系统

> **创建时间**: 2026-04-12  
> **状态**: ✅ 已就绪  
> **功能**: 创建多维表格 + 文件导入

---

## 🚀 快速开始

### 步骤 1: 创建多维表格

```bash
python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/create_bitable.py
```

**执行后会**:
- ✅ 创建"文件管理系统"多维表格
- ✅ 自动配置字段（文件名/类型/大小/时间/路径/标签/备注/状态）
- ✅ 保存 App ID 和 Table ID 到配置文件

**输出示例**:
```
============================================================
📊 创建飞书多维表格 - 文件管理系统
============================================================

1️⃣  测试连接...
✅ 连接成功

2️⃣  创建多维表格应用...
✅ App ID: cli_xxxxxxxxxxxxx

3️⃣  创建表格...
✅ Table ID: tbxxxxxxxxxxxxxx

4️⃣  保存配置...
✅ 配置已保存

============================================================
✅ 创建完成!
============================================================

📊 多维表格信息:
   应用名称：文件管理系统
   App ID: cli_xxxxxxxxxxxxx
   Table ID: tbxxxxxxxxxxxxxx

📥 使用方法:
   python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/import_files.py <文件路径>

🔗 访问链接:
   https://bytedance.feishu.cn/base/cli_xxxxxxxxxxxxx
```

---

### 步骤 2: 导入文件

#### 导入单个文件

```bash
python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/import_files.py data.xlsx
```

#### 导入多个文件

```bash
python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/import_files.py file1.csv file2.json file3.xlsx
```

#### 导入整个目录

```bash
python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/import_files.py --dir /path/to/files
```

---

## 📋 支持的格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| Excel | `.xlsx`, `.xls` | 自动读取所有工作表 |
| CSV | `.csv` | 自动检测编码 |
| JSON | `.json` | 支持对象/数组 |

---

## 🎯 表格字段

创建的多维表格包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 文件名 | 文本 | 文件名称 |
| 文件类型 | 文本 | 扩展名 (xlsx/csv/json) |
| 文件大小 (KB) | 数字 | 文件大小 |
| 创建时间 | 日期 | 文件创建时间 |
| 修改时间 | 日期 | 文件最后修改时间 |
| 文件路径 | 文本 | 完整路径 |
| 标签 | 文本 | 自定义标签 |
| 备注 | 文本 | 备注信息 |
| 状态 | 单选 | 待处理/已导入/已归档 |

---

## 💡 使用示例

### 示例 1: 导入 Excel 数据

```bash
# 假设有客户数据 Excel
python3 import_files.py customers.xlsx
```

**Excel 内容**:
```
| 姓名 | 电话 | 邮箱 | 公司 |
|------|------|------|------|
| 张三 | 13800138000 | zhangsan@example.com | ABC 公司 |
| 李四 | 13900139000 | lisi@example.com | XYZ 公司 |
```

**导入后**: 自动创建记录，每行一条

---

### 示例 2: 导入 CSV 日志

```bash
# 导入系统日志
python3 import_files.py --dir /var/log/exports/
```

---

### 示例 3: 导入 JSON 配置

```bash
# 导入配置文件
python3 import_files.py config.json
```

**JSON 内容**:
```json
[
  {"name": "项目 A", "budget": 100000, "status": "进行中"},
  {"name": "项目 B", "budget": 200000, "status": "已完成"}
]
```

---

## 🔧 高级用法

### 手动创建自定义表格

```python
from feishu_client import FeishuClient

client = FeishuClient()

# 创建应用
app_result = client._request("POST", 
    "https://open.feishu.cn/open-apis/bitable/v1/apps",
    json={"title": "我的表格"}
)
app_id = app_result['data']['app_id']

# 创建表格
fields = [
    {"field_name": "姓名", "type": 1},      # 文本
    {"field_name": "年龄", "type": 2},      # 数字
    {"field_name": "生日", "type": 3},      # 日期
    {"field_name": "部门", "type": 4},      # 单选
]

table_result = client._request("POST",
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables",
    json={"table_name": "员工表", "fields": fields}
)
table_id = table_result['data']['table_id']
```

---

### 批量导入记录

```python
from bitable_importer import FeishuBitableImporter

importer = FeishuBitableImporter()

records = [
    {"fields": {"姓名": "张三", "年龄": 30, "部门": "技术部"}},
    {"fields": {"姓名": "李四", "年龄": 28, "部门": "产品部"}},
    {"fields": {"姓名": "王五", "年龄": 35, "部门": "市场部"}},
]

importer.create_records(app_id, table_id, records)
```

---

## 📁 文件结构

```
skills/feishu-integration/
├── feishu_client.py        # 飞书客户端核心
├── bitable_importer.py     # 多维表格导入器
├── create_bitable.py       # 创建表格脚本
├── import_files.py         # 文件导入脚本
└── BITABLE_IMPORT.md       # 本文档
```

---

## 🔍 故障排除

### 问题 1: 未配置多维表格

**错误**: `❌ 未配置多维表格`

**解决**:
```bash
# 先创建多维表格
python3 create_bitable.py
```

---

### 问题 2: 连接失败

**错误**: `❌ 连接失败`

**解决**:
1. 检查配置文件：`cat config/feishu/config.json`
2. 确认 App ID 和 App Secret 正确
3. 确认应用已发布且有权限

---

### 问题 3: 文件格式不支持

**错误**: `❌ 不支持的文件类型：.xxx`

**解决**: 仅支持 `.xlsx`, `.xls`, `.csv`, `.json`

---

### 问题 4: 字段不匹配

**错误**: 导入成功但数据为空

**解决**:
1. 检查 CSV/Excel 表头是否与表格字段匹配
2. 字段名必须完全一致（包括空格）
3. 可以在导入前手动调整表格字段

---

## 📚 API 文档

- [飞书多维表格 API](https://open.feishu.cn/document/ukTMukTMukTM/uQjN1YjL0YDMxUjN)
- [记录管理](https://open.feishu.cn/document/ukTMukTMukTM/ukTMukTMukTM0Mz4SM4MjLxUzM)
- [字段类型](https://open.feishu.cn/document/ukTMukTMukTM/uQjN1YjL0YDMxUjM)

---

## 🎨 最佳实践

### 1. 定期导入
设置定时任务，每天自动导入新文件：

```bash
# crontab -e
0 2 * * * python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/import_files.py --dir /data/daily/
```

---

### 2. 数据备份
导入前备份原文件：

```bash
cp data.xlsx data.xlsx.bak
python3 import_files.py data.xlsx
```

---

### 3. 数据验证
导入后检查记录数：

```python
from feishu_client import FeishuClient

client = FeishuClient()
records = client.get_bitable_records(app_id, table_id)
print(f"总记录数：{len(records['items'])}")
```

---

### 4. 标签管理
使用标签分类文件：

```
标签示例:
- 财务
- 人事
- 项目
- 合同
- 报告
```

---

## 🌟 未来计划

- [ ] 支持 PDF 文件解析
- [ ] 支持图片 OCR 识别
- [ ] 支持自动字段映射
- [ ] 支持数据清洗
- [ ] 支持增量导入
- [ ] 支持导出功能

---

**太一 AGI · 2026-04-12** ✨
