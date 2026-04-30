---
name: feishu-bitable
description: |
  飞书多维表格（Bitable）的创建、查询、编辑和管理工具。支持记录增删改查、字段管理、视图管理、批量操作。
---

# Feishu Bitable Tool

**激活条件**：用户提到"多维表格"、"bitable"、"数据表"、"记录"、"字段"，或需要创建/管理飞书多维表格。

## 核心能力

| 操作 | 工具 | Action | 必填参数 |
|------|------|--------|---------|
| 创建多维表格 | feishu_bitable_app | create | name |
| 列出数据表 | feishu_bitable_app_table | list | app_token |
| 创建数据表 | feishu_bitable_app_table | create | app_token, name |
| 列出字段 | feishu_bitable_app_table_field | list | app_token, table_id |
| 创建字段 | feishu_bitable_app_table_field | create | app_token, table_id, field_name, type |
| 查询记录 | feishu_bitable_app_table_record | list | app_token, table_id |
| 新增记录 | feishu_bitable_app_table_record | create | app_token, table_id, fields |
| 批量创建 | feishu_bitable_app_table_record | batch_create | app_token, table_id, records |
| 更新记录 | feishu_bitable_app_table_record | update | app_token, table_id, record_id, fields |
| 批量更新 | feishu_bitable_app_table_record | batch_update | app_token, table_id, records |
| 删除记录 | feishu_bitable_app_table_record | delete | app_token, table_id, record_id |
| 批量删除 | feishu_bitable_app_table_record | batch_delete | app_token, table_id, record_ids |

## Token 提取

从 URL 提取 `app_token` 和 `table_id`：

- **多维表格 URL**: `https://xxx.feishu.cn/base/bascng7vrxcxpig7geggXiCtadY` → `app_token` = `bascng7vrxcxpig7geggXiCtadY`
- **数据表 URL**: `https://xxx.feishu.cn/base/bascng7vrxcxpig7geggXiCtadY?table=tblUa9vcYjWQYJCj` → `app_token` = `bascng7vrxcxpig7geggXiCtadY`, `table_id` = `tblUa9vcYjWQYJCj`

## 字段类型对照表

| type | ui_type | 字段类型 | 写入格式 |
|------|---------|---------|---------|
| 1 | Text | 文本 | `"字符串"` |
| 2 | Number | 数字 | `123` |
| 3 | SingleSelect | 单选 | `"选项名"` |
| 4 | MultiSelect | 多选 | `["选项 1", "选项 2"]` |
| 5 | DateTime | 日期 | `1674206443000` (毫秒时间戳) |
| 6 | Checkbox | 复选框 | `true` 或 `false` |
| 7 | Progress | 进度 | `0.5` (0-1 之间) |
| 11 | User | 人员 | `[{"id": "ou_xxx"}]` |
| 13 | Phone | 电话 | `"13800138000"` |
| 14 | Email | 邮箱 | `"test@example.com"` |
| 15 | Url | 超链接 | `{"link": "https://...", "text": "显示文本"}` |
| 17 | Attachment | 附件 | `[{"file_token": "..."}]` |
| 18 | Location | 地点 | `{"name": "地点名", "address": "地址"}` |
| 19 | GroupChat | 群聊 | `[{"chat_id": "..."}]` |
| 20 | Lookup | 引用 | 只读 |
| 21 | Formula | 公式 | 只读 |
| 22 | Link | 关联 | `[{"record_id": "..."}]` |
| 23 | CreatedTime | 创建时间 | 只读 |
| 24 | ModifiedTime | 修改时间 | 只读 |
| 25 | CreatedUser | 创建人 | 只读 |
| 26 | ModifiedUser | 修改人 | 只读 |

## 字段值格式详解

### 人员字段 (User)
```json
{
  "负责人": [{"id": "ou_73a52625b0df639c12a8ffb0ceeeeb83"}]
}
```
- 必须是数组对象格式
- 只能传 `id` 字段，使用 open_id (ou_...)

### 日期字段 (DateTime)
```json
{
  "截止日期": 1740441600000
}
```
- 必须是**毫秒时间戳**，不是秒
- 不能用字符串格式

### 单选字段 (SingleSelect)
```json
{
  "状态": "进行中"
}
```
- 直接传字符串，不是数组

### 多选字段 (MultiSelect)
```json
{
  "标签": ["重要", "紧急"]
}
```
- 必须是字符串数组

### 超链接字段 (Url)
```json
{
  "文档链接": {"link": "https://example.com", "text": "点击查看"}
}
```
- 必须是对象，包含 `link` 和 `text`

### 附件字段 (Attachment)
```json
{
  "附件": [{"file_token": "boxcnXXX"}]
}
```
- 必须先上传到当前多维表格
- 使用返回的 `file_token`

## 使用示例

### 1. 创建多维表格 + 数据表 + 字段

```json
{
  "action": "create",
  "name": "任务管理表",
  "folder_token": "fldcnXXX"
}
```

创建后，再创建数据表和字段：

```json
{
  "action": "create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "name": "任务列表",
  "fields": [
    {"field_name": "任务名称", "type": 1},
    {"field_name": "负责人", "type": 11},
    {"field_name": "截止日期", "type": 5},
    {"field_name": "状态", "type": 3, "property": {"options": [{"name": "待办"}, {"name": "进行中"}, {"name": "已完成"}]}}
  ]
}
```

### 2. 写入任务记录

```json
{
  "action": "create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "fields": {
    "任务名称": "完成太一镜像 v2.0",
    "负责人": [{"id": "ou_73a52625b0df639c12a8ffb0ceeeeb83"}],
    "截止日期": 1740441600000,
    "状态": "进行中"
  }
}
```

### 3. 批量写入任务/进度

```json
{
  "action": "batch_create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "records": [
    {
      "fields": {
        "任务名称": "TimesFM 集成",
        "状态": "已完成",
        "进度": 1
      }
    },
    {
      "fields": {
        "任务名称": "情景模式小程序",
        "状态": "已完成",
        "进度": 1
      }
    },
    {
      "fields": {
        "任务名称": "Hermes 学习循环",
        "状态": "进行中",
        "进度": 0.8
      }
    }
  ]
}
```

### 4. 查询记录（带筛选）

```json
{
  "action": "list",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "状态",
        "operator": "is",
        "value": ["进行中"]
      }
    ]
  },
  "sort": [
    {"field_name": "截止日期", "desc": false}
  ]
}
```

### 5. 更新记录

```json
{
  "action": "update",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "record_id": "recXXX",
  "fields": {
    "状态": "已完成",
    "进度": 1
  }
}
```

### 6. 双向同步（查询 + 更新）

```json
// 第一步：查询现有记录
{
  "action": "list",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {"field_name": "任务名称", "operator": "is", "value": ["TimesFM 集成"]}
    ]
  }
}

// 第二步：根据查询结果更新或创建
{
  "action": "update",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "record_id": "recXXX",
  "fields": {"进度": 1, "状态": "已完成"}
}
```

## 筛选器 Operator

| operator | 含义 | 支持字段 | value 要求 |
|----------|------|---------|-----------|
| is | 等于 | 所有 | 单个值 |
| isNot | 不等于 | 除日期外 | 单个值 |
| contains | 包含 | 除日期外 | 可多个值 |
| doesNotContain | 不包含 | 除日期外 | 可多个值 |
| isEmpty | 为空 | 所有 | 必须为 `[]` |
| isNotEmpty | 不为空 | 所有 | 必须为 `[]` |
| isGreater | 大于 | 数字、日期 | 单个值 |
| isGreaterEqual | 大于等于 | 数字 | 单个值 |
| isLess | 小于 | 数字、日期 | 单个值 |
| isLessEqual | 小于等于 | 数字 | 单个值 |

**日期字段特殊值**: `["Today"]`, `["Tomorrow"]`, `["ExactDate", "时间戳"]`

## 错误码速查

| 错误码 | 错误现象 | 解决方案 |
|--------|---------|---------|
| 1254064 | DatetimeFieldConvFail | 必须用毫秒时间戳 |
| 1254068 | URLFieldConvFail | 必须用 `{text, link}` 对象 |
| 1254066 | UserFieldConvFail | 必须传 `[{"id": "ou_xxx"}]` |
| 1254015 | Field types do not match | 先 list 字段，按类型构造格式 |
| 1254104 | RecordAddOnceExceedLimit | 分批调用，每批 ≤500 |
| 1254291 | Write conflict | 串行调用 + 延迟 0.5-1 秒 |
| 1254303 | AttachPermNotAllow | 先上传素材到当前表格 |
| 1254045 | FieldNameNotFound | 检查字段名（包括空格、大小写） |

## 限制

| 限制项 | 上限 |
|--------|------|
| 数据表 + 仪表盘 | 100（单个 App） |
| 记录数 | 20,000（单个数据表） |
| 字段数 | 300（单个数据表） |
| 视图数 | 200（单个数据表） |
| 批量创建/更新/删除 | 500（单次 API 调用） |
| 单元格文本 | 10 万字符 |
| 单选/多选选项 | 20,000（单个字段） |
| 单元格附件 | 100 |
| 单元格人员 | 1,000 |

## 最佳实践

### 写入前必读
1. **先获取字段列表** → `feishu_bitable_app_table_field.list` 获取字段 type/ui_type
2. **检查空行** → 新创建的表可能有空记录，先 list + batch_delete 清理
3. **字段值格式** → 严格按照上表格式构造，特别是人员、日期、单选/多选
4. **批量操作** → ≤500 条/批，超过需分批
5. **并发控制** → 同一数据表串行调用，间隔 0.5-1 秒

### 双向同步流程
```
1. list 记录（带 filter 查是否存在）
   ↓
2. 存在 → update 记录
   ↓ 不存在
3. create/batch_create 新记录
   ↓
4. 返回同步结果
```

## 配置

```yaml
channels:
  feishu:
    tools:
      bitable: true  # 默认：false（需手动启用）
```

## 权限

Required: `bitable:app`, `bitable:app:readonly`, `bitable:record:create`, `bitable:record:update`, `bitable:record:delete`
