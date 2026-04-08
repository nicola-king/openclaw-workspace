---
name: google-sheets-integration
version: 1.0.0
description: Google Sheets 集成 - 读取/写入/分析电子表格
category: integration
tags: ['google', 'sheets', 'spreadsheet', 'api', '自动化']
author: 太一 AGI
created: 2026-04-08
updated: 2026-04-08
status: active
priority: P1
---

# Google Sheets 集成技能

> **版本**: 1.0.0 | **创建**: 2026-04-08  
> **负责**: 太一 | **状态**: ✅ 已激活

---

## 🎯 功能

- ✅ 读取电子表格数据
- ✅ 写入/更新数据
- ✅ 创建新表格
- ✅ 追加行数据
- ✅ 获取表格元数据
- ✅ AI 数据分析

---

## 🔧 配置

### 1. 获取 Google API Credentials

1. 访问 https://console.cloud.google.com/
2. 创建新项目或选择现有项目
3. 启用 Google Sheets API
4. 创建服务账号
5. 下载 JSON 密钥文件
6. 保存到 `~/.openclaw/workspace-taiyi/config/google-credentials.json`

### 2. 启用配置

编辑 `~/.openclaw/workspace-taiyi/config/google-integration.json`:

```json
{
  "sheets": {
    "enabled": true,
    "credentialsPath": "~/.openclaw/workspace-taiyi/config/google-credentials.json",
    "spreadsheetId": "",
    "autoSync": true,
    "syncInterval": 900
  }
}
```

---

## 📋 命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `sheets read` | 读取数据 | `sheets read SPREADSHEET_ID "Sheet1!A1:D10"` |
| `sheets write` | 写入数据 | `sheets write SPREADSHEET_ID "Sheet1!A1" '[["Name","Score"],["Alice",95]]'` |
| `sheets append` | 追加行 | `sheets append SPREADSHEET_ID '[["New","Row"]]'` |
| `sheets create` | 创建表格 | `sheets create "Q1 Sales Report"` |
| `sheets info` | 获取元数据 | `sheets info SPREADSHEET_ID` |
| `sheets clear` | 清除范围 | `sheets clear SPREADSHEET_ID "Sheet1!A1:B2"` |
| `sheets analyze` | AI 分析 | `sheets analyze SPREADSHEET_ID` |

---

## 🚀 使用示例

### 读取数据
```bash
太一，读取表格 SPREADSHEET_ID 的 Sheet1!A1:D10
```

### 写入数据
```bash
太一，在表格中写入数据：[["姓名","分数"],["张三",95]]
```

### 创建新表格
```bash
太一，创建一个新表格 "2026 年销售数据"
```

### AI 分析
```bash
太一，分析这个表格的数据趋势
```

---

## 🔗 相关文件

- `skills/browser-automation/google-services-automation.py` - Google 服务自动化
- `workspace-taiyi/config/google-integration.json` - Google 集成配置

---

*创建：2026-04-08 | 太一 AGI*
