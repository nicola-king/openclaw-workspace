# 使用场景完整示例

本文档提供 8 个完整的多维表格使用场景示例。

---

## 场景 1：创建任务管理表（一次性定义字段）

**适用**：需求明确，知道需要哪些字段

```json
// 步骤 1：创建多维表格
{
  "action": "create",
  "name": "任务管理表",
  "folder_token": "fldcnXXX"
}

// 返回：{"app_token": "bascng7vrxcxpig7geggXiCtadY"}
```

```json
// 步骤 2：创建数据表（同时定义字段）
{
  "action": "create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "name": "任务列表",
  "fields": [
    {
      "field_name": "任务名称",
      "type": 1
    },
    {
      "field_name": "负责人",
      "type": 11
    },
    {
      "field_name": "截止日期",
      "type": 5
    },
    {
      "field_name": "状态",
      "type": 3,
      "property": {
        "options": [
          {"name": "待办"},
          {"name": "进行中"},
          {"name": "已完成"}
        ]
      }
    },
    {
      "field_name": "进度",
      "type": 7
    },
    {
      "field_name": "优先级",
      "type": 3,
      "property": {
        "options": [
          {"name": "低"},
          {"name": "中"},
          {"name": "高"}
        ]
      }
    }
  ]
}

// 返回：{"table_id": "tblUa9vcYjWQYJCj"}
```

**优点**：减少 API 调用次数，一次性完成

---

## 场景 2：创建任务管理表（探索式）

**适用**：需求不明确，需要逐步调整字段

```json
// 步骤 1：创建多维表格
{
  "action": "create",
  "name": "任务管理表"
}

// 返回：{"app_token": "bascng7vrxcxpig7geggXiCtadY"}
```

```json
// 步骤 2：使用默认表（自动创建的第一个表）
// 先列出数据表获取 table_id
{
  "action": "list",
  "app_token": "bascng7vrxcxpig7geggXiCtadY"
}

// 返回：{"tables": [{"table_id": "tblDefault", "name": "数据表 1"}]}
```

```json
// 步骤 3：逐步添加字段
{
  "action": "create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblDefault",
  "field_name": "任务名称",
  "type": 1
}

{
  "action": "create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblDefault",
  "field_name": "负责人",
  "type": 11
}

// ... 继续添加其他字段
```

**优点**：灵活，可随时调整

---

## 场景 3：批量导入任务数据

```json
{
  "action": "batch_create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "records": [
    {
      "fields": {
        "任务名称": "TimesFM 集成",
        "负责人": [{"id": "ou_73a52625b0df639c12a8ffb0ceeeeb83"}],
        "截止日期": 1740441600000,
        "状态": "已完成",
        "进度": 1,
        "优先级": "高"
      }
    },
    {
      "fields": {
        "任务名称": "情景模式小程序",
        "负责人": [{"id": "ou_73a52625b0df639c12a8ffb0ceeeeb83"}],
        "截止日期": 1740528000000,
        "状态": "已完成",
        "进度": 1,
        "优先级": "高"
      }
    },
    {
      "fields": {
        "任务名称": "Hermes 学习循环",
        "负责人": [{"id": "ou_xxx"}],
        "截止日期": 1740614400000,
        "状态": "进行中",
        "进度": 0.8,
        "优先级": "中"
      }
    },
    {
      "fields": {
        "任务名称": "太一镜像 v2.0",
        "负责人": [{"id": "ou_yyy"}],
        "截止日期": 1740700800000,
        "状态": "进行中",
        "进度": 0.6,
        "优先级": "高"
      }
    },
    {
      "fields": {
        "任务名称": "MarkItDown 集成",
        "负责人": [{"id": "ou_zzz"}],
        "截止日期": 1740787200000,
        "状态": "待办",
        "进度": 0,
        "优先级": "中"
      }
    }
  ]
}
```

**注意**：
- 单次最多 500 条记录
- 超过 500 条需分批调用

---

## 场景 4：筛选查询 + 排序

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
      },
      {
        "field_name": "优先级",
        "operator": "is",
        "value": ["高"]
      },
      {
        "field_name": "截止日期",
        "operator": "isLess",
        "value": ["ExactDate", "1740700800000"]
      }
    ]
  },
  "sort": [
    {
      "field_name": "截止日期",
      "desc": false
    },
    {
      "field_name": "优先级",
      "desc": true
    }
  ],
  "field_names": ["任务名称", "负责人", "截止日期", "状态", "进度"]
}
```

**筛选条件说明**：
- `conjunction`: "and" 或 "or"
- `conditions`: 筛选条件数组
- `operator`: is, isNot, contains, isLess, isGreater 等
- `value`: 筛选值（数组格式）

**日期筛选特殊值**：
- `["Today"]` - 今天
- `["Tomorrow"]` - 明天
- `["ExactDate", "1740700800000"]` - 指定日期

---

## 场景 5：更新任务进度（双向同步）

```json
// 步骤 1：查询现有记录
{
  "action": "list",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "任务名称",
        "operator": "is",
        "value": ["TimesFM 集成"]
      }
    ]
  }
}

// 返回：{"records": [{"record_id": "recXXX", "fields": {...}}]}
```

```json
// 步骤 2：更新记录
{
  "action": "update",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "record_id": "recXXX",
  "fields": {
    "进度": 1,
    "状态": "已完成"
  }
}
```

---

## 场景 6：处理空行（新表清理）

**问题**：新创建的数据表可能包含空记录（空行）

```json
// 步骤 1：列出所有记录
{
  "action": "list",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj"
}

// 返回：{"records": [{"record_id": "recEmpty1", "fields": {}}, ...]}
```

```json
// 步骤 2：删除空行
{
  "action": "batch_delete",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "record_ids": ["recEmpty1", "recEmpty2"]
}
```

```json
// 步骤 3：写入真实数据
{
  "action": "batch_create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "records": [...]
}
```

---

## 场景 7：高级筛选（ isEmpty / isNotEmpty）

```json
{
  "action": "list",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "负责人",
        "operator": "isEmpty",
        "value": []
      },
      {
        "field_name": "截止日期",
        "operator": "isNotEmpty",
        "value": []
      }
    ]
  }
}
```

**注意**：
- `isEmpty` 和 `isNotEmpty` 必须传 `value: []`（空数组）
- 虽然逻辑上不需要值，但 API 要求必须传

---

## 场景 8：处理附件字段

```json
// 步骤 1：上传文件到多维表格
{
  "action": "upload_file",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "file_path": "/tmp/需求文档.pdf",
  "filename": "需求文档.pdf"
}

// 返回：{"file_token": "boxcnXXX"}
```

```json
// 步骤 2：在记录中使用附件
{
  "action": "create",
  "app_token": "bascng7vrxcxpig7geggXiCtadY",
  "table_id": "tblUa9vcYjWQYJCj",
  "fields": {
    "任务名称": "完成需求评审",
    "附件": [
      {"file_token": "boxcnXXX"}
    ]
  }
}
```

---

## 场景 9：并发控制（避免写冲突）

**问题**：同一数据表不支持并发写

**解决**：串行调用 + 延迟

```javascript
// 伪代码示例
const records = [...]; // 1000 条记录

// 分批处理，每批 500 条
for (let i = 0; i < records.length; i += 500) {
  const batch = records.slice(i, i + 500);
  
  await api.batch_create({
    app_token,
    table_id,
    records: batch
  });
  
  // 延迟 0.5-1 秒，避免写冲突
  await sleep(1000);
}
```

---

## 场景 10：错误处理

```javascript
try {
  await api.create({
    app_token,
    table_id,
    fields: {
      "截止日期": "2026-02-27"  // ❌ 错误：字符串
    }
  });
} catch (error) {
  if (error.code === 1254064) {
    // DatetimeFieldConvFail - 日期格式错误
    // 解决：改用毫秒时间戳
    fields["截止日期"] = new Date("2026-02-27").getTime();
  } else if (error.code === 1254066) {
    // UserFieldConvFail - 人员格式错误
    // 解决：改用 [{"id": "ou_xxx"}]
  } else if (error.code === 1254291) {
    // Write conflict - 写冲突
    // 解决：等待后重试
    await sleep(1000);
    await retry();
  }
}
```

---

## 快速参考

### 字段值格式速查

| 字段类型 | 正确格式 | 错误格式 |
|---------|---------|---------|
| 人员 | `[{"id": "ou_xxx"}]` | `"ou_xxx"` |
| 日期 | `1740441600000` | `"2026-02-27"` |
| 单选 | `"进行中"` | `["进行中"]` |
| 多选 | `["重要", "紧急"]` | `"重要"` |
| 超链接 | `{"link": "...", "text": "..."}` | `"https://..."` |
| 附件 | `[{"file_token": "..."}]` | 外部 URL |
| 进度 | `0.75` | `75` |

### 错误码速查

| 错误码 | 含义 | 解决 |
|--------|------|------|
| 1254064 | 日期格式错误 | 用毫秒时间戳 |
| 1254066 | 人员格式错误 | 用 `[{"id": "ou_xxx"}]` |
| 1254068 | 超链接格式错误 | 用 `{link, text}` 对象 |
| 1254015 | 字段类型不匹配 | 先 list 字段 |
| 1254104 | 超过 500 条限制 | 分批调用 |
| 1254291 | 写冲突 | 串行 + 延迟 |
