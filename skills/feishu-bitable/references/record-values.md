# 记录值数据结构详解

本文档说明每种字段类型在创建/更新记录时，`fields` 参数需要的正确数据格式。

## 核心原则

**最大的坑**：不同字段类型对 value 的数据结构要求完全不同。

**强制流程**：
1. 先调用 `feishu_bitable_app_table_field.list` 获取字段的 `type` 和 `ui_type`
2. 根据下表构造正确格式
3. 错误码 `125406X` 或 `1254015` → 检查字段值格式

---

## 字段值格式对照表

| type | ui_type | 字段类型 | 写入格式 | 示例 | 常见错误 |
|------|---------|---------|---------|------|---------|
| 1 | Text | 文本 | 字符串 | `"任务名称"` | ❌ 无 |
| 2 | Number | 数字 | 数字 | `123` 或 `3.14` | ❌ 传字符串 `"123"` |
| 3 | SingleSelect | 单选 | 字符串 | `"进行中"` | ❌ 传数组 `["进行中"]` |
| 4 | MultiSelect | 多选 | 字符串数组 | `["重要", "紧急"]` | ❌ 传字符串 `"重要"` |
| 5 | DateTime | 日期 | 毫秒时间戳 | `1740441600000` | ❌ 秒时间戳/字符串 |
| 6 | Checkbox | 复选框 | 布尔值 | `true` 或 `false` | ❌ 传字符串 `"true"` |
| 7 | Progress | 进度 | 数字 (0-1) | `0.75` | ❌ 传百分比 `75` |
| 11 | User | 人员 | 对象数组 | `[{"id": "ou_xxx"}]` | ❌ 传字符串/传 name |
| 13 | Phone | 电话 | 字符串 | `"13800138000"` | ❌ 无 |
| 14 | Email | 邮箱 | 字符串 | `"test@example.com"` | ❌ 无 |
| 15 | Url | 超链接 | 对象 | `{"link": "...", "text": "..."}` | ❌ 只传 URL 字符串 |
| 17 | Attachment | 附件 | 对象数组 | `[{"file_token": "..."}]` | ❌ 传外部 URL |
| 18 | Location | 地点 | 对象 | `{"name": "...", "address": "..."}` | ❌ 只传字符串 |
| 19 | GroupChat | 群聊 | 对象数组 | `[{"chat_id": "..."}]` | ❌ 传字符串 |
| 22 | Link | 关联 | 对象数组 | `[{"record_id": "..."}]` | ❌ 传字符串 |

**只读字段**（不可写入）：
- type 20: Lookup（引用）
- type 21: Formula（公式）
- type 23: CreatedTime（创建时间）
- type 24: ModifiedTime（修改时间）
- type 25: CreatedUser（创建人）
- type 26: ModifiedUser（修改人）

---

## 详细格式说明

### 1. 人员字段 (User, type=11)

```json
{
  "负责人": [{"id": "ou_73a52625b0df639c12a8ffb0ceeeeb83"}],
  "参与人": [
    {"id": "ou_xxx"},
    {"id": "ou_yyy"}
  ]
}
```

**注意**：
- 必须是数组对象格式 `[{"id": "..."}]`
- 只能传 `id` 字段，使用 open_id (ou_...)
- 不能传 `name`、`email`、`user_id` 等其他字段
- 单个人员也要用数组：`[{"id": "ou_xxx"}]`

---

### 2. 日期字段 (DateTime, type=5)

```json
{
  "截止日期": 1740441600000,
  "开始日期": 1709251200000
}
```

**注意**：
- 必须是**毫秒时间戳**（13 位）
- 不能用秒时间戳（10 位）
- 不能用字符串格式（"2026-02-27"、"2026-02-27T10:00:00Z"）

**转换示例**（JavaScript）：
```javascript
// 正确
const timestamp = new Date("2026-02-27").getTime(); // 1740614400000

// 错误 ❌
const timestamp = Date.now() / 1000; // 秒时间戳
const timestamp = "2026-02-27"; // 字符串
```

---

### 3. 单选字段 (SingleSelect, type=3)

```json
{
  "状态": "进行中",
  "优先级": "高"
}
```

**注意**：
- 直接传字符串，**不是数组**
- 如果选项不存在，会自动创建新选项
- 选项名称必须完全匹配（包括空格、大小写）

**错误示例** ❌：
```json
{
  "状态": ["进行中"]  // ❌ 不能用数组
}
```

---

### 4. 多选字段 (MultiSelect, type=4)

```json
{
  "标签": ["重要", "紧急", "高优先级"],
  "技能": ["Python", "JavaScript"]
}
```

**注意**：
- 必须是字符串数组
- 单个选项也要用数组：`["选项 1"]`
- 如果选项不存在，会自动创建新选项

**错误示例** ❌：
```json
{
  "标签": "重要"  // ❌ 不能用字符串
}
```

---

### 5. 超链接字段 (Url, type=15)

```json
{
  "文档链接": {"link": "https://example.com", "text": "点击查看文档"},
  "官网": {"link": "https://company.com", "text": "公司官网"}
}
```

**注意**：
- 必须是对象，包含 `link` 和 `text` 两个字段
- `text` 是显示文本，可以省略（默认显示 URL）

**错误示例** ❌：
```json
{
  "文档链接": "https://example.com"  // ❌ 不能只传 URL 字符串
}
```

---

### 6. 附件字段 (Attachment, type=17)

```json
{
  "附件": [
    {"file_token": "boxcnXXX"},
    {"file_token": "boxcnYYY"}
  ]
}
```

**注意**：
- 必须先上传文件到当前多维表格
- 使用上传接口返回的 `file_token`
- 不能直接使用外部 URL 或本地路径

**上传流程**：
1. 调用附件上传接口（需要 file 参数）
2. 获取返回的 `file_token`
3. 在记录中使用 `{"file_token": "..."}`

---

### 7. 进度字段 (Progress, type=7)

```json
{
  "进度": 0.75,
  "完成率": 0.5
}
```

**注意**：
- 必须是 0-1 之间的数字
- 0 = 0%，1 = 100%
- 不能用百分比（75、50）

**错误示例** ❌：
```json
{
  "进度": 75  // ❌ 应该是 0.75
}
```

---

### 8. 地点字段 (Location, type=18)

```json
{
  "会议地点": {"name": "会议室 A", "address": "北京市朝阳区 xxx 路 xxx 号"}
}
```

**注意**：
- 必须是对象，包含 `name` 和 `address`
- `name` 是地点名称，`address` 是详细地址

---

### 9. 关联字段 (Link, type=22)

```json
{
  "关联任务": [
    {"record_id": "recXXX"},
    {"record_id": "recYYY"}
  ]
}
```

**注意**：
- 必须是对象数组
- 只能传 `record_id`
- 关联的记录必须在同一个多维表格的其他数据表中

---

## 完整示例

### 示例 1：任务管理

```json
{
  "action": "create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "fields": {
    "任务名称": "完成太一镜像 v2.0",
    "负责人": [{"id": "ou_73a52625b0df639c12a8ffb0ceeeeb83"}],
    "参与人": [
      {"id": "ou_xxx"},
      {"id": "ou_yyy"}
    ],
    "开始日期": 1709251200000,
    "截止日期": 1740441600000,
    "状态": "进行中",
    "优先级": "高",
    "标签": ["重要", "紧急"],
    "进度": 0.75,
    "文档链接": {"link": "https://example.com", "text": "需求文档"},
    "是否阻塞": true
  }
}
```

### 示例 2：客户管理

```json
{
  "action": "batch_create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "records": [
    {
      "fields": {
        "客户名称": "字节跳动",
        "联系人": "张三",
        "电话": "13800138000",
        "邮箱": "zhangsan@bytedance.com",
        "负责人": [{"id": "ou_xxx"}],
        "签约日期": 1740441600000,
        "合同金额": 500000,
        "状态": "已签约",
        "行业": ["互联网", "科技"]
      }
    },
    {
      "fields": {
        "客户名称": "飞书",
        "联系人": "李四",
        "电话": "13900139000",
        "邮箱": "lisi@feishu.cn",
        "负责人": [{"id": "ou_yyy"}],
        "签约日期": 1741046400000,
        "合同金额": 300000,
        "状态": "谈判中",
        "行业": ["SaaS", "企业服务"]
      }
    }
  ]
}
```

---

## 错误排查

### 错误码 1254064: DatetimeFieldConvFail

**原因**：日期字段格式错误

**解决**：
- 检查是否是毫秒时间戳（13 位）
- 不能用字符串或秒时间戳

```javascript
// 正确
const timestamp = new Date("2026-02-27").getTime(); // 1740614400000

// 错误 ❌
const timestamp = "2026-02-27";
const timestamp = Math.floor(Date.now() / 1000); // 秒
```

---

### 错误码 1254066: UserFieldConvFail

**原因**：人员字段格式错误

**解决**：
- 必须是 `[{"id": "ou_xxx"}]` 格式
- 确认使用 open_id（ou_开头）

```json
// 正确
{"负责人": [{"id": "ou_73a52625b0df639c12a8ffb0ceeeeb83"}]}

// 错误 ❌
{"负责人": "ou_73a52625b0df639c12a8ffb0ceeeeb83"}
{"负责人": [{"name": "张三"}]}
```

---

### 错误码 1254068: URLFieldConvFail

**原因**：超链接字段格式错误

**解决**：
- 必须是 `{"link": "...", "text": "..."}` 对象

```json
// 正确
{"文档链接": {"link": "https://example.com", "text": "点击查看"}}

// 错误 ❌
{"文档链接": "https://example.com"}
```

---

### 错误码 1254015: Field types do not match

**原因**：字段值格式与类型不匹配

**解决**：
1. 先调用 `field.list` 获取字段类型
2. 根据类型构造正确格式
3. 检查单选/多选、人员、日期等易错字段
